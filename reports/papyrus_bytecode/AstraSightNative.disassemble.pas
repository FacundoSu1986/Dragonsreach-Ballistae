.info
	.source "AstraSightNative.psc"
	.modifyTime 1791142172 ;Sun Oct 04 16:29:32 2026 Local
	.compileTime 1791224423 ;Mon Oct 05 15:20:23 2026 Local
	.user "Facu2"
	.computer "DESKTOP-DF3S14S"
.endInfo
.userFlagsRef
	.flag hidden 0	; 0x00000000
	.flag conditional 1	; 0x00000001
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
				.function GetCameraState native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Int
					.paramTable
					.endParamTable
				.endFunction
				.function IsAvailable native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
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
				.function EndSight native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param gun ObjectReference
						.param token Int
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
				.function IsSightReady native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param gun ObjectReference
						.param token Int
					.endParamTable
				.endFunction
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
			.endState
		.endStateTable
	.endObject
.endObjectTable
