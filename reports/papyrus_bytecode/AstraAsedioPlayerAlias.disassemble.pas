.info
	.source "AstraAsedioPlayerAlias.psc"
	.modifyTime 1791053881 ;Sat Oct 03 15:58:01 2026 Local
	.compileTime 1791224421 ;Mon Oct 05 15:20:21 2026 Local
	.user "Facu2"
	.computer "DESKTOP-DF3S14S"
.endInfo
.userFlagsRef
	.flag conditional 1	; 0x00000001
	.flag hidden 0	; 0x00000000
.endUserFlagsRef
.objectTable
	.object AstraAsedioPlayerAlias ReferenceAlias
		.userFlags 0	; Flags: 0x00000000
		.docString ""
		.autoState 
		.variableTable
			.variable ::Session_var astraasediosession
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
		.endVariableTable
		.propertyTable
			.property Session astraasediosession auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Session_var
			.endProperty
		.endPropertyTable
		.stateTable
			.state 
				.function OnDeath
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param akKiller Actor
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod CleanupSession self ::NoneVar                 ;@line 10
					.endCode
				.endFunction
				.function OnPlayerLoadGame
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod CleanupSession self ::NoneVar                 ;@line 7
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
				.function OnCellDetach
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod CleanupSession self ::NoneVar                 ;@line 13
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
				.function OnInit
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp0 objectreference
						.local ::temp1 String
						.local ::temp2 String
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod GetReference self ::temp0                     ;@line 4
						Cast ::temp1 ::temp0                                     ;@line 4
						StrCat ::temp1 "AstraAsedio Player alias initialized ref=" ::temp1  ;@line 4
						StrCat ::temp1 ::temp1 " session="                       ;@line 4
						Cast ::temp2 ::Session_var                               ;@line 4
						StrCat ::temp2 ::temp1 ::temp2                           ;@line 4
						CallStatic debug Trace ::NoneVar ::temp2 0               ;@line 4
					.endCode
				.endFunction
				.function CleanupSession
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp3 astraasediosession
						.local ::temp4 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						Cast ::temp3 None                                        ;@line 16
						CompareEQ ::temp4 ::Session_var ::temp3                  ;@line 16
						Not ::temp4 ::temp4                                      ;@line 16
						JumpF ::temp4 _label0                                    ;@line 16
						CallMethod EmergencyCleanup ::Session_var ::NoneVar      ;@line 17
						Jump _label1                                             ;@line 17
					_label0:
						CallStatic debug Trace ::NoneVar "AstraAsedio player alias PROPERTY_SESSION_NONE" 0  ;@line 19
						CallStatic debug Notification ::NoneVar "Astra: falta la quest de limpieza del jugador."  ;@line 20
					_label1:
					.endCode
				.endFunction
			.endState
		.endStateTable
	.endObject
.endObjectTable
