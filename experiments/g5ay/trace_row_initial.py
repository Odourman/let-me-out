"""Measure actual Gopher TIA bus-event order in a bounded raster slice."""
import re
from pathlib import Path
import time
from capture import BIN, Session, Rejected, expect

directory = Path("packedcopies")
symbols = (directory / "bank0.sym").read_text().splitlines()
address = next(line.split()[1] for line in symbols if line.startswith("LineAll_74 "))
rom = (directory / "g5ay_packedcopies_F6.bin").resolve()
with Session([str(BIN), "HEADLESS", str(rom)], "gopher-trace") as session:
    session.receive(time.monotonic()+15)
    expect(session, "VERSION REVISION", rb"v0\.57\.2\n2af86eb725739adbf3d9d45cea2ed69eea57da2a\n")
    for _ in range(4):
        session.command("STEP FRAME")
    expect(session, "CARTRIDGE MAPPED", rb"Bank: 0\n")
    expect(session, f"BREAK PC 0x{address}", rb"")
    expect(session, "LIST BREAKS", rb"breakpoints:\n 0: PC->0x" + address.encode() + rb"\n")
    expect(session, "RUN", rb"break on PC->0x" + address.encode() + rb"\n")
    expect(session, "DROP BREAK 0", rb"breakpoint #0 dropped\n")
    for register in ("RESP1", "GRP1", "GRP0", "ENAM0"):
        expect(session, f"TRACE {register}", rb"")
    session.command("LIST TRACES")
    for _ in range(5):
        expect(session, "TV", rb"FR=\d+ SL=\d+ CL=-?\d+\n")
        response = session.command("STEP SCANLINE")
        if b"write" not in response:
            raise Rejected(f"no bus write in scanline trace: {response!r}")
    expect(session, "TV", rb"FR=\d+ SL=\d+ CL=-?\d+\n")
