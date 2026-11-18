"""Build four F6 diagnostics from one 6502 source and frozen masks."""
from pathlib import Path
import json
import subprocess

MASKS = json.loads(Path("masks.json").read_text())["sprites"]
TYPES = ("large_male","large_female","small_male","small_female")
LABELS = ("Male","Female","SmallM","SmallF")
BIN = "/workspace/.g5ar-env01/bin/dasm"
MODES = {"hybrid": (0,1,0), "vdel": (1,1,0), "singlecopy": (0,0,0), "missile": (0,49,1)}
cycles = [min(66,max(22,(x+48)//3)) for x in range(256)]
cycle_table = [" ORG $fa00","CyclesByPixel:"]
for i in range(0,256,16):
    cycle_table.append(" byte "+",".join(str(x) for x in cycles[i:i+16]))
tables = []
for i, (label, kind) in enumerate(zip(LABELS,TYPES)):
    tables.extend([f" ORG ${0xf600+i*0x100:04x}",f"{label}:"," ds 32,0",
                   " byte "+",".join(f"${int(row,2):02x}" for row in MASKS[kind])," ds 32,0"])
tables.extend(cycle_table)
Path("tables.inc").write_text("\n".join(tables)+"\n")
for name,(vdel,copies,missile) in MODES.items():
    path = Path("roms")/name
    path.parent.mkdir(exist_ok=True)
    source = path.with_suffix(".asm")
    source.write_text(f"ACTORS=5\nROWSPLIT=0\nVDEL={vdel}\nCOPIES={copies}\nMISSILE={missile}\n include \"kernel.asm\"\n")
    subprocess.run([BIN,str(source),"-f3",f"-o{path}.bank",f"-l{path}.lst",f"-s{path}.sym"],check=True)
    bank=path.with_suffix(".bank").read_bytes()
    assert len(bank)==4096
    path.with_suffix(".bin").write_bytes(bank*4)
