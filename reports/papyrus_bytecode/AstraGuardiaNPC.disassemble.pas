.info
	.source "AstraGuardiaNPC.psc"
	.modifyTime 1791759002 ;Sun Oct 11 19:50:02 2026 Local
	.compileTime 1791759050 ;Sun Oct 11 19:50:50 2026 Local
	.user "AstraAsedio"
	.computer "Build"
.endInfo
.userFlagsRef
	.flag conditional 1	; 0x00000001
	.flag hidden 0	; 0x00000000
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
				.function Torre
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return AstraGuardiaAuto
					.paramTable
					.endParamTable
					.localTable
						.local ::temp0 objectreference
						.local ::temp1 AstraGuardiaAuto
					.endLocalTable
					.code
						CallMethod GetLinkedRef self ::temp0 None                ;@line 4
						Cast ::temp1 ::temp0                                     ;@line 4
						Return ::temp1                                           ;@line 4
					.endCode
				.endFunction
				.function OnUnload
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp13 AstraAsedioGuard
						.local ::temp14 Bool
						.local controller AstraAsedioGuard
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod ControllerV23 self ::temp13                   ;@line 41
						Assign controller ::temp13                               ;@line 41
						Cast ::temp13 None                                       ;@line 42
						CompareEQ ::temp14 controller ::temp13                   ;@line 42
						Not ::temp14 ::temp14                                    ;@line 42
						JumpF ::temp14 _label0                                   ;@line 42
						CallMethod StopV23 controller ::NoneVar                  ;@line 43
						Jump _label0                                             ;@line 43
					_label0:
					.endCode
				.endFunction
				.function OnLoad
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp6 AstraAsedioGuard
						.local ::temp7 Bool
						.local controller AstraAsedioGuard
						.local ::NoneVar None
						.local ::temp8 Actor
					.endLocalTable
					.code
						CallMethod ControllerV23 self ::temp6                    ;@line 19
						Assign controller ::temp6                                ;@line 19
						Cast ::temp6 None                                        ;@line 20
						CompareEQ ::temp7 controller ::temp6                     ;@line 20
						Not ::temp7 ::temp7                                      ;@line 20
						JumpF ::temp7 _label1                                    ;@line 20
						CallMethod StartV23 controller ::NoneVar                 ;@line 21
						CallMethod GetCombatTarget self ::temp8                  ;@line 22
						CallMethod NotifyCombatV23 controller ::NoneVar ::temp8  ;@line 22
						Jump _label1                                             ;@line 22
					_label1:
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
				.function ControllerV23
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return AstraAsedioGuard
					.paramTable
					.endParamTable
					.localTable
						.local ::temp2 objectreference
						.local ::temp3 AstraAsedioGuard
					.endLocalTable
					.code
						CallMethod GetLinkedRef self ::temp2 None                ;@line 8
						Cast ::temp3 ::temp2                                     ;@line 8
						Return ::temp3                                           ;@line 8
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
						.local ::temp9 AstraAsedioGuard
						.local ::temp10 Bool
						.local controller AstraAsedioGuard
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod ControllerV23 self ::temp9                    ;@line 27
						Assign controller ::temp9                                ;@line 27
						Cast ::temp9 None                                        ;@line 28
						CompareEQ ::temp10 controller ::temp9                    ;@line 28
						Not ::temp10 ::temp10                                    ;@line 28
						JumpF ::temp10 _label2                                   ;@line 28
						CallMethod NotifyCombatV23 controller ::NoneVar akTarget  ;@line 29
						Jump _label2                                             ;@line 29
					_label2:
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
						.local ::temp11 AstraAsedioGuard
						.local ::temp12 Bool
						.local controller AstraAsedioGuard
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod ControllerV23 self ::temp11                   ;@line 34
						Assign controller ::temp11                               ;@line 34
						Cast ::temp11 None                                       ;@line 35
						CompareEQ ::temp12 controller ::temp11                   ;@line 35
						Not ::temp12 ::temp12                                    ;@line 35
						JumpF ::temp12 _label3                                   ;@line 35
						CallMethod StopV23 controller ::NoneVar                  ;@line 36
						Jump _label3                                             ;@line 36
					_label3:
					.endCode
				.endFunction
				.function OnInit
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp4 AstraAsedioGuard
						.local ::temp5 Bool
						.local controller AstraAsedioGuard
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod ControllerV23 self ::temp4                    ;@line 12
						Assign controller ::temp4                                ;@line 12
						Cast ::temp4 None                                        ;@line 13
						CompareEQ ::temp5 controller ::temp4                     ;@line 13
						Not ::temp5 ::temp5                                      ;@line 13
						JumpF ::temp5 _label4                                    ;@line 13
						CallMethod StartV23 controller ::NoneVar                 ;@line 14
						Jump _label4                                             ;@line 14
					_label4:
					.endCode
				.endFunction
			.endState
		.endStateTable
	.endObject
.endObjectTable
