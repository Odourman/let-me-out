"""Chain the previously measured c49 instruction stencil without per-row RTS."""
from pathlib import Path
import json,re

MASKS=json.loads(Path("masks.json").read_text())["sprites"]
KINDS=("large_male","large_male","large_female","small_male","small_female")
ORDER=(1,4,2,3,0)
YS=(73,72,73,71,72)
SCENES=((76,77),(74,78),(71,81))

THIRD_X = (73, 67, 76, 82, 64)


def dynamic(right, rows, fourth):
    from emit_packet import pad
    records=[json.loads(line) for line in Path("solver.jsonl").read_text().splitlines()]
    valid={r["x"]:r for r in records if r["right"] == right and r["fourth"] == fourth and r["fetch"] == 3 and r["status"] == "sat" and (rows==11 or r["x"] in (67,73,76))}
    out = []
    for x,r in valid.items():
        out += [f"Dynamic{x}:", " sta WSYNC"]
        ops = stencil(r)
        end = max(start+duration for start,_,duration,_ in r["instructions"])
        for i in range(rows):
            out.append(f"Dynamic{x}Y{71+i}:")
            for op in ops:
                for slot in range(5):
                    op = op.replace(f"cache{slot}", f"CACHE+{slot*rows+i}")
                out.append(op)
            out.extend(pad((73 if i==rows-1 else 76)-end))
            if i==rows-1:
                out.append(" jmp LeaveBand")
    out += ["ThirdXs:", " byte "+",".join(str(THIRD_X.index(x)) if x in THIRD_X else "$ff" for x in range(64,83))]
    for key,prefix in (("DynamicLo","<"),("DynamicHi",">")):
        out += [key+":", " byte "+",".join(f"{prefix}Dynamic{x}" if x in valid else "0" for x in THIRD_X)]
    out += ["DynamicClocks:", " byte "+",".join("1" if x in valid else "0" for x in THIRD_X)]
    for i,kind in enumerate(KINDS):
        out += [" ALIGN 32",f"Mask{i}:", f" ds {rows-9},0",
                " byte "+",".join(f"${int(row,2):02x}" for row in MASKS[kind]),f" ds {rows-9},0"]
    out += ["MaskLo:"," byte "+",".join(f"<Mask{i}" for i in range(5)),
            "MaskHi:"," byte "+",".join(f">Mask{i}" for i in range(5))]
    return "\n".join(out)+"\n"


def stencil(record):
    from emit_packet import pad
    out=[" iny"]
    cursor=2
    registers=record["registers"]
    constants={"white":14,"yellow":30,"off":0}
    stores={
        "grp0_p0":("GRP0","p0"),"grp0_f":("GRP0","m2"),
        "enam0_off":("ENAM0","off"),"enam0_on":("ENAM0","yellow"),
        "colup0_white":("COLUP0","white"),"colup0_yellow":("COLUP0","yellow"),
    }
    for start,name,duration,_ in record["instructions"]:
        out.extend(pad(start-cursor))
        cursor=start+duration
        if name.startswith("load_"):
            value=name[5:]
            reg="x" if registers[value] else "a"
            if value=="p0":
                out.append(f" ld{reg} PlayerRows,y")
            elif value.startswith("m"):
                out.append(f" ld{reg}.b cache{value[-1]}")
            else:
                out.append(f" ld{reg} #{constants[value]}")
        elif name in ("reset_p0", "move_p0"):
            out.append(f" sty.{'w' if duration==4 else 'b'} RESP0")
        elif name.startswith("resp"):
            out.append(f" sty.{'w' if duration==4 else 'b'} RESP1")
        else:
            register,value=("GRP1","m"+name[-1]) if name.startswith("grp1_") else stores[name]
            out.append(f" st{'x' if registers[value] else 'a'}.{'w' if duration==4 else 'b'} {register}")
    return out
