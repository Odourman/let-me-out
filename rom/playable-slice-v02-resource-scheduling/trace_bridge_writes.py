"""Trace the actual P1 bridge on the separated-X fixture."""
import argparse
import re
from pathlib import Path
from time import monotonic

from capture import BIN, Session, record
from phase import stop_at, symbols

parser = argparse.ArgumentParser()
parser.add_argument("rom", type=Path)
a = parser.parse_args()
rom = a.rom.resolve()
syms = symbols(rom.with_name("top-video.sym"))
with Session([str(BIN), "HEADLESS", str(rom)], "bridge-writes") as session:
    session.receive(monotonic()+30)
    for _ in range(24):
        session.command("STEP FRAME")
    values = {0xb3: 1, 0x80: 24, 0x81: 151, 0x84: 0, 0xaf: 1, 0xb0: 85, 0xb1: 153}
    values.update({0x91+i: value for i, value in enumerate((90,30,60,59,120,20,48,96,148,118))})
    for address, value in values.items():
        session.command(f"POKE 0x{address:04x} 0x{value:02x}")
    for _ in range(3):
        session.command("STEP FRAME")
    for target in ("GRP0", "GRP1", "RESP1", "HMP1", "HMOVE", "COLUP1", "VDELP1"):
        session.command(f"TRACE {target}")
    stop_at(session, syms["BridgePreSync"])
    for _ in range(75):
        before = session.command("TV").decode().strip()
        cpu = session.command("CPU").decode().strip()
        instruction = session.last_prompt
        reply = session.command("STEP INSTRUCTION").decode().strip()
        prompt = instruction.decode() if isinstance(instruction, bytes) else instruction
        write = re.search(r"\bst[axy] (?:\$(?:02|10|11|1b|1c|20|21|25|26|2a|06|07)|grp[01]|resp[01]|hmp[01]|hmove|vdelp[01]|colup[01])\b", prompt, re.I)
        if write or "(TIA)" in reply:
            record("bridge_write", before=before, after=session.command("TV").decode().strip(),
                   cpu=cpu, instruction=prompt, reply=reply)
        if f"PC={int(syms['GlyphP1'],16)+8:04x}" in cpu:
            break
