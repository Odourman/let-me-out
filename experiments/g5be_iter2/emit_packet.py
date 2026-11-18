"""Convert Z3 instruction witnesses into DASM stencils with runtime byte patches."""
import json
from pathlib import Path

RECORDS = Path("evidence/brief/solver.jsonl")
CONST = {"white":14,"yellow":30,"off":0}


def pad(delta):
    if delta % 2:
        assert delta >= 3
        yield " bit FRAME"
        delta-=3
    for _ in range(delta//2):
        yield " nop"


def section(record):
    suffix = record["clocks"][3]
    lines = [f"Packet{suffix}:", " sta WSYNC", " iny"]
    cursor = 2
    registers = record["registers"]
    for start, name, duration, _ in record["instructions"]:
        lines.extend(pad(start-cursor))
        cursor=start+duration
        if name.startswith("load_"):
            value=name[5:]
            reg="x" if registers[value] else "a"
            if value=="p0":
                lines.append(f" ld{reg} PlayerRows,y")
            else:
                if value.startswith("m"):
                    lines.append(f"Packet{suffix}_{value}:")
                lines.append(f" ld{reg} #{CONST.get(value,0)}")
            continue
        if name.startswith("resp"):
            register="RESP1"
            reg="y"
        else:
            if name.startswith("grp1"):
                register,value="GRP1","m"+name[-1]
            else:
                register,value={
                    "grp0_p0":("GRP0","p0"),"grp0_f":("GRP0","m2"),
                    "enam0_off":("ENAM0","off"),"enam0_on":("ENAM0","yellow"),
                    "colup0_white":("COLUP0","white"),"colup0_yellow":("COLUP0","yellow"),
                }[name]
            reg="x" if registers[value] else "a"
        if duration==4 and reg!="a":
            # STX/STY absolute are real 6507 opcodes too.
            assert reg in ("x","y")
        lines.append(f" st{reg}.{'w' if duration==4 else 'b'} {register}")
    lines.extend(pad(71-cursor))
    lines += [" rts", f"Packet{suffix}End:",
              f" IF Packet{suffix}End-Packet{suffix} > 64", " ERR", " ENDIF"]
    lines.append(f"Packet{suffix}Offsets:")
    lines.append(" byte "+",".join(f"Packet{suffix}_m{i}-Packet{suffix}+1" for i in range(5)))
    return lines


def emit():
    records = [json.loads(line) for line in RECORDS.read_text().splitlines()]
    selected = [r for r in records if r["family"]=="p0-share" and r["status"]=="sat" and r["packet"]]
    selected.sort(key=lambda r:r["clocks"][3])
    assert [r["clocks"][3] for r in selected]==[48,49,50]
    lines = ["; Generated from evidence/brief/solver.jsonl by emit_packet.py."]
    for record in selected:
        lines.extend(section(record))
    for name,fmt in (
        ("PacketLo","<Packet{}"),("PacketHi",">Packet{}"),
        ("PacketSize","Packet{0}End-Packet{0}"),
        ("PacketPatchLo","<Packet{}Offsets"),("PacketPatchHi",">Packet{}Offsets"),
    ):
        lines += [name+":"," byte "+",".join(fmt.format(i) for i in (48,49,50))]
    Path("packet.inc").write_text("\n".join(lines)+"\n")


if __name__=="__main__":
    emit()
