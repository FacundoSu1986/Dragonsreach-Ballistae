Scriptname AstraSightNative Hidden

; Degrees; matching reference + positive lease token are required for every operation.
; BeginSight accepts a request. Only IsSightReady confirms game-thread acquisition.
bool Function IsAvailable() Global Native
; Metadata 3.0.0 is required before calling API 3 functions.
int Function GetAPIVersion() Global Native
; -1 means unavailable/unknown, never assumed to be first person.
int Function GetCameraState() Global Native
bool Function BeginSight(ObjectReference gun, int token, float initialYaw, float initialPitch) Global Native
bool Function IsSightReady(ObjectReference gun, int token) Global Native
bool Function ValidateShot(ObjectReference gun, int token, float yaw, float pitch, float pivotHeight) Global Native
; Typed empty float[] means unavailable. freeze captures and locks the applied pose atomically.
float[] Function CaptureAim(ObjectReference gun, int token, bool freeze) Global Native
bool Function SetFrozen(ObjectReference gun, int token, bool frozen) Global Native
bool Function EndSight(ObjectReference gun, int token) Global Native
