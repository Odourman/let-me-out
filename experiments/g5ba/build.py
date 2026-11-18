"""Build three F6 diagnostics from one 6502 source and frozen masks."""
from pathlib import Path
import json
import subprocess

MASKS = json.loads(Path("masks.json").read_text())["sprites"]
TYPES = ("large_male","large_female","small_male","small_female")
LABELS = ("Male","Female","SmallM","SmallF")
BIN = "/workspace/.g5ar-env01/bin/dasm"
MODES = {"pair": (2,0), "hybrid": (5,0), "rowprobe": (2,1)}
cycles = [min(66,max(22,(x+48)//3)) for x in range(256)]
tables = [" ORG $f500","CyclesByPixel:"]
for i in range(0,256,16):
    tables.append(" byte "+",".join(str(x) for x in cycles[i:i+16]))
for i, (label, kind) in enumerate(zip(LABELS,TYPES)):
    tables.extend([f" ORG ${0xf600+i*0x100:04x}",f"{label}:"," ds 32,0",
                   " byte "+",".join(f"${int(row,2):02x}" for row in MASKS[kind])," ds 32,0"])
Path("tables.inc").write_text("\n".join(tables)+"\n")
for name,(count,rowsplit) in MODES.items():
    path = Path("roms")/name
    path.parent.mkdir(exist_ok=True)
    source = path.with_suffix(".asm")
    source.write_text(f"ACTORS={count}\nROWSPLIT={rowsplit}\n include \"kernel.asm\"\n")
    subprocess.run([BIN,str(source),"-f3",f"-o{path}.bank",f"-l{path}.lst",f"-s{path}.sym"],check=True)
    bank=path.with_suffix(".bank").read_bytes()
    assert len(bank)==4096
    path.with_suffix(".bin").write_bytes(bank*4)
