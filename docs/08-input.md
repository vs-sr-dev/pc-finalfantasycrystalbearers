# Input: the Remote and the Nunchuk in this game, and the mouse

Crystal Bearers is played with the pointer and with swings of the Remote.
Layle's telekinesis, the heart of the game, is *a lock and an action*: point
at something, hold B until the ring fills, then swing. That is this port's
design problem. The pointer maps to the mouse almost one to one. The swings
do not.

This file has three parts:

1. What the game asks of the controllers, by context, from its official
   guides.
2. What the code reads and how it recognises gestures, from the stripped
   executable.
3. The proposed keyboard and mouse scheme, and the two ways to deliver it.

A gamepad is set aside on purpose. It would give back the stick's analogue
walk but lose the pointer, and everything here is aimed with the pointer.

## 1. What the game asks, by context

Sources:

- **[A]** the BradyGames *Signature Series* guide, scanned on archive.org.
  Its control table is the manual's.
- **[J]** the Japanese *Official Complete Guide*, also on archive.org.
- **[F]** GameFAQs FAQs, the Final Fantasy Wiki, and reviews and previews:
  RPGamer, Eurogamer, Cubed3, Vooks, Nintendo World Report, GAME Watch,
  Co-Optimus, nsidr.
- No instruction manual PDF was found.

Tags: [C] confirmed by [A] or [J]; [F] reported by an FAQ or review; [U]
unverified.

### The controllers

| Control | Use |
|---|---|
| Pointer | The cursor: lock, aim throws, shoot, menus. It turns red at low life. Player 2's is orange. [C] |
| B | Hold to lock. While carrying, a press throws at the cursor, or fires the held enemy's ability. Fires in the shooting events (hold for auto-fire). Cancel in menus. Dismount a chocobo. [C] |
| A | Context action: talk, jump at a jump icon, climb, slide a rope, open a simple chest, mount a chocobo, dig, **set down what is held**, confirm. There is no free jump. [C] |
| Remote swing: up, down, left, right | The action on a lock. Also, with no lock: a **roll** while moving, a throw in the facing direction while carrying, a slide on the waterfalls and the ski run, a chocobo dash. [C] |
| Remote shake | Shake an NPC for gil, split a flan, break a grab, win a sword duel. The shuttle crash: "wave the Remote as fast as you can". [C] |
| Nunchuk stick | Walk or run (a slight push walks, a full push runs). Steering in the vehicle events, and the flight in the last battle. [C] |
| Z | Tap: the camera behind Layle. Hold: a first-person look, aimed with the d-pad. [C] |
| C | Not in the control table. [U] The code has an alternate table that swaps C and Z (part 2). |
| D-pad | Turn the camera. Menus. [C] |
| 1 | Pause menu. [C] |
| 2 | Screenshot to SD, at any time, cutscenes included. [C] |
| +, − | Not in the control table. [U] |
| Nunchuk swing | Only in the Palace Ball dance: two lanes of notes, the Remote's and the Nunchuk's. [C] |
| Rumble | A cue in two places: fishing (with an icon on screen) and the chocobo egg (rumble alone). [C] |
| Remote alone, Classic, GameCube pad | Not supported. The game wants a Nunchuk. [F] (The code agrees: part 2.) |
| Player 2 | A second Remote with its own cursor. Player 2 can lock and flick, but not carry. [C] |

Options menu [A p.11]:

- Control Configuration, "Type A" (Type B is the alternate table that swaps
  C and Z in the code).
- **Wii Remote Sensitivity**, default "3". This picks the gesture
  thresholds; see part 2.
- Reaction Camera.
- Camera Controls.
- Subtitles.

### Telekinesis: the lock and the action

The lock [C]:

- The ring fills while the cursor stays on the target with B held.
- How fast it fills depends on the distance, the target's kind and the
  Focus stat. The Range stat limits how far away you can lock.
- The lock holds while B is held and the target stays in range.
- A target too heavy to move pulls Layle to it instead.

