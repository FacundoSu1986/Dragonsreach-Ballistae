Scriptname AstraGuardNative Hidden
; NPC API1. Begin accepts a request; GetStatus confirms actual game-thread state.
; Gun+positive token identifies an operation. End confirms completed cleanup.
bool Function IsAvailable() Global Native
int Function GetAPIVersion() Global Native
bool Function BeginOperation(ObjectReference gun, Actor guard, int token, Weapon launcher, Ammo ammo, Sound shotSound) Global Native
int Function GetStatus(ObjectReference gun, int token) Global Native
bool Function EndOperation(ObjectReference gun, int token) Global Native
bool Function NotifyCombat(ObjectReference gun, int token, Actor target) Global Native
