"""Read Dolphin's log of the breakpoints in tools/dolphin/RFCEGD.ini.

Each logged breakpoint is a line "BP <addr> <func>(r3 .. r12) LR=<caller>"
(the MI log). This groups the hits into bursts (a gap of --gap seconds or
more starts a new one: the tests of 07-next-session.md are separated by
pauses) and names what each breakpoint gives:

  80229B4C  detector bits, a device's frame (Remote | Nunchuk << 8)    r3
  80255308  P1 detector trig, read by a consumer                       r3, LR
  80262CC8  telekinesis gesture result (r28: not logged; the hit is)    -
  803633AC  an event script reads the detector trig                    r3
  80363394  an event script reads the detector hold                    r3
  802552D8  P1 action trig, read by a consumer                         r3, LR
  8003E7A4  samples read this frame                                    r3
  80229C40  Sensitivity row * 16                                       r4

    python tools/dolphinlog.py [%APPDATA%/Dolphin Emulator/Logs/dolphin.log] [--gap 1.5]
"""
import argparse
import collections
import os
import re

BITS = {0x1: "LR+", 0x2: "LR-", 0x4: "UD+", 0x8: "UD-", 0x10: "P1", 0x20: "P2", 0x40: "shake"}
WHAT = {
    0x80229B4C: "detector bits", 0x80255308: "P1 detector trig", 0x80262CC8: "telekinesis",
    0x803633AC: "script det trig", 0x80363394: "script det hold", 0x802552D8: "P1 action trig",
    0x8003E7A4: "samples/frame", 0x80229C40: "sensitivity row",
}
LINE = re.compile(r"^(\d+):(\d+):(\d+).*?BP ([0-9a-f]{8})\s+\S*\s*\(([0-9a-f ]+)\) LR=([0-9a-f]{8})")


def bits(v):
    names = [n for b, n in BITS.items() if v & b] + [f"Nun:{n}" for b, n in BITS.items() if v & (b << 8)]
    rest = v & ~0x7F7F
    return " ".join(names + ([f"+{rest:#x}"] if rest else [])) or "0"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log", nargs="?", default=os.path.join(os.environ.get("APPDATA", ""), "Dolphin Emulator", "Logs", "dolphin.log"))
    ap.add_argument("--gap", type=float, default=1.5)
    a = ap.parse_args()
    hits = []
    with open(a.log, encoding="utf-8", errors="replace") as f:
        for line in f:
            m = LINE.search(line)
            if m:
                mm, ss, ms = int(m[1]), int(m[2]), int(m[3])
                regs = [int(x, 16) for x in m[5].split()]
                hits.append((mm * 60 + ss + ms / 1000, int(m[4], 16), regs, int(m[6], 16)))
    print(f"{len(hits)} hits")
    burst, last = [], None
    for h in hits + [None]:
        if h is None or (last is not None and h[0] - last >= a.gap):
            if burst:
                report(burst)
            burst = []
        if h is None:
            break
        burst.append(h)
        last = h[0]


def report(burst):
    t0, t1 = burst[0][0], burst[-1][0]
    print(f"\n-- {t0:8.2f}s .. {t1:8.2f}s, {len(burst)} hits")
    by = collections.defaultdict(list)
    for t, addr, regs, lr in burst:
        by[addr].append((t, regs, lr))
    for addr, xs in sorted(by.items()):
        what = WHAT.get(addr, "?")
        if addr == 0x8003E7A4:
            c = collections.Counter(r[0] for _, r, _ in xs)
            print(f"   {what:18} {dict(sorted(c.items()))} over {len(xs)} reads")
        elif addr == 0x80229C40:
            c = collections.Counter(r[1] >> 4 for _, r, _ in xs)
            print(f"   {what:18} rows {dict(c)}")
        elif addr == 0x80262CC8:
            print(f"   {what:18} {len(xs)} hits")
        else:
            seq = []
            for t, r, lr in xs:
                s = bits(r[0]) + (f" <- {lr:08X}" if addr in (0x80255308, 0x802552D8) else "")
                if not seq or seq[-1][0] != s:
                    seq.append([s, 1, t])
                else:
                    seq[-1][1] += 1
            print(f"   {what:18} " + ", ".join(f"{s} x{n} @{t:.2f}" for s, n, t in seq))


if __name__ == "__main__":
    main()
