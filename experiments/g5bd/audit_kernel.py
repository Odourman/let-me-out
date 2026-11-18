"""Audit a Gopher-captured RIOT raster program, including indexed page timing."""
import json
from pathlib import Path
import sys

# Opcode: operand length, unbranched CPU cost in this raster loop.
OPS = {
    0x85: (1, 3), 0x86: (1, 3), 0x8D: (2, 4), 0xA5: (1, 3),
    0x19: (2, 4), 0xB9: (2, 4), 0xBE: (2, 4), 0x24: (1, 3),
    0xC8: (0, 2), 0xC0: (1, 2), 0xEA: (0, 2), 0xF0: (1, 2),
    0xD0: (1, 3), 0x4C: (2, 3),
}

def audit(code):
    assert len(code) == 64
    assert code[:2] == bytes([0x85, 0x02])
    offset, cycles = 0, 0
    indexed = []
    while offset < len(code):
        op = code[offset]
        size, cost = OPS[op]
        next_offset = offset + 1 + size
        operand = int.from_bytes(code[offset + 1:next_offset], "little")
        cycles += cost
        if op in (0xB9, 0xBE, 0x19):
            # Every active raster row uses Y from 0 to 23.
            assert (operand & 255) + 23 <= 255, (offset, operand)
            indexed.append(f"${operand:04x}")
        if op == 0x4C:
            assert operand == 0xB8, operand
            assert code[next_offset] == 0x60
            break
        if op == 0xD0:
            loop_entry = next_offset + operand - 256
            if loop_entry == 2:
                assert code[next_offset] == 0x60
                cycles -= 3  # WSYNC is an entry instruction, not in the loop.
                assert cycles == 76, cycles
            else:
                assert loop_entry == 0, operand
                assert code[next_offset:next_offset+3] == bytes([0x85, 0x02, 0x60])
            break
        offset = next_offset
    else:
        raise ValueError("no loop terminator before RIOT reserve ends")
    assert cycles <= 76, cycles
    size = next_offset + (3 if op == 0xD0 and loop_entry == 0 else 1)
    assert 0xB8 + size <= 0xF8
    return dict(active_cycles_including_wsync=cycles, emitted_bytes=size,
                reserved_bytes=64, indexed_sources=indexed)

for name in sys.argv[1:]:
    path = Path(name)
    records = [json.loads(line) for line in path.read_text().splitlines()]
    code = next(bytes.fromhex(record["hex"]) for record in records if record["event"] == "ram_kernel")
    print(json.dumps(dict(trace=path.name, **audit(code))))
