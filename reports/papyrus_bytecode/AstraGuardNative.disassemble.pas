.info
	.source "AstraGuardNative.psc"
	.modifyTime 1791719737 ;Sun Oct 11 08:55:37 2026 Local
	.compileTime 1791759051 ;Sun Oct 11 19:50:51 2026 Local
	.user "AstraAsedio"
	.computer "Build"
.endInfo
.userFlagsRef
	.flag conditional 1	; 0x00000001
	.flag hidden 0	; 0x00000000
.endUserFlagsRef
.objectTable
	.object AstraGuardNative 
		.userFlags 1	; Flags: 0x00000001
		.docString ""
		.autoState 
		.variableTable
		.endVariableTable
		.propertyTable
		.endPropertyTable
		.stateTable
			.state 
				.function GetStatus native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Int
					.paramTable
						.param gun ObjectReference
						.param token Int
					.endParamTable
				.endFunction
				.function NotifyCombat native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param gun ObjectReference
						.param token Int
						.param target Actor
					.endParamTable
				.endFunction
				.function GetAPIVersion native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Int
					.paramTable
					.endParamTable
				.endFunction
				.function EndOperation native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param gun ObjectReference
						.param token Int
					.endParamTable
				.endFunction
				.function IsAvailable native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
				.endFunction
				.function BeginOperation native static
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param gun ObjectReference
						.param guard Actor
						.param token Int
						.param launcher Weapon
						.param ammo ammo
						.param shotSound Sound
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
			.endState
		.endStateTable
	.endObject
.endObjectTable
