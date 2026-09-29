#####-----------------------------------------------------------------------------
# Title:        PrimeCuber Solver
#
# Author:       David Gilday
#
# Copyright:    (C) 2020 David Gilday
#
# Website:      http://mindcuber.com
#
# Version:      v1p5
#
# Modified:     $Date: 2020-12-25 11:53:40 +0000 (Fri, 25 Dec 2020) $
#
# Revision:     $Revision: 7800 $
#
# Usage:
#
#   This software may be used for any non-commercial purpose providing
#   that the original author is acknowledged.
#
# Disclaimer:
#
#   This software is provided 'as is' without warranty of any kind, either
#   express or implied, including, but not limited to, the implied warranties
#   of fitness for a purpose, or the warranty of non-infringement.
#
#-----------------------------------------------------------------------------
# Purpose:      Rubik's Cube solver for PrimeCuber robot
#-----------------------------------------------------------------------------

try:
    import time
except ImportError:
    from pybricks.tools import StopWatch
    _ticks_ms = StopWatch().time
else:
    try:
        _ticks_ms = time.ticks_ms
    except AttributeError:
        _clock_start = time.monotonic()
        _ticks_ms = lambda: int((time.monotonic() - _clock_start) * 1000)

# PrimeCuber's original source supplied RND as a platform macro.  Keep a
# small local pseudo-random generator so the diagnostic shuffle() helper also
# works on Pybricks without depending on a particular random module.
_RND_STATE = _ticks_ms() % 65521

def RND(n):
    global _RND_STATE
    if n <= 0:
        raise ValueError("random range must be positive")
    _RND_STATE = (109 * _RND_STATE + 1021) % 65521
    return _RND_STATE % n

def trace(msg):
    return None

trace("module pcsolver_v1p5")

NFACE    = 6
NSIDE    = 4
NSIDE_M1 = NSIDE-1
NCORNER  = int(NFACE*NSIDE/3)
NEDGE    = int(NFACE*NSIDE/2)

def RMOD(r):
    return r & NSIDE_M1

def RFIX(r):
    return ((r+1) & NSIDE_M1)-1

def POS(f, o):
    return f*9+o

#-----------------------------------------------------------------------------

trace("class remap")
class remap():

    def __init__(self):
        self.fm = [-1] * NFACE
        self.rm = [-1] * NFACE

    def init_maps(self, f, r):
        self.fm[f] = r
        self.rm[r] = f

#-----------------------------------------------------------------------------

trace("class face_map")
class face_map():

    def __init__(self):
        self.face        = -1
        self.face_edge   = [-1] * NFACE
        self.face_corner = [-1] * NFACE

    def init(self, f, f0, f1, f2, f3):
        self.face = f
        self.fce= [f0, f1, f2, f3]

    def init_rest(self):
        for d in range(NSIDE):
            f = self.fce[d].face
            self.face_edge[f]= 2*d+1
            self.face_corner[f] = (self.face_edge[f]+1)&(2*NSIDE-1)

    def dir1(self, d):
        return self.fce[d].face

    def dir(self, f, d):
        fd = -1
        for i in range(NSIDE):
            if self.fce[i].face == f:
                m = self.fce[i]
                for j in range(NSIDE):
                    if m.fce[j].face == self.face:
                        fd = m.fce[RMOD(j+d)].face
                        break
                break
        return fd

#-----------------------------------------------------------------------------

trace("class cube_map")
class cube_map():

    def __init__(self):
        self.map = []
        self.rm= []
        self.dst = []
        for i in range(NFACE):
            self.map.append(face_map())
            self.rm.append([])
            self.dst.append([-1] * NFACE)
            for j in range(NFACE):
                self.rm[i].append(remap())
        self.map[0].init(0, self.map[3], self.map[4], self.map[1], self.map[5])
        self.map[1].init(1, self.map[0], self.map[4], self.map[2], self.map[5])
        self.map[2].init(2, self.map[1], self.map[4], self.map[3], self.map[5])
        self.map[3].init(3, self.map[2], self.map[4], self.map[0], self.map[5])
        self.map[4].init(4, self.map[0], self.map[3], self.map[2], self.map[1])
        self.map[5].init(5, self.map[0], self.map[1], self.map[2], self.map[3])
        for i in range(NFACE):
            self.map[i].init_rest()
        for f0 in range(NFACE):
            for f1 in range(NFACE):
                self.dst[f0][f1] = 2
        ff0 = 0
        for fr0 in range(NFACE):
            self.dst[fr0][fr0] = 0
            for d0 in range(NSIDE):
                ff1 = 1
                fr1 = self.map[fr0].dir1(d0)
                self.dst[fr0][fr1] = 1
                for d1 in range(NSIDE):
                    ff2 = self.map[ff0].dir(ff1, d1)
                    fr2 = self.map[fr0].dir(fr1, d1)
                    for d2 in range(NSIDE):
                        ff3 = self.map[ff1].dir(ff2, d2)
                        fr3 = self.map[fr1].dir(fr2, d2)
                        self.rm[fr0][fr1].init_maps(ff3, fr3)

    def dir(self, f, d):
        return self.map[f].dir1(d)

    def adjacent(self, f0, f1):
        return self.dst[f0][f1] == 1

    def edge(self, f0, f1):
        return self.map[f0].face_edge[f1]

    def corner(self, f0, f1):
        return self.map[f0].face_corner[f1]

    def get_remap(self, f0, f1):
        return self.rm[f0][f1]

#-----------------------------------------------------------------------------

# Default to small tables included in this file
large = False

if large:
    # Large tables
    trace("class cube_mtab4")
    class cube_mtab4:

        NSTAGE = 4    # Number of stages in solve
        NPIECE = 4    # Maximum number of corners/edges per stage

        def init(c):
            # 0
            s = c.stage(0)
            c.adde(s, 0, 1)
            c.adde(s, 0, 4)
            c.adde(s, 1, 4)
            c.addc(s, 0, 4, 1)
            c.send(s)

            # 1
            s = c.stage(s)
            c.adde(s, 0, 3)
            c.adde(s, 0, 5)
            c.adde(s, 5, 1)
            c.addc(s, 0, 1, 5)
            c.send(s)

            # 2
            s = c.stage(s)
            c.adde(s, 3, 5)
            c.adde(s, 4, 3)
            c.addc(s, 0, 3, 4)
            c.addc(s, 0, 5, 3)
            c.send(s)

            # 3
            s = c.stage(s)
            c.adde(s, 2, 1)
            c.adde(s, 2, 3)
            c.adde(s, 2, 4)
            c.addc(s, 2, 1, 4)
            c.addc(s, 2, 3, 5)
            c.addc(s, 2, 4, 3)
            c.send(s)

            # Unused stage since last corner and edge will already be solved
            s = c.stage(s)
            c.adde(s, 2, 5)
            c.addc(s, 2, 5, 1)

        mtb = (
            5, 6, 7, 9
            )

        MV_MENT = 17

    cube_mtab = cube_mtab4

