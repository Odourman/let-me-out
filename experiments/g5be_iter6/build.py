"""Build the four F6 banks; each has identical blanking and dispatch code."""
from pathlib import Path
import argparse
import subprocess

from generate import dynamic
from layouts import DIRECT, COMBINED

def build(name, initial_right=127, initial_third=73, rows=11, unified=False, initial_second=46, initial_fourth=100, segmented=False, boot_far=False, initial_first=19):
    out = Path("roms")
    out.mkdir(exist_ok=True)
    banks = []
    positions = COMBINED if unified else DIRECT
    firsts=[row[0] for row in positions]
    geometry=out/f"{name}-geometry.inc"
    lo,hi=min(firsts),max(firsts)
    tables=("FIRST_MIN="+str(lo), "FIRST_SPAN="+str(hi-lo+1),
            "FirstBank:", " byte "+",".join(str(firsts.index(x)) if x in firsts else "$ff" for x in range(lo,hi+1)))
    lines=list(tables)
    for i,label in enumerate(("SecondX","FourthX","RightX"),1):
        lines.extend((label+":", " byte "+",".join(str(row[i]) for row in positions)))
    geometry.write_text("\n".join(lines)+"\n")
    for bank,(first,second,fourth,right) in enumerate(positions):
        stem=out/f"{name}-bank{bank}"
        include = stem.with_suffix(".inc")
        include.write_text(dynamic(first,second,right,rows,fourth,segmented))
        source = stem.with_suffix(".asm")
        source.write_text(Path("kernel.asm").read_text().replace('"dynamic.inc"', f'"{include}"').replace('"geometry.inc"',f'"{geometry}"'))
        subprocess.run(["/workspace/.g5ar-env01/bin/dasm",str(source),"-DDYNAMIC=1",f"-DROWS={rows}",f"-DUNIFIED={int(unified)}",f"-DSEGMENTED={int(segmented)}",f"-DBOOT_FAR={int(boot_far)}",
                        f"-DBOOT_SECOND={initial_second}",f"-DBOOT_FOURTH={initial_fourth}",f"-DBOOT_FIRST={initial_first}",f"-DBOOT_X={initial_third}",f"-DBOOT_RIGHT={initial_right}",
                        "-f3",f"-o{stem}.bank",f"-l{stem}.lst",f"-s{stem}.sym"],check=True)
        data=stem.with_suffix(".bank").read_bytes()
        assert len(data)==4096
        banks.append(data)
    (out/f"{name}.bin").write_bytes(b"".join(banks))


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--name",default="direct")
    p.add_argument("--right",type=int,default=127)
    p.add_argument("--third",type=int,default=73)
    p.add_argument("--rows",type=int,choices=(11,17),default=11)
    p.add_argument("--unified",action="store_true")
    p.add_argument("--second",type=int,default=46)
    p.add_argument("--fourth",type=int,default=100)
    p.add_argument("--segmented",action="store_true")
    p.add_argument("--boot-far",action="store_true")
    p.add_argument("--first",type=int,default=19)
    args=p.parse_args()
    build(args.name,args.right,args.third,args.rows,args.unified,args.second,args.fourth,args.segmented,args.boot_far,args.first)