| Swing while locked | Effect [C unless noted] |
|---|---|
| **Up** (toward yourself) | Lift it overhead, or pull it toward you. Enemies are tossed over your head and land stunned. On terrain or heavy objects, Layle is pulled in: a leap, or a strike. Once something is lifted, B may be released. |
| **Left / right** | Throw it that way. Many enemies **spin** instead: bomb, trickface, King Behemoth, the roller-bug ball. |
| **Down** (away, into the screen) | Slam it into the ground or push it away. Bury a goblin, plant a bloomer, close an Iron Giant's visor, jar a chest open, milk a cow, pull flying sheep down. |
| **Shake** | NPCs drop gil. Flans split. Armoured shells crack. A Yuke loses its head. Yuke warp points open. |
| Arrows on the reticle | Some targets accept only the directions shown in green. [F] |

While carrying (the HUD reads "Swing: Throw / B: Action / A: Release") [C]:

- **B** throws at the cursor, or fires the held enemy's ability a few times
  first.
- A **swing** throws where Layle faces.
- **A** sets it down.

### Field and exploration

Everything uses the same grammar:

- Lock and swing: a ledge to vault, a line of lamps to swing along, a door,
  a lever, a letter, a newspaper, a Zu's legs to ride it, the shuttle's
  panel (left or right), a miasma stream to close.
- Lock and shake: a warp point, an NPC.
- Things picked up by hovering over them: gil, materials, hearts.
- Riding a chocobo: the stick steers, a **shake** dashes, A digs, B
  dismounts.
- The bird bell: ring it, then **put the Remote down**, and a bird lands on
  Layle. Stillness or an idle timer, not yet known.

### Combat

- Lock and swing to throw, spin or toss.
- Hold an enemy and press B to use its ability.
- Throw enemies into each other: they take damage, and some fuse.
- **A swing while moving rolls.** The roll is invincible. A second swing at
  the end of a roll chains a second roll.
- Recovery in midair: a swing as you are hit [F]. One source says a button
  instead.

Bosses use the same verbs on parts:

| Boss | Gesture |
|---|---|
| Crystal Armor | The lever on its back. |
| Malboro | Its tongue: up or down. |
| Iron Giant | Its cog: spin it. |
| King Behemoth | Screw it into the snow, then break off a horn. |
| Bahamut | Lock on to pull yourself to him, then leap between highlighted spots. |
| The last battle | Plates and turrets pulled off. **Shake left and right** to break the arm's grab. |

### The thirteen playable events [J] and the side games

| Event | Controls |
|---|---|
| Shoot the Monsters! | Pointer and B (hold for auto-fire). |
| Alexis Emergency | Stick left and right only, with heavy lag. |
| Getaway (chocobo cart) | Lock and flick the pursuers. Sword duels: **shake fast**. Lock and swing on the scenery. |
| Bahamut Strike | Throw, pull, leap (as above). |
| Beach Battle | Flick the balls away. Lock on to Belle and pull her back. |
| Escape! Capital Express | **Swing left or right** (as the arrows show) to move between cover. Swing down to go prone. Shake to step out. Jerk up to kick a ball. |
| Fire Bearer | Swing sideways. Catch the fireball (swing up) and throw it back. |
| Chocobo Chase | Stick to steer; forward speeds up, back slows down. **Keep the pointer on the target** for score. |
| Awakened Beast | Swing to roll. |
| Palace Ball | **Swing the Remote or the Nunchuk** as its note hits the circle. Stick and A between dances. |
| Save the Selkies! | Throws, the crane (swing down), pipes. |
| Showdown! Alexis | Stick to steer. Lock and swing to cross. Rolls, and life rings thrown as decoys. |
| Shuttle crash | **Wave as fast as you can.** |
| Decisive Battle | The stick moves Layle in the screen's plane. Pull plates off. Shake to break the grab. |

Side games:

| Game | Controls |
|---|---|
| Fishing | Lock, wait for the rumble and the icon, then swing up. |
| Waterfall slides and the ski run | Stick, and a swing to dash sideways ("Swing: Slide"). |
| Picking contests (grapes, mushrooms, vegetables, petals, ore) | Lock and pull. |
| Kickerbaul | **Hold A to charge, release to kick.** |
| Chocobo race | Steer, shake to dash, A to dig. |
| Frog chorus | Point at the frogs, then a button (Z, by one FAQ). |
| Shop restock | A button and a shake. [U] |
| Chocobo egg | Throw it as the Remote rumbles. |

### What the players said

[F]:

- **The camera is the most criticised part.** It is slow, it turns only by
  taps of the d-pad, and it cannot move during jumps. One reviewer wished
  it turned at the screen's edge.
- **Misread swings**: a lift that throws sideways instead. A clean flick
  reads right; waggling does not. Flick and shake must stay distinct.
- **The lock is fiddly on moving targets**: the cursor must stay on them
  while the ring fills.
- Throwing at the cursor with B was praised.
- Wrists tire from the waggle sequences.

## 2. What the code reads and how it recognises gestures

Static analysis of the stripped DOL. The details and addresses are in
`03-executable.md`. In short:

- **KPAD only.** One call, `KPADRead(chan, buf, 16)` at 8003E79C, every
  frame. Up to 16 samples are read, newest first, at the Remote's rate
  (several per frame). This KPAD (June 2009, no MotionPlus) has a
  `KPADStatus` of **0xB0 bytes**.
- **Fields read**:
  - `hold`, the buttons. The game makes its own edges and key repeat.
  - `acc`, the Remote's acceleration, every sample.
  - `pos`, the pointer, from the newest sample with both sensor-bar points
    seen.
  - `dev_type`, `wpad_err`, `dpd_valid_fg`, `data_format`.
  - The Nunchuk's `fs.stick`, and its `fs.acc` for every sample.
- **Never read**: `acc_value`, `acc_speed`, `vec`, `speed`, `horizon`,
  `acc_vertical`, and **`dist`**. So there is no twist or roll, and **no
  push or pull toward the sensor bar**. "Toward" and "away" are swings,
  read from the accelerometer like the others.
- **The Nunchuk is required.**
  - `dev_type` 1 gives the game's normal mode. 0 (the Remote alone) gives a
    reduced mode; anything else stops the game.
  - Unless `data_format` is a Nunchuk format (3 to 5), the stick reads
    zero.
  - The stick's digital directions are at ±0.8, with the clamp set by
    `KPADSetFSStickClamp(15, 87)`.
- **Gestures come from raw acceleration.** The game has its own
  recognisers, run on every sample of every frame, for the Remote and the
  Nunchuk alike:

| Detector | Signal | Output bits (Remote / Nunchuk) |
|---|---|---|
| Left / right | `acc.x` | 0x1 / 0x100 and 0x2 / 0x200: a strong lobe after one of the opposite sign |
| Shake | `acc.x` | 0x40 / 0x4000: at least 5 short alternating lobes |
| Up / down | `acc.y`, gravity taken out | 0x4 / 0x400 and 0x8 / 0x800 |
| Posture sequences | (`acc.x`, `acc.y`) in sectors, windows of 30 and 60 samples | 0x10 / 0x1000 and 0x20 / 0x2000: meaning unknown (a raise and a bring-down?) |
| Horizontal swing | (`acc.x`, `acc.z`): a peak ≥ 1.0 g, then an opposite peak ≥ 0.8 g within 40 samples | An angle and a strength |

- **The thresholds are the Sensitivity option.** Its five values pick rows
  2, 3, 5, 7 and 9 of a table at 804B2228. Each row gives a start level, a
  sustain level and a "strong" level, in g, and a maximum gap in samples:

| Option | Start | Sustain | Strong | Gap |
|---|---|---|---|---|
| 0 | 0.5 | 0.3 | 0.65 | 26 |
| 1 | 0.6 | 0.4 | 0.8 | 28 |
| 2 | 0.8 | 0.5 | 1.2 | 33 |
| 3 | 1.0 | 0.7 | 1.6 | 40 |
| 4 | 1.4 | 1.0 | 2.0 | 50 |

  The menu's default "3" is probably option 2 (the menu counts 1 to 5).
  Synthetic motion that is "strong" at 2.0 g works at every setting.
- **Telekinesis** (`fn_80262814`):
  - A horizontal swing stronger than 1.2 g is turned into a world direction
    through the camera: left or right of the camera (dot product ±0.5).
  - Otherwise the left and right bits decide.
  - Up, down and shake are the bits 0x4, 0x8 and 0x40.
- **The event scripts read the raw detector bits** (VM opcodes 0x1DF to
  0x1E1). The playable events may use any of the fourteen bits, the posture
  and Nunchuk ones included. Which ones they use is still open.