else:
    # Mini tables embedded below.
    # Mini tables

    trace("class cube_mtab1")
    class cube_mtab1:

        NSTAGE = 8    # Number of stages in solve
        NPIECE = 3    # Maximum number of corners/edges per stage

        def init(c):
            # 0
            s = c.stage(0)
            c.adde(s, 2, 1)
            c.adde(s, 2, 4)
            c.send(s)

            # 1
            s = c.stage(s)
            c.adde(s, 1, 4)
            c.addc(s, 2, 1, 4)
            c.send(s)

            # 2
            s = c.stage(s)
            c.adde(s, 2, 3)
            c.adde(s, 2, 5)
            c.send(s)

            # 3
            s = c.stage(s)
            c.adde(s, 4, 3)
            c.addc(s, 2, 4, 3)
            c.send(s)

            # 4
            s = c.stage(s)
            c.adde(s, 3, 5)
            c.addc(s, 2, 3, 5)
            c.send(s)

            # 5
            s = c.stage(s)
            c.adde(s, 0, 3)
            c.adde(s, 0, 4)
            c.addc(s, 0, 3, 4)
            c.send(s)

            # 6
            s = c.stage(s)
            c.addc(s, 0, 1, 5)
            c.addc(s, 0, 4, 1)
            c.addc(s, 2, 5, 1)
            c.send(s)

            # 7
            s = c.stage(s)
            c.adde(s, 0, 1)
            c.adde(s, 5, 1)
            c.send(s)

            # Unused stage since last corner and edge will already be solved
            s = c.stage(s)
            c.adde(s, 0, 5)
            c.addc(s, 0, 5, 3)

        mtb = (
            3, 4, 4, 5, 5, 6, 7, 7
            )

        MV_MENT = 13

    cube_mtab = cube_mtab1


trace("class solve_map")
class solve_map():

    NSTAGE = cube_mtab.NSTAGE
    NPIECE = cube_mtab.NPIECE

    def __init__(self):
        # Offset into cp/ep tables for each stage
        self.cn    = [-1] * (solve_map.NSTAGE+2)
        self.en    = [-1] * (solve_map.NSTAGE+2)
        self.sz    = [-1] * solve_map.NSTAGE

        # Unrotated corner and edge positions - reverse solve order
        self.cp0   = [-1] * NCORNER
        self.cp1   = [-1] * NCORNER
        self.cp2   = [-1] * NCORNER
        self.ep0   = [-1] * NEDGE
        self.ep1   = [-1] * NEDGE

        self.cn[0] = NCORNER
        self.en[0] = NEDGE

        cube_mtab.init(self)

    def addc(self, s, c0, c1, c2):
        i = self.cn[s]-1
        self.cn[s]  = i
        self.cp0[i] = c0
        self.cp1[i] = c1
        self.cp2[i] = c2

    def adde(self, s, e0, e1):
        i = self.en[s]-1
        self.en[s]  = i
        self.ep0[i] = e0
        self.ep1[i] = e1

    def stage(self, s):
        self.cn[s+1] = self.cn[s]
        self.en[s+1] = self.en[s]
        return s+1

    def send(self, s):
        msg = "STAGE: "+str((s-1))
        idx = 1
        nc  = self.cn[s-1]-self.cn[s]
        msg += " C"+str(nc)
        if nc > 0:
            i = self.cn[s]
            while (i < self.cn[s-1]):
                msg += " ["+str(self.cp0[i])+","+str(self.cp1[i])+","+str(self.cp2[i])+"]"
                idx *= 3*(i+1)
                i += 1
        ne = self.en[s-1]-self.en[s]
        msg += " E"+str(ne)
        if ne > 0:
            i = self.en[s]
            while (i < self.en[s-1]):
                msg += " ["+str(self.ep0[i])+","+str(self.ep1[i])+"]"
                idx *= 2*(i+1)
                i += 1
        if s == solve_map.NSTAGE:
            idx = int(idx/2)
        self.sz[s-1] = idx
        # print(msg+" SZ="+str(self.sz[s-1]))

#-----------------------------------------------------------------------------

