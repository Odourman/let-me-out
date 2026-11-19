"""Build the four F6 banks; each has identical blanking and dispatch code."""
from pathlib import Path
import argparse
import subprocess

from generate import dynamic
LEFT = ((46,100,127),(43,100,127),(49,100,127),(52,100,127))
UNIFIED = ((46,100,127),(43,97,127),(49,103,133),(52,100,136))


def build(name, initial_right=127, initial_third=73, rows=11, unified=False, initial_second=46, initial_fourth=100, segmented=False, boot_far=False):
    out = Path("roms")
    out.mkdir(exist_ok=True)
    banks = []
    positions = UNIFIED if unified else LEFT
    for bank,(second,fourth,right) in enumerate(positions):
        stem=out/f"{name}-bank{bank}"
        include = stem.with_suffix(".inc")
        include.write_text(dynamic(second,right,rows,fourth,segmented))
        source = stem.with_suffix(".asm")
        source.write_text(Path("kernel.asm").read_text().replace('"dynamic.inc"', f'"{include}"'))
        subprocess.run(["/workspace/.g5ar-env01/bin/dasm",str(source),"-DDYNAMIC=1",f"-DROWS={rows}",f"-DUNIFIED={int(unified)}",f"-DSEGMENTED={int(segmented)}",f"-DBOOT_FAR={int(boot_far)}",
                        f"-DBOOT_SECOND={initial_second}",f"-DBOOT_FOURTH={initial_fourth}",f"-DBOOT_X={initial_third}",f"-DBOOT_RIGHT={initial_right}",
                        "-f3",f"-o{stem}.bank",f"-l{stem}.lst",f"-s{stem}.sym"],check=True)
        data=stem.with_suffix(".bank").read_bytes()
        assert len(data)==4096
        banks.append(data)
    (out/f"{name}.bin").write_bytes(b"".join(banks))


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--name",default="left")
    p.add_argument("--right",type=int,default=127)
    p.add_argument("--third",type=int,default=73)
    p.add_argument("--rows",type=int,choices=(11,17),default=11)
    p.add_argument("--unified",action="store_true")
    p.add_argument("--second",type=int,default=46)
    p.add_argument("--fourth",type=int,default=100)
    p.add_argument("--segmented",action="store_true")
    p.add_argument("--boot-far",action="store_true")
    args=p.parse_args()
    build(args.name,args.right,args.third,args.rows,args.unified,args.second,args.fourth,args.segmented,args.boot_far)
