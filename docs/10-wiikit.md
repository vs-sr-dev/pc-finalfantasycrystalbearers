# wiikit: what this port asks of it

The port takes wiikit as a submodule at `wiikit/`, pinned at 3166862 (the
same commit as the six other ports). Everything below is game-agnostic. It
goes into wiikit, and is checked on every port before it goes in.

Crystal Bearers is the first wiikit port whose game is played with **the
Remote's motion and the Nunchuk**. Dragon Quest Swords swings too, but there
the swing's direction came from the pointer, and a shake was enough
(`pc-dragonquestswords/docs/08-input.md`). Here the direction is in the
acceleration itself, so the motion must be real.

## The Remote and the Nunchuk (wpad.cpp, video.cpp)

**1. `KPADStatus` of 0xB0.**

- This KPAD (June 2009, no MotionPlus) has a third size, after 0x84 and
  0xF0.
- `wpad_set_kpad_status_size(0xB0)` from the port already works, since
  the layout to 0x60 is the same.
- Better: wiikit tells the size from KPAD itself (`KPADiRead`'s stride),
  so no port has to know it.

**2. The Nunchuk**, as wiikit already does for the Classic:

- `dev_type` 1 (`WPAD_DEV_FREESTYLE`) and `data_format` 5
  (`WPAD_FMT_FREESTYLE_ACC_DPD`) in `KPADStatus`.
- `ex_status.fs`: the stick at +0x60, acc at +0x68, acc_value and
  acc_speed.
- C and Z in `hold` (0x4000, 0x2000).
- `WPADFSStatus` (0x32 bytes) in WPAD's own samples.
- `WPADProbe`'s type, the extension callback, and the connect callbacks
  (this game registers KPAD's).
- The stick from keys (W A S D, a walk modifier at half deflection). Later,
  a gamepad's left stick merged in, as the Classic's are.
- The key file gains a `[Nunchuk]` section: Stick Up/Down/Left/Right,
  Walk, C, Z, Swing.
- A game says it wants the Nunchuk with `wpad_set_nunchuk(true)`, as
  `wpad_set_classic`.

**3. Several samples per `KPADRead`.** The Remote reports at about 100 to
200 Hz, so a game that reads 16 gets several each frame. This one counts
its gesture windows in samples, not frames.

- `KPADRead` returns the samples since the last read, by the time base, up
  to `len`, newest first.
- Each sample's motion is evaluated at its own time.
- Every sample carries gravity: the game skips an acc of (0, 0, 0).

The rate is to be measured in Dolphin (`[dev+0xAD20]`, see
`07-next-session.md`).

**4. A motion generator: synthetic Remote and Nunchuk motion.** This is
the "Next" in wiikit's README. A gesture is a waveform in the controller's
frame, added to gravity:

- **Swing** (direction: up, down, left, right, forward, back; strength):
  a lobe one way, then a strong lobe the other, about 100 to 150 ms
  together. It is the shape a real swing gives as the arm speeds up, then
  stops.
- **Shake**: alternating strong lobes at about 6 to 8 Hz, for as long as
  it is held.
- **Tilt / raise**: wiikit's existing `Raise`, kept.

Each gesture is given on the Remote or on the Nunchuk. The existing
`Shake` (±2 g from one sample to the next) stays as it is for the ports
that use it.

**5. Mouse gestures in the key file.** `Drag Left` exists already (a
button held, the mouse moving fast). It needs:

- **Directional drags**: `Flick Up/Down/Left/Right` with a button held,
  the direction fixed when the threshold is passed.
- **The pointer held still** during a flick (an option).
- **The wheel's notches** as bindings.
- **A shake from mouse reversals.**

They bind to the generator's gestures: `Swing Up = Flick Up (Mouse Left),
Wheel Down`.

## The Remote's speaker, streamed

This game encodes its own speaker sound: `WENCGetEncodeData` is in the DOL,
the Remote's 4-bit ADPCM. It sends the sound with `WPADSendStreamData` from
its sound driver's alarm. The Home Button menu does the same.

wiikit already mixes AX's Remote voices into the TV's sound (Dragon Quest
Swords). It answers `WPADSendStreamData` with "no controller", so this
sound is lost. What is needed:

- Decode the stream (WENC's format, at the rate `WPADControlSpeaker` set)
  and mix it as the AX Remote voices are.
- Answer `WPADCanSendStreamData` and `WPADControlSpeaker` as a Remote
  with a speaker would.

## Rumble with no pad

`WPADControlMotor` rumbles the channel's pad. With the mouse and keys there
is none, and this game uses rumble as a cue (the chocobo egg). That
belongs to the port's layer: a visible or audible cue when the motor
starts.

## Check on every port

- Victorious, Dragon Quest Swords and the others must play as before. For
  them the existing `Shake` and `Drag` are unchanged, and a game with no
  Nunchuk sees none.
- The gestures are checked against this game's own recognisers. The
  detector bits at `dev+0xADBC` are logged, one gesture at a time, at each
  of the five Sensitivity settings.