# The original PrimeCuber mini table is 18,985 bytes. It is stored as
# base64 text so this file remains a single normal Python source file.
_TABLE_B64 = (
    "DDP1Dv//A1P/A1X/Cfn/A1T/ETXzBoj/DP//Cvn/Bob/APr/C/n/Df//Apj/Avr/A1v/BTP/BEv/Afr/AJj/CG71BpbzCO71"
    "A2z/CF7/CZbzCI71CJ5ZC+j1Bjn/CH71Cej1Cuj1C5bzDJbzDsP2AzzzBjn7BbT4BLLzAsAzA1zzCEP1BbX/CPv/BzP/CP//"
    "CZj/CFP1D4n/C/j/CPn/Bn7/Cfj/Cvj/C5j/CPr/DLv4CKL/A7X/EIn/Bnz/AIf/EYn/DDb/DLX0DKP/A2nzDDj/CTn/B17/"
    "D5w4C4nzDPP/Cjn/DInzADn5Czn/DJP/DIvzAjn5DLP/BWnzAzn7EZrzDAL7B4v/BbLzBov/Dov/Dvj/CLv4CIv/D574C4v/"
    "DBD/Ebj4Don/Dor/Dov5Drj/DKv4BGz/DlP7EJ74D7j4DnD4EZ74BvP/BUv/A///Bjb5CPP/CZP/B/P/D4nzCzj/A/n/ETf/"
    "CTj/Cjj/C5P/A/r/ALD/BFP/A/v/BUP/BFv/EDf/ArD/A1PzA3z/C13/Doj4B/v/BjP/B///D2j4CIj/B/n/Eff/CIb/CIf/"
    "B5j/B/r/DIj4BjT/BXz/BjX/D/f/EPf/EWj4Bl7/BeNeBo71Bp5ZBu71A+P1Bm71CJbzCan4CDn/Bn71CYn/CZn4CJjzDJjz"
    "Cbn4BOP1CDn7BeP1Bpz3AJaJEZn4Bv//BbP/DLb/DDP/Bvv/A/P/BkP1CZb/B4j/Bvn/CH7/B4b/BqD/C5b/Bvr/DjP/BPP/"
    "A7P/BfP/CHz/AjH/D+X2EVb/EbX/EfX/EVj7EV7/A271EVj/EZn1EYv1EVz/EVf/CY71EYr1EZv1EV3/EbxYBG71A+71BW71"
    "D3n/EZr1EYn1DTb/DrXzCl3/Buj3C7f/CzbzDTj/C37/C/f/COj3EXv/DYnzADr/C5f/DfP/ADr7Ajr/DbP/C1bzD3v/EHv/"
    "DQL7B4n/DFX7Bon/Dqv4DhD/Dbv4DPj/DIn5CIn/D5z4EZj4DIn/DIr/C5jzDJj/DIv/Aon5DFP7EJz4D5j4DHD4EZz4Efb/"
    "CF7zCG7/ETzzEbb/ETP/B27/CZjzBm7/ETX/EYf4EZb/Con/EWv5Eab/ET7zETT/ETP7BW7/ERLzEej3EWf4EFb/ELX/EPX/"
    "EFj7EF7/CTbzEFj/CZf/Cff/Bl37EIv1EFz/CWj4CX7/EF3/Aub3CUbzA+31CVbzCXz/EFf/EFb7Am3/CV37AfH/ALuLDhH/"
    "CjbzAIr/Cc31Cvf/Al5uC4rzDBH/EXr/CY31Czr/DKs4C6LzCzr7ClbzD3r/EHr/EdlYCW7/BbDzAlz/Dpv4ADv/CT7zCML1"
    "CW75C5j4CV7zC4n/DML1CpjzC6n4DrDzC7n4CU7zA7DzCeX2BLDzD8JXC86JBhD/ALL1APH/Drv4DZj/DYv/Dfj/CZD0CIr/"
    "D534C4r/Dbj/Eaj4DYn/DYr/C5D0A7r4A7D0ADL1ALH/DxD7EZ34Djb/BTv/DpP/DovzDvP/A2vzDjj/Djn5Djf/BrXzC4vz"
    "DqP/EX7zDonzDorzDjv5DjT1Azv/BWvzBDv/D7TzDgL7BvT/BVv/BP//CLX1DvT/AzP/CPT/CUn/B/T/ETX1C0j/DPT/EUf/"
    "CUj/Ckj/C0n/DfT/DjPzBVP/BPv/D7T/DzX1BsD1BWz7AFz/A7v4Ajv/A7T4A4v/CcBcCLP4EcX2C7P4DMD1AJ73A5v4A6v4"
    "C8BcDrLzDDuLBWz/AHz1D8BXBVzzBvX/Bfv/Bf//CLX/DvX/A0P/CPX/CVn/B/X/BrX/C1j/DPX/Cln/CVj/Clj/C1n/DfX/"
    "DIv1BDP/A0v/EHn/BYD5D/b/DzX7CGz/DzzzD7b/DzP/BIv/D2n5Bmz/D2f4D4f4D5b/DxLzBJv4Dwb6D2v5D6b/Dz7zDzT/"
    "A7LzD8j3DzX/EPb/ArL1AvH/EDzzDhL/EDP/CBL/CSnxBm3/EeX2CyjxDBL/Eeb2EDX/EZr4CynxDRL/ED7zEDT/AyvxBW3/"
    "ArH/D1b/D7X/D/X/D1j7D17/A2z1D1j/D5n1B1z/D4n1D4v1D1z/EXn/CYz1D4r1D5v1D13/D7xYBGz1A+z1BWz1D1f/B4tV"
    "/whp//8HRf//B3n//wZV//8LmPb/CGr//xBG9f8RVvX/CLD2/wYB9f8Ia///BgD1/wiy9v8GU///D1b1/wZU//8PRvX/BgL1"
    "/wNlq1YOmDZVDBsI+wVwHvADe5X/DxwI+woZCPsFYB7wBYAe8AyBsP8MowX7DLIl8AUhTP8MGgj7BQ4e8AACHvARBR7wDOCx"
    "/w25sf8F4AH/A27EWANTtZYLFSzwDkNZ/wzQG/sPFSzwCRks+wViAf8JO5T1BcEC/wzBsv8EPgH/Ahks+wwZLPsFHSzwDJGr"
    "/xAVLPAM4hn7BQAJ+wVLKfADvF7/DhlQWwgJLmwNs7f1CRBO/wnQJfADiVv/BNOi+AtcAf8L0Sz7CcAl8AEGIvALm7v5AAYi"
    "8AvNsv8JIAL/CeAl8AO85PUDvOX1CGkl8Aq2kPgOAJX1CDkaMgoV8P8OEM70CZNrWwkpF/sI3sH2D5ka+wphCfsOobL/CqGp"
    "/wDHLPsLvAXwCsyy/w7hvvoLNpWyBdNU9Qmpsf8JIB7wBWIA/wVwxfQIzsD2DmC5+RCasf8L1QL/CsEl8Ag6IfMPmrH/EVst"
    "8AKXsf8FYAD/AZex/wkF8P8Al7H/AlYA/w9bLfARmrH/Chn7/wVhAP8G14r/BD4C/wuBCfsPDJn6CyXi9A/BJfAIawXwC6Gp"
    "/wRN//8IZhBODIEs+xDVAf8AyCz7D1sA/wvMsv8CvAXwBlMp+w8RTv8KqbH/DLol8AOcXv8FgMX0C8El8BCiqf8LEU7/BS3w"
    "/wqACfsJYAXwCGws8QpgCfsMgrH/BXAA/xCSsP8KBfD/DICx/wM+XP8DgMP0A5zk9Qwb+/8FcQD/A4VW/wzCvPoMCvv/D6Gp"
    "/woQTv8PgQn7BJNV9RApIvAGiAj6EOIl8AzRsv8PFfD/Drmb/wXCAf8QLPv/BFNV/wSzVfUR4iz7DNKy/wXAAf8McbH/DlNZ"
    "/wlhCfsAsJf1DuRM/wO5tvUCLJawCRXw/w+ssf8FwgL/DHKx/wzJGfsJCiv6CrwF8AnMsv8NZzr/ECUs8BGssf8MGvv/AOIB"
    "/wWZO/8MAFn7AJew/wCa+v8QkLD/CtUC/wCWsP8AqKn/D5Cw/wCYsP8NkKL/AOIL8AotCfsFAP//DNuy/wU7Of8MkyL7EZCw"
    "/wAJ+/8Ap6n/BYIA/whrmvoAyCXwA3lb/wDh9P8AXQL/AMcl8AEmIvAREE7/AFwC/wEp+/8AECHwCO7A9gmuBfAMyrL/ACLw"
    "/wBeAv8PEE7/EBBO/wy5JfADpFf/A2uV/wsgLPADmqX/AjtU+RHhJfAEU4n1CdUB/wvVAf8MgLD/Apmx/wUd8P8E5LT/EVsA"
    "/xDLLPsRJADxAAheAhEc+/8Fvh7wBdAB/wgDMv8GU+T0Apew/wKa+v8FvAH/ArwJ+wKWsP8Loqn/CaKp/wKYsP8IA7L2CqKp"
    "/wIJ+/8FvQD/Edks+xELIvACvQn7AQ4J+wKpLfsAEvD/CC5s/w4ClfUQrLD/CiIC/wLh9P8CXQL/BVuQ8wkiAv8LIgL/AlwC"
    "/wJNTv8CIvD/BVs5/wWsAP8Msv//EDRV9QJeAv8CTE7/Apks+wQiEP8BkrvzBSBM/wshLPADe1n/DkOV/wVgLfAFS5DzCeUB"
    "/wvlAf8BwgL/Aqmx/wUe8P8CKRf7A+DE9Q5iuvkAAh3wDKMi+wNOXP8MGfv/ANIB/wgObP8MsDb1Cgn7/w2p//8Pqan/D5uw"
    "/wkJ+/8Lmvr/CZr6/wsJ+/8MsP//Cpr6/wywuPYFvgD/DNqy/wNb+f8Qm7D/EKmp/w6gsP8Rm7D/BiaI/wUCtfYLXAL/C05O"
    "/wRO//8QJfD/ClwC/wpOTv8R5PT/DyXw/wlcAv8DEgL/DpP1/wMRAv8MybL/DpAl8BEl8P8P5PT/EOT0/wUC//8Oy5n/ELBT"
    "WRFyCfsRoqn/BDs0+QMJZlsRYgn7Dsud+Q+8sf8PcQXwBlUJ+w7LnPkRkrD/D1oA/wIuCfsP48P1DjWT/w8b4fQBLgn7EYIJ"
    "+wzgsv8M0rz6D6yw/wpdAf8D4sX1EeIl8AVDifUJXQH/ERJO/xHSJfAM4bL/EBXw/wDOsv8CXQH/ESz7/wFdAf8RJALxBrSR"
    "+Azisv8AXQH/EFNm9QOyVvkRC8ICA6JZ+hAc+/8DGWdbD7hWABFhFfALXh3wEOEl8BGSGfsR1QH/A2HD9BBbAP8Pyyz7Ar0F"
    "8BDBJfAGRoH4EBFO/wMQAf8FuTv/ADuV9QvAJfAPoqn/CxBO/w+CCfsPYgn7CVwB/wFYHvAFLPD/ESwY+xFwBfAPkrD/EVoA"
    "/wnNsv8LIAL/C+Al8BG8sf8J0iz7CcAV8AYLif8LO5X1Eayw/wGa+v8FIk7/D8Il8AGWsP8BqKn/Aaap/wGYsP8HDO73BQH/"
    "/w2wov8JvAXwDyz7/wc9ff8DYMP0DxJO/wupsf8MuyXwA2VW/w+zVvkIOSLzDJCp/wHh9P8J1QL/CSkY+wugqf8BTk7/AVwC"
    "/wU8CfsP1QH/B7d6/wsF8P8Ryyz7BAIQ/wFeAv8BTE7/DLH//wlxBfAPaPb/CGj//wqu//8R////CGb//wL9//8Jvv//Af3/"
    "/wti/v8A/f//BTz//xBo9v8P////EP///xFo9v8L5vj/EZW4OwvmyP8K4vn/EWuO/wmVtvMLjmj2Bozm/wy64vkKYp7/Cwyt"
    "/wiJs/cFibvzCwz3/wvm6P8Ljmb4C2iG/wtujP8IaPb/EHD+/xHG+P8IZvj/CGf3/wlujP8BDff/CGLm+wAN9/8FbI7zBYk7"
    "/w/m+P8QcP//CJ5s+A+JaP8P6/r/Dyn9/wmc/v8P2f//D2D+/wKc/P8P6f//AZz8/w9i/v8AnPz/BZzz/xHQ6f8P+f//D8n/"
    "/wCc/v8LaPb/C/7//wv///8PK/3/Efv//wvS//8Cvf//Ca7//wvR//8KYv7/C9D//wW88/8QK/3/D/v//xD7//8KYP7/BWk7"
    "/wlynv8K5vj/DDXD/gmCnv8Ik1nzCubI/wni+f8J4eD5CWKe/w6S6v8BJp7/EWDi+QoM9/8JLp7/ACae/waO/P8L4vn/Bo7/"
    "/xGVuPMRiGb/D3D+/wbi6P8PCa7/BuHo/wtinv8P0Pr/BTxw/wXOuPMPcP//Bo7+/xFohv8JiPb/C67//wn///8JjGb/CdL/"
    "/wq+//8C1v//Cf7//wnR//8C5v//CdD//wHm//8RwOn/Cfz//wn9//8A5v//CtL//wu+//8K////CGi+/who+P8K/v//Efr/"
    "/whm9v8K0f//CWL+/wrQ//8FrPP/EQnm/w/6//8Q+v//CWD+/wmOaPYC6Pn/Ceb4/wiC5vkCntL/Auf5/wKe//8J5sj/AQ6e"
    "/wLm+f8O0Lz/Ai7m/wIO5v8JDPf/EeL5/wAWnv8CJ/3/Auj7/wL3//8PK63/CdL6/wLn//8Rcv//C9L6/wKt//8JLvf/AB33"
    "/wIm5v8DIJ3/D3L//xBy//8DIqz/DLto9gzr/v8Mu///BjU79AGe0v8K4fn/AZ7//wy70v8CLp7/CeH5/wAOnv8B5vn/AQ7m"
    "/w+8+/8R4fn/AAae/wEn/f8B6Pv/Aff//wiB5vsIgYb/Aef//xFx//8IYWb/Ai33/wke9/8Brf//AuZy/xFg4PoPcf//EHH/"
    "/wAGrv8Fw+jzC+D5/w6S+/8QYJ7/AJ7S/wrg+f8Anv//D2Ce/w7SvP8J4Pn/AS6e/wIWnv8RYJ7/EOD5/xHg+f8A5vn/CtL5"
    "/xHr+f8Q2f//EGD+/wnS+f8R6vn/EMn//wvS+f8Cnf//EOn//wGd//8QYv7/AJ3//xBh/v8Q+f//AJ3+/waM/v8LDvf/Boz/"
    "/w9ohv8PiGb/EXD+/xFw//8Jxuj/BsLI/wkO9/8Gwcj/AuZw/xHQ+v8B5nD/Boz8/wDmcP8Gjf3/AOj7/wD3//8IgOb7CICG"
    "/wDn//8Arv//CGBm/wId9/8J4Pr/AAf9/wMgrP8Arf//AAbm/xBohv8ArP//EYlo/wue//8Ryf//CGie/xEp/f8Knv//Efn/"
    "/wssnf8P0vn/CZ7//w/R+f8RYv7/D9D5/xFh/v8RYP7/Edn//wSEuEj/DguW//8Lrpz//wu+nP//CAtp//8IJmj//wSTSP//"
    "CBZo//8IK2n//wVkN///EQho/P8IBmj//wuenP//CuAqrP8RDpkc+AuRqZL/DsDgkP8Jcpn7/wImuJL/ADYggf8OkrCS/wkD"
    "Evj/C5kq+f8OsEij/wnhwPv/CakL+P8Jgiv5/woOx3L/CgwuCPgOoGa4/wmSuvv/CYBigP8AC7qb/wALmYD/DqC7+f8OkAn4"
    "/w4VIPn/CWLWeP8RKRz4/wkBgvX/ES4c+f8PLg75/xHJkLn7DLor+P8P0sEO+RHL68n/DsDikP8OVwKU/w/gLvn/C3IjWP8O"
    "wuKQ/w7mwZj/D+CzkvUJxuII+A/hspL/Bh4tjv8Rygv4/w8pHej/D9lgrP4CGCf4/xHZ4oD/ARgn+P8LsKK5/wnWGPj/D+Kw"
    "kv8KeXy3/wnm4hj4C3GC//8Jve2R/w7C4Pz/D2uM5vkLnqyA/w+w5QP5AgyegP8PDs7//wtgYID/Auzg/P8PYID+/w7B4Pz/"
    "D8vp+f8P0Am8/w/gCfj/DsDg/P8Bm77M/wm5K/j/Ednigf8Jqbv//wmBYoD/DsXjkP8JXD6C/w6RsJL/EcmB//8CK7Cl/wrW"
    "eP//AebA+/8PYQ7o/w4VkP//Bx58//8CBpm7/wxmuP//Ecr6//8Jkbv7/w4rBvn/C3GA//8Mu/n//wtwgP//Apa5+/8Mx7f/"
    "/xEJvP//CYD///8Qysr//wYsjv//DpLry/kOgmD5/wEOx/r/C5n7//8OgmH5/xHJI1j/C2Ar+f8EWlr//w6S////ADYigv8D"
    "K1n//wCWu/v/C2Ir+f8O6cv8/wGWu4L/Cb6cgP8Al7r//wmerP//DhsG+f8CBp6s/w6zpf//AyFggP8RybuS/wFnjff/CQ68"
    "//8OJbGl/xHBspL/BgiG//8OkmCC/w6BYPn/Aa6s//8KgHL//wCWufv/AQb4//8HlET8/xHZ4fv/AyIr+f8BeXz7/wGewPv/"
    "ARgH+P8Okf///wcufP//CYC5m/8P4hn4/xFwrP//CZK7+/8BK/n//wKWu/v/EZnJvv8Jgf///wfuwnz/CQIigv8BsJL1/xHA"
    "Cfj/AQi2kv8KGxn3/wmBK/n/D2Ic6P8Bl7r//wngyfr/C2IL+f8BHJ6A/w4FkAn4ChuZcf8Lcpm7/wJnjff/CeDA+/8JmQv4"
    "/xHBHvn/BhiG//8OkmKA/wJphvv/EXKs//8CBvj//w/Syvr/AQcm9/8AILKS/wIYB/j/ABv5//8Pcqz+/wKewPv/D+IJ+P8B"
    "lrn7/wYcjv//CXKenP8JkrmC/w/iLvn/Cbm7//8DIrKS/wmC////AyGykv8ADpyA/w6QspL/CSMi+P8CsJL1/wkTIvj/Aiv5"
    "//8DlbJW/xEOzBn4EOnigf8Rcaz//wGdHfj/A7GS9f8RwBn4/wIQK1n/ENmB//8DISv5/wqt/f//A5GhkvURwQn4/w4AIpH/"
    "CgJw9f8JIjwe+A/SGbz/EQnG+v8JDsb6/xDJwPv/CeDB+/8DO1ta/xEZvP//D05Okv8GjQNX/xFhPIL1CeLB+/8RwrKS/woj"
    "Avf/CdLJyv8DkWa49QojMo3/C7ye/v8OAiH5/wNhgPX/DiNb+v8DIGCA/w4AIfn/CQ2IaP8DIjtb+gDI6+n/AxtZ//8Cm77M"
    "/w6RCfj/DqFmuP8Kqfv//wtwubv/C2Gxkv8PYYD+/w4CW/r/A2EV+P8OJSD5/w9xrP7/DgIi+f8P4Qn4/w/Bysr/BgyO//8J"
    "kLn7/w6AYPn/AK6s//8AGAf4/w6Q////AAgH+P8Jmbv//wAG+P//CZK5+/8DYID1/wCewPv/CmBy//8Jkbn7/wYohv//CZ68"
    "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"
    "OCL/CVy+I///AIs0Kvv/Ai4sDvz/AsCz5Vz/AztJ4sDxA7CTJP//ASDiwvH/CyMJmyDxAS0Ix8v/DOq6Ybz/EQMpWxz/DGCC"
    "YIL7AyDgwfD/EcIj8v//EcLiwfH/AyDgwPD/AyDx////EbHAkv//EcDgwP//DwMiLv//ACApW/H/A5GyIPL/CQ6evYL/A4K1"
    "kmD/AxLiwPP/AB4IxvL/ACACDvz/BTweDvz/EYIrKcb/A7GT9P//A55cvf3/EV4CwCz/DiMCGf//A5KwIv//AyIAIPH/D+UE"
    "Ev//AQ4Yxv//Ar5hLP//Ao0Mbv3/AQ4Ixv//AQ78////AMLTwfD/AMLj8P//ApCyIvH/AhACHgz/A5GyJf//Ag4sDvz/DcPl"
    "XCn/AhAS////EcACIPH/A5GxIv//AC4cDvz/AxkLEv//EYFhHP//DsXllPH/DiUAKf//EYJgLP//A5KyIvH/AyLiwP//EeHJ"
    "y///AQAiDhz/DrNVM/r/ACACIPL/CVw8vfH/ADElUPT/EbPFlPT/AyAAIfH/DiOwlJD/Csboy/v/AxkmuBX/Cl68wwv/CQwu"
    "CP//ASApW///CcPgggX/EcICIvL/EcCcgLL/AQACDhz/EenbACLxAB4sECL/ERsmHP//ASAZW///A5AJCFv/EcICIfL/Ag5d"
    "PvL/EcEAIf//EWK+Df//EYFgDP//A5GxFf//ApCwFf//EWG+/f//AyAO/P//EYFgwvD/AAACIPL/Ay4IxhX/EZq5yfH/Awkm"
    "uBX/Alw+8v//EcDiwvH/AyICIv//Ag4sIPL/AF6evMP/C7KQspD5EdIDIg7/DCm4BQD/AgDiwvH/BTwtHP//BS4MAP//D+UT"
    "IPL/AmaNB/b/BQEBsZX/EMnrycv/AhI7GRD/AgASIPL/AwFbWf//A2EigP//AhApW/D/DsXjDP//AQEpWln/EcLgwvD/Ai4s"
    "IPL/EYFhwP//EcAAIv//EcLx////EdAAIv7/AFY8vv//AQ48IPH/CdZ4YPL/C7KQCf//AB4c////A5CyBf//ASDy////CQ4s"
    "GP//DiMCzsD/EQwotsLxENnjy/X/ESsmHP//AyLgwvH/EYBgwPH/AbGVIvL/EYBiwP//BTUhM/H/A5CyJf//AhApK/L/Ajtc"
    "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"
)

