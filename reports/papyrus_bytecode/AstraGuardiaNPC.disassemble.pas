.info
	.source "AstraGuardiaNPC.psc"
	.modifyTime 1791676167 ;Sat Oct 10 20:49:27 2026 Local
	.compileTime 1791679489 ;Sat Oct 10 21:44:49 2026 Local
	.user "AstraAsedio"
	.computer "Build"
.endInfo
.userFlagsRef
	.flag hidden 0	; 0x00000000
	.flag conditional 1	; 0x00000001
.endUserFlagsRef
.objectTable
	.object AstraGuardiaNPC Actor
		.userFlags 0	; Flags: 0x00000000
		.docString ""
		.autoState 
		.variableTable
		.endVariableTable
		.propertyTable
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
						.local ::temp11 AstraGuardiaAuto
						.local Torre AstraGuardiaAuto
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod Torre self ::temp11                           ;@line 61
						Assign Torre ::temp11                                    ;@line 61
						JumpF Torre _label0                                      ;@line 62
						CallMethod CalmaCombat Torre ::NoneVar                   ;@line 63
						Jump _label0                                             ;@line 63
					_label0:
					.endCode
				.endFunction
				.function Torre
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return AstraGuardiaAuto
					.paramTable
					.endParamTable
					.localTable
						.local ::temp0 objectreference
						.local ::temp1 Bool
						.local enlace objectreference
						.local ::NoneVar None
						.local ::temp2 AstraGuardiaAuto
					.endLocalTable
					.code
						CallMethod GetLinkedRef self ::temp0 None                ;@line 17
						Assign enlace ::temp0                                    ;@line 17
						Cast ::temp0 None                                        ;@line 18
						CompareEQ ::temp1 enlace ::temp0                         ;@line 18
						JumpF ::temp1 _label1                                    ;@line 18
						CallStatic debug Trace ::NoneVar "AstraGuardiaNPC SIN_ENLACE: el NPC no tiene linked ref a la ballesta (Â¿ESP sin regenerar?)" 0  ;@line 19
						Cast ::temp2 None                                        ;@line 20
						Return ::temp2                                           ;@line 20
						Jump _label1                                             ;@line 20
					_label1:
						Cast ::temp2 enlace                                      ;@line 22
						Return ::temp2                                           ;@line 22
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
				.function OnCombatStateChanged
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param akTarget Actor
						.param aeCombatState Int
					.endParamTable
					.localTable
						.local ::temp8 AstraGuardiaAuto
						.local ::temp9 Bool
						.local ::temp10 Bool
						.local Torre AstraGuardiaAuto
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod Torre self ::temp8                            ;@line 45
						Assign Torre ::temp8                                     ;@line 45
						Cast ::temp8 None                                        ;@line 46
						CompareEQ ::temp9 Torre ::temp8                          ;@line 46
						JumpF ::temp9 _label2                                    ;@line 46
						Return None                                              ;@line 47
						Jump _label2                                             ;@line 47
					_label2:
						CompareEQ ::temp9 aeCombatState 1                        ;@line 49
						Cast ::temp9 ::temp9                                     ;@line 49
						JumpT ::temp9 _label3                                    ;@line 49
						CompareEQ ::temp10 aeCombatState 2                       ;@line 49
						Cast ::temp9 ::temp10                                    ;@line 49
					_label3:
						JumpF ::temp9 _label4                                    ;@line 49
						CallMethod AlertaCombat Torre ::NoneVar akTarget         ;@line 51
						Jump _label5                                             ;@line 51
					_label4:
						CompareEQ ::temp10 aeCombatState 0                       ;@line 52
						JumpF ::temp10 _label5                                   ;@line 52
						CallMethod CalmaCombat Torre ::NoneVar                   ;@line 54
						Jump _label5                                             ;@line 54
					_label5:
					.endCode
				.endFunction
				.function OnLoad
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp5 Bool
						.local ::temp6 AstraGuardiaAuto
						.local Torre AstraGuardiaAuto
						.local ::temp7 Actor
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod IsInCombat self ::temp5                       ;@line 36
						JumpF ::temp5 _label6                                    ;@line 36
						CallMethod Torre self ::temp6                            ;@line 37
						Assign Torre ::temp6                                     ;@line 37
						JumpF Torre _label7                                      ;@line 38
						CallMethod GetCombatTarget self ::temp7                  ;@line 39
						CallMethod AlertaCombat Torre ::NoneVar ::temp7          ;@line 39
						Jump _label7                                             ;@line 39
					_label7:
						Jump _label6                                             ;@line 39
					_label6:
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
						.local ::temp3 AstraGuardiaAuto
						.local ::temp4 Bool
						.local Torre AstraGuardiaAuto
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod Torre self ::temp3                            ;@line 27
						Assign Torre ::temp3                                     ;@line 27
						Cast ::temp3 None                                        ;@line 28
						CompareEQ ::temp4 Torre ::temp3                          ;@line 28
						JumpF ::temp4 _label8                                    ;@line 28
						CallStatic debug Trace ::NoneVar "AstraGuardiaNPC enlace no resuelve a AstraGuardiaAuto" 0  ;@line 29
						Jump _label8                                             ;@line 29
					_label8:
					.endCode
				.endFunction
			.endState
		.endStateTable
	.endObject
.endObjectTable
