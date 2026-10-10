.info
	.source "AstraSightNative.psc"
	.modifyTime 1791576007 ;Fri Oct 09 17:00:07 2026 Local
	.compileTime 1791649531 ;Sat Oct 10 13:25:31 2026 Local
	.user "AstraAsedio"
	.computer "Build"
.endInfo
.userFlagsRef
	.flag conditional 1	; 0x00000001
	.flag hidden 0	; 0x00000000
.endUserFlagsRef
.objectTable
	.object AstraSightNative 
		.userFlags 1	; Flags: 0x00000001
		.docString ""
		.autoState 
		.variableTable
		.endVariableTable
		.propertyTable
		.endPropertyTable
		.stateTable
			.state 
				.function SetFrozen native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param gun ObjectReference
						.param token Int
						.param frozen Bool
					.endParamTable
				.endFunction
				.function GetCameraState native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Int
					.paramTable
					.endParamTable
				.endFunction
				.function GetAPIVersion native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Int
					.paramTable
					.endParamTable
				.endFunction
				.function BeginSight native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param gun ObjectReference
						.param token Int
						.param initialYaw Float
						.param initialPitch Float
					.endParamTable
				.endFunction
				.function EndSight native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param gun ObjectReference
						.param token Int
					.endParamTable
				.endFunction
				.function CaptureAim native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Float[]
					.paramTable
						.param gun ObjectReference
						.param token Int
						.param freeze Bool
					.endParamTable
				.endFunction
				.function IsSightReady native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param gun ObjectReference
						.param token Int
					.endParamTable
				.endFunction
				.function BeginFastSight native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param gun ObjectReference
						.param token Int
						.param initialYaw Float
						.param initialPitch Float
						.param launcher Weapon
						.param shotAmmo Ammo
						.param costAmmo Ammo
						.param shotSound Sound
						.param settings Float[]
						.param continuous Bool
					.endParamTable
				.endFunction
				.function ValidateShot native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param gun ObjectReference
						.param token Int
						.param yaw Float
						.param pitch Float
						.param pivotHeight Float
					.endParamTable
				.endFunction
				.function GetFireMode native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Int
					.paramTable
						.param gun ObjectReference
						.param token Int
					.endParamTable
				.endFunction
				.function IsFastSightReady native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param gun ObjectReference
						.param token Int
					.endParamTable
				.endFunction
				.function ResetIdleScene native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param gun ObjectReference
					.endParamTable
				.endFunction
				.function IsAvailable native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
				.endFunction
				.function IsEffectsQuiescent native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param gun ObjectReference
						.param token Int
					.endParamTable
				.endFunction
				.function GotoState
					.userFlags 0	; Flags: 0x00000000
					.docString "Function that switches this object to the specified state"
					.return None
					.paramTable
						.param newState String
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod onEndState self ::NoneVar                     ;@line ??
						Assign ::State newState                                  ;@line ??
						CallMethod onBeginState self ::NoneVar                   ;@line ??
					.endCode
				.endFunction
				.function GetState
					.userFlags 0	; Flags: 0x00000000
					.docString "Function that returns the current state"
					.return String
					.paramTable
					.endParamTable
					.localTable
					.endLocalTable
					.code
						Return ::State                                           ;@line ??
					.endCode
				.endFunction
				.function onBeginState
					.userFlags 0	; Flags: 0x00000000
					.docString "Event received when this state is switched to"
					.return None
					.paramTable
					.endParamTable
					.localTable
					.endLocalTable
					.code
					.endCode
				.endFunction
				.function onEndState
					.userFlags 0	; Flags: 0x00000000
					.docString "Event received when this state is switched away from"
					.return None
					.paramTable
					.endParamTable
					.localTable
					.endLocalTable
					.code
					.endCode
				.endFunction
			.endState
		.endStateTable
	.endObject
.endObjectTable
