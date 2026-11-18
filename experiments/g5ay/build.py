"""Build standalone NTSC F6 test ROMs. No game logic."""
from pathlib import Path
import argparse
import json
import subprocess

DASM = "/workspace/.g5ar-env01/bin/dasm"
MASKS = json.loads(Path("masks.json").read_text())["sprites"]
TYPES = ("large_male", "large_male", "large_female", "small_male", "small_female")
PLAYER = (0x3c, 0x7e, 0x18, 0x7e, 0x1e, 0x3c, 0x18, 0x24, 0x42)
# Tuples are ordered by NPC identity, never by raster order.
# X is a CPU strobe-completion cycle, not a physical pixel coordinate.
SCENES = (
    {"name": "same_y", "x_cycles": [26, 36, 46, 56, 66], "y": [72]*5},
    {"name": "tight_reorder", "x_cycles": [63, 26, 45, 54, 35], "y": [73, 72, 73, 71, 72]},
    {"name": "staggered_y", "x_cycles": [35, 65, 25, 55, 45], "y": [70, 71, 72, 73, 74]},
    {"name": "tight_y_overlap", "x_cycles": [59, 32, 23, 50, 41], "y": [75, 74, 73, 72, 71]},
)
HEADER = """
 processor 6502
VSYNC=$00
VBLANK=$01
WSYNC=$02
NUSIZ0=$04
NUSIZ1=$05
COLUP0=$06
COLUP1=$07
COLUPF=$08
COLUBK=$09
CTRLPF=$0a
PF0=$0d
PF1=$0e
PF2=$0f
RESP0=$10
RESP1=$11
RESM0=$12
GRP0=$1b
GRP1=$1c
ENAM0=$1d
FRAME=$80
 ORG $f000
Reset:
 sei
 cld
 ldx #$ff
 txs
 lda #0
 ldx #$7f
Clear:
 sta $80,x
 dex
 bpl Clear
 sta VBLANK
 sta VSYNC
 sta GRP0
 sta GRP1
 sta ENAM0
 sta NUSIZ0
 sta COLUBK
 sta PF1
 sta PF2
 lda #$1e
 sta COLUP0
 lda #$0e
 sta COLUP1
 lda #$26
 sta COLUPF
 lda #$01
 sta CTRLPF
 lda #$30
 sta PF0
 lda #NUSIZ_TEST
 sta NUSIZ1
Frame:
 sta WSYNC
 lda #2
 sta VSYNC
 sta VBLANK
 lda FRAME
 lsr
 lsr
 lsr
 lsr
 and #3
 tax
 lda $fff6,x
BankSwitched:
 sta WSYNC
 sta WSYNC
 ; First of 37 VBLANK scanlines.
 sta WSYNC
 lda #0
 sta VSYNC
 sta GRP0
 sta GRP1
 sta ENAM0
 ; Distinct right-side P0/M0 x. No HMOVE needed for these fixed witnesses.
 sta WSYNC
 ldx #13
PositionPlayer:
 dex
 bne PositionPlayer
 sta RESP0
 sta WSYNC
 ldx #14
PositionMissile:
 dex
 bne PositionMissile
 sta RESM0
 ldx #34
BlankFill:
 sta WSYNC
 dex
 bne BlankFill
 ; Visible line 0 is the following WSYNC.
"""
TAIL = """
 ldx #30
Overscan:
 sta WSYNC
 lda #2
 sta VBLANK
 dex
 bne Overscan
 inc FRAME
 jmp Frame
EndKernel:
 ORG $fffa
 word Reset,Reset,Reset
"""


