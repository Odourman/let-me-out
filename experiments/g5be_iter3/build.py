"""Assemble the two independently scheduled diagnostic F6 kernels."""
from pathlib import Path
import subprocess

from generate import dynamic

out = Path("roms")
out.mkdir(exist_ok=True)
for name, family in (("late-p0", "late-p0-relaxed"), ("all-p1", "all-p1")):
    include = out/f"{name}.inc"
    include.write_text(dynamic(family))
    source = out/f"{name}.asm"
    source.write_text(Path("kernel.asm").read_text().replace('"dynamic.inc"', f'"{include}"'))
    for boot in (73, 67, 76, 82, 64):
        fixture = name if boot == 73 else f"{name}-boot{boot}"
        subprocess.run(["/workspace/.g5ar-env01/bin/dasm",str(source),"-DDYNAMIC=1",f"-DBOOT_X={boot}",
                        "-f3",f"-oroms/{fixture}.bank",f"-lroms/{fixture}.lst",f"-sroms/{fixture}.sym"],check=True)
        bank = (out/f"{fixture}.bank").read_bytes()
        assert len(bank) == 4096
        (out/f"{fixture}.bin").write_bytes(bank*4)