- Also from the code:
  - **The game streams sound to the Remote's speaker**: its sound driver,
    and the Home Button menu.
  - **Rumble** comes in patterns.
  - **The battery is checked**: at 0, all input is cleared. wiikit reports
    4, which is fine.
  - Two Remotes at most (the connect callback disconnects channels 2 and
    3).
  - The GameCube pad is initialised but never read.

### Seen in Dolphin (session 1)

The setup:

- An emulated Remote and Nunchuk (`tools/dolphin/FFCB-Mouse.ini`).
- Log-only breakpoints (`tools/dolphin/RFCEGD.ini`), read by
  `tools/dolphinlog.py`.
- Played by the user through the prologue and into the first areas on
  foot.

The measures:

| Measure | Result |
|---|---|
| **Frame rate** | 30 frames a second. |
| **Sample rate** | 6 to 8 samples per `KPADRead` on channel 0 (0 on channels 1 to 3), so **about 200 Hz**: Dolphin's rate. This fits the detectors' gaps of 26 to 50 samples (0.13 to 0.25 s). |
| **Sensitivity** | The default is row 5, option 2 (the menu's "3"): 0.8 / 0.5 / 1.2 g, a gap of 33 samples. |

The bits and what the game does with them:

| Bit | Dolphin's input | In the game |
|---|---|---|
| 0x1 | Swing Left | Locked on a passer-by: **thrown to the left**. Confirmed. |
| 0x2 | Swing Right | Seldom. Dolphin's sideways swings are too weak for the game's x thresholds, and nothing happened. 0x2 is right by symmetry. |
| 0x8 | Swing Up | One clean tap gave 0x8 alone, for 4 frames. **Lifts** the passer-by overhead; B then throws them. |
| 0x4 | Swing Down | Often held for half a second or more. On a passer-by it **lifts too**. Whether down slams depends on the target: try it on an enemy or an object. |
| 0x10, 0x20 | Tilt (forward, back, left, right) | **The posture detector reads tilts**, not swings. |

The other findings:

- **Rolling: any swing while Layle moves, in any direction.** The right
  button and a drag rolled whatever the drag's direction. The roll needs
  no direction from the gesture: Shift synthesises one plain swing.
- **The shake bit 0x40 never came from Dolphin's Shake.** Shake gives
  lobes alternating at about 2 Hz, too slow for five short lobes within
  the gap. Dolphin's Nunchuk shake did the same with 0x4000. A synthetic
  shake must alternate faster, at least 6 Hz, with strong lobes.
- **Dolphin's swings make lobes both ways.** The emulated Remote moves
  out on the press and back on the release, so one tap can give a flick
  and its opposite. This is one more reason to check the waveforms in the
  port, where they are under our control, and not in Dolphin.
- **Spurious Nunchuk bits at scene changes.** Four bursts of 0x1000 then
  0x400 for half a second, with no Nunchuk input, likely as KPAD or the
  game resets the controller between scenes. The synthetic acc must stay
  continuous, on gravity, across resets.
- **The prologue's playable events read no gestures:**
  - Shoot the Monsters is the pointer and B.
  - Alexis Emergency is the stick's left and right alone (the keys were
    enough).
  - The scripts' detector opcodes were never reached.
  - The P1 detector-trig accessor (80255308) was never called with bits
    set. Telekinesis reads the bits by another path, and its gesture
    function (80262CC8) ran on every swing, locked or not.

## 3. The proposed scheme

The principles:

- Keep the game's grammar: point, hold, gesture.
- Turn each gesture into a deliberate, unambiguous mouse act. Flick,
  shake and wheel are distinct, so the misreads players complained of
  cannot happen.