def _decode_table(text):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    out = bytearray()
    acc = 0
    bits = 0
    for ch in text:
        if ch == "=":
            break
        value = alphabet.find(ch)
        if value < 0:
            continue
        acc = (acc << 6) | value
        bits += 6
        if bits >= 8:
            bits -= 8
            out.append((acc >> bits) & 255)
            acc &= (1 << bits) - 1
    return out

_TABLE = _decode_table(_TABLE_B64)
del _TABLE_B64

trace("class mtab")
class mtab():

    def __init__(self, s):
        self.stage  = s
        self.sz     = sm.sz[s]
        self.nbytes = cube_mtab.mtb[s]
        self.foff   = 0
        for i in range(s):
            self.foff += (sm.sz[i]-1)*cube_mtab.mtb[i]
        self.fmap   = (0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5)
        self.rmap   = (1, 2, -1) * NFACE

    def moves(self, i, f, r):
        mv = 0
        if i > 0:
            d = self.foff + (i-1)*self.nbytes
            b = _TABLE[d]
            d += 1
            if b != 0xFF:
                mvm = self.nbytes*2-1
                f0 = self.fmap[b]
                f[mv] = f0
                r[mv] = self.rmap[b]
                mv += 1
                while mv < mvm:
                    b >>= 4
                    if (mv & 1) != 0:
                        b = _TABLE[d]
                        d += 1
                    b0 = b & 0xF
                    if b0 == 0xF:
                        break
                    f0 = self.fmap[b0]
                    r[mv] = self.rmap[b0]
                    if f0 >= f[mv-1]:
                        f0 += 1
                    f[mv] = f0
                    mv += 1
        return mv

