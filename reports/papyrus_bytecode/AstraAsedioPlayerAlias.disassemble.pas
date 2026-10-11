.info
	.source "AstraAsedioPlayerAlias.psc"
	.modifyTime 1791645499 ;Sat Oct 10 12:18:19 2026 Local
	.compileTime 1791679483 ;Sat Oct 10 21:44:43 2026 Local
	.user "AstraAsedio"
	.computer "Build"
.endInfo
.userFlagsRef
	.flag hidden 0	; 0x00000000
	.flag conditional 1	; 0x00000001
.endUserFlagsRef
.objectTable
	.object AstraAsedioPlayerAlias ReferenceAlias
		.userFlags 0	; Flags: 0x00000000
		.docString ""
		.autoState 
		.variableTable
			.variable cityRetirementBusy Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::Session_var astraasediosession
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable cityRetirementPending Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
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
				.function RetireLegacyCity
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param oldID Int
						.param newID Int
					.endParamTable
					.localTable
						.local ::temp7 form
						.local ::temp8 objectreference
						.local ::temp9 Bool
						.local ::temp10 Int
						.local ::temp12 astraasedioguard
						.local ::temp13 String
						.local ::temp14 String
						.local replacement objectreference
						.local previous objectreference
						.local ::temp11 Bool
						.local controller astraasedioguard
						.local drained Bool
						.local offset Int
						.local item objectreference
						.local ::NoneVar None
					.endLocalTable
					.code
						CallStatic game GetFormFromFile ::temp7 newID "AstraAsedio_WhiterunTorres.esp"  ;@line 52
						Cast ::temp8 ::temp7                                     ;@line 52
						Assign replacement ::temp8                               ;@line 52
						Cast ::temp8 None                                        ;@line 53
						CompareEQ ::temp9 replacement ::temp8                    ;@line 53
						JumpF ::temp9 _label0                                    ;@line 53
						Return True                                              ;@line 54
						Jump _label0                                             ;@line 54
					_label0:
						CallStatic game GetFormFromFile ::temp7 oldID "AstraAsedio_WhiterunTorres.esp"  ;@line 56
						Cast ::temp8 ::temp7                                     ;@line 56
						Assign previous ::temp8                                  ;@line 56
						Cast ::temp8 None                                        ;@line 57
						CompareEQ ::temp9 previous ::temp8                       ;@line 57
						JumpF ::temp9 _label1                                    ;@line 57
						Return True                                              ;@line 58
						Jump _label1                                             ;@line 58
					_label1:
						CallStatic skse GetPluginVersion ::temp10 "AstraSight"   ;@line 62
						CompareGTE ::temp9 ::temp10 50659328                     ;@line 62
						JumpF ::temp9 _label2                                    ;@line 62
						CallStatic astrasightnative IsEffectsQuiescent ::temp11 previous 0  ;@line 63
						Not ::temp11 ::temp11                                    ;@line 63
						JumpF ::temp11 _label3                                   ;@line 63
						Return False                                             ;@line 64
						Jump _label3                                             ;@line 64
					_label3:
						Jump _label2                                             ;@line 64
					_label2:
						Cast ::temp12 previous                                   ;@line 67
						Assign controller ::temp12                               ;@line 67
						Cast ::temp12 None                                       ;@line 68
						CompareEQ ::temp11 controller ::temp12                   ;@line 68
						Not ::temp11 ::temp11                                    ;@line 68
						JumpF ::temp11 _label4                                   ;@line 68
						CallMethod RetireStation controller ::temp9              ;@line 69
						Assign drained ::temp9                                   ;@line 69
						Not ::temp9 drained                                      ;@line 70
						JumpF ::temp9 _label5                                    ;@line 70
						Return False                                             ;@line 71
						Jump _label5                                             ;@line 71
					_label5:
						Jump _label4                                             ;@line 71
					_label4:
						Assign offset 0                                          ;@line 76
					_label8:
						CompareLT ::temp9 offset 5                               ;@line 77
						JumpF ::temp9 _label6                                    ;@line 77
						IAdd ::temp10 oldID offset                               ;@line 78
						CallStatic game GetFormFromFile ::temp7 ::temp10 "AstraAsedio_WhiterunTorres.esp"  ;@line 78
						Cast ::temp8 ::temp7                                     ;@line 78
						Assign item ::temp8                                      ;@line 78
						Cast ::temp8 None                                        ;@line 79
						CompareEQ ::temp11 item ::temp8                          ;@line 79
						Not ::temp11 ::temp11                                    ;@line 79
						JumpF ::temp11 _label7                                   ;@line 79
						CallMethod Disable item ::NoneVar False                  ;@line 80
						Jump _label7                                             ;@line 80
					_label7:
						IAdd ::temp10 offset 1                                   ;@line 82
						Assign offset ::temp10                                   ;@line 82
						Jump _label8                                             ;@line 82
					_label6:
						Cast ::temp13 oldID                                      ;@line 84
						StrCat ::temp13 "AstraAsedio city retired legacy=" ::temp13  ;@line 84
						StrCat ::temp13 ::temp13 " replacement="                 ;@line 84
						Cast ::temp14 newID                                      ;@line 84
						StrCat ::temp14 ::temp13 ::temp14                        ;@line 84
						CallStatic debug Trace ::NoneVar ::temp14 0              ;@line 84
						Return True                                              ;@line 85
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
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod CleanupSession self ::NoneVar                 ;@line 14
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
						CallMethod CleanupSession self ::NoneVar                 ;@line 10
						CallMethod StartCityRetirement self ::NoneVar            ;@line 11
					.endCode
				.endFunction
				.function OnUpdate
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp5 Bool
						.local ::temp6 Bool
						.local ::NoneVar None
						.local east Bool
						.local west Bool
					.endLocalTable
					.code
						Not ::temp5 cityRetirementPending                        ;@line 34
						JumpF ::temp5 _label9                                    ;@line 34
						Return None                                              ;@line 35
						Jump _label9                                             ;@line 35
					_label9:
						JumpF cityRetirementBusy _label10                        ;@line 37
						CallMethod RegisterForSingleUpdate self ::NoneVar 0.200000  ;@line 38
						Return None                                              ;@line 39
						Jump _label10                                            ;@line 39
					_label10:
						Assign cityRetirementBusy True                           ;@line 41
						CallMethod RetireLegacyCity self ::temp5 2880 2928       ;@line 42
						Assign east ::temp5                                      ;@line 42
						CallMethod RetireLegacyCity self ::temp5 2896 2944       ;@line 43
						Assign west ::temp5                                      ;@line 43
						Not ::temp5 east                                         ;@line 44
						Cast ::temp5 ::temp5                                     ;@line 44
						JumpT ::temp5 _label11                                   ;@line 44
						Not ::temp6 west                                         ;@line 44
						Cast ::temp5 ::temp6                                     ;@line 44
					_label11:
						Assign cityRetirementPending ::temp5                     ;@line 44
						Assign cityRetirementBusy False                          ;@line 45
						JumpF cityRetirementPending _label12                     ;@line 46
						CallMethod RegisterForSingleUpdate self ::NoneVar 0.200000  ;@line 47
						Jump _label12                                            ;@line 47
					_label12:
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
						CallMethod CleanupSession self ::NoneVar                 ;@line 17
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
						Cast ::temp3 None                                        ;@line 20
						CompareEQ ::temp4 ::Session_var ::temp3                  ;@line 20
						Not ::temp4 ::temp4                                      ;@line 20
						JumpF ::temp4 _label13                                   ;@line 20
						CallMethod EmergencyCleanup ::Session_var ::NoneVar      ;@line 21
						Jump _label14                                            ;@line 21
					_label13:
						CallStatic debug Trace ::NoneVar "AstraAsedio player alias PROPERTY_SESSION_NONE" 0  ;@line 23
						CallStatic debug Notification ::NoneVar "Astra: falta la quest de limpieza del jugador."  ;@line 24
					_label14:
					.endCode
				.endFunction
				.function StartCityRetirement
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						Assign cityRetirementPending True                        ;@line 29
						CallMethod RegisterForSingleUpdate self ::NoneVar 0.200000  ;@line 30
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
						CallMethod GetReference self ::temp0                     ;@line 6
						Cast ::temp1 ::temp0                                     ;@line 6
						StrCat ::temp1 "AstraAsedio Player alias initialized ref=" ::temp1  ;@line 6
						StrCat ::temp1 ::temp1 " session="                       ;@line 6
						Cast ::temp2 ::Session_var                               ;@line 6
						StrCat ::temp2 ::temp1 ::temp2                           ;@line 6
						CallStatic debug Trace ::NoneVar ::temp2 0               ;@line 6
						CallMethod StartCityRetirement self ::NoneVar            ;@line 7
					.endCode
				.endFunction
			.endState
		.endStateTable
	.endObject
.endObjectTable
