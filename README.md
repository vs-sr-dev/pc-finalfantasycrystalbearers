# pc-finalfantasycrystalbearers

Toward a native PC port of **Final Fantasy Crystal Chronicles: The Crystal
Bearers** (Wii, Square Enix, 2009). The game was never re-released: no
remaster, no digital release. The goal is the game running natively on PC,
played with the keyboard and the mouse.

The route is static recompilation: the game's own PowerPC code, translated
to C++ and built for the PC, running on a replacement for the Wii's
hardware and system software. Nothing is emulated at the instruction
level, and nothing of the game is rewritten.

This game is played with the Wii Remote's pointer and its motion: Layle's
telekinesis is a lock with the pointer and a swing of the Remote. How
swings, shakes and the Nunchuk become a mouse and keys is this port's
design problem ([docs/08-input.md](docs/08-input.md)).

This repository documents the port and holds its own tools and layer. It is
built on **[wiikit](https://github.com/vs-sr-dev/wiikit)**, the
game-agnostic Wii toolkit, taken here as a submodule at `wiikit/`. Where
this game needs something every Wii game would need, it goes into wiikit,
not here. The game's formats were reverse engineered earlier, in
[wii-ffcb-re](https://github.com/vs-sr-dev/wii-ffcb-re).

## Where it stands

Session 1: the research. What the game asks of the Remote and the Nunchuk,
from its official guides and from its code; the mouse and keyboard scheme
proposed. See [docs/00-sessions.md](docs/00-sessions.md) and the plan in
[docs/07-next-session.md](docs/07-next-session.md).

## BYOA — Bring Your Own Assets

This repository contains **documentation and tools only**. No game data, no
executables, no assets. You need your own original disc. The work is done on
the North American release, RFCE; the addresses in `tools/` and `docs/` are
that executable's.

## Layout

    docs/     the executable, the input, the plan, the session log
    tools/    Crystal Bearers-specific tools
    wiikit/   game-agnostic Wii toolkit (submodule: github.com/vs-sr-dev/wiikit)
    build/    (not in git) the disc, everything derived from it, the build

## Building

As for the other wiikit ports: Python 3.8+, CMake, Ninja, clang (MSYS2) and
SDL3; OpenGL 4.5 to run. From the root:

```sh
python -m wiikit.disc GAME.iso --extract build/extract
python tools/sigmatch.py build/extract/sys/main.dol --dsy <Dolphin>/Sys/totaldb.dsy \
    --out build/sig_guess.tsv
python tools/names.py build/extract/sys/main.dol          # -> build/names.tsv
```

`tools/look.py` is `wiikit.ppc` on the stripped DOL.

## Documentation

    00-sessions.md            progress log
    03-executable.md          the stripped DOL, its names
    07-next-session.md        the plan for the next session
    08-input.md               the Remote and Nunchuk in this game, and the mouse
    10-wiikit.md              what this port asks of wiikit

## Licence

MIT. This covers the documentation and tools in this repository only. It
says nothing about Final Fantasy Crystal Chronicles: The Crystal Bearers,
which remains the property of its rights holders.
