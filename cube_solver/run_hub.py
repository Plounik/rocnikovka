"""Compile a project and include precompiled native MPY modules explicitly.

The stock pybricksdev compiler currently skips native .mpy dependencies with
ABI 6, so this script builds the documented multi-module wire format itself.
"""
import argparse,asyncio,struct,sys,ast
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
sys.path.insert(0,str(ROOT))
from pybricksdev.compile import compile_file

async def bundle(program):
    # Discover local robot/scanner dependencies without bundling the desktop
    # branch of solver.py. Native modules are appended explicitly below.
    modules=[('__main__',program)]
    seen={'__main__'}
    search_roots=(ROOT.parent,program.parent,ROOT)
    for _,source in modules:
        tree=ast.parse(source.read_text(encoding='utf-8-sig'))
        names=[]
        for node in ast.walk(tree):
            if isinstance(node,ast.Import): names.extend(alias.name for alias in node.names)
            elif isinstance(node,ast.ImportFrom) and node.level==0 and node.module:
                names.append(node.module)
        for name in names:
            if name in seen or name in ('_solver','cube_solver.desktop_backend'):
                continue
            relative=Path(*name.split('.')).with_suffix('.py')
            path=next((base/relative for base in search_roots if (base/relative).is_file()),None)
            if path is not None:
                seen.add(name); modules.append((name,path))
    if 'solver' not in seen:
        seen.add('solver'); modules.append(('solver',ROOT.parent/'solver.py'))
    payload=bytearray(); sizes={}
    for name,path in modules:
        code=await compile_file(str(path.parent),path.name,6)
        sizes[name]=len(code); payload+=struct.pack('<I',len(code))+name.encode()+b'\0'+code
    native=(ROOT/'_solver.mpy').read_bytes()
    if native[:4]!=bytes((0x4d,6,0x17,31)):
        raise RuntimeError('Expected ARMv7-M MPY ABI 6.3 module')
    sizes['_solver']=len(native)
    payload+=struct.pack('<I',len(native))+b'_solver\0'+native
    # 4.0.1 uses 256 KiB writable storage divided across 5 slots minus metadata.
    if len(payload)>52000: raise RuntimeError('Bundle exceeds conservative 4.0.1 slot budget')
    return bytes(payload),sizes

async def main(args):
    program=Path(args.program)
    if not program.is_absolute(): program=ROOT/program
    data,sizes=await bundle(program)
    print('Bundle:',len(data),'bytes; modules:',sizes)
    if args.build_only: return
    from pybricksdev.ble import find_device
    from pybricksdev.connections.pybricks import PybricksHubBLE
    from pybricksdev.connections import ConnectionState
    from pybricksdev.ble.lwp3 import HubKind
    device=await find_device(name=args.name,timeout=10)
    hub=PybricksHubBLE(device)
    try:
        await hub.connect()
        print('Connected:',device.name,'firmware:',hub.fw_version)
        if hub.hub_kind!=HubKind.TECHNIC_LARGE:
            raise RuntimeError('This build requires a SPIKE Prime / Robot Inventor hub')
        if str(hub.fw_version) not in ('4.0.0','4.0.1'):
            raise RuntimeError('Native module was built against Pybricks 4.0.1; verify ABI before using another firmware')
        await hub.download_user_program(data)
        if args.download_only:
            print('Saved in the selected hub program slot. Run it with the hub buttons.')
        else:
            await hub.run(None,wait=True,print_output=True)
        lines=[x.decode('utf-8',errors='replace') if isinstance(x,(bytes,bytearray)) else str(x) for x in hub.output]
        if args.log:
            log=Path(args.log)
            log.write_text('\n'.join(lines)+'\n')
            print('Saved output:',log)
        if any('Traceback (most recent call last):' in line for line in lines):
            raise RuntimeError('The hub program failed. See the printed traceback'+(' and '+str(args.log) if args.log else ''))
        if args.stay_connected and not args.download_only:
            print('Connected. Press the hub button to run again; Ctrl+C disconnects.',flush=True)
            await asyncio.Future()
    finally:
        if hub.connection_state_observable.value==ConnectionState.CONNECTED:
            await hub.disconnect()

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--program',default=str(ROOT.parent/'main.py')); p.add_argument('--name',default=None)
    p.add_argument('--build-only',action='store_true'); p.add_argument('--download-only',action='store_true')
    p.add_argument('--log',default=None)
    p.add_argument('--stay-connected',action='store_true')
    args=p.parse_args()
    try: asyncio.run(main(args))
    except asyncio.TimeoutError: raise SystemExit('No Pybricks hub found. Turn it on and disconnect other apps.')
