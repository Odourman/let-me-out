"""Single-process, single-RUN G5AW pilot adapted from G5AV."""
import argparse
from collections import Counter
import errno
import hashlib
import json
import os
from pathlib import Path
import pty
import re
import select
import subprocess
import sys
import tempfile
import termios
import time

BIN = Path("/workspace/.g5ar-env01/bin/gopher2600")
PROMPT = re.compile(rb"\[ ([^\[\]\r\n]{1,300}) \] (>>|>) ")
VEOF = b"\x04"
class Rejected(Exception):
    pass


def record(event, **data):
    print(json.dumps(dict(event=event, unix_ns=time.time_ns(), **data)), flush=True)


class Session:
    def __init__(self, argv, name, session_limit=420):
        self.argv, self.name = argv, name
        self.session_limit = session_limit
        self.offsets = {"tx": 0, "rx": 0}
        self.seq = 0

    def __enter__(self):
        self.master, slave = pty.openpty()
        try:
            config = termios.tcgetattr(slave)
            config[0] = 0
            config[1] = 0
            config[3] = termios.ICANON
            config[6][termios.VEOF] = VEOF
            termios.tcsetattr(slave, termios.TCSANOW, config)
            actual = termios.tcgetattr(slave)
            record("termios", name=self.name, iflag=actual[0], oflag=actual[1],
                   cflag=actual[2], lflag=actual[3], cc_hex=b"".join(actual[6]).hex())
            os.set_blocking(self.master, False)
            self.stderr = tempfile.TemporaryFile()
            self.home = tempfile.TemporaryDirectory()
            env = dict(os.environ, HOME=self.home.name, XDG_CONFIG_HOME=self.home.name,
                       XDG_DATA_HOME=self.home.name, XDG_CACHE_HOME=self.home.name)
            self.started = time.monotonic()
            record("launch", name=self.name, argv=self.argv, isolated_home=True)
            self.child = subprocess.Popen(self.argv, stdin=slave, stdout=slave,
                                          stderr=self.stderr, env=env, cwd=self.home.name,
                                          start_new_session=True)
            record("started", pid=self.child.pid)
        finally:
            os.close(slave)
        return self

    def __exit__(self, *_):
        stop = "already exited"
        try:
            if self.child.poll() is None:
                stop = "SIGTERM"
                self.child.terminate()
                try:
                    self.child.wait(timeout=min(0.5, max(0, 120 - self.elapsed())))
                except subprocess.TimeoutExpired:
                    stop = "SIGTERM then SIGKILL"
                    self.child.kill()
            status = self.child.wait()
            # Preserve any bytes that arrived after the last accepted transaction.
            while select.select([self.master], [], [], 0)[0]:
                try:
                    chunk = os.read(self.master, 4096)
                except OSError as error:
                    if error.errno == errno.EIO:
                        break
                    raise
                if not chunk:
                    break
                self.raw("rx", chunk)
            self.stderr.seek(0)
            stderr = self.stderr.read()
            record("exit", name=self.name, status=status, stop=stop,
                   elapsed_s=self.elapsed(), stderr_hex=stderr.hex())
        finally:
            os.close(self.master)
            self.stderr.close()
            self.home.cleanup()

    def elapsed(self):
        return time.monotonic() - self.started

    def raw(self, direction, data):
        offset = self.offsets[direction]
        record(direction, name=self.name, seq=self.seq, offset=offset, hex=data.hex())
        self.offsets[direction] += len(data)

    def quiet(self):
        if os.fstat(self.stderr.fileno()).st_size:
            raise Rejected("unexpected stderr")
        if self.child.poll() is not None:
            raise Rejected("unexpected process exit")
        if select.select([self.master], [], [], 0)[0]:
            raise Rejected("unexpected buffered output before send")

    def receive(self, deadline):
        data = b""
        deadline = min(deadline, self.started + self.session_limit)
        while True:
            left = deadline - time.monotonic()
            if left <= 0 or not select.select([self.master], [], [], left)[0]:
                raise Rejected("response deadline")
            chunk = os.read(self.master, 4096)
            if not chunk:
                raise Rejected("EOF")
            self.raw("rx", chunk)
            data += chunk
            if len(data) > 65536:
                raise Rejected("output limit")
            prompt = PROMPT.search(data)
            if not prompt:
                continue
            answer = data[:prompt.start()]
            if prompt.end() != len(data) or any(line.startswith(b"* ") for line in answer.splitlines()):
                raise Rejected(repr(data))
            self.last_prompt = prompt[0].decode("ascii")
            record("ack", seq=self.seq, answer=answer.decode("ascii"), prompt=self.last_prompt)
            return answer

    def command(self, command):
        payload = command.encode("ascii") + VEOF
        if not re.fullmatch(rb"[ -~]{1,200}\x04", payload) or b";" in payload:
            raise Rejected("invalid request")
        if self.child.poll() is not None or select.select([self.master], [], [], 0)[0]:
            raise Rejected("unexpected terminal state before send")
        self.seq += 1
        start = time.monotonic()
        written = os.write(self.master, payload)
        self.raw("tx", payload[:written])
        if written != len(payload):
            raise Rejected("partial write")
        return self.receive(start + 5)


def expect(session, command, pattern):
    result = session.command(command)
    match = re.fullmatch(pattern, result)
    if match is None:
        raise Rejected(f"{command}: unexpected {result!r}")
    return match


def capture(rom, dest, frames, all_images):
    dest.mkdir(parents=True, exist_ok=False)
    totals = Counter()
    last_frame = None
    with Session([str(BIN), "HEADLESS", str(rom)], "gopher") as session:
        session.receive(time.monotonic() + 15)
        expect(session, "VERSION REVISION", rb"v0\.57\.2\n2af86eb725739adbf3d9d45cea2ed69eea57da2a\n")
        expect(session, "CARTRIDGE MAPPER", rb"F6\n")
        for i in range(1, frames+3):
            session.command("STEP FRAME")
            tv = expect(session, "TV", rb"FR=(\d+) SL=(\d+) CL=(-?\d+)\n")
            frame = int(tv[1])
            if last_frame is not None and frame != last_frame + 1:
                raise Rejected(f"nonconsecutive frame {last_frame} -> {frame}")
            last_frame = frame
            info = expect(session, "TV FRAME", rb"top: (\d+), bottom: (\d+), total: (\d+)\n")
            if i > 2:
                totals[int(info[3])] += 1
            if i > 2 and (all_images or frames <= 70 or frame % 16 in (7, 8)):
                target = dest / f"frame_{frame:04d}.png"
                session.command(f"SCREENSHOT {target}")
                if not target.is_file() or target.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
                    raise Rejected(f"missing PNG {target}")
                record("image", frame=frame, file=target.name, timing=info[0].decode().strip())
    record("frame_totals", counted=sum(totals.values()), totals=dict(totals))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("rom",type=Path)
    parser.add_argument("images",type=Path)
    parser.add_argument("frames",type=int)
    parser.add_argument("--all-images", action="store_true")
    args = parser.parse_args()
    capture(args.rom.resolve(),args.images.resolve(),args.frames,args.all_images)
