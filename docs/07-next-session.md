# Next session

Session 1 was research: what the game asks of the controllers, and what its
code reads (`08-input.md`, `03-executable.md`). Session 2 builds on it. It
has two threads, the boot and the motion. They meet when the game is played
with the mouse.

## 1. Dolphin: done, but for three checks

Session 1 measured the rate, the default Sensitivity, the bits for left, up
and the tilts, and the roll (`08-input.md`, "Seen in Dolphin"). Three checks
are left, to do whenever Dolphin is open:

- Down on an enemy or an object, not a passer-by: does it slam?
- A throw to the right with room on the target's right.
- The playable events past the prologue. Does the script breakpoint
  (803633AC) fire, and with which bits?

The setup stays in `tools/dolphin/`. `python tools/dolphinlog.py` reads the
log.

## 2. The port boots

The route of the other ports:

1. Disc: `build/extract` already has `sys/`. Link `files/` from
   `WII-FFCB-RE/extract/files` (a junction: 3 GB). Or re-extract with
   `wiikit.disc` and compare.
2. Recompile: `python -m wiikit.recomp build/extract/sys/main.dol --out
   build/recomp --symbols build/names.tsv --hooks tools/ffcb-hooks.txt`.
   Expect unknown targets to be seeded, as in the other stripped
   executables. Then CMake and Ninja with `tools/ffcb.cmake` and the port
   layer `tools/ffcb.cpp`.
3. `wiiboot`, from `__start` through the strap screen and the logos to the
   title.

Things to expect:

- **The Nunchuk** (wiikit, `10-wiikit.md` 1 and 2) is needed before the
  game takes any input. Without it the game is in mode 1 (the Remote
  alone) or mode 5 (no input at all).
- **The game's own sound driver** streams to the speaker. Until wiikit
  takes the stream, "no controller" must not stop it.
- The game's renderer: the RE found no NW4R at the top level. The GX
  paths are those the other ports already exercise.

## 3. The motion in wiikit

`10-wiikit.md`:

1. `KPADStatus` of 0xB0. The Nunchuk.
2. Several samples per read, at about 200 Hz (measured in Dolphin).
3. The motion generator: swing and shake, on the Remote and the Nunchuk.
   Shake at 6 Hz or more, with strong lobes; acc continuous across
   resets.
4. The mouse gestures in the key file: flicks, the wheel, shake by
   reversals.

The check: in the port, log the detector bits for each gesture at each
Sensitivity setting. Every directional flick must give exactly its bit,
and no shake. A shake must give 0x40 and no flick. Then play: lift, slam,
throw left and right, roll, shake an NPC.

## Still open

- The posture bits 0x10/0x20 (and the Nunchuk's 0x1000/0x2000): which
  gesture, and where they are used. The event scripts' data have not been
  scanned for the detector opcodes yet.
- The bird bell: stillness, or an idle timer?
- Control Configuration "Type B" is the C/Z swap. What do Reaction Camera
  and Camera Controls do?
- Air recovery: a swing or a button?
