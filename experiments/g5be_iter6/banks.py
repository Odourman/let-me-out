"""Report standard F6 bank lengths and free contiguous space before hotspots."""
import json
from pathlib import Path

from beam import sym

families=("direct","combined")
for family in families:
    rom=Path(f"roms/{family}.bin").read_bytes()
    assert len(rom)==16384
    for bank in range(4):
        path=Path(f"roms/{family}-bank{bank}")
        table=sym(path.with_suffix(".sym"))
        bank_bytes=path.with_suffix(".bank").read_bytes()
        assert len(bank_bytes)==4096 and bank_bytes==rom[4096*bank:4096*(bank+1)]
        last=int(table["PlayerRows"],16)+(92 if family=="combined" else 89)-1
        assert last<0xfff6 and set(bank_bytes[last-0xf000+1:0xff6]) <= {0xff}
        print(json.dumps(dict(rom=family, bank=bank,length=len(bank_bytes),player_rows_end=f"{last:04x}",
                              trailing_bytes_before_hotspots=0xfff6-last-1)))
