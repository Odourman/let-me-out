"""Build the four F6 banks; each has identical blanking and dispatch code."""
from pathlib import Path
import argparse
import subprocess

from generate import dynamic
RIGHT = (127, 130, 133, 136)


def build(name, initial_right=127, initial_third=73, rows=11, mixed=False):
    out = Path("roms")
    out.mkdir(exist_ok=True)
    banks = []
    positions = ((127,100),(127,97),(127,103),(133,103)) if mixed else tuple((x,100) for x in RIGHT)
    for bank,(right,fourth) in enumerate(positions):
        stem=out/f"{name}-bank{bank}"
        include = stem.with_suffix(".inc")
        include.write_text(dynamic(right,rows,fourth))
        source = stem.with_suffix(".asm")
        source.write_text(Path("kernel.asm").read_text().replace('"dynamic.inc"', f'"{include}"'))
        subprocess.run(["/workspace/.g5ar-env01/bin/dasm",str(source),"-DDYNAMIC=1",f"-DROWS={rows}",f"-DMIXED={int(mixed)}",
                        f"-DBOOT_X={initial_third}",f"-DBOOT_RIGHT={initial_right}",
                        "-f3",f"-o{stem}.bank",f"-l{stem}.lst",f"-s{stem}.sym"],check=True)
        data=stem.with_suffix(".bank").read_bytes()
        assert len(data)==4096
        banks.append(data)
    (out/f"{name}.bin").write_bytes(b"".join(banks))


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--name",default="outer")
    p.add_argument("--right",type=int,default=127)
    p.add_argument("--third",type=int,default=73)
    p.add_argument("--rows",type=int,choices=(11,17),default=11)
    p.add_argument("--mixed",action="store_true")
    args=p.parse_args()
    build(args.name,args.right,args.third,args.rows,args.mixed)
