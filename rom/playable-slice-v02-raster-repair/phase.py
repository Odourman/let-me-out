"""Correlate physical beam position with program stages and deepest wall check."""
import argparse
from pathlib import Path
import re
from time import monotonic

from capture import BIN,Session,record


def symbols(path):
    return {parts[0]:parts[1] for line in path.read_text().splitlines()
            if len(parts:=line.split())>=2 and re.fullmatch(r"[0-9a-f]{4}",parts[1])}


def stop_at(s, addr):
    s.command(f"BREAK PC 0x{addr}")
    reply=s.command("RUN")
    assert f"break on PC->0x{addr}".encode() in reply
    s.command("DROP BREAK 0")
    return s.command("TV").decode().strip()


def measure(s, video, logic, max_x):
    for _ in range(24):
        s.command("STEP FRAME")
    if max_x:
        for i in range(5):
            s.command(f"POKE 0x{0xa0+i:04x} 0x{'ff' if i==0 else '00'}")
        for addr,value in ((0x91,148),(0x96,90),(0xb3,1)):
            s.command(f"POKE 0x{addr:04x} 0x{value:02x}")
        for _ in range(2):
            s.command("STEP FRAME")
        for label in ("NpcSetupFirst","NpcSetupSync","GlyphStart"):
            record("phase",label=label,tv=stop_at(s,video[label]))
            if label != "NpcSetupSync":
                s.command("STEP INSTRUCTION")
                record("phase",label=label+"-executed",tv=s.command("TV").decode().strip())
        return
    for label in ("Frame","BlankWait","Top","Room","RoomEnd","Bottom","GameBank","Overscan","Frame"):
        record("phase",label=label,tv=stop_at(s,video[label]),frame=s.command("TV FRAME").decode().strip())
    s.command("STICK LEFT RIGHT")
    for _ in range(12):
        tv=stop_at(s,logic["HitPoint"])
        if int(re.search(r"SL=(\d+)",tv)[1])>=228:
            record("stack",tv=tv,cpu=s.command("CPU").decode().strip())
            break
    else:
        raise AssertionError("bank 1 collision breakpoint not reached during overscan")


def raster_profile(s, video):
    for _ in range(24):
        s.command("STEP FRAME")
    targets=("NextRoom","NpcPreSync","NpcSetupSync","RoomFinish")
    names={video[name]:name for name in targets}
    for address in names:
        s.command(f"BREAK PC 0x{address}")
    last_frame=None
    found=0
    while True:
        hit=s.command("RUN")
        match=re.search(rb"break on PC->0x([0-9a-f]+)",hit)
        assert match,hit
        name=names[match[1].decode()]
        tv=s.command("TV").decode().strip()
        frame=int(re.search(r"FR=(\d+)",tv)[1])
        if last_frame is None:
            last_frame=frame
        if frame!=last_frame:
            break
        timing=s.command("TIA").decode().strip()
        record("raster",label=name,tv=tv,tia=timing)
        found+=1
    assert found>=175,found


def transitions(s,video,mode):
    for _ in range(24):
        s.command("STEP FRAME")
    if mode=="assist":
        coords=(90,30,60,50,81,153,45,60,82,86)
        changes={0xb3:1,0x80:24,0x81:159}
        labels=("AssistStart","AssistSync","AssistMove")
    elif mode=="cap":
        coords=(64,67,72,53,78,151,47,60,82,86)
        changes={0xb3:1,0x80:4,0x81:100}
        labels=("BridgePreSync","CapSFReset","CapLateMotion","CapLateSync","CapGlyph","CapHeadDisable","GlyphP1","NextRoom")
    elif mode=="key-assist":
        coords=(90,30,60,59,120,20,48,96,148,118)
        changes={0xb3:1,0x80:123,0x81:159,0xaf:1,0xb0:85,0xb1:153}
        labels=("KeyAssistStart","KeyAssistPosition","AssistInstallRegisters")
    else:
        coords=(61,102,84,58,85,74,79,119,146,153)
        changes={0xb3:1,0x80:12,0x81:159,0xa4:0,0xaf:1,0xb0:85,0xb1:153}
        labels=("BridgePreSync","NpcSetupFirst","NpcSetupSync","GlyphStart")
    changes.update({0x91+i:value for i,value in enumerate(coords)})
    for address,value in changes.items():
        s.command(f"POKE 0x{address:04x} 0x{value:02x}")
    for _ in range(3):
        s.command("STEP FRAME")
    for label in labels:
        stamp=stop_at(s,video[label])
        record("transition",mode=mode,label=label,tv=stamp,cpu=s.command("CPU").decode().strip())


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("rom",type=Path)
    p.add_argument('--max-x',action='store_true')
    p.add_argument('--raster',action='store_true')
    p.add_argument('--transition',choices=('assist','bridge','key-assist','cap'))
    a=p.parse_args()
    a.rom=a.rom.resolve()
    with Session([str(BIN),"HEADLESS",str(a.rom)],"slice-phase") as s:
        s.receive(monotonic()+30)
        video=symbols(a.rom.with_name("video.sym"))
        if a.transition:
            transitions(s,video,a.transition)
        elif a.raster:
            raster_profile(s,video)
        else:
            measure(s,video,symbols(a.rom.with_name("logic.sym")),a.max_x)
