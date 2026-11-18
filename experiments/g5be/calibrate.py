"""Check the schedule front-end against four frozen developer observations."""
import json
from pathlib import Path
from audit_kernel import audit, OPS

REFERENCE={
    "positive": ([22,31,40,49,58], [25,43,52,61], (0,0), 5),
    "phaseprobe": ([22,31,40,49,58], [15,34,37,52,65], (5,20), 5),
    "shareearly": ([22,31,58], [16,38,53], (20,1), 4),
    "shadow": ([31,40,58], [21,34,55], (48,0), 3),
}


def decode(ram):
    resp, grp, offset, cycle = [], [], 2, 0
    while offset<len(ram):
        op=ram[offset]
        if op in (0x60,0x4C,0xD0):
            break
        n,cost=OPS[op]
        target=int.from_bytes(ram[offset+1:offset+1+n],"little")
        cycle+=cost
        if op in (0x85,0x86,0x84,0x8d,0x8e,0x8c):
            if target==0x11:
                resp.append(cycle)
            elif target==0x1c:
                grp.append(cycle)
        offset+=n+1
    return resp,grp


for mode,(resp,grp,pixels,slots) in REFERENCE.items():
    rows=[json.loads(s) for s in (Path("calibration")/f"{mode}.jsonl").read_text().splitlines()]
    ram=bytes.fromhex(next(r["hex"] for r in rows if r["event"]=="ram_kernel"))
    timings=[r for r in rows if r["event"]=="raster_timing"]
    status=audit(ram)
    assert decode(ram)==(resp,grp), (mode,decode(ram))
    assert len(timings)==24
    assert all(r["resp"]==resp and set(r["grp"])<=set(grp) for r in timings)
    # Pixel outcomes are independent frozen observations, never produced
    # by the scheduler or by fitting its timing envelope post hoc.
    print(json.dumps(dict(case=mode,resp1=resp,grp1_decoded=grp,
                          observed_slots=slots,frozen_pixels=pixels,
                          emulator_traced_rows=24,**status)))
