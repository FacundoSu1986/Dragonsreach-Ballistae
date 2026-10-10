Scriptname AstraSightNative Hidden

; Degrees; matching reference + positive lease token are required for every operation.
; BeginSight accepts a request. Only IsSightReady confirms game-thread acquisition.
bool Function IsAvailable() Global Native
; Metadata 3.5.0 and API 4 are required for the fast-shot functions.
int Function GetAPIVersion() Global Native
; -1 means unavailable/unknown, never assumed to be first person.
int Function GetCameraState() Global Native
bool Function BeginSight(ObjectReference gun, int token, float initialYaw, float initialPitch) Global Native
; settings: fire/release/reset/cycle, yawCenter/yawHalf, pitchMin/pitchMax,
; pivotHeight/operatorHeight/operatorDistance/operatorVerticalTolerance.
bool Function BeginFastSight(ObjectReference gun, int token, float initialYaw, float initialPitch, Weapon launcher, Ammo shotAmmo, Ammo costAmmo, Sound shotSound, float[] settings, bool continuous) Global Native
bool Function IsFastSightReady(ObjectReference gun, int token) Global Native
; EndSight returns true only after all old engine effects/scene cleanup finish.
; token 0 is a per-gun wildcard: false during any fast ownership or cleanup.
bool Function IsEffectsQuiescent(ObjectReference gun, int token) Global Native
; 3.5.4+, API4 extension. Settles Reset only while no sight owns this gun.
; Game-thread native, not tasklet-callable; never moves/reloads the reference.
bool Function ResetIdleScene(ObjectReference gun) Global Native
; -1 inactive, 0 single, 1 continuous. UI polling does not authorize shots.
int Function GetFireMode(ObjectReference gun, int token) Global Native
bool Function IsSightReady(ObjectReference gun, int token) Global Native
bool Function ValidateShot(ObjectReference gun, int token, float yaw, float pitch, float pivotHeight) Global Native
; Typed empty float[] means unavailable. freeze captures and locks the applied pose atomically.
float[] Function CaptureAim(ObjectReference gun, int token, bool freeze) Global Native
bool Function SetFrozen(ObjectReference gun, int token, bool frozen) Global Native
bool Function EndSight(ObjectReference gun, int token) Global Native
