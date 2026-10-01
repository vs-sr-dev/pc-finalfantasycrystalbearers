# The executable

RFCE `main.dol`, 5.3 MB, stripped. Built on the RVL SDK of early 2009
(`0x4302_145`): OS, GX, AX and the rest from 27 February 2009, KPAD and WPAD
from 22 June, RFL from July and FA from August. HBM is from March. There is
no RSO module and no REL. The game's own sound driver
(`CDev.Engine.Sd.SoundDriver`) sits on AX. JSystem names appear among the
signatures (`J3DGraphLoader`, `JKernel`), and only a few.

```
DOL  entry 80004050  bss 80552F80+A4DCC
  T0  80004000-800066C0      T1  80006E20-804AB640
  D0-D7 800066C0 .. 805F7D20
SDA bases (from __init_registers, 80004234): r13 = 805FB4E0, r2 = 805FD300
```

## Names

`tools/names.py` puts the names together, as in The Last Story:

| Source | Names | |
|---|---|---|
| `tools/names-manual.tsv` | 13 | KPAD, by its object's order against Victorious's symbolised ELF |
| debug strings | 27 | SDK functions that print their own names |
| signatures | 1 505 | Dolphin's `totaldb.dsy` (1 060) and Victorious's ELF (818), via `tools/sigmatch.py` |

That makes 18 270 candidate functions and 1 545 names. The game's code
carries almost no strings. What it does carry:

- Effect-parameter names (`ppp*`).
- Animation tags in packed four-letter tables (`capd`, `swng`, `shak`,
  `push`, `drgl`, `thro`…).
- A few state names (`Capture`, `CaptureThrow`, `Lockon`, `Pulley`).

`tools/look.py` sets the SDA bases, so `--xref` finds small-data
references, and `--func` shows the float each `lfs`/`lfd` from r2 loads.

## KPAD

This KPAD has no MotionPlus code. Its `KPADStatus` is **0xB0 bytes**: the
standard fields to 0x60, then a 0x50-byte `ex_status` union. That is neither
the 2006–07 size (0x84) nor the later one (0xF0).

| Address | Function |
|---|---|
| 803C9980 | `calc_acc` |
| 803C9D10 | `read_kpad_acc` (acc.x = −raw.x, acc.y = −raw.z, acc.z = raw.y) |
| 803CA8D0 | `calc_dpd_variable` |
| 803CAEA0 | `read_kpad_dpd` |
| 803CB320 / 803CB450 | `clamp_stick_circle` / `clamp_stick_cross` |
| 803CB680 | `read_kpad_ext` |
| 803CBF50 | `KPADRead`: `li r6,0; li r7,0; b KPADiRead` |
| 803CBF60 | `KPADiRead` |
| 803CC690 | `KPADInit` |
| 803CC6A0 | `KPADInitEx` |
| 803CCAF0 | `KPADReset` |
| 803CCB90 | `KPADiConnectCallback` |
| 803CCD00 | `KPADSetConnectCallback` |
| 803CCE40 | KPAD's sampling callback |

Calls the game makes, from the manager's constructor `fn_8003D308` and
around it:

- `PADInit` (the GameCube pad is never read).
- `WPADRegisterAllocator`.
- `KPADInit`.
- `WPADSetAutoSleepTime(5)`.
- `KPADSetConnectCallback` on channels 0 to 3. The callback disconnects
  channels 2 and up.
- `803C9550(15, 87)`, KPAD's Nunchuk stick clamp.
- `WPADGetInfoAsync` every few frames (`fn_8003D634`).
- Rumble patterns through `WPADControlMotor`.
- The speaker, from the sound driver (`fn_8045C26C`, an alarm
  `fn_8045CEDC`).

It never calls `WPADRead`, `WPADSetDataFormat`, `WPADGetAccGravityUnit`,
`KPADSet{Pos,Acc,Hori,Dist}Param`, `KPADSetSensorHeight`,
`KPADSetBtnRepeat`, or `KPADEnable/DisableDPD`. `WPADControlDpd` is reached
only through a virtual slot no one calls.

## The input device

There are four devices, 0xAE48 bytes each, at `*(805F4250) + 0x18 + chan *
0xAE48`. The vtable is at 804C5F78. Each frame, `fn_8003E758`:

1. Reads 16 samples into `dev+0xA220` (stride 0xB0). The count goes to
   `+0xAD20`.
2. Sets the mode at `+2` from the newest sample's `dev_type`:
   - 0 (the Remote alone) → 1.
   - **1 (the Nunchuk) → 2, the normal mode.**
   - Anything else → 5, and the input is cleared.
