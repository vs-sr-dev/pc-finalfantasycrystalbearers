# Next session

The game boots and plays with the pointer, B, A and the Nunchuk
(`00-sessions.md`, session 2). Two things stand between it and the whole
game: the Remote's swings, and the cut-scenes' stalls.

## 1. The swings (wiikit, then this port's keys)

`10-wiikit.md`, `08-input.md` part 3.

1. **Several samples per `KPADRead`**, at about 200 Hz (measured in
   Dolphin). The game counts its gesture windows in samples.
   - Each sample's motion is evaluated at its own time.
   - Every sample carries gravity, continuous across resets.
2. **The motion generator**: swing up, down, left, right, forward and back,
   and shake, on the Remote and on the Nunchuk.
   - A swing is a lobe one way, then a strong lobe the other.
   - A shake alternates at 6 Hz or more, with strong lobes.
   - What the game's detectors want is known (`03-executable.md`). For
     left and right, keep the first lobe under 1.0 g, so the horizontal
     swing detector never completes and the bits decide.
3. **The mouse in the key file**:
   - Flicks with a button held, the pointer held still meanwhile.
   - The wheel's notches.
   - A shake from the mouse's reversals.
   - A plain `Swing` for the roll (Shift).
4. **The check**: log the detector bits (`dev+0xADBC`, `dev = *(805F4250) +
   0x18`) for each gesture at each Sensitivity setting.
   - Every flick gives exactly its bit, and no shake.
   - A shake gives 0x40 and no flick.
   - Then play: lift, slam, throw left and right, roll, shake a passer-by.

## 2. The cut-scenes: shaders linked without stopping

The game has hundreds of TEV set-ups, most seen once, in cut-scenes. The
shader cache helps only the second time.

- **Asynchronous links.** Use `KHR_parallel_shader_compile` (NVIDIA has
  it). Start the link, go on, and skip the draws whose program is not
  ready yet, for a frame or two. This is Dolphin's asynchronous mode. It
  is game-agnostic, so it goes in wiikit's renderer.
- Later, an ubershader that interprets the TEV and leaves nothing out
  meanwhile. Dolphin's hybrid mode is the model.
- Measure with the render profiler (`WIIKIT_PROFILE=render`) and the
  report's link count.

## 3. Smaller things

- **The stop at boot**, once in about ten boots, with the render profiler
  on: AX stopped after "SoundSystem : Version 24/Jan/2008", 4 frames in.
  Does it happen without the profiler?
- The sound driver's "UpdateVSYNC Delay" (about 17 in a 40 s run, from
  loading) and the one menu background that dropped frames before the
  shader fixes: check again after 2.
- Dolphin's three checks:
  - Down on an enemy or an object (does it slam?).
  - A throw to the right.
  - Which detector bits the playable events' scripts read.
- Rumble: a cue on screen or in sound when the motor starts (the chocobo
  egg). This goes in the port's layer.
- The speaker stream (`WPADSendStreamData`, WENC ADPCM) into the TV's
  sound.