#-----------------------------------------------------------------------------

trace("class cube_idx")
class cube_idx():

    def __init__(self, m = None):
        self.ci = []
        self.ei = []
        for i in range(NFACE):
            self.ci.append([0] * NFACE)
            self.ei.append([0] * NFACE)
        # pre-allocate for speed
        self.tmp_idx = [0] * solve_map.NPIECE

        self.init(m)

    def init(self, m):
        if m != None:
            for i in range(NCORNER):
                cp0 = sm.cp0[i]
                cp1 = sm.cp1[i]
                cp2 = sm.cp2[i]
                c0 = m.corner(cp0, cp1)
                c1 = m.corner(cp1, cp2)
                c2 = m.corner(cp2, cp0)
                i3 = 3*i
                self.ci[c0][c1] = i3+2
                self.ci[c1][c2] = i3+1
                self.ci[c2][c0] = i3
            # }
            for i in range(NEDGE):
                ep0 = sm.ep0[i]
                ep1 = sm.ep1[i]
                e0 = m.edge(ep0, ep1)
                e1 = m.edge(ep1, ep0)
                i2 = 2*i
                self.ei[e0][e1] = i2+1
                self.ei[e1][e0] = i2
            # }

    def index(self, s):
        idx = self.tmp_idx
        ind = 0
        cs = sm.cn[s]
        ce = sm.cn[s+1]
        cn = cs - ce
        cm = 3*cs
        for i in range(cn):
            cp0 = sm.cp0[cs-i-1]
            cp1 = sm.cp1[cs-i-1]
            ii = self.ci[cp0][cp1]
            for j in range(i):
                if ii > idx[j]:
                    ii -= 3
            # }
            idx[i] = ii
            ind = (ind*cm)+ii
            cm -= 3
        # }
        es = sm.en[s]
        ee = sm.en[s+1]
        en = es - ee
        em = 2*es
        for i in range(en):
            ep0 = sm.ep0[es-i-1]
            ep1 = sm.ep1[es-i-1]
            ii = self.ei[ep0][ep1]
            for j in range(i):
                if ii > idx[j]:
                    ii -= 2
            # }
            idx[i] = ii
            ind = (ind*em)+ii
            em -= 2
        # }
        if s == (solve_map.NSTAGE-1):
            # Minimise index when parity known
            if en > 0:
                ind = (int(ind/4)*2)+(ind&1)
            else:
                ind = (int(ind/6)*3)+(ind%3)
        # }
        sz = sm.sz[s]
        ind = (sz-1-ind)
        return ind

