# Next session

Session 1 was research: what the game asks of the controllers, and what its
code reads (`08-input.md`, `03-executable.md`). Session 2 builds on it. It
has two threads, the boot and the motion. They meet when the game is played
with the mouse.

## 1. Ground truth from Dolphin (an hour, before any code)

Dolphin is at `D:\Emulatori\Wii\Dolphin-x64`.

1. Make a per-game controller profile for RFCE: an emulated Remote with
   the Nunchuk.
   - Swings on the numpad, shake on a key.
   - The Nunchuk's stick on W A S D, its swing on a key.
   - As for Dragon Quest Swords.
2. Watch these in Dolphin's memory view, with
   `dev = *(805F4250) + 0x18`:
   - **The sample count** `[dev+0xAD20]` after 8003E7A0: the Remote's
     rate, so how many samples a frame `KPADRead` must give.
   - **The detector bits** `[dev+0xADBC]` (trig at +0xADC0) while each
     emulated swing is made. This tells which of 0x1/0x2 is left and which
     is right, and the same for 0x4/0x8. It also shows whether Dolphin's
     swings make the posture bits 0x10/0x20.
   - **The horizontal swing**: the angle and strength at
     `*(805F4558)+0x40/+0x3C`. Does a screen-left swing give a world-left
     throw?
   - **The Sensitivity option** at `*(805F4570)+0x70` on a fresh save, and
     its value for each menu setting.
3. Play the first areas: lock, lift, throw, roll, shake an NPC.
   - Note which bits the roll reads (break on reads of `+0xADC0`).
   - Note which bits the first event scripts read (break at the VM's
     opcodes 0x1DF–0x1E1: 80363384, 8036339C, 803633B4).

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
2. Several samples per read, at the rate measured in 1.
3. The motion generator: swing and shake, on the Remote and the Nunchuk.
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
