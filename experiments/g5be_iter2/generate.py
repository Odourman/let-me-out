"""Chain the previously measured c49 instruction stencil without per-row RTS."""
from pathlib import Path
import json,re

MASKS=json.loads(Path("masks.json").read_text())["sprites"]
KINDS=("large_male","large_male","large_female","small_male","small_female")
ORDER=(1,4,2,3,0)
YS=(73,72,73,71,72)
SCENES=((76,77),(74,78),(71,81))

def build():
    code=Path("frozen-packet.inc").read_text().split("Packet49:\n",1)[1].split("Packet49End:",1)[0]
    code=code.splitlines()[1:-1] # entry WSYNC and terminal RTS
    out=[]
    for i,(start,end) in enumerate(SCENES):
        out += [f"Scene{i}:", " sta WSYNC"]
        for row in range(start,end+1):
            out.append(f"Scene{i}Y{row}:")
            slot=None
            for line in code:
                m=re.fullmatch(r"Packet49_m(\d):",line)
                if m:
                    slot=int(m[1])
                    continue
                if slot is not None:
                    actor=ORDER[slot]
                    index=row-YS[actor]
                    mask=int(MASKS[KINDS[actor]][index],2) if 0<=index<9 else 0
                    line=line.replace("#0",f"#${mask:02x}")
                    slot=None
                out.append(line)
            out.extend((" nop"," jmp LeaveBand") if row==end else (" bit FRAME"," nop"))
    for tag,values in (
        ("Starts",[str(a) for a,b in SCENES]),
        ("SceneLo",[f"<Scene{i}" for i in range(3)]),
        ("SceneHi",[f">Scene{i}" for i in range(3)]),
    ):
        out += [tag+":"," byte "+",".join(values)]
    return "\n".join(out)+"\n"

def dynamic():
    from emit_packet import pad
    records=[json.loads(line) for line in Path("solver.jsonl").read_text().splitlines()]
    records=[r for r in records if r["fetch"]==3 and r["status"]=="sat"]
    out=[]
    for r in records:
        clock=r["clocks"][3]
        suffix=str(clock)
        ops=stencil(r)
        out += [f"Dynamic{clock}:", " sta WSYNC"]
        for i in range(11):
            out.append(f"Dynamic{clock}Y{71+i}:")
            for line in ops:
                for slot in range(5):
                    line=line.replace(f"cache{slot}",f"CACHE+{slot*11+i}")
                out.append(line)
            end=max(start+duration for start,_,duration,_ in r["instructions"])
            if i==10 and end<=73 and 73-end!=1:
                out.extend(pad(73-end))
            else:
                out.extend(pad(76-end))
            if i==10:
                out.append(" jmp LeaveBand")
        out.append(f"Dynamic{suffix}End:")
    for key,fmt in (("DynamicLo","<Dynamic{}"),("DynamicHi",">Dynamic{}")):
        out += [key+":"," byte "+",".join(fmt.format(c) if any(r["clocks"][3]==c for r in records) else "0"
                                        for c in (48,49,50))]
    out += ["DynamicClocks:"," byte "+",".join("1" if any(r["clocks"][3]==c for r in records) else "0" for c in (48,49,50))]
    for i,kind in enumerate(KINDS):
        # Each lookup stays on-page for all admitted Y values and rows.
        out += [" ALIGN 32",f"Mask{i}:", " ds 2,0",
                " byte "+",".join(f"${int(row,2):02x}" for row in MASKS[kind])," ds 2,0"]
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
        elif name.startswith("resp"):
            out.append(f" sty.{'w' if duration==4 else 'b'} RESP1")
        else:
            register,value=("GRP1","m"+name[-1]) if name.startswith("grp1_") else stores[name]
            out.append(f" st{'x' if registers[value] else 'a'}.{'w' if duration==4 else 'b'} {register}")
    return out


if __name__=="__main__":
    Path("chain.inc").write_text(build())
    Path("dynamic.inc").write_text(dynamic())
