# Session log

## Session 1 — the research: the Remote, the Nunchuk, and the mouse

Goal: before any code, find out what Crystal Bearers asks of the Wii Remote
and the Nunchuk, in every part of the game, and how its code reads them.
Then propose how a mouse and a keyboard play it.

Results:

* **The port set up** on wiikit (submodule, pinned at 3166862, the other
  ports' commit). The disc was already extracted by the reverse engineering
  project (`WII-FFCB-RE`).
* **The executable** (`03-executable.md`): RFCE, stripped, the RVL SDK of
  2009 (KPAD and WPAD of June). 1 545 names: 1 505 by signature (Dolphin's
  database and Victorious's ELF), 27 from debug strings, and 13 by hand
  (KPAD, by its object's order against Victorious's). The SDA bases come
  from `__init_registers`. `tools/look.py` shows `lfs` constants.
* **The game, by context** (`08-input.md`, part 1). From the official
  guides (BradyGames, and the Japanese *Official Complete Guide*, both
  scanned on archive.org), FAQs and reviews:
  - Everything is a lock with the pointer and B, then a swing (up, down,
    left, right) or a shake.
  - A swing with no lock is a roll, a throw where Layle faces, a slide or
    a chocobo dash.
  - The Nunchuk's stick walks and runs; Z is the camera; the d-pad turns
    it.
  - Thirteen playable events and a dozen side games. The Palace Ball is
    the one place the Nunchuk is swung.
* **The code** (`08-input.md`, part 2, and `03-executable.md`):
  - One `KPADRead` of 16 samples a frame. `KPADStatus` is 0xB0, a size
    wiikit does not know yet.
  - The game reads the buttons, acc, the pointer, and the Nunchuk's stick
    and acc. Never the IR distance: "toward" and "away" are swings like
    the others. Never the twist.
  - **The Nunchuk is required.** Without it the game runs in a reduced
    mode or takes no input.
  - The game recognises gestures itself, sample by sample:
    - Left/right and up/down flicks: a strong lobe after an opposite one.
    - A shake: five short alternating lobes.
    - Posture sequences: still unknown.
    - A horizontal swing, as an angle and a strength.
  - The thresholds are the Sensitivity option's row in a table (804B2228,
    read and checked).
  - Telekinesis takes the horizontal swing above 1.2 g and turns it
    through the camera. The event scripts read the raw detector bits.
* **The scheme** (`08-input.md`, part 3):
  - The mouse is the pointer. The left button is B.
  - The left button held and a flick of the mouse is a swing in the
    flick's direction, the cursor held still.
  - The wheel: down (toward the player) pulls toward, up pushes away.
  - The right button and a flick is a swing without B. Shift is the roll.
  - A shake of the mouse, or F held, is a shake.
  - W A S D is the stick (Alt to walk). Space is A. The middle button is Z.
    Q and E turn the camera.
* **The delivery**: synthetic motion in wiikit, so the game's own
  recognisers run. This time their thresholds are known, so the waveforms
  can be designed against them. Injecting the detector bits at the game's
  collect is kept as the fallback.
* **What wiikit needs** (`10-wiikit.md`):
  - `KPADStatus` of 0xB0.
  - The Nunchuk.
  - Several samples per read.
  - A motion generator.
  - Mouse flicks, wheel and shake in the key file.
  - The game's own speaker stream (`WPADSendStreamData`, WENC ADPCM).

The user approved the scheme as a first, tentative mapping, to be adjusted
by playing. Nothing was recompiled yet. The plan is in `07-next-session.md`.
