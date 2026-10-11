.info
	.source "AstraAsedioActi.psc"
	.modifyTime 1791718973 ;Sun Oct 11 08:42:53 2026 Local
	.compileTime 1791759040 ;Sun Oct 11 19:50:40 2026 Local
	.user "AstraAsedio"
	.computer "Build"
.endInfo
.userFlagsRef
	.flag conditional 1	; 0x00000001
	.flag hidden 0	; 0x00000000
.endUserFlagsRef
.objectTable
	.object AstraAsedioActi ObjectReference
		.userFlags 0	; Flags: 0x00000000
		.docString ""
		.autoState 
		.variableTable
			.variable needsReset Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable timingRevision Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable muzzlePosition Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::ShotSound_var sound
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::YawNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "CTRL_GIRO_360"
			.endVariable
			.variable ::FireSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.200000
			.endVariable
			.variable modeMouse Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1
			.endVariable
			.variable ::UseMouseAim_var Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue True
			.endVariable
			.variable operating Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable rootPosition Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable endingSession Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable firstUpdatePending Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable shotFailure String
				.userFlags 0	; Flags: 0x00000000
				.initialValue ""
			.endVariable
			.variable sightFreezePending Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::ResetSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.800000
			.endVariable
			.variable shotCommitted Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::OperatorNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "OperatorNode"
			.endVariable
			.variable sightThawPending Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::YawSpeed_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 40.000000
			.endVariable
			.variable ::PitchPivotHeight_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 153.000000
			.endVariable
			.variable activateKeyboard Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1
			.endVariable
			.variable ::PitchSign_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1.000000
			.endVariable
			.variable lastTick Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable releaseLeft Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::PitchNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "CTRL_ELEVACION"
			.endVariable
			.variable releaseRight Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable pitch Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::OperatorVerticalTolerance_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 64.000000
			.endVariable
			.variable heldRight Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable nextCombatRetain Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable muzzleWorldMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable heldUp Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::ShotAmmo_var ammo
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable pitchMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::TickSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.050000
			.endVariable
			.variable yaw Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable heldDown Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable matricesReady Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable cameraGraceUntil Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable elapsed Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::QALog_var Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable inputPaused Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue True
			.endVariable
			.variable yawBase Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable heldMode Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable activateMouse Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1
			.endVariable
			.variable rootWorldMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::OperatorHeight_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 119.000000
			.endVariable
			.variable ::PitchMax_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 80.000000
			.endVariable
			.variable ::VisualBoltNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "VIROTE_VISUAL"
			.endVariable
			.variable ::CycleSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 1.000000
			.endVariable
			.variable fireReleaseSerial Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable generation Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable operatorFailure String
				.userFlags 0	; Flags: 0x00000000
				.initialValue ""
			.endVariable
			.variable settleFrames Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable ::YawHalfSector_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 180.000000
			.endVariable
			.variable token Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1
			.endVariable
			.variable demoUntil Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::UseSightCamera_var Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue True
			.endVariable
			.variable ::ContinuousFire_var Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable cameraEntryDeadline Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable heldFire Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue True
			.endVariable
			.variable releaseDown Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::ReleaseSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.066667
			.endVariable
			.variable repeatFire Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable cameraEntryPending Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable releaseUp Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable nativeSightRequested Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable activateReadyAt Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::SteelBolt_var ammo
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::Launcher_var weapon
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable pitchBase Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable fireKeyboard Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1
			.endVariable
			.variable sightFreezeGeneration Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1
			.endVariable
			.variable ::PitchMin_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue -20.000000
			.endVariable
			.variable modeKeyboard Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1
			.endVariable
			.variable player Actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable phase Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable yawMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable heldLeft Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable updating Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable activateBlockedUntil Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable matrixFailure String
				.userFlags 0	; Flags: 0x00000000
				.initialValue ""
			.endVariable
			.variable fireMouse Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1
			.endVariable
			.variable repeatRevision Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable ::YawCenter_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable shotGeneration Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1
			.endVariable
			.variable ::Session_var astraasediosession
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable modeReleaseSerial Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable menuWasOpen Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::OperatorDistance_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 160.000000
			.endVariable
			.variable ::OcupadaGuardia_var globalvariable
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::PitchSpeed_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 20.000000
			.endVariable
			.variable cameraEntryStartedAt Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable retainedCombatTarget Actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
		.endVariableTable
		.propertyTable
			.property UseSightCamera Bool auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::UseSightCamera_var
			.endProperty
			.property YawSpeed Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::YawSpeed_var
			.endProperty
			.property SteelBolt ammo auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::SteelBolt_var
			.endProperty
			.property ResetSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ResetSeconds_var
			.endProperty
			.property PitchPivotHeight Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchPivotHeight_var
			.endProperty
			.property Launcher weapon auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Launcher_var
			.endProperty
			.property OperatorVerticalTolerance Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::OperatorVerticalTolerance_var
			.endProperty
			.property OperatorHeight Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::OperatorHeight_var
			.endProperty
			.property TickSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::TickSeconds_var
			.endProperty
			.property YawHalfSector Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::YawHalfSector_var
			.endProperty
			.property PitchSign Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchSign_var
			.endProperty
			.property OperatorDistance Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::OperatorDistance_var
			.endProperty
			.property ShotSound sound auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ShotSound_var
			.endProperty
			.property YawCenter Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::YawCenter_var
			.endProperty
			.property OcupadaGuardia globalvariable auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::OcupadaGuardia_var
			.endProperty
			.property ContinuousFire Bool auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ContinuousFire_var
			.endProperty
			.property Session astraasediosession auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Session_var
			.endProperty
			.property PitchMax Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchMax_var
			.endProperty
			.property UseMouseAim Bool auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::UseMouseAim_var
			.endProperty
			.property YawNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::YawNode_var
			.endProperty
			.property PitchSpeed Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchSpeed_var
			.endProperty
			.property OperatorNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::OperatorNode_var
			.endProperty
			.property PitchMin Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchMin_var
			.endProperty
			.property VisualBoltNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::VisualBoltNode_var
			.endProperty
			.property QALog Bool auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::QALog_var
			.endProperty
			.property ShotAmmo ammo auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ShotAmmo_var
			.endProperty
			.property CycleSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::CycleSeconds_var
			.endProperty
			.property PitchNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchNode_var
			.endProperty
			.property ReleaseSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ReleaseSeconds_var
			.endProperty
			.property FireSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::FireSeconds_var
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
						.local ::temp163 Bool
						.local ::temp164 Bool
						.local ::temp165 Float
						.local ::temp166 Float
						.local ::NoneVar None
						.local currentGeneration Int
						.local currentPhase Int
						.local currentToken Int
						.local ::temp167 String
						.local ::temp168 String
						.local now Float
						.local dt Float
						.local operationValid Bool
						.local operationMenu Bool
						.local ::temp169 ObjectReference
						.local sightReady Bool
						.local nativeMenuOpen Bool
						.local ::temp170 Int
						.local nativeMode Int
						.local nextContinuous Bool
						.local dtCycle Float
						.local menuAfterAim Bool
						.local ::temp171 Bool
						.local ::temp172 Bool
						.local shotPrepared Bool
						.local ::temp173 Bool
						.local cycleResetStarted Bool
						.local reloadMenuOpen Bool
						.local ::temp174 Bool
					.endLocalTable
					.code
						Not ::temp163 operating                                  ;@line 1305
						Cast ::temp163 ::temp163                                 ;@line 1305
						JumpF ::temp163 _label0                                  ;@line 1305
						Not ::temp164 endingSession                              ;@line 1305
						Cast ::temp163 ::temp164                                 ;@line 1305
					_label0:
						Cast ::temp164 ::temp163                                 ;@line 1305
						JumpF ::temp164 _label1                                  ;@line 1305
						Cast ::temp164 ::OcupadaGuardia_var                      ;@line 1305
					_label1:
						Cast ::temp164 ::temp164                                 ;@line 1305
						JumpF ::temp164 _label2                                  ;@line 1305
						CallMethod GetValue ::OcupadaGuardia_var ::temp165       ;@line 1305
						Cast ::temp166 1                                         ;@line 1305
						CompareEQ ::temp163 ::temp165 ::temp166                  ;@line 1305
						Cast ::temp164 ::temp163                                 ;@line 1305
					_label2:
						Cast ::temp164 ::temp164                                 ;@line 1305
						JumpF ::temp164 _label3                                  ;@line 1305
						CallStatic utility GetCurrentRealTime ::temp166          ;@line 1305
						CompareGTE ::temp163 ::temp166 demoUntil                 ;@line 1305
						Cast ::temp164 ::temp163                                 ;@line 1305
					_label3:
						JumpF ::temp164 _label4                                  ;@line 1305
						Cast ::temp165 0                                         ;@line 1306
						CallMethod SetValue ::OcupadaGuardia_var ::NoneVar ::temp165  ;@line 1306
						Jump _label4                                             ;@line 1306
					_label4:
						Cast ::temp164 updating                                  ;@line 1308
						JumpT ::temp164 _label5                                  ;@line 1308
						Not ::temp163 operating                                  ;@line 1308
						Cast ::temp164 ::temp163                                 ;@line 1308
					_label5:
						JumpF ::temp164 _label6                                  ;@line 1308
						Return None                                              ;@line 1309
						Jump _label6                                             ;@line 1309
					_label6:
						Assign updating True                                     ;@line 1311
						Assign currentGeneration generation                      ;@line 1312
						Assign currentPhase phase                                ;@line 1313
						Assign currentToken token                                ;@line 1314
						JumpF firstUpdatePending _label7                         ;@line 1315
						Assign firstUpdatePending False                          ;@line 1316
						Cast ::temp167 token                                     ;@line 1317
						StrCat ::temp167 "AstraAsedio first OnUpdate token=" ::temp167  ;@line 1317
						StrCat ::temp167 ::temp167 " generation="                ;@line 1317
						Cast ::temp168 generation                                ;@line 1317
						StrCat ::temp168 ::temp167 ::temp168                     ;@line 1317
						StrCat ::temp167 ::temp168 " phase="                     ;@line 1317
						Cast ::temp168 phase                                     ;@line 1317
						StrCat ::temp168 ::temp167 ::temp168                     ;@line 1317
						CallStatic debug Trace ::NoneVar ::temp168 0             ;@line 1317
						Jump _label7                                             ;@line 1317
					_label7:
						CallStatic utility GetCurrentRealTime ::temp166          ;@line 1319
						Assign now ::temp166                                     ;@line 1319
						Not ::temp163 operating                                  ;@line 1321
						Cast ::temp163 ::temp163                                 ;@line 1321
						JumpT ::temp163 _label8                                  ;@line 1321
						CompareEQ ::temp164 generation currentGeneration         ;@line 1321
						Not ::temp164 ::temp164                                  ;@line 1321
						Cast ::temp163 ::temp164                                 ;@line 1321
					_label8:
						Cast ::temp163 ::temp163                                 ;@line 1321
						JumpT ::temp163 _label9                                  ;@line 1321
						CompareEQ ::temp164 token currentToken                   ;@line 1321
						Not ::temp164 ::temp164                                  ;@line 1321
						Cast ::temp163 ::temp164                                 ;@line 1321
					_label9:
						JumpF ::temp163 _label10                                 ;@line 1321
						Assign updating False                                    ;@line 1322
						Cast ::temp164 operating                                 ;@line 1323
						JumpF ::temp164 _label11                                 ;@line 1323
						CompareEQ ::temp164 token currentToken                   ;@line 1323
						Cast ::temp164 ::temp164                                 ;@line 1323
					_label11:
						JumpF ::temp164 _label12                                 ;@line 1323
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSeconds_var  ;@line 1324
						Jump _label12                                            ;@line 1324
					_label12:
						Return None                                              ;@line 1326
						Jump _label10                                            ;@line 1326
					_label10:
						FSubtract ::temp165 now lastTick                         ;@line 1328
						Assign dt ::temp165                                      ;@line 1328
						Assign lastTick now                                      ;@line 1329
						CompareGTE ::temp164 now nextCombatRetain                ;@line 1331
						JumpF ::temp164 _label13                                 ;@line 1331
						FAdd ::temp166 now 1.000000                              ;@line 1332
						Assign nextCombatRetain ::temp166                        ;@line 1332
						CallMethod RetainMountedCombat self ::NoneVar currentGeneration currentToken  ;@line 1333
						Jump _label13                                            ;@line 1333
					_label13:
						JumpF cameraEntryPending _label14                        ;@line 1335
						CallMethod PollFirstPerson self ::temp163 currentGeneration  ;@line 1336
						Not ::temp164 ::temp163                                  ;@line 1336
						JumpF ::temp164 _label15                                 ;@line 1336
						Assign updating False                                    ;@line 1337
						JumpF operating _label16                                 ;@line 1338
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSeconds_var  ;@line 1339
						Jump _label16                                            ;@line 1339
					_label16:
						Return None                                              ;@line 1341
						Jump _label15                                            ;@line 1341
					_label15:
						Assign dt 0.000000                                       ;@line 1343
						Jump _label14                                            ;@line 1343
					_label14:
						CallStatic utility IsInMenuMode ::temp163                ;@line 1345
						JumpF ::temp163 _label17                                 ;@line 1345
						Not ::temp164 inputPaused                                ;@line 1346
						JumpF ::temp164 _label18                                 ;@line 1346
						CallMethod PauseInput self ::NoneVar                     ;@line 1347
						Jump _label18                                            ;@line 1347
					_label18:
						Assign updating False                                    ;@line 1349
						JumpF operating _label19                                 ;@line 1350
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSeconds_var  ;@line 1351
						Jump _label19                                            ;@line 1351
					_label19:
						Return None                                              ;@line 1353
						Jump _label17                                            ;@line 1353
					_label17:
						JumpF menuWasOpen _label20                               ;@line 1355
						CallMethod ResumeInput self ::NoneVar                    ;@line 1356
						Assign dt 0.000000                                       ;@line 1357
						Jump _label20                                            ;@line 1357
					_label20:
						CallMethod CanOperate self ::temp164 currentGeneration   ;@line 1359
						Assign operationValid ::temp164                          ;@line 1359
						CallStatic utility IsInMenuMode ::temp163                ;@line 1360
						Assign operationMenu ::temp163                           ;@line 1360
						Not ::temp164 operating                                  ;@line 1361
						Cast ::temp164 ::temp164                                 ;@line 1361
						JumpT ::temp164 _label21                                 ;@line 1361
						CompareEQ ::temp163 generation currentGeneration         ;@line 1361
						Not ::temp163 ::temp163                                  ;@line 1361
						Cast ::temp164 ::temp163                                 ;@line 1361
					_label21:
						Cast ::temp164 ::temp164                                 ;@line 1361
						JumpT ::temp164 _label22                                 ;@line 1361
						CompareEQ ::temp163 token currentToken                   ;@line 1361
						Not ::temp163 ::temp163                                  ;@line 1361
						Cast ::temp164 ::temp163                                 ;@line 1361
					_label22:
						JumpF ::temp164 _label23                                 ;@line 1361
						Assign updating False                                    ;@line 1362
						Cast ::temp163 operating                                 ;@line 1363
						JumpF ::temp163 _label24                                 ;@line 1363
						CompareEQ ::temp163 token currentToken                   ;@line 1363
						Cast ::temp163 ::temp163                                 ;@line 1363
					_label24:
						JumpF ::temp163 _label25                                 ;@line 1363
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSeconds_var  ;@line 1365
						Jump _label25                                            ;@line 1365
					_label25:
						Return None                                              ;@line 1367
						Jump _label23                                            ;@line 1367
					_label23:
						Cast ::temp163 operationMenu                             ;@line 1369
						JumpT ::temp163 _label26                                 ;@line 1369
						Cast ::temp163 inputPaused                               ;@line 1369
					_label26:
						Cast ::temp164 ::temp163                                 ;@line 1369
						JumpT ::temp164 _label27                                 ;@line 1369
						Cast ::temp164 menuWasOpen                               ;@line 1369
					_label27:
						JumpF ::temp164 _label28                                 ;@line 1369
						Not ::temp163 inputPaused                                ;@line 1370
						JumpF ::temp163 _label29                                 ;@line 1370
						CallMethod PauseInput self ::NoneVar                     ;@line 1371
						Jump _label29                                            ;@line 1371
					_label29:
						Assign updating False                                    ;@line 1373
						JumpF operating _label30                                 ;@line 1374
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSeconds_var  ;@line 1375
						Jump _label30                                            ;@line 1375
					_label30:
						Return None                                              ;@line 1377
						Jump _label28                                            ;@line 1377
					_label28:
						Not ::temp163 operationValid                             ;@line 1379
						JumpF ::temp163 _label31                                 ;@line 1379
						Cast ::temp167 currentGeneration                         ;@line 1380
						StrCat ::temp168 "AstraAsedio operation invalid generation=" ::temp167  ;@line 1380
						StrCat ::temp167 ::temp168 " reason="                    ;@line 1380
						CallMethod SessionFailureReason self ::temp168           ;@line 1380
						StrCat ::temp167 ::temp167 ::temp168                     ;@line 1380
						CallStatic debug Trace ::NoneVar ::temp167 0             ;@line 1380
						JumpF ::UseSightCamera_var _label32                      ;@line 1381
						CallMethod RejectShot self ::NoneVar "NATIVE_SIGHT_OPERATION_INVALID: se perdiÃ³ la mira o su contexto."  ;@line 1382
						Jump _label32                                            ;@line 1382
					_label32:
						Assign updating False                                    ;@line 1384
						CallMethod EndSession self ::NoneVar                     ;@line 1385
						Return None                                              ;@line 1386
						Jump _label31                                            ;@line 1386
					_label31:
						JumpF ::UseSightCamera_var _label33                      ;@line 1388
						Cast ::temp169 self                                      ;@line 1389
						CallStatic astrasightnative IsFastSightReady ::temp164 ::temp169 currentToken  ;@line 1389
						Assign sightReady ::temp164                              ;@line 1389
						CallStatic utility IsInMenuMode ::temp163                ;@line 1390
						Assign nativeMenuOpen ::temp163                          ;@line 1390
						Not ::temp164 operating                                  ;@line 1391
						Cast ::temp164 ::temp164                                 ;@line 1391
						JumpT ::temp164 _label34                                 ;@line 1391
						CompareEQ ::temp163 generation currentGeneration         ;@line 1391
						Not ::temp163 ::temp163                                  ;@line 1391
						Cast ::temp164 ::temp163                                 ;@line 1391
					_label34:
						Cast ::temp164 ::temp164                                 ;@line 1391
						JumpT ::temp164 _label35                                 ;@line 1391
						CompareEQ ::temp163 token currentToken                   ;@line 1391
						Not ::temp163 ::temp163                                  ;@line 1391
						Cast ::temp164 ::temp163                                 ;@line 1391
					_label35:
						JumpF ::temp164 _label36                                 ;@line 1391
						Assign updating False                                    ;@line 1392
						Cast ::temp163 operating                                 ;@line 1393
						JumpF ::temp163 _label37                                 ;@line 1393
						CompareEQ ::temp163 token currentToken                   ;@line 1393
						Cast ::temp163 ::temp163                                 ;@line 1393
					_label37:
						JumpF ::temp163 _label38                                 ;@line 1393
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSeconds_var  ;@line 1395
						Jump _label38                                            ;@line 1395
					_label38:
						Return None                                              ;@line 1397
						Jump _label36                                            ;@line 1397
					_label36:
						Cast ::temp163 nativeMenuOpen                            ;@line 1399
						JumpT ::temp163 _label39                                 ;@line 1399
						Cast ::temp163 inputPaused                               ;@line 1399
					_label39:
						Cast ::temp164 ::temp163                                 ;@line 1399
						JumpT ::temp164 _label40                                 ;@line 1399
						Cast ::temp164 menuWasOpen                               ;@line 1399
					_label40:
						JumpF ::temp164 _label41                                 ;@line 1399
						Not ::temp163 inputPaused                                ;@line 1400
						JumpF ::temp163 _label42                                 ;@line 1400
						CallMethod PauseInput self ::NoneVar                     ;@line 1401
						Jump _label42                                            ;@line 1401
					_label42:
						Assign updating False                                    ;@line 1403
						JumpF operating _label43                                 ;@line 1404
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSeconds_var  ;@line 1405
						Jump _label43                                            ;@line 1405
					_label43:
						Return None                                              ;@line 1407
						Jump _label41                                            ;@line 1407
					_label41:
						Not ::temp163 sightReady                                 ;@line 1409
						JumpF ::temp163 _label44                                 ;@line 1409
						CallMethod RejectShot self ::NoneVar "NATIVE_SIGHT_NOT_READY: se perdiÃ³ la mira nativa."  ;@line 1410
						Assign updating False                                    ;@line 1411
						CallMethod EndSession self ::NoneVar                     ;@line 1412
						Return None                                              ;@line 1413
						Jump _label44                                            ;@line 1413
					_label44:
						Jump _label33                                            ;@line 1413
					_label33:
						JumpF ::UseSightCamera_var _label45                      ;@line 1416
						CallMethod UpdateAim self ::NoneVar dt                   ;@line 1419
						Cast ::temp169 self                                      ;@line 1420
						CallStatic astrasightnative GetFireMode ::temp170 ::temp169 currentToken  ;@line 1420
						Assign nativeMode ::temp170                              ;@line 1420
						Cast ::temp163 operating                                 ;@line 1421
						JumpF ::temp163 _label46                                 ;@line 1421
						CompareEQ ::temp164 generation currentGeneration         ;@line 1421
						Cast ::temp163 ::temp164                                 ;@line 1421
					_label46:
						Cast ::temp163 ::temp163                                 ;@line 1421
						JumpF ::temp163 _label47                                 ;@line 1421
						CompareEQ ::temp164 token currentToken                   ;@line 1421
						Cast ::temp163 ::temp164                                 ;@line 1421
					_label47:
						Cast ::temp163 ::temp163                                 ;@line 1421
						JumpF ::temp163 _label48                                 ;@line 1421
						CompareGTE ::temp164 nativeMode 0                        ;@line 1421
						Cast ::temp163 ::temp164                                 ;@line 1421
					_label48:
						JumpF ::temp163 _label49                                 ;@line 1421
						CompareEQ ::temp164 nativeMode 1                         ;@line 1422
						Assign nextContinuous ::temp164                          ;@line 1422
						CompareEQ ::temp164 ::ContinuousFire_var nextContinuous  ;@line 1423
						Not ::temp164 ::temp164                                  ;@line 1423
						JumpF ::temp164 _label50                                 ;@line 1423
						Assign ::ContinuousFire_var nextContinuous               ;@line 1424
						JumpF ::ContinuousFire_var _label51                      ;@line 1425
						CallStatic debug Notification ::NoneVar "Astra: tiro continuo. MantÃ©n Ataque; Sprint cambia el modo."  ;@line 1426
						Jump _label52                                            ;@line 1426
					_label51:
						CallStatic debug Notification ::NoneVar "Astra: tiro individual. Sprint cambia el modo."  ;@line 1428
					_label52:
						Jump _label50                                            ;@line 1428
					_label50:
						Jump _label49                                            ;@line 1428
					_label49:
						Assign updating False                                    ;@line 1432
						Cast ::temp163 operating                                 ;@line 1433
						JumpF ::temp163 _label53                                 ;@line 1433
						CompareEQ ::temp164 token currentToken                   ;@line 1433
						Cast ::temp163 ::temp164                                 ;@line 1433
					_label53:
						JumpF ::temp163 _label54                                 ;@line 1433
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSeconds_var  ;@line 1434
						Jump _label54                                            ;@line 1434
					_label54:
						Return None                                              ;@line 1436
						Jump _label45                                            ;@line 1436
					_label45:
						Assign dtCycle dt                                        ;@line 1438
						CompareLT ::temp164 dtCycle 0.000000                     ;@line 1439
						JumpF ::temp164 _label55                                 ;@line 1439
						Assign dtCycle 0.000000                                  ;@line 1440
						Jump _label55                                            ;@line 1440
					_label55:
						CompareGT ::temp163 dt 0.150000                          ;@line 1442
						JumpF ::temp163 _label56                                 ;@line 1442
						Assign dt 0.150000                                       ;@line 1443
						Jump _label57                                            ;@line 1443
					_label56:
						CompareLT ::temp164 dt 0.000000                          ;@line 1444
						JumpF ::temp164 _label57                                 ;@line 1444
						Assign dt 0.000000                                       ;@line 1445
						Jump _label57                                            ;@line 1445
					_label57:
						CompareEQ ::temp164 phase 0                              ;@line 1448
						Cast ::temp163 ::temp164                                 ;@line 1448
						JumpT ::temp163 _label58                                 ;@line 1448
						Cast ::temp163 shotCommitted                             ;@line 1448
					_label58:
						Cast ::temp163 ::temp163                                 ;@line 1448
						JumpT ::temp163 _label59                                 ;@line 1448
						CompareEQ ::temp164 phase 3                              ;@line 1448
						Cast ::temp163 ::temp164                                 ;@line 1448
					_label59:
						JumpF ::temp163 _label60                                 ;@line 1448
						CallMethod UpdateAim self ::NoneVar dt                   ;@line 1449
						Jump _label60                                            ;@line 1449
					_label60:
						CallStatic utility IsInMenuMode ::temp164                ;@line 1453
						Assign menuAfterAim ::temp164                            ;@line 1453
						Not ::temp163 operating                                  ;@line 1454
						Cast ::temp163 ::temp163                                 ;@line 1454
						JumpT ::temp163 _label61                                 ;@line 1454
						CompareEQ ::temp164 generation currentGeneration         ;@line 1454
						Not ::temp164 ::temp164                                  ;@line 1454
						Cast ::temp163 ::temp164                                 ;@line 1454
					_label61:
						Cast ::temp163 ::temp163                                 ;@line 1454
						JumpT ::temp163 _label62                                 ;@line 1454
						CompareEQ ::temp164 phase currentPhase                   ;@line 1454
						Not ::temp164 ::temp164                                  ;@line 1454
						Cast ::temp163 ::temp164                                 ;@line 1454
					_label62:
						Cast ::temp164 ::temp163                                 ;@line 1454
						JumpT ::temp164 _label63                                 ;@line 1454
						Cast ::temp164 inputPaused                               ;@line 1454
					_label63:
						Cast ::temp163 ::temp164                                 ;@line 1454
						JumpT ::temp163 _label64                                 ;@line 1454
						Cast ::temp163 menuWasOpen                               ;@line 1454
					_label64:
						Cast ::temp164 ::temp163                                 ;@line 1454
						JumpT ::temp164 _label65                                 ;@line 1454
						Cast ::temp164 menuAfterAim                              ;@line 1454
					_label65:
						JumpF ::temp164 _label66                                 ;@line 1454
						Cast ::temp163 operating                                 ;@line 1455
						JumpF ::temp163 _label67                                 ;@line 1455
						CompareEQ ::temp163 generation currentGeneration         ;@line 1455
						Cast ::temp163 ::temp163                                 ;@line 1455
					_label67:
						Cast ::temp163 ::temp163                                 ;@line 1455
						JumpF ::temp163 _label68                                 ;@line 1455
						Cast ::temp163 menuAfterAim                              ;@line 1455
					_label68:
						Cast ::temp163 ::temp163                                 ;@line 1455
						JumpF ::temp163 _label69                                 ;@line 1455
						Not ::temp171 inputPaused                                ;@line 1455
						Cast ::temp163 ::temp171                                 ;@line 1455
					_label69:
						JumpF ::temp163 _label70                                 ;@line 1455
						CallMethod PauseInput self ::NoneVar                     ;@line 1456
						Jump _label70                                            ;@line 1456
					_label70:
						Assign updating False                                    ;@line 1458
						JumpF operating _label71                                 ;@line 1459
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSeconds_var  ;@line 1460
						Jump _label71                                            ;@line 1460
					_label71:
						Return None                                              ;@line 1462
						Jump _label66                                            ;@line 1462
					_label66:
						CompareEQ ::temp171 phase 1                              ;@line 1464
						Cast ::temp164 ::temp171                                 ;@line 1464
						JumpF ::temp164 _label72                                 ;@line 1464
						Not ::temp163 sightFreezePending                         ;@line 1464
						Cast ::temp164 ::temp163                                 ;@line 1464
					_label72:
						Cast ::temp163 ::temp164                                 ;@line 1464
						JumpF ::temp163 _label73                                 ;@line 1464
						Not ::temp171 sightThawPending                           ;@line 1464
						Cast ::temp163 ::temp171                                 ;@line 1464
					_label73:
						JumpF ::temp163 _label74                                 ;@line 1464
						IAdd ::temp170 settleFrames 1                            ;@line 1467
						Assign settleFrames ::temp170                            ;@line 1467
						Cast ::temp171 ::UseSightCamera_var                      ;@line 1468
						JumpT ::temp171 _label75                                 ;@line 1468
						CompareGTE ::temp164 settleFrames 3                      ;@line 1468
						Cast ::temp171 ::temp164                                 ;@line 1468
					_label75:
						JumpF ::temp171 _label76                                 ;@line 1468
						CallMethod PrepareShotAnimation self ::temp164 shotGeneration  ;@line 1469
						Assign shotPrepared ::temp164                            ;@line 1469
						Not ::temp164 operating                                  ;@line 1470
						Cast ::temp164 ::temp164                                 ;@line 1470
						JumpT ::temp164 _label77                                 ;@line 1470
						CompareEQ ::temp172 generation currentGeneration         ;@line 1470
						Not ::temp172 ::temp172                                  ;@line 1470
						Cast ::temp164 ::temp172                                 ;@line 1470
					_label77:
						Cast ::temp164 ::temp164                                 ;@line 1470
						JumpT ::temp164 _label78                                 ;@line 1470
						CompareEQ ::temp172 token currentToken                   ;@line 1470
						Not ::temp172 ::temp172                                  ;@line 1470
						Cast ::temp164 ::temp172                                 ;@line 1470
					_label78:
						Cast ::temp164 ::temp164                                 ;@line 1470
						JumpT ::temp164 _label79                                 ;@line 1470
						CompareEQ ::temp172 phase 1                              ;@line 1470
						Not ::temp172 ::temp172                                  ;@line 1470
						Cast ::temp164 ::temp172                                 ;@line 1470
					_label79:
						Cast ::temp172 ::temp164                                 ;@line 1470
						JumpT ::temp172 _label80                                 ;@line 1470
						Cast ::temp172 inputPaused                               ;@line 1470
					_label80:
						Cast ::temp164 ::temp172                                 ;@line 1470
						JumpT ::temp164 _label81                                 ;@line 1470
						Cast ::temp164 menuWasOpen                               ;@line 1470
					_label81:
						JumpF ::temp164 _label82                                 ;@line 1470
						Assign updating False                                    ;@line 1471
						JumpF operating _label83                                 ;@line 1472
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSeconds_var  ;@line 1473
						Jump _label83                                            ;@line 1473
					_label83:
						Return None                                              ;@line 1475
						Jump _label82                                            ;@line 1475
					_label82:
						JumpF shotPrepared _label84                              ;@line 1477
						Assign phase 2                                           ;@line 1478
						Assign elapsed 0.000000                                  ;@line 1479
						JumpF ::QALog_var _label85                               ;@line 1480
						Cast ::temp168 generation                                ;@line 1481
						StrCat ::temp167 "AstraAsedio phase Fire generation=" ::temp168  ;@line 1481
						CallStatic debug Trace ::NoneVar ::temp167 0             ;@line 1481
						Jump _label85                                            ;@line 1481
					_label85:
						Jump _label86                                            ;@line 1481
					_label84:
						CallMethod StopRepeatFire self ::NoneVar                 ;@line 1484
						CallMethod RejectShot self ::NoneVar shotFailure         ;@line 1485
						CallMethod ThawSight self ::NoneVar currentGeneration currentToken  ;@line 1486
						Not ::temp172 operating                                  ;@line 1487
						Cast ::temp172 ::temp172                                 ;@line 1487
						JumpT ::temp172 _label87                                 ;@line 1487
						CompareEQ ::temp164 generation currentGeneration         ;@line 1487
						Not ::temp164 ::temp164                                  ;@line 1487
						Cast ::temp172 ::temp164                                 ;@line 1487
					_label87:
						Cast ::temp172 ::temp172                                 ;@line 1487
						JumpT ::temp172 _label88                                 ;@line 1487
						CompareEQ ::temp164 token currentToken                   ;@line 1487
						Not ::temp164 ::temp164                                  ;@line 1487
						Cast ::temp172 ::temp164                                 ;@line 1487
					_label88:
						Cast ::temp172 ::temp172                                 ;@line 1487
						JumpT ::temp172 _label89                                 ;@line 1487
						CompareEQ ::temp164 phase 1                              ;@line 1487
						Not ::temp164 ::temp164                                  ;@line 1487
						Cast ::temp172 ::temp164                                 ;@line 1487
					_label89:
						JumpF ::temp172 _label90                                 ;@line 1487
						Assign updating False                                    ;@line 1488
						Cast ::temp164 operating                                 ;@line 1489
						JumpF ::temp164 _label91                                 ;@line 1489
						CompareEQ ::temp164 token currentToken                   ;@line 1489
						Cast ::temp164 ::temp164                                 ;@line 1489
					_label91:
						JumpF ::temp164 _label92                                 ;@line 1489
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSeconds_var  ;@line 1490
						Jump _label92                                            ;@line 1490
					_label92:
						Return None                                              ;@line 1492
						Jump _label90                                            ;@line 1492
					_label90:
						Assign phase 0                                           ;@line 1494
						Assign needsReset False                                  ;@line 1495
					_label86:
						Jump _label76                                            ;@line 1495
					_label76:
						Jump _label93                                            ;@line 1495
					_label74:
						CompareEQ ::temp164 phase 2                              ;@line 1498
						JumpF ::temp164 _label94                                 ;@line 1498
						FAdd ::temp165 elapsed dtCycle                           ;@line 1499
						Assign elapsed ::temp165                                 ;@line 1499
						CompareGTE ::temp172 elapsed ::ReleaseSeconds_var        ;@line 1500
						Cast ::temp172 ::temp172                                 ;@line 1500
						JumpF ::temp172 _label95                                 ;@line 1500
						Not ::temp171 shotCommitted                              ;@line 1500
						Cast ::temp172 ::temp171                                 ;@line 1500
					_label95:
						JumpF ::temp172 _label96                                 ;@line 1500
						CallMethod CommitShot self ::NoneVar shotGeneration      ;@line 1501
						Not ::temp171 operating                                  ;@line 1502
						Cast ::temp171 ::temp171                                 ;@line 1502
						JumpT ::temp171 _label97                                 ;@line 1502
						CompareEQ ::temp173 generation currentGeneration         ;@line 1502
						Not ::temp173 ::temp173                                  ;@line 1502
						Cast ::temp171 ::temp173                                 ;@line 1502
					_label97:
						JumpF ::temp171 _label98                                 ;@line 1502
						Assign updating False                                    ;@line 1503
						Cast ::temp173 operating                                 ;@line 1504
						JumpF ::temp173 _label99                                 ;@line 1504
						CompareEQ ::temp173 token currentToken                   ;@line 1504
						Cast ::temp173 ::temp173                                 ;@line 1504
					_label99:
						JumpF ::temp173 _label100                                ;@line 1504
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSeconds_var  ;@line 1505
						Jump _label100                                           ;@line 1505
					_label100:
						Return None                                              ;@line 1507
						Jump _label98                                            ;@line 1507
					_label98:
						Jump _label96                                            ;@line 1507
					_label96:
						CompareGTE ::temp173 elapsed ::FireSeconds_var           ;@line 1510
						JumpF ::temp173 _label101                                ;@line 1510
						Not ::temp171 operating                                  ;@line 1511
						Cast ::temp171 ::temp171                                 ;@line 1511
						JumpT ::temp171 _label102                                ;@line 1511
						CompareEQ ::temp172 generation currentGeneration         ;@line 1511
						Not ::temp172 ::temp172                                  ;@line 1511
						Cast ::temp171 ::temp172                                 ;@line 1511
					_label102:
						Cast ::temp171 ::temp171                                 ;@line 1511
						JumpT ::temp171 _label103                                ;@line 1511
						CompareEQ ::temp172 token currentToken                   ;@line 1511
						Not ::temp172 ::temp172                                  ;@line 1511
						Cast ::temp171 ::temp172                                 ;@line 1511
					_label103:
						Cast ::temp171 ::temp171                                 ;@line 1511
						JumpT ::temp171 _label104                                ;@line 1511
						CompareEQ ::temp172 phase 2                              ;@line 1511
						Not ::temp172 ::temp172                                  ;@line 1511
						Cast ::temp171 ::temp172                                 ;@line 1511
					_label104:
						Cast ::temp172 ::temp171                                 ;@line 1511
						JumpT ::temp172 _label105                                ;@line 1511
						Cast ::temp172 inputPaused                               ;@line 1511
					_label105:
						Cast ::temp171 ::temp172                                 ;@line 1511
						JumpT ::temp171 _label106                                ;@line 1511
						Cast ::temp171 menuWasOpen                               ;@line 1511
					_label106:
						JumpF ::temp171 _label107                                ;@line 1511
						Assign updating False                                    ;@line 1512
						Cast ::temp172 operating                                 ;@line 1513
						JumpF ::temp172 _label108                                ;@line 1513
						CompareEQ ::temp172 token currentToken                   ;@line 1513
						Cast ::temp172 ::temp172                                 ;@line 1513
					_label108:
						JumpF ::temp172 _label109                                ;@line 1513
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSeconds_var  ;@line 1514
						Jump _label109                                           ;@line 1514
					_label109:
						Return None                                              ;@line 1516
						Jump _label107                                           ;@line 1516
					_label107:
						CallMethod PlayGamebryoAnimation self ::temp172 "Reset" True 0.000000  ;@line 1518
						Assign cycleResetStarted ::temp172                       ;@line 1518
						Not ::temp171 operating                                  ;@line 1521
						Cast ::temp171 ::temp171                                 ;@line 1521
						JumpT ::temp171 _label110                                ;@line 1521
						CompareEQ ::temp172 generation currentGeneration         ;@line 1521
						Not ::temp172 ::temp172                                  ;@line 1521
						Cast ::temp171 ::temp172                                 ;@line 1521
					_label110:
						Cast ::temp171 ::temp171                                 ;@line 1521
						JumpT ::temp171 _label111                                ;@line 1521
						CompareEQ ::temp172 token currentToken                   ;@line 1521
						Not ::temp172 ::temp172                                  ;@line 1521
						Cast ::temp171 ::temp172                                 ;@line 1521
					_label111:
						Cast ::temp171 ::temp171                                 ;@line 1521
						JumpT ::temp171 _label112                                ;@line 1521
						CompareEQ ::temp172 phase 2                              ;@line 1521
						Not ::temp172 ::temp172                                  ;@line 1521
						Cast ::temp171 ::temp172                                 ;@line 1521
					_label112:
						Cast ::temp172 ::temp171                                 ;@line 1521
						JumpT ::temp172 _label113                                ;@line 1521
						Cast ::temp172 inputPaused                               ;@line 1521
					_label113:
						Cast ::temp171 ::temp172                                 ;@line 1521
						JumpT ::temp171 _label114                                ;@line 1521
						Cast ::temp171 menuWasOpen                               ;@line 1521
					_label114:
						JumpF ::temp171 _label115                                ;@line 1521
						Assign updating False                                    ;@line 1522
						Cast ::temp172 operating                                 ;@line 1523
						JumpF ::temp172 _label116                                ;@line 1523
						CompareEQ ::temp172 token currentToken                   ;@line 1523
						Cast ::temp172 ::temp172                                 ;@line 1523
					_label116:
						JumpF ::temp172 _label117                                ;@line 1523
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSeconds_var  ;@line 1524
						Jump _label117                                           ;@line 1524
					_label117:
						Return None                                              ;@line 1526
						Jump _label115                                           ;@line 1526
					_label115:
						JumpF cycleResetStarted _label118                        ;@line 1528
						Assign phase 3                                           ;@line 1529
						Assign elapsed 0.000000                                  ;@line 1530
						Jump _label119                                           ;@line 1530
					_label118:
						CallMethod RejectShot self ::NoneVar "RESET_ANIMATION_FAILED: fin del disparo."  ;@line 1532
						Assign updating False                                    ;@line 1533
						CallMethod EndSession self ::NoneVar                     ;@line 1534
						Return None                                              ;@line 1535
					_label119:
						Jump _label101                                           ;@line 1535
					_label101:
						Jump _label93                                            ;@line 1535
					_label94:
						CompareEQ ::temp172 phase 3                              ;@line 1538
						JumpF ::temp172 _label93                                 ;@line 1538
						FAdd ::temp166 elapsed dtCycle                           ;@line 1539
						Assign elapsed ::temp166                                 ;@line 1539
						CompareGTE ::temp171 elapsed ::ResetSeconds_var          ;@line 1540
						Cast ::temp164 ::temp171                                 ;@line 1540
						JumpF ::temp164 _label120                                ;@line 1540
						FSubtract ::temp165 ::CycleSeconds_var ::FireSeconds_var  ;@line 1540
						CompareGTE ::temp173 elapsed ::temp165                   ;@line 1540
						Cast ::temp164 ::temp173                                 ;@line 1540
					_label120:
						JumpF ::temp164 _label121                                ;@line 1540
						Cast ::temp169 self                                      ;@line 1541
						CallStatic netimmerse SetNodeScale ::NoneVar ::temp169 ::VisualBoltNode_var 1.000000 False  ;@line 1541
						CallStatic utility IsInMenuMode ::temp171                ;@line 1542
						Assign reloadMenuOpen ::temp171                          ;@line 1542
						Not ::temp173 operating                                  ;@line 1545
						Cast ::temp173 ::temp173                                 ;@line 1545
						JumpT ::temp173 _label122                                ;@line 1545
						CompareEQ ::temp171 generation currentGeneration         ;@line 1545
						Not ::temp171 ::temp171                                  ;@line 1545
						Cast ::temp173 ::temp171                                 ;@line 1545
					_label122:
						Cast ::temp173 ::temp173                                 ;@line 1545
						JumpT ::temp173 _label123                                ;@line 1545
						CompareEQ ::temp171 token currentToken                   ;@line 1545
						Not ::temp171 ::temp171                                  ;@line 1545
						Cast ::temp173 ::temp171                                 ;@line 1545
					_label123:
						Cast ::temp173 ::temp173                                 ;@line 1545
						JumpT ::temp173 _label124                                ;@line 1545
						CompareEQ ::temp171 phase 3                              ;@line 1545
						Not ::temp171 ::temp171                                  ;@line 1545
						Cast ::temp173 ::temp171                                 ;@line 1545
					_label124:
						Cast ::temp171 ::temp173                                 ;@line 1545
						JumpT ::temp171 _label125                                ;@line 1545
						Cast ::temp171 inputPaused                               ;@line 1545
					_label125:
						Cast ::temp173 ::temp171                                 ;@line 1545
						JumpT ::temp173 _label126                                ;@line 1545
						Cast ::temp173 menuWasOpen                               ;@line 1545
					_label126:
						Cast ::temp171 ::temp173                                 ;@line 1545
						JumpT ::temp171 _label127                                ;@line 1545
						Cast ::temp171 reloadMenuOpen                            ;@line 1545
					_label127:
						JumpF ::temp171 _label128                                ;@line 1545
						Cast ::temp173 operating                                 ;@line 1546
						JumpF ::temp173 _label129                                ;@line 1546
						CompareEQ ::temp173 generation currentGeneration         ;@line 1546
						Cast ::temp173 ::temp173                                 ;@line 1546
					_label129:
						Cast ::temp173 ::temp173                                 ;@line 1546
						JumpF ::temp173 _label130                                ;@line 1546
						CompareEQ ::temp174 token currentToken                   ;@line 1546
						Cast ::temp173 ::temp174                                 ;@line 1546
					_label130:
						Cast ::temp174 ::temp173                                 ;@line 1546
						JumpF ::temp174 _label131                                ;@line 1546
						Cast ::temp174 reloadMenuOpen                            ;@line 1546
					_label131:
						Cast ::temp174 ::temp174                                 ;@line 1546
						JumpF ::temp174 _label132                                ;@line 1546
						Not ::temp173 inputPaused                                ;@line 1546
						Cast ::temp174 ::temp173                                 ;@line 1546
					_label132:
						JumpF ::temp174 _label133                                ;@line 1546
						CallMethod PauseInput self ::NoneVar                     ;@line 1547
						Jump _label133                                           ;@line 1547
					_label133:
						Assign updating False                                    ;@line 1549
						Cast ::temp174 operating                                 ;@line 1550
						JumpF ::temp174 _label134                                ;@line 1550
						CompareEQ ::temp173 token currentToken                   ;@line 1550
						Cast ::temp174 ::temp173                                 ;@line 1550
					_label134:
						JumpF ::temp174 _label135                                ;@line 1550
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSeconds_var  ;@line 1551
						Jump _label135                                           ;@line 1551
					_label135:
						Return None                                              ;@line 1553
						Jump _label128                                           ;@line 1553
					_label128:
						Assign phase 0                                           ;@line 1555
						Assign needsReset False                                  ;@line 1556
						Assign shotCommitted False                               ;@line 1557
						CallMethod TryRepeatShot self ::NoneVar currentGeneration  ;@line 1558
						Jump _label121                                           ;@line 1558
					_label121:
						Jump _label93                                            ;@line 1558
					_label93:
						Assign updating False                                    ;@line 1561
						JumpF operating _label136                                ;@line 1562
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSeconds_var  ;@line 1563
						Jump _label136                                           ;@line 1563
					_label136:
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
						.local ::temp15 String
						.local ::temp16 String
						.local ::NoneVar None
						.local ::temp17 Bool
						.local ::temp18 Bool
						.local ::temp19 Actor
						.local ::temp20 ObjectReference
						.local ::temp21 Float
						.local ::temp22 Int
						.local ::temp23 astraasediosession
						.local ::temp24 weapon
						.local ::temp25 ammo
						.local activationGeneration Int
						.local activationToken Int
						.local actionIsPlayer Bool
						.local activationTime Float
						.local nativeVersion Int
						.local nativeAPI Int
						.local activationCamera Int
						.local combatAtEntry Actor
						.local acquiredToken Int
						.local entryGeneration Int
						.local entryToken Int
						.local aligned Bool
						.local ::temp26 Bool
						.local entryResetStarted Bool
					.endLocalTable
					.code
						Assign activationGeneration generation                   ;@line 224
						Assign activationToken token                             ;@line 225
						Cast ::temp15 self                                       ;@line 226
						StrCat ::temp15 "AstraAsedio OnActivate ref=" ::temp15   ;@line 226
						StrCat ::temp15 ::temp15 " actor="                       ;@line 226
						Cast ::temp16 akActionRef                                ;@line 226
						StrCat ::temp16 ::temp15 ::temp16                        ;@line 226
						CallStatic debug Trace ::NoneVar ::temp16 0              ;@line 226
						CompareEQ ::temp17 generation activationGeneration       ;@line 227
						Not ::temp17 ::temp17                                    ;@line 227
						Cast ::temp17 ::temp17                                   ;@line 227
						JumpT ::temp17 _label137                                 ;@line 227
						CompareEQ ::temp18 token activationToken                 ;@line 227
						Not ::temp18 ::temp18                                    ;@line 227
						Cast ::temp17 ::temp18                                   ;@line 227
					_label137:
						JumpF ::temp17 _label138                                 ;@line 227
						Return None                                              ;@line 228
						Jump _label138                                           ;@line 228
					_label138:
						CallStatic game GetPlayer ::temp19                       ;@line 230
						Cast ::temp20 ::temp19                                   ;@line 230
						CompareEQ ::temp18 akActionRef ::temp20                  ;@line 230
						Assign actionIsPlayer ::temp18                           ;@line 230
						CompareEQ ::temp17 generation activationGeneration       ;@line 231
						Not ::temp17 ::temp17                                    ;@line 231
						Cast ::temp17 ::temp17                                   ;@line 231
						JumpT ::temp17 _label139                                 ;@line 231
						CompareEQ ::temp18 token activationToken                 ;@line 231
						Not ::temp18 ::temp18                                    ;@line 231
						Cast ::temp17 ::temp18                                   ;@line 231
					_label139:
						JumpF ::temp17 _label140                                 ;@line 231
						Return None                                              ;@line 232
						Jump _label140                                           ;@line 232
					_label140:
						Not ::temp18 actionIsPlayer                              ;@line 234
						JumpF ::temp18 _label141                                 ;@line 234
						CallMethod RejectActivation self ::NoneVar "ACTOR_NOT_PLAYER: solo el jugador puede manejarla."  ;@line 235
						Return None                                              ;@line 236
						Jump _label141                                           ;@line 236
					_label141:
						CallStatic utility GetCurrentRealTime ::temp21           ;@line 239
						CompareLT ::temp17 ::temp21 demoUntil                    ;@line 239
						JumpF ::temp17 _label142                                 ;@line 239
						Return None                                              ;@line 240
						Jump _label142                                           ;@line 240
					_label142:
						CallStatic game GetPlayer ::temp19                       ;@line 243
						CallMethod IsSneaking ::temp19 ::temp18                  ;@line 243
						JumpF ::temp18 _label143                                 ;@line 243
						CallStatic utility GetCurrentRealTime ::temp21           ;@line 244
						FAdd ::temp21 ::temp21 24.000000                         ;@line 244
						Assign demoUntil ::temp21                                ;@line 244
						CallMethod PlayGuardiaDemo self ::NoneVar                ;@line 245
						Return None                                              ;@line 246
						Jump _label143                                           ;@line 246
					_label143:
						JumpF endingSession _label144                            ;@line 248
						Return None                                              ;@line 249
						Jump _label144                                           ;@line 249
					_label144:
						JumpF operating _label145                                ;@line 251
						CallMethod RequestExit self ::NoneVar "OnActivate"       ;@line 252
						Return None                                              ;@line 253
						Jump _label145                                           ;@line 253
					_label145:
						CallStatic utility GetCurrentRealTime ::temp21           ;@line 257
						Assign activationTime ::temp21                           ;@line 257
						Cast ::temp17 operating                                  ;@line 258
						JumpT ::temp17 _label146                                 ;@line 258
						Cast ::temp17 endingSession                              ;@line 258
					_label146:
						Cast ::temp17 ::temp17                                   ;@line 258
						JumpT ::temp17 _label147                                 ;@line 258
						CompareEQ ::temp18 generation activationGeneration       ;@line 258
						Not ::temp18 ::temp18                                    ;@line 258
						Cast ::temp17 ::temp18                                   ;@line 258
					_label147:
						Cast ::temp17 ::temp17                                   ;@line 258
						JumpT ::temp17 _label148                                 ;@line 258
						CompareEQ ::temp18 token activationToken                 ;@line 258
						Not ::temp18 ::temp18                                    ;@line 258
						Cast ::temp17 ::temp18                                   ;@line 258
					_label148:
						JumpF ::temp17 _label149                                 ;@line 258
						Return None                                              ;@line 259
						Jump _label149                                           ;@line 259
					_label149:
						CompareLT ::temp18 activationTime activateBlockedUntil   ;@line 261
						JumpF ::temp18 _label150                                 ;@line 261
						Return None                                              ;@line 262
						Jump _label150                                           ;@line 262
					_label150:
						CallStatic game GetPlayer ::temp19                       ;@line 264
						Assign player ::temp19                                   ;@line 264
						CallStatic skse GetVersion ::temp22                      ;@line 265
						CompareLT ::temp17 ::temp22 2                            ;@line 265
						JumpF ::temp17 _label151                                 ;@line 265
						CallMethod RejectActivation self ::NoneVar "SKSE_MISSING: inicia Skyrim con SKSE64."  ;@line 266
						Return None                                              ;@line 267
						Jump _label151                                           ;@line 267
					_label151:
						CallStatic skse GetPluginVersion ::temp22 "AstraSight"   ;@line 270
						Assign nativeVersion ::temp22                            ;@line 270
						Cast ::temp18 operating                                  ;@line 271
						JumpT ::temp18 _label152                                 ;@line 271
						Cast ::temp18 endingSession                              ;@line 271
					_label152:
						Cast ::temp18 ::temp18                                   ;@line 271
						JumpT ::temp18 _label153                                 ;@line 271
						CompareEQ ::temp17 generation activationGeneration       ;@line 271
						Not ::temp17 ::temp17                                    ;@line 271
						Cast ::temp18 ::temp17                                   ;@line 271
					_label153:
						JumpF ::temp18 _label154                                 ;@line 271
						Return None                                              ;@line 272
						Jump _label154                                           ;@line 272
					_label154:
						CompareLT ::temp17 nativeVersion 50659328                ;@line 274
						JumpF ::temp17 _label155                                 ;@line 274
						CallMethod RejectActivation self ::NoneVar "NATIVE_SIGHT_MISSING: instala AstraSight.dll 3.5.0 de esta versiÃ³n."  ;@line 275
						Return None                                              ;@line 276
						Jump _label155                                           ;@line 276
					_label155:
						CallStatic astrasightnative GetAPIVersion ::temp22       ;@line 278
						Assign nativeAPI ::temp22                                ;@line 278
						Cast ::temp18 operating                                  ;@line 279
						JumpT ::temp18 _label156                                 ;@line 279
						Cast ::temp18 endingSession                              ;@line 279
					_label156:
						Cast ::temp18 ::temp18                                   ;@line 279
						JumpT ::temp18 _label157                                 ;@line 279
						CompareEQ ::temp17 generation activationGeneration       ;@line 279
						Not ::temp17 ::temp17                                    ;@line 279
						Cast ::temp18 ::temp17                                   ;@line 279
					_label157:
						JumpF ::temp18 _label158                                 ;@line 279
						Return None                                              ;@line 280
						Jump _label158                                           ;@line 280
					_label158:
						CompareEQ ::temp17 nativeAPI 4                           ;@line 282
						Not ::temp17 ::temp17                                    ;@line 282
						JumpF ::temp17 _label159                                 ;@line 282
						CallMethod RejectActivation self ::NoneVar "NATIVE_API_MISMATCH: reinstala los archivos completos de esta versiÃ³n."  ;@line 283
						Return None                                              ;@line 284
						Jump _label159                                           ;@line 284
					_label159:
						JumpF ::UseSightCamera_var _label160                     ;@line 286
						CallStatic astrasightnative IsAvailable ::temp18         ;@line 288
						Not ::temp17 ::temp18                                    ;@line 288
						JumpF ::temp17 _label161                                 ;@line 288
						CallMethod RejectActivation self ::NoneVar "NATIVE_SIGHT_UNAVAILABLE: la mira nativa no estÃ¡ disponible."  ;@line 289
						Return None                                              ;@line 290
						Jump _label161                                           ;@line 290
					_label161:
						Cast ::temp18 operating                                  ;@line 292
						JumpT ::temp18 _label162                                 ;@line 292
						Cast ::temp18 endingSession                              ;@line 292
					_label162:
						Cast ::temp18 ::temp18                                   ;@line 292
						JumpT ::temp18 _label163                                 ;@line 292
						CompareEQ ::temp17 generation activationGeneration       ;@line 292
						Not ::temp17 ::temp17                                    ;@line 292
						Cast ::temp18 ::temp17                                   ;@line 292
					_label163:
						JumpF ::temp18 _label164                                 ;@line 292
						Return None                                              ;@line 293
						Jump _label164                                           ;@line 293
					_label164:
						Jump _label160                                           ;@line 293
					_label160:
						Cast ::temp23 None                                       ;@line 296
						CompareEQ ::temp17 ::Session_var ::temp23                ;@line 296
						JumpF ::temp17 _label165                                 ;@line 296
						CallMethod RejectActivation self ::NoneVar "PROPERTY_SESSION_NONE: falta AstraAsedioSessionQuest."  ;@line 297
						Return None                                              ;@line 298
						Jump _label165                                           ;@line 298
					_label165:
						Cast ::temp24 None                                       ;@line 300
						CompareEQ ::temp18 ::Launcher_var ::temp24               ;@line 300
						JumpF ::temp18 _label166                                 ;@line 300
						CallMethod RejectActivation self ::NoneVar "PROPERTY_LAUNCHER_NONE: falta el arma de disparo."  ;@line 301
						Return None                                              ;@line 302
						Jump _label166                                           ;@line 302
					_label166:
						Cast ::temp25 None                                       ;@line 304
						CompareEQ ::temp17 ::ShotAmmo_var ::temp25               ;@line 304
						JumpF ::temp17 _label167                                 ;@line 304
						CallMethod RejectActivation self ::NoneVar "PROPERTY_SHOTAMMO_NONE: falta el virote nativo."  ;@line 305
						Return None                                              ;@line 306
						Jump _label167                                           ;@line 306
					_label167:
						Cast ::temp25 None                                       ;@line 308
						CompareEQ ::temp18 ::SteelBolt_var ::temp25              ;@line 308
						JumpF ::temp18 _label168                                 ;@line 308
						CallMethod RejectActivation self ::NoneVar "PROPERTY_STEELBOLT_NONE: falta el virote de acero."  ;@line 309
						Return None                                              ;@line 310
						Jump _label168                                           ;@line 310
					_label168:
						CallMethod IsRunning ::Session_var ::temp17              ;@line 312
						Not ::temp18 ::temp17                                    ;@line 312
						JumpF ::temp18 _label169                                 ;@line 312
						CallMethod RejectActivation self ::NoneVar "SESSION_NOT_RUNNING: la quest de control no ha iniciado."  ;@line 313
						Return None                                              ;@line 314
						Jump _label169                                           ;@line 314
					_label169:
						CallMethod IsDead player ::temp17                        ;@line 316
						JumpF ::temp17 _label170                                 ;@line 316
						CallMethod RejectActivation self ::NoneVar "PLAYER_DEAD: no se puede operar durante la muerte."  ;@line 317
						Return None                                              ;@line 318
						Jump _label170                                           ;@line 318
					_label170:
						CallStatic game IsLookingControlsEnabled ::temp18        ;@line 320
						Not ::temp17 ::temp18                                    ;@line 320
						JumpF ::temp17 _label171                                 ;@line 320
						CallMethod RejectActivation self ::NoneVar "LOOKING_CONTROLS_DISABLED: otro control ha bloqueado la mirada."  ;@line 321
						Return None                                              ;@line 322
						Jump _label171                                           ;@line 322
					_label171:
						CallMethod ReadCameraState self ::temp22                 ;@line 324
						Assign activationCamera ::temp22                         ;@line 324
						CompareEQ ::temp18 activationCamera 0                    ;@line 325
						Not ::temp18 ::temp18                                    ;@line 325
						Cast ::temp18 ::temp18                                   ;@line 325
						JumpF ::temp18 _label172                                 ;@line 325
						CompareEQ ::temp17 activationCamera 8                    ;@line 325
						Not ::temp17 ::temp17                                    ;@line 325
						Cast ::temp18 ::temp17                                   ;@line 325
					_label172:
						Cast ::temp18 ::temp18                                   ;@line 325
						JumpF ::temp18 _label173                                 ;@line 325
						CompareEQ ::temp17 activationCamera 9                    ;@line 325
						Not ::temp17 ::temp17                                    ;@line 325
						Cast ::temp18 ::temp17                                   ;@line 325
					_label173:
						JumpF ::temp18 _label174                                 ;@line 325
						CallMethod RejectActivation self ::NoneVar "CAMERA_STATE_UNSUPPORTED: sal de la cÃ¡mara especial para operar."  ;@line 326
						Return None                                              ;@line 327
						Jump _label174                                           ;@line 327
					_label174:
						CallMethod CaptureMatrices self ::temp17                 ;@line 329
						Not ::temp18 ::temp17                                    ;@line 329
						JumpF ::temp18 _label175                                 ;@line 329
						CallMethod RejectActivation self ::NoneVar matrixFailure  ;@line 330
						Return None                                              ;@line 331
						Jump _label175                                           ;@line 331
					_label175:
						CallMethod NearOperator self ::temp17                    ;@line 333
						Not ::temp18 ::temp17                                    ;@line 333
						JumpF ::temp18 _label176                                 ;@line 333
						CallMethod RejectActivation self ::NoneVar operatorFailure  ;@line 334
						Return None                                              ;@line 335
						Jump _label176                                           ;@line 335
					_label176:
						Cast ::temp17 operating                                  ;@line 337
						JumpT ::temp17 _label177                                 ;@line 337
						Cast ::temp17 endingSession                              ;@line 337
					_label177:
						Cast ::temp17 ::temp17                                   ;@line 337
						JumpT ::temp17 _label178                                 ;@line 337
						CompareEQ ::temp18 generation activationGeneration       ;@line 337
						Not ::temp18 ::temp18                                    ;@line 337
						Cast ::temp17 ::temp18                                   ;@line 337
					_label178:
						JumpF ::temp17 _label179                                 ;@line 337
						Return None                                              ;@line 338
						Jump _label179                                           ;@line 338
					_label179:
						Cast ::temp19 None                                       ;@line 341
						Assign combatAtEntry ::temp19                            ;@line 341
						Cast ::temp19 None                                       ;@line 342
						CompareEQ ::temp18 player ::temp19                       ;@line 342
						Not ::temp18 ::temp18                                    ;@line 342
						JumpF ::temp18 _label180                                 ;@line 342
						CallMethod GetCombatTarget player ::temp19               ;@line 343
						Assign combatAtEntry ::temp19                            ;@line 343
						Jump _label180                                           ;@line 343
					_label180:
						CallMethod Acquire ::Session_var ::temp22 self           ;@line 345
						Assign acquiredToken ::temp22                            ;@line 345
						Cast ::temp17 operating                                  ;@line 346
						JumpT ::temp17 _label181                                 ;@line 346
						Cast ::temp17 endingSession                              ;@line 346
					_label181:
						Cast ::temp17 ::temp17                                   ;@line 346
						JumpT ::temp17 _label182                                 ;@line 346
						CompareEQ ::temp18 generation activationGeneration       ;@line 346
						Not ::temp18 ::temp18                                    ;@line 346
						Cast ::temp17 ::temp18                                   ;@line 346
					_label182:
						JumpF ::temp17 _label183                                 ;@line 346
						CallMethod Release ::Session_var ::NoneVar self acquiredToken  ;@line 348
						Return None                                              ;@line 349
						Jump _label183                                           ;@line 349
					_label183:
						Assign token acquiredToken                               ;@line 351
						CompareLT ::temp18 token 0                               ;@line 352
						JumpF ::temp18 _label184                                 ;@line 352
						CallMethod RejectActivation self ::NoneVar "SESSION_ENTRY_CANCELLED: entrada cancelada o sesiÃ³n de control ocupada."  ;@line 353
						Return None                                              ;@line 354
						Jump _label184                                           ;@line 354
					_label184:
						IAdd ::temp22 generation 1                               ;@line 356
						Assign generation ::temp22                               ;@line 356
						Assign entryGeneration generation                        ;@line 357
						Assign entryToken token                                  ;@line 358
						Assign operating True                                    ;@line 359
						JumpF ::OcupadaGuardia_var _label185                     ;@line 360
						Cast ::temp21 1                                          ;@line 361
						CallMethod SetValue ::OcupadaGuardia_var ::NoneVar ::temp21  ;@line 361
						Jump _label185                                           ;@line 361
					_label185:
						Assign retainedCombatTarget combatAtEntry                ;@line 363
						Assign nextCombatRetain 0.000000                         ;@line 364
						Assign cameraEntryPending True                           ;@line 365
						CallStatic utility GetCurrentRealTime ::temp21           ;@line 366
						Assign cameraEntryStartedAt ::temp21                     ;@line 366
						FAdd ::temp21 cameraEntryStartedAt 1.500000              ;@line 368
						Assign cameraEntryDeadline ::temp21                      ;@line 368
						Assign aligned False                                     ;@line 369
						CompareEQ ::temp17 cameraEntryStartedAt cameraEntryStartedAt  ;@line 370
						Cast ::temp17 ::temp17                                   ;@line 370
						JumpF ::temp17 _label186                                 ;@line 370
						CompareGTE ::temp18 cameraEntryStartedAt 0.000000        ;@line 370
						Cast ::temp17 ::temp18                                   ;@line 370
					_label186:
						Cast ::temp17 ::temp17                                   ;@line 370
						JumpF ::temp17 _label187                                 ;@line 370
						CompareLTE ::temp18 cameraEntryStartedAt 1000000000.000000  ;@line 370
						Cast ::temp17 ::temp18                                   ;@line 370
					_label187:
						JumpF ::temp17 _label188                                 ;@line 370
						CallMethod AlignLookToWeapon self ::temp18 entryGeneration  ;@line 371
						Assign aligned ::temp18                                  ;@line 371
						Jump _label188                                           ;@line 371
					_label188:
						Not ::temp18 operating                                   ;@line 373
						Cast ::temp18 ::temp18                                   ;@line 373
						JumpT ::temp18 _label189                                 ;@line 373
						CompareEQ ::temp17 generation entryGeneration            ;@line 373
						Not ::temp17 ::temp17                                    ;@line 373
						Cast ::temp18 ::temp17                                   ;@line 373
					_label189:
						Cast ::temp18 ::temp18                                   ;@line 373
						JumpT ::temp18 _label190                                 ;@line 373
						CompareEQ ::temp17 token entryToken                      ;@line 373
						Not ::temp17 ::temp17                                    ;@line 373
						Cast ::temp18 ::temp17                                   ;@line 373
					_label190:
						JumpF ::temp18 _label191                                 ;@line 373
						Return None                                              ;@line 374
						Jump _label191                                           ;@line 374
					_label191:
						Not ::temp17 aligned                                     ;@line 376
						JumpF ::temp17 _label192                                 ;@line 376
						CallMethod RejectActivation self ::NoneVar "CAMERA_ENTRY_FAILED: no se pudo alinear la mirada."  ;@line 377
						CallMethod EndSession self ::NoneVar                     ;@line 378
						Return None                                              ;@line 379
						Jump _label192                                           ;@line 379
					_label192:
						Assign phase 0                                           ;@line 381
						Cast ::temp17 needsReset                                 ;@line 382
						JumpF ::temp17 _label193                                 ;@line 382
						Not ::temp18 ::UseSightCamera_var                        ;@line 382
						Cast ::temp17 ::temp18                                   ;@line 382
					_label193:
						JumpF ::temp17 _label194                                 ;@line 382
						Assign phase 3                                           ;@line 383
						Assign elapsed 0.000000                                  ;@line 384
						CallMethod PlayGamebryoAnimation self ::temp18 "Reset" True 0.000000  ;@line 385
						Assign entryResetStarted ::temp18                        ;@line 385
						Not ::temp18 operating                                   ;@line 386
						Cast ::temp18 ::temp18                                   ;@line 386
						JumpT ::temp18 _label195                                 ;@line 386
						CompareEQ ::temp26 generation entryGeneration            ;@line 386
						Not ::temp26 ::temp26                                    ;@line 386
						Cast ::temp18 ::temp26                                   ;@line 386
					_label195:
						Cast ::temp18 ::temp18                                   ;@line 386
						JumpT ::temp18 _label196                                 ;@line 386
						CompareEQ ::temp26 token entryToken                      ;@line 386
						Not ::temp26 ::temp26                                    ;@line 386
						Cast ::temp18 ::temp26                                   ;@line 386
					_label196:
						JumpF ::temp18 _label197                                 ;@line 386
						Return None                                              ;@line 387
						Jump _label197                                           ;@line 387
					_label197:
						Not ::temp26 entryResetStarted                           ;@line 389
						JumpF ::temp26 _label198                                 ;@line 389
						CallMethod RejectShot self ::NoneVar "RESET_ANIMATION_FAILED: no se pudo iniciar la recarga."  ;@line 390
						CallMethod EndSession self ::NoneVar                     ;@line 391
						Return None                                              ;@line 392
						Jump _label198                                           ;@line 392
					_label198:
						Jump _label194                                           ;@line 392
					_label194:
						CallMethod ClearHeldInput self ::NoneVar False           ;@line 395
						Assign inputPaused False                                 ;@line 396
						Assign menuWasOpen False                                 ;@line 397
						Assign cameraGraceUntil 0.000000                         ;@line 398
						CallStatic utility GetCurrentRealTime ::temp21           ;@line 399
						Assign lastTick ::temp21                                 ;@line 399
						FAdd ::temp21 lastTick 0.350000                          ;@line 400
						Assign activateReadyAt ::temp21                          ;@line 400
						Assign firstUpdatePending True                           ;@line 401
						CallMethod RegisterMenus self ::NoneVar                  ;@line 402
						CallMethod RegisterInput self ::NoneVar                  ;@line 403
						Not ::temp18 operating                                   ;@line 404
						Cast ::temp17 ::temp18                                   ;@line 404
						JumpT ::temp17 _label199                                 ;@line 404
						CompareEQ ::temp26 generation entryGeneration            ;@line 404
						Not ::temp26 ::temp26                                    ;@line 404
						Cast ::temp17 ::temp26                                   ;@line 404
					_label199:
						Cast ::temp26 ::temp17                                   ;@line 404
						JumpT ::temp26 _label200                                 ;@line 404
						CompareEQ ::temp18 token entryToken                      ;@line 404
						Not ::temp18 ::temp18                                    ;@line 404
						Cast ::temp26 ::temp18                                   ;@line 404
					_label200:
						JumpF ::temp26 _label201                                 ;@line 404
						Return None                                              ;@line 405
						Jump _label201                                           ;@line 405
					_label201:
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSeconds_var  ;@line 407
						Cast ::temp15 token                                      ;@line 408
						StrCat ::temp16 "AstraAsedio session acquired token=" ::temp15  ;@line 408
						StrCat ::temp15 ::temp16 " generation="                  ;@line 408
						Cast ::temp16 generation                                 ;@line 408
						StrCat ::temp16 ::temp15 ::temp16                        ;@line 408
						CallStatic debug Trace ::NoneVar ::temp16 0              ;@line 408
						CallStatic debug Notification ::NoneVar "Astra: ratÃ³n apunta, ataque dispara, activar sale. Necesita virotes de acero."  ;@line 409
					.endCode
				.endFunction
				.function SessionFailureReason
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return String
					.paramTable
					.endParamTable
					.localTable
						.local ::temp98 Bool
					.endLocalTable
					.code
						JumpF ::UseSightCamera_var _label202                     ;@line 887
						Return "NATIVE_SIGHT_NOT_READY: la mira nativa no estÃ¡ activa (cambiÃ³ la cÃ¡mara o el contexto)."  ;@line 888
						Jump _label202                                           ;@line 888
					_label202:
						CompareEQ ::temp98 operatorFailure ""                    ;@line 890
						Not ::temp98 ::temp98                                    ;@line 890
						JumpF ::temp98 _label203                                 ;@line 890
						Return operatorFailure                                   ;@line 891
						Jump _label203                                           ;@line 891
					_label203:
						Return "SESSION_CONTEXT_LOST: la sesiÃ³n de control ya no es vÃ¡lida."  ;@line 893
					.endCode
				.endFunction
				.function EndSession
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
						.local ::temp222 Actor
						.local ::temp223 Bool
						.local ::temp224 Float
						.local ::temp225 Int
						.local ::temp226 String
						.local ::temp227 String
						.local ::temp228 Bool
						.local ::temp233 astraasediosession
						.local oldToken Int
						.local restoreSightAim Bool
						.local oldPhase Int
						.local oldCommitted Bool
						.local cleanupGeneration Int
						.local exitTime Float
						.local ::temp229 ObjectReference
						.local ::temp230 Bool
						.local ::temp231 Bool
						.local quiet Bool
						.local spins Int
						.local started Float
						.local now Float
						.local ::temp232 Bool
					.endLocalTable
					.code
						CallMethod TraceRetainedCombat self ::NoneVar "exit"     ;@line 1928
						Cast ::temp222 None                                      ;@line 1929
						Assign retainedCombatTarget ::temp222                    ;@line 1929
						Assign nextCombatRetain 0.000000                         ;@line 1930
						JumpF endingSession _label204                            ;@line 1931
						Return None                                              ;@line 1932
						Jump _label204                                           ;@line 1932
					_label204:
						Assign endingSession True                                ;@line 1934
						Assign oldToken token                                    ;@line 1935
						Assign restoreSightAim False                             ;@line 1936
						Assign oldPhase phase                                    ;@line 1937
						Assign oldCommitted shotCommitted                        ;@line 1938
						CompareGT ::temp223 phase 0                              ;@line 1939
						JumpF ::temp223 _label205                                ;@line 1939
						Assign needsReset True                                   ;@line 1940
						Jump _label205                                           ;@line 1940
					_label205:
						Assign operating False                                   ;@line 1942
						Cast ::temp223 ::OcupadaGuardia_var                      ;@line 1943
						JumpF ::temp223 _label206                                ;@line 1943
						CallStatic utility GetCurrentRealTime ::temp224          ;@line 1943
						CompareGTE ::temp223 ::temp224 demoUntil                 ;@line 1943
						Cast ::temp223 ::temp223                                 ;@line 1943
					_label206:
						JumpF ::temp223 _label207                                ;@line 1943
						Cast ::temp224 0                                         ;@line 1944
						CallMethod SetValue ::OcupadaGuardia_var ::NoneVar ::temp224  ;@line 1944
						Jump _label207                                           ;@line 1944
					_label207:
						Assign cameraEntryPending False                          ;@line 1946
						Assign cameraGraceUntil 0.000000                         ;@line 1947
						Assign firstUpdatePending False                          ;@line 1948
						IAdd ::temp225 generation 1                              ;@line 1949
						Assign generation ::temp225                              ;@line 1949
						Assign cleanupGeneration generation                      ;@line 1950
						Assign token -1                                          ;@line 1951
						Assign nativeSightRequested False                        ;@line 1952
						Assign sightFreezePending False                          ;@line 1953
						Assign sightThawPending False                            ;@line 1954
						Assign sightFreezeGeneration -1                          ;@line 1955
						Assign shotGeneration -1                                 ;@line 1956
						Assign phase 0                                           ;@line 1957
						Assign shotCommitted False                               ;@line 1958
						Assign updating False                                    ;@line 1959
						Assign inputPaused True                                  ;@line 1960
						Assign menuWasOpen False                                 ;@line 1961
						CallMethod ClearHeldInput self ::NoneVar True            ;@line 1962
						Cast ::temp226 oldToken                                  ;@line 1963
						StrCat ::temp226 "AstraAsedio EndSession token=" ::temp226  ;@line 1963
						StrCat ::temp226 ::temp226 " generation="                ;@line 1963
						Cast ::temp227 cleanupGeneration                         ;@line 1963
						StrCat ::temp227 ::temp226 ::temp227                     ;@line 1963
						StrCat ::temp226 ::temp227 " phase="                     ;@line 1963
						Cast ::temp227 oldPhase                                  ;@line 1963
						StrCat ::temp227 ::temp226 ::temp227                     ;@line 1963
						StrCat ::temp226 ::temp227 " committed="                 ;@line 1963
						Cast ::temp227 oldCommitted                              ;@line 1963
						StrCat ::temp227 ::temp226 ::temp227                     ;@line 1963
						CallStatic debug Trace ::NoneVar ::temp227 0             ;@line 1963
						CallMethod CleanupCurrent self ::temp223 cleanupGeneration  ;@line 1964
						Not ::temp223 ::temp223                                  ;@line 1964
						JumpF ::temp223 _label208                                ;@line 1964
						Return None                                              ;@line 1965
						Jump _label208                                           ;@line 1965
					_label208:
						CallStatic utility GetCurrentRealTime ::temp224          ;@line 1967
						Assign exitTime ::temp224                                ;@line 1967
						CallMethod CleanupCurrent self ::temp223 cleanupGeneration  ;@line 1968
						Not ::temp223 ::temp223                                  ;@line 1968
						JumpF ::temp223 _label209                                ;@line 1968
						Return None                                              ;@line 1969
						Jump _label209                                           ;@line 1969
					_label209:
						FAdd ::temp224 exitTime 0.350000                         ;@line 1971
						Assign activateBlockedUntil ::temp224                    ;@line 1971
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 1972
						CallMethod CleanupCurrent self ::temp223 cleanupGeneration  ;@line 1973
						Not ::temp223 ::temp223                                  ;@line 1973
						JumpF ::temp223 _label210                                ;@line 1973
						Return None                                              ;@line 1974
						Jump _label210                                           ;@line 1974
					_label210:
						CallMethod UnregisterForAllKeys self ::NoneVar           ;@line 1976
						CallMethod CleanupCurrent self ::temp223 cleanupGeneration  ;@line 1977
						Not ::temp223 ::temp223                                  ;@line 1977
						JumpF ::temp223 _label211                                ;@line 1977
						Return None                                              ;@line 1978
						Jump _label211                                           ;@line 1978
					_label211:
						CallMethod UnregisterForAllControls self ::NoneVar       ;@line 1980
						CallMethod CleanupCurrent self ::temp223 cleanupGeneration  ;@line 1981
						Not ::temp223 ::temp223                                  ;@line 1981
						JumpF ::temp223 _label212                                ;@line 1981
						Return None                                              ;@line 1982
						Jump _label212                                           ;@line 1982
					_label212:
						CallMethod UnregisterForAllMenus self ::NoneVar          ;@line 1984
						CallMethod CleanupCurrent self ::temp223 cleanupGeneration  ;@line 1985
						Not ::temp223 ::temp223                                  ;@line 1985
						JumpF ::temp223 _label213                                ;@line 1985
						Return None                                              ;@line 1986
						Jump _label213                                           ;@line 1986
					_label213:
						Cast ::temp223 ::UseSightCamera_var                      ;@line 1988
						JumpF ::temp223 _label214                                ;@line 1988
						CompareGT ::temp223 oldToken 0                           ;@line 1988
						Cast ::temp223 ::temp223                                 ;@line 1988
					_label214:
						Cast ::temp223 ::temp223                                 ;@line 1988
						JumpF ::temp223 _label215                                ;@line 1988
						CallStatic skse GetPluginVersion ::temp225 "AstraSight"  ;@line 1988
						CompareGTE ::temp228 ::temp225 1                         ;@line 1988
						Cast ::temp223 ::temp228                                 ;@line 1988
					_label215:
						JumpF ::temp223 _label216                                ;@line 1988
						Cast ::temp229 self                                      ;@line 1989
						CallStatic astrasightnative EndSight ::temp228 ::temp229 oldToken  ;@line 1989
						CallStatic skse GetPluginVersion ::temp225 "AstraSight"  ;@line 1990
						CompareGTE ::temp228 ::temp225 50659328                  ;@line 1990
						JumpF ::temp228 _label217                                ;@line 1990
						Cast ::temp229 self                                      ;@line 1995
						CallStatic astrasightnative IsEffectsQuiescent ::temp230 ::temp229 oldToken  ;@line 1995
						Assign quiet ::temp230                                   ;@line 1995
						Assign spins 0                                           ;@line 1996
						Assign started 0.000000                                  ;@line 1997
						Assign now 0.000000                                      ;@line 1998
						Not ::temp230 quiet                                      ;@line 1999
						JumpF ::temp230 _label218                                ;@line 1999
						CallStatic utility GetCurrentRealTime ::temp224          ;@line 2000
						Assign started ::temp224                                 ;@line 2000
						Assign now started                                       ;@line 2001
						Jump _label218                                           ;@line 2001
					_label218:
						Not ::temp230 quiet                                      ;@line 2003
						Cast ::temp230 ::temp230                                 ;@line 2003
						JumpF ::temp230 _label219                                ;@line 2003
						CompareLT ::temp231 spins 500                            ;@line 2003
						Cast ::temp230 ::temp231                                 ;@line 2003
					_label219:
						JumpF ::temp230 _label220                                ;@line 2003
						IAdd ::temp225 spins 1                                   ;@line 2004
						Assign spins ::temp225                                   ;@line 2004
						CallStatic utility GetCurrentRealTime ::temp224          ;@line 2005
						Assign now ::temp224                                     ;@line 2005
						CompareEQ ::temp231 now now                              ;@line 2006
						Not ::temp231 ::temp231                                  ;@line 2006
						Cast ::temp231 ::temp231                                 ;@line 2006
						JumpT ::temp231 _label221                                ;@line 2006
						CompareLT ::temp232 now started                          ;@line 2006
						Cast ::temp231 ::temp232                                 ;@line 2006
					_label221:
						Cast ::temp231 ::temp231                                 ;@line 2006
						JumpT ::temp231 _label222                                ;@line 2006
						FAdd ::temp224 started 5.000000                          ;@line 2006
						CompareGTE ::temp232 now ::temp224                       ;@line 2006
						Cast ::temp231 ::temp232                                 ;@line 2006
					_label222:
						JumpF ::temp231 _label223                                ;@line 2006
						Assign spins 500                                         ;@line 2007
						Jump _label224                                           ;@line 2007
					_label223:
						CallStatic utility WaitMenuMode ::NoneVar 0.010000       ;@line 2009
						Cast ::temp229 self                                      ;@line 2010
						CallStatic astrasightnative IsEffectsQuiescent ::temp232 ::temp229 oldToken  ;@line 2010
						Assign quiet ::temp232                                   ;@line 2010
					_label224:
						Jump _label218                                           ;@line 2010
					_label220:
						Not ::temp232 quiet                                      ;@line 2013
						JumpF ::temp232 _label225                                ;@line 2013
						Cast ::temp226 oldToken                                  ;@line 2014
						StrCat ::temp227 "AstraAsedio EndSession effects quiescence timed out token=" ::temp226  ;@line 2014
						CallStatic debug Trace ::NoneVar ::temp227 0             ;@line 2014
						Jump _label225                                           ;@line 2014
					_label225:
						CallMethod CleanupCurrent self ::temp231 cleanupGeneration  ;@line 2016
						Not ::temp230 ::temp231                                  ;@line 2016
						JumpF ::temp230 _label226                                ;@line 2016
						Return None                                              ;@line 2017
						Jump _label226                                           ;@line 2017
					_label226:
						Assign yaw 0.000000                                      ;@line 2020
						Assign pitch 0.000000                                    ;@line 2021
						Assign matricesReady False                               ;@line 2022
						Jump _label217                                           ;@line 2022
					_label217:
						Jump _label216                                           ;@line 2022
					_label216:
						Cast ::temp233 None                                      ;@line 2025
						CompareEQ ::temp232 ::Session_var ::temp233              ;@line 2025
						Not ::temp232 ::temp232                                  ;@line 2025
						JumpF ::temp232 _label227                                ;@line 2025
						CallMethod Release ::Session_var ::NoneVar self oldToken  ;@line 2026
						Jump _label227                                           ;@line 2026
					_label227:
						CompareEQ ::temp231 generation cleanupGeneration         ;@line 2028
						Not ::temp231 ::temp231                                  ;@line 2028
						Cast ::temp228 ::temp231                                 ;@line 2028
						JumpT ::temp228 _label228                                ;@line 2028
						CompareEQ ::temp230 token -1                             ;@line 2028
						Not ::temp230 ::temp230                                  ;@line 2028
						Cast ::temp228 ::temp230                                 ;@line 2028
					_label228:
						Cast ::temp223 ::temp228                                 ;@line 2028
						JumpT ::temp223 _label229                                ;@line 2028
						Cast ::temp223 operating                                 ;@line 2028
					_label229:
						JumpF ::temp223 _label230                                ;@line 2028
						Return None                                              ;@line 2029
						Jump _label230                                           ;@line 2029
					_label230:
						CallMethod Is3DLoaded self ::temp232                     ;@line 2031
						JumpF ::temp232 _label231                                ;@line 2031
						CompareEQ ::temp231 generation cleanupGeneration         ;@line 2032
						Not ::temp231 ::temp231                                  ;@line 2032
						Cast ::temp228 ::temp231                                 ;@line 2032
						JumpT ::temp228 _label232                                ;@line 2032
						CompareEQ ::temp230 token -1                             ;@line 2032
						Not ::temp230 ::temp230                                  ;@line 2032
						Cast ::temp228 ::temp230                                 ;@line 2032
					_label232:
						Cast ::temp223 ::temp228                                 ;@line 2032
						JumpT ::temp223 _label233                                ;@line 2032
						Cast ::temp223 operating                                 ;@line 2032
					_label233:
						JumpF ::temp223 _label234                                ;@line 2032
						Return None                                              ;@line 2033
						Jump _label234                                           ;@line 2033
					_label234:
						JumpF restoreSightAim _label235                          ;@line 2035
						CallMethod ApplyAim self ::NoneVar                       ;@line 2038
						Jump _label235                                           ;@line 2038
					_label235:
						CallMethod CleanupCurrent self ::temp231 cleanupGeneration  ;@line 2040
						Not ::temp230 ::temp231                                  ;@line 2040
						JumpF ::temp230 _label236                                ;@line 2040
						Return None                                              ;@line 2041
						Jump _label236                                           ;@line 2041
					_label236:
						Not ::temp228 ::UseSightCamera_var                       ;@line 2043
						JumpF ::temp228 _label237                                ;@line 2043
						CallMethod PlayGamebryoAnimation self ::temp223 "Reset" True 0.000000  ;@line 2044
						Jump _label237                                           ;@line 2044
					_label237:
						CallMethod CleanupCurrent self ::temp231 cleanupGeneration  ;@line 2046
						Not ::temp230 ::temp231                                  ;@line 2046
						JumpF ::temp230 _label238                                ;@line 2046
						Return None                                              ;@line 2047
						Jump _label238                                           ;@line 2047
					_label238:
						Not ::temp223 ::UseSightCamera_var                       ;@line 2049
						JumpF ::temp223 _label239                                ;@line 2049
						Cast ::temp229 self                                      ;@line 2050
						CallStatic netimmerse SetNodeScale ::NoneVar ::temp229 ::VisualBoltNode_var 1.000000 False  ;@line 2050
						Jump _label239                                           ;@line 2050
					_label239:
						Jump _label231                                           ;@line 2050
					_label231:
						CallMethod CleanupCurrent self ::temp228 cleanupGeneration  ;@line 2053
						JumpF ::temp228 _label240                                ;@line 2053
						Assign endingSession False                               ;@line 2054
						Jump _label240                                           ;@line 2054
					_label240:
					.endCode
				.endFunction
				.function PrepareShotAnimation
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param expectedGeneration Int
					.endParamTable
					.localTable
						.local ::temp187 Bool
						.local ::temp188 Bool
						.local ::temp190 form
						.local ::temp191 Int
						.local ::temp189 String
						.local transformReady Bool
					.endLocalTable
					.code
						CallMethod InputReady self ::temp187                     ;@line 1702
						Not ::temp187 ::temp187                                  ;@line 1702
						Cast ::temp187 ::temp187                                 ;@line 1702
						JumpT ::temp187 _label241                                ;@line 1702
						CallMethod CanOperate self ::temp188 expectedGeneration  ;@line 1702
						Not ::temp188 ::temp188                                  ;@line 1702
						Cast ::temp187 ::temp188                                 ;@line 1702
					_label241:
						JumpF ::temp187 _label242                                ;@line 1702
						CallMethod SessionFailureReason self ::temp189           ;@line 1703
						StrCat ::temp189 "SHOT_SESSION_INVALID: " ::temp189      ;@line 1703
						Assign shotFailure ::temp189                             ;@line 1703
						Return False                                             ;@line 1704
						Jump _label242                                           ;@line 1704
					_label242:
						Not ::temp188 ::UseSightCamera_var                       ;@line 1706
						Cast ::temp188 ::temp188                                 ;@line 1706
						JumpF ::temp188 _label243                                ;@line 1706
						Cast ::temp190 ::SteelBolt_var                           ;@line 1706
						CallMethod GetItemCount player ::temp191 ::temp190       ;@line 1706
						CompareLT ::temp187 ::temp191 1                          ;@line 1706
						Cast ::temp188 ::temp187                                 ;@line 1706
					_label243:
						JumpF ::temp188 _label244                                ;@line 1706
						Assign shotFailure "SHOT_NO_STEEL_BOLT: necesita un virote de acero."  ;@line 1707
						Return False                                             ;@line 1708
						Jump _label244                                           ;@line 1708
					_label244:
						CallMethod ShotTransformReady self ::temp187             ;@line 1710
						Assign transformReady ::temp187                          ;@line 1710
						Not ::temp188 operating                                  ;@line 1711
						Cast ::temp188 ::temp188                                 ;@line 1711
						JumpT ::temp188 _label245                                ;@line 1711
						CompareEQ ::temp187 generation expectedGeneration        ;@line 1711
						Not ::temp187 ::temp187                                  ;@line 1711
						Cast ::temp188 ::temp187                                 ;@line 1711
					_label245:
						Cast ::temp188 ::temp188                                 ;@line 1711
						JumpT ::temp188 _label246                                ;@line 1711
						CompareEQ ::temp187 phase 1                              ;@line 1711
						Not ::temp187 ::temp187                                  ;@line 1711
						Cast ::temp188 ::temp187                                 ;@line 1711
					_label246:
						Cast ::temp187 ::temp188                                 ;@line 1711
						JumpT ::temp187 _label247                                ;@line 1711
						Cast ::temp187 inputPaused                               ;@line 1711
					_label247:
						Cast ::temp188 ::temp187                                 ;@line 1711
						JumpT ::temp188 _label248                                ;@line 1711
						Cast ::temp188 menuWasOpen                               ;@line 1711
					_label248:
						JumpF ::temp188 _label249                                ;@line 1711
						Return False                                             ;@line 1712
						Jump _label249                                           ;@line 1712
					_label249:
						Not ::temp187 transformReady                             ;@line 1714
						JumpF ::temp187 _label250                                ;@line 1714
						Return False                                             ;@line 1715
						Jump _label250                                           ;@line 1715
					_label250:
						CallMethod PlayGamebryoAnimation self ::temp188 "Fire" True 0.000000  ;@line 1717
						Not ::temp187 ::temp188                                  ;@line 1717
						JumpF ::temp187 _label251                                ;@line 1717
						Assign shotFailure "FIRE_ANIMATION_FAILED: PlayGamebryoAnimation devolviÃ³ false."  ;@line 1718
						Return False                                             ;@line 1719
						Jump _label251                                           ;@line 1719
					_label251:
						Return True                                              ;@line 1721
					.endCode
				.endFunction
				.function NearOperator
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
					.localTable
						.local ::temp89 Bool
						.local ::temp90 ObjectReference
						.local ::temp91 Bool
						.local i Int
						.local ::temp92 Float
						.local ::temp93 Float
						.local ::temp94 Bool
						.local ::temp95 Int
						.local rootScale Float
						.local height Float
						.local dx Float
						.local dy Float
						.local dz Float
						.local inRange Bool
						.local ::temp96 String
						.local ::temp97 String
					.endLocalTable
					.code
						Assign operatorFailure ""                                ;@line 843
						CallMethod Is3DLoaded self ::temp89                      ;@line 844
						Not ::temp89 ::temp89                                    ;@line 844
						Cast ::temp89 ::temp89                                   ;@line 844
						JumpT ::temp89 _label252                                 ;@line 844
						Cast ::temp90 self                                       ;@line 844
						CallStatic netimmerse HasNode ::temp91 ::temp90 ::OperatorNode_var False  ;@line 844
						Not ::temp91 ::temp91                                    ;@line 844
						Cast ::temp89 ::temp91                                   ;@line 844
					_label252:
						JumpF ::temp89 _label253                                 ;@line 844
						Assign operatorFailure "OPERATOR_NODE_UNAVAILABLE: la manivela aÃºn no estÃ¡ cargada."  ;@line 845
						Return False                                             ;@line 846
						Jump _label253                                           ;@line 846
					_label253:
						Cast ::temp90 self                                       ;@line 848
						CallStatic netimmerse GetNodeWorldRotationMatrix ::temp91 ::temp90 "" rootWorldMatrix False  ;@line 848
						Not ::temp89 ::temp91                                    ;@line 848
						JumpF ::temp89 _label254                                 ;@line 848
						Assign operatorFailure "OPERATOR_ROOT_MATRIX_FAILED: no se pudo leer la raÃ­z de la ballesta."  ;@line 849
						Return False                                             ;@line 850
						Jump _label254                                           ;@line 850
					_label254:
						Assign i 0                                               ;@line 852
					_label258:
						CompareLT ::temp91 i 9                                   ;@line 853
						JumpF ::temp91 _label255                                 ;@line 853
						ArrayGetElement ::temp92 rootWorldMatrix i               ;@line 854
						ArrayGetElement ::temp93 rootWorldMatrix i               ;@line 854
						CompareEQ ::temp89 ::temp92 ::temp93                     ;@line 854
						Not ::temp89 ::temp89                                    ;@line 854
						Cast ::temp89 ::temp89                                   ;@line 854
						JumpT ::temp89 _label256                                 ;@line 854
						ArrayGetElement ::temp92 rootWorldMatrix i               ;@line 854
						CallStatic math Abs ::temp93 ::temp92                    ;@line 854
						CompareGT ::temp94 ::temp93 1.050000                     ;@line 854
						Cast ::temp89 ::temp94                                   ;@line 854
					_label256:
						JumpF ::temp89 _label257                                 ;@line 854
						Assign operatorFailure "OPERATOR_ROOT_MATRIX_INVALID: transformaciÃ³n no finita."  ;@line 855
						Return False                                             ;@line 856
						Jump _label257                                           ;@line 856
					_label257:
						IAdd ::temp95 i 1                                        ;@line 858
						Assign i ::temp95                                        ;@line 858
						Jump _label258                                           ;@line 858
					_label255:
						Cast ::temp90 self                                       ;@line 860
						CallStatic netimmerse GetNodeScale ::temp92 ::temp90 "" False  ;@line 860
						Assign rootScale ::temp92                                ;@line 860
						CompareEQ ::temp94 rootScale rootScale                   ;@line 861
						Not ::temp94 ::temp94                                    ;@line 861
						Cast ::temp91 ::temp94                                   ;@line 861
						JumpT ::temp91 _label259                                 ;@line 861
						CompareLTE ::temp89 rootScale 0.000000                   ;@line 861
						Cast ::temp91 ::temp89                                   ;@line 861
					_label259:
						Cast ::temp89 ::temp91                                   ;@line 861
						JumpT ::temp89 _label260                                 ;@line 861
						CompareGT ::temp94 rootScale 100.000000                  ;@line 861
						Cast ::temp89 ::temp94                                   ;@line 861
					_label260:
						JumpF ::temp89 _label261                                 ;@line 861
						Assign operatorFailure "OPERATOR_ROOT_SCALE_INVALID: escala no vÃ¡lida."  ;@line 862
						Return False                                             ;@line 863
						Jump _label261                                           ;@line 863
					_label261:
						FMultiply ::temp93 ::OperatorHeight_var rootScale        ;@line 867
						Assign height ::temp93                                   ;@line 867
						CallMethod GetPositionX player ::temp92                  ;@line 868
						Cast ::temp90 self                                       ;@line 868
						CallStatic netimmerse GetNodeWorldPositionX ::temp93 ::temp90 ::OperatorNode_var False  ;@line 868
						FSubtract ::temp92 ::temp92 ::temp93                     ;@line 868
						ArrayGetElement ::temp93 rootWorldMatrix 2               ;@line 868
						FMultiply ::temp93 height ::temp93                       ;@line 868
						FAdd ::temp92 ::temp92 ::temp93                          ;@line 868
						Assign dx ::temp92                                       ;@line 868
						CallMethod GetPositionY player ::temp93                  ;@line 869
						Cast ::temp90 self                                       ;@line 869
						CallStatic netimmerse GetNodeWorldPositionY ::temp92 ::temp90 ::OperatorNode_var False  ;@line 869
						FSubtract ::temp93 ::temp93 ::temp92                     ;@line 869
						ArrayGetElement ::temp92 rootWorldMatrix 5               ;@line 869
						FMultiply ::temp92 height ::temp92                       ;@line 869
						FAdd ::temp93 ::temp93 ::temp92                          ;@line 869
						Assign dy ::temp93                                       ;@line 869
						CallMethod GetPositionZ player ::temp92                  ;@line 870
						Cast ::temp90 self                                       ;@line 870
						CallStatic netimmerse GetNodeWorldPositionZ ::temp93 ::temp90 ::OperatorNode_var False  ;@line 870
						FSubtract ::temp92 ::temp92 ::temp93                     ;@line 870
						ArrayGetElement ::temp93 rootWorldMatrix 8               ;@line 870
						FMultiply ::temp93 height ::temp93                       ;@line 870
						FAdd ::temp92 ::temp92 ::temp93                          ;@line 870
						Assign dz ::temp92                                       ;@line 870
						CompareEQ ::temp91 dx dx                                 ;@line 871
						Not ::temp91 ::temp91                                    ;@line 871
						Cast ::temp89 ::temp91                                   ;@line 871
						JumpT ::temp89 _label262                                 ;@line 871
						CompareEQ ::temp94 dy dy                                 ;@line 871
						Not ::temp94 ::temp94                                    ;@line 871
						Cast ::temp89 ::temp94                                   ;@line 871
					_label262:
						Cast ::temp94 ::temp89                                   ;@line 871
						JumpT ::temp94 _label263                                 ;@line 871
						CompareEQ ::temp91 dz dz                                 ;@line 871
						Not ::temp91 ::temp91                                    ;@line 871
						Cast ::temp94 ::temp91                                   ;@line 871
					_label263:
						Cast ::temp91 ::temp94                                   ;@line 871
						JumpT ::temp91 _label264                                 ;@line 871
						CallStatic math Abs ::temp93 dx                          ;@line 871
						CompareGT ::temp89 ::temp93 1000000.000000               ;@line 871
						Cast ::temp91 ::temp89                                   ;@line 871
					_label264:
						Cast ::temp89 ::temp91                                   ;@line 871
						JumpT ::temp89 _label265                                 ;@line 871
						CallStatic math Abs ::temp92 dy                          ;@line 871
						CompareGT ::temp94 ::temp92 1000000.000000               ;@line 871
						Cast ::temp89 ::temp94                                   ;@line 871
					_label265:
						Cast ::temp94 ::temp89                                   ;@line 871
						JumpT ::temp94 _label266                                 ;@line 871
						CallStatic math Abs ::temp93 dz                          ;@line 871
						CompareGT ::temp91 ::temp93 1000000.000000               ;@line 871
						Cast ::temp94 ::temp91                                   ;@line 871
					_label266:
						JumpF ::temp94 _label267                                 ;@line 871
						Assign operatorFailure "OPERATOR_POSITION_INVALID: posiciÃ³n no finita."  ;@line 872
						Return False                                             ;@line 873
						Jump _label267                                           ;@line 873
					_label267:
						Assign operatorFailure ""                                ;@line 877
						FMultiply ::temp92 dx dx                                 ;@line 878
						FMultiply ::temp93 dy dy                                 ;@line 878
						FAdd ::temp92 ::temp92 ::temp93                          ;@line 878
						FMultiply ::temp93 ::OperatorDistance_var ::OperatorDistance_var  ;@line 878
						CompareLTE ::temp89 ::temp92 ::temp93                    ;@line 878
						Cast ::temp94 ::temp89                                   ;@line 878
						JumpF ::temp94 _label268                                 ;@line 878
						CallStatic math Abs ::temp92 dz                          ;@line 878
						CompareLTE ::temp91 ::temp92 ::OperatorVerticalTolerance_var  ;@line 878
						Cast ::temp94 ::temp91                                   ;@line 878
					_label268:
						Assign inRange ::temp94                                  ;@line 878
						Not ::temp89 inRange                                     ;@line 879
						JumpF ::temp89 _label269                                 ;@line 879
						Cast ::temp96 dx                                         ;@line 880
						StrCat ::temp96 "OPERATOR_OUT_OF_RANGE: AcÃ©rcate a la manivela. dx=" ::temp96  ;@line 880
						StrCat ::temp96 ::temp96 " dy="                          ;@line 880
						Cast ::temp97 dy                                         ;@line 880
						StrCat ::temp97 ::temp96 ::temp97                        ;@line 880
						StrCat ::temp96 ::temp97 " dz="                          ;@line 880
						Cast ::temp97 dz                                         ;@line 880
						StrCat ::temp97 ::temp96 ::temp97                        ;@line 880
						Assign operatorFailure ::temp97                          ;@line 880
						Jump _label269                                           ;@line 880
					_label269:
						FMultiply ::temp93 dx dx                                 ;@line 882
						FMultiply ::temp92 dy dy                                 ;@line 882
						FAdd ::temp93 ::temp93 ::temp92                          ;@line 882
						FMultiply ::temp92 ::OperatorDistance_var ::OperatorDistance_var  ;@line 882
						CompareLTE ::temp91 ::temp93 ::temp92                    ;@line 882
						Cast ::temp89 ::temp91                                   ;@line 882
						JumpF ::temp89 _label270                                 ;@line 882
						CallStatic math Abs ::temp93 dz                          ;@line 882
						CompareLTE ::temp94 ::temp93 ::OperatorVerticalTolerance_var  ;@line 882
						Cast ::temp89 ::temp94                                   ;@line 882
					_label270:
						Return ::temp89                                          ;@line 882
					.endCode
				.endFunction
				.function OnMenuClose
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param menuName String
					.endParamTable
					.localTable
						.local ::NoneVar None
						.local ::temp87 String
						.local ::temp88 String
					.endLocalTable
					.code
						JumpF operating _label271                                ;@line 835
						CallMethod PauseInput self ::NoneVar                     ;@line 836
						StrCat ::temp87 "AstraAsedio OnMenuClose menu=" menuName  ;@line 837
						StrCat ::temp87 ::temp87 " generation="                  ;@line 837
						Cast ::temp88 generation                                 ;@line 837
						StrCat ::temp88 ::temp87 ::temp88                        ;@line 837
						CallStatic debug Trace ::NoneVar ::temp88 0              ;@line 837
						Jump _label271                                           ;@line 837
					_label271:
					.endCode
				.endFunction
				.function RequestShot
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp73 Bool
						.local ::temp74 Bool
						.local ::temp75 String
						.local ::temp76 String
						.local ::NoneVar None
						.local requestGeneration Int
						.local requestToken Int
						.local pressReleaseSerial Int
						.local shotInputReady Bool
						.local releasedDuringPress Bool
					.endLocalTable
					.code
						JumpF ::UseSightCamera_var _label272                     ;@line 731
						Return None                                              ;@line 732
						Jump _label272                                           ;@line 732
					_label272:
						Assign requestGeneration generation                      ;@line 734
						Assign requestToken token                                ;@line 735
						Assign pressReleaseSerial fireReleaseSerial              ;@line 738
						CallMethod InputReady self ::temp73                      ;@line 739
						Assign shotInputReady ::temp73                           ;@line 739
						Not ::temp73 operating                                   ;@line 740
						Cast ::temp73 ::temp73                                   ;@line 740
						JumpT ::temp73 _label273                                 ;@line 740
						CompareEQ ::temp74 generation requestGeneration          ;@line 740
						Not ::temp74 ::temp74                                    ;@line 740
						Cast ::temp73 ::temp74                                   ;@line 740
					_label273:
						Cast ::temp73 ::temp73                                   ;@line 740
						JumpT ::temp73 _label274                                 ;@line 740
						CompareEQ ::temp74 token requestToken                    ;@line 740
						Not ::temp74 ::temp74                                    ;@line 740
						Cast ::temp73 ::temp74                                   ;@line 740
					_label274:
						JumpF ::temp73 _label275                                 ;@line 740
						Return None                                              ;@line 741
						Jump _label275                                           ;@line 741
					_label275:
						CompareEQ ::temp74 fireReleaseSerial pressReleaseSerial  ;@line 743
						Not ::temp74 ::temp74                                    ;@line 743
						Assign releasedDuringPress ::temp74                      ;@line 743
						Not ::temp73 shotInputReady                              ;@line 744
						JumpF ::temp73 _label276                                 ;@line 744
						Cast ::temp74 operating                                  ;@line 745
						JumpF ::temp74 _label277                                 ;@line 745
						Not ::temp74 releasedDuringPress                         ;@line 745
						Cast ::temp74 ::temp74                                   ;@line 745
					_label277:
						JumpF ::temp74 _label278                                 ;@line 745
						Assign heldFire True                                     ;@line 746
						Jump _label278                                           ;@line 746
					_label278:
						Return None                                              ;@line 748
						Jump _label276                                           ;@line 748
					_label276:
						JumpF heldFire _label279                                 ;@line 750
						Return None                                              ;@line 751
						Jump _label279                                           ;@line 751
					_label279:
						Not ::temp74 releasedDuringPress                         ;@line 755
						Assign heldFire ::temp74                                 ;@line 755
						Cast ::temp74 ::ContinuousFire_var                       ;@line 756
						JumpF ::temp74 _label280                                 ;@line 756
						Not ::temp73 releasedDuringPress                         ;@line 756
						Cast ::temp74 ::temp73                                   ;@line 756
					_label280:
						Assign repeatFire ::temp74                               ;@line 756
						Cast ::temp75 phase                                      ;@line 757
						StrCat ::temp75 "AstraAsedio fire input phase=" ::temp75  ;@line 757
						StrCat ::temp75 ::temp75 " generation="                  ;@line 757
						Cast ::temp76 generation                                 ;@line 757
						StrCat ::temp76 ::temp75 ::temp76                        ;@line 757
						CallStatic debug Trace ::NoneVar ::temp76 0              ;@line 757
						Not ::temp73 operating                                   ;@line 758
						Cast ::temp73 ::temp73                                   ;@line 758
						JumpT ::temp73 _label281                                 ;@line 758
						CompareEQ ::temp74 generation requestGeneration          ;@line 758
						Not ::temp74 ::temp74                                    ;@line 758
						Cast ::temp73 ::temp74                                   ;@line 758
					_label281:
						Cast ::temp73 ::temp73                                   ;@line 758
						JumpT ::temp73 _label282                                 ;@line 758
						CompareEQ ::temp74 token requestToken                    ;@line 758
						Not ::temp74 ::temp74                                    ;@line 758
						Cast ::temp73 ::temp74                                   ;@line 758
					_label282:
						JumpF ::temp73 _label283                                 ;@line 758
						Return None                                              ;@line 759
						Jump _label283                                           ;@line 759
					_label283:
						CompareEQ ::temp74 phase 0                               ;@line 761
						JumpF ::temp74 _label284                                 ;@line 761
						CallMethod BeginShot self ::NoneVar requestGeneration -1  ;@line 762
						Jump _label284                                           ;@line 762
					_label284:
					.endCode
				.endFunction
				.function IsPlayerOperating
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
					.localTable
					.endLocalTable
					.code
						Return operating                                         ;@line 2063
					.endCode
				.endFunction
				.function CancelPendingShot
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp80 Bool
						.local ::temp81 Bool
						.local ::temp82 Bool
						.local ::temp83 Int
						.local ::NoneVar None
						.local ::temp84 String
						.local cancelledGeneration Int
						.local cancelledToken Int
						.local cancellationGeneration Int
						.local reset3DLoaded Bool
						.local cancelledResetStarted Bool
					.endLocalTable
					.code
						JumpF ::UseSightCamera_var _label285                     ;@line 787
						Return None                                              ;@line 789
						Jump _label285                                           ;@line 789
					_label285:
						Not ::temp80 shotCommitted                               ;@line 791
						Cast ::temp82 ::temp80                                   ;@line 791
						JumpF ::temp82 _label286                                 ;@line 791
						CompareEQ ::temp81 phase 1                               ;@line 791
						Cast ::temp81 ::temp81                                   ;@line 791
						JumpT ::temp81 _label287                                 ;@line 791
						CompareEQ ::temp82 phase 2                               ;@line 791
						Cast ::temp81 ::temp82                                   ;@line 791
					_label287:
						Cast ::temp82 ::temp81                                   ;@line 791
					_label286:
						JumpF ::temp82 _label288                                 ;@line 791
						Assign cancelledGeneration shotGeneration                ;@line 792
						Assign cancelledToken token                              ;@line 793
						IAdd ::temp83 generation 1                               ;@line 794
						Assign generation ::temp83                               ;@line 794
						Assign cancellationGeneration generation                 ;@line 795
						Assign shotGeneration -1                                 ;@line 796
						Assign needsReset True                                   ;@line 797
						Assign phase 3                                           ;@line 798
						Assign elapsed 0.000000                                  ;@line 799
						Assign settleFrames 0                                    ;@line 800
						CallMethod ThawSight self ::NoneVar cancelledGeneration cancelledToken  ;@line 801
						Not ::temp80 operating                                   ;@line 802
						Cast ::temp80 ::temp80                                   ;@line 802
						JumpT ::temp80 _label289                                 ;@line 802
						CompareEQ ::temp81 generation cancellationGeneration     ;@line 802
						Not ::temp81 ::temp81                                    ;@line 802
						Cast ::temp80 ::temp81                                   ;@line 802
					_label289:
						Cast ::temp80 ::temp80                                   ;@line 802
						JumpT ::temp80 _label290                                 ;@line 802
						CompareEQ ::temp81 token cancelledToken                  ;@line 802
						Not ::temp81 ::temp81                                    ;@line 802
						Cast ::temp80 ::temp81                                   ;@line 802
					_label290:
						Cast ::temp80 ::temp80                                   ;@line 802
						JumpT ::temp80 _label291                                 ;@line 802
						CompareEQ ::temp81 phase 3                               ;@line 802
						Not ::temp81 ::temp81                                    ;@line 802
						Cast ::temp80 ::temp81                                   ;@line 802
					_label291:
						JumpF ::temp80 _label292                                 ;@line 802
						Return None                                              ;@line 803
						Jump _label292                                           ;@line 803
					_label292:
						Cast ::temp84 generation                                 ;@line 805
						StrCat ::temp84 "AstraAsedio pending shot cancelled generation=" ::temp84  ;@line 805
						CallStatic debug Trace ::NoneVar ::temp84 0              ;@line 805
						CallMethod Is3DLoaded self ::temp81                      ;@line 806
						Assign reset3DLoaded ::temp81                            ;@line 806
						Not ::temp80 operating                                   ;@line 807
						Cast ::temp80 ::temp80                                   ;@line 807
						JumpT ::temp80 _label293                                 ;@line 807
						CompareEQ ::temp81 generation cancellationGeneration     ;@line 807
						Not ::temp81 ::temp81                                    ;@line 807
						Cast ::temp80 ::temp81                                   ;@line 807
					_label293:
						Cast ::temp80 ::temp80                                   ;@line 807
						JumpT ::temp80 _label294                                 ;@line 807
						CompareEQ ::temp81 token cancelledToken                  ;@line 807
						Not ::temp81 ::temp81                                    ;@line 807
						Cast ::temp80 ::temp81                                   ;@line 807
					_label294:
						Cast ::temp80 ::temp80                                   ;@line 807
						JumpT ::temp80 _label295                                 ;@line 807
						CompareEQ ::temp81 phase 3                               ;@line 807
						Not ::temp81 ::temp81                                    ;@line 807
						Cast ::temp80 ::temp81                                   ;@line 807
					_label295:
						JumpF ::temp80 _label296                                 ;@line 807
						Return None                                              ;@line 808
						Jump _label296                                           ;@line 808
					_label296:
						JumpF reset3DLoaded _label297                            ;@line 810
						CallMethod PlayGamebryoAnimation self ::temp81 "Reset" True 0.000000  ;@line 811
						Assign cancelledResetStarted ::temp81                    ;@line 811
						Not ::temp80 operating                                   ;@line 812
						Cast ::temp80 ::temp80                                   ;@line 812
						JumpT ::temp80 _label298                                 ;@line 812
						CompareEQ ::temp81 generation cancellationGeneration     ;@line 812
						Not ::temp81 ::temp81                                    ;@line 812
						Cast ::temp80 ::temp81                                   ;@line 812
					_label298:
						Cast ::temp80 ::temp80                                   ;@line 812
						JumpT ::temp80 _label299                                 ;@line 812
						CompareEQ ::temp81 token cancelledToken                  ;@line 812
						Not ::temp81 ::temp81                                    ;@line 812
						Cast ::temp80 ::temp81                                   ;@line 812
					_label299:
						Cast ::temp80 ::temp80                                   ;@line 812
						JumpT ::temp80 _label300                                 ;@line 812
						CompareEQ ::temp81 phase 3                               ;@line 812
						Not ::temp81 ::temp81                                    ;@line 812
						Cast ::temp80 ::temp81                                   ;@line 812
					_label300:
						JumpF ::temp80 _label301                                 ;@line 812
						Return None                                              ;@line 813
						Jump _label301                                           ;@line 813
					_label301:
						Not ::temp81 cancelledResetStarted                       ;@line 815
						JumpF ::temp81 _label302                                 ;@line 815
						CallMethod RejectShot self ::NoneVar "RESET_ANIMATION_FAILED: cancelaciÃ³n del disparo."  ;@line 816
						CallMethod EndSession self ::NoneVar                     ;@line 817
						Jump _label302                                           ;@line 817
					_label302:
						Jump _label297                                           ;@line 817
					_label297:
						Jump _label288                                           ;@line 817
					_label288:
					.endCode
				.endFunction
				.function IsPlayerCleanupPending
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
					.localTable
					.endLocalTable
					.code
						Return endingSession                                     ;@line 2067
					.endCode
				.endFunction
				.function ReadCameraState
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Int
					.paramTable
					.endParamTable
					.localTable
						.local ::temp99 Int
						.local ::temp100 Bool
					.endLocalTable
					.code
						CallStatic skse GetPluginVersion ::temp99 "AstraSight"   ;@line 898
						CompareLT ::temp100 ::temp99 33554432                    ;@line 898
						JumpF ::temp100 _label303                                ;@line 898
						Return -1                                                ;@line 899
						Jump _label303                                           ;@line 899
					_label303:
						CallStatic astrasightnative GetCameraState ::temp99      ;@line 901
						Return ::temp99                                          ;@line 901
					.endCode
				.endFunction
				.function ResumeInput
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp35 Float
						.local ::temp36 Bool
						.local ::temp37 Bool
						.local resumeGeneration Int
						.local resumeToken Int
						.local resumedAt Float
					.endLocalTable
					.code
						Assign resumeGeneration generation                       ;@line 486
						Assign resumeToken token                                 ;@line 487
						Assign inputPaused False                                 ;@line 488
						Assign menuWasOpen False                                 ;@line 489
						CallStatic utility GetCurrentRealTime ::temp35           ;@line 490
						Assign resumedAt ::temp35                                ;@line 490
						Cast ::temp36 operating                                  ;@line 493
						JumpF ::temp36 _label304                                 ;@line 493
						CompareEQ ::temp36 token resumeToken                     ;@line 493
						Cast ::temp36 ::temp36                                   ;@line 493
					_label304:
						JumpF ::temp36 _label305                                 ;@line 493
						FAdd ::temp35 resumedAt 3.000000                         ;@line 494
						Assign cameraGraceUntil ::temp35                         ;@line 494
						Jump _label305                                           ;@line 494
					_label305:
						Not ::temp36 operating                                   ;@line 496
						Cast ::temp36 ::temp36                                   ;@line 496
						JumpT ::temp36 _label306                                 ;@line 496
						CompareEQ ::temp37 generation resumeGeneration           ;@line 496
						Not ::temp37 ::temp37                                    ;@line 496
						Cast ::temp36 ::temp37                                   ;@line 496
					_label306:
						Cast ::temp36 ::temp36                                   ;@line 496
						JumpT ::temp36 _label307                                 ;@line 496
						CompareEQ ::temp37 token resumeToken                     ;@line 496
						Not ::temp37 ::temp37                                    ;@line 496
						Cast ::temp36 ::temp37                                   ;@line 496
					_label307:
						Cast ::temp37 ::temp36                                   ;@line 496
						JumpT ::temp37 _label308                                 ;@line 496
						Cast ::temp37 inputPaused                                ;@line 496
					_label308:
						Cast ::temp36 ::temp37                                   ;@line 496
						JumpT ::temp36 _label309                                 ;@line 496
						Cast ::temp36 menuWasOpen                                ;@line 496
					_label309:
						JumpF ::temp36 _label310                                 ;@line 496
						Return None                                              ;@line 497
						Jump _label310                                           ;@line 497
					_label310:
						Assign lastTick resumedAt                                ;@line 499
					.endCode
				.endFunction
				.function CommitShot
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param expectedGeneration Int
					.endParamTable
					.localTable
						.local ::temp202 Bool
						.local ::temp203 Bool
						.local ::temp205 form
						.local ::temp206 Int
						.local ::temp207 ObjectReference
						.local committedToken Int
						.local commitSessionValid Bool
						.local commitMenuOpen Bool
						.local ::NoneVar None
						.local ::temp204 String
						.local availableAmmo Int
						.local commitTransformReady Bool
						.local ::temp208 String
						.local ::temp209 Float
					.endLocalTable
					.code
						JumpF ::UseSightCamera_var _label311                     ;@line 1802
						Return None                                              ;@line 1803
						Jump _label311                                           ;@line 1803
					_label311:
						Assign committedToken token                              ;@line 1805
						JumpF shotCommitted _label312                            ;@line 1806
						Return None                                              ;@line 1807
						Jump _label312                                           ;@line 1807
					_label312:
						CallMethod InputReady self ::temp202                     ;@line 1809
						Cast ::temp202 ::temp202                                 ;@line 1809
						JumpF ::temp202 _label313                                ;@line 1809
						CallMethod CanOperate self ::temp203 expectedGeneration  ;@line 1809
						Cast ::temp202 ::temp203                                 ;@line 1809
					_label313:
						Assign commitSessionValid ::temp202                      ;@line 1809
						CallStatic utility IsInMenuMode ::temp203                ;@line 1810
						Assign commitMenuOpen ::temp203                          ;@line 1810
						Not ::temp202 operating                                  ;@line 1811
						Cast ::temp202 ::temp202                                 ;@line 1811
						JumpT ::temp202 _label314                                ;@line 1811
						CompareEQ ::temp203 generation expectedGeneration        ;@line 1811
						Not ::temp203 ::temp203                                  ;@line 1811
						Cast ::temp202 ::temp203                                 ;@line 1811
					_label314:
						Cast ::temp202 ::temp202                                 ;@line 1811
						JumpT ::temp202 _label315                                ;@line 1811
						CompareEQ ::temp203 token committedToken                 ;@line 1811
						Not ::temp203 ::temp203                                  ;@line 1811
						Cast ::temp202 ::temp203                                 ;@line 1811
					_label315:
						JumpF ::temp202 _label316                                ;@line 1811
						Return None                                              ;@line 1812
						Jump _label316                                           ;@line 1812
					_label316:
						Cast ::temp203 commitMenuOpen                            ;@line 1814
						JumpT ::temp203 _label317                                ;@line 1814
						Cast ::temp203 inputPaused                               ;@line 1814
					_label317:
						Cast ::temp202 ::temp203                                 ;@line 1814
						JumpT ::temp202 _label318                                ;@line 1814
						Cast ::temp202 menuWasOpen                               ;@line 1814
					_label318:
						JumpF ::temp202 _label319                                ;@line 1814
						CallMethod PauseInput self ::NoneVar                     ;@line 1815
						Return None                                              ;@line 1816
						Jump _label319                                           ;@line 1816
					_label319:
						Not ::temp203 commitSessionValid                         ;@line 1818
						JumpF ::temp203 _label320                                ;@line 1818
						CallMethod SessionFailureReason self ::temp204           ;@line 1819
						StrCat ::temp204 "SHOT_CANCELLED_BEFORE_COMMIT: " ::temp204  ;@line 1819
						CallMethod RejectShot self ::NoneVar ::temp204           ;@line 1819
						CallMethod EndSession self ::NoneVar                     ;@line 1820
						Return None                                              ;@line 1821
						Jump _label320                                           ;@line 1821
					_label320:
						Cast ::temp205 ::SteelBolt_var                           ;@line 1823
						CallMethod GetItemCount player ::temp206 ::temp205       ;@line 1823
						Assign availableAmmo ::temp206                           ;@line 1823
						Not ::temp202 operating                                  ;@line 1824
						Cast ::temp202 ::temp202                                 ;@line 1824
						JumpT ::temp202 _label321                                ;@line 1824
						CompareEQ ::temp203 generation expectedGeneration        ;@line 1824
						Not ::temp203 ::temp203                                  ;@line 1824
						Cast ::temp202 ::temp203                                 ;@line 1824
					_label321:
						Cast ::temp202 ::temp202                                 ;@line 1824
						JumpT ::temp202 _label322                                ;@line 1824
						CompareEQ ::temp203 token committedToken                 ;@line 1824
						Not ::temp203 ::temp203                                  ;@line 1824
						Cast ::temp202 ::temp203                                 ;@line 1824
					_label322:
						JumpF ::temp202 _label323                                ;@line 1824
						Return None                                              ;@line 1825
						Jump _label323                                           ;@line 1825
					_label323:
						CompareLT ::temp203 availableAmmo 1                      ;@line 1827
						JumpF ::temp203 _label324                                ;@line 1827
						CallMethod RejectShot self ::NoneVar "SHOT_NO_STEEL_BOLT: antes del lanzamiento."  ;@line 1828
						CallMethod EndSession self ::NoneVar                     ;@line 1829
						Return None                                              ;@line 1830
						Jump _label324                                           ;@line 1830
					_label324:
						CallMethod ShotTransformReady self ::temp202             ;@line 1832
						Assign commitTransformReady ::temp202                    ;@line 1832
						Not ::temp203 operating                                  ;@line 1833
						Cast ::temp203 ::temp203                                 ;@line 1833
						JumpT ::temp203 _label325                                ;@line 1833
						CompareEQ ::temp202 generation expectedGeneration        ;@line 1833
						Not ::temp202 ::temp202                                  ;@line 1833
						Cast ::temp203 ::temp202                                 ;@line 1833
					_label325:
						Cast ::temp203 ::temp203                                 ;@line 1833
						JumpT ::temp203 _label326                                ;@line 1833
						CompareEQ ::temp202 token committedToken                 ;@line 1833
						Not ::temp202 ::temp202                                  ;@line 1833
						Cast ::temp203 ::temp202                                 ;@line 1833
					_label326:
						JumpF ::temp203 _label327                                ;@line 1833
						Return None                                              ;@line 1834
						Jump _label327                                           ;@line 1834
					_label327:
						Not ::temp202 commitTransformReady                       ;@line 1836
						JumpF ::temp202 _label328                                ;@line 1836
						CallMethod RejectShot self ::NoneVar shotFailure         ;@line 1837
						CallMethod EndSession self ::NoneVar                     ;@line 1838
						Return None                                              ;@line 1839
						Jump _label328                                           ;@line 1839
					_label328:
						Not ::temp203 operating                                  ;@line 1843
						Cast ::temp203 ::temp203                                 ;@line 1843
						JumpT ::temp203 _label329                                ;@line 1843
						CompareEQ ::temp202 generation expectedGeneration        ;@line 1843
						Not ::temp202 ::temp202                                  ;@line 1843
						Cast ::temp203 ::temp202                                 ;@line 1843
					_label329:
						Cast ::temp203 ::temp203                                 ;@line 1843
						JumpT ::temp203 _label330                                ;@line 1843
						CompareEQ ::temp202 shotGeneration expectedGeneration    ;@line 1843
						Not ::temp202 ::temp202                                  ;@line 1843
						Cast ::temp203 ::temp202                                 ;@line 1843
					_label330:
						Cast ::temp203 ::temp203                                 ;@line 1843
						JumpT ::temp203 _label331                                ;@line 1843
						CompareEQ ::temp202 phase 2                              ;@line 1843
						Not ::temp202 ::temp202                                  ;@line 1843
						Cast ::temp203 ::temp202                                 ;@line 1843
					_label331:
						Cast ::temp202 ::temp203                                 ;@line 1843
						JumpT ::temp202 _label332                                ;@line 1843
						Cast ::temp202 shotCommitted                             ;@line 1843
					_label332:
						Cast ::temp203 ::temp202                                 ;@line 1843
						JumpT ::temp203 _label333                                ;@line 1843
						Cast ::temp203 inputPaused                               ;@line 1843
					_label333:
						Cast ::temp202 ::temp203                                 ;@line 1843
						JumpT ::temp202 _label334                                ;@line 1843
						Cast ::temp202 menuWasOpen                               ;@line 1843
					_label334:
						JumpF ::temp202 _label335                                ;@line 1843
						CallMethod RejectShot self ::NoneVar "SHOT_STALE_AFTER_PREFLIGHT: el disparo se cancelÃ³ durante la comprobaciÃ³n."  ;@line 1844
						Return None                                              ;@line 1845
						Jump _label335                                           ;@line 1845
					_label335:
						Assign shotCommitted True                                ;@line 1849
						Cast ::temp205 ::SteelBolt_var                           ;@line 1850
						CallMethod RemoveItem player ::NoneVar ::temp205 1 True None  ;@line 1850
						Cast ::temp207 self                                      ;@line 1851
						CallMethod Fire ::Launcher_var ::NoneVar ::temp207 ::ShotAmmo_var  ;@line 1851
						Cast ::temp202 operating                                 ;@line 1852
						JumpF ::temp202 _label336                                ;@line 1852
						CompareEQ ::temp203 token committedToken                 ;@line 1852
						Cast ::temp202 ::temp203                                 ;@line 1852
					_label336:
						Cast ::temp202 ::temp202                                 ;@line 1852
						JumpF ::temp202 _label337                                ;@line 1852
						CompareEQ ::temp203 generation expectedGeneration        ;@line 1852
						Cast ::temp202 ::temp203                                 ;@line 1852
					_label337:
						Cast ::temp202 ::temp202                                 ;@line 1852
						JumpF ::temp202 _label338                                ;@line 1852
						CompareEQ ::temp203 phase 2                              ;@line 1852
						Cast ::temp202 ::temp203                                 ;@line 1852
					_label338:
						Cast ::temp203 ::temp202                                 ;@line 1852
						JumpF ::temp203 _label339                                ;@line 1852
						Cast ::temp203 shotCommitted                             ;@line 1852
					_label339:
						JumpF ::temp203 _label340                                ;@line 1852
						CallMethod ThawSight self ::NoneVar expectedGeneration committedToken  ;@line 1853
						Jump _label340                                           ;@line 1853
					_label340:
						Cast ::temp203 operating                                 ;@line 1856
						JumpF ::temp203 _label341                                ;@line 1856
						CompareEQ ::temp202 generation expectedGeneration        ;@line 1856
						Cast ::temp203 ::temp202                                 ;@line 1856
					_label341:
						Cast ::temp203 ::temp203                                 ;@line 1856
						JumpF ::temp203 _label342                                ;@line 1856
						CompareEQ ::temp202 phase 2                              ;@line 1856
						Cast ::temp203 ::temp202                                 ;@line 1856
					_label342:
						JumpF ::temp203 _label343                                ;@line 1856
						Cast ::temp207 self                                      ;@line 1857
						CallStatic netimmerse SetNodeScale ::NoneVar ::temp207 ::VisualBoltNode_var 0.000000 False  ;@line 1857
						Jump _label343                                           ;@line 1857
					_label343:
						JumpF ::ShotSound_var _label344                          ;@line 1862
						Cast ::temp207 self                                      ;@line 1863
						CallMethod Play ::ShotSound_var ::temp206 ::temp207      ;@line 1863
						Jump _label344                                           ;@line 1863
					_label344:
						Cast ::temp203 ::QALog_var                               ;@line 1865
						JumpF ::temp203 _label345                                ;@line 1865
						Not ::temp202 ::UseSightCamera_var                       ;@line 1865
						Cast ::temp203 ::temp202                                 ;@line 1865
					_label345:
						JumpF ::temp203 _label346                                ;@line 1865
						Cast ::temp204 yaw                                       ;@line 1866
						StrCat ::temp204 "AstraAsedio Fire committed yaw=" ::temp204  ;@line 1866
						StrCat ::temp204 ::temp204 " pitch="                     ;@line 1866
						Cast ::temp208 pitch                                     ;@line 1866
						StrCat ::temp208 ::temp204 ::temp208                     ;@line 1866
						StrCat ::temp204 ::temp208 " generation="                ;@line 1866
						Cast ::temp208 generation                                ;@line 1866
						StrCat ::temp208 ::temp204 ::temp208                     ;@line 1866
						StrCat ::temp204 ::temp208 " muzzle="                    ;@line 1866
						ArrayGetElement ::temp209 muzzlePosition 0               ;@line 1866
						Cast ::temp208 ::temp209                                 ;@line 1866
						StrCat ::temp208 ::temp204 ::temp208                     ;@line 1866
						StrCat ::temp204 ::temp208 ","                           ;@line 1866
						ArrayGetElement ::temp209 muzzlePosition 1               ;@line 1866
						Cast ::temp208 ::temp209                                 ;@line 1866
						StrCat ::temp208 ::temp204 ::temp208                     ;@line 1866
						StrCat ::temp204 ::temp208 ","                           ;@line 1866
						ArrayGetElement ::temp209 muzzlePosition 2               ;@line 1866
						Cast ::temp208 ::temp209                                 ;@line 1866
						StrCat ::temp208 ::temp204 ::temp208                     ;@line 1866
						StrCat ::temp204 ::temp208 " forward="                   ;@line 1866
						ArrayGetElement ::temp209 muzzleWorldMatrix 1            ;@line 1866
						Cast ::temp208 ::temp209                                 ;@line 1866
						StrCat ::temp208 ::temp204 ::temp208                     ;@line 1866
						StrCat ::temp204 ::temp208 ","                           ;@line 1866
						ArrayGetElement ::temp209 muzzleWorldMatrix 4            ;@line 1866
						Cast ::temp208 ::temp209                                 ;@line 1866
						StrCat ::temp208 ::temp204 ::temp208                     ;@line 1866
						StrCat ::temp204 ::temp208 ","                           ;@line 1866
						ArrayGetElement ::temp209 muzzleWorldMatrix 7            ;@line 1866
						Cast ::temp208 ::temp209                                 ;@line 1866
						StrCat ::temp208 ::temp204 ::temp208                     ;@line 1866
						CallStatic debug Trace ::NoneVar ::temp208 0             ;@line 1866
						Jump _label346                                           ;@line 1866
					_label346:
					.endCode
				.endFunction
				.function ShotTransformReady
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
					.localTable
						.local ::temp194 Bool
						.local ::temp200 Float
						.local ::temp192 ObjectReference
						.local ::temp193 Bool
						.local i Int
						.local ::temp195 Float
						.local ::temp196 Float
						.local ::temp197 Bool
						.local ::temp199 Int
						.local ::temp198 String
						.local yc Float
						.local ys Float
						.local pc Float
						.local ps Float
						.local lx Float
						.local ly Float
						.local lz Float
						.local ex Float
						.local ey Float
						.local ez Float
						.local directionDot Float
						.local directionLength Float
						.local ::temp201 String
						.local rootScale Float
						.local dx Float
						.local dy Float
						.local dz Float
						.local positionError Float
					.endLocalTable
					.code
						Assign shotFailure ""                                    ;@line 1725
						JumpF ::UseSightCamera_var _label347                     ;@line 1726
						Cast ::temp192 self                                      ;@line 1728
						CallStatic astrasightnative ValidateShot ::temp193 ::temp192 token yaw pitch ::PitchPivotHeight_var  ;@line 1728
						Not ::temp193 ::temp193                                  ;@line 1728
						JumpF ::temp193 _label348                                ;@line 1728
						Assign shotFailure "SHOT_NATIVE_PREFLIGHT_FAILED: pose congelada o boca no vÃ¡lida."  ;@line 1729
						Return False                                             ;@line 1730
						Jump _label348                                           ;@line 1730
					_label348:
						Return True                                              ;@line 1732
						Jump _label347                                           ;@line 1732
					_label347:
						Cast ::temp192 self                                      ;@line 1736
						CallStatic netimmerse GetNodeWorldRotationMatrix ::temp193 ::temp192 "" rootWorldMatrix False  ;@line 1736
						Not ::temp193 ::temp193                                  ;@line 1736
						Cast ::temp193 ::temp193                                 ;@line 1736
						JumpT ::temp193 _label349                                ;@line 1736
						Cast ::temp192 self                                      ;@line 1736
						CallStatic netimmerse GetNodeWorldRotationMatrix ::temp194 ::temp192 "ProjectileNode" muzzleWorldMatrix False  ;@line 1736
						Not ::temp194 ::temp194                                  ;@line 1736
						Cast ::temp193 ::temp194                                 ;@line 1736
					_label349:
						JumpF ::temp193 _label350                                ;@line 1736
						Assign shotFailure "SHOT_MATRIX_READ_FAILED: raÃ­z o ProjectileNode."  ;@line 1737
						Return False                                             ;@line 1738
						Jump _label350                                           ;@line 1738
					_label350:
						Cast ::temp192 self                                      ;@line 1740
						CallStatic netimmerse GetNodeWorldPosition ::temp194 ::temp192 "" rootPosition False  ;@line 1740
						Not ::temp193 ::temp194                                  ;@line 1740
						Cast ::temp193 ::temp193                                 ;@line 1740
						JumpT ::temp193 _label351                                ;@line 1740
						Cast ::temp192 self                                      ;@line 1740
						CallStatic netimmerse GetNodeWorldPosition ::temp194 ::temp192 "ProjectileNode" muzzlePosition False  ;@line 1740
						Not ::temp194 ::temp194                                  ;@line 1740
						Cast ::temp193 ::temp194                                 ;@line 1740
					_label351:
						JumpF ::temp193 _label352                                ;@line 1740
						Assign shotFailure "SHOT_POSITION_READ_FAILED: raÃ­z o ProjectileNode."  ;@line 1741
						Return False                                             ;@line 1742
						Jump _label352                                           ;@line 1742
					_label352:
						Assign i 0                                               ;@line 1744
					_label358:
						CompareLT ::temp194 i 9                                  ;@line 1745
						JumpF ::temp194 _label353                                ;@line 1745
						ArrayGetElement ::temp195 rootWorldMatrix i              ;@line 1746
						ArrayGetElement ::temp196 rootWorldMatrix i              ;@line 1746
						CompareEQ ::temp193 ::temp195 ::temp196                  ;@line 1746
						Not ::temp193 ::temp193                                  ;@line 1746
						Cast ::temp193 ::temp193                                 ;@line 1746
						JumpT ::temp193 _label354                                ;@line 1746
						ArrayGetElement ::temp195 muzzleWorldMatrix i            ;@line 1746
						ArrayGetElement ::temp196 muzzleWorldMatrix i            ;@line 1746
						CompareEQ ::temp197 ::temp195 ::temp196                  ;@line 1746
						Not ::temp197 ::temp197                                  ;@line 1746
						Cast ::temp193 ::temp197                                 ;@line 1746
					_label354:
						Cast ::temp193 ::temp193                                 ;@line 1746
						JumpT ::temp193 _label355                                ;@line 1746
						ArrayGetElement ::temp195 rootWorldMatrix i              ;@line 1746
						CallStatic math Abs ::temp196 ::temp195                  ;@line 1746
						CompareGT ::temp197 ::temp196 1.050000                   ;@line 1746
						Cast ::temp193 ::temp197                                 ;@line 1746
					_label355:
						Cast ::temp193 ::temp193                                 ;@line 1746
						JumpT ::temp193 _label356                                ;@line 1746
						ArrayGetElement ::temp195 muzzleWorldMatrix i            ;@line 1746
						CallStatic math Abs ::temp196 ::temp195                  ;@line 1746
						CompareGT ::temp197 ::temp196 1.050000                   ;@line 1746
						Cast ::temp193 ::temp197                                 ;@line 1746
					_label356:
						JumpF ::temp193 _label357                                ;@line 1746
						Cast ::temp198 i                                         ;@line 1747
						StrCat ::temp198 "SHOT_MATRIX_INVALID: Ã­ndice=" ::temp198  ;@line 1747
						Assign shotFailure ::temp198                             ;@line 1747
						Return False                                             ;@line 1748
						Jump _label357                                           ;@line 1748
					_label357:
						IAdd ::temp199 i 1                                       ;@line 1750
						Assign i ::temp199                                       ;@line 1750
						Jump _label358                                           ;@line 1750
					_label353:
						Assign i 0                                               ;@line 1752
					_label364:
						CompareLT ::temp197 i 3                                  ;@line 1753
						JumpF ::temp197 _label359                                ;@line 1753
						ArrayGetElement ::temp195 rootPosition i                 ;@line 1754
						ArrayGetElement ::temp196 rootPosition i                 ;@line 1754
						CompareEQ ::temp193 ::temp195 ::temp196                  ;@line 1754
						Not ::temp193 ::temp193                                  ;@line 1754
						Cast ::temp193 ::temp193                                 ;@line 1754
						JumpT ::temp193 _label360                                ;@line 1754
						ArrayGetElement ::temp195 muzzlePosition i               ;@line 1754
						ArrayGetElement ::temp196 muzzlePosition i               ;@line 1754
						CompareEQ ::temp194 ::temp195 ::temp196                  ;@line 1754
						Not ::temp194 ::temp194                                  ;@line 1754
						Cast ::temp193 ::temp194                                 ;@line 1754
					_label360:
						Cast ::temp193 ::temp193                                 ;@line 1754
						JumpT ::temp193 _label361                                ;@line 1754
						ArrayGetElement ::temp195 rootPosition i                 ;@line 1754
						CallStatic math Abs ::temp196 ::temp195                  ;@line 1754
						CompareGT ::temp194 ::temp196 1000000.000000             ;@line 1754
						Cast ::temp193 ::temp194                                 ;@line 1754
					_label361:
						Cast ::temp193 ::temp193                                 ;@line 1754
						JumpT ::temp193 _label362                                ;@line 1754
						ArrayGetElement ::temp195 muzzlePosition i               ;@line 1754
						CallStatic math Abs ::temp196 ::temp195                  ;@line 1754
						CompareGT ::temp194 ::temp196 1000000.000000             ;@line 1754
						Cast ::temp193 ::temp194                                 ;@line 1754
					_label362:
						JumpF ::temp193 _label363                                ;@line 1754
						Cast ::temp198 i                                         ;@line 1755
						StrCat ::temp198 "SHOT_POSITION_INVALID: Ã­ndice=" ::temp198  ;@line 1755
						Assign shotFailure ::temp198                             ;@line 1755
						Return False                                             ;@line 1756
						Jump _label363                                           ;@line 1756
					_label363:
						IAdd ::temp199 i 1                                       ;@line 1758
						Assign i ::temp199                                       ;@line 1758
						Jump _label364                                           ;@line 1758
					_label359:
						CallStatic math Cos ::temp195 yaw                        ;@line 1760
						Assign yc ::temp195                                      ;@line 1760
						CallStatic math Sin ::temp196 yaw                        ;@line 1761
						Assign ys ::temp196                                      ;@line 1761
						CallStatic math Cos ::temp195 pitch                      ;@line 1762
						Assign pc ::temp195                                      ;@line 1762
						CallStatic math Sin ::temp196 pitch                      ;@line 1763
						Assign ps ::temp196                                      ;@line 1763
						FMultiply ::temp195 ys pc                                ;@line 1764
						Assign lx ::temp195                                      ;@line 1764
						FNegate ::temp196 yc                                     ;@line 1765
						FMultiply ::temp195 ::temp196 pc                         ;@line 1765
						Assign ly ::temp195                                      ;@line 1765
						Assign lz ps                                             ;@line 1766
						ArrayGetElement ::temp196 rootWorldMatrix 0              ;@line 1767
						FMultiply ::temp195 ::temp196 lx                         ;@line 1767
						ArrayGetElement ::temp196 rootWorldMatrix 1              ;@line 1767
						FMultiply ::temp196 ::temp196 ly                         ;@line 1767
						FAdd ::temp195 ::temp195 ::temp196                       ;@line 1767
						ArrayGetElement ::temp196 rootWorldMatrix 2              ;@line 1767
						FMultiply ::temp196 ::temp196 lz                         ;@line 1767
						FAdd ::temp195 ::temp195 ::temp196                       ;@line 1767
						Assign ex ::temp195                                      ;@line 1767
						ArrayGetElement ::temp196 rootWorldMatrix 3              ;@line 1768
						FMultiply ::temp195 ::temp196 lx                         ;@line 1768
						ArrayGetElement ::temp196 rootWorldMatrix 4              ;@line 1768
						FMultiply ::temp196 ::temp196 ly                         ;@line 1768
						FAdd ::temp195 ::temp195 ::temp196                       ;@line 1768
						ArrayGetElement ::temp196 rootWorldMatrix 5              ;@line 1768
						FMultiply ::temp196 ::temp196 lz                         ;@line 1768
						FAdd ::temp195 ::temp195 ::temp196                       ;@line 1768
						Assign ey ::temp195                                      ;@line 1768
						ArrayGetElement ::temp196 rootWorldMatrix 6              ;@line 1769
						FMultiply ::temp195 ::temp196 lx                         ;@line 1769
						ArrayGetElement ::temp196 rootWorldMatrix 7              ;@line 1769
						FMultiply ::temp196 ::temp196 ly                         ;@line 1769
						FAdd ::temp195 ::temp195 ::temp196                       ;@line 1769
						ArrayGetElement ::temp196 rootWorldMatrix 8              ;@line 1769
						FMultiply ::temp196 ::temp196 lz                         ;@line 1769
						FAdd ::temp195 ::temp195 ::temp196                       ;@line 1769
						Assign ez ::temp195                                      ;@line 1769
						ArrayGetElement ::temp196 muzzleWorldMatrix 1            ;@line 1770
						FMultiply ::temp195 ex ::temp196                         ;@line 1770
						ArrayGetElement ::temp196 muzzleWorldMatrix 4            ;@line 1770
						FMultiply ::temp196 ey ::temp196                         ;@line 1770
						FAdd ::temp195 ::temp195 ::temp196                       ;@line 1770
						ArrayGetElement ::temp196 muzzleWorldMatrix 7            ;@line 1770
						FMultiply ::temp196 ez ::temp196                         ;@line 1770
						FAdd ::temp195 ::temp195 ::temp196                       ;@line 1770
						Assign directionDot ::temp195                            ;@line 1770
						ArrayGetElement ::temp196 muzzleWorldMatrix 1            ;@line 1771
						ArrayGetElement ::temp195 muzzleWorldMatrix 1            ;@line 1771
						FMultiply ::temp196 ::temp196 ::temp195                  ;@line 1771
						ArrayGetElement ::temp195 muzzleWorldMatrix 4            ;@line 1771
						ArrayGetElement ::temp200 muzzleWorldMatrix 4            ;@line 1771
						FMultiply ::temp195 ::temp195 ::temp200                  ;@line 1771
						FAdd ::temp200 ::temp196 ::temp195                       ;@line 1771
						ArrayGetElement ::temp196 muzzleWorldMatrix 7            ;@line 1771
						ArrayGetElement ::temp195 muzzleWorldMatrix 7            ;@line 1771
						FMultiply ::temp196 ::temp196 ::temp195                  ;@line 1771
						FAdd ::temp195 ::temp200 ::temp196                       ;@line 1771
						Assign directionLength ::temp195                         ;@line 1771
						CompareLT ::temp194 directionDot 0.999000                ;@line 1772
						Cast ::temp197 ::temp194                                 ;@line 1772
						JumpT ::temp197 _label365                                ;@line 1772
						FSubtract ::temp200 directionLength 1.000000             ;@line 1772
						CallStatic math Abs ::temp196 ::temp200                  ;@line 1772
						CompareGT ::temp193 ::temp196 0.002000                   ;@line 1772
						Cast ::temp197 ::temp193                                 ;@line 1772
					_label365:
						JumpF ::temp197 _label366                                ;@line 1772
						Cast ::temp198 directionDot                              ;@line 1773
						StrCat ::temp198 "SHOT_DIRECTION_MISMATCH: dot=" ::temp198  ;@line 1773
						StrCat ::temp198 ::temp198 " length="                    ;@line 1773
						Cast ::temp201 directionLength                           ;@line 1773
						StrCat ::temp201 ::temp198 ::temp201                     ;@line 1773
						StrCat ::temp198 ::temp201 " yaw="                       ;@line 1773
						Cast ::temp201 yaw                                       ;@line 1773
						StrCat ::temp201 ::temp198 ::temp201                     ;@line 1773
						StrCat ::temp198 ::temp201 " pitch="                     ;@line 1773
						Cast ::temp201 pitch                                     ;@line 1773
						StrCat ::temp201 ::temp198 ::temp201                     ;@line 1773
						Assign shotFailure ::temp201                             ;@line 1773
						Return False                                             ;@line 1774
						Jump _label366                                           ;@line 1774
					_label366:
						FMultiply ::temp195 -224.000000 pc                       ;@line 1778
						FMultiply ::temp200 19.600000 ps                         ;@line 1778
						FAdd ::temp196 ::temp195 ::temp200                       ;@line 1778
						Assign ly ::temp196                                      ;@line 1778
						FNegate ::temp195 ly                                     ;@line 1779
						FMultiply ::temp200 ::temp195 ys                         ;@line 1779
						Assign lx ::temp200                                      ;@line 1779
						FMultiply ::temp196 224.000000 ps                        ;@line 1780
						FAdd ::temp195 ::PitchPivotHeight_var ::temp196          ;@line 1780
						FMultiply ::temp200 19.600000 pc                         ;@line 1780
						FAdd ::temp196 ::temp195 ::temp200                       ;@line 1780
						Assign lz ::temp196                                      ;@line 1780
						FMultiply ::temp195 ly yc                                ;@line 1781
						Assign ly ::temp195                                      ;@line 1781
						Cast ::temp192 self                                      ;@line 1782
						CallStatic netimmerse GetNodeScale ::temp200 ::temp192 "" False  ;@line 1782
						Assign rootScale ::temp200                               ;@line 1782
						CompareEQ ::temp194 rootScale rootScale                  ;@line 1783
						Not ::temp194 ::temp194                                  ;@line 1783
						Cast ::temp197 ::temp194                                 ;@line 1783
						JumpT ::temp197 _label367                                ;@line 1783
						CompareLTE ::temp193 rootScale 0.000000                  ;@line 1783
						Cast ::temp197 ::temp193                                 ;@line 1783
					_label367:
						Cast ::temp193 ::temp197                                 ;@line 1783
						JumpT ::temp193 _label368                                ;@line 1783
						CompareGT ::temp194 rootScale 100.000000                 ;@line 1783
						Cast ::temp193 ::temp194                                 ;@line 1783
					_label368:
						JumpF ::temp193 _label369                                ;@line 1783
						Cast ::temp198 rootScale                                 ;@line 1784
						StrCat ::temp201 "SHOT_ROOT_SCALE_INVALID: scale=" ::temp198  ;@line 1784
						Assign shotFailure ::temp201                             ;@line 1784
						Return False                                             ;@line 1785
						Jump _label369                                           ;@line 1785
					_label369:
						ArrayGetElement ::temp196 rootPosition 0                 ;@line 1787
						ArrayGetElement ::temp195 rootWorldMatrix 0              ;@line 1787
						FMultiply ::temp200 ::temp195 lx                         ;@line 1787
						ArrayGetElement ::temp195 rootWorldMatrix 1              ;@line 1787
						FMultiply ::temp195 ::temp195 ly                         ;@line 1787
						FAdd ::temp200 ::temp200 ::temp195                       ;@line 1787
						ArrayGetElement ::temp195 rootWorldMatrix 2              ;@line 1787
						FMultiply ::temp195 ::temp195 lz                         ;@line 1787
						FAdd ::temp200 ::temp200 ::temp195                       ;@line 1787
						FMultiply ::temp195 rootScale ::temp200                  ;@line 1787
						FAdd ::temp200 ::temp196 ::temp195                       ;@line 1787
						Assign ex ::temp200                                      ;@line 1787
						ArrayGetElement ::temp196 rootPosition 1                 ;@line 1788
						ArrayGetElement ::temp195 rootWorldMatrix 3              ;@line 1788
						FMultiply ::temp200 ::temp195 lx                         ;@line 1788
						ArrayGetElement ::temp195 rootWorldMatrix 4              ;@line 1788
						FMultiply ::temp195 ::temp195 ly                         ;@line 1788
						FAdd ::temp200 ::temp200 ::temp195                       ;@line 1788
						ArrayGetElement ::temp195 rootWorldMatrix 5              ;@line 1788
						FMultiply ::temp195 ::temp195 lz                         ;@line 1788
						FAdd ::temp200 ::temp200 ::temp195                       ;@line 1788
						FMultiply ::temp195 rootScale ::temp200                  ;@line 1788
						FAdd ::temp200 ::temp196 ::temp195                       ;@line 1788
						Assign ey ::temp200                                      ;@line 1788
						ArrayGetElement ::temp196 rootPosition 2                 ;@line 1789
						ArrayGetElement ::temp195 rootWorldMatrix 6              ;@line 1789
						FMultiply ::temp200 ::temp195 lx                         ;@line 1789
						ArrayGetElement ::temp195 rootWorldMatrix 7              ;@line 1789
						FMultiply ::temp195 ::temp195 ly                         ;@line 1789
						FAdd ::temp200 ::temp200 ::temp195                       ;@line 1789
						ArrayGetElement ::temp195 rootWorldMatrix 8              ;@line 1789
						FMultiply ::temp195 ::temp195 lz                         ;@line 1789
						FAdd ::temp200 ::temp200 ::temp195                       ;@line 1789
						FMultiply ::temp195 rootScale ::temp200                  ;@line 1789
						FAdd ::temp200 ::temp196 ::temp195                       ;@line 1789
						Assign ez ::temp200                                      ;@line 1789
						ArrayGetElement ::temp196 muzzlePosition 0               ;@line 1790
						FSubtract ::temp195 ex ::temp196                         ;@line 1790
						Assign dx ::temp195                                      ;@line 1790
						ArrayGetElement ::temp200 muzzlePosition 1               ;@line 1791
						FSubtract ::temp196 ey ::temp200                         ;@line 1791
						Assign dy ::temp196                                      ;@line 1791
						ArrayGetElement ::temp195 muzzlePosition 2               ;@line 1792
						FSubtract ::temp200 ez ::temp195                         ;@line 1792
						Assign dz ::temp200                                      ;@line 1792
						FMultiply ::temp196 dx dx                                ;@line 1793
						FMultiply ::temp195 dy dy                                ;@line 1793
						FAdd ::temp200 ::temp196 ::temp195                       ;@line 1793
						FMultiply ::temp196 dz dz                                ;@line 1793
						FAdd ::temp195 ::temp200 ::temp196                       ;@line 1793
						Assign positionError ::temp195                           ;@line 1793
						CompareGT ::temp197 positionError 4.000000               ;@line 1794
						JumpF ::temp197 _label370                                ;@line 1794
						Cast ::temp198 positionError                             ;@line 1795
						StrCat ::temp201 "SHOT_POSITION_MISMATCH: squaredError=" ::temp198  ;@line 1795
						StrCat ::temp198 ::temp201 " dx="                        ;@line 1795
						Cast ::temp201 dx                                        ;@line 1795
						StrCat ::temp201 ::temp198 ::temp201                     ;@line 1795
						StrCat ::temp198 ::temp201 " dy="                        ;@line 1795
						Cast ::temp201 dy                                        ;@line 1795
						StrCat ::temp201 ::temp198 ::temp201                     ;@line 1795
						StrCat ::temp198 ::temp201 " dz="                        ;@line 1795
						Cast ::temp201 dz                                        ;@line 1795
						StrCat ::temp201 ::temp198 ::temp201                     ;@line 1795
						Assign shotFailure ::temp201                             ;@line 1795
						Return False                                             ;@line 1796
						Jump _label370                                           ;@line 1796
					_label370:
						Return True                                              ;@line 1798
					.endCode
				.endFunction
				.function InputReady
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
					.localTable
						.local ::temp33 Bool
						.local ::temp34 Bool
						.local inputGeneration Int
						.local inputToken Int
						.local inputMenuOpen Bool
						.local ::NoneVar None
						.local resumedMenuOpen Bool
					.endLocalTable
					.code
						Assign inputGeneration generation                        ;@line 465
						Assign inputToken token                                  ;@line 466
						Not ::temp33 operating                                   ;@line 467
						Cast ::temp33 ::temp33                                   ;@line 467
						JumpT ::temp33 _label371                                 ;@line 467
						Cast ::temp33 cameraEntryPending                         ;@line 467
					_label371:
						JumpF ::temp33 _label372                                 ;@line 467
						Return False                                             ;@line 468
						Jump _label372                                           ;@line 468
					_label372:
						CallStatic utility IsInMenuMode ::temp33                 ;@line 470
						Assign inputMenuOpen ::temp33                            ;@line 470
						Not ::temp33 operating                                   ;@line 471
						Cast ::temp33 ::temp33                                   ;@line 471
						JumpT ::temp33 _label373                                 ;@line 471
						Cast ::temp33 cameraEntryPending                         ;@line 471
					_label373:
						Cast ::temp33 ::temp33                                   ;@line 471
						JumpT ::temp33 _label374                                 ;@line 471
						CompareEQ ::temp34 generation inputGeneration            ;@line 471
						Not ::temp34 ::temp34                                    ;@line 471
						Cast ::temp33 ::temp34                                   ;@line 471
					_label374:
						Cast ::temp33 ::temp33                                   ;@line 471
						JumpT ::temp33 _label375                                 ;@line 471
						CompareEQ ::temp34 token inputToken                      ;@line 471
						Not ::temp34 ::temp34                                    ;@line 471
						Cast ::temp33 ::temp34                                   ;@line 471
					_label375:
						Cast ::temp34 ::temp33                                   ;@line 471
						JumpT ::temp34 _label376                                 ;@line 471
						Cast ::temp34 inputMenuOpen                              ;@line 471
					_label376:
						JumpF ::temp34 _label377                                 ;@line 471
						Return False                                             ;@line 472
						Jump _label377                                           ;@line 472
					_label377:
						Cast ::temp33 inputPaused                                ;@line 476
						JumpT ::temp33 _label378                                 ;@line 476
						Cast ::temp33 menuWasOpen                                ;@line 476
					_label378:
						JumpF ::temp33 _label379                                 ;@line 476
						CallMethod ResumeInput self ::NoneVar                    ;@line 477
						Jump _label379                                           ;@line 477
					_label379:
						CallStatic utility IsInMenuMode ::temp34                 ;@line 479
						Assign resumedMenuOpen ::temp34                          ;@line 479
						Cast ::temp34 operating                                  ;@line 480
						JumpF ::temp34 _label380                                 ;@line 480
						Not ::temp33 cameraEntryPending                          ;@line 480
						Cast ::temp34 ::temp33                                   ;@line 480
					_label380:
						Cast ::temp34 ::temp34                                   ;@line 480
						JumpF ::temp34 _label381                                 ;@line 480
						CompareEQ ::temp33 generation inputGeneration            ;@line 480
						Cast ::temp34 ::temp33                                   ;@line 480
					_label381:
						Cast ::temp34 ::temp34                                   ;@line 480
						JumpF ::temp34 _label382                                 ;@line 480
						CompareEQ ::temp33 token inputToken                      ;@line 480
						Cast ::temp34 ::temp33                                   ;@line 480
					_label382:
						Cast ::temp34 ::temp34                                   ;@line 480
						JumpF ::temp34 _label383                                 ;@line 480
						Not ::temp33 inputPaused                                 ;@line 480
						Cast ::temp34 ::temp33                                   ;@line 480
					_label383:
						Cast ::temp34 ::temp34                                   ;@line 480
						JumpF ::temp34 _label384                                 ;@line 480
						Not ::temp33 menuWasOpen                                 ;@line 480
						Cast ::temp34 ::temp33                                   ;@line 480
					_label384:
						Cast ::temp34 ::temp34                                   ;@line 480
						JumpF ::temp34 _label385                                 ;@line 480
						Not ::temp33 resumedMenuOpen                             ;@line 480
						Cast ::temp34 ::temp33                                   ;@line 480
					_label385:
						Return ::temp34                                          ;@line 480
					.endCode
				.endFunction
				.function SetAimKey
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param keyCode Int
						.param isDown Bool
					.endParamTable
					.localTable
						.local ::temp44 Bool
						.local keyGeneration Int
						.local keyToken Int
						.local aimInputReady Bool
						.local ::temp45 Bool
						.local ::temp46 Bool
						.local ::temp47 Bool
					.endLocalTable
					.code
						Not ::temp44 operating                                   ;@line 576
						JumpF ::temp44 _label386                                 ;@line 576
						Return None                                              ;@line 577
						Jump _label386                                           ;@line 577
					_label386:
						Assign keyGeneration generation                          ;@line 579
						Assign keyToken token                                    ;@line 580
						Assign aimInputReady True                                ;@line 581
						JumpF isDown _label387                                   ;@line 582
						CallMethod InputReady self ::temp44                      ;@line 583
						Assign aimInputReady ::temp44                            ;@line 583
						Not ::temp44 operating                                   ;@line 584
						Cast ::temp44 ::temp44                                   ;@line 584
						JumpT ::temp44 _label388                                 ;@line 584
						CompareEQ ::temp45 generation keyGeneration              ;@line 584
						Not ::temp45 ::temp45                                    ;@line 584
						Cast ::temp44 ::temp45                                   ;@line 584
					_label388:
						Cast ::temp44 ::temp44                                   ;@line 584
						JumpT ::temp44 _label389                                 ;@line 584
						CompareEQ ::temp45 token keyToken                        ;@line 584
						Not ::temp45 ::temp45                                    ;@line 584
						Cast ::temp44 ::temp45                                   ;@line 584
					_label389:
						JumpF ::temp44 _label390                                 ;@line 584
						Return None                                              ;@line 585
						Jump _label390                                           ;@line 585
					_label390:
						Jump _label387                                           ;@line 585
					_label387:
						Cast ::temp44 isDown                                     ;@line 588
						JumpF ::temp44 _label391                                 ;@line 588
						Not ::temp45 aimInputReady                               ;@line 588
						Cast ::temp44 ::temp45                                   ;@line 588
					_label391:
						JumpF ::temp44 _label392                                 ;@line 588
						CompareEQ ::temp45 keyCode 203                           ;@line 589
						JumpF ::temp45 _label393                                 ;@line 589
						Assign releaseLeft True                                  ;@line 590
						Jump _label394                                           ;@line 590
					_label393:
						CompareEQ ::temp46 keyCode 205                           ;@line 591
						JumpF ::temp46 _label395                                 ;@line 591
						Assign releaseRight True                                 ;@line 592
						Jump _label394                                           ;@line 592
					_label395:
						CompareEQ ::temp46 keyCode 200                           ;@line 593
						JumpF ::temp46 _label396                                 ;@line 593
						Assign releaseUp True                                    ;@line 594
						Jump _label394                                           ;@line 594
					_label396:
						CompareEQ ::temp46 keyCode 208                           ;@line 595
						JumpF ::temp46 _label394                                 ;@line 595
						Assign releaseDown True                                  ;@line 596
						Jump _label394                                           ;@line 596
					_label394:
						Return None                                              ;@line 598
						Jump _label392                                           ;@line 598
					_label392:
						CompareEQ ::temp46 keyCode 203                           ;@line 600
						JumpF ::temp46 _label397                                 ;@line 600
						Not ::temp45 isDown                                      ;@line 601
						JumpF ::temp45 _label398                                 ;@line 601
						Assign heldLeft False                                    ;@line 602
						Assign releaseLeft False                                 ;@line 603
						Jump _label399                                           ;@line 603
					_label398:
						Not ::temp44 releaseLeft                                 ;@line 604
						JumpF ::temp44 _label399                                 ;@line 604
						Assign heldLeft True                                     ;@line 605
						Jump _label399                                           ;@line 605
					_label399:
						Jump _label400                                           ;@line 605
					_label397:
						CompareEQ ::temp44 keyCode 205                           ;@line 607
						JumpF ::temp44 _label401                                 ;@line 607
						Not ::temp45 isDown                                      ;@line 608
						JumpF ::temp45 _label402                                 ;@line 608
						Assign heldRight False                                   ;@line 609
						Assign releaseRight False                                ;@line 610
						Jump _label403                                           ;@line 610
					_label402:
						Not ::temp47 releaseRight                                ;@line 611
						JumpF ::temp47 _label403                                 ;@line 611
						Assign heldRight True                                    ;@line 612
						Jump _label403                                           ;@line 612
					_label403:
						Jump _label400                                           ;@line 612
					_label401:
						CompareEQ ::temp47 keyCode 200                           ;@line 614
						JumpF ::temp47 _label404                                 ;@line 614
						Not ::temp45 isDown                                      ;@line 615
						JumpF ::temp45 _label405                                 ;@line 615
						Assign heldUp False                                      ;@line 616
						Assign releaseUp False                                   ;@line 617
						Jump _label406                                           ;@line 617
					_label405:
						Not ::temp44 releaseUp                                   ;@line 618
						JumpF ::temp44 _label406                                 ;@line 618
						Assign heldUp True                                       ;@line 619
						Jump _label406                                           ;@line 619
					_label406:
						Jump _label400                                           ;@line 619
					_label404:
						CompareEQ ::temp44 keyCode 208                           ;@line 621
						JumpF ::temp44 _label400                                 ;@line 621
						Not ::temp45 isDown                                      ;@line 622
						JumpF ::temp45 _label407                                 ;@line 622
						Assign heldDown False                                    ;@line 623
						Assign releaseDown False                                 ;@line 624
						Jump _label408                                           ;@line 624
					_label407:
						Not ::temp47 releaseDown                                 ;@line 625
						JumpF ::temp47 _label408                                 ;@line 625
						Assign heldDown True                                     ;@line 626
						Jump _label408                                           ;@line 626
					_label408:
						Jump _label400                                           ;@line 626
					_label400:
					.endCode
				.endFunction
				.function PauseInput
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
						.local ::temp77 Bool
						.local ::temp78 Bool
						.local ::temp79 Float
						.local pauseToken Int
						.local pauseGeneration Int
						.local pausedAt Float
					.endLocalTable
					.code
						Assign pauseToken token                                  ;@line 767
						Assign inputPaused True                                  ;@line 768
						Assign menuWasOpen True                                  ;@line 769
						CallMethod ClearHeldInput self ::NoneVar True            ;@line 770
						CallMethod CancelPendingShot self ::NoneVar              ;@line 771
						Not ::temp77 operating                                   ;@line 772
						Cast ::temp77 ::temp77                                   ;@line 772
						JumpT ::temp77 _label409                                 ;@line 772
						CompareEQ ::temp78 token pauseToken                      ;@line 772
						Not ::temp78 ::temp78                                    ;@line 772
						Cast ::temp77 ::temp78                                   ;@line 772
					_label409:
						Cast ::temp77 ::temp77                                   ;@line 772
						JumpT ::temp77 _label410                                 ;@line 772
						Not ::temp78 inputPaused                                 ;@line 772
						Cast ::temp77 ::temp78                                   ;@line 772
					_label410:
						Cast ::temp77 ::temp77                                   ;@line 772
						JumpT ::temp77 _label411                                 ;@line 772
						Not ::temp78 menuWasOpen                                 ;@line 772
						Cast ::temp77 ::temp78                                   ;@line 772
					_label411:
						JumpF ::temp77 _label412                                 ;@line 772
						Return None                                              ;@line 773
						Jump _label412                                           ;@line 773
					_label412:
						Assign pauseGeneration generation                        ;@line 776
						CallStatic utility GetCurrentRealTime ::temp79           ;@line 777
						Assign pausedAt ::temp79                                 ;@line 777
						Not ::temp78 operating                                   ;@line 778
						Cast ::temp78 ::temp78                                   ;@line 778
						JumpT ::temp78 _label413                                 ;@line 778
						CompareEQ ::temp77 generation pauseGeneration            ;@line 778
						Not ::temp77 ::temp77                                    ;@line 778
						Cast ::temp78 ::temp77                                   ;@line 778
					_label413:
						Cast ::temp78 ::temp78                                   ;@line 778
						JumpT ::temp78 _label414                                 ;@line 778
						CompareEQ ::temp77 token pauseToken                      ;@line 778
						Not ::temp77 ::temp77                                    ;@line 778
						Cast ::temp78 ::temp77                                   ;@line 778
					_label414:
						Cast ::temp78 ::temp78                                   ;@line 778
						JumpT ::temp78 _label415                                 ;@line 778
						Not ::temp77 inputPaused                                 ;@line 778
						Cast ::temp78 ::temp77                                   ;@line 778
					_label415:
						Cast ::temp78 ::temp78                                   ;@line 778
						JumpT ::temp78 _label416                                 ;@line 778
						Not ::temp77 menuWasOpen                                 ;@line 778
						Cast ::temp78 ::temp77                                   ;@line 778
					_label416:
						JumpF ::temp78 _label417                                 ;@line 778
						Return None                                              ;@line 779
						Jump _label417                                           ;@line 779
					_label417:
						Assign lastTick pausedAt                                 ;@line 781
						FAdd ::temp79 pausedAt 3.000000                          ;@line 783
						Assign cameraGraceUntil ::temp79                         ;@line 783
					.endCode
				.endFunction
				.function RegisterMappedKey
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param keyCode Int
					.endParamTable
					.localTable
						.local ::temp31 Bool
						.local ::temp32 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CompareGTE ::temp31 keyCode 0                            ;@line 459
						Cast ::temp31 ::temp31                                   ;@line 459
						JumpF ::temp31 _label418                                 ;@line 459
						CompareEQ ::temp32 keyCode 255                           ;@line 459
						Not ::temp32 ::temp32                                    ;@line 459
						Cast ::temp31 ::temp32                                   ;@line 459
					_label418:
						Cast ::temp31 ::temp31                                   ;@line 459
						JumpF ::temp31 _label419                                 ;@line 459
						CompareLT ::temp32 keyCode 266                           ;@line 459
						Cast ::temp31 ::temp32                                   ;@line 459
					_label419:
						JumpF ::temp31 _label420                                 ;@line 459
						CallMethod RegisterForKey self ::NoneVar keyCode         ;@line 460
						Jump _label420                                           ;@line 460
					_label420:
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
				.function OnMenuOpen
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param menuName String
					.endParamTable
					.localTable
						.local ::temp85 String
						.local ::temp86 String
						.local ::NoneVar None
					.endLocalTable
					.code
						JumpF operating _label421                                ;@line 824
						JumpF cameraEntryPending _label422                       ;@line 825
						CallMethod EndSession self ::NoneVar                     ;@line 826
						Jump _label423                                           ;@line 826
					_label422:
						CallMethod PauseInput self ::NoneVar                     ;@line 828
					_label423:
						StrCat ::temp85 "AstraAsedio OnMenuOpen menu=" menuName  ;@line 830
						StrCat ::temp85 ::temp85 " generation="                  ;@line 830
						Cast ::temp86 generation                                 ;@line 830
						StrCat ::temp86 ::temp85 ::temp86                        ;@line 830
						CallStatic debug Trace ::NoneVar ::temp86 0              ;@line 830
						Jump _label421                                           ;@line 830
					_label421:
					.endCode
				.endFunction
				.function OnLoad
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp0 Bool
						.local ::NoneVar None
						.local ::temp1 Bool
						.local loadGeneration Int
						.local captured Bool
						.local ::temp2 ObjectReference
						.local ::temp3 String
					.endLocalTable
					.code
						CompareGT ::temp0 ::PitchMin_var -20.000000              ;@line 113
						JumpF ::temp0 _label424                                  ;@line 113
						Assign ::PitchMin_var -20.000000                         ;@line 114
						Jump _label424                                           ;@line 114
					_label424:
						CallMethod RecoverStationLoad self ::NoneVar             ;@line 116
						Cast ::temp0 operating                                   ;@line 119
						JumpT ::temp0 _label425                                  ;@line 119
						Cast ::temp0 nativeSightRequested                        ;@line 119
					_label425:
						JumpF ::temp0 _label426                                  ;@line 119
						CallMethod EndSession self ::NoneVar                     ;@line 120
						Jump _label426                                           ;@line 120
					_label426:
						Assign endingSession True                                ;@line 122
						Assign loadGeneration generation                         ;@line 123
						CallMethod NormalizeTimingProperties self ::NoneVar      ;@line 125
						CallMethod BlockActivation self ::NoneVar True           ;@line 126
						CallMethod CaptureMatrices self ::temp0                  ;@line 128
						Assign captured ::temp0                                  ;@line 128
						CompareEQ ::temp0 generation loadGeneration              ;@line 129
						Not ::temp0 ::temp0                                      ;@line 129
						Cast ::temp0 ::temp0                                     ;@line 129
						JumpT ::temp0 _label427                                  ;@line 129
						CompareEQ ::temp1 token -1                               ;@line 129
						Not ::temp1 ::temp1                                      ;@line 129
						Cast ::temp0 ::temp1                                     ;@line 129
					_label427:
						Cast ::temp1 ::temp0                                     ;@line 129
						JumpT ::temp1 _label428                                  ;@line 129
						Cast ::temp1 operating                                   ;@line 129
					_label428:
						JumpF ::temp1 _label429                                  ;@line 129
						Return None                                              ;@line 130
						Jump _label429                                           ;@line 130
					_label429:
						JumpF captured _label430                                 ;@line 132
						CallMethod ApplyAim self ::NoneVar                       ;@line 133
						CompareEQ ::temp0 generation loadGeneration              ;@line 134
						Not ::temp0 ::temp0                                      ;@line 134
						Cast ::temp0 ::temp0                                     ;@line 134
						JumpT ::temp0 _label431                                  ;@line 134
						CompareEQ ::temp1 token -1                               ;@line 134
						Not ::temp1 ::temp1                                      ;@line 134
						Cast ::temp0 ::temp1                                     ;@line 134
					_label431:
						Cast ::temp1 ::temp0                                     ;@line 134
						JumpT ::temp1 _label432                                  ;@line 134
						Cast ::temp1 operating                                   ;@line 134
					_label432:
						JumpF ::temp1 _label433                                  ;@line 134
						Return None                                              ;@line 135
						Jump _label433                                           ;@line 135
					_label433:
						Cast ::temp2 self                                        ;@line 137
						CallStatic netimmerse SetNodeScale ::NoneVar ::temp2 ::VisualBoltNode_var 1.000000 False  ;@line 137
						Jump _label434                                           ;@line 137
					_label430:
						StrCat ::temp3 "AstraAsedio OnLoad: " matrixFailure      ;@line 139
						CallStatic debug Trace ::NoneVar ::temp3 0               ;@line 139
					_label434:
						CompareEQ ::temp0 generation loadGeneration              ;@line 141
						Cast ::temp0 ::temp0                                     ;@line 141
						JumpF ::temp0 _label435                                  ;@line 141
						CompareEQ ::temp1 token -1                               ;@line 141
						Cast ::temp0 ::temp1                                     ;@line 141
					_label435:
						Cast ::temp0 ::temp0                                     ;@line 141
						JumpF ::temp0 _label436                                  ;@line 141
						Not ::temp1 operating                                    ;@line 141
						Cast ::temp0 ::temp1                                     ;@line 141
					_label436:
						JumpF ::temp0 _label437                                  ;@line 141
						Assign endingSession False                               ;@line 142
						Jump _label437                                           ;@line 142
					_label437:
					.endCode
				.endFunction
				.function StopRepeatFire
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp39 Int
					.endLocalTable
					.code
						Assign repeatFire False                                  ;@line 525
						IAdd ::temp39 repeatRevision 1                           ;@line 526
						Assign repeatRevision ::temp39                           ;@line 526
					.endCode
				.endFunction
				.function RetainMountedCombat
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp217 Bool
						.local ::temp218 Bool
						.local ::temp219 Actor
						.local ::NoneVar None
						.local ::temp220 worldspace
						.local ::temp221 worldspace
						.local operator Actor
						.local target Actor
					.endLocalTable
					.code
						Not ::temp217 operating                                  ;@line 1902
						Cast ::temp217 ::temp217                                 ;@line 1902
						JumpT ::temp217 _label438                                ;@line 1902
						CompareEQ ::temp218 generation expectedGeneration        ;@line 1902
						Not ::temp218 ::temp218                                  ;@line 1902
						Cast ::temp217 ::temp218                                 ;@line 1902
					_label438:
						Cast ::temp217 ::temp217                                 ;@line 1902
						JumpT ::temp217 _label439                                ;@line 1902
						CompareEQ ::temp218 token expectedToken                  ;@line 1902
						Not ::temp218 ::temp218                                  ;@line 1902
						Cast ::temp217 ::temp218                                 ;@line 1902
					_label439:
						JumpF ::temp217 _label440                                ;@line 1902
						Return None                                              ;@line 1903
						Jump _label440                                           ;@line 1903
					_label440:
						Assign operator player                                   ;@line 1905
						Assign target retainedCombatTarget                       ;@line 1906
						Cast ::temp219 None                                      ;@line 1907
						CompareEQ ::temp218 operator ::temp219                   ;@line 1907
						Cast ::temp218 ::temp218                                 ;@line 1907
						JumpT ::temp218 _label441                                ;@line 1907
						Cast ::temp219 None                                      ;@line 1907
						CompareEQ ::temp217 target ::temp219                     ;@line 1907
						Cast ::temp218 ::temp217                                 ;@line 1907
					_label441:
						Cast ::temp218 ::temp218                                 ;@line 1907
						JumpT ::temp218 _label442                                ;@line 1907
						CompareEQ ::temp217 target operator                      ;@line 1907
						Cast ::temp218 ::temp217                                 ;@line 1907
					_label442:
						JumpF ::temp218 _label443                                ;@line 1907
						Return None                                              ;@line 1908
						Jump _label443                                           ;@line 1908
					_label443:
						CallMethod TraceRetainedCombat self ::NoneVar "tick"     ;@line 1910
						Not ::temp217 operating                                  ;@line 1912
						Cast ::temp217 ::temp217                                 ;@line 1912
						JumpT ::temp217 _label444                                ;@line 1912
						CompareEQ ::temp218 generation expectedGeneration        ;@line 1912
						Not ::temp218 ::temp218                                  ;@line 1912
						Cast ::temp217 ::temp218                                 ;@line 1912
					_label444:
						Cast ::temp217 ::temp217                                 ;@line 1912
						JumpT ::temp217 _label445                                ;@line 1912
						CompareEQ ::temp218 token expectedToken                  ;@line 1912
						Not ::temp218 ::temp218                                  ;@line 1912
						Cast ::temp217 ::temp218                                 ;@line 1912
					_label445:
						Cast ::temp217 ::temp217                                 ;@line 1912
						JumpT ::temp217 _label446                                ;@line 1912
						CompareEQ ::temp218 retainedCombatTarget target          ;@line 1912
						Not ::temp218 ::temp218                                  ;@line 1912
						Cast ::temp217 ::temp218                                 ;@line 1912
					_label446:
						JumpF ::temp217 _label447                                ;@line 1912
						Return None                                              ;@line 1913
						Jump _label447                                           ;@line 1913
					_label447:
						CallMethod IsDead target ::temp218                       ;@line 1915
						Cast ::temp218 ::temp218                                 ;@line 1915
						JumpT ::temp218 _label448                                ;@line 1915
						CallMethod IsDead operator ::temp217                     ;@line 1915
						Cast ::temp218 ::temp217                                 ;@line 1915
					_label448:
						Cast ::temp218 ::temp218                                 ;@line 1915
						JumpT ::temp218 _label449                                ;@line 1915
						CallMethod GetWorldSpace operator ::temp220              ;@line 1915
						CallMethod GetWorldSpace target ::temp221                ;@line 1915
						CompareEQ ::temp217 ::temp220 ::temp221                  ;@line 1915
						Not ::temp217 ::temp217                                  ;@line 1915
						Cast ::temp218 ::temp217                                 ;@line 1915
					_label449:
						JumpF ::temp218 _label450                                ;@line 1915
						Cast ::temp219 None                                      ;@line 1916
						Assign retainedCombatTarget ::temp219                    ;@line 1916
						Return None                                              ;@line 1917
						Jump _label450                                           ;@line 1917
					_label450:
						CallMethod GetCombatTarget target ::temp219              ;@line 1919
						CompareEQ ::temp217 ::temp219 operator                   ;@line 1919
						Not ::temp217 ::temp217                                  ;@line 1919
						JumpF ::temp217 _label451                                ;@line 1919
						CallMethod StartCombat target ::NoneVar operator         ;@line 1920
						Jump _label451                                           ;@line 1920
					_label451:
						CallMethod GetCombatTarget operator ::temp219            ;@line 1922
						CompareEQ ::temp218 ::temp219 target                     ;@line 1922
						Not ::temp218 ::temp218                                  ;@line 1922
						JumpF ::temp218 _label452                                ;@line 1922
						CallMethod StartCombat operator ::NoneVar target         ;@line 1923
						Jump _label452                                           ;@line 1923
					_label452:
					.endCode
				.endFunction
				.function TimingFinite
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param value Float
						.param minimum Float
						.param maximum Float
					.endParamTable
					.localTable
						.local ::temp7 Bool
						.local ::temp8 Bool
					.endLocalTable
					.code
						CompareEQ ::temp7 value value                            ;@line 162
						Cast ::temp7 ::temp7                                     ;@line 162
						JumpF ::temp7 _label453                                  ;@line 162
						CompareGTE ::temp8 value minimum                         ;@line 162
						Cast ::temp7 ::temp8                                     ;@line 162
					_label453:
						Cast ::temp7 ::temp7                                     ;@line 162
						JumpF ::temp7 _label454                                  ;@line 162
						CompareLTE ::temp8 value maximum                         ;@line 162
						Cast ::temp7 ::temp8                                     ;@line 162
					_label454:
						Return ::temp7                                           ;@line 162
					.endCode
				.endFunction
				.function OnControlDown
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param control String
					.endParamTable
					.localTable
						.local ::temp60 Bool
						.local ::temp61 String
						.local ::temp62 String
						.local ::NoneVar None
						.local ::temp63 Bool
						.local ::temp64 Bool
						.local controlEventGeneration Int
						.local controlEventToken Int
					.endLocalTable
					.code
						Not ::temp60 operating                                   ;@line 673
						JumpF ::temp60 _label455                                 ;@line 673
						Return None                                              ;@line 674
						Jump _label455                                           ;@line 674
					_label455:
						Assign controlEventGeneration generation                 ;@line 676
						Assign controlEventToken token                           ;@line 677
						StrCat ::temp61 "AstraAsedio OnControlDown control=" control  ;@line 678
						StrCat ::temp61 ::temp61 " phase="                       ;@line 678
						Cast ::temp62 phase                                      ;@line 678
						StrCat ::temp62 ::temp61 ::temp62                        ;@line 678
						StrCat ::temp61 ::temp62 " generation="                  ;@line 678
						Cast ::temp62 generation                                 ;@line 678
						StrCat ::temp62 ::temp61 ::temp62                        ;@line 678
						CallStatic debug Trace ::NoneVar ::temp62 0              ;@line 678
						Not ::temp60 operating                                   ;@line 679
						Cast ::temp60 ::temp60                                   ;@line 679
						JumpT ::temp60 _label456                                 ;@line 679
						CompareEQ ::temp63 generation controlEventGeneration     ;@line 679
						Not ::temp63 ::temp63                                    ;@line 679
						Cast ::temp60 ::temp63                                   ;@line 679
					_label456:
						Cast ::temp60 ::temp60                                   ;@line 679
						JumpT ::temp60 _label457                                 ;@line 679
						CompareEQ ::temp63 token controlEventToken               ;@line 679
						Not ::temp63 ::temp63                                    ;@line 679
						Cast ::temp60 ::temp63                                   ;@line 679
					_label457:
						JumpF ::temp60 _label458                                 ;@line 679
						Return None                                              ;@line 680
						Jump _label458                                           ;@line 680
					_label458:
						CompareEQ ::temp63 control "Activate"                    ;@line 682
						JumpF ::temp63 _label459                                 ;@line 682
						CallMethod RequestExit self ::NoneVar "OnControlDown"    ;@line 683
						Jump _label460                                           ;@line 683
					_label459:
						Not ::temp60 ::UseSightCamera_var                        ;@line 684
						Cast ::temp60 ::temp60                                   ;@line 684
						JumpF ::temp60 _label461                                 ;@line 684
						CompareEQ ::temp64 control "Right Attack/Block"          ;@line 684
						Cast ::temp60 ::temp64                                   ;@line 684
					_label461:
						JumpF ::temp60 _label462                                 ;@line 684
						CallMethod RequestShot self ::NoneVar                    ;@line 685
						Jump _label460                                           ;@line 685
					_label462:
						Not ::temp64 ::UseSightCamera_var                        ;@line 686
						Cast ::temp64 ::temp64                                   ;@line 686
						JumpF ::temp64 _label463                                 ;@line 686
						CompareEQ ::temp60 control "Sprint"                      ;@line 686
						Cast ::temp64 ::temp60                                   ;@line 686
					_label463:
						JumpF ::temp64 _label460                                 ;@line 686
						CallMethod RequestFireMode self ::NoneVar                ;@line 687
						Jump _label460                                           ;@line 687
					_label460:
					.endCode
				.endFunction
				.function OnKeyUp
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param keyCode Int
						.param holdTime Float
					.endParamTable
					.localTable
						.local ::temp54 Bool
						.local ::NoneVar None
						.local ::temp55 Bool
						.local ::temp59 Bool
						.local ::temp56 Int
						.local ::temp57 String
						.local ::temp58 String
					.endLocalTable
					.code
						Not ::temp54 operating                                   ;@line 653
						JumpF ::temp54 _label464                                 ;@line 653
						Return None                                              ;@line 654
						Jump _label464                                           ;@line 654
					_label464:
						JumpF ::UseSightCamera_var _label465                     ;@line 656
						Return None                                              ;@line 657
						Jump _label465                                           ;@line 657
					_label465:
						CallMethod SetAimKey self ::NoneVar keyCode False        ;@line 659
						CompareEQ ::temp54 keyCode fireKeyboard                  ;@line 660
						Cast ::temp54 ::temp54                                   ;@line 660
						JumpT ::temp54 _label466                                 ;@line 660
						CompareEQ ::temp55 keyCode fireMouse                     ;@line 660
						Cast ::temp54 ::temp55                                   ;@line 660
					_label466:
						JumpF ::temp54 _label467                                 ;@line 660
						IAdd ::temp56 fireReleaseSerial 1                        ;@line 661
						Assign fireReleaseSerial ::temp56                        ;@line 661
						Assign heldFire False                                    ;@line 662
						CallMethod StopRepeatFire self ::NoneVar                 ;@line 663
						Cast ::temp57 keyCode                                    ;@line 665
						StrCat ::temp57 "AstraAsedio OnKeyUp code=" ::temp57     ;@line 665
						StrCat ::temp57 ::temp57 " phase="                       ;@line 665
						Cast ::temp58 phase                                      ;@line 665
						StrCat ::temp58 ::temp57 ::temp58                        ;@line 665
						StrCat ::temp57 ::temp58 " generation="                  ;@line 665
						Cast ::temp58 generation                                 ;@line 665
						StrCat ::temp58 ::temp57 ::temp58                        ;@line 665
						CallStatic debug Trace ::NoneVar ::temp58 0              ;@line 665
						Jump _label468                                           ;@line 665
					_label467:
						CompareEQ ::temp55 keyCode modeKeyboard                  ;@line 666
						Cast ::temp55 ::temp55                                   ;@line 666
						JumpT ::temp55 _label469                                 ;@line 666
						CompareEQ ::temp59 keyCode modeMouse                     ;@line 666
						Cast ::temp55 ::temp59                                   ;@line 666
					_label469:
						JumpF ::temp55 _label468                                 ;@line 666
						IAdd ::temp56 modeReleaseSerial 1                        ;@line 667
						Assign modeReleaseSerial ::temp56                        ;@line 667
						Assign heldMode False                                    ;@line 668
						Jump _label468                                           ;@line 668
					_label468:
					.endCode
				.endFunction
				.function NormalizeTimingProperties
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp9 Bool
						.local ::temp12 Float
						.local ::temp10 Bool
						.local ::temp11 Bool
					.endLocalTable
					.code
						CompareLT ::temp9 timingRevision 14                      ;@line 168
						JumpF ::temp9 _label470                                  ;@line 168
						CompareGTE ::temp10 ::FireSeconds_var 0.299990           ;@line 169
						Cast ::temp10 ::temp10                                   ;@line 169
						JumpF ::temp10 _label471                                 ;@line 169
						CompareLTE ::temp11 ::FireSeconds_var 0.300010           ;@line 169
						Cast ::temp10 ::temp11                                   ;@line 169
					_label471:
						JumpF ::temp10 _label472                                 ;@line 169
						Assign ::FireSeconds_var 0.200000                        ;@line 170
						Jump _label472                                           ;@line 170
					_label472:
						CompareGTE ::temp11 ::ReleaseSeconds_var 0.099990        ;@line 172
						Cast ::temp11 ::temp11                                   ;@line 172
						JumpF ::temp11 _label473                                 ;@line 172
						CompareLTE ::temp10 ::ReleaseSeconds_var 0.100010        ;@line 172
						Cast ::temp11 ::temp10                                   ;@line 172
					_label473:
						JumpF ::temp11 _label474                                 ;@line 172
						Assign ::ReleaseSeconds_var 0.066667                     ;@line 173
						Jump _label474                                           ;@line 173
					_label474:
						CompareGTE ::temp10 ::ResetSeconds_var 1.199990          ;@line 175
						Cast ::temp10 ::temp10                                   ;@line 175
						JumpF ::temp10 _label475                                 ;@line 175
						CompareLTE ::temp11 ::ResetSeconds_var 1.200010          ;@line 175
						Cast ::temp10 ::temp11                                   ;@line 175
					_label475:
						JumpF ::temp10 _label476                                 ;@line 175
						Assign ::ResetSeconds_var 0.800000                       ;@line 176
						Jump _label476                                           ;@line 176
					_label476:
						CompareGTE ::temp11 ::CycleSeconds_var 1.499990          ;@line 178
						Cast ::temp11 ::temp11                                   ;@line 178
						JumpF ::temp11 _label477                                 ;@line 178
						CompareLTE ::temp10 ::CycleSeconds_var 1.500010          ;@line 178
						Cast ::temp11 ::temp10                                   ;@line 178
					_label477:
						JumpF ::temp11 _label478                                 ;@line 178
						Assign ::CycleSeconds_var 1.000000                       ;@line 179
						Jump _label478                                           ;@line 179
					_label478:
						Assign timingRevision 14                                 ;@line 181
						Jump _label470                                           ;@line 181
					_label470:
						CallMethod TimingFinite self ::temp10 ::FireSeconds_var 0.200000 2.000000  ;@line 183
						Not ::temp11 ::temp10                                    ;@line 183
						JumpF ::temp11 _label479                                 ;@line 183
						Assign ::FireSeconds_var 0.200000                        ;@line 184
						Jump _label479                                           ;@line 184
					_label479:
						CallMethod TimingFinite self ::temp9 ::ReleaseSeconds_var 0.066667 1.000000  ;@line 186
						Not ::temp10 ::temp9                                     ;@line 186
						Cast ::temp9 ::temp10                                    ;@line 186
						JumpT ::temp9 _label480                                  ;@line 186
						CompareGT ::temp11 ::ReleaseSeconds_var ::FireSeconds_var  ;@line 186
						Cast ::temp9 ::temp11                                    ;@line 186
					_label480:
						JumpF ::temp9 _label481                                  ;@line 186
						Assign ::ReleaseSeconds_var 0.066667                     ;@line 187
						Jump _label481                                           ;@line 187
					_label481:
						CallMethod TimingFinite self ::temp10 ::ResetSeconds_var 0.800000 5.000000  ;@line 189
						Not ::temp11 ::temp10                                    ;@line 189
						JumpF ::temp11 _label482                                 ;@line 189
						Assign ::ResetSeconds_var 0.800000                       ;@line 190
						Jump _label482                                           ;@line 190
					_label482:
						CallMethod TimingFinite self ::temp9 ::CycleSeconds_var 1.000000 7.000000  ;@line 192
						Not ::temp10 ::temp9                                     ;@line 192
						JumpF ::temp10 _label483                                 ;@line 192
						Assign ::CycleSeconds_var 1.000000                       ;@line 193
						Jump _label483                                           ;@line 193
					_label483:
						FAdd ::temp12 ::FireSeconds_var ::ResetSeconds_var       ;@line 195
						CompareLT ::temp11 ::CycleSeconds_var ::temp12           ;@line 195
						JumpF ::temp11 _label484                                 ;@line 195
						FAdd ::temp12 ::FireSeconds_var ::ResetSeconds_var       ;@line 196
						Assign ::CycleSeconds_var ::temp12                       ;@line 196
						Jump _label484                                           ;@line 196
					_label484:
					.endCode
				.endFunction
				.function OnKeyDown
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param keyCode Int
					.endParamTable
					.localTable
						.local ::temp48 Bool
						.local ::temp49 String
						.local ::temp50 String
						.local ::NoneVar None
						.local ::temp51 Bool
						.local ::temp52 Bool
						.local ::temp53 Bool
						.local keyEventGeneration Int
						.local keyEventToken Int
					.endLocalTable
					.code
						Not ::temp48 operating                                   ;@line 632
						JumpF ::temp48 _label485                                 ;@line 632
						Return None                                              ;@line 633
						Jump _label485                                           ;@line 633
					_label485:
						Assign keyEventGeneration generation                     ;@line 635
						Assign keyEventToken token                               ;@line 636
						Cast ::temp49 keyCode                                    ;@line 637
						StrCat ::temp49 "AstraAsedio OnKeyDown code=" ::temp49   ;@line 637
						StrCat ::temp49 ::temp49 " phase="                       ;@line 637
						Cast ::temp50 phase                                      ;@line 637
						StrCat ::temp50 ::temp49 ::temp50                        ;@line 637
						StrCat ::temp49 ::temp50 " generation="                  ;@line 637
						Cast ::temp50 generation                                 ;@line 637
						StrCat ::temp50 ::temp49 ::temp50                        ;@line 637
						CallStatic debug Trace ::NoneVar ::temp50 0              ;@line 637
						Not ::temp48 operating                                   ;@line 638
						Cast ::temp48 ::temp48                                   ;@line 638
						JumpT ::temp48 _label486                                 ;@line 638
						CompareEQ ::temp51 generation keyEventGeneration         ;@line 638
						Not ::temp51 ::temp51                                    ;@line 638
						Cast ::temp48 ::temp51                                   ;@line 638
					_label486:
						Cast ::temp48 ::temp48                                   ;@line 638
						JumpT ::temp48 _label487                                 ;@line 638
						CompareEQ ::temp51 token keyEventToken                   ;@line 638
						Not ::temp51 ::temp51                                    ;@line 638
						Cast ::temp48 ::temp51                                   ;@line 638
					_label487:
						JumpF ::temp48 _label488                                 ;@line 638
						Return None                                              ;@line 639
						Jump _label488                                           ;@line 639
					_label488:
						CompareEQ ::temp51 keyCode activateKeyboard              ;@line 641
						Cast ::temp51 ::temp51                                   ;@line 641
						JumpT ::temp51 _label489                                 ;@line 641
						CompareEQ ::temp48 keyCode activateMouse                 ;@line 641
						Cast ::temp51 ::temp48                                   ;@line 641
					_label489:
						JumpF ::temp51 _label490                                 ;@line 641
						CallMethod RequestExit self ::NoneVar "OnKeyDown"        ;@line 642
						Jump _label491                                           ;@line 642
					_label490:
						Not ::temp48 ::UseSightCamera_var                        ;@line 643
						Cast ::temp53 ::temp48                                   ;@line 643
						JumpF ::temp53 _label492                                 ;@line 643
						CompareEQ ::temp52 keyCode fireKeyboard                  ;@line 643
						Cast ::temp52 ::temp52                                   ;@line 643
						JumpT ::temp52 _label493                                 ;@line 643
						CompareEQ ::temp53 keyCode fireMouse                     ;@line 643
						Cast ::temp52 ::temp53                                   ;@line 643
					_label493:
						Cast ::temp53 ::temp52                                   ;@line 643
					_label492:
						JumpF ::temp53 _label494                                 ;@line 643
						CallMethod RequestShot self ::NoneVar                    ;@line 644
						Jump _label491                                           ;@line 644
					_label494:
						Not ::temp48 ::UseSightCamera_var                        ;@line 645
						Cast ::temp53 ::temp48                                   ;@line 645
						JumpF ::temp53 _label495                                 ;@line 645
						CompareEQ ::temp52 keyCode modeKeyboard                  ;@line 645
						Cast ::temp52 ::temp52                                   ;@line 645
						JumpT ::temp52 _label496                                 ;@line 645
						CompareEQ ::temp53 keyCode modeMouse                     ;@line 645
						Cast ::temp52 ::temp53                                   ;@line 645
					_label496:
						Cast ::temp53 ::temp52                                   ;@line 645
					_label495:
						JumpF ::temp53 _label497                                 ;@line 645
						CallMethod RequestFireMode self ::NoneVar                ;@line 646
						Jump _label491                                           ;@line 646
					_label497:
						CallMethod SetAimKey self ::NoneVar keyCode True         ;@line 648
					_label491:
					.endCode
				.endFunction
				.function ReadAimRoot
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
					.localTable
						.local ::temp111 ObjectReference
						.local ::temp112 Bool
						.local i Int
						.local ::temp113 Float
						.local ::temp114 Float
						.local ::temp115 Bool
						.local ::temp116 Bool
						.local ::temp117 Int
					.endLocalTable
					.code
						Cast ::temp111 self                                      ;@line 934
						CallStatic netimmerse GetNodeWorldRotationMatrix ::temp112 ::temp111 "" rootWorldMatrix False  ;@line 934
						Not ::temp112 ::temp112                                  ;@line 934
						JumpF ::temp112 _label498                                ;@line 934
						Return False                                             ;@line 935
						Jump _label498                                           ;@line 935
					_label498:
						Assign i 0                                               ;@line 937
					_label502:
						CompareLT ::temp112 i 9                                  ;@line 938
						JumpF ::temp112 _label499                                ;@line 938
						ArrayGetElement ::temp113 rootWorldMatrix i              ;@line 939
						ArrayGetElement ::temp114 rootWorldMatrix i              ;@line 939
						CompareEQ ::temp115 ::temp113 ::temp114                  ;@line 939
						Not ::temp115 ::temp115                                  ;@line 939
						Cast ::temp115 ::temp115                                 ;@line 939
						JumpT ::temp115 _label500                                ;@line 939
						ArrayGetElement ::temp113 rootWorldMatrix i              ;@line 939
						CallStatic math Abs ::temp114 ::temp113                  ;@line 939
						CompareGT ::temp116 ::temp114 1.050000                   ;@line 939
						Cast ::temp115 ::temp116                                 ;@line 939
					_label500:
						JumpF ::temp115 _label501                                ;@line 939
						Return False                                             ;@line 940
						Jump _label501                                           ;@line 940
					_label501:
						IAdd ::temp117 i 1                                       ;@line 942
						Assign i ::temp117                                       ;@line 942
						Jump _label502                                           ;@line 942
					_label499:
						Return True                                              ;@line 944
					.endCode
				.endFunction
				.function ClearHeldInput
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param requireRelease Bool
					.endParamTable
					.localTable
						.local ::NoneVar None
						.local ::temp38 Bool
					.endLocalTable
					.code
						JumpF requireRelease _label503                           ;@line 503
						Cast ::temp38 releaseLeft                                ;@line 505
						JumpT ::temp38 _label504                                 ;@line 505
						Cast ::temp38 heldLeft                                   ;@line 505
					_label504:
						Assign releaseLeft ::temp38                              ;@line 505
						Cast ::temp38 releaseRight                               ;@line 506
						JumpT ::temp38 _label505                                 ;@line 506
						Cast ::temp38 heldRight                                  ;@line 506
					_label505:
						Assign releaseRight ::temp38                             ;@line 506
						Cast ::temp38 releaseUp                                  ;@line 507
						JumpT ::temp38 _label506                                 ;@line 507
						Cast ::temp38 heldUp                                     ;@line 507
					_label506:
						Assign releaseUp ::temp38                                ;@line 507
						Cast ::temp38 releaseDown                                ;@line 508
						JumpT ::temp38 _label507                                 ;@line 508
						Cast ::temp38 heldDown                                   ;@line 508
					_label507:
						Assign releaseDown ::temp38                              ;@line 508
						Jump _label508                                           ;@line 508
					_label503:
						Assign releaseLeft False                                 ;@line 510
						Assign releaseRight False                                ;@line 511
						Assign releaseUp False                                   ;@line 512
						Assign releaseDown False                                 ;@line 513
					_label508:
						Assign heldLeft False                                    ;@line 515
						Assign heldRight False                                   ;@line 516
						Assign heldUp False                                      ;@line 517
						Assign heldDown False                                    ;@line 518
						Cast ::temp38 heldFire                                   ;@line 519
						JumpF ::temp38 _label509                                 ;@line 519
						Cast ::temp38 requireRelease                             ;@line 519
					_label509:
						Assign heldFire ::temp38                                 ;@line 519
						Cast ::temp38 heldMode                                   ;@line 520
						JumpF ::temp38 _label510                                 ;@line 520
						Cast ::temp38 requireRelease                             ;@line 520
					_label510:
						Assign heldMode ::temp38                                 ;@line 520
						CallMethod StopRepeatFire self ::NoneVar                 ;@line 521
					.endCode
				.endFunction
				.function SampleLookAim
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param expectedGeneration Int
					.endParamTable
					.localTable
						.local ::temp142 Int
						.local ::temp143 Bool
					.endLocalTable
					.code
						CallMethod SampleLookAimResult self ::temp142 expectedGeneration  ;@line 1145
						CompareEQ ::temp143 ::temp142 1                          ;@line 1145
						Return ::temp143                                         ;@line 1145
					.endCode
				.endFunction
				.function SampleSightAimResult
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Int
					.paramTable
						.param expectedGeneration Int
						.param freeze Bool
					.endParamTable
					.localTable
						.local ::temp129 Bool
						.local ::temp130 ObjectReference
						.local ::temp131 Float[]
						.local ::temp132 Int
						.local ::temp133 Float
						.local ::temp134 Bool
						.local aimToken Int
						.local ready Bool
						.local readinessMenu Bool
						.local snapshot Float[]
						.local sampleMenu Bool
						.local nextYaw Float
						.local nextPitch Float
						.local currentLease Bool
						.local cameraState Int
						.local menuOpen Bool
						.local ::temp135 Bool
						.local graceNow Float
					.endLocalTable
					.code
						Assign aimToken token                                    ;@line 1058
						CallMethod SightSampleCurrent self ::temp129 expectedGeneration aimToken freeze  ;@line 1059
						Not ::temp129 ::temp129                                  ;@line 1059
						JumpF ::temp129 _label511                                ;@line 1059
						Return 0                                                 ;@line 1060
						Jump _label511                                           ;@line 1060
					_label511:
						Cast ::temp130 self                                      ;@line 1062
						CallStatic astrasightnative IsSightReady ::temp129 ::temp130 aimToken  ;@line 1062
						Assign ready ::temp129                                   ;@line 1062
						CallStatic utility IsInMenuMode ::temp129                ;@line 1063
						Assign readinessMenu ::temp129                           ;@line 1063
						CallMethod SightSampleCurrent self ::temp129 expectedGeneration aimToken freeze  ;@line 1064
						Not ::temp129 ::temp129                                  ;@line 1064
						Cast ::temp129 ::temp129                                 ;@line 1064
						JumpT ::temp129 _label512                                ;@line 1064
						Cast ::temp129 readinessMenu                             ;@line 1064
					_label512:
						JumpF ::temp129 _label513                                ;@line 1064
						Return 0                                                 ;@line 1065
						Jump _label513                                           ;@line 1065
					_label513:
						Not ::temp129 ready                                      ;@line 1067
						JumpF ::temp129 _label514                                ;@line 1067
						Return -1                                                ;@line 1068
						Jump _label514                                           ;@line 1068
					_label514:
						Cast ::temp130 self                                      ;@line 1070
						CallStatic astrasightnative CaptureAim ::temp131 ::temp130 aimToken freeze  ;@line 1070
						Assign snapshot ::temp131                                ;@line 1070
						CallStatic utility IsInMenuMode ::temp129                ;@line 1072
						Assign sampleMenu ::temp129                              ;@line 1072
						CallMethod SightSampleCurrent self ::temp129 expectedGeneration aimToken freeze  ;@line 1073
						Not ::temp129 ::temp129                                  ;@line 1073
						Cast ::temp129 ::temp129                                 ;@line 1073
						JumpT ::temp129 _label515                                ;@line 1073
						Cast ::temp129 sampleMenu                                ;@line 1073
					_label515:
						JumpF ::temp129 _label516                                ;@line 1073
						Return 0                                                 ;@line 1074
						Jump _label516                                           ;@line 1074
					_label516:
						ArrayLength ::temp132 snapshot                           ;@line 1076
						CompareEQ ::temp129 ::temp132 2                          ;@line 1076
						Not ::temp129 ::temp129                                  ;@line 1076
						JumpF ::temp129 _label517                                ;@line 1076
						Return -1                                                ;@line 1077
						Jump _label517                                           ;@line 1077
					_label517:
						ArrayGetElement ::temp133 snapshot 0                     ;@line 1079
						Assign nextYaw ::temp133                                 ;@line 1079
						ArrayGetElement ::temp133 snapshot 1                     ;@line 1080
						Assign nextPitch ::temp133                               ;@line 1080
						CompareEQ ::temp129 nextYaw 360.000000                   ;@line 1083
						JumpF ::temp129 _label518                                ;@line 1083
						Assign nextYaw 0.000000                                  ;@line 1084
						Jump _label518                                           ;@line 1084
					_label518:
						CompareEQ ::temp129 nextYaw nextYaw                      ;@line 1086
						Not ::temp129 ::temp129                                  ;@line 1086
						Cast ::temp129 ::temp129                                 ;@line 1086
						JumpT ::temp129 _label519                                ;@line 1086
						CompareEQ ::temp134 nextPitch nextPitch                  ;@line 1086
						Not ::temp134 ::temp134                                  ;@line 1086
						Cast ::temp129 ::temp134                                 ;@line 1086
					_label519:
						Cast ::temp129 ::temp129                                 ;@line 1086
						JumpT ::temp129 _label520                                ;@line 1086
						CompareLT ::temp134 nextYaw 0.000000                     ;@line 1086
						Cast ::temp129 ::temp134                                 ;@line 1086
					_label520:
						Cast ::temp129 ::temp129                                 ;@line 1086
						JumpT ::temp129 _label521                                ;@line 1086
						CompareGTE ::temp134 nextYaw 360.000000                  ;@line 1086
						Cast ::temp129 ::temp134                                 ;@line 1086
					_label521:
						Cast ::temp129 ::temp129                                 ;@line 1086
						JumpT ::temp129 _label522                                ;@line 1086
						CompareLT ::temp134 nextPitch ::PitchMin_var             ;@line 1086
						Cast ::temp129 ::temp134                                 ;@line 1086
					_label522:
						Cast ::temp129 ::temp129                                 ;@line 1086
						JumpT ::temp129 _label523                                ;@line 1086
						CompareGT ::temp134 nextPitch ::PitchMax_var             ;@line 1086
						Cast ::temp129 ::temp134                                 ;@line 1086
					_label523:
						JumpF ::temp129 _label524                                ;@line 1086
						Return -1                                                ;@line 1087
						Jump _label524                                           ;@line 1087
					_label524:
						CallMethod IsCurrent ::Session_var ::temp134 self aimToken  ;@line 1089
						Assign currentLease ::temp134                            ;@line 1089
						CallMethod ReadCameraState self ::temp132                ;@line 1090
						Assign cameraState ::temp132                             ;@line 1090
						CallStatic utility IsInMenuMode ::temp129                ;@line 1091
						Assign menuOpen ::temp129                                ;@line 1091
						CallMethod SightSampleCurrent self ::temp134 expectedGeneration aimToken freeze  ;@line 1092
						Not ::temp129 ::temp134                                  ;@line 1092
						Cast ::temp134 ::temp129                                 ;@line 1092
						JumpT ::temp134 _label525                                ;@line 1092
						Cast ::temp134 menuOpen                                  ;@line 1092
					_label525:
						JumpF ::temp134 _label526                                ;@line 1092
						Return 0                                                 ;@line 1093
						Jump _label526                                           ;@line 1093
					_label526:
						Not ::temp129 currentLease                               ;@line 1095
						JumpF ::temp129 _label527                                ;@line 1095
						Return -1                                                ;@line 1096
						Jump _label527                                           ;@line 1096
					_label527:
						CompareEQ ::temp134 cameraState 0                        ;@line 1098
						Not ::temp134 ::temp134                                  ;@line 1098
						JumpF ::temp134 _label528                                ;@line 1098
						CallStatic utility GetCurrentRealTime ::temp133          ;@line 1102
						Assign graceNow ::temp133                                ;@line 1102
						CompareEQ ::temp129 cameraState 6                        ;@line 1103
						Cast ::temp129 ::temp129                                 ;@line 1103
						JumpT ::temp129 _label529                                ;@line 1103
						CompareEQ ::temp135 cameraState 7                        ;@line 1103
						Cast ::temp129 ::temp135                                 ;@line 1103
					_label529:
						Cast ::temp129 ::temp129                                 ;@line 1103
						JumpF ::temp129 _label530                                ;@line 1103
						CompareLT ::temp135 graceNow cameraGraceUntil            ;@line 1103
						Cast ::temp129 ::temp135                                 ;@line 1103
					_label530:
						JumpF ::temp129 _label531                                ;@line 1103
						Return 0                                                 ;@line 1104
						Jump _label531                                           ;@line 1104
					_label531:
						Return -1                                                ;@line 1106
						Jump _label528                                           ;@line 1106
					_label528:
						Assign yaw nextYaw                                       ;@line 1108
						Assign pitch nextPitch                                   ;@line 1109
						Return 1                                                 ;@line 1111
					.endCode
				.endFunction
				.function CaptureMatrices
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
					.localTable
						.local ::temp150 Int
						.local ::temp151 Bool
						.local ::temp152 ObjectReference
						.local ::temp153 String
						.local ::temp154 Float[]
						.local ::temp155 Bool
						.local ::temp156 Bool
					.endLocalTable
					.code
						Assign matrixFailure ""                                  ;@line 1221
						CallStatic skse GetVersion ::temp150                     ;@line 1222
						CompareLT ::temp151 ::temp150 2                          ;@line 1222
						JumpF ::temp151 _label532                                ;@line 1222
						Assign matrixFailure "SKSE_MISSING: inicia Skyrim con SKSE64."  ;@line 1223
						Return False                                             ;@line 1224
						Jump _label532                                           ;@line 1224
					_label532:
						CallMethod Is3DLoaded self ::temp151                     ;@line 1226
						Not ::temp151 ::temp151                                  ;@line 1226
						JumpF ::temp151 _label533                                ;@line 1226
						Assign matrixFailure "MODEL_NOT_LOADED: la malla aÃºn no estÃ¡ cargada."  ;@line 1227
						Return False                                             ;@line 1228
						Jump _label533                                           ;@line 1228
					_label533:
						Cast ::temp152 self                                      ;@line 1230
						CallStatic netimmerse HasNode ::temp151 ::temp152 ::YawNode_var False  ;@line 1230
						Not ::temp151 ::temp151                                  ;@line 1230
						JumpF ::temp151 _label534                                ;@line 1230
						StrCat ::temp153 "NODE_MISSING: " ::YawNode_var          ;@line 1231
						Assign matrixFailure ::temp153                           ;@line 1231
						Return False                                             ;@line 1232
						Jump _label534                                           ;@line 1232
					_label534:
						Cast ::temp152 self                                      ;@line 1234
						CallStatic netimmerse HasNode ::temp151 ::temp152 ::PitchNode_var False  ;@line 1234
						Not ::temp151 ::temp151                                  ;@line 1234
						JumpF ::temp151 _label535                                ;@line 1234
						StrCat ::temp153 "NODE_MISSING: " ::PitchNode_var        ;@line 1235
						Assign matrixFailure ::temp153                           ;@line 1235
						Return False                                             ;@line 1236
						Jump _label535                                           ;@line 1236
					_label535:
						Cast ::temp152 self                                      ;@line 1238
						CallStatic netimmerse HasNode ::temp151 ::temp152 ::VisualBoltNode_var False  ;@line 1238
						Not ::temp151 ::temp151                                  ;@line 1238
						JumpF ::temp151 _label536                                ;@line 1238
						StrCat ::temp153 "NODE_MISSING: " ::VisualBoltNode_var   ;@line 1239
						Assign matrixFailure ::temp153                           ;@line 1239
						Return False                                             ;@line 1240
						Jump _label536                                           ;@line 1240
					_label536:
						Cast ::temp152 self                                      ;@line 1242
						CallStatic netimmerse HasNode ::temp151 ::temp152 "ProjectileNode" False  ;@line 1242
						Not ::temp151 ::temp151                                  ;@line 1242
						JumpF ::temp151 _label537                                ;@line 1242
						Assign matrixFailure "NODE_MISSING: ProjectileNode"      ;@line 1243
						Return False                                             ;@line 1244
						Jump _label537                                           ;@line 1244
					_label537:
						Cast ::temp152 self                                      ;@line 1246
						CallStatic netimmerse HasNode ::temp151 ::temp152 ::OperatorNode_var False  ;@line 1246
						Not ::temp151 ::temp151                                  ;@line 1246
						JumpF ::temp151 _label538                                ;@line 1246
						StrCat ::temp153 "NODE_MISSING: " ::OperatorNode_var     ;@line 1247
						Assign matrixFailure ::temp153                           ;@line 1247
						Return False                                             ;@line 1248
						Jump _label538                                           ;@line 1248
					_label538:
						Not ::temp151 matricesReady                              ;@line 1254
						JumpF ::temp151 _label539                                ;@line 1254
						ArrayCreate ::temp154 9                                  ;@line 1255
						Assign yawBase ::temp154                                 ;@line 1255
						ArrayCreate ::temp154 9                                  ;@line 1256
						Assign pitchBase ::temp154                               ;@line 1256
						ArrayCreate ::temp154 9                                  ;@line 1257
						Assign yawMatrix ::temp154                               ;@line 1257
						ArrayCreate ::temp154 9                                  ;@line 1258
						Assign pitchMatrix ::temp154                             ;@line 1258
						ArrayCreate ::temp154 9                                  ;@line 1259
						Assign rootWorldMatrix ::temp154                         ;@line 1259
						ArrayCreate ::temp154 9                                  ;@line 1260
						Assign muzzleWorldMatrix ::temp154                       ;@line 1260
						ArrayCreate ::temp154 3                                  ;@line 1261
						Assign rootPosition ::temp154                            ;@line 1261
						ArrayCreate ::temp154 3                                  ;@line 1262
						Assign muzzlePosition ::temp154                          ;@line 1262
						Cast ::temp152 self                                      ;@line 1263
						CallStatic netimmerse GetNodeLocalRotationMatrix ::temp155 ::temp152 ::YawNode_var yawBase False  ;@line 1263
						Not ::temp155 ::temp155                                  ;@line 1263
						Cast ::temp155 ::temp155                                 ;@line 1263
						JumpT ::temp155 _label540                                ;@line 1263
						Cast ::temp152 self                                      ;@line 1263
						CallStatic netimmerse GetNodeLocalRotationMatrix ::temp156 ::temp152 ::PitchNode_var pitchBase False  ;@line 1263
						Not ::temp156 ::temp156                                  ;@line 1263
						Cast ::temp155 ::temp156                                 ;@line 1263
					_label540:
						JumpF ::temp155 _label541                                ;@line 1263
						Assign matrixFailure "MATRIX_READ_FAILED: no se pudieron capturar los controles de giro."  ;@line 1264
						Return False                                             ;@line 1265
						Jump _label541                                           ;@line 1265
					_label541:
						Assign matricesReady True                                ;@line 1267
						Jump _label539                                           ;@line 1267
					_label539:
						Return True                                              ;@line 1269
					.endCode
				.endFunction
				.function SampleLookAimResult
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Int
					.paramTable
						.param expectedGeneration Int
					.endParamTable
					.localTable
						.local ::temp144 Bool
						.local ::temp145 Bool
						.local ::temp146 Bool
						.local ::temp147 Float
						.local ::temp148 Float
						.local ::temp149 Int
						.local ::NoneVar None
						.local heading Float
						.local angleX Float
						.local horizontal Float
						.local wx Float
						.local wy Float
						.local wz Float
						.local lx Float
						.local ly Float
						.local lz Float
						.local lengthSquared Float
						.local vectorMagnitude Float
						.local nextYaw Float
						.local nextPitch Float
						.local currentLease Bool
						.local cameraState Int
						.local menuOpen Bool
					.endLocalTable
					.code
						Not ::temp144 operating                                  ;@line 1151
						Cast ::temp144 ::temp144                                 ;@line 1151
						JumpT ::temp144 _label542                                ;@line 1151
						Cast ::temp144 cameraEntryPending                        ;@line 1151
					_label542:
						Cast ::temp144 ::temp144                                 ;@line 1151
						JumpT ::temp144 _label543                                ;@line 1151
						CompareEQ ::temp145 generation expectedGeneration        ;@line 1151
						Not ::temp145 ::temp145                                  ;@line 1151
						Cast ::temp144 ::temp145                                 ;@line 1151
					_label543:
						Cast ::temp145 ::temp144                                 ;@line 1151
						JumpT ::temp145 _label544                                ;@line 1151
						Cast ::temp145 inputPaused                               ;@line 1151
					_label544:
						Cast ::temp144 ::temp145                                 ;@line 1151
						JumpT ::temp144 _label545                                ;@line 1151
						Cast ::temp144 menuWasOpen                               ;@line 1151
					_label545:
						Cast ::temp144 ::temp144                                 ;@line 1151
						JumpT ::temp144 _label546                                ;@line 1151
						CallStatic utility IsInMenuMode ::temp145                ;@line 1151
						Cast ::temp144 ::temp145                                 ;@line 1151
					_label546:
						Cast ::temp146 ::temp144                                 ;@line 1151
						JumpT ::temp146 _label547                                ;@line 1151
						CompareEQ ::temp145 phase 0                              ;@line 1151
						Not ::temp145 ::temp145                                  ;@line 1151
						Cast ::temp145 ::temp145                                 ;@line 1151
						JumpF ::temp145 _label548                                ;@line 1151
						CompareEQ ::temp146 phase 3                              ;@line 1151
						Not ::temp146 ::temp146                                  ;@line 1151
						Cast ::temp145 ::temp146                                 ;@line 1151
					_label548:
						Cast ::temp145 ::temp145                                 ;@line 1151
						JumpF ::temp145 _label549                                ;@line 1151
						Not ::temp146 shotCommitted                              ;@line 1151
						Cast ::temp145 ::temp146                                 ;@line 1151
					_label549:
						Cast ::temp146 ::temp145                                 ;@line 1151
					_label547:
						JumpF ::temp146 _label550                                ;@line 1151
						Return 0                                                 ;@line 1152
						Jump _label550                                           ;@line 1152
					_label550:
						CallMethod GetAngleZ player ::temp147                    ;@line 1154
						Assign heading ::temp147                                 ;@line 1154
						CallMethod GetAngleX player ::temp147                    ;@line 1155
						Assign angleX ::temp147                                  ;@line 1155
						CompareEQ ::temp144 heading heading                      ;@line 1156
						Not ::temp144 ::temp144                                  ;@line 1156
						Cast ::temp146 ::temp144                                 ;@line 1156
						JumpT ::temp146 _label551                                ;@line 1156
						CompareEQ ::temp145 angleX angleX                        ;@line 1156
						Not ::temp145 ::temp145                                  ;@line 1156
						Cast ::temp146 ::temp145                                 ;@line 1156
					_label551:
						Cast ::temp145 ::temp146                                 ;@line 1156
						JumpT ::temp145 _label552                                ;@line 1156
						CallStatic math Abs ::temp147 heading                    ;@line 1156
						CompareGT ::temp144 ::temp147 720.000000                 ;@line 1156
						Cast ::temp145 ::temp144                                 ;@line 1156
					_label552:
						Cast ::temp144 ::temp145                                 ;@line 1156
						JumpT ::temp144 _label553                                ;@line 1156
						CallStatic math Abs ::temp147 angleX                     ;@line 1156
						CompareGT ::temp146 ::temp147 360.000000                 ;@line 1156
						Cast ::temp144 ::temp146                                 ;@line 1156
					_label553:
						Cast ::temp145 ::temp144                                 ;@line 1156
						JumpT ::temp145 _label554                                ;@line 1156
						CallMethod ReadAimRoot self ::temp145                    ;@line 1156
						Not ::temp146 ::temp145                                  ;@line 1156
						Cast ::temp145 ::temp146                                 ;@line 1156
					_label554:
						JumpF ::temp145 _label555                                ;@line 1156
						Return -1                                                ;@line 1157
						Jump _label555                                           ;@line 1157
					_label555:
						CompareGT ::temp144 angleX 180.000000                    ;@line 1160
						JumpF ::temp144 _label556                                ;@line 1160
						FSubtract ::temp147 angleX 360.000000                    ;@line 1161
						Assign angleX ::temp147                                  ;@line 1161
						Jump _label555                                           ;@line 1161
					_label556:
						CompareLTE ::temp146 angleX -180.000000                  ;@line 1163
						JumpF ::temp146 _label557                                ;@line 1163
						FAdd ::temp147 angleX 360.000000                         ;@line 1164
						Assign angleX ::temp147                                  ;@line 1164
						Jump _label556                                           ;@line 1164
					_label557:
						FNegate ::temp147 angleX                                 ;@line 1166
						CallStatic math Cos ::temp147 ::temp147                  ;@line 1166
						Assign horizontal ::temp147                              ;@line 1166
						CallStatic math Sin ::temp147 heading                    ;@line 1167
						FMultiply ::temp147 ::temp147 horizontal                 ;@line 1167
						Assign wx ::temp147                                      ;@line 1167
						CallStatic math Cos ::temp147 heading                    ;@line 1168
						FMultiply ::temp147 ::temp147 horizontal                 ;@line 1168
						Assign wy ::temp147                                      ;@line 1168
						FNegate ::temp147 angleX                                 ;@line 1169
						CallStatic math Sin ::temp147 ::temp147                  ;@line 1169
						Assign wz ::temp147                                      ;@line 1169
						ArrayGetElement ::temp147 rootWorldMatrix 0              ;@line 1171
						FMultiply ::temp147 ::temp147 wx                         ;@line 1171
						ArrayGetElement ::temp148 rootWorldMatrix 3              ;@line 1171
						FMultiply ::temp148 ::temp148 wy                         ;@line 1171
						FAdd ::temp147 ::temp147 ::temp148                       ;@line 1171
						ArrayGetElement ::temp148 rootWorldMatrix 6              ;@line 1171
						FMultiply ::temp148 ::temp148 wz                         ;@line 1171
						FAdd ::temp147 ::temp147 ::temp148                       ;@line 1171
						Assign lx ::temp147                                      ;@line 1171
						ArrayGetElement ::temp148 rootWorldMatrix 1              ;@line 1172
						FMultiply ::temp147 ::temp148 wx                         ;@line 1172
						ArrayGetElement ::temp148 rootWorldMatrix 4              ;@line 1172
						FMultiply ::temp148 ::temp148 wy                         ;@line 1172
						FAdd ::temp147 ::temp147 ::temp148                       ;@line 1172
						ArrayGetElement ::temp148 rootWorldMatrix 7              ;@line 1172
						FMultiply ::temp148 ::temp148 wz                         ;@line 1172
						FAdd ::temp147 ::temp147 ::temp148                       ;@line 1172
						Assign ly ::temp147                                      ;@line 1172
						ArrayGetElement ::temp148 rootWorldMatrix 2              ;@line 1173
						FMultiply ::temp147 ::temp148 wx                         ;@line 1173
						ArrayGetElement ::temp148 rootWorldMatrix 5              ;@line 1173
						FMultiply ::temp148 ::temp148 wy                         ;@line 1173
						FAdd ::temp147 ::temp147 ::temp148                       ;@line 1173
						ArrayGetElement ::temp148 rootWorldMatrix 8              ;@line 1173
						FMultiply ::temp148 ::temp148 wz                         ;@line 1173
						FAdd ::temp147 ::temp147 ::temp148                       ;@line 1173
						Assign lz ::temp147                                      ;@line 1173
						FMultiply ::temp148 lx lx                                ;@line 1174
						FMultiply ::temp147 ly ly                                ;@line 1174
						FAdd ::temp148 ::temp148 ::temp147                       ;@line 1174
						FMultiply ::temp147 lz lz                                ;@line 1174
						FAdd ::temp148 ::temp148 ::temp147                       ;@line 1174
						Assign lengthSquared ::temp148                           ;@line 1174
						CompareEQ ::temp145 lengthSquared lengthSquared          ;@line 1175
						Not ::temp145 ::temp145                                  ;@line 1175
						Cast ::temp146 ::temp145                                 ;@line 1175
						JumpT ::temp146 _label558                                ;@line 1175
						CompareLT ::temp144 lengthSquared 0.990000               ;@line 1175
						Cast ::temp146 ::temp144                                 ;@line 1175
					_label558:
						Cast ::temp144 ::temp146                                 ;@line 1175
						JumpT ::temp144 _label559                                ;@line 1175
						CompareGT ::temp145 lengthSquared 1.010000               ;@line 1175
						Cast ::temp144 ::temp145                                 ;@line 1175
					_label559:
						JumpF ::temp144 _label560                                ;@line 1175
						Return -1                                                ;@line 1176
						Jump _label560                                           ;@line 1176
					_label560:
						CallStatic math Sqrt ::temp147 lengthSquared             ;@line 1178
						Assign vectorMagnitude ::temp147                         ;@line 1178
						FDivide ::temp148 lx vectorMagnitude                     ;@line 1179
						Assign lx ::temp148                                      ;@line 1179
						FDivide ::temp147 ly vectorMagnitude                     ;@line 1180
						Assign ly ::temp147                                      ;@line 1180
						FDivide ::temp148 lz vectorMagnitude                     ;@line 1181
						Assign lz ::temp148                                      ;@line 1181
						CompareGT ::temp146 lz 1.000000                          ;@line 1182
						JumpF ::temp146 _label561                                ;@line 1182
						Assign lz 1.000000                                       ;@line 1183
						Jump _label562                                           ;@line 1183
					_label561:
						CompareLT ::temp145 lz -1.000000                         ;@line 1184
						JumpF ::temp145 _label562                                ;@line 1184
						Assign lz -1.000000                                      ;@line 1185
						Jump _label562                                           ;@line 1185
					_label562:
						FNegate ::temp147 ly                                     ;@line 1187
						CallMethod HeadingFromVector self ::temp148 lx ::temp147 yaw  ;@line 1187
						Assign nextYaw ::temp148                                 ;@line 1187
						CallStatic math ASin ::temp147 lz                        ;@line 1188
						Assign nextPitch ::temp147                               ;@line 1188
						CompareGT ::temp144 nextPitch ::PitchMax_var             ;@line 1189
						JumpF ::temp144 _label563                                ;@line 1189
						Assign nextPitch ::PitchMax_var                          ;@line 1190
						Jump _label564                                           ;@line 1190
					_label563:
						CompareLT ::temp145 nextPitch ::PitchMin_var             ;@line 1191
						JumpF ::temp145 _label564                                ;@line 1191
						Assign nextPitch ::PitchMin_var                          ;@line 1192
						Jump _label564                                           ;@line 1192
					_label564:
						CallMethod IsCurrent ::Session_var ::temp146 self token  ;@line 1196
						Assign currentLease ::temp146                            ;@line 1196
						CallMethod ReadCameraState self ::temp149                ;@line 1197
						Assign cameraState ::temp149                             ;@line 1197
						CallStatic utility IsInMenuMode ::temp145                ;@line 1198
						Assign menuOpen ::temp145                                ;@line 1198
						Not ::temp144 operating                                  ;@line 1199
						Cast ::temp145 ::temp144                                 ;@line 1199
						JumpT ::temp145 _label565                                ;@line 1199
						CompareEQ ::temp146 generation expectedGeneration        ;@line 1199
						Not ::temp146 ::temp146                                  ;@line 1199
						Cast ::temp145 ::temp146                                 ;@line 1199
					_label565:
						Cast ::temp144 ::temp145                                 ;@line 1199
						JumpT ::temp144 _label566                                ;@line 1199
						Cast ::temp144 cameraEntryPending                        ;@line 1199
					_label566:
						JumpF ::temp144 _label567                                ;@line 1199
						Return 0                                                 ;@line 1200
						Jump _label567                                           ;@line 1200
					_label567:
						Not ::temp146 currentLease                               ;@line 1202
						JumpF ::temp146 _label568                                ;@line 1202
						Return -1                                                ;@line 1203
						Jump _label568                                           ;@line 1203
					_label568:
						Cast ::temp145 menuOpen                                  ;@line 1205
						JumpT ::temp145 _label569                                ;@line 1205
						Cast ::temp145 inputPaused                               ;@line 1205
					_label569:
						Cast ::temp144 ::temp145                                 ;@line 1205
						JumpT ::temp144 _label570                                ;@line 1205
						Cast ::temp144 menuWasOpen                               ;@line 1205
					_label570:
						JumpF ::temp144 _label571                                ;@line 1205
						Return 0                                                 ;@line 1206
						Jump _label571                                           ;@line 1206
					_label571:
						CompareEQ ::temp146 cameraState 0                        ;@line 1208
						Not ::temp146 ::temp146                                  ;@line 1208
						JumpF ::temp146 _label572                                ;@line 1208
						Return -1                                                ;@line 1209
						Jump _label572                                           ;@line 1209
					_label572:
						CompareEQ ::temp145 phase 0                              ;@line 1211
						Not ::temp145 ::temp145                                  ;@line 1211
						Cast ::temp146 ::temp145                                 ;@line 1211
						JumpF ::temp146 _label573                                ;@line 1211
						CompareEQ ::temp144 phase 3                              ;@line 1211
						Not ::temp144 ::temp144                                  ;@line 1211
						Cast ::temp146 ::temp144                                 ;@line 1211
					_label573:
						Cast ::temp144 ::temp146                                 ;@line 1211
						JumpF ::temp144 _label574                                ;@line 1211
						Not ::temp145 shotCommitted                              ;@line 1211
						Cast ::temp144 ::temp145                                 ;@line 1211
					_label574:
						JumpF ::temp144 _label575                                ;@line 1211
						Return 0                                                 ;@line 1212
						Jump _label575                                           ;@line 1212
					_label575:
						Assign yaw nextYaw                                       ;@line 1214
						Assign pitch nextPitch                                   ;@line 1215
						CallMethod ApplyAim self ::NoneVar                       ;@line 1216
						Return 1                                                 ;@line 1217
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
						CallMethod BlockActivation self ::NoneVar True           ;@line 108
					.endCode
				.endFunction
				.function PlayGuardiaDemo
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp13 Bool
						.local ::NoneVar None
						.local ::temp14 Float
						.local demoStarted Bool
					.endLocalTable
					.code
						Cast ::temp13 operating                                  ;@line 209
						JumpT ::temp13 _label576                                 ;@line 209
						Cast ::temp13 endingSession                              ;@line 209
					_label576:
						JumpF ::temp13 _label577                                 ;@line 209
						Return None                                              ;@line 210
						Jump _label577                                           ;@line 210
					_label577:
						CallStatic debug Trace ::NoneVar "AstraAsedio demo del guardia (GuardiaCiclo)" 0  ;@line 212
						JumpF ::OcupadaGuardia_var _label578                     ;@line 213
						Cast ::temp14 1                                          ;@line 214
						CallMethod SetValue ::OcupadaGuardia_var ::NoneVar ::temp14  ;@line 214
						CallMethod RegisterForSingleUpdate self ::NoneVar 26.000000  ;@line 215
						Jump _label578                                           ;@line 215
					_label578:
						CallMethod PlayGamebryoAnimation self ::temp13 "GuardiaCiclo" True 0.000000  ;@line 217
						Assign demoStarted ::temp13                              ;@line 217
						Not ::temp13 demoStarted                                 ;@line 218
						JumpF ::temp13 _label579                                 ;@line 218
						CallStatic debug Trace ::NoneVar "AstraAsedio GUARDIA_CICLO_MISSING: la secuencia no estÃ¡ en el NIF (corrÃ© build_guardia.py)" 0  ;@line 219
						Jump _label579                                           ;@line 219
					_label579:
					.endCode
				.endFunction
				.function SightSampleCurrent
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param expectedGeneration Int
						.param expectedToken Int
						.param freeze Bool
					.endParamTable
					.localTable
						.local ::temp136 Bool
						.local ::temp137 Bool
						.local ::temp138 Bool
					.endLocalTable
					.code
						Not ::temp136 operating                                  ;@line 1115
						Cast ::temp136 ::temp136                                 ;@line 1115
						JumpT ::temp136 _label580                                ;@line 1115
						Cast ::temp136 cameraEntryPending                        ;@line 1115
					_label580:
						Cast ::temp136 ::temp136                                 ;@line 1115
						JumpT ::temp136 _label581                                ;@line 1115
						CompareEQ ::temp137 generation expectedGeneration        ;@line 1115
						Not ::temp137 ::temp137                                  ;@line 1115
						Cast ::temp136 ::temp137                                 ;@line 1115
					_label581:
						Cast ::temp136 ::temp136                                 ;@line 1115
						JumpT ::temp136 _label582                                ;@line 1115
						CompareEQ ::temp137 token expectedToken                  ;@line 1115
						Not ::temp137 ::temp137                                  ;@line 1115
						Cast ::temp136 ::temp137                                 ;@line 1115
					_label582:
						Cast ::temp137 ::temp136                                 ;@line 1115
						JumpT ::temp137 _label583                                ;@line 1115
						Cast ::temp137 inputPaused                               ;@line 1115
					_label583:
						Cast ::temp136 ::temp137                                 ;@line 1115
						JumpT ::temp136 _label584                                ;@line 1115
						Cast ::temp136 menuWasOpen                               ;@line 1115
					_label584:
						JumpF ::temp136 _label585                                ;@line 1115
						Return False                                             ;@line 1116
						Jump _label585                                           ;@line 1116
					_label585:
						JumpF freeze _label586                                   ;@line 1118
						CompareEQ ::temp137 phase 1                              ;@line 1119
						Cast ::temp137 ::temp137                                 ;@line 1119
						JumpF ::temp137 _label587                                ;@line 1119
						CompareEQ ::temp136 shotGeneration expectedGeneration    ;@line 1119
						Cast ::temp137 ::temp136                                 ;@line 1119
					_label587:
						Cast ::temp137 ::temp137                                 ;@line 1119
						JumpF ::temp137 _label588                                ;@line 1119
						Not ::temp136 shotCommitted                              ;@line 1119
						Cast ::temp137 ::temp136                                 ;@line 1119
					_label588:
						Return ::temp137                                         ;@line 1119
						Jump _label586                                           ;@line 1119
					_label586:
						CompareEQ ::temp136 phase 0                              ;@line 1121
						Cast ::temp136 ::temp136                                 ;@line 1121
						JumpT ::temp136 _label589                                ;@line 1121
						CompareEQ ::temp138 phase 3                              ;@line 1121
						Cast ::temp136 ::temp138                                 ;@line 1121
					_label589:
						Cast ::temp138 ::temp136                                 ;@line 1121
						JumpT ::temp138 _label590                                ;@line 1121
						Cast ::temp138 shotCommitted                             ;@line 1121
					_label590:
						Return ::temp138                                         ;@line 1121
					.endCode
				.endFunction
				.function ResetStationAim
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp236 Bool
					.endLocalTable
					.code
						Cast ::temp236 operating                                 ;@line 2071
						JumpT ::temp236 _label591                                ;@line 2071
						Cast ::temp236 endingSession                             ;@line 2071
					_label591:
						JumpF ::temp236 _label592                                ;@line 2071
						Return None                                              ;@line 2072
						Jump _label592                                           ;@line 2072
					_label592:
						Assign yaw 0.000000                                      ;@line 2075
						Assign pitch 0.000000                                    ;@line 2076
						Assign matricesReady False                               ;@line 2077
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
				.function ThawSight
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param frozenGeneration Int
						.param frozenToken Int
					.endParamTable
					.localTable
						.local ::temp139 Bool
						.local ::temp140 Bool
						.local ::temp141 ObjectReference
						.local thawed Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						Not ::temp139 ::UseSightCamera_var                       ;@line 1125
						Cast ::temp139 ::temp139                                 ;@line 1125
						JumpT ::temp139 _label593                                ;@line 1125
						Not ::temp140 operating                                  ;@line 1125
						Cast ::temp139 ::temp140                                 ;@line 1125
					_label593:
						Cast ::temp139 ::temp139                                 ;@line 1125
						JumpT ::temp139 _label594                                ;@line 1125
						CompareEQ ::temp140 token frozenToken                    ;@line 1125
						Not ::temp140 ::temp140                                  ;@line 1125
						Cast ::temp139 ::temp140                                 ;@line 1125
					_label594:
						Cast ::temp139 ::temp139                                 ;@line 1125
						JumpT ::temp139 _label595                                ;@line 1125
						CompareEQ ::temp140 sightFreezeGeneration frozenGeneration  ;@line 1125
						Not ::temp140 ::temp140                                  ;@line 1125
						Cast ::temp139 ::temp140                                 ;@line 1125
					_label595:
						JumpF ::temp139 _label596                                ;@line 1125
						Return None                                              ;@line 1126
						Jump _label596                                           ;@line 1126
					_label596:
						Assign sightThawPending True                             ;@line 1129
						Not ::temp140 sightFreezePending                         ;@line 1130
						JumpF ::temp140 _label597                                ;@line 1130
						Assign sightFreezeGeneration -1                          ;@line 1131
						Jump _label597                                           ;@line 1131
					_label597:
						Cast ::temp141 self                                      ;@line 1133
						CallStatic astrasightnative SetFrozen ::temp139 ::temp141 frozenToken False  ;@line 1133
						Assign thawed ::temp139                                  ;@line 1133
						Not ::temp140 operating                                  ;@line 1134
						Cast ::temp140 ::temp140                                 ;@line 1134
						JumpT ::temp140 _label598                                ;@line 1134
						CompareEQ ::temp139 token frozenToken                    ;@line 1134
						Not ::temp139 ::temp139                                  ;@line 1134
						Cast ::temp140 ::temp139                                 ;@line 1134
					_label598:
						JumpF ::temp140 _label599                                ;@line 1134
						Return None                                              ;@line 1135
						Jump _label599                                           ;@line 1135
					_label599:
						Assign sightThawPending False                            ;@line 1137
						Not ::temp139 thawed                                     ;@line 1138
						JumpF ::temp139 _label600                                ;@line 1138
						CallMethod RejectShot self ::NoneVar "NATIVE_SIGHT_THAW_FAILED: se perdiÃ³ la mira nativa."  ;@line 1139
						CallMethod EndSession self ::NoneVar                     ;@line 1140
						Jump _label600                                           ;@line 1140
					_label600:
					.endCode
				.endFunction
				.function CleanupCurrent
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param expectedGeneration Int
					.endParamTable
					.localTable
						.local ::temp234 Bool
						.local ::temp235 Bool
					.endLocalTable
					.code
						Cast ::temp234 endingSession                             ;@line 2059
						JumpF ::temp234 _label601                                ;@line 2059
						CompareEQ ::temp234 generation expectedGeneration        ;@line 2059
						Cast ::temp234 ::temp234                                 ;@line 2059
					_label601:
						Cast ::temp234 ::temp234                                 ;@line 2059
						JumpF ::temp234 _label602                                ;@line 2059
						CompareEQ ::temp235 token -1                             ;@line 2059
						Cast ::temp234 ::temp235                                 ;@line 2059
					_label602:
						Cast ::temp234 ::temp234                                 ;@line 2059
						JumpF ::temp234 _label603                                ;@line 2059
						Not ::temp235 operating                                  ;@line 2059
						Cast ::temp234 ::temp235                                 ;@line 2059
					_label603:
						Return ::temp234                                         ;@line 2059
					.endCode
				.endFunction
				.function RecoverStationLoad
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp4 Int
						.local ::temp5 astraasediosession
						.local ::temp6 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						JumpF endingSession _label604                            ;@line 149
						Assign endingSession False                               ;@line 150
						IAdd ::temp4 generation 1                                ;@line 151
						Assign generation ::temp4                                ;@line 151
						Cast ::temp5 None                                        ;@line 152
						CompareEQ ::temp6 ::Session_var ::temp5                  ;@line 152
						Not ::temp6 ::temp6                                      ;@line 152
						JumpF ::temp6 _label605                                  ;@line 152
						CallMethod EmergencyCleanup ::Session_var ::NoneVar      ;@line 153
						Jump _label605                                           ;@line 153
					_label605:
						Jump _label604                                           ;@line 153
					_label604:
						Cast ::temp6 operating                                   ;@line 156
						JumpT ::temp6 _label606                                  ;@line 156
						Cast ::temp6 nativeSightRequested                        ;@line 156
					_label606:
						JumpF ::temp6 _label607                                  ;@line 156
						CallMethod EndSession self ::NoneVar                     ;@line 157
						Jump _label607                                           ;@line 157
					_label607:
					.endCode
				.endFunction
				.function RequestFireMode
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp40 Bool
						.local ::temp41 Bool
						.local ::NoneVar None
						.local modeGeneration Int
						.local modeToken Int
						.local pressReleaseSerial Int
						.local readyForMode Bool
						.local releasedDuringPress Bool
					.endLocalTable
					.code
						JumpF ::UseSightCamera_var _label608                     ;@line 530
						Return None                                              ;@line 531
						Jump _label608                                           ;@line 531
					_label608:
						Assign modeGeneration generation                         ;@line 533
						Assign modeToken token                                   ;@line 534
						Assign pressReleaseSerial modeReleaseSerial              ;@line 535
						CallMethod InputReady self ::temp40                      ;@line 536
						Assign readyForMode ::temp40                             ;@line 536
						Not ::temp40 operating                                   ;@line 537
						Cast ::temp40 ::temp40                                   ;@line 537
						JumpT ::temp40 _label609                                 ;@line 537
						CompareEQ ::temp41 generation modeGeneration             ;@line 537
						Not ::temp41 ::temp41                                    ;@line 537
						Cast ::temp40 ::temp41                                   ;@line 537
					_label609:
						Cast ::temp40 ::temp40                                   ;@line 537
						JumpT ::temp40 _label610                                 ;@line 537
						CompareEQ ::temp41 token modeToken                       ;@line 537
						Not ::temp41 ::temp41                                    ;@line 537
						Cast ::temp40 ::temp41                                   ;@line 537
					_label610:
						JumpF ::temp40 _label611                                 ;@line 537
						Return None                                              ;@line 538
						Jump _label611                                           ;@line 538
					_label611:
						CompareEQ ::temp41 modeReleaseSerial pressReleaseSerial  ;@line 540
						Not ::temp41 ::temp41                                    ;@line 540
						Assign releasedDuringPress ::temp41                      ;@line 540
						Not ::temp40 readyForMode                                ;@line 541
						JumpF ::temp40 _label612                                 ;@line 541
						Not ::temp41 releasedDuringPress                         ;@line 542
						Assign heldMode ::temp41                                 ;@line 542
						Return None                                              ;@line 543
						Jump _label612                                           ;@line 543
					_label612:
						JumpF heldMode _label613                                 ;@line 545
						Return None                                              ;@line 546
						Jump _label613                                           ;@line 546
					_label613:
						Not ::temp41 releasedDuringPress                         ;@line 548
						Assign heldMode ::temp41                                 ;@line 548
						Not ::temp40 ::ContinuousFire_var                        ;@line 549
						Assign ::ContinuousFire_var ::temp40                     ;@line 549
						CallMethod StopRepeatFire self ::NoneVar                 ;@line 550
						JumpF ::ContinuousFire_var _label614                     ;@line 552
						CallStatic debug Notification ::NoneVar "Astra: tiro continuo. MantÃ©n Ataque; Sprint cambia el modo."  ;@line 553
						Jump _label615                                           ;@line 553
					_label614:
						CallStatic debug Notification ::NoneVar "Astra: tiro individual. Sprint cambia el modo."  ;@line 555
					_label615:
					.endCode
				.endFunction
				.function BeginShot
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param expectedGeneration Int
						.param expectedRepeatRevision Int
					.endParamTable
					.localTable
						.local ::temp179 Bool
						.local ::temp180 Bool
						.local ::temp181 Bool
						.local ::temp183 form
						.local ::temp184 Int
						.local expectedToken Int
						.local shotSessionValid Bool
						.local shotMenuOpen Bool
						.local ::NoneVar None
						.local ::temp182 String
						.local shotAvailableAmmo Int
						.local freezeResult Int
						.local ::temp185 String
					.endLocalTable
					.code
						JumpF ::UseSightCamera_var _label616                     ;@line 1612
						Return None                                              ;@line 1613
						Jump _label616                                           ;@line 1613
					_label616:
						Assign expectedToken token                               ;@line 1615
						CallMethod InputReady self ::temp179                     ;@line 1616
						Cast ::temp179 ::temp179                                 ;@line 1616
						JumpF ::temp179 _label617                                ;@line 1616
						CallMethod CanOperate self ::temp180 expectedGeneration  ;@line 1616
						Cast ::temp179 ::temp180                                 ;@line 1616
					_label617:
						Assign shotSessionValid ::temp179                        ;@line 1616
						CallStatic utility IsInMenuMode ::temp180                ;@line 1617
						Assign shotMenuOpen ::temp180                            ;@line 1617
						Not ::temp179 operating                                  ;@line 1618
						Cast ::temp179 ::temp179                                 ;@line 1618
						JumpT ::temp179 _label618                                ;@line 1618
						CompareEQ ::temp180 generation expectedGeneration        ;@line 1618
						Not ::temp180 ::temp180                                  ;@line 1618
						Cast ::temp179 ::temp180                                 ;@line 1618
					_label618:
						Cast ::temp179 ::temp179                                 ;@line 1618
						JumpT ::temp179 _label619                                ;@line 1618
						CompareEQ ::temp180 token expectedToken                  ;@line 1618
						Not ::temp180 ::temp180                                  ;@line 1618
						Cast ::temp179 ::temp180                                 ;@line 1618
					_label619:
						JumpF ::temp179 _label620                                ;@line 1618
						Return None                                              ;@line 1619
						Jump _label620                                           ;@line 1619
					_label620:
						CompareEQ ::temp180 phase 0                              ;@line 1621
						JumpF ::temp180 _label621                                ;@line 1621
						CallMethod NormalizeTimingProperties self ::NoneVar      ;@line 1623
						Jump _label621                                           ;@line 1623
					_label621:
						CompareGTE ::temp179 expectedRepeatRevision 0            ;@line 1625
						Cast ::temp181 ::temp179                                 ;@line 1625
						JumpF ::temp181 _label622                                ;@line 1625
						Not ::temp180 ::ContinuousFire_var                       ;@line 1625
						Cast ::temp180 ::temp180                                 ;@line 1625
						JumpT ::temp180 _label623                                ;@line 1625
						Not ::temp181 repeatFire                                 ;@line 1625
						Cast ::temp180 ::temp181                                 ;@line 1625
					_label623:
						Cast ::temp180 ::temp180                                 ;@line 1625
						JumpT ::temp180 _label624                                ;@line 1625
						CompareEQ ::temp181 repeatRevision expectedRepeatRevision  ;@line 1625
						Not ::temp181 ::temp181                                  ;@line 1625
						Cast ::temp180 ::temp181                                 ;@line 1625
					_label624:
						Cast ::temp181 ::temp180                                 ;@line 1625
					_label622:
						JumpF ::temp181 _label625                                ;@line 1625
						Return None                                              ;@line 1626
						Jump _label625                                           ;@line 1626
					_label625:
						Cast ::temp179 shotMenuOpen                              ;@line 1628
						JumpT ::temp179 _label626                                ;@line 1628
						Cast ::temp179 inputPaused                               ;@line 1628
					_label626:
						Cast ::temp180 ::temp179                                 ;@line 1628
						JumpT ::temp180 _label627                                ;@line 1628
						Cast ::temp180 menuWasOpen                               ;@line 1628
					_label627:
						JumpF ::temp180 _label628                                ;@line 1628
						Return None                                              ;@line 1629
						Jump _label628                                           ;@line 1629
					_label628:
						Not ::temp181 shotSessionValid                           ;@line 1631
						JumpF ::temp181 _label629                                ;@line 1631
						CallMethod SessionFailureReason self ::temp182           ;@line 1632
						StrCat ::temp182 "SHOT_SESSION_INVALID: " ::temp182      ;@line 1632
						CallMethod RejectShot self ::NoneVar ::temp182           ;@line 1632
						JumpF ::UseSightCamera_var _label630                     ;@line 1633
						CallMethod EndSession self ::NoneVar                     ;@line 1634
						Jump _label630                                           ;@line 1634
					_label630:
						Return None                                              ;@line 1636
						Jump _label629                                           ;@line 1636
					_label629:
						Not ::temp179 ::UseSightCamera_var                       ;@line 1639
						Cast ::temp180 ::temp179                                 ;@line 1639
						JumpF ::temp180 _label631                                ;@line 1639
						Cast ::temp180 ::UseMouseAim_var                         ;@line 1639
					_label631:
						Cast ::temp181 ::temp180                                 ;@line 1639
						JumpF ::temp181 _label632                                ;@line 1639
						CallMethod SampleLookAim self ::temp181 expectedGeneration  ;@line 1639
						Not ::temp179 ::temp181                                  ;@line 1639
						Cast ::temp181 ::temp179                                 ;@line 1639
					_label632:
						JumpF ::temp181 _label633                                ;@line 1639
						CallMethod RejectShot self ::NoneVar "SHOT_AIM_SAMPLE_FAILED: mirada no disponible o sesiÃ³n cancelada."  ;@line 1640
						Return None                                              ;@line 1641
						Jump _label633                                           ;@line 1641
					_label633:
						Cast ::temp183 ::SteelBolt_var                           ;@line 1643
						CallMethod GetItemCount player ::temp184 ::temp183       ;@line 1643
						Assign shotAvailableAmmo ::temp184                       ;@line 1643
						Not ::temp180 operating                                  ;@line 1644
						Cast ::temp181 ::temp180                                 ;@line 1644
						JumpT ::temp181 _label634                                ;@line 1644
						CompareEQ ::temp179 generation expectedGeneration        ;@line 1644
						Not ::temp179 ::temp179                                  ;@line 1644
						Cast ::temp181 ::temp179                                 ;@line 1644
					_label634:
						Cast ::temp179 ::temp181                                 ;@line 1644
						JumpT ::temp179 _label635                                ;@line 1644
						CompareEQ ::temp180 token expectedToken                  ;@line 1644
						Not ::temp180 ::temp180                                  ;@line 1644
						Cast ::temp179 ::temp180                                 ;@line 1644
					_label635:
						Cast ::temp180 ::temp179                                 ;@line 1644
						JumpT ::temp180 _label636                                ;@line 1644
						CompareEQ ::temp181 phase 0                              ;@line 1644
						Not ::temp181 ::temp181                                  ;@line 1644
						Cast ::temp180 ::temp181                                 ;@line 1644
					_label636:
						JumpF ::temp180 _label637                                ;@line 1644
						Return None                                              ;@line 1645
						Jump _label637                                           ;@line 1645
					_label637:
						CompareLT ::temp179 shotAvailableAmmo 1                  ;@line 1647
						JumpF ::temp179 _label638                                ;@line 1647
						CallMethod StopRepeatFire self ::NoneVar                 ;@line 1648
						CallMethod RejectShot self ::NoneVar "SHOT_NO_STEEL_BOLT: necesita un virote de acero."  ;@line 1649
						Return None                                              ;@line 1650
						Jump _label638                                           ;@line 1650
					_label638:
						Not ::temp181 operating                                  ;@line 1653
						Cast ::temp179 ::temp181                                 ;@line 1653
						JumpT ::temp179 _label639                                ;@line 1653
						CompareEQ ::temp180 generation expectedGeneration        ;@line 1653
						Not ::temp180 ::temp180                                  ;@line 1653
						Cast ::temp179 ::temp180                                 ;@line 1653
					_label639:
						Cast ::temp180 ::temp179                                 ;@line 1653
						JumpT ::temp180 _label640                                ;@line 1653
						CompareEQ ::temp181 token expectedToken                  ;@line 1653
						Not ::temp181 ::temp181                                  ;@line 1653
						Cast ::temp180 ::temp181                                 ;@line 1653
					_label640:
						Cast ::temp179 ::temp180                                 ;@line 1653
						JumpT ::temp179 _label641                                ;@line 1653
						Cast ::temp179 cameraEntryPending                        ;@line 1653
					_label641:
						Cast ::temp181 ::temp179                                 ;@line 1653
						JumpT ::temp181 _label642                                ;@line 1653
						Cast ::temp181 inputPaused                               ;@line 1653
					_label642:
						Cast ::temp180 ::temp181                                 ;@line 1653
						JumpT ::temp180 _label643                                ;@line 1653
						Cast ::temp180 menuWasOpen                               ;@line 1653
					_label643:
						Cast ::temp181 ::temp180                                 ;@line 1653
						JumpT ::temp181 _label644                                ;@line 1653
						CompareEQ ::temp179 phase 0                              ;@line 1653
						Not ::temp179 ::temp179                                  ;@line 1653
						Cast ::temp181 ::temp179                                 ;@line 1653
					_label644:
						Cast ::temp180 ::temp181                                 ;@line 1653
						JumpT ::temp180 _label645                                ;@line 1653
						Cast ::temp180 sightFreezePending                        ;@line 1653
					_label645:
						Cast ::temp179 ::temp180                                 ;@line 1653
						JumpT ::temp179 _label646                                ;@line 1653
						Cast ::temp179 sightThawPending                          ;@line 1653
					_label646:
						JumpF ::temp179 _label647                                ;@line 1653
						CallMethod RejectShot self ::NoneVar "SHOT_STALE_BEFORE_FREEZE: sesiÃ³n cancelada durante el apuntado."  ;@line 1654
						Return None                                              ;@line 1655
						Jump _label647                                           ;@line 1655
					_label647:
						CompareGTE ::temp181 expectedRepeatRevision 0            ;@line 1657
						Cast ::temp179 ::temp181                                 ;@line 1657
						JumpF ::temp179 _label648                                ;@line 1657
						Not ::temp180 ::ContinuousFire_var                       ;@line 1657
						Cast ::temp180 ::temp180                                 ;@line 1657
						JumpT ::temp180 _label649                                ;@line 1657
						Not ::temp179 repeatFire                                 ;@line 1657
						Cast ::temp180 ::temp179                                 ;@line 1657
					_label649:
						Cast ::temp180 ::temp180                                 ;@line 1657
						JumpT ::temp180 _label650                                ;@line 1657
						CompareEQ ::temp179 repeatRevision expectedRepeatRevision  ;@line 1657
						Not ::temp179 ::temp179                                  ;@line 1657
						Cast ::temp180 ::temp179                                 ;@line 1657
					_label650:
						Cast ::temp179 ::temp180                                 ;@line 1657
					_label648:
						JumpF ::temp179 _label651                                ;@line 1657
						Return None                                              ;@line 1658
						Jump _label651                                           ;@line 1658
					_label651:
						Assign shotGeneration expectedGeneration                 ;@line 1660
						Assign shotCommitted False                               ;@line 1661
						Assign needsReset True                                   ;@line 1662
						Assign settleFrames 0                                    ;@line 1663
						Assign phase 1                                           ;@line 1664
						JumpF ::UseSightCamera_var _label652                     ;@line 1665
						Assign sightFreezeGeneration expectedGeneration          ;@line 1667
						Assign sightFreezePending True                           ;@line 1668
						CallMethod SampleSightAimResult self ::temp184 expectedGeneration True  ;@line 1669
						Assign freezeResult ::temp184                            ;@line 1669
						Not ::temp181 operating                                  ;@line 1670
						Cast ::temp179 ::temp181                                 ;@line 1670
						JumpT ::temp179 _label653                                ;@line 1670
						CompareEQ ::temp180 token expectedToken                  ;@line 1670
						Not ::temp180 ::temp180                                  ;@line 1670
						Cast ::temp179 ::temp180                                 ;@line 1670
					_label653:
						Cast ::temp180 ::temp179                                 ;@line 1670
						JumpT ::temp180 _label654                                ;@line 1670
						CompareEQ ::temp181 sightFreezeGeneration expectedGeneration  ;@line 1670
						Not ::temp181 ::temp181                                  ;@line 1670
						Cast ::temp180 ::temp181                                 ;@line 1670
					_label654:
						JumpF ::temp180 _label655                                ;@line 1670
						Return None                                              ;@line 1671
						Jump _label655                                           ;@line 1671
					_label655:
						Assign sightFreezePending False                          ;@line 1673
						CompareEQ ::temp179 freezeResult 0                       ;@line 1674
						Cast ::temp180 ::temp179                                 ;@line 1674
						JumpT ::temp180 _label656                                ;@line 1674
						CompareEQ ::temp181 generation expectedGeneration        ;@line 1674
						Not ::temp181 ::temp181                                  ;@line 1674
						Cast ::temp180 ::temp181                                 ;@line 1674
					_label656:
						Cast ::temp181 ::temp180                                 ;@line 1674
						JumpT ::temp181 _label657                                ;@line 1674
						CompareEQ ::temp179 phase 1                              ;@line 1674
						Not ::temp179 ::temp179                                  ;@line 1674
						Cast ::temp181 ::temp179                                 ;@line 1674
					_label657:
						JumpF ::temp181 _label658                                ;@line 1674
						CallMethod ThawSight self ::NoneVar expectedGeneration expectedToken  ;@line 1675
						Cast ::temp179 operating                                 ;@line 1678
						JumpF ::temp179 _label659                                ;@line 1678
						CompareEQ ::temp180 token expectedToken                  ;@line 1678
						Cast ::temp179 ::temp180                                 ;@line 1678
					_label659:
						Cast ::temp179 ::temp179                                 ;@line 1678
						JumpF ::temp179 _label660                                ;@line 1678
						CompareEQ ::temp180 generation expectedGeneration        ;@line 1678
						Cast ::temp179 ::temp180                                 ;@line 1678
					_label660:
						Cast ::temp179 ::temp179                                 ;@line 1678
						JumpF ::temp179 _label661                                ;@line 1678
						CompareEQ ::temp180 phase 1                              ;@line 1678
						Cast ::temp179 ::temp180                                 ;@line 1678
					_label661:
						Cast ::temp179 ::temp179                                 ;@line 1678
						JumpF ::temp179 _label662                                ;@line 1678
						Not ::temp180 shotCommitted                              ;@line 1678
						Cast ::temp179 ::temp180                                 ;@line 1678
					_label662:
						Cast ::temp179 ::temp179                                 ;@line 1678
						JumpF ::temp179 _label663                                ;@line 1678
						CompareEQ ::temp180 shotGeneration expectedGeneration    ;@line 1678
						Cast ::temp179 ::temp180                                 ;@line 1678
					_label663:
						JumpF ::temp179 _label664                                ;@line 1678
						Assign phase 0                                           ;@line 1679
						Assign needsReset False                                  ;@line 1680
						Assign shotGeneration -1                                 ;@line 1681
						Jump _label664                                           ;@line 1681
					_label664:
						Return None                                              ;@line 1683
						Jump _label658                                           ;@line 1683
					_label658:
						CompareLT ::temp180 freezeResult 0                       ;@line 1685
						JumpF ::temp180 _label665                                ;@line 1685
						CallMethod RejectShot self ::NoneVar "NATIVE_SIGHT_FREEZE_FAILED: no se pudo fijar el disparo."  ;@line 1686
						CallMethod EndSession self ::NoneVar                     ;@line 1687
						Return None                                              ;@line 1688
						Jump _label665                                           ;@line 1688
					_label665:
						Jump _label652                                           ;@line 1688
					_label652:
						JumpF ::QALog_var _label666                              ;@line 1691
						Cast ::temp182 yaw                                       ;@line 1692
						StrCat ::temp182 "AstraAsedio phase settle yaw=" ::temp182  ;@line 1692
						StrCat ::temp182 ::temp182 " pitch="                     ;@line 1692
						Cast ::temp185 pitch                                     ;@line 1692
						StrCat ::temp185 ::temp182 ::temp185                     ;@line 1692
						StrCat ::temp182 ::temp185 " generation="                ;@line 1692
						Cast ::temp185 generation                                ;@line 1692
						StrCat ::temp185 ::temp182 ::temp185                     ;@line 1692
						CallStatic debug Trace ::NoneVar ::temp185 0             ;@line 1692
						Jump _label666                                           ;@line 1692
					_label666:
					.endCode
				.endFunction
				.function RejectActivation
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param reason String
					.endParamTable
					.localTable
						.local ::temp27 String
						.local ::NoneVar None
					.endLocalTable
					.code
						StrCat ::temp27 "AstraAsedio activation rejected: " reason  ;@line 414
						CallStatic debug Trace ::NoneVar ::temp27 0              ;@line 414
						StrCat ::temp27 "Astra: " reason                         ;@line 415
						CallStatic debug Notification ::NoneVar ::temp27         ;@line 415
					.endCode
				.endFunction
				.function RegisterMenus
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod RegisterForMenu self ::NoneVar "InventoryMenu"  ;@line 419
						CallMethod RegisterForMenu self ::NoneVar "MagicMenu"    ;@line 420
						CallMethod RegisterForMenu self ::NoneVar "MapMenu"      ;@line 421
						CallMethod RegisterForMenu self ::NoneVar "Journal Menu"  ;@line 422
						CallMethod RegisterForMenu self ::NoneVar "TweenMenu"    ;@line 423
						CallMethod RegisterForMenu self ::NoneVar "Console"      ;@line 424
						CallMethod RegisterForMenu self ::NoneVar "Dialogue Menu"  ;@line 425
						CallMethod RegisterForMenu self ::NoneVar "Loading Menu"  ;@line 426
						CallMethod RegisterForMenu self ::NoneVar "BarterMenu"   ;@line 427
						CallMethod RegisterForMenu self ::NoneVar "ContainerMenu"  ;@line 428
						CallMethod RegisterForMenu self ::NoneVar "FavoritesMenu"  ;@line 429
						CallMethod RegisterForMenu self ::NoneVar "Sleep/Wait Menu"  ;@line 430
						CallMethod RegisterForMenu self ::NoneVar "MessageBoxMenu"  ;@line 431
					.endCode
				.endFunction
				.function UpdateAim
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param dt Float
					.endParamTable
					.localTable
						.local ::temp175 Int
						.local ::temp176 Bool
						.local ::temp177 Bool
						.local sightGeneration Int
						.local sightToken Int
						.local sightResult Int
						.local ::NoneVar None
						.local aimGeneration Int
						.local sampleResult Int
						.local ::temp178 Float
					.endLocalTable
					.code
						JumpF ::UseSightCamera_var _label667                     ;@line 1568
						Assign sightGeneration generation                        ;@line 1569
						Assign sightToken token                                  ;@line 1570
						CallMethod SampleSightAimResult self ::temp175 sightGeneration False  ;@line 1571
						Assign sightResult ::temp175                             ;@line 1571
						CompareLT ::temp176 sightResult 0                        ;@line 1572
						Cast ::temp176 ::temp176                                 ;@line 1572
						JumpF ::temp176 _label668                                ;@line 1572
						Cast ::temp176 operating                                 ;@line 1572
					_label668:
						Cast ::temp176 ::temp176                                 ;@line 1572
						JumpF ::temp176 _label669                                ;@line 1572
						CompareEQ ::temp177 generation sightGeneration           ;@line 1572
						Cast ::temp176 ::temp177                                 ;@line 1572
					_label669:
						Cast ::temp176 ::temp176                                 ;@line 1572
						JumpF ::temp176 _label670                                ;@line 1572
						CompareEQ ::temp177 token sightToken                     ;@line 1572
						Cast ::temp176 ::temp177                                 ;@line 1572
					_label670:
						JumpF ::temp176 _label671                                ;@line 1572
						CallMethod RejectShot self ::NoneVar "NATIVE_SIGHT_SAMPLE_FAILED: se perdiÃ³ la mira nativa."  ;@line 1573
						CallMethod EndSession self ::NoneVar                     ;@line 1574
						Jump _label671                                           ;@line 1574
					_label671:
						Return None                                              ;@line 1576
						Jump _label667                                           ;@line 1576
					_label667:
						JumpF ::UseMouseAim_var _label672                        ;@line 1578
						Assign aimGeneration generation                          ;@line 1579
						CallMethod SampleLookAimResult self ::temp175 aimGeneration  ;@line 1580
						Assign sampleResult ::temp175                            ;@line 1580
						CompareLT ::temp177 sampleResult 0                       ;@line 1581
						Cast ::temp176 ::temp177                                 ;@line 1581
						JumpF ::temp176 _label673                                ;@line 1581
						Cast ::temp176 operating                                 ;@line 1581
					_label673:
						Cast ::temp176 ::temp176                                 ;@line 1581
						JumpF ::temp176 _label674                                ;@line 1581
						CompareEQ ::temp177 generation aimGeneration             ;@line 1581
						Cast ::temp176 ::temp177                                 ;@line 1581
					_label674:
						JumpF ::temp176 _label675                                ;@line 1581
						CallMethod EndSession self ::NoneVar                     ;@line 1582
						Jump _label675                                           ;@line 1582
					_label675:
						Return None                                              ;@line 1584
						Jump _label672                                           ;@line 1584
					_label672:
						JumpF heldLeft _label676                                 ;@line 1586
						FMultiply ::temp178 ::YawSpeed_var dt                    ;@line 1587
						FAdd ::temp178 yaw ::temp178                             ;@line 1587
						Assign yaw ::temp178                                     ;@line 1587
						Jump _label676                                           ;@line 1587
					_label676:
						JumpF heldRight _label677                                ;@line 1589
						FMultiply ::temp178 ::YawSpeed_var dt                    ;@line 1590
						FSubtract ::temp178 yaw ::temp178                        ;@line 1590
						Assign yaw ::temp178                                     ;@line 1590
						Jump _label677                                           ;@line 1590
					_label677:
						JumpF heldUp _label678                                   ;@line 1592
						FMultiply ::temp178 ::PitchSpeed_var dt                  ;@line 1593
						FAdd ::temp178 pitch ::temp178                           ;@line 1593
						Assign pitch ::temp178                                   ;@line 1593
						Jump _label678                                           ;@line 1593
					_label678:
						JumpF heldDown _label679                                 ;@line 1595
						FMultiply ::temp178 ::PitchSpeed_var dt                  ;@line 1596
						FSubtract ::temp178 pitch ::temp178                      ;@line 1596
						Assign pitch ::temp178                                   ;@line 1596
						Jump _label679                                           ;@line 1596
					_label679:
						CompareGT ::temp177 pitch ::PitchMax_var                 ;@line 1598
						JumpF ::temp177 _label680                                ;@line 1598
						Assign pitch ::PitchMax_var                              ;@line 1599
						Jump _label681                                           ;@line 1599
					_label680:
						CompareLT ::temp176 pitch ::PitchMin_var                 ;@line 1600
						JumpF ::temp176 _label681                                ;@line 1600
						Assign pitch ::PitchMin_var                              ;@line 1601
						Jump _label681                                           ;@line 1601
					_label681:
						CompareGTE ::temp176 yaw 360.000000                      ;@line 1603
						JumpF ::temp176 _label682                                ;@line 1603
						FSubtract ::temp178 yaw 360.000000                       ;@line 1604
						Assign yaw ::temp178                                     ;@line 1604
						Jump _label683                                           ;@line 1604
					_label682:
						CompareLT ::temp177 yaw 0.000000                         ;@line 1605
						JumpF ::temp177 _label683                                ;@line 1605
						FAdd ::temp178 yaw 360.000000                            ;@line 1606
						Assign yaw ::temp178                                     ;@line 1606
						Jump _label683                                           ;@line 1606
					_label683:
						CallMethod ApplyAim self ::NoneVar                       ;@line 1608
					.endCode
				.endFunction
				.function ApplyAim
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp157 Bool
						.local ::temp158 Float
						.local ::temp162 ObjectReference
						.local applyGeneration Int
						.local yc Float
						.local ys Float
						.local pc Float
						.local ps Float
						.local j Int
						.local ::temp159 Float
						.local ::temp160 Int
						.local ::temp161 Float
					.endLocalTable
					.code
						Assign applyGeneration generation                        ;@line 1273
						Cast ::temp157 ::UseSightCamera_var                      ;@line 1274
						JumpF ::temp157 _label684                                ;@line 1274
						Cast ::temp157 operating                                 ;@line 1274
					_label684:
						JumpF ::temp157 _label685                                ;@line 1274
						Return None                                              ;@line 1275
						Jump _label685                                           ;@line 1275
					_label685:
						CallStatic math Cos ::temp158 yaw                        ;@line 1277
						Assign yc ::temp158                                      ;@line 1277
						CallStatic math Sin ::temp158 yaw                        ;@line 1278
						Assign ys ::temp158                                      ;@line 1278
						FMultiply ::temp158 pitch ::PitchSign_var                ;@line 1279
						CallStatic math Cos ::temp158 ::temp158                  ;@line 1279
						Assign pc ::temp158                                      ;@line 1279
						FMultiply ::temp158 pitch ::PitchSign_var                ;@line 1280
						CallStatic math Sin ::temp158 ::temp158                  ;@line 1280
						Assign ps ::temp158                                      ;@line 1280
						Assign j 0                                               ;@line 1282
					_label687:
						CompareLT ::temp157 j 3                                  ;@line 1283
						JumpF ::temp157 _label686                                ;@line 1283
						ArrayGetElement ::temp159 yawBase j                      ;@line 1284
						FMultiply ::temp159 yc ::temp159                         ;@line 1284
						IAdd ::temp160 j 3                                       ;@line 1284
						ArrayGetElement ::temp161 yawBase ::temp160              ;@line 1284
						FMultiply ::temp161 ys ::temp161                         ;@line 1284
						FSubtract ::temp159 ::temp159 ::temp161                  ;@line 1284
						Assign ::temp158 ::temp159                               ;@line 1284
						ArraySetElement yawMatrix j ::temp158                    ;@line 1284
						ArrayGetElement ::temp158 yawBase j                      ;@line 1285
						FMultiply ::temp159 ys ::temp158                         ;@line 1285
						IAdd ::temp160 j 3                                       ;@line 1285
						ArrayGetElement ::temp158 yawBase ::temp160              ;@line 1285
						FMultiply ::temp158 yc ::temp158                         ;@line 1285
						FAdd ::temp159 ::temp159 ::temp158                       ;@line 1285
						Assign ::temp161 ::temp159                               ;@line 1285
						IAdd ::temp160 j 3                                       ;@line 1285
						ArraySetElement yawMatrix ::temp160 ::temp161            ;@line 1285
						IAdd ::temp160 j 6                                       ;@line 1286
						ArrayGetElement ::temp161 yawBase ::temp160              ;@line 1286
						Assign ::temp158 ::temp161                               ;@line 1286
						IAdd ::temp160 j 6                                       ;@line 1286
						ArraySetElement yawMatrix ::temp160 ::temp158            ;@line 1286
						ArrayGetElement ::temp158 pitchBase j                    ;@line 1287
						Assign ::temp159 ::temp158                               ;@line 1287
						ArraySetElement pitchMatrix j ::temp159                  ;@line 1287
						IAdd ::temp160 j 3                                       ;@line 1288
						ArrayGetElement ::temp159 pitchBase ::temp160            ;@line 1288
						FMultiply ::temp158 pc ::temp159                         ;@line 1288
						IAdd ::temp160 j 6                                       ;@line 1288
						ArrayGetElement ::temp159 pitchBase ::temp160            ;@line 1288
						FMultiply ::temp159 ps ::temp159                         ;@line 1288
						FSubtract ::temp158 ::temp158 ::temp159                  ;@line 1288
						Assign ::temp161 ::temp158                               ;@line 1288
						IAdd ::temp160 j 3                                       ;@line 1288
						ArraySetElement pitchMatrix ::temp160 ::temp161          ;@line 1288
						IAdd ::temp160 j 3                                       ;@line 1289
						ArrayGetElement ::temp161 pitchBase ::temp160            ;@line 1289
						FMultiply ::temp158 ps ::temp161                         ;@line 1289
						IAdd ::temp160 j 6                                       ;@line 1289
						ArrayGetElement ::temp161 pitchBase ::temp160            ;@line 1289
						FMultiply ::temp161 pc ::temp161                         ;@line 1289
						FAdd ::temp158 ::temp158 ::temp161                       ;@line 1289
						Assign ::temp159 ::temp158                               ;@line 1289
						IAdd ::temp160 j 6                                       ;@line 1289
						ArraySetElement pitchMatrix ::temp160 ::temp159          ;@line 1289
						IAdd ::temp160 j 1                                       ;@line 1290
						Assign j ::temp160                                       ;@line 1290
						Jump _label687                                           ;@line 1290
					_label686:
						Cast ::temp157 ::UseSightCamera_var                      ;@line 1292
						JumpF ::temp157 _label688                                ;@line 1292
						Cast ::temp157 operating                                 ;@line 1292
						JumpT ::temp157 _label689                                ;@line 1292
						CompareEQ ::temp157 generation applyGeneration           ;@line 1292
						Not ::temp157 ::temp157                                  ;@line 1292
						Cast ::temp157 ::temp157                                 ;@line 1292
					_label689:
						Cast ::temp157 ::temp157                                 ;@line 1292
					_label688:
						JumpF ::temp157 _label690                                ;@line 1292
						Return None                                              ;@line 1293
						Jump _label690                                           ;@line 1293
					_label690:
						Cast ::temp162 self                                      ;@line 1295
						CallStatic netimmerse SetNodeLocalRotationMatrix ::temp157 ::temp162 ::YawNode_var yawMatrix False  ;@line 1295
						Cast ::temp157 ::UseSightCamera_var                      ;@line 1296
						JumpF ::temp157 _label691                                ;@line 1296
						Cast ::temp157 operating                                 ;@line 1296
						JumpT ::temp157 _label692                                ;@line 1296
						CompareEQ ::temp157 generation applyGeneration           ;@line 1296
						Not ::temp157 ::temp157                                  ;@line 1296
						Cast ::temp157 ::temp157                                 ;@line 1296
					_label692:
						Cast ::temp157 ::temp157                                 ;@line 1296
					_label691:
						JumpF ::temp157 _label693                                ;@line 1296
						Return None                                              ;@line 1297
						Jump _label693                                           ;@line 1297
					_label693:
						Cast ::temp162 self                                      ;@line 1299
						CallStatic netimmerse SetNodeLocalRotationMatrix ::temp157 ::temp162 ::PitchNode_var pitchMatrix False  ;@line 1299
					.endCode
				.endFunction
				.function RejectShot
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param reason String
					.endParamTable
					.localTable
						.local ::temp186 String
						.local ::NoneVar None
					.endLocalTable
					.code
						StrCat ::temp186 "AstraAsedio shot rejected: " reason    ;@line 1697
						CallStatic debug Trace ::NoneVar ::temp186 0             ;@line 1697
						StrCat ::temp186 "Astra: " reason                        ;@line 1698
						CallStatic debug Notification ::NoneVar ::temp186        ;@line 1698
					.endCode
				.endFunction
				.function AlignLookToWeapon
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param expectedGeneration Int
					.endParamTable
					.localTable
						.local ::temp118 Bool
						.local ::temp119 Float
						.local ::temp120 Float
						.local ::temp121 Bool
						.local ::NoneVar None
						.local yc Float
						.local ys Float
						.local pc Float
						.local ps Float
						.local lx Float
						.local ly Float
						.local wx Float
						.local wy Float
						.local wz Float
						.local heading Float
						.local angleX Float
						.local currentLease Bool
						.local menuOpen Bool
						.local playerDead Bool
					.endLocalTable
					.code
						CallMethod ReadAimRoot self ::temp118                    ;@line 948
						Not ::temp118 ::temp118                                  ;@line 948
						JumpF ::temp118 _label694                                ;@line 948
						Return False                                             ;@line 949
						Jump _label694                                           ;@line 949
					_label694:
						CallStatic math Cos ::temp119 yaw                        ;@line 951
						Assign yc ::temp119                                      ;@line 951
						CallStatic math Sin ::temp119 yaw                        ;@line 952
						Assign ys ::temp119                                      ;@line 952
						CallStatic math Cos ::temp119 pitch                      ;@line 953
						Assign pc ::temp119                                      ;@line 953
						CallStatic math Sin ::temp119 pitch                      ;@line 954
						Assign ps ::temp119                                      ;@line 954
						FMultiply ::temp119 ys pc                                ;@line 955
						Assign lx ::temp119                                      ;@line 955
						FNegate ::temp119 yc                                     ;@line 956
						FMultiply ::temp119 ::temp119 pc                         ;@line 956
						Assign ly ::temp119                                      ;@line 956
						ArrayGetElement ::temp119 rootWorldMatrix 0              ;@line 957
						FMultiply ::temp119 ::temp119 lx                         ;@line 957
						ArrayGetElement ::temp120 rootWorldMatrix 1              ;@line 957
						FMultiply ::temp120 ::temp120 ly                         ;@line 957
						FAdd ::temp119 ::temp119 ::temp120                       ;@line 957
						ArrayGetElement ::temp120 rootWorldMatrix 2              ;@line 957
						FMultiply ::temp120 ::temp120 ps                         ;@line 957
						FAdd ::temp119 ::temp119 ::temp120                       ;@line 957
						Assign wx ::temp119                                      ;@line 957
						ArrayGetElement ::temp120 rootWorldMatrix 3              ;@line 958
						FMultiply ::temp119 ::temp120 lx                         ;@line 958
						ArrayGetElement ::temp120 rootWorldMatrix 4              ;@line 958
						FMultiply ::temp120 ::temp120 ly                         ;@line 958
						FAdd ::temp119 ::temp119 ::temp120                       ;@line 958
						ArrayGetElement ::temp120 rootWorldMatrix 5              ;@line 958
						FMultiply ::temp120 ::temp120 ps                         ;@line 958
						FAdd ::temp119 ::temp119 ::temp120                       ;@line 958
						Assign wy ::temp119                                      ;@line 958
						ArrayGetElement ::temp120 rootWorldMatrix 6              ;@line 959
						FMultiply ::temp119 ::temp120 lx                         ;@line 959
						ArrayGetElement ::temp120 rootWorldMatrix 7              ;@line 959
						FMultiply ::temp120 ::temp120 ly                         ;@line 959
						FAdd ::temp119 ::temp119 ::temp120                       ;@line 959
						ArrayGetElement ::temp120 rootWorldMatrix 8              ;@line 959
						FMultiply ::temp120 ::temp120 ps                         ;@line 959
						FAdd ::temp119 ::temp119 ::temp120                       ;@line 959
						Assign wz ::temp119                                      ;@line 959
						CompareEQ ::temp118 wx wx                                ;@line 960
						Not ::temp118 ::temp118                                  ;@line 960
						Cast ::temp118 ::temp118                                 ;@line 960
						JumpT ::temp118 _label695                                ;@line 960
						CompareEQ ::temp121 wy wy                                ;@line 960
						Not ::temp121 ::temp121                                  ;@line 960
						Cast ::temp118 ::temp121                                 ;@line 960
					_label695:
						Cast ::temp118 ::temp118                                 ;@line 960
						JumpT ::temp118 _label696                                ;@line 960
						CompareEQ ::temp121 wz wz                                ;@line 960
						Not ::temp121 ::temp121                                  ;@line 960
						Cast ::temp118 ::temp121                                 ;@line 960
					_label696:
						Cast ::temp118 ::temp118                                 ;@line 960
						JumpT ::temp118 _label697                                ;@line 960
						CompareLT ::temp121 wz -1.001000                         ;@line 960
						Cast ::temp118 ::temp121                                 ;@line 960
					_label697:
						Cast ::temp118 ::temp118                                 ;@line 960
						JumpT ::temp118 _label698                                ;@line 960
						CompareGT ::temp121 wz 1.001000                          ;@line 960
						Cast ::temp118 ::temp121                                 ;@line 960
					_label698:
						JumpF ::temp118 _label699                                ;@line 960
						Return False                                             ;@line 961
						Jump _label699                                           ;@line 961
					_label699:
						CompareGT ::temp121 wz 1.000000                          ;@line 963
						JumpF ::temp121 _label700                                ;@line 963
						Assign wz 1.000000                                       ;@line 964
						Jump _label701                                           ;@line 964
					_label700:
						CompareLT ::temp118 wz -1.000000                         ;@line 965
						JumpF ::temp118 _label701                                ;@line 965
						Assign wz -1.000000                                      ;@line 966
						Jump _label701                                           ;@line 966
					_label701:
						CallMethod GetAngleZ player ::temp120                    ;@line 968
						CallMethod HeadingFromVector self ::temp119 wx wy ::temp120  ;@line 968
						Assign heading ::temp119                                 ;@line 968
						CallStatic math ASin ::temp120 wz                        ;@line 969
						FNegate ::temp119 ::temp120                              ;@line 969
						Assign angleX ::temp119                                  ;@line 969
						CallMethod IsCurrent ::Session_var ::temp118 self token  ;@line 970
						Assign currentLease ::temp118                            ;@line 970
						CallStatic utility IsInMenuMode ::temp121                ;@line 971
						Assign menuOpen ::temp121                                ;@line 971
						CallMethod IsDead player ::temp118                       ;@line 972
						Assign playerDead ::temp118                              ;@line 972
						Not ::temp121 currentLease                               ;@line 973
						Cast ::temp118 ::temp121                                 ;@line 973
						JumpT ::temp118 _label702                                ;@line 973
						Cast ::temp118 menuOpen                                  ;@line 973
					_label702:
						Cast ::temp121 ::temp118                                 ;@line 973
						JumpT ::temp121 _label703                                ;@line 973
						Cast ::temp121 playerDead                                ;@line 973
					_label703:
						Cast ::temp121 ::temp121                                 ;@line 973
						JumpT ::temp121 _label704                                ;@line 973
						Not ::temp118 operating                                  ;@line 973
						Cast ::temp121 ::temp118                                 ;@line 973
					_label704:
						Cast ::temp121 ::temp121                                 ;@line 973
						JumpT ::temp121 _label705                                ;@line 973
						CompareEQ ::temp118 generation expectedGeneration        ;@line 973
						Not ::temp118 ::temp118                                  ;@line 973
						Cast ::temp121 ::temp118                                 ;@line 973
					_label705:
						JumpF ::temp121 _label706                                ;@line 973
						Return False                                             ;@line 974
						Jump _label706                                           ;@line 974
					_label706:
						CallMethod SetAngle player ::NoneVar angleX 0.000000 heading  ;@line 976
						CallMethod IsCurrent ::Session_var ::temp118 self token  ;@line 977
						Assign currentLease ::temp118                            ;@line 977
						Cast ::temp121 currentLease                              ;@line 978
						JumpF ::temp121 _label707                                ;@line 978
						Cast ::temp121 operating                                 ;@line 978
					_label707:
						Cast ::temp121 ::temp121                                 ;@line 978
						JumpF ::temp121 _label708                                ;@line 978
						CompareEQ ::temp118 generation expectedGeneration        ;@line 978
						Cast ::temp121 ::temp118                                 ;@line 978
					_label708:
						Return ::temp121                                         ;@line 978
					.endCode
				.endFunction
				.function RegisterInput
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp28 Int
						.local ::NoneVar None
						.local ::temp29 String
						.local ::temp30 String
					.endLocalTable
					.code
						CallStatic input GetMappedKey ::temp28 "Activate" 0      ;@line 436
						Assign activateKeyboard ::temp28                         ;@line 436
						CallStatic input GetMappedKey ::temp28 "Activate" 1      ;@line 437
						Assign activateMouse ::temp28                            ;@line 437
						CallStatic input GetMappedKey ::temp28 "Right Attack/Block" 0  ;@line 438
						Assign fireKeyboard ::temp28                             ;@line 438
						CallStatic input GetMappedKey ::temp28 "Right Attack/Block" 1  ;@line 439
						Assign fireMouse ::temp28                                ;@line 439
						CallStatic input GetMappedKey ::temp28 "Sprint" 0        ;@line 440
						Assign modeKeyboard ::temp28                             ;@line 440
						CallStatic input GetMappedKey ::temp28 "Sprint" 1        ;@line 441
						Assign modeMouse ::temp28                                ;@line 441
						CallMethod RegisterForKey self ::NoneVar 203             ;@line 442
						CallMethod RegisterForKey self ::NoneVar 205             ;@line 443
						CallMethod RegisterForKey self ::NoneVar 200             ;@line 444
						CallMethod RegisterForKey self ::NoneVar 208             ;@line 445
						CallMethod RegisterMappedKey self ::NoneVar activateKeyboard  ;@line 446
						CallMethod RegisterMappedKey self ::NoneVar activateMouse  ;@line 447
						CallMethod RegisterMappedKey self ::NoneVar fireKeyboard  ;@line 448
						CallMethod RegisterMappedKey self ::NoneVar fireMouse    ;@line 449
						CallMethod RegisterMappedKey self ::NoneVar modeKeyboard  ;@line 450
						CallMethod RegisterMappedKey self ::NoneVar modeMouse    ;@line 451
						CallMethod RegisterForControl self ::NoneVar "Activate"  ;@line 452
						CallMethod RegisterForControl self ::NoneVar "Right Attack/Block"  ;@line 453
						CallMethod RegisterForControl self ::NoneVar "Sprint"    ;@line 454
						Cast ::temp29 generation                                 ;@line 455
						StrCat ::temp29 "AstraAsedio input registered generation=" ::temp29  ;@line 455
						StrCat ::temp29 ::temp29 " activate="                    ;@line 455
						Cast ::temp30 activateKeyboard                           ;@line 455
						StrCat ::temp30 ::temp29 ::temp30                        ;@line 455
						StrCat ::temp29 ::temp30 ","                             ;@line 455
						Cast ::temp30 activateMouse                              ;@line 455
						StrCat ::temp30 ::temp29 ::temp30                        ;@line 455
						StrCat ::temp29 ::temp30 " fire="                        ;@line 455
						Cast ::temp30 fireKeyboard                               ;@line 455
						StrCat ::temp30 ::temp29 ::temp30                        ;@line 455
						StrCat ::temp29 ::temp30 ","                             ;@line 455
						Cast ::temp30 fireMouse                                  ;@line 455
						StrCat ::temp30 ::temp29 ::temp30                        ;@line 455
						StrCat ::temp29 ::temp30 " arrows=203,205,200,208"       ;@line 455
						CallStatic debug Trace ::NoneVar ::temp29 0              ;@line 455
					.endCode
				.endFunction
				.function PollFirstPerson
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param expectedGeneration Int
					.endParamTable
					.localTable
						.local ::temp122 Float
						.local ::temp123 Int
						.local ::temp124 Bool
						.local ::temp125 Bool
						.local ::temp126 Bool
						.local entryToken Int
						.local now Float
						.local cameraState Int
						.local currentLease Bool
						.local menuOpen Bool
						.local playerDead Bool
						.local ::NoneVar None
						.local ::temp127 Float[]
						.local ::temp128 ObjectReference
						.local settings Float[]
						.local accepted Bool
						.local ready Bool
					.endLocalTable
					.code
						Assign entryToken token                                  ;@line 982
						CallStatic utility GetCurrentRealTime ::temp122          ;@line 983
						Assign now ::temp122                                     ;@line 983
						CallMethod ReadCameraState self ::temp123                ;@line 984
						Assign cameraState ::temp123                             ;@line 984
						CallMethod IsCurrent ::Session_var ::temp124 self entryToken  ;@line 985
						Assign currentLease ::temp124                            ;@line 985
						CallStatic utility IsInMenuMode ::temp124                ;@line 986
						Assign menuOpen ::temp124                                ;@line 986
						CallMethod IsDead player ::temp124                       ;@line 987
						Assign playerDead ::temp124                              ;@line 987
						Not ::temp124 operating                                  ;@line 988
						Cast ::temp124 ::temp124                                 ;@line 988
						JumpT ::temp124 _label709                                ;@line 988
						CompareEQ ::temp125 generation expectedGeneration        ;@line 988
						Not ::temp125 ::temp125                                  ;@line 988
						Cast ::temp124 ::temp125                                 ;@line 988
					_label709:
						Cast ::temp124 ::temp124                                 ;@line 988
						JumpT ::temp124 _label710                                ;@line 988
						CompareEQ ::temp125 token entryToken                     ;@line 988
						Not ::temp125 ::temp125                                  ;@line 988
						Cast ::temp124 ::temp125                                 ;@line 988
					_label710:
						JumpF ::temp124 _label711                                ;@line 988
						Return False                                             ;@line 989
						Jump _label711                                           ;@line 989
					_label711:
						Not ::temp125 currentLease                               ;@line 991
						JumpF ::temp125 _label712                                ;@line 991
						CallMethod EndSession self ::NoneVar                     ;@line 992
						Return False                                             ;@line 993
						Jump _label712                                           ;@line 993
					_label712:
						Cast ::temp124 menuOpen                                  ;@line 995
						JumpT ::temp124 _label713                                ;@line 995
						Cast ::temp124 playerDead                                ;@line 995
					_label713:
						Cast ::temp124 ::temp124                                 ;@line 995
						JumpT ::temp124 _label714                                ;@line 995
						CompareEQ ::temp125 now now                              ;@line 995
						Not ::temp125 ::temp125                                  ;@line 995
						Cast ::temp124 ::temp125                                 ;@line 995
					_label714:
						Cast ::temp124 ::temp124                                 ;@line 995
						JumpT ::temp124 _label715                                ;@line 995
						CompareLT ::temp125 now cameraEntryStartedAt             ;@line 995
						Cast ::temp124 ::temp125                                 ;@line 995
					_label715:
						Cast ::temp124 ::temp124                                 ;@line 995
						JumpT ::temp124 _label716                                ;@line 995
						CompareGTE ::temp125 now cameraEntryDeadline             ;@line 995
						Cast ::temp124 ::temp125                                 ;@line 995
					_label716:
						Cast ::temp126 ::temp124                                 ;@line 995
						JumpT ::temp126 _label717                                ;@line 995
						CompareEQ ::temp125 cameraState 0                        ;@line 995
						Not ::temp125 ::temp125                                  ;@line 995
						Cast ::temp125 ::temp125                                 ;@line 995
						JumpF ::temp125 _label718                                ;@line 995
						CompareEQ ::temp126 cameraState 6                        ;@line 995
						Not ::temp126 ::temp126                                  ;@line 995
						Cast ::temp125 ::temp126                                 ;@line 995
					_label718:
						Cast ::temp125 ::temp125                                 ;@line 995
						JumpF ::temp125 _label719                                ;@line 995
						CompareEQ ::temp126 cameraState 8                        ;@line 995
						Not ::temp126 ::temp126                                  ;@line 995
						Cast ::temp125 ::temp126                                 ;@line 995
					_label719:
						Cast ::temp125 ::temp125                                 ;@line 995
						JumpF ::temp125 _label720                                ;@line 995
						CompareEQ ::temp126 cameraState 9                        ;@line 995
						Not ::temp126 ::temp126                                  ;@line 995
						Cast ::temp125 ::temp126                                 ;@line 995
					_label720:
						Cast ::temp126 ::temp125                                 ;@line 995
					_label717:
						JumpF ::temp126 _label721                                ;@line 995
						CallMethod RejectActivation self ::NoneVar "CAMERA_ENTRY_FAILED: primera persona no disponible."  ;@line 996
						CallMethod EndSession self ::NoneVar                     ;@line 997
						Return False                                             ;@line 998
						Jump _label721                                           ;@line 998
					_label721:
						CompareEQ ::temp124 cameraState 0                        ;@line 1000
						Not ::temp124 ::temp124                                  ;@line 1000
						JumpF ::temp124 _label722                                ;@line 1000
						Return False                                             ;@line 1001
						Jump _label722                                           ;@line 1001
					_label722:
						JumpF ::UseSightCamera_var _label723                     ;@line 1003
						Not ::temp125 nativeSightRequested                       ;@line 1004
						JumpF ::temp125 _label724                                ;@line 1004
						Assign nativeSightRequested True                         ;@line 1006
						ArrayCreate ::temp127 12                                 ;@line 1007
						Assign settings ::temp127                                ;@line 1007
						Assign ::temp122 ::FireSeconds_var                       ;@line 1008
						ArraySetElement settings 0 ::temp122                     ;@line 1008
						Assign ::temp122 ::ReleaseSeconds_var                    ;@line 1009
						ArraySetElement settings 1 ::temp122                     ;@line 1009
						Assign ::temp122 ::ResetSeconds_var                      ;@line 1010
						ArraySetElement settings 2 ::temp122                     ;@line 1010
						Assign ::temp122 ::CycleSeconds_var                      ;@line 1011
						ArraySetElement settings 3 ::temp122                     ;@line 1011
						Assign ::temp122 ::YawCenter_var                         ;@line 1012
						ArraySetElement settings 4 ::temp122                     ;@line 1012
						Assign ::temp122 ::YawHalfSector_var                     ;@line 1013
						ArraySetElement settings 5 ::temp122                     ;@line 1013
						Assign ::temp122 ::PitchMin_var                          ;@line 1014
						ArraySetElement settings 6 ::temp122                     ;@line 1014
						Assign ::temp122 ::PitchMax_var                          ;@line 1015
						ArraySetElement settings 7 ::temp122                     ;@line 1015
						Assign ::temp122 ::PitchPivotHeight_var                  ;@line 1016
						ArraySetElement settings 8 ::temp122                     ;@line 1016
						Assign ::temp122 ::OperatorHeight_var                    ;@line 1017
						ArraySetElement settings 9 ::temp122                     ;@line 1017
						Assign ::temp122 ::OperatorDistance_var                  ;@line 1018
						ArraySetElement settings 10 ::temp122                    ;@line 1018
						Assign ::temp122 ::OperatorVerticalTolerance_var         ;@line 1019
						ArraySetElement settings 11 ::temp122                    ;@line 1019
						Cast ::temp128 self                                      ;@line 1020
						CallStatic astrasightnative BeginFastSight ::temp126 ::temp128 entryToken yaw pitch ::Launcher_var ::ShotAmmo_var ::SteelBolt_var ::ShotSound_var settings ::ContinuousFire_var  ;@line 1020
						Assign accepted ::temp126                                ;@line 1020
						Not ::temp124 operating                                  ;@line 1021
						Cast ::temp124 ::temp124                                 ;@line 1021
						JumpT ::temp124 _label725                                ;@line 1021
						CompareEQ ::temp126 generation expectedGeneration        ;@line 1021
						Not ::temp126 ::temp126                                  ;@line 1021
						Cast ::temp124 ::temp126                                 ;@line 1021
					_label725:
						Cast ::temp124 ::temp124                                 ;@line 1021
						JumpT ::temp124 _label726                                ;@line 1021
						CompareEQ ::temp126 token entryToken                     ;@line 1021
						Not ::temp126 ::temp126                                  ;@line 1021
						Cast ::temp124 ::temp126                                 ;@line 1021
					_label726:
						JumpF ::temp124 _label727                                ;@line 1021
						Cast ::temp128 self                                      ;@line 1023
						CallStatic astrasightnative EndSight ::temp126 ::temp128 entryToken  ;@line 1023
						Return False                                             ;@line 1024
						Jump _label727                                           ;@line 1024
					_label727:
						Not ::temp126 accepted                                   ;@line 1026
						JumpF ::temp126 _label728                                ;@line 1026
						CallMethod RejectActivation self ::NoneVar "NATIVE_SIGHT_BEGIN_FAILED: la mira rechazÃ³ la entrada."  ;@line 1027
						CallMethod EndSession self ::NoneVar                     ;@line 1028
						Return False                                             ;@line 1029
						Jump _label728                                           ;@line 1029
					_label728:
						Jump _label724                                           ;@line 1029
					_label724:
						Cast ::temp128 self                                      ;@line 1032
						CallStatic astrasightnative IsFastSightReady ::temp124 ::temp128 entryToken  ;@line 1032
						Assign ready ::temp124                                   ;@line 1032
						Not ::temp126 operating                                  ;@line 1033
						Cast ::temp124 ::temp126                                 ;@line 1033
						JumpT ::temp124 _label729                                ;@line 1033
						CompareEQ ::temp125 generation expectedGeneration        ;@line 1033
						Not ::temp125 ::temp125                                  ;@line 1033
						Cast ::temp124 ::temp125                                 ;@line 1033
					_label729:
						Cast ::temp125 ::temp124                                 ;@line 1033
						JumpT ::temp125 _label730                                ;@line 1033
						CompareEQ ::temp126 token entryToken                     ;@line 1033
						Not ::temp126 ::temp126                                  ;@line 1033
						Cast ::temp125 ::temp126                                 ;@line 1033
					_label730:
						JumpF ::temp125 _label731                                ;@line 1033
						Return False                                             ;@line 1034
						Jump _label731                                           ;@line 1034
					_label731:
						Not ::temp124 ready                                      ;@line 1036
						JumpF ::temp124 _label732                                ;@line 1036
						Return False                                             ;@line 1037
						Jump _label732                                           ;@line 1037
					_label732:
						CallStatic utility GetCurrentRealTime ::temp122          ;@line 1039
						Assign now ::temp122                                     ;@line 1039
						CallStatic utility IsInMenuMode ::temp126                ;@line 1040
						Assign menuOpen ::temp126                                ;@line 1040
						CallMethod IsDead player ::temp125                       ;@line 1041
						Assign playerDead ::temp125                              ;@line 1041
						Not ::temp124 operating                                  ;@line 1042
						Cast ::temp125 ::temp124                                 ;@line 1042
						JumpT ::temp125 _label733                                ;@line 1042
						CompareEQ ::temp126 generation expectedGeneration        ;@line 1042
						Not ::temp126 ::temp126                                  ;@line 1042
						Cast ::temp125 ::temp126                                 ;@line 1042
					_label733:
						Cast ::temp126 ::temp125                                 ;@line 1042
						JumpT ::temp126 _label734                                ;@line 1042
						CompareEQ ::temp124 token entryToken                     ;@line 1042
						Not ::temp124 ::temp124                                  ;@line 1042
						Cast ::temp126 ::temp124                                 ;@line 1042
					_label734:
						JumpF ::temp126 _label735                                ;@line 1042
						Return False                                             ;@line 1043
						Jump _label735                                           ;@line 1043
					_label735:
						Cast ::temp125 menuOpen                                  ;@line 1045
						JumpT ::temp125 _label736                                ;@line 1045
						Cast ::temp125 playerDead                                ;@line 1045
					_label736:
						Cast ::temp126 ::temp125                                 ;@line 1045
						JumpT ::temp126 _label737                                ;@line 1045
						CompareEQ ::temp124 now now                              ;@line 1045
						Not ::temp124 ::temp124                                  ;@line 1045
						Cast ::temp126 ::temp124                                 ;@line 1045
					_label737:
						Cast ::temp124 ::temp126                                 ;@line 1045
						JumpT ::temp124 _label738                                ;@line 1045
						CompareLT ::temp125 now cameraEntryStartedAt             ;@line 1045
						Cast ::temp124 ::temp125                                 ;@line 1045
					_label738:
						Cast ::temp125 ::temp124                                 ;@line 1045
						JumpT ::temp125 _label739                                ;@line 1045
						CompareGTE ::temp126 now cameraEntryDeadline             ;@line 1045
						Cast ::temp125 ::temp126                                 ;@line 1045
					_label739:
						JumpF ::temp125 _label740                                ;@line 1045
						CallMethod RejectActivation self ::NoneVar "NATIVE_SIGHT_ENTRY_TIMEOUT: la mira no estuvo lista a tiempo."  ;@line 1046
						CallMethod EndSession self ::NoneVar                     ;@line 1047
						Return False                                             ;@line 1048
						Jump _label740                                           ;@line 1048
					_label740:
						Jump _label723                                           ;@line 1048
					_label723:
						Assign cameraEntryPending False                          ;@line 1051
						CallMethod ResumeInput self ::NoneVar                    ;@line 1052
						Cast ::temp126 operating                                 ;@line 1053
						JumpF ::temp126 _label741                                ;@line 1053
						CompareEQ ::temp124 generation expectedGeneration        ;@line 1053
						Cast ::temp126 ::temp124                                 ;@line 1053
					_label741:
						Return ::temp126                                         ;@line 1053
					.endCode
				.endFunction
				.function RequestExit
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param inputSource String
					.endParamTable
					.localTable
						.local ::temp68 Bool
						.local ::temp69 Bool
						.local ::temp70 Float
						.local ::temp71 String
						.local ::temp72 String
						.local ::NoneVar None
						.local exitGeneration Int
						.local exitToken Int
						.local exitMenuOpen Bool
						.local requestedExitAt Float
					.endLocalTable
					.code
						Assign exitGeneration generation                         ;@line 707
						Assign exitToken token                                   ;@line 708
						Not ::temp68 operating                                   ;@line 709
						JumpF ::temp68 _label742                                 ;@line 709
						Return None                                              ;@line 710
						Jump _label742                                           ;@line 710
					_label742:
						CallStatic utility IsInMenuMode ::temp68                 ;@line 712
						Assign exitMenuOpen ::temp68                             ;@line 712
						Not ::temp68 operating                                   ;@line 713
						Cast ::temp68 ::temp68                                   ;@line 713
						JumpT ::temp68 _label743                                 ;@line 713
						CompareEQ ::temp69 generation exitGeneration             ;@line 713
						Not ::temp69 ::temp69                                    ;@line 713
						Cast ::temp68 ::temp69                                   ;@line 713
					_label743:
						Cast ::temp68 ::temp68                                   ;@line 713
						JumpT ::temp68 _label744                                 ;@line 713
						CompareEQ ::temp69 token exitToken                       ;@line 713
						Not ::temp69 ::temp69                                    ;@line 713
						Cast ::temp68 ::temp69                                   ;@line 713
					_label744:
						Cast ::temp69 ::temp68                                   ;@line 713
						JumpT ::temp69 _label745                                 ;@line 713
						Cast ::temp69 exitMenuOpen                               ;@line 713
					_label745:
						JumpF ::temp69 _label746                                 ;@line 713
						Return None                                              ;@line 714
						Jump _label746                                           ;@line 714
					_label746:
						CallStatic utility GetCurrentRealTime ::temp70           ;@line 716
						Assign requestedExitAt ::temp70                          ;@line 716
						Not ::temp68 operating                                   ;@line 717
						Cast ::temp68 ::temp68                                   ;@line 717
						JumpT ::temp68 _label747                                 ;@line 717
						CompareEQ ::temp69 generation exitGeneration             ;@line 717
						Not ::temp69 ::temp69                                    ;@line 717
						Cast ::temp68 ::temp69                                   ;@line 717
					_label747:
						Cast ::temp68 ::temp68                                   ;@line 717
						JumpT ::temp68 _label748                                 ;@line 717
						CompareEQ ::temp69 token exitToken                       ;@line 717
						Not ::temp69 ::temp69                                    ;@line 717
						Cast ::temp68 ::temp69                                   ;@line 717
					_label748:
						JumpF ::temp68 _label749                                 ;@line 717
						Return None                                              ;@line 718
						Jump _label749                                           ;@line 718
					_label749:
						CompareLT ::temp69 requestedExitAt activateReadyAt       ;@line 720
						JumpF ::temp69 _label750                                 ;@line 720
						Return None                                              ;@line 721
						Jump _label750                                           ;@line 721
					_label750:
						StrCat ::temp71 "AstraAsedio cancel source=" inputSource  ;@line 723
						StrCat ::temp71 ::temp71 " generation="                  ;@line 723
						Cast ::temp72 generation                                 ;@line 723
						StrCat ::temp72 ::temp71 ::temp72                        ;@line 723
						CallStatic debug Trace ::NoneVar ::temp72 0              ;@line 723
						Not ::temp68 operating                                   ;@line 724
						Cast ::temp68 ::temp68                                   ;@line 724
						JumpT ::temp68 _label751                                 ;@line 724
						CompareEQ ::temp69 generation exitGeneration             ;@line 724
						Not ::temp69 ::temp69                                    ;@line 724
						Cast ::temp68 ::temp69                                   ;@line 724
					_label751:
						Cast ::temp68 ::temp68                                   ;@line 724
						JumpT ::temp68 _label752                                 ;@line 724
						CompareEQ ::temp69 token exitToken                       ;@line 724
						Not ::temp69 ::temp69                                    ;@line 724
						Cast ::temp68 ::temp69                                   ;@line 724
					_label752:
						JumpF ::temp68 _label753                                 ;@line 724
						Return None                                              ;@line 725
						Jump _label753                                           ;@line 725
					_label753:
						CallMethod EndSession self ::NoneVar                     ;@line 727
					.endCode
				.endFunction
				.function TryRepeatShot
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param expectedGeneration Int
					.endParamTable
					.localTable
						.local ::temp42 Bool
						.local ::temp43 Bool
						.local ::NoneVar None
						.local repeatToken Int
						.local expectedRevision Int
						.local repeatInputReady Bool
					.endLocalTable
					.code
						JumpF ::UseSightCamera_var _label754                     ;@line 560
						Return None                                              ;@line 561
						Jump _label754                                           ;@line 561
					_label754:
						Assign repeatToken token                                 ;@line 563
						Assign expectedRevision repeatRevision                   ;@line 564
						Not ::temp42 operating                                   ;@line 565
						Cast ::temp42 ::temp42                                   ;@line 565
						JumpT ::temp42 _label755                                 ;@line 565
						CompareEQ ::temp43 generation expectedGeneration         ;@line 565
						Not ::temp43 ::temp43                                    ;@line 565
						Cast ::temp42 ::temp43                                   ;@line 565
					_label755:
						Cast ::temp42 ::temp42                                   ;@line 565
						JumpT ::temp42 _label756                                 ;@line 565
						CompareEQ ::temp43 phase 0                               ;@line 565
						Not ::temp43 ::temp43                                    ;@line 565
						Cast ::temp42 ::temp43                                   ;@line 565
					_label756:
						Cast ::temp42 ::temp42                                   ;@line 565
						JumpT ::temp42 _label757                                 ;@line 565
						Not ::temp43 ::ContinuousFire_var                        ;@line 565
						Cast ::temp42 ::temp43                                   ;@line 565
					_label757:
						Cast ::temp42 ::temp42                                   ;@line 565
						JumpT ::temp42 _label758                                 ;@line 565
						Not ::temp43 repeatFire                                  ;@line 565
						Cast ::temp42 ::temp43                                   ;@line 565
					_label758:
						JumpF ::temp42 _label759                                 ;@line 565
						Return None                                              ;@line 566
						Jump _label759                                           ;@line 566
					_label759:
						CallMethod InputReady self ::temp43                      ;@line 568
						Assign repeatInputReady ::temp43                         ;@line 568
						Not ::temp42 operating                                   ;@line 569
						Cast ::temp42 ::temp42                                   ;@line 569
						JumpT ::temp42 _label760                                 ;@line 569
						CompareEQ ::temp43 generation expectedGeneration         ;@line 569
						Not ::temp43 ::temp43                                    ;@line 569
						Cast ::temp42 ::temp43                                   ;@line 569
					_label760:
						Cast ::temp42 ::temp42                                   ;@line 569
						JumpT ::temp42 _label761                                 ;@line 569
						CompareEQ ::temp43 token repeatToken                     ;@line 569
						Not ::temp43 ::temp43                                    ;@line 569
						Cast ::temp42 ::temp43                                   ;@line 569
					_label761:
						Cast ::temp42 ::temp42                                   ;@line 569
						JumpT ::temp42 _label762                                 ;@line 569
						CompareEQ ::temp43 phase 0                               ;@line 569
						Not ::temp43 ::temp43                                    ;@line 569
						Cast ::temp42 ::temp43                                   ;@line 569
					_label762:
						Cast ::temp42 ::temp42                                   ;@line 569
						JumpT ::temp42 _label763                                 ;@line 569
						Not ::temp43 ::ContinuousFire_var                        ;@line 569
						Cast ::temp42 ::temp43                                   ;@line 569
					_label763:
						Cast ::temp42 ::temp42                                   ;@line 569
						JumpT ::temp42 _label764                                 ;@line 569
						Not ::temp43 repeatFire                                  ;@line 569
						Cast ::temp42 ::temp43                                   ;@line 569
					_label764:
						Cast ::temp42 ::temp42                                   ;@line 569
						JumpT ::temp42 _label765                                 ;@line 569
						CompareEQ ::temp43 repeatRevision expectedRevision       ;@line 569
						Not ::temp43 ::temp43                                    ;@line 569
						Cast ::temp42 ::temp43                                   ;@line 569
					_label765:
						Cast ::temp42 ::temp42                                   ;@line 569
						JumpT ::temp42 _label766                                 ;@line 569
						Not ::temp43 repeatInputReady                            ;@line 569
						Cast ::temp42 ::temp43                                   ;@line 569
					_label766:
						JumpF ::temp42 _label767                                 ;@line 569
						Return None                                              ;@line 570
						Jump _label767                                           ;@line 570
					_label767:
						CallMethod BeginShot self ::NoneVar expectedGeneration expectedRevision  ;@line 572
					.endCode
				.endFunction
				.function OnUnload
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod EndSession self ::NoneVar                     ;@line 201
					.endCode
				.endFunction
				.function HeadingFromVector
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Float
					.paramTable
						.param vectorX Float
						.param vectorY Float
						.param fallback Float
					.endParamTable
					.localTable
						.local ::temp107 Float
						.local ::temp108 Float
						.local ::temp109 Bool
						.local ::temp110 Bool
						.local horizontal Float
						.local cosine Float
						.local angle Float
					.endLocalTable
					.code
						FMultiply ::temp107 vectorX vectorX                      ;@line 913
						FMultiply ::temp108 vectorY vectorY                      ;@line 913
						FAdd ::temp107 ::temp107 ::temp108                       ;@line 913
						CallStatic math Sqrt ::temp108 ::temp107                 ;@line 913
						Assign horizontal ::temp108                              ;@line 913
						CompareLT ::temp109 horizontal 0.000010                  ;@line 914
						JumpF ::temp109 _label768                                ;@line 914
						Return fallback                                          ;@line 915
						Jump _label768                                           ;@line 915
					_label768:
						FDivide ::temp107 vectorY horizontal                     ;@line 917
						Assign cosine ::temp107                                  ;@line 917
						CompareGT ::temp109 cosine 1.000000                      ;@line 918
						JumpF ::temp109 _label769                                ;@line 918
						Assign cosine 1.000000                                   ;@line 919
						Jump _label770                                           ;@line 919
					_label769:
						CompareLT ::temp110 cosine -1.000000                     ;@line 920
						JumpF ::temp110 _label770                                ;@line 920
						Assign cosine -1.000000                                  ;@line 921
						Jump _label770                                           ;@line 921
					_label770:
						CallStatic math ACos ::temp108 cosine                    ;@line 923
						Assign angle ::temp108                                   ;@line 923
						CompareLT ::temp110 vectorX 0.000000                     ;@line 924
						JumpF ::temp110 _label771                                ;@line 924
						FSubtract ::temp107 360.000000 angle                     ;@line 925
						Assign angle ::temp107                                   ;@line 925
						Jump _label771                                           ;@line 925
					_label771:
						CompareGTE ::temp109 angle 360.000000                    ;@line 927
						JumpF ::temp109 _label772                                ;@line 927
						FSubtract ::temp108 angle 360.000000                     ;@line 928
						Assign angle ::temp108                                   ;@line 928
						Jump _label772                                           ;@line 928
					_label772:
						Return angle                                             ;@line 930
					.endCode
				.endFunction
				.function OnControlUp
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param control String
						.param holdTime Float
					.endParamTable
					.localTable
						.local ::temp65 Bool
						.local ::temp67 Bool
						.local ::temp66 Int
						.local ::NoneVar None
					.endLocalTable
					.code
						JumpF ::UseSightCamera_var _label773                     ;@line 692
						Return None                                              ;@line 693
						Jump _label773                                           ;@line 693
					_label773:
						Cast ::temp65 operating                                  ;@line 695
						JumpF ::temp65 _label774                                 ;@line 695
						CompareEQ ::temp65 control "Right Attack/Block"          ;@line 695
						Cast ::temp65 ::temp65                                   ;@line 695
					_label774:
						JumpF ::temp65 _label775                                 ;@line 695
						IAdd ::temp66 fireReleaseSerial 1                        ;@line 696
						Assign fireReleaseSerial ::temp66                        ;@line 696
						Assign heldFire False                                    ;@line 697
						CallMethod StopRepeatFire self ::NoneVar                 ;@line 698
						Jump _label776                                           ;@line 698
					_label775:
						Cast ::temp67 operating                                  ;@line 699
						JumpF ::temp67 _label777                                 ;@line 699
						CompareEQ ::temp67 control "Sprint"                      ;@line 699
						Cast ::temp67 ::temp67                                   ;@line 699
					_label777:
						JumpF ::temp67 _label776                                 ;@line 699
						IAdd ::temp66 modeReleaseSerial 1                        ;@line 700
						Assign modeReleaseSerial ::temp66                        ;@line 700
						Assign heldMode False                                    ;@line 701
						Jump _label776                                           ;@line 701
					_label776:
					.endCode
				.endFunction
				.function TraceRetainedCombat
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param where String
					.endParamTable
					.localTable
						.local ::temp210 Actor
						.local ::temp211 Bool
						.local ::temp212 Bool
						.local ::temp213 Float
						.local ::temp214 Int
						.local ::temp215 String
						.local ::temp216 String
						.local ::NoneVar None
						.local operator Actor
						.local target Actor
						.local dead Int
						.local targetIsPlayer Int
						.local health Float
						.local combat Int
						.local cameraState Int
						.local fight Int
						.local camSwitch Int
					.endLocalTable
					.code
						Assign operator player                                   ;@line 1872
						Assign target retainedCombatTarget                       ;@line 1873
						Cast ::temp210 None                                      ;@line 1874
						CompareEQ ::temp211 operator ::temp210                   ;@line 1874
						Cast ::temp211 ::temp211                                 ;@line 1874
						JumpT ::temp211 _label778                                ;@line 1874
						Cast ::temp210 None                                      ;@line 1874
						CompareEQ ::temp212 target ::temp210                     ;@line 1874
						Cast ::temp211 ::temp212                                 ;@line 1874
					_label778:
						Cast ::temp211 ::temp211                                 ;@line 1874
						JumpT ::temp211 _label779                                ;@line 1874
						CompareEQ ::temp212 target operator                      ;@line 1874
						Cast ::temp211 ::temp212                                 ;@line 1874
					_label779:
						JumpF ::temp211 _label780                                ;@line 1874
						Return None                                              ;@line 1875
						Jump _label780                                           ;@line 1875
					_label780:
						Assign dead 0                                            ;@line 1877
						CallMethod IsDead target ::temp212                       ;@line 1878
						JumpF ::temp212 _label781                                ;@line 1878
						Assign dead 1                                            ;@line 1879
						Jump _label781                                           ;@line 1879
					_label781:
						Assign targetIsPlayer 0                                  ;@line 1881
						CallMethod GetCombatTarget target ::temp210              ;@line 1882
						CompareEQ ::temp211 ::temp210 operator                   ;@line 1882
						JumpF ::temp211 _label782                                ;@line 1882
						Assign targetIsPlayer 1                                  ;@line 1883
						Jump _label782                                           ;@line 1883
					_label782:
						CallMethod GetActorValue target ::temp213 "health"       ;@line 1885
						Assign health ::temp213                                  ;@line 1885
						CallMethod GetCombatState target ::temp214               ;@line 1886
						Assign combat ::temp214                                  ;@line 1886
						CallMethod ReadCameraState self ::temp214                ;@line 1887
						Assign cameraState ::temp214                             ;@line 1887
						Assign fight 0                                           ;@line 1888
						CallStatic game IsFightingControlsEnabled ::temp212      ;@line 1889
						JumpF ::temp212 _label783                                ;@line 1889
						Assign fight 1                                           ;@line 1890
						Jump _label783                                           ;@line 1890
					_label783:
						Assign camSwitch 0                                       ;@line 1892
						CallStatic game IsCamSwitchControlsEnabled ::temp211     ;@line 1893
						JumpF ::temp211 _label784                                ;@line 1893
						Assign camSwitch 1                                       ;@line 1894
						Jump _label784                                           ;@line 1894
					_label784:
						StrCat ::temp215 "AstraAsedio retain " where             ;@line 1896
						StrCat ::temp215 ::temp215 " ref="                       ;@line 1896
						Cast ::temp216 target                                    ;@line 1896
						StrCat ::temp216 ::temp215 ::temp216                     ;@line 1896
						StrCat ::temp215 ::temp216 " dead="                      ;@line 1896
						Cast ::temp216 dead                                      ;@line 1896
						StrCat ::temp216 ::temp215 ::temp216                     ;@line 1896
						StrCat ::temp215 ::temp216 " health="                    ;@line 1896
						Cast ::temp216 health                                    ;@line 1896
						StrCat ::temp216 ::temp215 ::temp216                     ;@line 1896
						StrCat ::temp215 ::temp216 " combat="                    ;@line 1896
						Cast ::temp216 combat                                    ;@line 1896
						StrCat ::temp216 ::temp215 ::temp216                     ;@line 1896
						StrCat ::temp215 ::temp216 " targetIsPlayer="            ;@line 1896
						Cast ::temp216 targetIsPlayer                            ;@line 1896
						StrCat ::temp216 ::temp215 ::temp216                     ;@line 1896
						StrCat ::temp215 ::temp216 " cam="                       ;@line 1896
						Cast ::temp216 cameraState                               ;@line 1896
						StrCat ::temp216 ::temp215 ::temp216                     ;@line 1896
						StrCat ::temp215 ::temp216 " fight="                     ;@line 1896
						Cast ::temp216 fight                                     ;@line 1896
						StrCat ::temp216 ::temp215 ::temp216                     ;@line 1896
						StrCat ::temp215 ::temp216 " camSwitch="                 ;@line 1896
						Cast ::temp216 camSwitch                                 ;@line 1896
						StrCat ::temp216 ::temp215 ::temp216                     ;@line 1896
						CallStatic debug Trace ::NoneVar ::temp216 0             ;@line 1896
					.endCode
				.endFunction
				.function CanOperate
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param expectedGeneration Int
					.endParamTable
					.localTable
						.local ::temp104 Bool
						.local ::temp105 Int
						.local ::temp106 Bool
						.local ::temp101 Bool
						.local ::temp102 Bool
						.local ::temp103 ObjectReference
					.endLocalTable
					.code
						JumpF ::UseSightCamera_var _label785                     ;@line 905
						Cast ::temp101 operating                                 ;@line 907
						JumpF ::temp101 _label786                                ;@line 907
						Not ::temp101 cameraEntryPending                         ;@line 907
						Cast ::temp101 ::temp101                                 ;@line 907
					_label786:
						Cast ::temp101 ::temp101                                 ;@line 907
						JumpF ::temp101 _label787                                ;@line 907
						CompareEQ ::temp102 generation expectedGeneration        ;@line 907
						Cast ::temp101 ::temp102                                 ;@line 907
					_label787:
						Cast ::temp101 ::temp101                                 ;@line 907
						JumpF ::temp101 _label788                                ;@line 907
						CallMethod IsCurrent ::Session_var ::temp102 self token  ;@line 907
						Cast ::temp101 ::temp102                                 ;@line 907
					_label788:
						Cast ::temp101 ::temp101                                 ;@line 907
						JumpF ::temp101 _label789                                ;@line 907
						Cast ::temp103 self                                      ;@line 907
						CallStatic astrasightnative IsFastSightReady ::temp102 ::temp103 token  ;@line 907
						Cast ::temp101 ::temp102                                 ;@line 907
					_label789:
						Return ::temp101                                         ;@line 907
						Jump _label785                                           ;@line 907
					_label785:
						Cast ::temp102 operating                                 ;@line 909
						JumpF ::temp102 _label790                                ;@line 909
						Not ::temp102 cameraEntryPending                         ;@line 909
						Cast ::temp102 ::temp102                                 ;@line 909
					_label790:
						Cast ::temp102 ::temp102                                 ;@line 909
						JumpF ::temp102 _label791                                ;@line 909
						CompareEQ ::temp104 generation expectedGeneration        ;@line 909
						Cast ::temp102 ::temp104                                 ;@line 909
					_label791:
						Cast ::temp102 ::temp102                                 ;@line 909
						JumpF ::temp102 _label792                                ;@line 909
						CallMethod IsCurrent ::Session_var ::temp104 self token  ;@line 909
						Cast ::temp102 ::temp104                                 ;@line 909
					_label792:
						Cast ::temp102 ::temp102                                 ;@line 909
						JumpF ::temp102 _label793                                ;@line 909
						CallMethod ReadCameraState self ::temp105                ;@line 909
						CompareEQ ::temp104 ::temp105 0                          ;@line 909
						Cast ::temp102 ::temp104                                 ;@line 909
					_label793:
						Cast ::temp102 ::temp102                                 ;@line 909
						JumpF ::temp102 _label794                                ;@line 909
						CallMethod IsDead player ::temp104                       ;@line 909
						Not ::temp104 ::temp104                                  ;@line 909
						Cast ::temp102 ::temp104                                 ;@line 909
					_label794:
						Cast ::temp102 ::temp102                                 ;@line 909
						JumpF ::temp102 _label795                                ;@line 909
						CallMethod NearOperator self ::temp104                   ;@line 909
						Cast ::temp102 ::temp104                                 ;@line 909
					_label795:
						Cast ::temp102 ::temp102                                 ;@line 909
						JumpF ::temp102 _label796                                ;@line 909
						Cast ::temp103 self                                      ;@line 909
						CallStatic netimmerse HasNode ::temp104 ::temp103 "ProjectileNode" False  ;@line 909
						Cast ::temp102 ::temp104                                 ;@line 909
					_label796:
						Cast ::temp102 ::temp102                                 ;@line 909
						JumpF ::temp102 _label797                                ;@line 909
						Cast ::temp103 self                                      ;@line 909
						CallStatic netimmerse HasNode ::temp104 ::temp103 ::YawNode_var False  ;@line 909
						Cast ::temp102 ::temp104                                 ;@line 909
					_label797:
						Cast ::temp102 ::temp102                                 ;@line 909
						JumpF ::temp102 _label798                                ;@line 909
						Cast ::temp103 self                                      ;@line 909
						CallStatic netimmerse HasNode ::temp104 ::temp103 ::PitchNode_var False  ;@line 909
						Cast ::temp102 ::temp104                                 ;@line 909
					_label798:
						Cast ::temp102 ::temp102                                 ;@line 909
						JumpF ::temp102 _label799                                ;@line 909
						Cast ::temp103 self                                      ;@line 909
						CallStatic netimmerse HasNode ::temp104 ::temp103 ::VisualBoltNode_var False  ;@line 909
						Cast ::temp102 ::temp104                                 ;@line 909
					_label799:
						Cast ::temp106 ::temp102                                 ;@line 909
						JumpF ::temp106 _label800                                ;@line 909
						Not ::temp104 ::UseSightCamera_var                       ;@line 909
						Cast ::temp104 ::temp104                                 ;@line 909
						JumpT ::temp104 _label801                                ;@line 909
						Cast ::temp103 self                                      ;@line 909
						CallStatic astrasightnative IsSightReady ::temp106 ::temp103 token  ;@line 909
						Cast ::temp104 ::temp106                                 ;@line 909
					_label801:
						Cast ::temp106 ::temp104                                 ;@line 909
					_label800:
						Return ::temp106                                         ;@line 909
					.endCode
				.endFunction
			.endState
		.endStateTable
	.endObject
.endObjectTable