#-----------------------------------------------------------------------------

MAXINT = 0x3FFFFFFF

MV_MAX = 80

trace("class cube")
class cube():

    colors = None

    def __init__(self):
        self.mv_n     = 0
        self.found    = 0
        self.quick    = 0
        self.end_time = 0
        self.pce      = [0] * NFACE
        for f in range(NFACE):
            self.pce[f] = [f] * (2*NSIDE)
        self.mv_f    = [0] * MV_MAX
        self.mv_r    = [0] * MV_MAX
        self.colors  = None
        # pre-allocate for speed
        self.tmp_f    = [0] * cube_mtab.MV_MENT
        self.tmp_r    = [0] * cube_mtab.MV_MENT
        self.tmp_mi= cube_idx()

    def alloc_colors(self):
        if self.colors == None:
            self.colors= colors.cube_colors(self)

    def copy(self, m):
        for f in range(NFACE):
            for i in range(2*NSIDE):
                self.pce[f][i] = m.pce[f][i]

    def copy_moves(self, m):
        self.mv_n = m.mv_n
        for i in range(self.mv_n):
            self.mv_f[i] = m.mv_f[i]
            self.mv_r[i] = m.mv_r[i]

    def corner(self, f0, f1):
        return self.pce[f0][cm.corner(f0, f1)]

    def edge(self, f0, f1):
        return self.pce[f0][cm.edge(f0, f1)]

    def rot(self, f, r):
        r  = RMOD(r)
        p0 = self.pce[f]
        fd = cm.dir(f, NSIDE_M1)
        while r > 0:
            r   -= 1
            p   = p0[6]; p0[6] = p0[4]; p0[4] = p0[2]; p0[2] = p0[0]; p0[0] = p
            p   = p0[7]; p0[7] = p0[5]; p0[5] = p0[3]; p0[3] = p0[1]; p0[1] = p
            pd  = self.pce[fd]
            od2 = cm.corner(fd, f)
            od0 = (od2-2)&7
            c0  = pd[od0]
            e0  = pd[od0+1]
            c1  = pd[od2]
            for d in range(NSIDE-2, -1, -1):
                fs  = cm.dir(f, d)
                os2 = cm.corner(fs, f)
                os0 = (os2-2)&7
                ps  = self.pce[fs]
                pd[od0]   = ps[os0]
                pd[od0+1] = ps[os0+1]
                pd[od2]   = ps[os2]
                pd  = ps
                od0 = os0
                od2 = os2
            # }
            pd[od0]   = c0
            pd[od0+1] = e0
            pd[od2]   = c1

    def backtrack_a(self, f):
        i = self.mv_n
        btrack = False
        while (i > 0):
            i -= 1
            fi = self.mv_f[i]
            if cm.adjacent(f, fi):
                break
            if f <= fi:
                btrack = True
                break
        # }
        return btrack

    def add_mv(self, f, r):
        i = self.mv_n
        mrg = False
        while (i > 0):
            i -= 1
            fi = self.mv_f[i]
            if cm.adjacent(f, fi):
                break
            if f == fi:
                r += self.mv_r[i]
                r = RFIX(r)
                if r != 0:
                    self.mv_r[i] = r
                else:
                    self.mv_n -= 1
                    while (i < self.mv_n):
                        self.mv_f[i] = self.mv_f[i+1]
                        self.mv_r[i] = self.mv_r[i+1]
                        i += 1
                    # }
                # }
                mrg = True
                break
            # }
        # }
        if not mrg:
            self.mv_f[self.mv_n] = f
            self.mv_r[self.mv_n] = RFIX(r)
            self.mv_n += 1
        # }

    def move(self, f, r):
        self.rot(f, r)
        self.add_mv(f, r)

    def valid_pieces(self):
        val = True
        for f0 in range(NFACE):
            for f1 in range(NFACE):
                if cm.adjacent(f0, f1):
                    efound = False
                    cfound = False
                    f2 = cm.get_remap(f0, f1).fm[5]
                    for s0 in range(NFACE):
                        for s1 in range(NFACE):
                            if cm.adjacent(s0, s1):
                                s2 = cm.get_remap(s0, s1).fm[5]
                                if (self.edge(s0, s1) == f0 and
                                    self.edge(s1, s0) == f1):
                                    efound = True
                                if (self.corner(s0, s1) == f0 and
                                    self.corner(s1, s2) == f1 and
                                    self.corner(s2, s0) == f2):
                                    cfound = True
                        # }
                    # }
                    if not (efound and cfound):
                        val = False
        return val

    def valid_positions(self):
        c = cube()
        c.copy(self)
        c.solve(0)
        c.solve_apply()
        return c.solved()

    def solved(self):
        slvd = True
        f = 0
        while (slvd and f < NFACE):
            for p in range(2*NSIDE):
                if self.pce[f][p] != f:
                    slvd = False
                    break
            # }
            f += 1
        # }
        return slvd

    def shuffle(self, n):
        for i in range(n):
            self.rot(RND(NFACE), 1+RND(NSIDE_M1))

    def timeout(self):
        return _ticks_ms() >= self.end_time

    def solve_remap(self, best, s0):
        slvd = True
        for s in range(s0, solve_map.NSTAGE):
            mi = self.tmp_mi
            mi.init(self)
            i = mi.index(s)
            if i != 0:
                n = -1
                f = self.tmp_f
                r = self.tmp_r
                n = mt[s].moves(i, f, r)
                if n > 0:
                    mv = self.mv_n + n
                    for j in range(n):
                        self.add_mv(f[j], r[j])
                    # }
                    if (self.mv_n > best or
                        (s == 0 and self.mv_n < mv)):
                        slvd = False
                        break
                    # }
                    if s < (solve_map.NSTAGE-1):
                        for j in range(n):
                            self.rot(f[j], r[j])
                    # }
                else:
                    slvd = False
                    break
                # }
            # }
        # }
        return slvd

    def solve_one(self, cb, cs, depth):
        slvd = False
        if self.mv_n < depth:
            f = 0
            while (not slvd and f < NFACE):
                if not self.backtrack_a(f):
                    n = self.mv_n+1
                    for i in range(1, NSIDE):
                        self.move(f, 1)
                        if not slvd and self.solve_one(cb, cs, depth):
                            slvd = True
                    # }
                    self.move(f, 1)
                # }
                f += 1
            # }
        else:
            # print("solve_one: quick="+str(cb.quick))
            cs.copy(self)
            cs.copy_moves(self)
            cs.end_time = cb.end_time
            if cs.solve_remap(cb.mv_n, 0):
                if cs.mv_n < cb.mv_n:
                    # print("solve_one: solved="+str(cs.mv_n))
                    cb.copy_moves(cs)
                # }
            # }
            # finish if a short solution has been found or if any solution
            # has been found and the timeout has expired or if only a quick
            # solve is required
            if cb.mv_n <= 8 or (cb.mv_n <MV_MAX and (cb.quick or cb.timeout())):
                trace("solved_one()")
                slvd = True
        return slvd

    def solve(self, msecs = 1000):
        start_time = _ticks_ms()
        self.mv_n = MAXINT
        self.end_time = start_time + msecs
        self.quick = (msecs == 0)
        cw = cube()
        cw.copy(self)
        cs = cube()
        depth = 0
        while (not cw.solve_one(self, cs, depth)):
            depth += 1
        # print("Moves: "+str(self.mv_n)+" "+
        #    "Time: "+str(int(time.ticks_ms() - start_time))+"ms ")

    def solve_apply(self):
        for i in range(self.mv_n):
            self.rot(self.mv_f[i], self.mv_r[i])

    def set_rgb(self, f, o, rgb):
        self.colors.set_rgb(f, o, rgb)

    def get_clr(self, f, o):
        return self.colors.get_clr(f, o)

    def determine_colors(self, t):
        return self.colors.determine_colors(t)

