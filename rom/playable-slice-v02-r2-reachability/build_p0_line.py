"""Build isolated 262-line F6 probes with a second P0 register sequence."""
import argparse
from pathlib import Path
import subprocess

parser=argparse.ArgumentParser()
parser.add_argument("directory",type=Path)
parser.add_argument("--variant",choices=("final","resp-first","grp-first","timed-copy-unshifted"),default="final")
a=parser.parse_args()
a.directory=a.directory.resolve()
a.directory.mkdir(parents=True,exist_ok=True)
here=Path(__file__).resolve().parent
for name,x,first,second,delay,copies in (
        ("far-right",24,0x7e,0x38,0,0),
        ("near-right",60,0x7e,0x38,0,0),
        ("key-left",85,0x70,0x7e,3,0),
        ("far-timed-copy",24,0x7e,0x70,0,1),
        ("near-timed-copy",60,0x7e,0x70,0,1)):
    if copies and a.variant in ("resp-first","grp-first"):
        continue
    if not copies and a.variant=="timed-copy-unshifted":
        continue
    if name=="key-left" and a.variant=="resp-first":
        delay=1
    source="p0_line.asm" if a.variant=="final" else f"p0-variants/{a.variant}.asm"
    bank=a.directory/f"{name}.bank"
    fixed={ "FIRST_X":x,"FIRST_BITS":first,"SECOND_BITS":second,"DELAY":delay,"SECOND_COPY":copies}
    subprocess.run(["/workspace/.g5ar-env01/bin/dasm",source,
                    *(f"-D{k}={v}" for k,v in fixed.items()),"-f3",f"-o{bank}",
                    f"-s{a.directory/name}.sym"],cwd=here,check=True)
    data=bank.read_bytes()
    assert len(data)==4096
    (a.directory/f"{name}.bin").write_bytes(data*4)
