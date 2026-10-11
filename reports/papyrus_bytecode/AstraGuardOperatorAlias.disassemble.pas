.info
	.source "AstraGuardOperatorAlias.psc"
	.modifyTime 1791719737 ;Sun Oct 11 08:55:37 2026 Local
	.compileTime 1791759052 ;Sun Oct 11 19:50:52 2026 Local
	.user "AstraAsedio"
	.computer "Build"
.endInfo
.userFlagsRef
	.flag conditional 1	; 0x00000001
	.flag hidden 0	; 0x00000000
.endUserFlagsRef
.objectTable
	.object AstraGuardOperatorAlias ReferenceAlias
		.userFlags 0	; Flags: 0x00000000
		.docString ""
		.autoState 
		.variableTable
			.variable ::Controller_var astraasedioguard
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
		.endVariableTable
		.propertyTable
			.property Controller astraasedioguard auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Controller_var
			.endProperty
		.endPropertyTable
		.stateTable
			.state 
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
				.function OnCombatStateChanged
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param akTarget Actor
						.param aeCombatState Int
					.endParamTable
					.localTable
						.local ::temp2 astraasedioguard
						.local ::temp3 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						Cast ::temp2 None                                        ;@line 11
						CompareEQ ::temp3 ::Controller_var ::temp2               ;@line 11
						Not ::temp3 ::temp3                                      ;@line 11
						JumpF ::temp3 _label0                                    ;@line 11
						CallMethod NotifyCombatV23 ::Controller_var ::NoneVar akTarget  ;@line 12
						Jump _label0                                             ;@line 12
					_label0:
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
				.function OnDeath
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param akKiller Actor
					.endParamTable
					.localTable
						.local ::temp4 astraasedioguard
						.local ::temp5 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						Cast ::temp4 None                                        ;@line 17
						CompareEQ ::temp5 ::Controller_var ::temp4               ;@line 17
						Not ::temp5 ::temp5                                      ;@line 17
						JumpF ::temp5 _label1                                    ;@line 17
						CallMethod StopV23 ::Controller_var ::NoneVar            ;@line 18
						Jump _label1                                             ;@line 18
					_label1:
					.endCode
				.endFunction
				.function OnLoad
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp0 astraasedioguard
						.local ::temp1 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						Cast ::temp0 None                                        ;@line 5
						CompareEQ ::temp1 ::Controller_var ::temp0               ;@line 5
						Not ::temp1 ::temp1                                      ;@line 5
						JumpF ::temp1 _label2                                    ;@line 5
						CallMethod StartV23 ::Controller_var ::NoneVar           ;@line 6
						Jump _label2                                             ;@line 6
					_label2:
					.endCode
				.endFunction
				.function OnUnload
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp6 astraasedioguard
						.local ::temp7 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						Cast ::temp6 None                                        ;@line 23
						CompareEQ ::temp7 ::Controller_var ::temp6               ;@line 23
						Not ::temp7 ::temp7                                      ;@line 23
						JumpF ::temp7 _label3                                    ;@line 23
						CallMethod StopV23 ::Controller_var ::NoneVar            ;@line 24
						Jump _label3                                             ;@line 24
					_label3:
					.endCode
				.endFunction
			.endState
		.endStateTable
	.endObject
.endObjectTable
