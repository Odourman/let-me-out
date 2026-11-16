#!/usr/bin/env python3
"""Exact C02 source -> TIA PF tables for isolated NTSC v0.18/R3."""
from pathlib import Path
import json, hashlib
HERE=Path(__file__).resolve().parent.parent
REPO=HERE.parents[3]
SOURCE=REPO/"design/PLANERADE_RUMSKARTOR_V011.json"
obj=json.loads(SOURCE.read_text(encoding="utf-8"))
room=next(x for x in obj["rooms"] if x.get("selected_layout_id")=="C02")
g=room["grid"]
assert len(g)==22 and all(len(s)==40 for s in g)
assert all(s[0]=="#" for s in g)
assert [y for y in range(22) if g[y][39]=="D"]==[9,10,11,12]
assert all(g[y][39]=="#" for y in range(22) if y not in (9,10,11,12))
assert all(g[y][38]=="." for y in (9,10,11,12))
assert room["door"]["x"]==39 and room["door"]["rows"]==[9,10,11,12]
def encode_half(a):
    assert len(a)==20
    return [sum(a[i]<<(4+i) for i in range(4)),
            sum(a[4+i]<<(7-i) for i in range(8)),
            sum(a[12+i]<<i for i in range(8))]
def pf_values(row):
    b=[int(s=="#") for s in row]
    return encode_half(b[:20])+encode_half(b[20:])
wall_data=[[],[],[],[],[],[]]
door_data=[]
for rowidx,row in enumerate(g):
    vals=pf_values(row)
    for scan in range(8):
        for i,v in enumerate(vals):
            wall_data[i].append(v)
        if rowidx in (9,10,11,12):
            z=(rowidx-9)*8+scan
            # 8px-wide orange P1; transparent black keyhole: round head + narrow shaft.
            keyhole={10:0xE7,11:0xC3,12:0xC3,13:0xC3,
                     14:0xE7,15:0xE7,16:0xEF,17:0xEF,
                     18:0xEF,19:0xEF,20:0xEF}
            door_data.append(keyhole.get(z,0xFF))
        else:
            door_data.append(0)
assert all(len(x)==176 for x in wall_data+[door_data])
out=HERE/"dist"
out.mkdir(parents=True,exist_ok=True)
names=["LEFT0","LEFT1","LEFT2","RIGHT0","RIGHT1","RIGHT2","DOORROWS"]
text=["; Generated from "+str(SOURCE.relative_to(REPO)),
      "; exact JSON SHA256 "+hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
      "; C02 no map alteration, 22*8=176 physical scanlines.",
      " ORG $F600"]
for name,arr in zip(names,wall_data+[door_data]):
    text.append(name+":")
    for start in range(0,len(arr),16):
        text.append(" BYTE "+",".join("$%02X"%n for n in arr[start:start+16]))
(out/"r3_tables.inc").write_text("\n".join(text)+"\n",encoding="ascii")
(out/"source_geometry.json").write_text(json.dumps({
 "source_path":str(SOURCE.relative_to(REPO)),
 "source_sha256":hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
 "selected_layout_id":room["selected_layout_id"],"grid_exact":g,
 "left_wall_every_row":True,"right_door_cells":[[39,y] for y in range(9,13)],
 "right_locked_PF_D_cells":"open for P1 overlay, logic remains locked until unlock",
 "door_P1_nominal_colorclocks":[152,159],"raster_map_physical_lines":176,
 "generated_PF_register_bytes":1056,"generated_P1_door_mask_bytes":176
},indent=2,ensure_ascii=False)+"\n")
print("Exact C02 source verified, table bytes:",7*176)