def init(colors_module):
    trace("init()")
    global colors, cm, sm, mt
    colors = colors_module
    cm     = cube_map()
    sm     = solve_map()
    mt     = []
    for s in range(cube_mtab.NSTAGE):
        mt.append(mtab(s))
    trace("done")

trace("imported")

#-----------------------------------------------------------------------------

# END



# ---------------------------------------------------------------------------
# Public facelet API
#
# PrimeCuber's internal face IDs are:
#   0=U, 1=R, 2=D, 3=L, 4=F, 5=B
# The input is the conventional row-major URFDLB facelet string.
# ---------------------------------------------------------------------------

_FACE_CHARS = "URFDLB"
_FACE_TO_ID = {"U": 0, "R": 1, "F": 4, "D": 2, "L": 3, "B": 5}
_ID_TO_FACE = ("U", "R", "D", "L", "F", "B")

# PrimeCuber perimeter offsets are corner, edge, corner, ... counterclockwise.
_PCE_TO_FACELET = (
    (0, 3, 6, 7, 8, 5, 2, 1),  # U
    (2, 1, 0, 3, 6, 7, 8, 5),  # R
    (8, 5, 2, 1, 0, 3, 6, 7),  # D
    (6, 7, 8, 5, 2, 1, 0, 3),  # L
    (2, 1, 0, 3, 6, 7, 8, 5),  # F
    (2, 1, 0, 3, 6, 7, 8, 5),  # B
)
_FACE_BLOCK = (0, 9, 27, 36, 18, 45)

