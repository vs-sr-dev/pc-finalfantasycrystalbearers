// Final Fantasy Crystal Chronicles: The Crystal Bearers — the port's own
// layer over the wiikit runtime.
//
// Linked into wiiboot by ffcb.cmake; the functions it replaces are listed in
// ffcb-hooks.txt, which the recompiler takes with --hooks. What belongs here
// is what only this game needs.
#include "rt.h"

namespace {

void install() {
    // This KPAD (June 2009, no MotionPlus) has a KPADStatus of 0xB0 bytes:
    // the game reads 16 of them at that stride (03-executable.md).
    wpad_set_kpad_status_size(0xB0);
    // It plays with the Remote and the Nunchuk, and stops at the title
    // without one ("Connect the Nunchuk to the Wii Remote").
    wpad_set_nunchuk(true);
}

RtGameLayer layer("Final Fantasy Crystal Chronicles: The Crystal Bearers", install);

}  // namespace