def pad(cycles):
    if cycles < 0 or cycles == 1:
        raise ValueError(f"unrepresentable pad {cycles}")
    return ([" bit FRAME"] if cycles % 2 else []) + [" nop"] * (cycles // 2 - cycles % 2)


def row(y, scene, group):
    player = PLAYER[y-72] if 72 <= y < 81 else 0
    instructions = [" sta WSYNC", f" lda #${player:02x}", " sta GRP0",
                    f" lda #${2 if 75 <= y < 77 else 0:02x}", " sta ENAM0",
                    " lda #0", " sta GRP1"]
    cycle = 15
    positions = []
    suppressed = []
    for i in sorted(group, key=scene["x_cycles"].__getitem__):
        off = y - scene["y"][i]
        if 0 <= off < 9:
            data = int(MASKS[TYPES[i]][off], 2)
            at = scene["x_cycles"][i]
            gap = at - cycle - 5
            if gap < 0 and scene.get("overlap_probe"):
                suppressed.append(i)
                continue
            indexed = gap == 1
            if not indexed:
                instructions.extend(pad(gap))
            # X is 0 on both paths after TopFill.
            instructions.extend([f" lda #${data:02x}", " sta RESP1,x" if indexed else " sta RESP1"])
            lateness = scene.get("grp1_delay", {}).get((i,y),0)
            if lateness > 1:
                instructions.extend(pad(lateness))
            instructions.append(" sta GRP1,x" if lateness == 1 else " sta GRP1")
            cycle = at + 3 + lateness
            positions.append((i, at, cycle))
    return instructions, {"y":y, "stores":positions, "suppressed":suppressed, "last_cycle":cycle}


def r2_row(y, refined):
    """Static co-raster probe. Last slot replaces SF with a gold key."""
    index = y - 72
    player = PLAYER[index]
    key = (0x38,0x44,0x44,0x38,0x10,0x1c,0x10,0x18,0x00)[index]
    door = 0x20 if index in (2,3,4) else 0x30
    instructions = [" sta WSYNC", " lda #$30", " sta PF0", " lda #$26",
                    " sta COLUPF", " lda #$0e", " sta COLUP1",
                    f" lda #${player:02x}", " sta GRP0", f" ldx #${door:02x}"]
    if refined:
        # Keep the previous line's PF0 shape on the left during the hole.
        # Brown color remains, but 4 px wall thickness is a known tradeoff.
        del instructions[1:3]
        instructions.extend(pad(2))
    stores = []
    for slot, at in enumerate((24,32,40,48) if refined else (27,35,43,51)):
        data = int(MASKS[TYPES[slot]][index], 2)
        instructions.extend([f" lda #${data:02x}", " sta RESP1", " sta GRP1"])
        stores.append((slot,at,at+3))
    if refined:
        instructions.extend(pad(3))
    instructions.extend([" lda #$2c", " sta COLUP1", f" lda #${key:02x}",
                         " sta RESP1", " sta GRP1", " stx PF0", " sty COLUPF"])
    stores.append((4,64,67))
    return instructions, {"y":y, "stores":stores, "last_cycle":73}


def r2(refined):
    text = ["RasterR2:", " ldx #72", " ldy #$38", "TopFillR2:",
            " sta WSYNC", " lda #0", " sta VBLANK", " dex", " bne TopFillR2",
            " lda #2", " sta ENAM0"]
    timing = []
    for y in range(72,81):
        instructions, trace = r2_row(y, refined)
        text.append(f"LineR2_{y}:")
        text.extend(instructions)
        timing.append(trace)
    text.extend([" sta WSYNC", " lda #0", " sta GRP1", " sta GRP0", " sta ENAM0",
                 " lda #$30", " sta PF0", " lda #$26", " sta COLUPF",
                 " ldx #110", "BottomFillR2:", " sta WSYNC", " dex", " bne BottomFillR2"])
    return "\n".join(text), timing


def raster(scene, group, suffix):
    text = [f"Raster{suffix}:", " ldx #68", f"TopFill{suffix}:",
            " sta WSYNC", " lda #0", " sta VBLANK", " dex", f" bne TopFill{suffix}"]
    timing = []
    for line in range(68, 86):
        code, trace = row(line, scene, group)
        text.append(f"Line{suffix}_{line}:")
        text.extend(code)
        timing.append(trace)
    text.extend([" sta WSYNC", " lda #0", " sta GRP1", " sta GRP0", " sta ENAM0",
                 " ldx #105", f"BottomFill{suffix}:", " sta WSYNC", " dex", f" bne BottomFill{suffix}"])
    return "\n".join(text), timing


def build(mode):
    if mode in ("fixedcopies", "packedcopies", "splitcopies", "clean1", "clean2", "rephase", "alternate"):
        scenes = [dict(scene, x_cycles=list(scene["x_cycles"])) for scene in SCENES]
        for scene in scenes:
            first = min(range(5), key=scene["x_cycles"].__getitem__)
            if mode in ("rephase", "alternate", "packedcopies", "splitcopies", "clean1", "clean2"):
                scene["x_cycles"][first] = 22
    else:
        scenes = SCENES
    if mode in ("packedcopies", "splitcopies", "clean1", "clean2"):
        # Keep the last actor short of the fixed right-side shot. In the last
        # scene NPC 0/1 request the same X; skipped rows count as diagnostic FAIL.
        plans = ([22,31,40,49,58], [59,22,40,50,31],
                 [31,58,22,49,40], [40,40,22,49,31])
        for scene, x_cycles in zip(scenes, plans):
            scene["x_cycles"] = list(x_cycles)
        scenes[3]["overlap_probe"] = True
        if mode in ("clean1", "clean2"):
            scenes[2]["grp1_delay"] = {(0,71):int(mode[-1])}
    prefix = Path(mode)
    prefix.mkdir(exist_ok=True)
    manifest = []
    banks = []
    for bank, scene in enumerate(scenes):
        intercept = "NUSIZ_TEST=1\n" if mode in ("copies", "fixedcopies", "packedcopies", "splitcopies", "clean1", "clean2", "r2probe", "r2probe2") else "NUSIZ_TEST=0\n"
        if mode in ("alternate", "splitcopies"):
            dispatch = "\n lda FRAME\n and #1\n beq EvenJump\n jmp RasterOdd\nEvenJump:\n jmp RasterEven\n"
            groups = [("Even",(0,2,4)),("Odd",(1,3))]
        else:
            dispatch = "\n"
            groups = [("All",tuple(range(5)))]
        bodies, budgets = [], {}
        for suffix, group in groups:
            body, timing = r2(mode == "r2probe2") if mode in ("r2probe", "r2probe2") else raster(scene, group, suffix)
            if suffix == "Even":
                body += "\n jmp EndRaster\n"
            bodies.append(body)
            budgets[suffix] = timing
        manifest.append(dict(scene={k:v for k,v in scene.items() if k!="grp1_delay"}, bankslot=bank, row_budget=budgets))
        path = prefix / f"bank{bank}.asm"
        header = HEADER
        if mode in ("fixedcopies", "packedcopies", "splitcopies", "clean1", "clean2"):
            # Old missile delay + LDX + next WSYNC reached cycle 79.
            header = header.replace("ldx #14", "ldx #13")
        if mode in ("packedcopies", "splitcopies", "clean1", "clean2"):
            header = header.replace("ldx #13\nPositionPlayer", "ldx #4\nPositionPlayer")
        if mode in ("r2probe", "r2probe2"):
            header = header.replace("ldx #14", "ldx #5").replace("ldx #13\nPositionPlayer","ldx #4\nPositionPlayer")
            manifest[-1]["scene"] = {"name":mode,"x_cycles":[24,32,40,48,64] if mode=="r2probe2" else [27,35,43,51,64],"y":[72]*5}
        path.write_text(intercept + header + dispatch + "\n".join(bodies) + "\nEndRaster:\n" + TAIL)
        stem = path.with_suffix("")
        subprocess.run([DASM,str(path),"-f3",f"-o{stem}.bin",f"-l{stem}.lst",f"-s{stem}.sym"],check=True)
        data = stem.with_suffix(".bin").read_bytes()
        assert len(data) == 4096
        banks.append(data)
    # All bytes executed before the selector must match across banks.
    positions = [next(int(line.split()[1],16) for line in (prefix/f"bank{i}.sym").read_text().splitlines() if line.startswith("BankSwitched ")) for i in range(4)]
    assert len(set(positions)) == 1
    assert all(bank[:positions[0]-0xf000] == banks[0][:positions[0]-0xf000] for bank in banks)
    (prefix/f"g5ay_{mode}_F6.bin").write_bytes(b"".join(banks))
    (prefix/"schedule.json").write_text(json.dumps(manifest,indent=2)+"\n")

def contrasts():
    """One bank/slot changes one chosen numeric coordinate at a time."""
    base = {"x_cycles":[22,31,40,49,58], "y":[72]*5}
    scenes = []
    for position in range(16):
        scene = {key:value.copy() for key,value in base.items()}
        scene["name"] = "reference"
        if position:
            axis, shift = (("x_cycles",1),("y",1),("x_cycles",-1))[(position-1)//5]
            identity = (position-1)%5
            scene[axis][identity] += shift
            scene["name"] = f"NPC{identity}_{axis}_{shift:+d}"
        scenes.append(scene)
    directory = Path("contrasts")
    directory.mkdir(exist_ok=True)
    header = HEADER.replace("ldx #14", "ldx #13").replace("ldx #13\nPositionPlayer","ldx #4\nPositionPlayer")
    # Two temporary RAM bytes, not aliases of the frame counter.
    dispatch = """
 lda FRAME
 lsr
 lsr
 and #3
 tax
 lda LowJump,x
 sta $81
 lda HighJump,x
 sta $82
 jmp ($0081)
LowJump:
 byte <Raster0,<Raster1,<Raster2,<Raster3
HighJump:
 byte >Raster0,>Raster1,>Raster2,>Raster3
"""
    banks, plans = [], []
    for bank in range(4):
        bodies = []
        for slot in range(4):
            scene = scenes[4*bank+slot]
            code, timing = raster(scene, range(5), str(slot))
            bodies.append(code + "\n jmp EndRaster\n")
            plans.append(dict(scene=scene, bankslot=bank, slot=slot, row_budget={"All":timing}))
        path = directory/f"bank{bank}.asm"
        path.write_text("NUSIZ_TEST=1\n"+header+dispatch+"\n".join(bodies)+"\nEndRaster:\n"+TAIL)
        stem = path.with_suffix("")
        subprocess.run([DASM,str(path),"-f3",f"-o{stem}.bin",f"-l{stem}.lst",f"-s{stem}.sym"],check=True)
        bank_bytes = stem.with_suffix(".bin").read_bytes()
        assert len(bank_bytes)==4096
        banks.append(bank_bytes)
    switches = [next(int(line.split()[1],16) for line in (directory/f"bank{i}.sym").read_text().splitlines() if line.startswith("BankSwitched ")) for i in range(4)]
    assert len(set(switches))==1
    assert all(bank[:switches[0]-0xf000]==banks[0][:switches[0]-0xf000] for bank in banks)
    (directory/"g5ay_contrasts_F6.bin").write_bytes(b"".join(banks))
    (directory/"schedule.json").write_text(json.dumps(plans,indent=2)+"\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode",choices=("direct","copies","alternate","rephase","fixedcopies","packedcopies","splitcopies","r2probe","r2probe2","contrasts","clean1","clean2"))
    mode = parser.parse_args().mode
    if mode == "contrasts":
        contrasts()
    else:
        build(mode)
