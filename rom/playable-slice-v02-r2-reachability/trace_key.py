"""Trace the key selection decision and the resulting visible-line path."""
import argparse
from pathlib import Path
from time import monotonic

from capture import BIN, Session, record
from phase import stop_at, symbols

parser = argparse.ArgumentParser()
parser.add_argument("rom", type=Path)
parser.add_argument("px", type=int)
parser.add_argument("py", type=int)
parser.add_argument("--early-p1-probe", action="store_true")
args = parser.parse_args()
rom = args.rom.resolve()
edge = rom.stem.rsplit("-", 1)[-1]
video = symbols(rom.with_name(f"{edge}-video.sym"))
with Session([str(BIN), "HEADLESS", str(rom)], "key-decision") as session:
    session.receive(monotonic() + 30)
    for _ in range(24):
        session.command("STEP FRAME")
    values = {0xb3: 1, 0x80: args.px, 0x81: args.py, 0x84: 0,
              0xaf: 1, 0xb0: 85, 0xb1: 153}
    values.update({0x91 + i: v for i, v in enumerate((90,30,60,59,120,20,48,96,148,118))})
    for address, value in values.items():
        session.command(f"POKE 0x{address:04x} 0x{value:02x}")
    for _ in range(3):
        session.command("STEP FRAME")
    selected = args.py >= 159
    labels = ("PrepareKeyAssist", "KeyAssistPlayer")
    labels += ("InstallKeyAssist", "KeyAssistStart", "KeyAssistGrpOld", "KeyAssistHmp0",
               "KeyAssistResp0", "KeyAssistHmp1", "KeyAssistMove", "KeyAssistGrpNew",
               "AssistInstallRegisters") if selected else (
                   "KeyAssistRejected", "BridgeFloorKey", "BridgeReject")
    if args.early_p1_probe:
        labels = ("BridgeFloorKey", "AppendBridge", "BridgePreSync", "NpcSetupFirst",
                  "NpcSetupSync", "GlyphStart", "GlyphP1")
    for label in labels:
        record("key_trace", label=label, px=args.px, py=args.py,
               tv=stop_at(session, video[label]), cpu=session.command("CPU").decode().strip(),
               tia=session.command("TIA").decode().strip())
