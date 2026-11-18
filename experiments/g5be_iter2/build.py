from pathlib import Path
import subprocess

subprocess.run(["python","generate.py"],check=True)
out=Path("roms")
out.mkdir(exist_ok=True)
for mode, dynamic in (("chain",0),("stream",1)):
    subprocess.run(["/workspace/.g5ar-env01/bin/dasm","kernel.asm",f"-DDYNAMIC={dynamic}","-f3",
                    f"-oroms/{mode}.bank",f"-lroms/{mode}.lst",f"-sroms/{mode}.sym"],check=True)
    bank=(out/f"{mode}.bank").read_bytes()
    assert len(bank)==4096
    (out/f"{mode}.bin").write_bytes(bank*4)
