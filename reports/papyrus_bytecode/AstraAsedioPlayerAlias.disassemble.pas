.info
	.source "AstraAsedioPlayerAlias.psc"
	.modifyTime 1791759002 ;Sun Oct 11 19:50:02 2026 Local
	.compileTime 1791759045 ;Sun Oct 11 19:50:45 2026 Local
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
			.variable ::Session_var astraasediosession
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable cityRetirementPending Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable cityRetirementBusy Bool
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
						CallMethod BootstrapGuardV23 self ::NoneVar              ;@line 8
					.endCode
				.endFunction
				.function BootstrapGuardV23
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp15 form
						.local ::temp16 quest
						.local ::temp17 Bool
						.local ::temp18 Bool
						.local sensors quest
						.local index Int
						.local ::temp19 Int
						.local ::temp20 astraasedioguard
						.local formID Int
						.local controller astraasedioguard
						.local ::NoneVar None
						.local ::temp21 Actor
						.local ::temp22 Bool
						.local ::temp23 Bool
						.local operatorRef Actor
						.local ::temp24 alias
						.local ::temp25 ReferenceAlias
						.local operatorAlias ReferenceAlias
						.local ::temp26 objectreference
					.endLocalTable
					.code
						CallStatic game GetFormFromFile ::temp15 2054 "AstraAsedio_GuardAnim.esp"  ;@line 91
						Cast ::temp16 ::temp15                                   ;@line 91
						Assign sensors ::temp16                                  ;@line 91
						Cast ::temp16 None                                       ;@line 92
						CompareEQ ::temp17 sensors ::temp16                      ;@line 92
						Not ::temp17 ::temp17                                    ;@line 92
						Cast ::temp17 ::temp17                                   ;@line 92
						JumpF ::temp17 _label0                                   ;@line 92
						CallMethod IsRunning sensors ::temp18                    ;@line 92
						Not ::temp18 ::temp18                                    ;@line 92
						Cast ::temp17 ::temp18                                   ;@line 92
					_label0:
						JumpF ::temp17 _label1                                   ;@line 92
						CallMethod Start sensors ::temp18                        ;@line 93
						Jump _label1                                             ;@line 93
					_label1:
						Assign index 0                                           ;@line 95
					_label8:
						CompareLT ::temp18 index 2                               ;@line 96
						JumpF ::temp18 _label2                                   ;@line 96
						IMultiply ::temp19 index 16                              ;@line 97
						IAdd ::temp19 2928 ::temp19                              ;@line 97
						Assign formID ::temp19                                   ;@line 97
						CallStatic game GetFormFromFile ::temp15 formID "AstraAsedio_WhiterunTorres.esp"  ;@line 98
						Cast ::temp20 ::temp15                                   ;@line 98
						Assign controller ::temp20                               ;@line 98
						Cast ::temp20 None                                       ;@line 99
						CompareEQ ::temp17 controller ::temp20                   ;@line 99
						Not ::temp17 ::temp17                                    ;@line 99
						JumpF ::temp17 _label3                                   ;@line 99
						CallMethod StartV23 controller ::NoneVar                 ;@line 102
						IAdd ::temp19 formID 1                                   ;@line 103
						CallStatic game GetFormFromFile ::temp15 ::temp19 "AstraAsedio_WhiterunTorres.esp"  ;@line 103
						Cast ::temp21 ::temp15                                   ;@line 103
						Assign operatorRef ::temp21                              ;@line 103
						Cast ::temp16 None                                       ;@line 104
						CompareEQ ::temp22 sensors ::temp16                      ;@line 104
						Not ::temp22 ::temp22                                    ;@line 104
						Cast ::temp22 ::temp22                                   ;@line 104
						JumpF ::temp22 _label4                                   ;@line 104
						CallMethod IsRunning sensors ::temp23                    ;@line 104
						Cast ::temp22 ::temp23                                   ;@line 104
					_label4:
						Cast ::temp22 ::temp22                                   ;@line 104
						JumpF ::temp22 _label5                                   ;@line 104
						Cast ::temp21 None                                       ;@line 104
						CompareEQ ::temp23 operatorRef ::temp21                  ;@line 104
						Not ::temp23 ::temp23                                    ;@line 104
						Cast ::temp22 ::temp23                                   ;@line 104
					_label5:
						JumpF ::temp22 _label6                                   ;@line 104
						CallMethod GetAlias sensors ::temp24 index               ;@line 105
						Cast ::temp25 ::temp24                                   ;@line 105
						Assign operatorAlias ::temp25                            ;@line 105
						Cast ::temp25 None                                       ;@line 106
						CompareEQ ::temp23 operatorAlias ::temp25                ;@line 106
						Not ::temp23 ::temp23                                    ;@line 106
						JumpF ::temp23 _label7                                   ;@line 106
						CallMethod Clear operatorAlias ::NoneVar                 ;@line 109
						Cast ::temp26 operatorRef                                ;@line 110
						CallMethod ForceRefTo operatorAlias ::NoneVar ::temp26   ;@line 110
						CallMethod EvaluatePackage operatorRef ::NoneVar         ;@line 111
						Jump _label7                                             ;@line 111
					_label7:
						Jump _label6                                             ;@line 111
					_label6:
						Jump _label3                                             ;@line 111
					_label3:
						IAdd ::temp19 index 1                                    ;@line 115
						Assign index ::temp19                                    ;@line 115
						Jump _label8                                             ;@line 115
					_label2:
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
						CallMethod CleanupSession self ::NoneVar                 ;@line 11
						CallMethod StartCityRetirement self ::NoneVar            ;@line 12
						CallMethod BootstrapGuardV23 self ::NoneVar              ;@line 13
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
						CallMethod CleanupSession self ::NoneVar                 ;@line 16
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
						CallStatic game GetFormFromFile ::temp7 newID "AstraAsedio_WhiterunTorres.esp"  ;@line 54
						Cast ::temp8 ::temp7                                     ;@line 54
						Assign replacement ::temp8                               ;@line 54
						Cast ::temp8 None                                        ;@line 55
						CompareEQ ::temp9 replacement ::temp8                    ;@line 55
						JumpF ::temp9 _label9                                    ;@line 55
						Return True                                              ;@line 56
						Jump _label9                                             ;@line 56
					_label9:
						CallStatic game GetFormFromFile ::temp7 oldID "AstraAsedio_WhiterunTorres.esp"  ;@line 58
						Cast ::temp8 ::temp7                                     ;@line 58
						Assign previous ::temp8                                  ;@line 58
						Cast ::temp8 None                                        ;@line 59
						CompareEQ ::temp9 previous ::temp8                       ;@line 59
						JumpF ::temp9 _label10                                   ;@line 59
						Return True                                              ;@line 60
						Jump _label10                                            ;@line 60
					_label10:
						CallStatic skse GetPluginVersion ::temp10 "AstraSight"   ;@line 64
						CompareGTE ::temp9 ::temp10 50659328                     ;@line 64
						JumpF ::temp9 _label11                                   ;@line 64
						CallStatic astrasightnative IsEffectsQuiescent ::temp11 previous 0  ;@line 65
						Not ::temp11 ::temp11                                    ;@line 65
						JumpF ::temp11 _label12                                  ;@line 65
						Return False                                             ;@line 66
						Jump _label12                                            ;@line 66
					_label12:
						Jump _label11                                            ;@line 66
					_label11:
						Cast ::temp12 previous                                   ;@line 69
						Assign controller ::temp12                               ;@line 69
						Cast ::temp12 None                                       ;@line 70
						CompareEQ ::temp11 controller ::temp12                   ;@line 70
						Not ::temp11 ::temp11                                    ;@line 70
						JumpF ::temp11 _label13                                  ;@line 70
						CallMethod RetireStation controller ::temp9              ;@line 71
						Assign drained ::temp9                                   ;@line 71
						Not ::temp9 drained                                      ;@line 72
						JumpF ::temp9 _label14                                   ;@line 72
						Return False                                             ;@line 73
						Jump _label14                                            ;@line 73
					_label14:
						Jump _label13                                            ;@line 73
					_label13:
						Assign offset 0                                          ;@line 78
					_label17:
						CompareLT ::temp9 offset 5                               ;@line 79
						JumpF ::temp9 _label15                                   ;@line 79
						IAdd ::temp10 oldID offset                               ;@line 80
						CallStatic game GetFormFromFile ::temp7 ::temp10 "AstraAsedio_WhiterunTorres.esp"  ;@line 80
						Cast ::temp8 ::temp7                                     ;@line 80
						Assign item ::temp8                                      ;@line 80
						Cast ::temp8 None                                        ;@line 81
						CompareEQ ::temp11 item ::temp8                          ;@line 81
						Not ::temp11 ::temp11                                    ;@line 81
						JumpF ::temp11 _label16                                  ;@line 81
						CallMethod Disable item ::NoneVar False                  ;@line 82
						Jump _label16                                            ;@line 82
					_label16:
						IAdd ::temp10 offset 1                                   ;@line 84
						Assign offset ::temp10                                   ;@line 84
						Jump _label17                                            ;@line 84
					_label15:
						Cast ::temp13 oldID                                      ;@line 86
						StrCat ::temp13 "AstraAsedio city retired legacy=" ::temp13  ;@line 86
						StrCat ::temp13 ::temp13 " replacement="                 ;@line 86
						Cast ::temp14 newID                                      ;@line 86
						StrCat ::temp14 ::temp13 ::temp14                        ;@line 86
						CallStatic debug Trace ::NoneVar ::temp14 0              ;@line 86
						Return True                                              ;@line 87
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
						Not ::temp5 cityRetirementPending                        ;@line 36
						JumpF ::temp5 _label18                                   ;@line 36
						Return None                                              ;@line 37
						Jump _label18                                            ;@line 37
					_label18:
						JumpF cityRetirementBusy _label19                        ;@line 39
						CallMethod RegisterForSingleUpdate self ::NoneVar 0.200000  ;@line 40
						Return None                                              ;@line 41
						Jump _label19                                            ;@line 41
					_label19:
						Assign cityRetirementBusy True                           ;@line 43
						CallMethod RetireLegacyCity self ::temp5 2880 2928       ;@line 44
						Assign east ::temp5                                      ;@line 44
						CallMethod RetireLegacyCity self ::temp5 2896 2944       ;@line 45
						Assign west ::temp5                                      ;@line 45
						Not ::temp5 east                                         ;@line 46
						Cast ::temp5 ::temp5                                     ;@line 46
						JumpT ::temp5 _label20                                   ;@line 46
						Not ::temp6 west                                         ;@line 46
						Cast ::temp5 ::temp6                                     ;@line 46
					_label20:
						Assign cityRetirementPending ::temp5                     ;@line 46
						Assign cityRetirementBusy False                          ;@line 47
						JumpF cityRetirementPending _label21                     ;@line 48
						CallMethod RegisterForSingleUpdate self ::NoneVar 0.200000  ;@line 49
						Jump _label21                                            ;@line 49
					_label21:
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
						Assign cityRetirementPending True                        ;@line 31
						CallMethod RegisterForSingleUpdate self ::NoneVar 0.200000  ;@line 32
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
						CallMethod CleanupSession self ::NoneVar                 ;@line 19
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
						Cast ::temp3 None                                        ;@line 22
						CompareEQ ::temp4 ::Session_var ::temp3                  ;@line 22
						Not ::temp4 ::temp4                                      ;@line 22
						JumpF ::temp4 _label22                                   ;@line 22
						CallMethod EmergencyCleanup ::Session_var ::NoneVar      ;@line 23
						Jump _label23                                            ;@line 23
					_label22:
						CallStatic debug Trace ::NoneVar "AstraAsedio player alias PROPERTY_SESSION_NONE" 0  ;@line 25
						CallStatic debug Notification ::NoneVar "Astra: falta la quest de limpieza del jugador."  ;@line 26
					_label23:
					.endCode
				.endFunction
			.endState
		.endStateTable
	.endObject
.endObjectTable