| PC | Wii | Why |
|---|---|---|
| Mouse move | The pointer | One to one. The game's own filter (a 0.02 dead zone, a 0.1 s glide) stays. |
| **Left button** | **B** | Hold to lock. Press to throw at the cursor or use the held enemy's ability. Hold to fire in the shooting events. |
| **Left held + a flick of the mouse** | **Swing** in the flick's direction (the main axis: up, down, left, right) | The lock and the action in one hand. The flick is fast movement past a threshold (about 40 px in 120 ms at 1080p, scaled to the window). The cursor stays where it was during the flick, so the aim and the gesture do not fight, and B is not released. |
| **Wheel down** (rolled toward you) | **Swing up**: lift, pull toward | The wheel moves the way the object does: rolled toward the player, it comes toward Layle. One notch, with or without the left button held: lock with the left button, then a notch to lift or slam. The user's choice (session 1); it can be inverted in the settings. |
| **Wheel up** (rolled away) | **Swing down**: slam, push away | |
| **Right button + a flick** | Swing **without B** | Throw in the facing direction while carrying (a left-button press would throw at the cursor), and the context swings with no lock. |
| **Shift** | A **swing** with no direction of its own | The roll while moving: the PC's dodge key (any swing rolls, in Dolphin). Also the slide dash and the chocobo dash. |
| **Rapid back-and-forth of the mouse** (left or right button held) | **Shake** | Three reversals within about 0.4 s. A flick is one movement, a shake many. |
| **F** held | Shake, for as long as it is held | The waggle sequences: duels, the shuttle crash, the last battle's grab, warp points, gil. The wrists are spared. |
| W A S D | The Nunchuk stick | Full deflection; diagonals normalised. **Alt** held: half deflection, a walk (for the medal that wants a slow approach). |
| Space | A | Context action, confirm. Hold to charge a kick. |
| Middle button | Z | Tap: the camera behind Layle. Hold: the first-person look. |
| Q / E, or the arrows | D-pad left / right: turn the camera | The arrows give the whole d-pad (up and down too: the first-person look, menus). |
| C | C | Unused by the game in Type A, but given anyway. |
| X | A **Nunchuk swing** | The Palace Ball's second lane. |
| Tab | 1: pause menu | |
| P | 2: screenshot | |
| Enter, Backspace, F1 | +, −, HOME | |
| Esc | The port's pause box | As in the other ports. |

### Details to settle by playing

Each of these becomes a setting:

- **Flick threshold and window**, and whether the flick fires at the
  threshold (lower latency) or on release.
- **Swing strength.** Synthesise strong swings (at least 2.0 g), so the
  in-game Sensitivity no longer matters, or follow the flick's speed.
- **The horizontal swing.** Left and right also feed the horizontal-swing
  detector. Above 1.2 g its world direction is used, and this must agree
  with the screen direction of the flick.
- **The posture bits 0x10 and 0x20.** Find which events read them, then
  give them keys.
- **Camera from the screen edge.** A port option, as the reviewer wished:
  the pointer held at the left or right edge turns the camera (d-pad
  taps). It is off by default, since aiming near the edges is common.
- **Lock assist.** None at first: the game's own ring and the Focus stat
  stay. With a mouse, the hand is steadier than on the Remote.
- **Rumble with no pad.** The chocobo egg is cued by rumble alone. With a
  mouse and keyboard, the port shows or plays a cue when the motor starts.
  The fishing has its own icon already.
- **The speaker's sound** plays through the PC's audio. Some of the game's
  sound is the Remote's.
- **Player 2**: a gamepad's stick as a second cursor, later or never.

### Two ways to deliver a swing

As in Dragon Quest Swords (`pc-dragonquestswords/docs/08-input.md`).

**1. Synthesise the motion (wiikit, game-agnostic).** The runtime fills
`acc` and `fs.acc` sample by sample with the waveform of a real swing: a
lobe one way, then a strong lobe the other, in the Remote's frame. The
game's own recognisers run, untouched.

Here, unlike in Dragon Quest Swords, we know exactly what the recognisers
want. The waveform can be designed against them and checked in the port:
log the detector bits (`dev+0xADBC`) and the horizontal-swing angle, one
gesture at a time, at every Sensitivity setting.

It needs, in wiikit:

- `KPADStatus` of 0xB0.
- The Nunchuk.
- Several samples per `KPADRead`.
- A motion generator.

(`10-wiikit.md`.)

**2. Deliver the gesture where the game reads it (this port's layer).**
Set the detector bits and the swing summary directly, at the end of the
detectors' per-frame collect (`fn_80229AFC`). The result is exact: no
waveform latency, no dependence on the Sensitivity option.

**The plan uses 1 first.** It belongs in wiikit: every waggle game needs
synthetic motion, and wiikit's own README lists it as its next step. It
keeps the game's rules, and this game's detectors tell us exactly how to
shape it. 2 stays in hand for any gesture whose waveform proves fragile.
