"""Cycle ledger from the emitted 6507 bytes for each complete raster package."""
import json
import re
from pathlib import Path

COSTS = {
    0xc8: (1, 2), 0xb9: (3, 4), 0xbe: (3, 4),
    0xa9: (2, 2), 0xa2: (2, 2), 0xa5: (2, 3), 0xa6: (2, 3),
    0x85: (2, 3), 0x86: (2, 3), 0x84: (2, 3),
    0x8d: (3, 4), 0x8e: (3, 4), 0x8c: (3, 4),
    0x24: (2, 3), 0xea: (1, 2), 0x4c: (3, 3), 0x6c: (3, 5),
}
STORES = {0x85, 0x86, 0x84, 0x8d, 0x8e, 0x8c}


def audit(name):
    image = Path(f"roms/{name}.bank").read_bytes()
    symbols = {p[0]: int(p[1], 16) for line in Path(f"roms/{name}.sym").read_text().splitlines()
               if len(p := line.split()) >= 2 and re.fullmatch(r"[0-9a-f]{4}", p[1])}
    rows = sorted((address, label) for label, address in symbols.items()
                  if re.fullmatch(r"(?:Dynamic|Tail)\d+Y\d+", label))
    player = symbols["PlayerRows"]
    assert player >> 8 == (player + (91 if name.startswith("combined") else 88)) >> 8
    assert all(symbols[f"Mask{i}"] >> 8 == (symbols[f"Mask{i}"] + (31 if name.startswith("combined") else 24 if name.startswith("unified") else 12)) >> 8 for i in range(5))
    for i, (start, label) in enumerate(rows):
        group = label.partition("Y")[0]
        end = rows[i+1][0] if i+1 < len(rows) and rows[i+1][1].startswith(group + "Y") else None
        pc, cycles, writes, jumps = start, 0, [], []
        while pc != end:
            opcode = image[pc-0xf000]
            length, cost = COSTS[opcode]
            operand = int.from_bytes(image[pc-0xf000+1:pc-0xf000+length], "little")
            pc += length
            cycles += cost
            if opcode in {0xb9, 0xbe}:
                assert operand == player, (label, operand)
            if opcode in STORES:
                writes.append([cycles, f"{operand:02x}"])
            if opcode in (0x4c,0x6c):
                targets = (symbols["LeaveBand"],symbols.get("LeaveLong")) if opcode==0x4c else (symbols["ORDER"],)
                assert end is None and operand in targets
                jumps.append(cycles-cost)
                break
        # Schedule c0 means first instruction starts at the scanline boundary.
        assert cycles in (76, 79) and max(c for c, _ in writes) <= 76
        assert cycles <= 76 or jumps == [76]
        print(json.dumps(dict(rom=name, row=label, pc=f"{start:04x}", bytes=pc-start,
                              row_cycles=min(cycles, 76), transfer_next_row=cycles-76,
                              last_store=writes[-1][0], tia_writes=writes)))


if __name__ == "__main__":
    for family in ("direct", "combined"):
        for bank in range(4):
            audit(f"{family}-bank{bank}")