3. Unless `data_format` is 3 to 5, the stick is zeroed.
4. If the battery, as `WPADGetInfo` reports it, is 0, the input is cleared.

The layout:

| Offset | Content |
|---|---|
| +0x88 / +0x98 / +0x9C | hold, trig, release. The stick's digital directions at ±0.8 are OR'd in as 0x10000…0x80000. |
| +0x8C | Key repeat: first at 0.25 s, then every 0.09 s. |
| +0x90 | The Nunchuk stick (`fn_8003E070`). |
| +0xCC / +0x516C | The Nunchuk's and the Remote's motion analysers (0x50A0 bytes each). |
| +0xA20C | The gesture detectors. |
| +0xAD24 / +0xAD5C | The Remote's and the Nunchuk's gesture summaries. |
| +0xAD94 / +0xADA0 | The newest acc of each. |
| +0xADAC | The pointer, filtered: a 0.02 dead zone, unless the movement keeps one direction (within 60°) for 0.1 s; a glide over 0.1 s below 0.04, a snap above. |
| +0xADBC / C0 / C4 | The detector bits: hold, trig, release. |

Samples whose acc is (0, 0, 0), or whose `wpad_err` is not 0, are skipped.
The pointer is taken only from samples with `dpd_valid_fg == 2`.

### Gesture detectors

The detectors are built by `fn_80229868`: three classes, each made twice
(for `acc` and for `fs.acc`). They are fed per sample by `fn_80229A6C`, and
their bits collected per frame by `fn_80229AFC`.

The thresholds are a row of the table at 804B2228. Each row holds start,
sustain and strong levels as `f32`, and the gap as `s16`. The row is chosen
by the Sensitivity option at `*(805F4570)+0x70`: options 0 to 4 give rows
2, 3, 5, 7 and 9 (`fn_80229BC4`).

A segmenter (`fn_8022A494`, `fn_80229C44`) keeps a ring of 16 lobes:

- A lobe starts beyond the start level and lasts while beyond the sustain
  level.
- It is strong beyond the strong level.
- A flick is a strong lobe after one of the opposite sign, directly or
  within the gap.

| Class | Signal | Bits |
|---|---|---|
| Left / right (vtable 80504C08) | acc.x | 0x1, 0x2, and shake 0x40 (5 short alternating lobes, `fn_8022A118`) |
| Up / down (vtable 80504C28) | 1 + acc.y, doubled below −1 | 0x4, 0x8 |
| Posture (vtable 80504C48, `fn_8022AE98`, `fn_8022B46C`) | (acc.x, acc.y) in sectors at ±0.7, ±1.5, −0.4, −0.5, −1.7, −2.0; a jolt latch below −1.6 (cleared above −1.1); windows of 30 and 60 samples | 0x10, 0x20 |

The Nunchuk's bits are the Remote's shifted left by 8.

The horizontal swing is detected at `analyser + 0xAB0`, with the code at
`fn_80041884`, `fn_800413C4`, `fn_80041464` and `fn_8004151C`, fed (acc.x,
acc.z) from 8003F68C:

- It needs a peak ≥ 1.0 g, then an opposite peak ≥ 0.8 g within 40 samples.
- It completes when the signal settles.
- It gives the angle `atan2(x, z)` and a strength, the mean of the two
  peaks.

A third recogniser, by axis and level (`fn_8003F71C`), runs but nothing
reads its output.

### Consumers

The game's input object is at `*(805F4558)` (vtable 8050AB38), updated by
`fn_80254E2C`. It holds:

| Offset | Content |
|---|---|
| +4 | The pointer in pixels (640 × 456). |
| +0x2C | The stick. |
| +0x3C / +0x40 | The swing's strength and angle. |
| +0x5C… | The actions. |
| +0x74… | The detector bits. |

Buttons become actions through 20-byte tables:

- 8050A8CC, the default ("Type A").
- 8050A778, with C and Z swapped (option byte `+0x6F`).

| Consumer | What it does |
|---|---|
| `fn_80262814`, telekinesis | A horizontal swing above 1.2 g becomes left or right of the camera (dot product ±0.5). Otherwise the bits 0x1 and 0x2 decide. 0x4, 0x8 and 0x40 pass through. |
| The event-script VM (`fn_803620C8`) | Opcodes 0x1DB–0x1DE: buttons. 0x1DF–0x1E1: the raw detector bits. 0x1E2 and 0x1E3: the stick. 0x1E5 and 0x1E6: the pointer. |
| HOME | trig & 0x8000 opens the Home Button menu (`fn_801979FC`). It copies the whole newest sample. |

The scratch scripts of this analysis did not survive as tools.
`tools/look.py` covers what they did.
