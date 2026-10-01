"""wiikit.ppc on the stripped DOL: functions from discovery, names from build/names.tsv.

Discovery takes a while, so its units are kept in build/units.tsv (delete it
after names.tsv gains seeds).

    python tools/look.py --func KPADRead          # or an address: 8034D208
    python tools/look.py --callers 8034D1C0
    python tools/look.py --xref 805391C0 [--span 0x10]

The DOL is stripped of _SDA_BASE_ and _SDA2_BASE_: they are taken from
__init_registers (80004234: r13 = 805FB4E0, r2 = 805FD300), so --xref sees
small-data references, and --func shows the float each lfs/lfd from r2 loads.
"""
import argparse
import os
import re
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # wiikit/

from wiikit import ppc
from wiikit.dol import Image, Symbol
from wiikit.recomp.discover import load_names, symbolise

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DOL = os.path.join(ROOT, "build", "extract", "sys", "main.dol")
UNITS = os.path.join(ROOT, "build", "units.tsv")
SDA, SDA2 = 0x805FB4E0, 0x805FD300                 # __init_registers' r13 and r2


def load(dol=DOL):
    img = Image(dol)
    img.sda, img.sda2 = SDA, SDA2
    names_path = os.path.join(ROOT, "build", "names.tsv")
    names = load_names(names_path) if os.path.exists(names_path) else {}
    if os.path.exists(UNITS):
        with open(UNITS) as f:
            units = [tuple(int(x, 16) for x in line.split()) for line in f]
        for a, e in units:
            img.symbols.append(Symbol(a, e - a, 1, 2, ".text", names.get(a, f"fn_{a:08X}")))
        img.symbols.sort(key=lambda x: x.addr)
        img._sym_addrs = [x.addr for x in img.symbols]
        img.by_name = {x.name: x for x in img.symbols}
    else:
        units, _ = symbolise(img, names, log=lambda *a: None)
        with open(UNITS, "w") as f:
            for a, e in units:
                f.write(f"{a:08X} {e:08X}\n")
    return img


def resolve(img, q):
    try:
        a = int(q, 16)
        for s in img.symbols:
            if s.is_func and s.addr <= a < s.addr + max(s.size, 1):
                return s
        raise SystemExit(f"no function at {a:08X}")
    except ValueError:
        s = img.by_name.get(q)
        if not s:
            raise SystemExit(f"no function {q!r}")
        return s


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--func")
    ap.add_argument("--callers")
    ap.add_argument("--xref")
    ap.add_argument("--span", type=lambda s: int(s, 0), default=1)
    a = ap.parse_args()
    img = load()
    if a.func:
        lines = []
        ppc.disassemble(img, resolve(img, a.func), True, out=lines.append)
        for line in lines:
            m = re.search(r"\b(lfsu?|lfdu?) f\d+, (-?0x[0-9a-f]+|-?\d+)\(r2\)", line)
            if m:
                at = (SDA2 + int(m.group(2), 0)) & 0xFFFFFFFF
                raw = img.read(at, 8)
                v = struct.unpack(">f", raw[:4])[0] if m.group(1).startswith("lfs") else struct.unpack(">d", raw)[0]
                line += f"   ; [{at:08X}] = {v:g}"
            print(line)
    elif a.callers:
        fn = resolve(img, a.callers)
        print(f"callers of {fn.name} ({fn.addr:08X}):")
        for site, f in ppc.callers(img, fn.addr):
            print(f"  {site:08X}  {f.name}+{site - f.addr:#x}")
    elif a.xref:
        for site, f, ref in ppc.xrefs(img, int(a.xref, 16), a.span):
            print(f"  {site:08X}  {f.name}+{site - f.addr:#x}  -> {ref:08X}")


if __name__ == "__main__":
    main()
