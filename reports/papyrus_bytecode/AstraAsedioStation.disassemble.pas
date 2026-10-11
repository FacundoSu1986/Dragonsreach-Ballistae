.info
	.source "AstraAsedioStation.psc"
	.modifyTime 1791718973 ;Sun Oct 11 08:42:53 2026 Local
	.compileTime 1791759047 ;Sun Oct 11 19:50:47 2026 Local
	.user "AstraAsedio"
	.computer "Build"
.endInfo
.userFlagsRef
	.flag hidden 0	; 0x00000000
	.flag conditional 1	; 0x00000001
.endUserFlagsRef
.objectTable
	.object AstraAsedioStation AstraAsedioActi
		.userFlags 0	; Flags: 0x00000000
		.docString ""
		.autoState 
		.variableTable
			.variable stationReleaseStarted Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable stationDestroyed Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable stationWaitStarted Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable stationLease Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable ::Guard_var astraasedioguard
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable stationReleaseDeadline Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable stationBusy Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable stationCoordinator astraasedioguard
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable stationUnavailable Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable stationRevision Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable stationWaiting Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable stationWaitDeadline Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable stationBusyRevision Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1
			.endVariable
			.variable stationReleasing Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
		.endVariableTable
		.propertyTable
			.property Guard astraasedioguard auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Guard_var
			.endProperty
		.endPropertyTable
		.stateTable
			.state 
				.function OnUpdate
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp39 Bool
						.local ::temp40 Bool
						.local ::NoneVar None
						.local ::temp41 Bool
						.local updateRevision Int
						.local coordinator astraasedioguard
						.local lease Int
						.local active Bool
						.local stillActive Bool
					.endLocalTable
					.code
						JumpF stationWaiting _label0                             ;@line 332
						CallMethod PollStationEntry self ::NoneVar               ;@line 333
						Jump _label1                                             ;@line 333
					_label0:
						JumpF stationReleasing _label2                           ;@line 334
						CallMethod PollStationRelease self ::NoneVar             ;@line 335
						Jump _label1                                             ;@line 335
					_label2:
						Not ::temp39 stationBusy                                 ;@line 336
						Cast ::temp39 ::temp39                                   ;@line 336
						JumpF ::temp39 _label3                                   ;@line 336
						CompareGT ::temp40 stationLease 0                        ;@line 336
						Cast ::temp39 ::temp40                                   ;@line 336
					_label3:
						JumpF ::temp39 _label1                                   ;@line 336
						Assign stationBusy True                                  ;@line 337
						Assign updateRevision stationRevision                    ;@line 338
						Assign stationBusyRevision updateRevision                ;@line 339
						Assign coordinator stationCoordinator                    ;@line 340
						Assign lease stationLease                                ;@line 341
						CallParent IsPlayerOperating ::temp40                    ;@line 342
						Assign active ::temp40                                   ;@line 342
						CallMethod StationCurrent self ::temp40 updateRevision coordinator lease  ;@line 343
						Cast ::temp40 ::temp40                                   ;@line 343
						JumpF ::temp40 _label4                                   ;@line 343
						Cast ::temp40 active                                     ;@line 343
					_label4:
						JumpF ::temp40 _label5                                   ;@line 343
						CallParent OnUpdate ::NoneVar                            ;@line 344
						Jump _label5                                             ;@line 344
					_label5:
						CallParent IsPlayerOperating ::temp40                    ;@line 346
						Assign stillActive ::temp40                              ;@line 346
						CallMethod FinishStationCall self ::NoneVar updateRevision  ;@line 347
						CallMethod StationCurrent self ::temp40 updateRevision coordinator lease  ;@line 348
						Not ::temp40 ::temp40                                    ;@line 348
						Cast ::temp40 ::temp40                                   ;@line 348
						JumpT ::temp40 _label6                                   ;@line 348
						Not ::temp41 stillActive                                 ;@line 348
						Cast ::temp40 ::temp41                                   ;@line 348
					_label6:
						JumpF ::temp40 _label7                                   ;@line 348
						CallMethod EndSession self ::NoneVar                     ;@line 349
						Jump _label7                                             ;@line 349
					_label7:
						Jump _label1                                             ;@line 349
					_label1:
						CallMethod ScheduleStationPoll self ::NoneVar            ;@line 352
					.endCode
				.endFunction
				.function StationCurrent
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param expectedRevision Int
						.param expectedGuard astraasedioguard
						.param expectedLease Int
					.endParamTable
					.localTable
						.local ::temp0 Bool
						.local ::temp1 Bool
					.endLocalTable
					.code
						CompareEQ ::temp0 stationRevision expectedRevision       ;@line 25
						Cast ::temp0 ::temp0                                     ;@line 25
						JumpF ::temp0 _label8                                    ;@line 25
						CompareEQ ::temp1 stationCoordinator expectedGuard       ;@line 25
						Cast ::temp0 ::temp1                                     ;@line 25
					_label8:
						Cast ::temp0 ::temp0                                     ;@line 25
						JumpF ::temp0 _label9                                    ;@line 25
						CompareEQ ::temp1 stationLease expectedLease             ;@line 25
						Cast ::temp0 ::temp1                                     ;@line 25
					_label9:
						Return ::temp0                                           ;@line 25
					.endCode
				.endFunction
				.function OnLoad
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp47 String
						.local ::temp48 String
						.local ::NoneVar None
						.local ::temp49 Int
						.local ::temp50 Bool
						.local ::temp51 astraasedioguard
						.local loadRevision Int
						.local ownSlot Bool
					.endLocalTable
					.code
						Cast ::temp47 self                                       ;@line 383
						StrCat ::temp47 "AstraAsedioStation OnLoad ref=" ::temp47  ;@line 383
						StrCat ::temp47 ::temp47 " revision="                    ;@line 383
						Cast ::temp48 stationRevision                            ;@line 383
						StrCat ::temp48 ::temp47 ::temp48                        ;@line 383
						CallStatic debug Trace ::NoneVar ::temp48 0              ;@line 383
						Assign stationUnavailable False                          ;@line 385
						IAdd ::temp49 stationRevision 1                          ;@line 386
						Assign stationRevision ::temp49                          ;@line 386
						Assign loadRevision stationRevision                      ;@line 387
						Not ::temp50 stationBusy                                 ;@line 388
						Assign ownSlot ::temp50                                  ;@line 388
						JumpF ownSlot _label10                                   ;@line 389
						Assign stationBusy True                                  ;@line 390
						Assign stationBusyRevision loadRevision                  ;@line 391
						Jump _label10                                            ;@line 391
					_label10:
						Assign stationWaiting False                              ;@line 393
						Assign stationReleaseStarted 0.000000                    ;@line 394
						Assign stationReleaseDeadline 0.000000                   ;@line 395
						Cast ::temp51 None                                       ;@line 396
						CompareEQ ::temp50 stationCoordinator ::temp51           ;@line 396
						Not ::temp50 ::temp50                                    ;@line 396
						Assign stationReleasing ::temp50                         ;@line 396
						CallParent RecoverStationLoad ::NoneVar                  ;@line 399
						CallParent NormalizeTimingProperties ::NoneVar           ;@line 400
						CallMethod BlockActivation self ::NoneVar True           ;@line 401
						JumpF ownSlot _label11                                   ;@line 402
						CallMethod FinishStationCall self ::NoneVar loadRevision  ;@line 403
						Jump _label11                                            ;@line 403
					_label11:
						CallMethod PollStationRelease self ::NoneVar             ;@line 405
						CallMethod ScheduleStationPoll self ::NoneVar            ;@line 406
					.endCode
				.endFunction
				.function OnUnload
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp42 String
						.local ::temp43 String
						.local ::NoneVar None
					.endLocalTable
					.code
						Cast ::temp42 self                                       ;@line 364
						StrCat ::temp42 "AstraAsedioStation OnUnload ref=" ::temp42  ;@line 364
						StrCat ::temp42 ::temp42 " revision="                    ;@line 364
						Cast ::temp43 stationRevision                            ;@line 364
						StrCat ::temp43 ::temp42 ::temp43                        ;@line 364
						CallStatic debug Trace ::NoneVar ::temp43 0              ;@line 364
						Assign stationUnavailable True                           ;@line 365
						CallMethod EndSession self ::NoneVar                     ;@line 366
					.endCode
				.endFunction
				.function OnCellDetach
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp44 String
						.local ::temp45 String
						.local ::NoneVar None
					.endLocalTable
					.code
						Cast ::temp44 self                                       ;@line 370
						StrCat ::temp44 "AstraAsedioStation OnCellDetach ref=" ::temp44  ;@line 370
						StrCat ::temp44 ::temp44 " revision="                    ;@line 370
						Cast ::temp45 stationRevision                            ;@line 370
						StrCat ::temp45 ::temp44 ::temp45                        ;@line 370
						CallStatic debug Trace ::NoneVar ::temp45 0              ;@line 370
						Assign stationUnavailable True                           ;@line 371
						CallMethod EndSession self ::NoneVar                     ;@line 372
					.endCode
				.endFunction
				.function FinishStationCall
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param expectedRevision Int
					.endParamTable
					.localTable
						.local ::temp4 Bool
					.endLocalTable
					.code
						Cast ::temp4 stationBusy                                 ;@line 39
						JumpF ::temp4 _label12                                   ;@line 39
						CompareEQ ::temp4 stationBusyRevision expectedRevision   ;@line 39
						Cast ::temp4 ::temp4                                     ;@line 39
					_label12:
						JumpF ::temp4 _label13                                   ;@line 39
						Assign stationBusy False                                 ;@line 40
						Assign stationBusyRevision -1                            ;@line 41
						Jump _label13                                            ;@line 41
					_label13:
					.endCode
				.endFunction
				.function OnInit
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						CallParent OnInit ::NoneVar                              ;@line 21
					.endCode
				.endFunction
				.function OnActivate
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param akActionRef ObjectReference
					.endParamTable
					.localTable
						.local ::temp7 Bool
						.local ::temp8 String
						.local ::temp9 String
						.local ::NoneVar None
						.local ::temp10 actor
						.local ::temp11 ObjectReference
						.local ::temp12 Bool
						.local ::temp14 astraasedioguard
						.local ::temp15 Int
						.local ::temp16 Float
						.local activationRevision Int
						.local coordinator astraasedioguard
						.local lease Int
						.local operator actor
						.local ::temp13 Bool
						.local active Bool
						.local stillActive Bool
						.local configuredGuard astraasedioguard
						.local nativeFailure String
						.local now Float
					.endLocalTable
					.code
						Cast ::temp7 stationBusy                                 ;@line 79
						JumpT ::temp7 _label14                                   ;@line 79
						Cast ::temp7 stationWaiting                              ;@line 79
					_label14:
						Cast ::temp7 ::temp7                                     ;@line 79
						JumpT ::temp7 _label15                                   ;@line 79
						Cast ::temp7 stationReleasing                            ;@line 79
					_label15:
						Cast ::temp7 ::temp7                                     ;@line 79
						JumpT ::temp7 _label16                                   ;@line 79
						Cast ::temp7 stationDestroyed                            ;@line 79
					_label16:
						Cast ::temp7 ::temp7                                     ;@line 79
						JumpT ::temp7 _label17                                   ;@line 79
						Cast ::temp7 stationUnavailable                          ;@line 79
					_label17:
						JumpF ::temp7 _label18                                   ;@line 79
						Return None                                              ;@line 80
						Jump _label18                                            ;@line 80
					_label18:
						Assign stationBusy True                                  ;@line 82
						Assign activationRevision stationRevision                ;@line 83
						Assign stationBusyRevision activationRevision            ;@line 84
						Cast ::temp8 self                                        ;@line 85
						StrCat ::temp8 "AstraAsedioStation activate ref=" ::temp8  ;@line 85
						StrCat ::temp8 ::temp8 " revision="                      ;@line 85
						Cast ::temp9 activationRevision                          ;@line 85
						StrCat ::temp9 ::temp8 ::temp9                           ;@line 85
						CallStatic debug Trace ::NoneVar ::temp9 0               ;@line 85
						Assign coordinator stationCoordinator                    ;@line 86
						Assign lease stationLease                                ;@line 87
						CallStatic game GetPlayer ::temp10                       ;@line 88
						Assign operator ::temp10                                 ;@line 88
						CallMethod StationCurrent self ::temp7 activationRevision coordinator lease  ;@line 89
						Not ::temp7 ::temp7                                      ;@line 89
						Cast ::temp7 ::temp7                                     ;@line 89
						JumpT ::temp7 _label19                                   ;@line 89
						Cast ::temp11 operator                                   ;@line 89
						CompareEQ ::temp12 akActionRef ::temp11                  ;@line 89
						Not ::temp12 ::temp12                                    ;@line 89
						Cast ::temp7 ::temp12                                    ;@line 89
					_label19:
						JumpF ::temp7 _label20                                   ;@line 89
						CallMethod FinishStationCall self ::NoneVar activationRevision  ;@line 90
						CallMethod ScheduleStationPoll self ::NoneVar            ;@line 91
						Return None                                              ;@line 92
						Jump _label20                                            ;@line 92
					_label20:
						CompareGT ::temp12 lease 0                               ;@line 94
						JumpF ::temp12 _label21                                  ;@line 94
						CallParent IsPlayerOperating ::temp7                     ;@line 95
						Assign active ::temp7                                    ;@line 95
						CallMethod StationCurrent self ::temp7 activationRevision coordinator lease  ;@line 96
						Cast ::temp7 ::temp7                                     ;@line 96
						JumpF ::temp7 _label22                                   ;@line 96
						Cast ::temp7 active                                      ;@line 96
					_label22:
						JumpF ::temp7 _label23                                   ;@line 96
						CallParent OnActivate ::NoneVar akActionRef              ;@line 98
						Jump _label23                                            ;@line 98
					_label23:
						CallParent IsPlayerOperating ::temp7                     ;@line 100
						Assign stillActive ::temp7                               ;@line 100
						CallMethod FinishStationCall self ::NoneVar activationRevision  ;@line 101
						CallMethod StationCurrent self ::temp7 activationRevision coordinator lease  ;@line 102
						Not ::temp7 ::temp7                                      ;@line 102
						Cast ::temp7 ::temp7                                     ;@line 102
						JumpT ::temp7 _label24                                   ;@line 102
						Not ::temp13 stillActive                                 ;@line 102
						Cast ::temp7 ::temp13                                    ;@line 102
					_label24:
						JumpF ::temp7 _label25                                   ;@line 102
						CallMethod EndSession self ::NoneVar                     ;@line 103
						Jump _label25                                            ;@line 103
					_label25:
						Return None                                              ;@line 105
						Jump _label21                                            ;@line 105
					_label21:
						Assign configuredGuard ::Guard_var                       ;@line 107
						Cast ::temp14 None                                       ;@line 108
						CompareEQ ::temp13 configuredGuard ::temp14              ;@line 108
						JumpF ::temp13 _label26                                  ;@line 108
						CallMethod FinishStationCall self ::NoneVar activationRevision  ;@line 109
						CallParent RejectActivation ::NoneVar "PROPERTY_GUARD_NONE: falta el coordinador de la estaciÃ³n."  ;@line 110
						Return None                                              ;@line 111
						Jump _label26                                            ;@line 111
					_label26:
						CallMethod StationNativeFailure self ::temp8 activationRevision coordinator lease  ;@line 113
						Assign nativeFailure ::temp8                             ;@line 113
						CallMethod StationCurrent self ::temp7 activationRevision coordinator lease  ;@line 114
						Not ::temp12 ::temp7                                     ;@line 114
						JumpF ::temp12 _label27                                  ;@line 114
						CallMethod FinishStationCall self ::NoneVar activationRevision  ;@line 115
						CallMethod ScheduleStationPoll self ::NoneVar            ;@line 116
						Return None                                              ;@line 117
						Jump _label27                                            ;@line 117
					_label27:
						CompareEQ ::temp13 nativeFailure ""                      ;@line 119
						Not ::temp13 ::temp13                                    ;@line 119
						JumpF ::temp13 _label28                                  ;@line 119
						CallParent RejectActivation ::NoneVar nativeFailure      ;@line 120
						CallMethod FinishStationCall self ::NoneVar activationRevision  ;@line 121
						CallMethod ScheduleStationPoll self ::NoneVar            ;@line 122
						Return None                                              ;@line 123
						Jump _label28                                            ;@line 123
					_label28:
						Assign coordinator configuredGuard                       ;@line 125
						IAdd ::temp15 stationRevision 1                          ;@line 126
						Assign stationRevision ::temp15                          ;@line 126
						Assign activationRevision stationRevision                ;@line 127
						Assign stationBusyRevision activationRevision            ;@line 128
						Assign stationCoordinator coordinator                    ;@line 129
						Assign stationWaiting True                               ;@line 130
						CallMethod ReservePlayerLease coordinator ::temp15       ;@line 131
						Assign lease ::temp15                                    ;@line 131
						CompareGT ::temp7 lease 0                                ;@line 134
						JumpF ::temp7 _label29                                   ;@line 134
						Assign stationLease lease                                ;@line 135
						Jump _label29                                            ;@line 135
					_label29:
						CallMethod StationCurrent self ::temp12 activationRevision coordinator lease  ;@line 137
						Not ::temp13 ::temp12                                    ;@line 137
						Cast ::temp12 ::temp13                                   ;@line 137
						JumpT ::temp12 _label30                                  ;@line 137
						CompareLTE ::temp7 lease 0                               ;@line 137
						Cast ::temp12 ::temp7                                    ;@line 137
					_label30:
						JumpF ::temp12 _label31                                  ;@line 137
						Cast ::temp9 self                                        ;@line 138
						StrCat ::temp8 "AstraAsedioStation reservation rejected ref=" ::temp9  ;@line 138
						StrCat ::temp9 ::temp8 " lease="                         ;@line 138
						Cast ::temp8 lease                                       ;@line 138
						StrCat ::temp8 ::temp9 ::temp8                           ;@line 138
						CallStatic debug Trace ::NoneVar ::temp8 0               ;@line 138
						CallMethod FinishStationCall self ::NoneVar activationRevision  ;@line 139
						CallMethod EndSession self ::NoneVar                     ;@line 140
						Return None                                              ;@line 141
						Jump _label31                                            ;@line 141
					_label31:
						CallStatic utility GetCurrentRealTime ::temp16           ;@line 143
						Assign now ::temp16                                      ;@line 143
						CallMethod StationCurrent self ::temp13 activationRevision coordinator lease  ;@line 144
						Not ::temp7 ::temp13                                     ;@line 144
						Cast ::temp13 ::temp7                                    ;@line 144
						JumpT ::temp13 _label32                                  ;@line 144
						CompareEQ ::temp12 now now                               ;@line 144
						Not ::temp12 ::temp12                                    ;@line 144
						Cast ::temp13 ::temp12                                   ;@line 144
					_label32:
						Cast ::temp12 ::temp13                                   ;@line 144
						JumpT ::temp12 _label33                                  ;@line 144
						CompareLT ::temp7 now 0.000000                           ;@line 144
						Cast ::temp12 ::temp7                                    ;@line 144
					_label33:
						Cast ::temp7 ::temp12                                    ;@line 144
						JumpT ::temp7 _label34                                   ;@line 144
						CompareGT ::temp13 now 1000000000.000000                 ;@line 144
						Cast ::temp7 ::temp13                                    ;@line 144
					_label34:
						JumpF ::temp7 _label35                                   ;@line 144
						CallMethod FinishStationCall self ::NoneVar activationRevision  ;@line 145
						CallMethod EndSession self ::NoneVar                     ;@line 146
						Return None                                              ;@line 147
						Jump _label35                                            ;@line 147
					_label35:
						Assign stationWaitStarted now                            ;@line 149
						FAdd ::temp16 now 10.000000                              ;@line 152
						Assign stationWaitDeadline ::temp16                      ;@line 152
						CallParent RegisterMenus ::NoneVar                       ;@line 153
						CallMethod FinishStationCall self ::NoneVar activationRevision  ;@line 154
						CallMethod StationCurrent self ::temp12 activationRevision coordinator lease  ;@line 155
						Not ::temp13 ::temp12                                    ;@line 155
						JumpF ::temp13 _label36                                  ;@line 155
						CallMethod EndSession self ::NoneVar                     ;@line 156
						Return None                                              ;@line 157
						Jump _label36                                            ;@line 157
					_label36:
						CallMethod PollStationEntry self ::NoneVar               ;@line 159
					.endCode
				.endFunction
				.function ScheduleStationPoll
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp2 Bool
						.local ::temp3 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						Cast ::temp2 stationWaiting                              ;@line 31
						JumpT ::temp2 _label37                                   ;@line 31
						Cast ::temp2 stationReleasing                            ;@line 31
					_label37:
						Cast ::temp2 ::temp2                                     ;@line 31
						JumpT ::temp2 _label38                                   ;@line 31
						Cast ::temp3 stationBusy                                 ;@line 31
						JumpF ::temp3 _label39                                   ;@line 31
						CompareGT ::temp3 stationLease 0                         ;@line 31
						Cast ::temp3 ::temp3                                     ;@line 31
					_label39:
						Cast ::temp2 ::temp3                                     ;@line 31
					_label38:
						JumpF ::temp2 _label40                                   ;@line 31
						CallMethod RegisterForSingleUpdate self ::NoneVar 0.050000  ;@line 32
						Jump _label40                                            ;@line 32
					_label40:
					.endCode
				.endFunction
				.function StationEntryValid
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param expectedRevision Int
						.param expectedGuard astraasedioguard
						.param expectedLease Int
						.param operator actor
					.endParamTable
					.localTable
						.local ::temp17 Bool
						.local ::temp18 actor
						.local ::temp19 Bool
						.local ::temp20 Float
						.local loaded Bool
						.local menuOpen Bool
						.local dead Bool
						.local now Float
					.endLocalTable
					.code
						CallMethod StationCurrent self ::temp17 expectedRevision expectedGuard expectedLease  ;@line 163
						Not ::temp17 ::temp17                                    ;@line 163
						Cast ::temp17 ::temp17                                   ;@line 163
						JumpT ::temp17 _label41                                  ;@line 163
						Cast ::temp18 None                                       ;@line 163
						CompareEQ ::temp19 operator ::temp18                     ;@line 163
						Cast ::temp17 ::temp19                                   ;@line 163
					_label41:
						Cast ::temp19 ::temp17                                   ;@line 163
						JumpT ::temp19 _label42                                  ;@line 163
						Cast ::temp19 stationUnavailable                         ;@line 163
					_label42:
						Cast ::temp17 ::temp19                                   ;@line 163
						JumpT ::temp17 _label43                                  ;@line 163
						Cast ::temp17 stationDestroyed                           ;@line 163
					_label43:
						JumpF ::temp17 _label44                                  ;@line 163
						Return False                                             ;@line 164
						Jump _label44                                            ;@line 164
					_label44:
						CallMethod Is3DLoaded self ::temp19                      ;@line 166
						Assign loaded ::temp19                                   ;@line 166
						CallMethod StationCurrent self ::temp17 expectedRevision expectedGuard expectedLease  ;@line 167
						Not ::temp19 ::temp17                                    ;@line 167
						Cast ::temp19 ::temp19                                   ;@line 167
						JumpT ::temp19 _label45                                  ;@line 167
						Not ::temp17 loaded                                      ;@line 167
						Cast ::temp19 ::temp17                                   ;@line 167
					_label45:
						JumpF ::temp19 _label46                                  ;@line 167
						Return False                                             ;@line 168
						Jump _label46                                            ;@line 168
					_label46:
						CallStatic utility IsInMenuMode ::temp17                 ;@line 170
						Assign menuOpen ::temp17                                 ;@line 170
						CallMethod StationCurrent self ::temp19 expectedRevision expectedGuard expectedLease  ;@line 171
						Not ::temp17 ::temp19                                    ;@line 171
						Cast ::temp19 ::temp17                                   ;@line 171
						JumpT ::temp19 _label47                                  ;@line 171
						Cast ::temp19 menuOpen                                   ;@line 171
					_label47:
						JumpF ::temp19 _label48                                  ;@line 171
						Return False                                             ;@line 172
						Jump _label48                                            ;@line 172
					_label48:
						CallMethod IsDead operator ::temp17                      ;@line 174
						Assign dead ::temp17                                     ;@line 174
						CallMethod StationCurrent self ::temp19 expectedRevision expectedGuard expectedLease  ;@line 175
						Not ::temp17 ::temp19                                    ;@line 175
						Cast ::temp19 ::temp17                                   ;@line 175
						JumpT ::temp19 _label49                                  ;@line 175
						Cast ::temp19 dead                                       ;@line 175
					_label49:
						JumpF ::temp19 _label50                                  ;@line 175
						Return False                                             ;@line 176
						Jump _label50                                            ;@line 176
					_label50:
						CallStatic utility GetCurrentRealTime ::temp20           ;@line 178
						Assign now ::temp20                                      ;@line 178
						CallMethod StationCurrent self ::temp17 expectedRevision expectedGuard expectedLease  ;@line 179
						Cast ::temp17 ::temp17                                   ;@line 179
						JumpF ::temp17 _label51                                  ;@line 179
						CompareEQ ::temp19 now now                               ;@line 179
						Cast ::temp17 ::temp19                                   ;@line 179
					_label51:
						Cast ::temp17 ::temp17                                   ;@line 179
						JumpF ::temp17 _label52                                  ;@line 179
						CompareGTE ::temp19 now stationWaitStarted               ;@line 179
						Cast ::temp17 ::temp19                                   ;@line 179
					_label52:
						Cast ::temp17 ::temp17                                   ;@line 179
						JumpF ::temp17 _label53                                  ;@line 179
						CompareLTE ::temp19 now stationWaitDeadline              ;@line 179
						Cast ::temp17 ::temp19                                   ;@line 179
					_label53:
						Return ::temp17                                          ;@line 179
					.endCode
				.endFunction
				.function PollStationEntry
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp21 Bool
						.local ::temp22 actor
						.local ::temp23 Bool
						.local ::temp26 ObjectReference
						.local entryRevision Int
						.local coordinator astraasedioguard
						.local lease Int
						.local operator actor
						.local valid Bool
						.local ::temp24 String
						.local ::temp25 String
						.local ::NoneVar None
						.local ready Bool
						.local active Bool
					.endLocalTable
					.code
						Cast ::temp21 stationBusy                                ;@line 183
						JumpT ::temp21 _label54                                  ;@line 183
						Not ::temp21 stationWaiting                              ;@line 183
						Cast ::temp21 ::temp21                                   ;@line 183
					_label54:
						Cast ::temp21 ::temp21                                   ;@line 183
						JumpT ::temp21 _label55                                  ;@line 183
						Cast ::temp21 stationReleasing                           ;@line 183
					_label55:
						JumpF ::temp21 _label56                                  ;@line 183
						Return None                                              ;@line 184
						Jump _label56                                            ;@line 184
					_label56:
						Assign stationBusy True                                  ;@line 186
						Assign entryRevision stationRevision                     ;@line 187
						Assign stationBusyRevision entryRevision                 ;@line 188
						Assign coordinator stationCoordinator                    ;@line 189
						Assign lease stationLease                                ;@line 190
						CallStatic game GetPlayer ::temp22                       ;@line 191
						Assign operator ::temp22                                 ;@line 191
						CallMethod StationEntryValid self ::temp21 entryRevision coordinator lease operator  ;@line 192
						Assign valid ::temp21                                    ;@line 192
						CallMethod StationCurrent self ::temp21 entryRevision coordinator lease  ;@line 193
						Not ::temp21 ::temp21                                    ;@line 193
						Cast ::temp21 ::temp21                                   ;@line 193
						JumpT ::temp21 _label57                                  ;@line 193
						Not ::temp23 valid                                       ;@line 193
						Cast ::temp21 ::temp23                                   ;@line 193
					_label57:
						JumpF ::temp21 _label58                                  ;@line 193
						Cast ::temp24 self                                       ;@line 194
						StrCat ::temp24 "AstraAsedioStation entry cancelled before prepare ref=" ::temp24  ;@line 194
						StrCat ::temp24 ::temp24 " lease="                       ;@line 194
						Cast ::temp25 lease                                      ;@line 194
						StrCat ::temp25 ::temp24 ::temp25                        ;@line 194
						CallStatic debug Trace ::NoneVar ::temp25 0              ;@line 194
						CallMethod FinishStationCall self ::NoneVar entryRevision  ;@line 195
						CallMethod EndSession self ::NoneVar                     ;@line 196
						Return None                                              ;@line 197
						Jump _label58                                            ;@line 197
					_label58:
						CallMethod PreparePlayerLease coordinator ::temp23 lease  ;@line 199
						Assign ready ::temp23                                    ;@line 199
						CallMethod StationEntryValid self ::temp21 entryRevision coordinator lease operator  ;@line 201
						Assign valid ::temp21                                    ;@line 201
						CallMethod StationCurrent self ::temp23 entryRevision coordinator lease  ;@line 202
						Not ::temp21 ::temp23                                    ;@line 202
						Cast ::temp21 ::temp21                                   ;@line 202
						JumpT ::temp21 _label59                                  ;@line 202
						Not ::temp23 valid                                       ;@line 202
						Cast ::temp21 ::temp23                                   ;@line 202
					_label59:
						JumpF ::temp21 _label60                                  ;@line 202
						Cast ::temp24 self                                       ;@line 203
						StrCat ::temp25 "AstraAsedioStation entry cancelled after prepare ref=" ::temp24  ;@line 203
						StrCat ::temp24 ::temp25 " lease="                       ;@line 203
						Cast ::temp25 lease                                      ;@line 203
						StrCat ::temp25 ::temp24 ::temp25                        ;@line 203
						StrCat ::temp24 ::temp25 " ready="                       ;@line 203
						Cast ::temp25 ready                                      ;@line 203
						StrCat ::temp25 ::temp24 ::temp25                        ;@line 203
						CallStatic debug Trace ::NoneVar ::temp25 0              ;@line 203
						CallMethod FinishStationCall self ::NoneVar entryRevision  ;@line 204
						CallMethod EndSession self ::NoneVar                     ;@line 205
						Return None                                              ;@line 206
						Jump _label60                                            ;@line 206
					_label60:
						Not ::temp23 ready                                       ;@line 208
						JumpF ::temp23 _label61                                  ;@line 208
						CallMethod FinishStationCall self ::NoneVar entryRevision  ;@line 209
						CallMethod ScheduleStationPoll self ::NoneVar            ;@line 210
						Return None                                              ;@line 211
						Jump _label61                                            ;@line 211
					_label61:
						CallParent ResetStationAim ::NoneVar                     ;@line 213
						CallMethod StationEntryValid self ::temp21 entryRevision coordinator lease operator  ;@line 214
						Assign valid ::temp21                                    ;@line 214
						CallMethod StationCurrent self ::temp23 entryRevision coordinator lease  ;@line 215
						Not ::temp21 ::temp23                                    ;@line 215
						Cast ::temp21 ::temp21                                   ;@line 215
						JumpT ::temp21 _label62                                  ;@line 215
						Not ::temp23 valid                                       ;@line 215
						Cast ::temp21 ::temp23                                   ;@line 215
					_label62:
						JumpF ::temp21 _label63                                  ;@line 215
						CallMethod FinishStationCall self ::NoneVar entryRevision  ;@line 216
						CallMethod EndSession self ::NoneVar                     ;@line 217
						Return None                                              ;@line 218
						Jump _label63                                            ;@line 218
					_label63:
						Assign stationWaiting False                              ;@line 220
						Cast ::temp24 self                                       ;@line 221
						StrCat ::temp25 "AstraAsedioStation entering player sight ref=" ::temp24  ;@line 221
						StrCat ::temp24 ::temp25 " lease="                       ;@line 221
						Cast ::temp25 lease                                      ;@line 221
						StrCat ::temp25 ::temp24 ::temp25                        ;@line 221
						CallStatic debug Trace ::NoneVar ::temp25 0              ;@line 221
						Cast ::temp26 operator                                   ;@line 222
						CallParent OnActivate ::NoneVar ::temp26                 ;@line 222
						CallParent IsPlayerOperating ::temp23                    ;@line 225
						Assign active ::temp23                                   ;@line 225
						CallMethod FinishStationCall self ::NoneVar entryRevision  ;@line 226
						CallMethod StationCurrent self ::temp21 entryRevision coordinator lease  ;@line 227
						Not ::temp23 ::temp21                                    ;@line 227
						Cast ::temp23 ::temp23                                   ;@line 227
						JumpT ::temp23 _label64                                  ;@line 227
						Not ::temp21 active                                      ;@line 227
						Cast ::temp23 ::temp21                                   ;@line 227
					_label64:
						JumpF ::temp23 _label65                                  ;@line 227
						CallMethod EndSession self ::NoneVar                     ;@line 228
						Jump _label65                                            ;@line 228
					_label65:
					.endCode
				.endFunction
				.function StationNativeFailure
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return String
					.paramTable
						.param expectedRevision Int
						.param expectedGuard astraasedioguard
						.param expectedLease Int
					.endParamTable
					.localTable
						.local ::temp5 Int
						.local ::temp6 Bool
						.local skseVersion Int
						.local pluginVersion Int
						.local api Int
						.local available Bool
					.endLocalTable
					.code
						CallStatic skse GetVersion ::temp5                       ;@line 47
						Assign skseVersion ::temp5                               ;@line 47
						CallMethod StationCurrent self ::temp6 expectedRevision expectedGuard expectedLease  ;@line 48
						Not ::temp6 ::temp6                                      ;@line 48
						JumpF ::temp6 _label66                                   ;@line 48
						Return "STATION_ENTRY_CANCELLED"                         ;@line 49
						Jump _label66                                            ;@line 49
					_label66:
						CompareLT ::temp6 skseVersion 2                          ;@line 51
						JumpF ::temp6 _label67                                   ;@line 51
						Return "SKSE_MISSING: inicia Skyrim con SKSE64."         ;@line 52
						Jump _label67                                            ;@line 52
					_label67:
						CallStatic skse GetPluginVersion ::temp5 "AstraSight"    ;@line 54
						Assign pluginVersion ::temp5                             ;@line 54
						CallMethod StationCurrent self ::temp6 expectedRevision expectedGuard expectedLease  ;@line 55
						Not ::temp6 ::temp6                                      ;@line 55
						JumpF ::temp6 _label68                                   ;@line 55
						Return "STATION_ENTRY_CANCELLED"                         ;@line 56
						Jump _label68                                            ;@line 56
					_label68:
						CompareLT ::temp6 pluginVersion 50659392                 ;@line 58
						JumpF ::temp6 _label69                                   ;@line 58
						Return "NATIVE_SIGHT_MISSING: instala AstraSight.dll 3.5.4 de esta versiÃ³n."  ;@line 59
						Jump _label69                                            ;@line 59
					_label69:
						CallStatic astrasightnative GetAPIVersion ::temp5        ;@line 61
						Assign api ::temp5                                       ;@line 61
						CallMethod StationCurrent self ::temp6 expectedRevision expectedGuard expectedLease  ;@line 62
						Not ::temp6 ::temp6                                      ;@line 62
						JumpF ::temp6 _label70                                   ;@line 62
						Return "STATION_ENTRY_CANCELLED"                         ;@line 63
						Jump _label70                                            ;@line 63
					_label70:
						CompareEQ ::temp6 api 4                                  ;@line 65
						Not ::temp6 ::temp6                                      ;@line 65
						JumpF ::temp6 _label71                                   ;@line 65
						Return "NATIVE_API_MISMATCH: reinstala los archivos completos de esta versiÃ³n."  ;@line 66
						Jump _label71                                            ;@line 66
					_label71:
						CallStatic astrasightnative IsAvailable ::temp6          ;@line 68
						Assign available ::temp6                                 ;@line 68
						CallMethod StationCurrent self ::temp6 expectedRevision expectedGuard expectedLease  ;@line 69
						Not ::temp6 ::temp6                                      ;@line 69
						JumpF ::temp6 _label72                                   ;@line 69
						Return "STATION_ENTRY_CANCELLED"                         ;@line 70
						Jump _label72                                            ;@line 70
					_label72:
						Not ::temp6 available                                    ;@line 72
						JumpF ::temp6 _label73                                   ;@line 72
						Return "NATIVE_SIGHT_UNAVAILABLE: la mira nativa no estÃ¡ disponible."  ;@line 73
						Jump _label73                                            ;@line 73
					_label73:
						Return ""                                                ;@line 75
					.endCode
				.endFunction
				.function OnMenuOpen
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param menuName String
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						JumpF stationWaiting _label74                            ;@line 356
						CallMethod EndSession self ::NoneVar                     ;@line 357
						Jump _label75                                            ;@line 357
					_label74:
						CallParent OnMenuOpen ::NoneVar menuName                 ;@line 359
					_label75:
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
				.function OnDestructionStageChanged
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param aiOldStage Int
						.param aiCurrentStage Int
					.endParamTable
					.localTable
						.local ::temp46 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CompareGT ::temp46 aiCurrentStage 0                      ;@line 376
						JumpF ::temp46 _label76                                  ;@line 376
						Assign stationDestroyed True                             ;@line 377
						CallMethod EndSession self ::NoneVar                     ;@line 378
						Jump _label76                                            ;@line 378
					_label76:
					.endCode
				.endFunction
				.function EndSession
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp27 Int
						.local ::temp28 astraasedioguard
						.local ::temp29 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						IAdd ::temp27 stationRevision 1                          ;@line 234
						Assign stationRevision ::temp27                          ;@line 234
						Assign stationWaiting False                              ;@line 235
						Assign stationReleaseStarted 0.000000                    ;@line 236
						Assign stationReleaseDeadline 0.000000                   ;@line 237
						Cast ::temp28 None                                       ;@line 238
						CompareEQ ::temp29 stationCoordinator ::temp28           ;@line 238
						Not ::temp29 ::temp29                                    ;@line 238
						Assign stationReleasing ::temp29                         ;@line 238
						CallParent EndSession ::NoneVar                          ;@line 239
						CallMethod PollStationRelease self ::NoneVar             ;@line 240
						CallMethod ScheduleStationPoll self ::NoneVar            ;@line 241
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
				.function PollStationRelease
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp30 Bool
						.local ::temp31 Int
						.local ::temp38 astraasedioguard
						.local releaseRevision Int
						.local coordinator astraasedioguard
						.local lease Int
						.local active Bool
						.local ::NoneVar None
						.local pending Bool
						.local pluginVersion Int
						.local quiet Bool
						.local ::temp32 ObjectReference
						.local ::temp33 Bool
						.local ::temp34 Float
						.local ::temp35 Bool
						.local ::temp36 String
						.local ::temp37 String
						.local now Float
						.local clockOk Bool
					.endLocalTable
					.code
						Cast ::temp30 stationBusy                                ;@line 245
						JumpT ::temp30 _label77                                  ;@line 245
						Not ::temp30 stationReleasing                            ;@line 245
						Cast ::temp30 ::temp30                                   ;@line 245
					_label77:
						JumpF ::temp30 _label78                                  ;@line 245
						Return None                                              ;@line 246
						Jump _label78                                            ;@line 246
					_label78:
						Assign stationBusy True                                  ;@line 248
						Assign releaseRevision stationRevision                   ;@line 249
						Assign stationBusyRevision releaseRevision               ;@line 250
						Assign coordinator stationCoordinator                    ;@line 251
						Assign lease stationLease                                ;@line 252
						CallParent IsPlayerOperating ::temp30                    ;@line 253
						Assign active ::temp30                                   ;@line 253
						CallMethod StationCurrent self ::temp30 releaseRevision coordinator lease  ;@line 254
						Not ::temp30 ::temp30                                    ;@line 254
						Cast ::temp30 ::temp30                                   ;@line 254
						JumpT ::temp30 _label79                                  ;@line 254
						Cast ::temp30 active                                     ;@line 254
					_label79:
						JumpF ::temp30 _label80                                  ;@line 254
						CallMethod FinishStationCall self ::NoneVar releaseRevision  ;@line 255
						CallMethod ScheduleStationPoll self ::NoneVar            ;@line 256
						Return None                                              ;@line 257
						Jump _label80                                            ;@line 257
					_label80:
						CallParent IsPlayerCleanupPending ::temp30               ;@line 259
						Assign pending ::temp30                                  ;@line 259
						CallMethod StationCurrent self ::temp30 releaseRevision coordinator lease  ;@line 260
						Not ::temp30 ::temp30                                    ;@line 260
						Cast ::temp30 ::temp30                                   ;@line 260
						JumpT ::temp30 _label81                                  ;@line 260
						Cast ::temp30 pending                                    ;@line 260
					_label81:
						JumpF ::temp30 _label82                                  ;@line 260
						CallMethod FinishStationCall self ::NoneVar releaseRevision  ;@line 261
						CallMethod ScheduleStationPoll self ::NoneVar            ;@line 262
						Return None                                              ;@line 263
						Jump _label82                                            ;@line 263
					_label82:
						CallStatic skse GetPluginVersion ::temp31 "AstraSight"   ;@line 266
						Assign pluginVersion ::temp31                            ;@line 266
						CallMethod StationCurrent self ::temp30 releaseRevision coordinator lease  ;@line 267
						Not ::temp30 ::temp30                                    ;@line 267
						JumpF ::temp30 _label83                                  ;@line 267
						CallMethod FinishStationCall self ::NoneVar releaseRevision  ;@line 268
						CallMethod ScheduleStationPoll self ::NoneVar            ;@line 269
						Return None                                              ;@line 270
						Jump _label83                                            ;@line 270
					_label83:
						Assign quiet True                                        ;@line 272
						CompareGTE ::temp30 pluginVersion 50659328               ;@line 273
						JumpF ::temp30 _label84                                  ;@line 273
						Cast ::temp32 self                                       ;@line 274
						CallStatic astrasightnative IsEffectsQuiescent ::temp33 ::temp32 0  ;@line 274
						Assign quiet ::temp33                                    ;@line 274
						Jump _label84                                            ;@line 274
					_label84:
						CallMethod StationCurrent self ::temp33 releaseRevision coordinator lease  ;@line 276
						Not ::temp30 ::temp33                                    ;@line 276
						JumpF ::temp30 _label85                                  ;@line 276
						CallMethod FinishStationCall self ::NoneVar releaseRevision  ;@line 277
						CallMethod ScheduleStationPoll self ::NoneVar            ;@line 278
						Return None                                              ;@line 279
						Jump _label85                                            ;@line 279
					_label85:
						Not ::temp33 quiet                                       ;@line 281
						JumpF ::temp33 _label86                                  ;@line 281
						CallStatic utility GetCurrentRealTime ::temp34           ;@line 282
						Assign now ::temp34                                      ;@line 282
						CallMethod StationCurrent self ::temp30 releaseRevision coordinator lease  ;@line 283
						Not ::temp30 ::temp30                                    ;@line 283
						JumpF ::temp30 _label87                                  ;@line 283
						CallMethod FinishStationCall self ::NoneVar releaseRevision  ;@line 284
						CallMethod ScheduleStationPoll self ::NoneVar            ;@line 285
						Return None                                              ;@line 286
						Jump _label87                                            ;@line 286
					_label87:
						CompareEQ ::temp30 now now                               ;@line 290
						Cast ::temp30 ::temp30                                   ;@line 290
						JumpF ::temp30 _label88                                  ;@line 290
						CompareGTE ::temp35 now 0.000000                         ;@line 290
						Cast ::temp30 ::temp35                                   ;@line 290
					_label88:
						Cast ::temp30 ::temp30                                   ;@line 290
						JumpF ::temp30 _label89                                  ;@line 290
						CompareLTE ::temp35 now 1000000000.000000                ;@line 290
						Cast ::temp30 ::temp35                                   ;@line 290
					_label89:
						Assign clockOk ::temp30                                  ;@line 290
						Cast ::temp30 clockOk                                    ;@line 291
						JumpF ::temp30 _label90                                  ;@line 291
						CompareLTE ::temp35 stationReleaseDeadline 0.000000      ;@line 291
						Cast ::temp30 ::temp35                                   ;@line 291
					_label90:
						JumpF ::temp30 _label91                                  ;@line 291
						Assign stationReleaseStarted now                         ;@line 292
						FAdd ::temp34 now 5.000000                               ;@line 293
						Assign stationReleaseDeadline ::temp34                   ;@line 293
						Jump _label91                                            ;@line 293
					_label91:
						Cast ::temp30 clockOk                                    ;@line 295
						JumpF ::temp30 _label92                                  ;@line 295
						CompareGTE ::temp35 now stationReleaseStarted            ;@line 295
						Cast ::temp30 ::temp35                                   ;@line 295
					_label92:
						Cast ::temp30 ::temp30                                   ;@line 295
						JumpF ::temp30 _label93                                  ;@line 295
						CompareLTE ::temp35 now stationReleaseDeadline           ;@line 295
						Cast ::temp30 ::temp35                                   ;@line 295
					_label93:
						JumpF ::temp30 _label94                                  ;@line 295
						CallMethod FinishStationCall self ::NoneVar releaseRevision  ;@line 296
						CallMethod ScheduleStationPoll self ::NoneVar            ;@line 297
						Return None                                              ;@line 298
						Jump _label94                                            ;@line 298
					_label94:
						Cast ::temp36 self                                       ;@line 300
						StrCat ::temp36 "AstraAsedioStation effects quiescence timed out ref=" ::temp36  ;@line 300
						StrCat ::temp36 ::temp36 " lease="                       ;@line 300
						Cast ::temp37 lease                                      ;@line 300
						StrCat ::temp37 ::temp36 ::temp37                        ;@line 300
						CallStatic debug Trace ::NoneVar ::temp37 0              ;@line 300
						CallMethod StationCurrent self ::temp35 releaseRevision coordinator lease  ;@line 301
						Not ::temp30 ::temp35                                    ;@line 301
						JumpF ::temp30 _label95                                  ;@line 301
						CallMethod FinishStationCall self ::NoneVar releaseRevision  ;@line 302
						CallMethod ScheduleStationPoll self ::NoneVar            ;@line 303
						Return None                                              ;@line 304
						Jump _label95                                            ;@line 304
					_label95:
						Assign quiet True                                        ;@line 306
						Jump _label86                                            ;@line 306
					_label86:
						CallMethod StationCurrent self ::temp35 releaseRevision coordinator lease  ;@line 308
						Not ::temp30 ::temp35                                    ;@line 308
						Cast ::temp35 ::temp30                                   ;@line 308
						JumpT ::temp35 _label96                                  ;@line 308
						Not ::temp33 quiet                                       ;@line 308
						Cast ::temp35 ::temp33                                   ;@line 308
					_label96:
						JumpF ::temp35 _label97                                  ;@line 308
						CallMethod FinishStationCall self ::NoneVar releaseRevision  ;@line 309
						CallMethod ScheduleStationPoll self ::NoneVar            ;@line 310
						Return None                                              ;@line 311
						Jump _label97                                            ;@line 311
					_label97:
						Assign stationReleaseStarted 0.000000                    ;@line 315
						Assign stationReleaseDeadline 0.000000                   ;@line 316
						Cast ::temp38 None                                       ;@line 317
						CompareEQ ::temp30 coordinator ::temp38                  ;@line 317
						Not ::temp30 ::temp30                                    ;@line 317
						Cast ::temp35 ::temp30                                   ;@line 317
						JumpF ::temp35 _label98                                  ;@line 317
						CompareGT ::temp33 lease 0                               ;@line 317
						Cast ::temp35 ::temp33                                   ;@line 317
					_label98:
						JumpF ::temp35 _label99                                  ;@line 317
						CallMethod ReleasePlayerLease coordinator ::temp30 lease  ;@line 320
						Jump _label99                                            ;@line 320
					_label99:
						CallMethod StationCurrent self ::temp33 releaseRevision coordinator lease  ;@line 322
						JumpF ::temp33 _label100                                 ;@line 322
						Cast ::temp38 None                                       ;@line 323
						Assign stationCoordinator ::temp38                       ;@line 323
						Assign stationLease 0                                    ;@line 324
						Assign stationReleasing False                            ;@line 325
						Jump _label100                                           ;@line 325
					_label100:
						CallMethod FinishStationCall self ::NoneVar releaseRevision  ;@line 327
						CallMethod ScheduleStationPoll self ::NoneVar            ;@line 328
					.endCode
				.endFunction
			.endState
		.endStateTable
	.endObject
.endObjectTable