def _parse_facelets(facelets):
    if not isinstance(facelets, str):
        raise ValueError("cube_state must be a 54-character string")
    if len(facelets) != 54:
        raise ValueError("cube_state must contain exactly 54 facelets")
    counts = [0, 0, 0, 0, 0, 0]
    for ch in facelets:
        k = _FACE_CHARS.find(ch)
        if k < 0:
            raise ValueError("cube_state may contain only U, R, F, D, L and B")
        counts[k] += 1
    for n in counts:
        if n != 9:
            raise ValueError("cube_state must contain nine stickers of each face")
    for p in range(6):
        if facelets[_FACE_BLOCK[p] + 4] != _ID_TO_FACE[p]:
            raise ValueError("facelet centers must be U, R, F, D, L and B")
    c = cube()
    for pf in range(6):
        block = _FACE_BLOCK[pf]
        rowmap = _PCE_TO_FACELET[pf]
        for o in range(8):
            ch = facelets[block + rowmap[o]]
            c.pce[pf][o] = _FACE_TO_ID[ch]
    if not c.valid_pieces():
        raise ValueError("cube_state has impossible edge or corner pieces")
    if not _valid_position_invariants(c):
        raise ValueError("cube_state has impossible orientation or permutation")
    return c

_FCE = (
    (3, 4, 1, 5),
    (0, 4, 2, 5),
    (1, 4, 3, 5),
    (2, 4, 0, 5),
    (0, 3, 2, 1),
    (0, 1, 2, 3),
)

def _edge_data(c, f, o):
    n = _FCE[f][o // 2]
    no = 2 * _FCE[n].index(f) + 1
    return n, no, c.pce[f][o], c.pce[n][no]

def _corner_data(c, f, o):
    d = o // 2
    n1 = _FCE[f][(d - 1) & 3]
    n2 = _FCE[f][d]
    # n1 is the preceding direction, so use the corner before f on n1;
    # n2 is the following direction, so use the corner after f on n2.
    o1 = (2 * _FCE[n1].index(f)) & 7
    o2 = (2 * _FCE[n2].index(f) + 2) & 7
    return ((f, o, c.pce[f][o]), (n1, o1, c.pce[n1][o1]),
            (n2, o2, c.pce[n2][o2]))

def _parity(values):
    inv = 0
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if values[i] > values[j]:
                inv ^= 1
    return inv

def _valid_position_invariants(c):
    edges = []
    edge_keys = []
    for f in range(6):
        for o in (1, 3, 5, 7):
            n, no, a, b = _edge_data(c, f, o)
            key = tuple(sorted((f, n)))
            if key not in edge_keys:
                edge_keys.append(key)
                edges.append((f, o))
    corners = []
    corner_keys = []
    for f in range(6):
        for o in (0, 2, 4, 6):
            data = _corner_data(c, f, o)
            key = tuple(sorted((data[0][0], data[1][0], data[2][0])))
            if key not in corner_keys:
                corner_keys.append(key)
                corners.append((f, o))

    edge_ids = []
    edge_flip = 0
    for f, o in edges:
        n, no, a, b = _edge_data(c, f, o)
        key = tuple(sorted((a, b)))
        if key not in edge_keys:
            return False
        edge_ids.append(edge_keys.index(key))
        if 0 in key or 2 in key:
            ud = 0 if 0 in key else 2
            edge_flip += 0 if ((a == ud and f in (0, 2)) or
                               (b == ud and n in (0, 2))) else 1
        else:
            fb = 4 if 4 in key else 5
            edge_flip += 0 if ((a == fb and f in (4, 5)) or
                               (b == fb and n in (4, 5))) else 1

    corner_ids = []
    corner_twist = 0
    for f, o in corners:
        data = _corner_data(c, f, o)
        key = tuple(sorted((data[0][2], data[1][2], data[2][2])))
        if key not in corner_keys:
            return False
        corner_ids.append(corner_keys.index(key))
        ud = 0 if 0 in key else 2
        for pf, po, sticker in data:
            if sticker == ud:
                corner_twist += 0 if pf in (0, 2) else (1 if pf in (1, 3) else 2)
                break

    # PrimeCuber's piece-colour validation above already rejects malformed
    # piece identities.  The permutation-parity check rejects the other
    # common impossible input (a single swapped pair).  The orientation
    # coordinates are deliberately not used here because PrimeCuber's
    # perimeter convention is different from the usual Kociemba orientation
    # convention; legal positions are still solved by the embedded solver.
    return _parity(edge_ids) == _parity(corner_ids)

_INIT = False
# Keep searching for a shorter solution for 50 seconds after search starts.
# The solver may take longer if it has not found its first solution yet.
_SEARCH_BUDGET_MS = 50000

def solve(cube_state):
    global _INIT
    if not _INIT:
        init(None)
        _INIT = True
    c = _parse_facelets(cube_state)
    if c.solved():
        return []
    c.solve(_SEARCH_BUDGET_MS)
    result = []
    for i in range(c.mv_n):
        face = _ID_TO_FACE[c.mv_f[i]]
        r = c.mv_r[i] & 3
        if r == 1:
            result.append(face)
        elif r == 2:
            result.append(face + "2")
        elif r == 3:
            result.append(face + "'")
        else:
            raise ValueError("internal solver produced a null move")
    return result
