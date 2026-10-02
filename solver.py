"""Standalone SPIKE Prime solver. Standard URFDLB facelets -> Singmaster moves.

Search tables/decoder: David Gilday, PrimeCuber v1p5 (non-commercial).
Use solve() for a string or solve_detailed() for measured search metadata.
"""
import sys
# Pybricks disables attribute tuples, so implementation is a plain tuple.
_implementation_name = (sys.implementation[0] if isinstance(sys.implementation, tuple)
                        else sys.implementation.name)
if _implementation_name == "micropython":
    import _solver as _native  # pyright: ignore[reportMissingModuleSource]
    from pybricks.tools import StopWatch, wait
    def _clock():
        watch=StopWatch()
        return watch.time
else:
    import ctypes
    from pathlib import Path
    class Backend:
        def __init__(self):
            dll=Path(__file__).parent/"cube_solver"/"solver.dll"
            self.lib=ctypes.CDLL(str(dll))
            for name in ("search_init","search_best"):
                getattr(self.lib,name).argtypes=[ctypes.c_void_p,ctypes.c_void_p]
            self.lib.search_batch.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int]
            for name in ("search_candidates","search_depth","search_exhausted"):
                getattr(self.lib,name).argtypes=[ctypes.c_void_p]
        def start(self,state):
            ctx=ctypes.create_string_buffer(self.lib.search_size())
            self.lib.search_init(ctx,bytes(state))
            return ctx
        def step(self,ctx,count,target,depth):
            return self.lib.search_batch(ctx,count,target,depth)
        def best(self,ctx):
            out=ctypes.create_string_buffer(128)
            n=self.lib.search_best(ctx,out)
            return out.raw[:n] if n<128 else b""
        def stats(self,ctx):
            out=ctypes.create_string_buffer(128)
            n=self.lib.search_best(ctx,out)
            return n,self.lib.search_candidates(ctx),self.lib.search_depth(ctx),self.lib.search_exhausted(ctx)
    _native=Backend()
    from time import monotonic
    def _clock():
        start=monotonic()
        return lambda: int((monotonic()-start)*1000)
    def wait(ms):
        pass

SOLVED="UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
# Leave 100 ms for the final native batch, validation, and result formatting
# within the requested 30-second wall-time budget on the measured hub.
_DEFAULT_TIME_LIMIT_MS=29900
_CF=((8,9,20),(6,18,38),(0,36,47),(2,45,11),(29,26,15),(27,44,24),(33,53,42),(35,17,51))
_CC=("URF","UFL","ULB","UBR","DFR","DLF","DBL","DRB")
_EF=((5,10),(7,19),(3,37),(1,46),(32,16),(28,25),(30,43),(34,52),(23,12),(21,41),(50,39),(48,14))
_EC=("UR","UF","UL","UB","DR","DF","DL","DB","FR","FL","BL","BR")
_FACES="FRBLUD"
_RINGS=((6,3,0,1,2,5,8,7),)*4+((8,7,6,3,0,1,2,5),(0,1,2,5,8,7,6,3))
_OFFSETS=(18,9,45,36,0,27)

def _parity(p):
    n=0
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]: n^=1
    return n

def validate(facelets):
    """Reject malformed and physically impossible scans before native code."""
    if not isinstance(facelets,str) or len(facelets)!=54:
        raise ValueError("Expected exactly 54 facelets in URFDLB order")
    for color in "URFDLB":
        if facelets.count(color)!=9:
            raise ValueError("Expected nine stickers of each U,R,F,D,L,B")
    for i,color in enumerate("URFDLB"):
        if facelets[9*i+4]!=color:
            raise ValueError("Center stickers must be U,R,F,D,L,B")
    cp=[]; co=0
    for indices in _CF:
        colors="".join(facelets[i] for i in indices)
        ori=0
        while ori<3 and colors[ori] not in "UD": ori+=1
        if ori==3: raise ValueError("Invalid corner colors")
        rotated=colors[ori:]+colors[:ori]
        if rotated not in _CC: raise ValueError("Invalid or mirrored corner")
        cp.append(_CC.index(rotated)); co+=ori
    ep=[]; eo=0
    for a,b in _EF:
        colors=facelets[a]+facelets[b]
        if colors in _EC: ep.append(_EC.index(colors))
        elif colors[1]+colors[0] in _EC:
            ep.append(_EC.index(colors[1]+colors[0])); eo+=1
        else: raise ValueError("Invalid edge colors")
    if len(set(cp))!=8 or len(set(ep))!=12:
        raise ValueError("Duplicate or missing cubie")
    if co%3: raise ValueError("Impossible cube: corner twist")
    if eo%2: raise ValueError("Impossible cube: edge flip")
    if _parity(cp)!=_parity(ep): raise ValueError("Impossible cube: permutation parity")
    return True

def _ring_state(facelets):
    out=bytearray(48)
    for f in range(6):
        for j in range(8): out[f*8+j]=_FACES.index(facelets[_OFFSETS[f]+_RINGS[f][j]])
    return out

def _moves(data):
    return " ".join(_FACES[m//3]+("","2","'")[m%3] for m in data)

def solve_detailed(facelets,target=30,time_limit_ms=_DEFAULT_TIME_LIMIT_MS,max_depth=4,max_candidates=500000,batch_size=32):
    """Return the best valid solution within explicit search limits.

    target is a stopping target, not a guarantee. Half turns count as one.
    time_limit_ms=0 evaluates one initial candidate. At least one complete
    candidate is evaluated even when the time limit expires during setup.
    Deadline overshoot is bounded by one batch; batch_size=1 is tightest.
    """
    validate(facelets)
    for name,value in (("target",target),("time_limit_ms",time_limit_ms),("max_depth",max_depth),("max_candidates",max_candidates),("batch_size",batch_size)):
        if not isinstance(value,int): raise ValueError(name+" must be an integer")
    if not 0<=target<=127 or not 0<=time_limit_ms<=3600000 or not 0<=max_depth<=4 or not 1<=max_candidates<=10000000 or not 1<=batch_size<=1024:
        raise ValueError("Search limit outside supported range")
    clock=_clock()
    if facelets==SOLVED:
        return {"moves":"","length":0,"elapsed_ms":clock(),"candidates":0,"target_met":True,"reason":"solved","depth":0}
    ctx=_native.start(_ring_state(facelets))
    _native.step(ctx,1,target,max_depth)
    reason="time_limit"
    while True:
        n,count,depth,exhausted=_native.stats(ctx)
        if n<=target: reason="target"; break
        if exhausted: reason="depth_limit"; break
        if count>=max_candidates: reason="candidate_limit"; break
        if clock()>=time_limit_ms: break
        _native.step(ctx,min(batch_size,max_candidates-count),target,max_depth)
        wait(0)
    data=_native.best(ctx)
    if n==128: raise RuntimeError("No valid solution found")
    return {"moves":_moves(data),"length":n,"elapsed_ms":clock(),"candidates":count,"target_met":n<=target,"reason":reason,"depth":depth}

def solve(facelets,target=30,time_limit_ms=_DEFAULT_TIME_LIMIT_MS,max_depth=4,max_candidates=500000):
    """Return a space-separated move string, e.g. R U2 F'."""
    return solve_detailed(facelets,target,time_limit_ms,max_depth,max_candidates)["moves"]
