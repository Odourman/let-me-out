"""Rebuild each archived fixture from its exact settings and check its pixels."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
target = Path(sys.argv[1]).resolve()
target.mkdir(parents=True, exist_ok=False)
for plan in sorted((root / "evidence").glob("*/plan.json")):
    options = json.loads(plan.read_text())["options"]
    out = target / plan.parent.name
    cmd = [sys.executable, str(root / "build_multirow.py"), str(out)]
    for name, value in options.items():
        if name == "out" or value is False:
            continue
        cmd.append("--" + name.replace("_", "-"))
        if value is not True:
            cmd.append(str(value))
    subprocess.run(cmd, check=True)
    assert (out / "probe.bin").read_bytes() == (plan.parent / "probe.bin").read_bytes(), out
    with (out / "raw.jsonl").open("w") as log:
        subprocess.run([sys.executable, str(root / "measure_multirow.py"), str(out / "probe.bin")],
                       stdout=log, check=True)
    subprocess.run([sys.executable, str(root / "check_map.py"), str(out)], check=True)
