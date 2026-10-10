.info
	.source "AstraAsedioGuard.psc"
	.modifyTime 1791460956 ;Thu Oct 08 09:02:36 2026 Local
	.compileTime 1791461085 ;Thu Oct 08 09:04:45 2026 Local
	.user "Facu2"
	.computer "DESKTOP-DF3S14S"
.endInfo
.userFlagsRef
	.flag conditional 1	; 0x00000001
	.flag hidden 0	; 0x00000000
.endUserFlagsRef
.objectTable
	.object AstraAsedioGuard ObjectReference
		.userFlags 0	; Flags: 0x00000000
		.docString ""
		.autoState 
		.variableTable
			.variable yaw Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable yawMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable generation Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable ::ProjectileSpeed_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 5400.000000
			.endVariable
			.variable ::PitchMin_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue -20.000000
			.endVariable
			.variable faulted Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable muzzlePosition Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable rootPosition Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable matricesReady Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable shotTarget actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable pitch Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::PitchMax_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 45.000000
			.endVariable
			.variable aimX Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::PitchNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "CTRL_ELEVACION"
			.endVariable
			.variable ::ShotAmmo_var ammo
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable desiredYaw Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::ReleaseSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.100000
			.endVariable
			.variable ::ShotSound_var sound
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable phaseAt Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::Artillero_var actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::ResetSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 1.200000
			.endVariable
			.variable ::Launcher_var weapon
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable phase Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable desiredPitch Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable nextShotAt Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable updating Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::TargetHeight_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 60.000000
			.endVariable
			.variable yawBase Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable token Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1
			.endVariable
			.variable ownedGuard actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable serial Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable ::CadenceSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 4.000000
			.endVariable
			.variable running Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable recovering Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable lastTick Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable sceneBusy Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable pitchMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable rootWorldMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable destroyed Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable aimZ Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable muzzleWorldMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable aimY Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1.000000
			.endVariable
			.variable ::YawNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "CTRL_GIRO_360"
			.endVariable
			.variable ::VisualBoltNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "VIROTE_VISUAL"
			.endVariable
			.variable pitchBase Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable targetHorizontal Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable pinBusy Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::Puesto_var ObjectReference
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::FireSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.300000
			.endVariable
			.variable ::ProjectileGravity_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 240.345001
			.endVariable
			.variable ::TurnRate_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 30.000000
			.endVariable
			.variable ::MuzzleNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "ProjectileNode"
			.endVariable
			.variable recoveryRequested Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
		.endVariableTable
		.propertyTable
			.property MuzzleNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::MuzzleNode_var
			.endProperty
			.property ProjectileGravity Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ProjectileGravity_var
			.endProperty
			.property PitchNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchNode_var
			.endProperty
			.property ShotSound sound auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ShotSound_var
			.endProperty
			.property TurnRate Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::TurnRate_var
			.endProperty
			.property Artillero actor auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Artillero_var
			.endProperty
			.property CadenceSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::CadenceSeconds_var
			.endProperty
			.property FireSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::FireSeconds_var
			.endProperty
			.property Puesto ObjectReference auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Puesto_var
			.endProperty
			.property PitchMin Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchMin_var
			.endProperty
			.property Launcher weapon auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Launcher_var
			.endProperty
			.property PitchMax Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchMax_var
			.endProperty
			.property ProjectileSpeed Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ProjectileSpeed_var
			.endProperty
			.property ShotAmmo ammo auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ShotAmmo_var
			.endProperty
			.property YawNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::YawNode_var
			.endProperty
			.property ResetSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ResetSeconds_var
			.endProperty
			.property VisualBoltNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::VisualBoltNode_var
			.endProperty
			.property TargetHeight Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::TargetHeight_var
			.endProperty
			.property ReleaseSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ReleaseSeconds_var
			.endProperty
		.endPropertyTable
		.stateTable
			.state 
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
						CallMethod Shutdown self ::NoneVar                       ;@line 74
					.endCode
				.endFunction
				.function ValidTarget
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param target actor
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp62 Bool
						.local ::temp63 actor
						.local ::temp64 Bool
						.local ::temp65 Int
						.local ::temp66 ObjectReference
						.local player actor
						.local valid Bool
						.local visible Bool
						.local combatTarget actor
					.endLocalTable
					.code
						CallMethod GuardReady self ::temp62 expectedGeneration expectedToken  ;@line 495
						Not ::temp62 ::temp62                                    ;@line 495
						Cast ::temp62 ::temp62                                   ;@line 495
						JumpT ::temp62 _label0                                   ;@line 495
						Cast ::temp63 None                                       ;@line 495
						CompareEQ ::temp64 target ::temp63                       ;@line 495
						Cast ::temp62 ::temp64                                   ;@line 495
					_label0:
						Cast ::temp62 ::temp62                                   ;@line 495
						JumpT ::temp62 _label1                                   ;@line 495
						CompareEQ ::temp64 target ::Artillero_var                ;@line 495
						Cast ::temp62 ::temp64                                   ;@line 495
					_label1:
						JumpF ::temp62 _label2                                   ;@line 495
						Return False                                             ;@line 496
						Jump _label2                                             ;@line 496
					_label2:
						CallStatic game GetPlayer ::temp63                       ;@line 498
						Assign player ::temp63                                   ;@line 498
						CallMethod Current self ::temp64 expectedGeneration expectedToken  ;@line 499
						Not ::temp62 ::temp64                                    ;@line 499
						Cast ::temp62 ::temp62                                   ;@line 499
						JumpT ::temp62 _label3                                   ;@line 499
						CompareEQ ::temp64 target player                         ;@line 499
						Cast ::temp62 ::temp64                                   ;@line 499
					_label3:
						JumpF ::temp62 _label4                                   ;@line 499
						Return False                                             ;@line 500
						Jump _label4                                             ;@line 500
					_label4:
						CallMethod Is3DLoaded target ::temp64                    ;@line 502
						Cast ::temp64 ::temp64                                   ;@line 502
						JumpF ::temp64 _label5                                   ;@line 502
						CallMethod IsDisabled target ::temp62                    ;@line 502
						Not ::temp62 ::temp62                                    ;@line 502
						Cast ::temp64 ::temp62                                   ;@line 502
					_label5:
						Cast ::temp64 ::temp64                                   ;@line 502
						JumpF ::temp64 _label6                                   ;@line 502
						CallMethod IsDead target ::temp62                        ;@line 502
						Not ::temp62 ::temp62                                    ;@line 502
						Cast ::temp64 ::temp62                                   ;@line 502
					_label6:
						Cast ::temp64 ::temp64                                   ;@line 502
						JumpF ::temp64 _label7                                   ;@line 502
						CallMethod IsPlayerTeammate target ::temp62              ;@line 502
						Not ::temp62 ::temp62                                    ;@line 502
						Cast ::temp64 ::temp62                                   ;@line 502
					_label7:
						Cast ::temp64 ::temp64                                   ;@line 502
						JumpF ::temp64 _label8                                   ;@line 502
						CallMethod IsHostileToActor target ::temp62 ::Artillero_var  ;@line 502
						Cast ::temp64 ::temp62                                   ;@line 502
					_label8:
						Cast ::temp64 ::temp64                                   ;@line 502
						JumpF ::temp64 _label9                                   ;@line 502
						CallMethod GetCombatState target ::temp65                ;@line 502
						CompareGT ::temp62 ::temp65 0                            ;@line 502
						Cast ::temp64 ::temp62                                   ;@line 502
					_label9:
						Cast ::temp64 ::temp64                                   ;@line 502
						JumpF ::temp64 _label10                                  ;@line 502
						CallMethod GetCombatState ::Artillero_var ::temp65       ;@line 502
						CompareEQ ::temp62 ::temp65 1                            ;@line 502
						Cast ::temp64 ::temp62                                   ;@line 502
					_label10:
						Assign valid ::temp64                                    ;@line 502
						Cast ::temp66 target                                     ;@line 503
						CallMethod HasLOS ::Artillero_var ::temp62 ::temp66      ;@line 503
						Assign visible ::temp62                                  ;@line 503
						CallMethod GetCombatTarget ::Artillero_var ::temp63      ;@line 504
						Assign combatTarget ::temp63                             ;@line 504
						CallMethod Current self ::temp64 expectedGeneration expectedToken  ;@line 505
						Cast ::temp62 ::temp64                                   ;@line 505
						JumpF ::temp62 _label11                                  ;@line 505
						Cast ::temp62 valid                                      ;@line 505
					_label11:
						Cast ::temp64 ::temp62                                   ;@line 505
						JumpF ::temp64 _label12                                  ;@line 505
						Cast ::temp64 visible                                    ;@line 505
					_label12:
						Cast ::temp64 ::temp64                                   ;@line 505
						JumpF ::temp64 _label13                                  ;@line 505
						CompareEQ ::temp62 combatTarget target                   ;@line 505
						Cast ::temp64 ::temp62                                   ;@line 505
					_label13:
						Return ::temp64                                          ;@line 505
					.endCode
				.endFunction
				.function ReleaseOwnedGuard
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp20 actor
						.local ::temp21 Bool
						.local previousGuard actor
						.local player actor
						.local ::NoneVar None
					.endLocalTable
					.code
						JumpF pinBusy _label14                                   ;@line 292
						Return None                                              ;@line 293
						Jump _label14                                            ;@line 293
					_label14:
						Assign previousGuard ownedGuard                          ;@line 295
						Cast ::temp20 None                                       ;@line 296
						Assign ownedGuard ::temp20                               ;@line 296
						Cast ::temp20 None                                       ;@line 297
						CompareEQ ::temp21 previousGuard ::temp20                ;@line 297
						JumpF ::temp21 _label15                                  ;@line 297
						Return None                                              ;@line 298
						Jump _label15                                            ;@line 298
					_label15:
						Assign pinBusy True                                      ;@line 300
						CallStatic game GetPlayer ::temp20                       ;@line 301
						Assign player ::temp20                                   ;@line 301
						CompareEQ ::temp21 previousGuard player                  ;@line 302
						Not ::temp21 ::temp21                                    ;@line 302
						JumpF ::temp21 _label16                                  ;@line 302
						CallMethod SetDontMove previousGuard ::NoneVar False     ;@line 303
						Jump _label16                                            ;@line 303
					_label16:
						Assign pinBusy False                                     ;@line 305
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 306
					.endCode
				.endFunction
				.function PlaySceneAnimation
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param name String
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp27 Bool
						.local started Bool
						.local valid Bool
					.endLocalTable
					.code
						Cast ::temp27 sceneBusy                                  ;@line 345
						JumpT ::temp27 _label17                                  ;@line 345
						CallMethod Current self ::temp27 expectedGeneration expectedToken  ;@line 345
						Not ::temp27 ::temp27                                    ;@line 345
						Cast ::temp27 ::temp27                                   ;@line 345
					_label17:
						JumpF ::temp27 _label18                                  ;@line 345
						Return False                                             ;@line 346
						Jump _label18                                            ;@line 346
					_label18:
						Assign sceneBusy True                                    ;@line 348
						CallMethod PlayGamebryoAnimation self ::temp27 name True 0.000000  ;@line 349
						Assign started ::temp27                                  ;@line 349
						CallMethod FinishSceneEffect self ::temp27 expectedGeneration expectedToken  ;@line 350
						Assign valid ::temp27                                    ;@line 350
						Cast ::temp27 valid                                      ;@line 351
						JumpF ::temp27 _label19                                  ;@line 351
						Cast ::temp27 started                                    ;@line 351
					_label19:
						Return ::temp27                                          ;@line 351
					.endCode
				.endFunction
				.function WriteAimNode
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param node String
						.param matrix Float[]
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp30 Bool
						.local ::temp31 ObjectReference
					.endLocalTable
					.code
						Cast ::temp30 sceneBusy                                  ;@line 364
						JumpT ::temp30 _label20                                  ;@line 364
						CallMethod Current self ::temp30 expectedGeneration expectedToken  ;@line 364
						Not ::temp30 ::temp30                                    ;@line 364
						Cast ::temp30 ::temp30                                   ;@line 364
					_label20:
						JumpF ::temp30 _label21                                  ;@line 364
						Return None                                              ;@line 365
						Jump _label21                                            ;@line 365
					_label21:
						Assign sceneBusy True                                    ;@line 367
						Cast ::temp31 self                                       ;@line 368
						CallStatic netimmerse SetNodeLocalRotationMatrix ::temp30 ::temp31 node matrix False  ;@line 368
						CallMethod FinishSceneEffect self ::temp30 expectedGeneration expectedToken  ;@line 369
					.endCode
				.endFunction
				.function RestoreNeutralScene
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp24 Bool
						.local loaded Bool
						.local ::temp25 ObjectReference
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod Is3DLoaded self ::temp24                      ;@line 327
						Assign loaded ::temp24                                   ;@line 327
						JumpF loaded _label22                                    ;@line 328
						CallMethod PlayGamebryoAnimation self ::temp24 "Reset" True 0.000000  ;@line 329
						Cast ::temp25 self                                       ;@line 330
						CallStatic netimmerse SetNodeScale ::NoneVar ::temp25 ::VisualBoltNode_var 1.000000 False  ;@line 330
						Jump _label22                                            ;@line 330
					_label22:
					.endCode
				.endFunction
				.function FinishSceneEffect
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp26 Bool
						.local valid Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod Current self ::temp26 expectedGeneration expectedToken  ;@line 335
						Assign valid ::temp26                                    ;@line 335
						Not ::temp26 valid                                       ;@line 336
						JumpF ::temp26 _label23                                  ;@line 336
						CallMethod RestoreNeutralScene self ::NoneVar            ;@line 337
						Jump _label23                                            ;@line 337
					_label23:
						Assign sceneBusy False                                   ;@line 339
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 340
						Return valid                                             ;@line 341
					.endCode
				.endFunction
				.function CaptureMatrices
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
					.localTable
						.local ::temp32 Int
						.local ::temp33 Bool
						.local ::temp34 Bool
						.local ::temp35 ObjectReference
						.local ::temp36 Float[]
						.local ::temp37 Float
						.local captureGeneration Int
					.endLocalTable
					.code
						Assign captureGeneration generation                      ;@line 373
						CallStatic skse GetVersion ::temp32                      ;@line 374
						CompareLT ::temp33 ::temp32 2                            ;@line 374
						Cast ::temp33 ::temp33                                   ;@line 374
						JumpT ::temp33 _label24                                  ;@line 374
						CallMethod Is3DLoaded self ::temp34                      ;@line 374
						Not ::temp34 ::temp34                                    ;@line 374
						Cast ::temp33 ::temp34                                   ;@line 374
					_label24:
						JumpF ::temp33 _label25                                  ;@line 374
						Return False                                             ;@line 375
						Jump _label25                                            ;@line 375
					_label25:
						Cast ::temp35 self                                       ;@line 377
						CallStatic netimmerse HasNode ::temp34 ::temp35 ::YawNode_var False  ;@line 377
						Not ::temp33 ::temp34                                    ;@line 377
						Cast ::temp33 ::temp33                                   ;@line 377
						JumpT ::temp33 _label26                                  ;@line 377
						Cast ::temp35 self                                       ;@line 377
						CallStatic netimmerse HasNode ::temp34 ::temp35 ::PitchNode_var False  ;@line 377
						Not ::temp34 ::temp34                                    ;@line 377
						Cast ::temp33 ::temp34                                   ;@line 377
					_label26:
						Cast ::temp33 ::temp33                                   ;@line 377
						JumpT ::temp33 _label27                                  ;@line 377
						Cast ::temp35 self                                       ;@line 377
						CallStatic netimmerse HasNode ::temp34 ::temp35 ::MuzzleNode_var False  ;@line 377
						Not ::temp34 ::temp34                                    ;@line 377
						Cast ::temp33 ::temp34                                   ;@line 377
					_label27:
						Cast ::temp33 ::temp33                                   ;@line 377
						JumpT ::temp33 _label28                                  ;@line 377
						Cast ::temp35 self                                       ;@line 377
						CallStatic netimmerse HasNode ::temp34 ::temp35 ::VisualBoltNode_var False  ;@line 377
						Not ::temp34 ::temp34                                    ;@line 377
						Cast ::temp33 ::temp34                                   ;@line 377
					_label28:
						JumpF ::temp33 _label29                                  ;@line 377
						Return False                                             ;@line 378
						Jump _label29                                            ;@line 378
					_label29:
						CompareEQ ::temp34 generation captureGeneration          ;@line 380
						Not ::temp34 ::temp34                                    ;@line 380
						Cast ::temp34 ::temp34                                   ;@line 380
						JumpT ::temp34 _label30                                  ;@line 380
						CompareEQ ::temp33 token -1                              ;@line 380
						Not ::temp33 ::temp33                                    ;@line 380
						Cast ::temp34 ::temp33                                   ;@line 380
					_label30:
						Cast ::temp34 ::temp34                                   ;@line 380
						JumpT ::temp34 _label31                                  ;@line 380
						Not ::temp33 recovering                                  ;@line 380
						Cast ::temp34 ::temp33                                   ;@line 380
					_label31:
						JumpF ::temp34 _label32                                  ;@line 380
						Return False                                             ;@line 381
						Jump _label32                                            ;@line 381
					_label32:
						ArrayCreate ::temp36 9                                   ;@line 386
						Assign yawBase ::temp36                                  ;@line 386
						ArrayCreate ::temp36 9                                   ;@line 387
						Assign pitchBase ::temp36                                ;@line 387
						ArrayCreate ::temp36 9                                   ;@line 388
						Assign yawMatrix ::temp36                                ;@line 388
						ArrayCreate ::temp36 9                                   ;@line 389
						Assign pitchMatrix ::temp36                              ;@line 389
						ArrayCreate ::temp36 9                                   ;@line 390
						Assign rootWorldMatrix ::temp36                          ;@line 390
						ArrayCreate ::temp36 9                                   ;@line 391
						Assign muzzleWorldMatrix ::temp36                        ;@line 391
						ArrayCreate ::temp36 3                                   ;@line 392
						Assign rootPosition ::temp36                             ;@line 392
						ArrayCreate ::temp36 3                                   ;@line 393
						Assign muzzlePosition ::temp36                           ;@line 393
						Assign ::temp37 1.000000                                 ;@line 394
						ArraySetElement yawBase 0 ::temp37                       ;@line 394
						Assign ::temp37 1.000000                                 ;@line 395
						ArraySetElement yawBase 4 ::temp37                       ;@line 395
						Assign ::temp37 1.000000                                 ;@line 396
						ArraySetElement yawBase 8 ::temp37                       ;@line 396
						Assign ::temp37 1.000000                                 ;@line 397
						ArraySetElement pitchBase 0 ::temp37                     ;@line 397
						Assign ::temp37 1.000000                                 ;@line 398
						ArraySetElement pitchBase 4 ::temp37                     ;@line 398
						Assign ::temp37 1.000000                                 ;@line 399
						ArraySetElement pitchBase 8 ::temp37                     ;@line 399
						Assign matricesReady True                                ;@line 400
						Return True                                              ;@line 401
					.endCode
				.endFunction
				.function ApplyAim
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp38 Bool
						.local ::temp39 Bool
						.local ::temp40 Float
						.local ::NoneVar None
						.local yc Float
						.local ys Float
						.local pc Float
						.local ps Float
						.local j Int
						.local ::temp41 Float
						.local ::temp42 Int
						.local ::temp43 Float
					.endLocalTable
					.code
						CallMethod Current self ::temp38 expectedGeneration expectedToken  ;@line 405
						Not ::temp38 ::temp38                                    ;@line 405
						Cast ::temp38 ::temp38                                   ;@line 405
						JumpT ::temp38 _label33                                  ;@line 405
						Not ::temp39 matricesReady                               ;@line 405
						Cast ::temp38 ::temp39                                   ;@line 405
					_label33:
						JumpF ::temp38 _label34                                  ;@line 405
						Return None                                              ;@line 406
						Jump _label34                                            ;@line 406
					_label34:
						CallStatic math Cos ::temp40 yaw                         ;@line 408
						Assign yc ::temp40                                       ;@line 408
						CallStatic math Sin ::temp40 yaw                         ;@line 409
						Assign ys ::temp40                                       ;@line 409
						FNegate ::temp40 pitch                                   ;@line 410
						CallStatic math Cos ::temp40 ::temp40                    ;@line 410
						Assign pc ::temp40                                       ;@line 410
						FNegate ::temp40 pitch                                   ;@line 411
						CallStatic math Sin ::temp40 ::temp40                    ;@line 411
						Assign ps ::temp40                                       ;@line 411
						CallMethod Current self ::temp39 expectedGeneration expectedToken  ;@line 412
						Not ::temp38 ::temp39                                    ;@line 412
						JumpF ::temp38 _label35                                  ;@line 412
						Return None                                              ;@line 413
						Jump _label35                                            ;@line 413
					_label35:
						Assign j 0                                               ;@line 415
					_label37:
						CompareLT ::temp39 j 3                                   ;@line 416
						JumpF ::temp39 _label36                                  ;@line 416
						ArrayGetElement ::temp41 yawBase j                       ;@line 417
						FMultiply ::temp41 yc ::temp41                           ;@line 417
						IAdd ::temp42 j 3                                        ;@line 417
						ArrayGetElement ::temp43 yawBase ::temp42                ;@line 417
						FMultiply ::temp43 ys ::temp43                           ;@line 417
						FSubtract ::temp41 ::temp41 ::temp43                     ;@line 417
						Assign ::temp40 ::temp41                                 ;@line 417
						ArraySetElement yawMatrix j ::temp40                     ;@line 417
						ArrayGetElement ::temp40 yawBase j                       ;@line 418
						FMultiply ::temp41 ys ::temp40                           ;@line 418
						IAdd ::temp42 j 3                                        ;@line 418
						ArrayGetElement ::temp40 yawBase ::temp42                ;@line 418
						FMultiply ::temp40 yc ::temp40                           ;@line 418
						FAdd ::temp41 ::temp41 ::temp40                          ;@line 418
						Assign ::temp43 ::temp41                                 ;@line 418
						IAdd ::temp42 j 3                                        ;@line 418
						ArraySetElement yawMatrix ::temp42 ::temp43              ;@line 418
						IAdd ::temp42 j 6                                        ;@line 419
						ArrayGetElement ::temp43 yawBase ::temp42                ;@line 419
						Assign ::temp40 ::temp43                                 ;@line 419
						IAdd ::temp42 j 6                                        ;@line 419
						ArraySetElement yawMatrix ::temp42 ::temp40              ;@line 419
						ArrayGetElement ::temp40 pitchBase j                     ;@line 420
						Assign ::temp41 ::temp40                                 ;@line 420
						ArraySetElement pitchMatrix j ::temp41                   ;@line 420
						IAdd ::temp42 j 3                                        ;@line 421
						ArrayGetElement ::temp41 pitchBase ::temp42              ;@line 421
						FMultiply ::temp40 pc ::temp41                           ;@line 421
						IAdd ::temp42 j 6                                        ;@line 421
						ArrayGetElement ::temp41 pitchBase ::temp42              ;@line 421
						FMultiply ::temp41 ps ::temp41                           ;@line 421
						FSubtract ::temp40 ::temp40 ::temp41                     ;@line 421
						Assign ::temp43 ::temp40                                 ;@line 421
						IAdd ::temp42 j 3                                        ;@line 421
						ArraySetElement pitchMatrix ::temp42 ::temp43            ;@line 421
						IAdd ::temp42 j 3                                        ;@line 422
						ArrayGetElement ::temp43 pitchBase ::temp42              ;@line 422
						FMultiply ::temp40 ps ::temp43                           ;@line 422
						IAdd ::temp42 j 6                                        ;@line 422
						ArrayGetElement ::temp43 pitchBase ::temp42              ;@line 422
						FMultiply ::temp43 pc ::temp43                           ;@line 422
						FAdd ::temp40 ::temp40 ::temp43                          ;@line 422
						Assign ::temp41 ::temp40                                 ;@line 422
						IAdd ::temp42 j 6                                        ;@line 422
						ArraySetElement pitchMatrix ::temp42 ::temp41            ;@line 422
						IAdd ::temp42 j 1                                        ;@line 423
						Assign j ::temp42                                        ;@line 423
						Jump _label37                                            ;@line 423
					_label36:
						CallMethod WriteAimNode self ::NoneVar ::YawNode_var yawMatrix expectedGeneration expectedToken  ;@line 427
						CallMethod Current self ::temp38 expectedGeneration expectedToken  ;@line 428
						Not ::temp39 ::temp38                                    ;@line 428
						JumpF ::temp39 _label38                                  ;@line 428
						Return None                                              ;@line 429
						Jump _label38                                            ;@line 429
					_label38:
						CallMethod WriteAimNode self ::NoneVar ::PitchNode_var pitchMatrix expectedGeneration expectedToken  ;@line 431
					.endCode
				.endFunction
				.function BeginShot
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param target actor
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp98 Bool
						.local ::temp99 Bool
						.local ::temp100 Float
						.local now Float
						.local cadence Float
						.local started Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod Current self ::temp98 expectedGeneration expectedToken  ;@line 725
						Not ::temp98 ::temp98                                    ;@line 725
						Cast ::temp98 ::temp98                                   ;@line 725
						JumpT ::temp98 _label39                                  ;@line 725
						CompareEQ ::temp99 phase 0                               ;@line 725
						Not ::temp99 ::temp99                                    ;@line 725
						Cast ::temp98 ::temp99                                   ;@line 725
					_label39:
						JumpF ::temp98 _label40                                  ;@line 725
						Return None                                              ;@line 726
						Jump _label40                                            ;@line 726
					_label40:
						CallStatic utility GetCurrentRealTime ::temp100          ;@line 728
						Assign now ::temp100                                     ;@line 728
						CallMethod Current self ::temp99 expectedGeneration expectedToken  ;@line 729
						Not ::temp98 ::temp99                                    ;@line 729
						Cast ::temp98 ::temp98                                   ;@line 729
						JumpT ::temp98 _label41                                  ;@line 729
						CompareEQ ::temp99 phase 0                               ;@line 729
						Not ::temp99 ::temp99                                    ;@line 729
						Cast ::temp98 ::temp99                                   ;@line 729
					_label41:
						Cast ::temp98 ::temp98                                   ;@line 729
						JumpT ::temp98 _label42                                  ;@line 729
						CompareLT ::temp99 now nextShotAt                        ;@line 729
						Cast ::temp98 ::temp99                                   ;@line 729
					_label42:
						JumpF ::temp98 _label43                                  ;@line 729
						Return None                                              ;@line 730
						Jump _label43                                            ;@line 730
					_label43:
						Assign phase 1                                           ;@line 732
						Assign phaseAt now                                       ;@line 733
						Assign shotTarget target                                 ;@line 734
						Assign cadence ::CadenceSeconds_var                      ;@line 735
						CallMethod Finite self ::temp99 cadence 4.000000 60.000000  ;@line 736
						Not ::temp98 ::temp99                                    ;@line 736
						JumpF ::temp98 _label44                                  ;@line 736
						Assign cadence 4.000000                                  ;@line 737
						Jump _label44                                            ;@line 737
					_label44:
						FAdd ::temp100 now cadence                               ;@line 739
						Assign nextShotAt ::temp100                              ;@line 739
						CallMethod PlaySceneAnimation self ::temp99 "Fire" expectedGeneration expectedToken  ;@line 740
						Assign started ::temp99                                  ;@line 740
						CallMethod Current self ::temp98 expectedGeneration expectedToken  ;@line 741
						Not ::temp99 ::temp98                                    ;@line 741
						Cast ::temp99 ::temp99                                   ;@line 741
						JumpT ::temp99 _label45                                  ;@line 741
						CompareEQ ::temp98 phase 1                               ;@line 741
						Not ::temp98 ::temp98                                    ;@line 741
						Cast ::temp99 ::temp98                                   ;@line 741
					_label45:
						Cast ::temp99 ::temp99                                   ;@line 741
						JumpT ::temp99 _label46                                  ;@line 741
						CompareEQ ::temp98 shotTarget target                     ;@line 741
						Not ::temp98 ::temp98                                    ;@line 741
						Cast ::temp99 ::temp98                                   ;@line 741
					_label46:
						JumpF ::temp99 _label47                                  ;@line 741
						Return None                                              ;@line 742
						Jump _label47                                            ;@line 742
					_label47:
						Not ::temp98 started                                     ;@line 744
						JumpF ::temp98 _label48                                  ;@line 744
						CallMethod AbortShot self ::NoneVar expectedGeneration expectedToken  ;@line 745
						Jump _label48                                            ;@line 745
					_label48:
					.endCode
				.endFunction
				.function Current
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp1 Bool
						.local ::temp2 Bool
					.endLocalTable
					.code
						Cast ::temp1 running                                     ;@line 93
						JumpF ::temp1 _label49                                   ;@line 93
						Not ::temp1 recovering                                   ;@line 93
						Cast ::temp1 ::temp1                                     ;@line 93
					_label49:
						Cast ::temp1 ::temp1                                     ;@line 93
						JumpF ::temp1 _label50                                   ;@line 93
						Not ::temp2 destroyed                                    ;@line 93
						Cast ::temp1 ::temp2                                     ;@line 93
					_label50:
						Cast ::temp1 ::temp1                                     ;@line 93
						JumpF ::temp1 _label51                                   ;@line 93
						Not ::temp2 faulted                                      ;@line 93
						Cast ::temp1 ::temp2                                     ;@line 93
					_label51:
						Cast ::temp1 ::temp1                                     ;@line 93
						JumpF ::temp1 _label52                                   ;@line 93
						CompareEQ ::temp2 generation expectedGeneration          ;@line 93
						Cast ::temp1 ::temp2                                     ;@line 93
					_label52:
						Cast ::temp1 ::temp1                                     ;@line 93
						JumpF ::temp1 _label53                                   ;@line 93
						CompareEQ ::temp2 token expectedToken                    ;@line 93
						Cast ::temp1 ::temp2                                     ;@line 93
					_label53:
						Cast ::temp1 ::temp1                                     ;@line 93
						JumpF ::temp1 _label54                                   ;@line 93
						CompareGT ::temp2 token 0                                ;@line 93
						Cast ::temp1 ::temp2                                     ;@line 93
					_label54:
						Return ::temp1                                           ;@line 93
					.endCode
				.endFunction
				.function SetVisualBolt
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param scale Float
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp28 Bool
						.local ::temp29 ObjectReference
						.local ::NoneVar None
					.endLocalTable
					.code
						Cast ::temp28 sceneBusy                                  ;@line 355
						JumpT ::temp28 _label55                                  ;@line 355
						CallMethod Current self ::temp28 expectedGeneration expectedToken  ;@line 355
						Not ::temp28 ::temp28                                    ;@line 355
						Cast ::temp28 ::temp28                                   ;@line 355
					_label55:
						JumpF ::temp28 _label56                                  ;@line 355
						Return None                                              ;@line 356
						Jump _label56                                            ;@line 356
					_label56:
						Assign sceneBusy True                                    ;@line 358
						Cast ::temp29 self                                       ;@line 359
						CallStatic netimmerse SetNodeScale ::NoneVar ::temp29 ::VisualBoltNode_var scale False  ;@line 359
						CallMethod FinishSceneEffect self ::temp28 expectedGeneration expectedToken  ;@line 360
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
						CallMethod BlockActivation self ::NoneVar True           ;@line 63
						CallMethod BeginRecovery self ::NoneVar                  ;@line 64
					.endCode
				.endFunction
				.function StartReset
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp109 Float
						.local ::temp110 Bool
						.local now Float
						.local started Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallStatic utility GetCurrentRealTime ::temp109          ;@line 814
						Assign now ::temp109                                     ;@line 814
						CallMethod Current self ::temp110 expectedGeneration expectedToken  ;@line 815
						Not ::temp110 ::temp110                                  ;@line 815
						JumpF ::temp110 _label57                                 ;@line 815
						Return None                                              ;@line 816
						Jump _label57                                            ;@line 816
					_label57:
						Assign phase 3                                           ;@line 818
						Assign phaseAt now                                       ;@line 819
						CallMethod PlaySceneAnimation self ::temp110 "Reset" expectedGeneration expectedToken  ;@line 820
						Assign started ::temp110                                 ;@line 820
						CallMethod Current self ::temp110 expectedGeneration expectedToken  ;@line 821
						Not ::temp110 ::temp110                                  ;@line 821
						JumpF ::temp110 _label58                                 ;@line 821
						Return None                                              ;@line 822
						Jump _label58                                            ;@line 822
					_label58:
						Not ::temp110 started                                    ;@line 824
						JumpF ::temp110 _label59                                 ;@line 824
						Assign faulted True                                      ;@line 825
						CallMethod Shutdown self ::NoneVar                       ;@line 826
						Jump _label59                                            ;@line 826
					_label59:
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
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod BlockActivation self ::NoneVar True           ;@line 89
					.endCode
				.endFunction
				.function BeginRecovery
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp5 Int
						.local ::temp6 actor
						.local ::temp7 Bool
						.local ::NoneVar None
						.local ::temp8 Bool
						.local ::temp9 ObjectReference
						.local ::temp10 weapon
						.local ::temp11 ammo
						.local ::temp12 Float
						.local recoveryGeneration Int
						.local player actor
						.local gunLoaded Bool
						.local guardLoaded Bool
						.local guardDead Bool
						.local guardDisabled Bool
						.local captured Bool
						.local distance Float
						.local ::temp13 Bool
						.local aliveAfterMove Bool
						.local pinAcquired Bool
						.local recoveryToken Int
						.local now Float
						.local resetStarted Bool
					.endLocalTable
					.code
						Assign running False                                     ;@line 101
						IAdd ::temp5 generation 1                                ;@line 102
						Assign generation ::temp5                                ;@line 102
						Assign recoveryGeneration generation                     ;@line 103
						Assign token -1                                          ;@line 104
						IAdd ::temp5 serial 1                                    ;@line 105
						Assign serial ::temp5                                    ;@line 105
						Assign recovering True                                   ;@line 106
						Assign updating False                                    ;@line 107
						Assign phase 0                                           ;@line 108
						Cast ::temp6 None                                        ;@line 109
						Assign shotTarget ::temp6                                ;@line 109
						Assign faulted False                                     ;@line 110
						Assign matricesReady False                               ;@line 111
						Assign recoveryRequested False                           ;@line 112
						Cast ::temp7 pinBusy                                     ;@line 113
						JumpT ::temp7 _label60                                   ;@line 113
						Cast ::temp7 sceneBusy                                   ;@line 113
					_label60:
						JumpF ::temp7 _label61                                   ;@line 113
						Assign recoveryRequested True                            ;@line 116
						Assign recovering False                                  ;@line 117
						Return None                                              ;@line 118
						Jump _label61                                            ;@line 118
					_label61:
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 120
						CompareEQ ::temp7 generation recoveryGeneration          ;@line 121
						Not ::temp7 ::temp7                                      ;@line 121
						Cast ::temp7 ::temp7                                     ;@line 121
						JumpT ::temp7 _label62                                   ;@line 121
						CompareEQ ::temp8 token -1                               ;@line 121
						Not ::temp8 ::temp8                                      ;@line 121
						Cast ::temp7 ::temp8                                     ;@line 121
					_label62:
						JumpF ::temp7 _label63                                   ;@line 121
						Return None                                              ;@line 122
						Jump _label63                                            ;@line 122
					_label63:
						CallMethod ReleaseOwnedGuard self ::NoneVar              ;@line 124
						CompareEQ ::temp8 generation recoveryGeneration          ;@line 125
						Not ::temp8 ::temp8                                      ;@line 125
						Cast ::temp8 ::temp8                                     ;@line 125
						JumpT ::temp8 _label64                                   ;@line 125
						CompareEQ ::temp7 token -1                               ;@line 125
						Not ::temp7 ::temp7                                      ;@line 125
						Cast ::temp8 ::temp7                                     ;@line 125
					_label64:
						JumpF ::temp8 _label65                                   ;@line 125
						Return None                                              ;@line 126
						Jump _label65                                            ;@line 126
					_label65:
						CallStatic game GetPlayer ::temp6                        ;@line 128
						Assign player ::temp6                                    ;@line 128
						CompareEQ ::temp7 generation recoveryGeneration          ;@line 129
						Not ::temp7 ::temp7                                      ;@line 129
						Cast ::temp7 ::temp7                                     ;@line 129
						JumpT ::temp7 _label66                                   ;@line 129
						CompareEQ ::temp8 token -1                               ;@line 129
						Not ::temp8 ::temp8                                      ;@line 129
						Cast ::temp7 ::temp8                                     ;@line 129
					_label66:
						JumpF ::temp7 _label67                                   ;@line 129
						Return None                                              ;@line 130
						Jump _label67                                            ;@line 130
					_label67:
						CallMethod BlockActivation self ::NoneVar True           ;@line 132
						CompareEQ ::temp8 generation recoveryGeneration          ;@line 133
						Not ::temp8 ::temp8                                      ;@line 133
						Cast ::temp8 ::temp8                                     ;@line 133
						JumpT ::temp8 _label68                                   ;@line 133
						CompareEQ ::temp7 token -1                               ;@line 133
						Not ::temp7 ::temp7                                      ;@line 133
						Cast ::temp8 ::temp7                                     ;@line 133
					_label68:
						JumpF ::temp8 _label69                                   ;@line 133
						Return None                                              ;@line 134
						Jump _label69                                            ;@line 134
					_label69:
						Cast ::temp8 destroyed                                   ;@line 136
						JumpT ::temp8 _label70                                   ;@line 136
						Cast ::temp6 None                                        ;@line 136
						CompareEQ ::temp7 ::Artillero_var ::temp6                ;@line 136
						Cast ::temp8 ::temp7                                     ;@line 136
					_label70:
						Cast ::temp8 ::temp8                                     ;@line 136
						JumpT ::temp8 _label71                                   ;@line 136
						CompareEQ ::temp7 ::Artillero_var player                 ;@line 136
						Cast ::temp8 ::temp7                                     ;@line 136
					_label71:
						Cast ::temp8 ::temp8                                     ;@line 136
						JumpT ::temp8 _label72                                   ;@line 136
						Cast ::temp9 None                                        ;@line 136
						CompareEQ ::temp7 ::Puesto_var ::temp9                   ;@line 136
						Cast ::temp8 ::temp7                                     ;@line 136
					_label72:
						Cast ::temp8 ::temp8                                     ;@line 136
						JumpT ::temp8 _label73                                   ;@line 136
						Cast ::temp10 None                                       ;@line 136
						CompareEQ ::temp7 ::Launcher_var ::temp10                ;@line 136
						Cast ::temp8 ::temp7                                     ;@line 136
					_label73:
						Cast ::temp8 ::temp8                                     ;@line 136
						JumpT ::temp8 _label74                                   ;@line 136
						Cast ::temp11 None                                       ;@line 136
						CompareEQ ::temp7 ::ShotAmmo_var ::temp11                ;@line 136
						Cast ::temp8 ::temp7                                     ;@line 136
					_label74:
						JumpF ::temp8 _label75                                   ;@line 136
						Assign faulted True                                      ;@line 137
						Assign recovering False                                  ;@line 138
						Return None                                              ;@line 139
						Jump _label75                                            ;@line 139
					_label75:
						CallMethod Is3DLoaded self ::temp7                       ;@line 141
						Assign gunLoaded ::temp7                                 ;@line 141
						CallMethod Is3DLoaded ::Artillero_var ::temp8            ;@line 142
						Assign guardLoaded ::temp8                               ;@line 142
						CallMethod IsDead ::Artillero_var ::temp7                ;@line 143
						Assign guardDead ::temp7                                 ;@line 143
						CallMethod IsDisabled ::Artillero_var ::temp8            ;@line 144
						Assign guardDisabled ::temp8                             ;@line 144
						CompareEQ ::temp7 generation recoveryGeneration          ;@line 145
						Not ::temp7 ::temp7                                      ;@line 145
						Cast ::temp7 ::temp7                                     ;@line 145
						JumpT ::temp7 _label76                                   ;@line 145
						CompareEQ ::temp8 token -1                               ;@line 145
						Not ::temp8 ::temp8                                      ;@line 145
						Cast ::temp7 ::temp8                                     ;@line 145
					_label76:
						JumpF ::temp7 _label77                                   ;@line 145
						Return None                                              ;@line 146
						Jump _label77                                            ;@line 146
					_label77:
						Cast ::temp8 guardDead                                   ;@line 148
						JumpT ::temp8 _label78                                   ;@line 148
						Cast ::temp8 guardDisabled                               ;@line 148
					_label78:
						Cast ::temp7 ::temp8                                     ;@line 148
						JumpT ::temp7 _label79                                   ;@line 148
						Cast ::temp7 destroyed                                   ;@line 148
					_label79:
						JumpF ::temp7 _label80                                   ;@line 148
						Assign faulted True                                      ;@line 149
						Assign recovering False                                  ;@line 150
						Return None                                              ;@line 151
						Jump _label80                                            ;@line 151
					_label80:
						Not ::temp8 gunLoaded                                    ;@line 153
						Cast ::temp8 ::temp8                                     ;@line 153
						JumpT ::temp8 _label81                                   ;@line 153
						Not ::temp7 guardLoaded                                  ;@line 153
						Cast ::temp8 ::temp7                                     ;@line 153
					_label81:
						JumpF ::temp8 _label82                                   ;@line 153
						Assign recovering False                                  ;@line 154
						JumpF gunLoaded _label83                                 ;@line 155
						CallMethod RegisterForSingleUpdate self ::NoneVar 1.000000  ;@line 156
						Jump _label83                                            ;@line 156
					_label83:
						Return None                                              ;@line 158
						Jump _label82                                            ;@line 158
					_label82:
						CallMethod CaptureMatrices self ::temp7                  ;@line 160
						Assign captured ::temp7                                  ;@line 160
						CompareEQ ::temp8 generation recoveryGeneration          ;@line 161
						Not ::temp8 ::temp8                                      ;@line 161
						Cast ::temp8 ::temp8                                     ;@line 161
						JumpT ::temp8 _label84                                   ;@line 161
						CompareEQ ::temp7 token -1                               ;@line 161
						Not ::temp7 ::temp7                                      ;@line 161
						Cast ::temp8 ::temp7                                     ;@line 161
					_label84:
						JumpF ::temp8 _label85                                   ;@line 161
						Return None                                              ;@line 162
						Jump _label85                                            ;@line 162
					_label85:
						Not ::temp7 captured                                     ;@line 164
						JumpF ::temp7 _label86                                   ;@line 164
						Assign faulted True                                      ;@line 165
						Assign recovering False                                  ;@line 166
						CallStatic debug Trace ::NoneVar "AstraAsedioGuard: missing or invalid model controls; controller stopped." 0  ;@line 167
						Return None                                              ;@line 168
						Jump _label86                                            ;@line 168
					_label86:
						CallMethod GetDistance ::Artillero_var ::temp12 ::Puesto_var  ;@line 170
						Assign distance ::temp12                                 ;@line 170
						CompareEQ ::temp8 generation recoveryGeneration          ;@line 171
						Not ::temp8 ::temp8                                      ;@line 171
						Cast ::temp8 ::temp8                                     ;@line 171
						JumpT ::temp8 _label87                                   ;@line 171
						CompareEQ ::temp7 token -1                               ;@line 171
						Not ::temp7 ::temp7                                      ;@line 171
						Cast ::temp8 ::temp7                                     ;@line 171
					_label87:
						JumpF ::temp8 _label88                                   ;@line 171
						Return None                                              ;@line 172
						Jump _label88                                            ;@line 172
					_label88:
						CallMethod Finite self ::temp7 distance 0.000000 1000000.000000  ;@line 174
						Not ::temp8 ::temp7                                      ;@line 174
						JumpF ::temp8 _label89                                   ;@line 174
						Assign faulted True                                      ;@line 175
						Assign recovering False                                  ;@line 176
						Return None                                              ;@line 177
						Jump _label89                                            ;@line 177
					_label89:
						CompareGT ::temp7 distance 64.000000                     ;@line 179
						JumpF ::temp7 _label90                                   ;@line 179
						CallMethod MoveTo ::Artillero_var ::NoneVar ::Puesto_var 0.000000 0.000000 0.000000 True  ;@line 182
						CompareEQ ::temp8 generation recoveryGeneration          ;@line 183
						Not ::temp8 ::temp8                                      ;@line 183
						Cast ::temp8 ::temp8                                     ;@line 183
						JumpT ::temp8 _label91                                   ;@line 183
						CompareEQ ::temp13 token -1                              ;@line 183
						Not ::temp13 ::temp13                                    ;@line 183
						Cast ::temp8 ::temp13                                    ;@line 183
					_label91:
						JumpF ::temp8 _label92                                   ;@line 183
						Return None                                              ;@line 184
						Jump _label92                                            ;@line 184
					_label92:
						Jump _label90                                            ;@line 184
					_label90:
						CallMethod IsDead ::Artillero_var ::temp13               ;@line 187
						Not ::temp8 ::temp13                                     ;@line 187
						Cast ::temp7 ::temp8                                     ;@line 187
						JumpF ::temp7 _label93                                   ;@line 187
						CallMethod IsDisabled ::Artillero_var ::temp7            ;@line 187
						Not ::temp13 ::temp7                                     ;@line 187
						Cast ::temp7 ::temp13                                    ;@line 187
					_label93:
						Cast ::temp13 ::temp7                                    ;@line 187
						JumpF ::temp13 _label94                                  ;@line 187
						CallMethod Is3DLoaded ::Artillero_var ::temp8            ;@line 187
						Cast ::temp13 ::temp8                                    ;@line 187
					_label94:
						Assign aliveAfterMove ::temp13                           ;@line 187
						CompareEQ ::temp7 generation recoveryGeneration          ;@line 188
						Not ::temp7 ::temp7                                      ;@line 188
						Cast ::temp13 ::temp7                                    ;@line 188
						JumpT ::temp13 _label95                                  ;@line 188
						CompareEQ ::temp8 token -1                               ;@line 188
						Not ::temp8 ::temp8                                      ;@line 188
						Cast ::temp13 ::temp8                                    ;@line 188
					_label95:
						JumpF ::temp13 _label96                                  ;@line 188
						Return None                                              ;@line 189
						Jump _label96                                            ;@line 189
					_label96:
						Not ::temp7 aliveAfterMove                               ;@line 191
						JumpF ::temp7 _label97                                   ;@line 191
						Assign faulted True                                      ;@line 192
						Assign recovering False                                  ;@line 193
						Return None                                              ;@line 194
						Jump _label97                                            ;@line 194
					_label97:
						CallMethod AcquirePin self ::temp8 recoveryGeneration    ;@line 196
						Assign pinAcquired ::temp8                               ;@line 196
						CompareEQ ::temp13 generation recoveryGeneration         ;@line 197
						Not ::temp13 ::temp13                                    ;@line 197
						Cast ::temp8 ::temp13                                    ;@line 197
						JumpT ::temp8 _label98                                   ;@line 197
						CompareEQ ::temp7 token -1                               ;@line 197
						Not ::temp7 ::temp7                                      ;@line 197
						Cast ::temp8 ::temp7                                     ;@line 197
					_label98:
						JumpF ::temp8 _label99                                   ;@line 197
						Return None                                              ;@line 198
						Jump _label99                                            ;@line 198
					_label99:
						Not ::temp13 pinAcquired                                 ;@line 200
						JumpF ::temp13 _label100                                 ;@line 200
						Assign faulted True                                      ;@line 201
						Assign recovering False                                  ;@line 202
						Return None                                              ;@line 203
						Jump _label100                                           ;@line 203
					_label100:
						Assign yaw 0.000000                                      ;@line 205
						Assign pitch 0.000000                                    ;@line 206
						Assign token serial                                      ;@line 207
						Assign running True                                      ;@line 208
						Assign recovering False                                  ;@line 209
						Assign recoveryToken token                               ;@line 210
						CallStatic utility GetCurrentRealTime ::temp12           ;@line 211
						Assign now ::temp12                                      ;@line 211
						CallMethod Current self ::temp7 recoveryGeneration recoveryToken  ;@line 212
						Not ::temp8 ::temp7                                      ;@line 212
						JumpF ::temp8 _label101                                  ;@line 212
						Return None                                              ;@line 213
						Jump _label101                                           ;@line 213
					_label101:
						CallMethod Finite self ::temp13 now 0.000000 1000000000.000000  ;@line 215
						Not ::temp7 ::temp13                                     ;@line 215
						JumpF ::temp7 _label102                                  ;@line 215
						Assign faulted True                                      ;@line 216
						CallMethod Shutdown self ::NoneVar                       ;@line 217
						Return None                                              ;@line 218
						Jump _label102                                           ;@line 218
					_label102:
						Assign lastTick now                                      ;@line 220
						FAdd ::temp12 now 4.000000                               ;@line 221
						Assign nextShotAt ::temp12                               ;@line 221
						CallMethod PlaySceneAnimation self ::temp8 "Reset" recoveryGeneration recoveryToken  ;@line 222
						Assign resetStarted ::temp8                              ;@line 222
						CallMethod Current self ::temp13 recoveryGeneration recoveryToken  ;@line 223
						Not ::temp7 ::temp13                                     ;@line 223
						JumpF ::temp7 _label103                                  ;@line 223
						Return None                                              ;@line 224
						Jump _label103                                           ;@line 224
					_label103:
						Not ::temp8 resetStarted                                 ;@line 226
						JumpF ::temp8 _label104                                  ;@line 226
						Assign faulted True                                      ;@line 227
						CallMethod Shutdown self ::NoneVar                       ;@line 228
						Return None                                              ;@line 229
						Jump _label104                                           ;@line 229
					_label104:
						CallMethod ApplyAim self ::NoneVar recoveryGeneration recoveryToken  ;@line 231
						CallMethod Current self ::temp13 recoveryGeneration recoveryToken  ;@line 232
						Not ::temp7 ::temp13                                     ;@line 232
						JumpF ::temp7 _label105                                  ;@line 232
						Return None                                              ;@line 233
						Jump _label105                                           ;@line 233
					_label105:
						CallMethod SetVisualBolt self ::NoneVar 1.000000 recoveryGeneration recoveryToken  ;@line 235
						CallMethod Current self ::temp8 recoveryGeneration recoveryToken  ;@line 236
						JumpF ::temp8 _label106                                  ;@line 236
						CallMethod RegisterForSingleUpdate self ::NoneVar 0.200000  ;@line 237
						Jump _label106                                           ;@line 237
					_label106:
					.endCode
				.endFunction
				.function OnUpdate
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp112 Bool
						.local ::temp113 Float
						.local ::NoneVar None
						.local updateGeneration Int
						.local updateToken Int
						.local now Float
						.local dt Float
						.local ready Bool
						.local ::temp114 Bool
						.local ::temp115 Bool
						.local dead Bool
						.local guardLoaded Bool
						.local gunLoaded Bool
						.local menuOpen Bool
						.local releaseDelay Float
						.local fireDelay Float
						.local resetDelay Float
						.local ::temp116 Bool
						.local ::temp117 actor
						.local target actor
						.local sampled Bool
						.local poseRead Bool
						.local ::temp118 Float
						.local heading Float
						.local aligned Bool
					.endLocalTable
					.code
						Cast ::temp112 updating                                  ;@line 839
						JumpT ::temp112 _label107                                ;@line 839
						Cast ::temp112 recovering                                ;@line 839
					_label107:
						Cast ::temp112 ::temp112                                 ;@line 839
						JumpT ::temp112 _label108                                ;@line 839
						Cast ::temp112 pinBusy                                   ;@line 839
					_label108:
						Cast ::temp112 ::temp112                                 ;@line 839
						JumpT ::temp112 _label109                                ;@line 839
						Cast ::temp112 sceneBusy                                 ;@line 839
					_label109:
						Cast ::temp112 ::temp112                                 ;@line 839
						JumpT ::temp112 _label110                                ;@line 839
						Cast ::temp112 destroyed                                 ;@line 839
					_label110:
						Cast ::temp112 ::temp112                                 ;@line 839
						JumpT ::temp112 _label111                                ;@line 839
						Cast ::temp112 faulted                                   ;@line 839
					_label111:
						JumpF ::temp112 _label112                                ;@line 839
						Return None                                              ;@line 840
						Jump _label112                                           ;@line 840
					_label112:
						Not ::temp112 running                                    ;@line 842
						JumpF ::temp112 _label113                                ;@line 842
						CallMethod BeginRecovery self ::NoneVar                  ;@line 843
						Return None                                              ;@line 844
						Jump _label113                                           ;@line 844
					_label113:
						Assign updating True                                     ;@line 846
						Assign updateGeneration generation                       ;@line 847
						Assign updateToken token                                 ;@line 848
						CallStatic utility GetCurrentRealTime ::temp113          ;@line 849
						Assign now ::temp113                                     ;@line 849
						CallMethod Current self ::temp112 updateGeneration updateToken  ;@line 850
						Not ::temp112 ::temp112                                  ;@line 850
						JumpF ::temp112 _label114                                ;@line 850
						Return None                                              ;@line 851
						Jump _label114                                           ;@line 851
					_label114:
						CallMethod Finite self ::temp112 now 0.000000 1000000000.000000  ;@line 853
						Not ::temp112 ::temp112                                  ;@line 853
						JumpF ::temp112 _label115                                ;@line 853
						Assign faulted True                                      ;@line 854
						CallMethod Shutdown self ::NoneVar                       ;@line 855
						Return None                                              ;@line 856
						Jump _label115                                           ;@line 856
					_label115:
						CompareLT ::temp112 now lastTick                         ;@line 858
						JumpF ::temp112 _label116                                ;@line 858
						CallMethod BeginRecovery self ::NoneVar                  ;@line 861
						Return None                                              ;@line 862
						Jump _label116                                           ;@line 862
					_label116:
						FSubtract ::temp113 now lastTick                         ;@line 864
						Assign dt ::temp113                                      ;@line 864
						CompareGT ::temp112 dt 0.400000                          ;@line 865
						JumpF ::temp112 _label117                                ;@line 865
						Assign dt 0.400000                                       ;@line 866
						Jump _label117                                           ;@line 866
					_label117:
						Assign lastTick now                                      ;@line 868
						CallMethod GuardReady self ::temp112 updateGeneration updateToken  ;@line 869
						Assign ready ::temp112                                   ;@line 869
						CallMethod Current self ::temp112 updateGeneration updateToken  ;@line 870
						Not ::temp112 ::temp112                                  ;@line 870
						JumpF ::temp112 _label118                                ;@line 870
						Return None                                              ;@line 871
						Jump _label118                                           ;@line 871
					_label118:
						Not ::temp112 ready                                      ;@line 873
						JumpF ::temp112 _label119                                ;@line 873
						CallMethod IsDead ::Artillero_var ::temp114              ;@line 874
						Assign dead ::temp114                                    ;@line 874
						CallMethod Is3DLoaded ::Artillero_var ::temp114          ;@line 875
						Assign guardLoaded ::temp114                             ;@line 875
						CallMethod Is3DLoaded self ::temp114                     ;@line 876
						Assign gunLoaded ::temp114                               ;@line 876
						CallMethod Current self ::temp114 updateGeneration updateToken  ;@line 877
						Not ::temp114 ::temp114                                  ;@line 877
						JumpF ::temp114 _label120                                ;@line 877
						Return None                                              ;@line 878
						Jump _label120                                           ;@line 878
					_label120:
						Cast ::temp114 dead                                      ;@line 882
						JumpT ::temp114 _label121                                ;@line 882
						Cast ::temp114 guardLoaded                               ;@line 882
					_label121:
						Assign faulted ::temp114                                 ;@line 882
						CallMethod Shutdown self ::NoneVar                       ;@line 883
						Not ::temp114 faulted                                    ;@line 884
						Cast ::temp114 ::temp114                                 ;@line 884
						JumpF ::temp114 _label122                                ;@line 884
						Cast ::temp114 gunLoaded                                 ;@line 884
					_label122:
						Cast ::temp114 ::temp114                                 ;@line 884
						JumpF ::temp114 _label123                                ;@line 884
						Not ::temp115 destroyed                                  ;@line 884
						Cast ::temp114 ::temp115                                 ;@line 884
					_label123:
						JumpF ::temp114 _label124                                ;@line 884
						CallMethod RegisterForSingleUpdate self ::NoneVar 1.000000  ;@line 885
						Jump _label124                                           ;@line 885
					_label124:
						Return None                                              ;@line 887
						Jump _label119                                           ;@line 887
					_label119:
						CallStatic utility IsInMenuMode ::temp115                ;@line 889
						Assign menuOpen ::temp115                                ;@line 889
						CallMethod Current self ::temp114 updateGeneration updateToken  ;@line 890
						Not ::temp112 ::temp114                                  ;@line 890
						JumpF ::temp112 _label125                                ;@line 890
						Return None                                              ;@line 891
						Jump _label125                                           ;@line 891
					_label125:
						Cast ::temp115 menuOpen                                  ;@line 893
						JumpF ::temp115 _label126                                ;@line 893
						CompareEQ ::temp115 phase 1                              ;@line 893
						Cast ::temp112 ::temp115                                 ;@line 893
						JumpT ::temp112 _label127                                ;@line 893
						CompareEQ ::temp114 phase 2                              ;@line 893
						Cast ::temp112 ::temp114                                 ;@line 893
					_label127:
						Cast ::temp115 ::temp112                                 ;@line 893
					_label126:
						JumpF ::temp115 _label128                                ;@line 893
						CallMethod AbortShot self ::NoneVar updateGeneration updateToken  ;@line 894
						Jump _label128                                           ;@line 894
					_label128:
						CallMethod Current self ::temp114 updateGeneration updateToken  ;@line 896
						Not ::temp112 ::temp114                                  ;@line 896
						JumpF ::temp112 _label129                                ;@line 896
						Return None                                              ;@line 897
						Jump _label129                                           ;@line 897
					_label129:
						CompareEQ ::temp115 phase 1                              ;@line 899
						JumpF ::temp115 _label130                                ;@line 899
						Assign releaseDelay ::ReleaseSeconds_var                 ;@line 901
						CallMethod Finite self ::temp114 releaseDelay 0.100000 1.000000  ;@line 902
						Not ::temp112 ::temp114                                  ;@line 902
						JumpF ::temp112 _label131                                ;@line 902
						Assign releaseDelay 0.100000                             ;@line 903
						Jump _label131                                           ;@line 903
					_label131:
						FAdd ::temp113 phaseAt releaseDelay                      ;@line 905
						CompareGTE ::temp114 now ::temp113                       ;@line 905
						JumpF ::temp114 _label132                                ;@line 905
						CallMethod CommitShot self ::NoneVar shotTarget updateGeneration updateToken  ;@line 906
						Jump _label132                                           ;@line 906
					_label132:
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 0.200000  ;@line 908
						Return None                                              ;@line 909
						Jump _label133                                           ;@line 909
					_label130:
						CompareEQ ::temp112 phase 2                              ;@line 910
						JumpF ::temp112 _label134                                ;@line 910
						Assign fireDelay ::FireSeconds_var                       ;@line 911
						CallMethod Finite self ::temp114 fireDelay 0.300000 2.000000  ;@line 912
						Not ::temp114 ::temp114                                  ;@line 912
						JumpF ::temp114 _label135                                ;@line 912
						Assign fireDelay 0.300000                                ;@line 913
						Jump _label135                                           ;@line 913
					_label135:
						FAdd ::temp113 phaseAt fireDelay                         ;@line 915
						CompareGTE ::temp114 now ::temp113                       ;@line 915
						JumpF ::temp114 _label136                                ;@line 915
						CallMethod StartReset self ::NoneVar updateGeneration updateToken  ;@line 916
						Jump _label136                                           ;@line 916
					_label136:
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 0.200000  ;@line 918
						Return None                                              ;@line 919
						Jump _label133                                           ;@line 919
					_label134:
						CompareEQ ::temp114 phase 3                              ;@line 920
						JumpF ::temp114 _label133                                ;@line 920
						Assign resetDelay ::ResetSeconds_var                     ;@line 921
						CallMethod Finite self ::temp112 resetDelay 1.200000 5.000000  ;@line 922
						Not ::temp112 ::temp112                                  ;@line 922
						JumpF ::temp112 _label137                                ;@line 922
						Assign resetDelay 1.200000                               ;@line 923
						Jump _label137                                           ;@line 923
					_label137:
						FAdd ::temp113 phaseAt resetDelay                        ;@line 925
						CompareGTE ::temp112 now ::temp113                       ;@line 925
						JumpF ::temp112 _label138                                ;@line 925
						CallMethod SetVisualBolt self ::NoneVar 1.000000 updateGeneration updateToken  ;@line 926
						CallMethod Current self ::temp116 updateGeneration updateToken  ;@line 927
						Not ::temp116 ::temp116                                  ;@line 927
						JumpF ::temp116 _label139                                ;@line 927
						Return None                                              ;@line 928
						Jump _label139                                           ;@line 928
					_label139:
						Assign phase 0                                           ;@line 930
						Cast ::temp117 None                                      ;@line 931
						Assign shotTarget ::temp117                              ;@line 931
						Jump _label138                                           ;@line 931
					_label138:
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 0.200000  ;@line 933
						Return None                                              ;@line 934
						Jump _label133                                           ;@line 934
					_label133:
						JumpF menuOpen _label140                                 ;@line 936
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 1.000000  ;@line 937
						Return None                                              ;@line 938
						Jump _label140                                           ;@line 938
					_label140:
						CallMethod GetCombatTarget ::Artillero_var ::temp117     ;@line 940
						Assign target ::temp117                                  ;@line 940
						CallMethod SampleTarget self ::temp116 target updateGeneration updateToken  ;@line 941
						Assign sampled ::temp116                                 ;@line 941
						CallMethod Current self ::temp112 updateGeneration updateToken  ;@line 942
						Not ::temp114 ::temp112                                  ;@line 942
						JumpF ::temp114 _label141                                ;@line 942
						Return None                                              ;@line 943
						Jump _label141                                           ;@line 943
					_label141:
						Not ::temp115 sampled                                    ;@line 945
						JumpF ::temp115 _label142                                ;@line 945
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 1.000000  ;@line 946
						Return None                                              ;@line 947
						Jump _label142                                           ;@line 947
					_label142:
						CallMethod TurnToward self ::NoneVar dt updateGeneration updateToken  ;@line 949
						CallMethod Current self ::temp116 updateGeneration updateToken  ;@line 950
						Not ::temp112 ::temp116                                  ;@line 950
						JumpF ::temp112 _label143                                ;@line 950
						Return None                                              ;@line 951
						Jump _label143                                           ;@line 951
					_label143:
						CallMethod ReadPose self ::temp114 updateGeneration updateToken  ;@line 953
						Assign poseRead ::temp114                                ;@line 953
						CallMethod Current self ::temp115 updateGeneration updateToken  ;@line 954
						Not ::temp116 ::temp115                                  ;@line 954
						JumpF ::temp116 _label144                                ;@line 954
						Return None                                              ;@line 955
						Jump _label144                                           ;@line 955
					_label144:
						JumpF poseRead _label145                                 ;@line 957
						ArrayGetElement ::temp113 muzzleWorldMatrix 1            ;@line 958
						ArrayGetElement ::temp118 muzzleWorldMatrix 4            ;@line 958
						CallMethod HeadingFromVector self ::temp113 ::temp113 ::temp118 0.000000  ;@line 958
						Assign heading ::temp113                                 ;@line 958
						CallMethod Current self ::temp112 updateGeneration updateToken  ;@line 959
						Not ::temp114 ::temp112                                  ;@line 959
						JumpF ::temp114 _label146                                ;@line 959
						Return None                                              ;@line 960
						Jump _label146                                           ;@line 960
					_label146:
						CallMethod SetAngle ::Artillero_var ::NoneVar 0.000000 0.000000 heading  ;@line 962
						Jump _label145                                           ;@line 962
					_label145:
						CompareGTE ::temp115 now nextShotAt                      ;@line 965
						JumpF ::temp115 _label147                                ;@line 965
						CallMethod ShotPreflight self ::temp116 target updateGeneration updateToken  ;@line 966
						Assign aligned ::temp116                                 ;@line 966
						CallMethod Current self ::temp112 updateGeneration updateToken  ;@line 967
						Not ::temp114 ::temp112                                  ;@line 967
						JumpF ::temp114 _label148                                ;@line 967
						Return None                                              ;@line 968
						Jump _label148                                           ;@line 968
					_label148:
						JumpF aligned _label149                                  ;@line 970
						CallMethod BeginShot self ::NoneVar target updateGeneration updateToken  ;@line 971
						Jump _label149                                           ;@line 971
					_label149:
						Jump _label147                                           ;@line 971
					_label147:
						CallMethod Current self ::temp116 updateGeneration updateToken  ;@line 974
						JumpF ::temp116 _label150                                ;@line 974
						CompareEQ ::temp112 phase 1                              ;@line 975
						JumpF ::temp112 _label151                                ;@line 975
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 0.100000  ;@line 976
						Jump _label152                                           ;@line 976
					_label151:
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 0.200000  ;@line 978
					_label152:
						Jump _label150                                           ;@line 978
					_label150:
					.endCode
				.endFunction
				.function AbortShot
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp107 Bool
						.local ::temp108 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod Current self ::temp107 expectedGeneration expectedToken  ;@line 807
						Not ::temp107 ::temp107                                  ;@line 807
						Cast ::temp107 ::temp107                                 ;@line 807
						JumpT ::temp107 _label153                                ;@line 807
						CompareEQ ::temp108 phase 0                              ;@line 807
						Cast ::temp107 ::temp108                                 ;@line 807
					_label153:
						JumpF ::temp107 _label154                                ;@line 807
						Return None                                              ;@line 808
						Jump _label154                                           ;@line 808
					_label154:
						CallMethod StartReset self ::NoneVar expectedGeneration expectedToken  ;@line 810
					.endCode
				.endFunction
				.function Shutdown
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp14 Int
						.local ::temp15 actor
						.local ::NoneVar None
						.local ::temp16 Bool
						.local ::temp17 Bool
						.local cleanupGeneration Int
					.endLocalTable
					.code
						Assign running False                                     ;@line 242
						IAdd ::temp14 generation 1                               ;@line 243
						Assign generation ::temp14                               ;@line 243
						Assign cleanupGeneration generation                      ;@line 244
						Assign token -1                                          ;@line 245
						Assign recovering False                                  ;@line 246
						Assign updating False                                    ;@line 247
						Assign phase 0                                           ;@line 248
						Cast ::temp15 None                                       ;@line 249
						Assign shotTarget ::temp15                               ;@line 249
						Assign matricesReady False                               ;@line 250
						Assign recoveryRequested False                           ;@line 251
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 252
						CompareEQ ::temp16 generation cleanupGeneration          ;@line 253
						Not ::temp16 ::temp16                                    ;@line 253
						Cast ::temp16 ::temp16                                   ;@line 253
						JumpT ::temp16 _label155                                 ;@line 253
						CompareEQ ::temp17 token -1                              ;@line 253
						Not ::temp17 ::temp17                                    ;@line 253
						Cast ::temp16 ::temp17                                   ;@line 253
					_label155:
						JumpF ::temp16 _label156                                 ;@line 253
						Return None                                              ;@line 254
						Jump _label156                                           ;@line 254
					_label156:
						CallMethod ReleaseOwnedGuard self ::NoneVar              ;@line 258
						CompareEQ ::temp17 generation cleanupGeneration          ;@line 259
						Not ::temp17 ::temp17                                    ;@line 259
						Cast ::temp17 ::temp17                                   ;@line 259
						JumpT ::temp17 _label157                                 ;@line 259
						CompareEQ ::temp16 token -1                              ;@line 259
						Not ::temp16 ::temp16                                    ;@line 259
						Cast ::temp17 ::temp16                                   ;@line 259
					_label157:
						JumpF ::temp17 _label158                                 ;@line 259
						Return None                                              ;@line 260
						Jump _label158                                           ;@line 260
					_label158:
						Not ::temp16 sceneBusy                                   ;@line 262
						JumpF ::temp16 _label159                                 ;@line 262
						Assign sceneBusy True                                    ;@line 263
						CallMethod RestoreNeutralScene self ::NoneVar            ;@line 264
						Assign sceneBusy False                                   ;@line 265
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 266
						Jump _label159                                           ;@line 266
					_label159:
					.endCode
				.endFunction
				.function FinishUpdate
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param expectedGeneration Int
						.param expectedToken Int
						.param delay Float
					.endParamTable
					.localTable
						.local ::temp111 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod Current self ::temp111 expectedGeneration expectedToken  ;@line 831
						Not ::temp111 ::temp111                                  ;@line 831
						JumpF ::temp111 _label160                                ;@line 831
						Return None                                              ;@line 832
						Jump _label160                                           ;@line 832
					_label160:
						Assign updating False                                    ;@line 834
						CallMethod RegisterForSingleUpdate self ::NoneVar delay  ;@line 835
					.endCode
				.endFunction
				.function Finite
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param value Float
						.param minimum Float
						.param maximum Float
					.endParamTable
					.localTable
						.local ::temp3 Bool
						.local ::temp4 Bool
					.endLocalTable
					.code
						CompareEQ ::temp3 value value                            ;@line 97
						Cast ::temp3 ::temp3                                     ;@line 97
						JumpF ::temp3 _label161                                  ;@line 97
						CompareGTE ::temp4 value minimum                         ;@line 97
						Cast ::temp3 ::temp4                                     ;@line 97
					_label161:
						Cast ::temp3 ::temp3                                     ;@line 97
						JumpF ::temp3 _label162                                  ;@line 97
						CompareLTE ::temp4 value maximum                         ;@line 97
						Cast ::temp3 ::temp4                                     ;@line 97
					_label162:
						Return ::temp3                                           ;@line 97
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
						.local ::temp0 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CompareGT ::temp0 aiCurrentStage 0                       ;@line 82
						JumpF ::temp0 _label163                                  ;@line 82
						Assign destroyed True                                    ;@line 83
						CallMethod Shutdown self ::NoneVar                       ;@line 84
						Jump _label163                                           ;@line 84
					_label163:
					.endCode
				.endFunction
				.function RotationValid
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param matrix Float[]
					.endParamTable
					.localTable
						.local ::temp44 Bool
						.local ::temp48 Float
						.local ::temp49 Float
						.local ::temp50 Float
						.local ::temp51 Float
						.local i Int
						.local ::temp45 Float
						.local ::temp46 Bool
						.local ::temp47 Int
						.local a Float
						.local b Float
						.local c Float
						.local ab Float
						.local ac Float
						.local bc Float
						.local determinant Float
					.endLocalTable
					.code
						Assign i 0                                               ;@line 435
					_label166:
						CompareLT ::temp44 i 9                                   ;@line 436
						JumpF ::temp44 _label164                                 ;@line 436
						ArrayGetElement ::temp45 matrix i                        ;@line 437
						CallMethod Finite self ::temp46 ::temp45 -1.050000 1.050000  ;@line 437
						Not ::temp46 ::temp46                                    ;@line 437
						JumpF ::temp46 _label165                                 ;@line 437
						Return False                                             ;@line 438
						Jump _label165                                           ;@line 438
					_label165:
						IAdd ::temp47 i 1                                        ;@line 440
						Assign i ::temp47                                        ;@line 440
						Jump _label166                                           ;@line 440
					_label164:
						ArrayGetElement ::temp45 matrix 0                        ;@line 442
						ArrayGetElement ::temp48 matrix 0                        ;@line 442
						FMultiply ::temp45 ::temp45 ::temp48                     ;@line 442
						ArrayGetElement ::temp48 matrix 3                        ;@line 442
						ArrayGetElement ::temp49 matrix 3                        ;@line 442
						FMultiply ::temp48 ::temp48 ::temp49                     ;@line 442
						FAdd ::temp49 ::temp45 ::temp48                          ;@line 442
						ArrayGetElement ::temp45 matrix 6                        ;@line 442
						ArrayGetElement ::temp48 matrix 6                        ;@line 442
						FMultiply ::temp45 ::temp45 ::temp48                     ;@line 442
						FAdd ::temp48 ::temp49 ::temp45                          ;@line 442
						Assign a ::temp48                                        ;@line 442
						ArrayGetElement ::temp49 matrix 1                        ;@line 443
						ArrayGetElement ::temp45 matrix 1                        ;@line 443
						FMultiply ::temp48 ::temp49 ::temp45                     ;@line 443
						ArrayGetElement ::temp49 matrix 4                        ;@line 443
						ArrayGetElement ::temp45 matrix 4                        ;@line 443
						FMultiply ::temp49 ::temp49 ::temp45                     ;@line 443
						FAdd ::temp45 ::temp48 ::temp49                          ;@line 443
						ArrayGetElement ::temp48 matrix 7                        ;@line 443
						ArrayGetElement ::temp49 matrix 7                        ;@line 443
						FMultiply ::temp48 ::temp48 ::temp49                     ;@line 443
						FAdd ::temp49 ::temp45 ::temp48                          ;@line 443
						Assign b ::temp49                                        ;@line 443
						ArrayGetElement ::temp45 matrix 2                        ;@line 444
						ArrayGetElement ::temp48 matrix 2                        ;@line 444
						FMultiply ::temp49 ::temp45 ::temp48                     ;@line 444
						ArrayGetElement ::temp45 matrix 5                        ;@line 444
						ArrayGetElement ::temp48 matrix 5                        ;@line 444
						FMultiply ::temp45 ::temp45 ::temp48                     ;@line 444
						FAdd ::temp48 ::temp49 ::temp45                          ;@line 444
						ArrayGetElement ::temp49 matrix 8                        ;@line 444
						ArrayGetElement ::temp45 matrix 8                        ;@line 444
						FMultiply ::temp49 ::temp49 ::temp45                     ;@line 444
						FAdd ::temp45 ::temp48 ::temp49                          ;@line 444
						Assign c ::temp45                                        ;@line 444
						ArrayGetElement ::temp48 matrix 0                        ;@line 445
						ArrayGetElement ::temp49 matrix 1                        ;@line 445
						FMultiply ::temp45 ::temp48 ::temp49                     ;@line 445
						ArrayGetElement ::temp48 matrix 3                        ;@line 445
						ArrayGetElement ::temp49 matrix 4                        ;@line 445
						FMultiply ::temp48 ::temp48 ::temp49                     ;@line 445
						FAdd ::temp49 ::temp45 ::temp48                          ;@line 445
						ArrayGetElement ::temp45 matrix 6                        ;@line 445
						ArrayGetElement ::temp48 matrix 7                        ;@line 445
						FMultiply ::temp45 ::temp45 ::temp48                     ;@line 445
						FAdd ::temp48 ::temp49 ::temp45                          ;@line 445
						Assign ab ::temp48                                       ;@line 445
						ArrayGetElement ::temp49 matrix 0                        ;@line 446
						ArrayGetElement ::temp45 matrix 2                        ;@line 446
						FMultiply ::temp48 ::temp49 ::temp45                     ;@line 446
						ArrayGetElement ::temp49 matrix 3                        ;@line 446
						ArrayGetElement ::temp45 matrix 5                        ;@line 446
						FMultiply ::temp49 ::temp49 ::temp45                     ;@line 446
						FAdd ::temp45 ::temp48 ::temp49                          ;@line 446
						ArrayGetElement ::temp48 matrix 6                        ;@line 446
						ArrayGetElement ::temp49 matrix 8                        ;@line 446
						FMultiply ::temp48 ::temp48 ::temp49                     ;@line 446
						FAdd ::temp49 ::temp45 ::temp48                          ;@line 446
						Assign ac ::temp49                                       ;@line 446
						ArrayGetElement ::temp45 matrix 1                        ;@line 447
						ArrayGetElement ::temp48 matrix 2                        ;@line 447
						FMultiply ::temp49 ::temp45 ::temp48                     ;@line 447
						ArrayGetElement ::temp45 matrix 4                        ;@line 447
						ArrayGetElement ::temp48 matrix 5                        ;@line 447
						FMultiply ::temp45 ::temp45 ::temp48                     ;@line 447
						FAdd ::temp48 ::temp49 ::temp45                          ;@line 447
						ArrayGetElement ::temp49 matrix 7                        ;@line 447
						ArrayGetElement ::temp45 matrix 8                        ;@line 447
						FMultiply ::temp49 ::temp49 ::temp45                     ;@line 447
						FAdd ::temp45 ::temp48 ::temp49                          ;@line 447
						Assign bc ::temp45                                       ;@line 447
						ArrayGetElement ::temp48 matrix 0                        ;@line 448
						ArrayGetElement ::temp49 matrix 4                        ;@line 448
						ArrayGetElement ::temp45 matrix 8                        ;@line 448
						FMultiply ::temp49 ::temp49 ::temp45                     ;@line 448
						ArrayGetElement ::temp45 matrix 5                        ;@line 448
						ArrayGetElement ::temp50 matrix 7                        ;@line 448
						FMultiply ::temp45 ::temp45 ::temp50                     ;@line 448
						FSubtract ::temp50 ::temp49 ::temp45                     ;@line 448
						FMultiply ::temp49 ::temp48 ::temp50                     ;@line 448
						ArrayGetElement ::temp45 matrix 1                        ;@line 448
						ArrayGetElement ::temp48 matrix 3                        ;@line 448
						ArrayGetElement ::temp50 matrix 8                        ;@line 448
						FMultiply ::temp48 ::temp48 ::temp50                     ;@line 448
						ArrayGetElement ::temp50 matrix 5                        ;@line 448
						ArrayGetElement ::temp51 matrix 6                        ;@line 448
						FMultiply ::temp50 ::temp50 ::temp51                     ;@line 448
						FSubtract ::temp51 ::temp48 ::temp50                     ;@line 448
						FMultiply ::temp48 ::temp45 ::temp51                     ;@line 448
						FSubtract ::temp50 ::temp49 ::temp48                     ;@line 448
						ArrayGetElement ::temp45 matrix 2                        ;@line 448
						ArrayGetElement ::temp51 matrix 3                        ;@line 448
						ArrayGetElement ::temp49 matrix 7                        ;@line 448
						FMultiply ::temp48 ::temp51 ::temp49                     ;@line 448
						ArrayGetElement ::temp51 matrix 4                        ;@line 448
						ArrayGetElement ::temp49 matrix 6                        ;@line 448
						FMultiply ::temp51 ::temp51 ::temp49                     ;@line 448
						FSubtract ::temp49 ::temp48 ::temp51                     ;@line 448
						FMultiply ::temp48 ::temp45 ::temp49                     ;@line 448
						FAdd ::temp51 ::temp50 ::temp48                          ;@line 448
						Assign determinant ::temp51                              ;@line 448
						FSubtract ::temp45 a 1.000000                            ;@line 449
						CallStatic math Abs ::temp49 ::temp45                    ;@line 449
						CompareLTE ::temp46 ::temp49 0.002000                    ;@line 449
						Cast ::temp46 ::temp46                                   ;@line 449
						JumpF ::temp46 _label167                                 ;@line 449
						FSubtract ::temp50 b 1.000000                            ;@line 449
						CallStatic math Abs ::temp48 ::temp50                    ;@line 449
						CompareLTE ::temp44 ::temp48 0.002000                    ;@line 449
						Cast ::temp46 ::temp44                                   ;@line 449
					_label167:
						Cast ::temp46 ::temp46                                   ;@line 449
						JumpF ::temp46 _label168                                 ;@line 449
						FSubtract ::temp51 c 1.000000                            ;@line 449
						CallStatic math Abs ::temp45 ::temp51                    ;@line 449
						CompareLTE ::temp44 ::temp45 0.002000                    ;@line 449
						Cast ::temp46 ::temp44                                   ;@line 449
					_label168:
						Cast ::temp46 ::temp46                                   ;@line 449
						JumpF ::temp46 _label169                                 ;@line 449
						CallStatic math Abs ::temp49 ab                          ;@line 449
						CompareLTE ::temp44 ::temp49 0.002000                    ;@line 449
						Cast ::temp46 ::temp44                                   ;@line 449
					_label169:
						Cast ::temp46 ::temp46                                   ;@line 449
						JumpF ::temp46 _label170                                 ;@line 449
						CallStatic math Abs ::temp50 ac                          ;@line 449
						CompareLTE ::temp44 ::temp50 0.002000                    ;@line 449
						Cast ::temp46 ::temp44                                   ;@line 449
					_label170:
						Cast ::temp46 ::temp46                                   ;@line 449
						JumpF ::temp46 _label171                                 ;@line 449
						CallStatic math Abs ::temp48 bc                          ;@line 449
						CompareLTE ::temp44 ::temp48 0.002000                    ;@line 449
						Cast ::temp46 ::temp44                                   ;@line 449
					_label171:
						Cast ::temp46 ::temp46                                   ;@line 449
						JumpF ::temp46 _label172                                 ;@line 449
						FSubtract ::temp51 determinant 1.000000                  ;@line 449
						CallStatic math Abs ::temp45 ::temp51                    ;@line 449
						CompareLTE ::temp44 ::temp45 0.004000                    ;@line 449
						Cast ::temp46 ::temp44                                   ;@line 449
					_label172:
						Return ::temp46                                          ;@line 449
					.endCode
				.endFunction
				.function Approach
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Float
					.paramTable
						.param value Float
						.param goal Float
						.param maximumStep Float
					.endParamTable
					.localTable
						.local ::temp77 Float
						.local ::temp78 Bool
						.local ::temp79 Float
						.local ::temp80 Bool
						.local difference Float
					.endLocalTable
					.code
						FSubtract ::temp77 goal value                            ;@line 597
						Assign difference ::temp77                               ;@line 597
						CompareGT ::temp78 difference maximumStep                ;@line 598
						JumpF ::temp78 _label173                                 ;@line 598
						FAdd ::temp77 value maximumStep                          ;@line 599
						Return ::temp77                                          ;@line 599
						Jump _label174                                           ;@line 599
					_label173:
						FNegate ::temp79 maximumStep                             ;@line 600
						CompareLT ::temp80 difference ::temp79                   ;@line 600
						JumpF ::temp80 _label174                                 ;@line 600
						FSubtract ::temp79 value maximumStep                     ;@line 601
						Return ::temp79                                          ;@line 601
						Jump _label174                                           ;@line 601
					_label174:
						Return goal                                              ;@line 603
					.endCode
				.endFunction
				.function OnLoad
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod BeginRecovery self ::NoneVar                  ;@line 70
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
						.local ::temp67 Float
						.local ::temp68 Float
						.local ::temp69 Bool
						.local ::temp70 Bool
						.local horizontal Float
						.local cosine Float
						.local angle Float
					.endLocalTable
					.code
						FMultiply ::temp67 vectorX vectorX                       ;@line 509
						FMultiply ::temp68 vectorY vectorY                       ;@line 509
						FAdd ::temp67 ::temp67 ::temp68                          ;@line 509
						CallStatic math Sqrt ::temp68 ::temp67                   ;@line 509
						Assign horizontal ::temp68                               ;@line 509
						CompareLT ::temp69 horizontal 0.000010                   ;@line 510
						JumpF ::temp69 _label175                                 ;@line 510
						Return fallback                                          ;@line 511
						Jump _label175                                           ;@line 511
					_label175:
						FDivide ::temp67 vectorY horizontal                      ;@line 513
						Assign cosine ::temp67                                   ;@line 513
						CompareGT ::temp69 cosine 1.000000                       ;@line 514
						JumpF ::temp69 _label176                                 ;@line 514
						Assign cosine 1.000000                                   ;@line 515
						Jump _label177                                           ;@line 515
					_label176:
						CompareLT ::temp70 cosine -1.000000                      ;@line 516
						JumpF ::temp70 _label177                                 ;@line 516
						Assign cosine -1.000000                                  ;@line 517
						Jump _label177                                           ;@line 517
					_label177:
						CallStatic math ACos ::temp68 cosine                     ;@line 519
						Assign angle ::temp68                                    ;@line 519
						CompareLT ::temp70 vectorX 0.000000                      ;@line 520
						JumpF ::temp70 _label178                                 ;@line 520
						FSubtract ::temp67 360.000000 angle                      ;@line 521
						Assign angle ::temp67                                    ;@line 521
						Jump _label178                                           ;@line 521
					_label178:
						CompareGTE ::temp69 angle 360.000000                     ;@line 523
						JumpF ::temp69 _label179                                 ;@line 523
						FSubtract ::temp68 angle 360.000000                      ;@line 524
						Assign angle ::temp68                                    ;@line 524
						Jump _label179                                           ;@line 524
					_label179:
						Return angle                                             ;@line 526
					.endCode
				.endFunction
				.function SampleTarget
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param target actor
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp71 Bool
						.local ::temp72 Bool
						.local ::temp73 Float
						.local ::temp74 Float
						.local tx Float
						.local ty Float
						.local tz Float
						.local dx Float
						.local dy Float
						.local dz Float
						.local rangeSquared Float
						.local horizontal Float
						.local tangent Float
						.local ::temp75 Float
						.local ::temp76 Bool
						.local speedSquared Float
						.local discriminant Float
						.local horizontalFactor Float
						.local wx Float
						.local wy Float
						.local wz Float
						.local lx Float
						.local ly Float
						.local lz Float
						.local nextYaw Float
						.local nextPitch Float
					.endLocalTable
					.code
						CallMethod ValidTarget self ::temp71 target expectedGeneration expectedToken  ;@line 530
						Not ::temp71 ::temp71                                    ;@line 530
						Cast ::temp71 ::temp71                                   ;@line 530
						JumpT ::temp71 _label180                                 ;@line 530
						CallMethod ReadPose self ::temp72 expectedGeneration expectedToken  ;@line 530
						Not ::temp72 ::temp72                                    ;@line 530
						Cast ::temp71 ::temp72                                   ;@line 530
					_label180:
						JumpF ::temp71 _label181                                 ;@line 530
						Return False                                             ;@line 531
						Jump _label181                                           ;@line 531
					_label181:
						CallMethod GetPositionX target ::temp73                  ;@line 533
						Assign tx ::temp73                                       ;@line 533
						CallMethod GetPositionY target ::temp73                  ;@line 534
						Assign ty ::temp73                                       ;@line 534
						CallMethod GetPositionZ target ::temp73                  ;@line 535
						FAdd ::temp73 ::temp73 ::TargetHeight_var                ;@line 535
						Assign tz ::temp73                                       ;@line 535
						CallMethod Current self ::temp72 expectedGeneration expectedToken  ;@line 536
						Not ::temp71 ::temp72                                    ;@line 536
						Cast ::temp71 ::temp71                                   ;@line 536
						JumpT ::temp71 _label182                                 ;@line 536
						CallMethod Finite self ::temp72 tx -1000000.000000 1000000.000000  ;@line 536
						Not ::temp72 ::temp72                                    ;@line 536
						Cast ::temp71 ::temp72                                   ;@line 536
					_label182:
						Cast ::temp71 ::temp71                                   ;@line 536
						JumpT ::temp71 _label183                                 ;@line 536
						CallMethod Finite self ::temp72 ty -1000000.000000 1000000.000000  ;@line 536
						Not ::temp72 ::temp72                                    ;@line 536
						Cast ::temp71 ::temp72                                   ;@line 536
					_label183:
						Cast ::temp71 ::temp71                                   ;@line 536
						JumpT ::temp71 _label184                                 ;@line 536
						CallMethod Finite self ::temp72 tz -1000000.000000 1000000.000000  ;@line 536
						Not ::temp72 ::temp72                                    ;@line 536
						Cast ::temp71 ::temp72                                   ;@line 536
					_label184:
						JumpF ::temp71 _label185                                 ;@line 536
						Return False                                             ;@line 537
						Jump _label185                                           ;@line 537
					_label185:
						ArrayGetElement ::temp73 muzzlePosition 0                ;@line 539
						FSubtract ::temp73 tx ::temp73                           ;@line 539
						Assign dx ::temp73                                       ;@line 539
						ArrayGetElement ::temp73 muzzlePosition 1                ;@line 540
						FSubtract ::temp73 ty ::temp73                           ;@line 540
						Assign dy ::temp73                                       ;@line 540
						ArrayGetElement ::temp73 muzzlePosition 2                ;@line 541
						FSubtract ::temp73 tz ::temp73                           ;@line 541
						Assign dz ::temp73                                       ;@line 541
						FMultiply ::temp73 dx dx                                 ;@line 542
						FMultiply ::temp74 dy dy                                 ;@line 542
						FAdd ::temp73 ::temp73 ::temp74                          ;@line 542
						FMultiply ::temp74 dz dz                                 ;@line 542
						FAdd ::temp73 ::temp73 ::temp74                          ;@line 542
						Assign rangeSquared ::temp73                             ;@line 542
						CallMethod Finite self ::temp72 rangeSquared 6400.000000 36000000.000000  ;@line 543
						Not ::temp71 ::temp72                                    ;@line 543
						Cast ::temp71 ::temp71                                   ;@line 543
						JumpT ::temp71 _label186                                 ;@line 543
						CallMethod Finite self ::temp72 ::ProjectileSpeed_var 1.000000 100000.000000  ;@line 543
						Not ::temp72 ::temp72                                    ;@line 543
						Cast ::temp71 ::temp72                                   ;@line 543
					_label186:
						Cast ::temp71 ::temp71                                   ;@line 543
						JumpT ::temp71 _label187                                 ;@line 543
						CallMethod Finite self ::temp72 ::ProjectileGravity_var 0.000000 5000.000000  ;@line 543
						Not ::temp72 ::temp72                                    ;@line 543
						Cast ::temp71 ::temp72                                   ;@line 543
					_label187:
						JumpF ::temp71 _label188                                 ;@line 543
						Return False                                             ;@line 544
						Jump _label188                                           ;@line 544
					_label188:
						FMultiply ::temp74 dx dx                                 ;@line 546
						FMultiply ::temp73 dy dy                                 ;@line 546
						FAdd ::temp74 ::temp74 ::temp73                          ;@line 546
						CallStatic math Sqrt ::temp73 ::temp74                   ;@line 546
						Assign horizontal ::temp73                               ;@line 546
						CompareLT ::temp72 horizontal 0.010000                   ;@line 547
						JumpF ::temp72 _label189                                 ;@line 547
						Return False                                             ;@line 548
						Jump _label189                                           ;@line 548
					_label189:
						FDivide ::temp74 dz horizontal                           ;@line 550
						Assign tangent ::temp74                                  ;@line 550
						CompareGT ::temp71 ::ProjectileGravity_var 0.000000      ;@line 551
						JumpF ::temp71 _label190                                 ;@line 551
						FMultiply ::temp73 ::ProjectileSpeed_var ::ProjectileSpeed_var  ;@line 555
						Assign speedSquared ::temp73                             ;@line 555
						FMultiply ::temp74 speedSquared speedSquared             ;@line 556
						FMultiply ::temp73 ::ProjectileGravity_var horizontal    ;@line 556
						FMultiply ::temp73 ::temp73 horizontal                   ;@line 556
						FMultiply ::temp75 2.000000 dz                           ;@line 556
						FMultiply ::temp75 ::temp75 speedSquared                 ;@line 556
						FAdd ::temp73 ::temp73 ::temp75                          ;@line 556
						FMultiply ::temp75 ::ProjectileGravity_var ::temp73      ;@line 556
						FSubtract ::temp73 ::temp74 ::temp75                     ;@line 556
						Assign discriminant ::temp73                             ;@line 556
						CompareLT ::temp72 discriminant 0.000000                 ;@line 557
						Cast ::temp72 ::temp72                                   ;@line 557
						JumpT ::temp72 _label191                                 ;@line 557
						CompareEQ ::temp76 discriminant discriminant             ;@line 557
						Not ::temp76 ::temp76                                    ;@line 557
						Cast ::temp72 ::temp76                                   ;@line 557
					_label191:
						JumpF ::temp72 _label192                                 ;@line 557
						Return False                                             ;@line 558
						Jump _label192                                           ;@line 558
					_label192:
						FMultiply ::temp74 ::ProjectileGravity_var horizontal    ;@line 560
						FMultiply ::temp75 ::temp74 horizontal                   ;@line 560
						FMultiply ::temp73 2.000000 dz                           ;@line 560
						FMultiply ::temp74 ::temp73 speedSquared                 ;@line 560
						FAdd ::temp73 ::temp75 ::temp74                          ;@line 560
						CallStatic math Sqrt ::temp75 discriminant               ;@line 560
						FAdd ::temp74 speedSquared ::temp75                      ;@line 560
						FMultiply ::temp75 horizontal ::temp74                   ;@line 560
						FDivide ::temp74 ::temp73 ::temp75                       ;@line 560
						Assign tangent ::temp74                                  ;@line 560
						Jump _label190                                           ;@line 560
					_label190:
						FMultiply ::temp73 tangent tangent                       ;@line 562
						FAdd ::temp75 1.000000 ::temp73                          ;@line 562
						CallStatic math Sqrt ::temp74 ::temp75                   ;@line 562
						FDivide ::temp73 1.000000 ::temp74                       ;@line 562
						Assign horizontalFactor ::temp73                         ;@line 562
						FDivide ::temp75 dx horizontal                           ;@line 563
						FMultiply ::temp74 ::temp75 horizontalFactor             ;@line 563
						Assign wx ::temp74                                       ;@line 563
						FDivide ::temp73 dy horizontal                           ;@line 564
						FMultiply ::temp75 ::temp73 horizontalFactor             ;@line 564
						Assign wy ::temp75                                       ;@line 564
						FMultiply ::temp74 tangent horizontalFactor              ;@line 565
						Assign wz ::temp74                                       ;@line 565
						ArrayGetElement ::temp73 rootWorldMatrix 0               ;@line 567
						FMultiply ::temp75 ::temp73 wx                           ;@line 567
						ArrayGetElement ::temp74 rootWorldMatrix 3               ;@line 567
						FMultiply ::temp73 ::temp74 wy                           ;@line 567
						FAdd ::temp74 ::temp75 ::temp73                          ;@line 567
						ArrayGetElement ::temp75 rootWorldMatrix 6               ;@line 567
						FMultiply ::temp73 ::temp75 wz                           ;@line 567
						FAdd ::temp75 ::temp74 ::temp73                          ;@line 567
						Assign lx ::temp75                                       ;@line 567
						ArrayGetElement ::temp74 rootWorldMatrix 1               ;@line 568
						FMultiply ::temp73 ::temp74 wx                           ;@line 568
						ArrayGetElement ::temp75 rootWorldMatrix 4               ;@line 568
						FMultiply ::temp74 ::temp75 wy                           ;@line 568
						FAdd ::temp75 ::temp73 ::temp74                          ;@line 568
						ArrayGetElement ::temp73 rootWorldMatrix 7               ;@line 568
						FMultiply ::temp74 ::temp73 wz                           ;@line 568
						FAdd ::temp73 ::temp75 ::temp74                          ;@line 568
						Assign ly ::temp73                                       ;@line 568
						ArrayGetElement ::temp75 rootWorldMatrix 2               ;@line 569
						FMultiply ::temp74 ::temp75 wx                           ;@line 569
						ArrayGetElement ::temp73 rootWorldMatrix 5               ;@line 569
						FMultiply ::temp75 ::temp73 wy                           ;@line 569
						FAdd ::temp73 ::temp74 ::temp75                          ;@line 569
						ArrayGetElement ::temp74 rootWorldMatrix 8               ;@line 569
						FMultiply ::temp75 ::temp74 wz                           ;@line 569
						FAdd ::temp74 ::temp73 ::temp75                          ;@line 569
						Assign lz ::temp74                                       ;@line 569
						CompareGT ::temp76 lz 1.000000                           ;@line 570
						JumpF ::temp76 _label193                                 ;@line 570
						Assign lz 1.000000                                       ;@line 571
						Jump _label194                                           ;@line 571
					_label193:
						CompareLT ::temp72 lz -1.000000                          ;@line 572
						JumpF ::temp72 _label194                                 ;@line 572
						Assign lz -1.000000                                      ;@line 573
						Jump _label194                                           ;@line 573
					_label194:
						FNegate ::temp73 ly                                      ;@line 575
						CallMethod HeadingFromVector self ::temp75 lx ::temp73 yaw  ;@line 575
						Assign nextYaw ::temp75                                  ;@line 575
						CompareGT ::temp71 nextYaw 180.000000                    ;@line 576
						JumpF ::temp71 _label195                                 ;@line 576
						FSubtract ::temp74 nextYaw 360.000000                    ;@line 577
						Assign nextYaw ::temp74                                  ;@line 577
						Jump _label195                                           ;@line 577
					_label195:
						CallStatic math ASin ::temp73 lz                         ;@line 579
						Assign nextPitch ::temp73                                ;@line 579
						CallMethod Finite self ::temp72 ::PitchMin_var -20.000000 45.000000  ;@line 581
						Not ::temp76 ::temp72                                    ;@line 581
						Cast ::temp71 ::temp76                                   ;@line 581
						JumpT ::temp71 _label196                                 ;@line 581
						CallMethod Finite self ::temp71 ::PitchMax_var -20.000000 45.000000  ;@line 581
						Not ::temp72 ::temp71                                    ;@line 581
						Cast ::temp71 ::temp72                                   ;@line 581
					_label196:
						Cast ::temp72 ::temp71                                   ;@line 581
						JumpT ::temp72 _label197                                 ;@line 581
						CompareGTE ::temp76 ::PitchMin_var ::PitchMax_var        ;@line 581
						Cast ::temp72 ::temp76                                   ;@line 581
					_label197:
						JumpF ::temp72 _label198                                 ;@line 581
						Return False                                             ;@line 582
						Jump _label198                                           ;@line 582
					_label198:
						CallMethod Finite self ::temp71 nextYaw -60.000000 60.000000  ;@line 584
						Not ::temp76 ::temp71                                    ;@line 584
						Cast ::temp72 ::temp76                                   ;@line 584
						JumpT ::temp72 _label199                                 ;@line 584
						CallMethod Finite self ::temp72 nextPitch ::PitchMin_var ::PitchMax_var  ;@line 584
						Not ::temp71 ::temp72                                    ;@line 584
						Cast ::temp72 ::temp71                                   ;@line 584
					_label199:
						Cast ::temp76 ::temp72                                   ;@line 584
						JumpT ::temp76 _label200                                 ;@line 584
						CallMethod Current self ::temp76 expectedGeneration expectedToken  ;@line 584
						Not ::temp71 ::temp76                                    ;@line 584
						Cast ::temp76 ::temp71                                   ;@line 584
					_label200:
						JumpF ::temp76 _label201                                 ;@line 584
						Return False                                             ;@line 585
						Jump _label201                                           ;@line 585
					_label201:
						Assign desiredYaw nextYaw                                ;@line 587
						Assign desiredPitch nextPitch                            ;@line 588
						Assign aimX wx                                           ;@line 589
						Assign aimY wy                                           ;@line 590
						Assign aimZ wz                                           ;@line 591
						Assign targetHorizontal horizontal                       ;@line 592
						Return True                                              ;@line 593
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
				.function TurnToward
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param dt Float
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp81 Bool
						.local ::temp82 Float
						.local ::NoneVar None
						.local rate Float
						.local nextYaw Float
						.local nextPitch Float
					.endLocalTable
					.code
						Assign rate ::TurnRate_var                               ;@line 608
						CallMethod Finite self ::temp81 rate 1.000000 30.000000  ;@line 609
						Not ::temp81 ::temp81                                    ;@line 609
						JumpF ::temp81 _label202                                 ;@line 609
						Assign rate 30.000000                                    ;@line 610
						Jump _label202                                           ;@line 610
					_label202:
						FMultiply ::temp82 rate dt                               ;@line 612
						CallMethod Approach self ::temp82 yaw desiredYaw ::temp82  ;@line 612
						Assign nextYaw ::temp82                                  ;@line 612
						FMultiply ::temp82 rate dt                               ;@line 613
						CallMethod Approach self ::temp82 pitch desiredPitch ::temp82  ;@line 613
						Assign nextPitch ::temp82                                ;@line 613
						CallMethod Current self ::temp81 expectedGeneration expectedToken  ;@line 614
						Not ::temp81 ::temp81                                    ;@line 614
						JumpF ::temp81 _label203                                 ;@line 614
						Return None                                              ;@line 615
						Jump _label203                                           ;@line 615
					_label203:
						Assign yaw nextYaw                                       ;@line 617
						Assign pitch nextPitch                                   ;@line 618
						CallMethod ApplyAim self ::NoneVar expectedGeneration expectedToken  ;@line 619
					.endCode
				.endFunction
				.function ReadPose
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp52 Bool
						.local ::temp53 Bool
						.local ::temp54 ObjectReference
						.local rootRead Bool
						.local muzzleRead Bool
						.local rootPointRead Bool
						.local muzzlePointRead Bool
						.local i Int
						.local ::temp55 Float
						.local ::temp56 Bool
						.local ::temp57 Int
					.endLocalTable
					.code
						CallMethod Current self ::temp52 expectedGeneration expectedToken  ;@line 453
						Not ::temp52 ::temp52                                    ;@line 453
						Cast ::temp52 ::temp52                                   ;@line 453
						JumpT ::temp52 _label204                                 ;@line 453
						Not ::temp53 matricesReady                               ;@line 453
						Cast ::temp52 ::temp53                                   ;@line 453
					_label204:
						JumpF ::temp52 _label205                                 ;@line 453
						Return False                                             ;@line 454
						Jump _label205                                           ;@line 454
					_label205:
						Cast ::temp54 self                                       ;@line 456
						CallStatic netimmerse GetNodeWorldRotationMatrix ::temp53 ::temp54 "" rootWorldMatrix False  ;@line 456
						Assign rootRead ::temp53                                 ;@line 456
						CallMethod Current self ::temp52 expectedGeneration expectedToken  ;@line 457
						Not ::temp53 ::temp52                                    ;@line 457
						Cast ::temp53 ::temp53                                   ;@line 457
						JumpT ::temp53 _label206                                 ;@line 457
						Not ::temp52 rootRead                                    ;@line 457
						Cast ::temp53 ::temp52                                   ;@line 457
					_label206:
						JumpF ::temp53 _label207                                 ;@line 457
						Return False                                             ;@line 458
						Jump _label207                                           ;@line 458
					_label207:
						Cast ::temp54 self                                       ;@line 460
						CallStatic netimmerse GetNodeWorldRotationMatrix ::temp52 ::temp54 ::MuzzleNode_var muzzleWorldMatrix False  ;@line 460
						Assign muzzleRead ::temp52                               ;@line 460
						CallMethod Current self ::temp53 expectedGeneration expectedToken  ;@line 461
						Not ::temp52 ::temp53                                    ;@line 461
						Cast ::temp52 ::temp52                                   ;@line 461
						JumpT ::temp52 _label208                                 ;@line 461
						Not ::temp53 muzzleRead                                  ;@line 461
						Cast ::temp52 ::temp53                                   ;@line 461
					_label208:
						JumpF ::temp52 _label209                                 ;@line 461
						Return False                                             ;@line 462
						Jump _label209                                           ;@line 462
					_label209:
						Cast ::temp54 self                                       ;@line 464
						CallStatic netimmerse GetNodeWorldPosition ::temp53 ::temp54 "" rootPosition False  ;@line 464
						Assign rootPointRead ::temp53                            ;@line 464
						CallMethod Current self ::temp52 expectedGeneration expectedToken  ;@line 465
						Not ::temp53 ::temp52                                    ;@line 465
						Cast ::temp53 ::temp53                                   ;@line 465
						JumpT ::temp53 _label210                                 ;@line 465
						Not ::temp52 rootPointRead                               ;@line 465
						Cast ::temp53 ::temp52                                   ;@line 465
					_label210:
						JumpF ::temp53 _label211                                 ;@line 465
						Return False                                             ;@line 466
						Jump _label211                                           ;@line 466
					_label211:
						Cast ::temp54 self                                       ;@line 468
						CallStatic netimmerse GetNodeWorldPosition ::temp52 ::temp54 ::MuzzleNode_var muzzlePosition False  ;@line 468
						Assign muzzlePointRead ::temp52                          ;@line 468
						CallMethod Current self ::temp53 expectedGeneration expectedToken  ;@line 469
						Not ::temp52 ::temp53                                    ;@line 469
						Cast ::temp52 ::temp52                                   ;@line 469
						JumpT ::temp52 _label212                                 ;@line 469
						Not ::temp53 muzzlePointRead                             ;@line 469
						Cast ::temp52 ::temp53                                   ;@line 469
					_label212:
						JumpF ::temp52 _label213                                 ;@line 469
						Return False                                             ;@line 470
						Jump _label213                                           ;@line 470
					_label213:
						CallMethod RotationValid self ::temp53 rootWorldMatrix   ;@line 472
						Not ::temp52 ::temp53                                    ;@line 472
						Cast ::temp52 ::temp52                                   ;@line 472
						JumpT ::temp52 _label214                                 ;@line 472
						CallMethod RotationValid self ::temp53 muzzleWorldMatrix  ;@line 472
						Not ::temp53 ::temp53                                    ;@line 472
						Cast ::temp52 ::temp53                                   ;@line 472
					_label214:
						JumpF ::temp52 _label215                                 ;@line 472
						Return False                                             ;@line 473
						Jump _label215                                           ;@line 473
					_label215:
						Assign i 0                                               ;@line 475
					_label219:
						CompareLT ::temp53 i 3                                   ;@line 476
						JumpF ::temp53 _label216                                 ;@line 476
						ArrayGetElement ::temp55 rootPosition i                  ;@line 477
						CallMethod Finite self ::temp52 ::temp55 -1000000.000000 1000000.000000  ;@line 477
						Not ::temp52 ::temp52                                    ;@line 477
						Cast ::temp52 ::temp52                                   ;@line 477
						JumpT ::temp52 _label217                                 ;@line 477
						ArrayGetElement ::temp55 muzzlePosition i                ;@line 477
						CallMethod Finite self ::temp56 ::temp55 -1000000.000000 1000000.000000  ;@line 477
						Not ::temp56 ::temp56                                    ;@line 477
						Cast ::temp52 ::temp56                                   ;@line 477
					_label217:
						JumpF ::temp52 _label218                                 ;@line 477
						Return False                                             ;@line 478
						Jump _label218                                           ;@line 478
					_label218:
						IAdd ::temp57 i 1                                        ;@line 480
						Assign i ::temp57                                        ;@line 480
						Jump _label219                                           ;@line 480
					_label216:
						CallMethod Current self ::temp56 expectedGeneration expectedToken  ;@line 482
						Return ::temp56                                          ;@line 482
					.endCode
				.endFunction
				.function AcquirePin
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param expectedGeneration Int
					.endParamTable
					.localTable
						.local ::temp18 Bool
						.local ::temp19 Bool
						.local ::NoneVar None
						.local candidate actor
					.endLocalTable
					.code
						Cast ::temp18 pinBusy                                    ;@line 271
						JumpT ::temp18 _label220                                 ;@line 271
						CompareEQ ::temp18 generation expectedGeneration         ;@line 271
						Not ::temp18 ::temp18                                    ;@line 271
						Cast ::temp18 ::temp18                                   ;@line 271
					_label220:
						Cast ::temp18 ::temp18                                   ;@line 271
						JumpT ::temp18 _label221                                 ;@line 271
						CompareEQ ::temp19 token -1                              ;@line 271
						Not ::temp19 ::temp19                                    ;@line 271
						Cast ::temp18 ::temp19                                   ;@line 271
					_label221:
						Cast ::temp18 ::temp18                                   ;@line 271
						JumpT ::temp18 _label222                                 ;@line 271
						Not ::temp19 recovering                                  ;@line 271
						Cast ::temp18 ::temp19                                   ;@line 271
					_label222:
						Cast ::temp19 ::temp18                                   ;@line 271
						JumpT ::temp19 _label223                                 ;@line 271
						Cast ::temp19 destroyed                                  ;@line 271
					_label223:
						Cast ::temp18 ::temp19                                   ;@line 271
						JumpT ::temp18 _label224                                 ;@line 271
						Cast ::temp18 faulted                                    ;@line 271
					_label224:
						JumpF ::temp18 _label225                                 ;@line 271
						Return False                                             ;@line 272
						Jump _label225                                           ;@line 272
					_label225:
						Assign candidate ::Artillero_var                         ;@line 274
						Assign pinBusy True                                      ;@line 275
						CallMethod SetDontMove candidate ::NoneVar True          ;@line 276
						CompareEQ ::temp19 generation expectedGeneration         ;@line 277
						Not ::temp19 ::temp19                                    ;@line 277
						Cast ::temp19 ::temp19                                   ;@line 277
						JumpT ::temp19 _label226                                 ;@line 277
						CompareEQ ::temp18 token -1                              ;@line 277
						Not ::temp18 ::temp18                                    ;@line 277
						Cast ::temp19 ::temp18                                   ;@line 277
					_label226:
						Cast ::temp19 ::temp19                                   ;@line 277
						JumpT ::temp19 _label227                                 ;@line 277
						Not ::temp18 recovering                                  ;@line 277
						Cast ::temp19 ::temp18                                   ;@line 277
					_label227:
						Cast ::temp18 ::temp19                                   ;@line 277
						JumpT ::temp18 _label228                                 ;@line 277
						Cast ::temp18 destroyed                                  ;@line 277
					_label228:
						Cast ::temp19 ::temp18                                   ;@line 277
						JumpT ::temp19 _label229                                 ;@line 277
						Cast ::temp19 faulted                                    ;@line 277
					_label229:
						JumpF ::temp19 _label230                                 ;@line 277
						CallMethod SetDontMove candidate ::NoneVar False         ;@line 281
						Assign pinBusy False                                     ;@line 282
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 283
						Return False                                             ;@line 284
						Jump _label230                                           ;@line 284
					_label230:
						Assign ownedGuard candidate                              ;@line 286
						Assign pinBusy False                                     ;@line 287
						Return True                                              ;@line 288
					.endCode
				.endFunction
				.function CommitShot
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param target actor
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp101 Bool
						.local ::temp102 Bool
						.local ::temp103 Float
						.local ::temp104 ObjectReference
						.local ::temp105 sound
						.local now Float
						.local safe Bool
						.local ::NoneVar None
						.local cadence Float
						.local launchedAt Float
						.local ::temp106 Int
					.endLocalTable
					.code
						CallMethod Current self ::temp101 expectedGeneration expectedToken  ;@line 750
						Not ::temp101 ::temp101                                  ;@line 750
						Cast ::temp101 ::temp101                                 ;@line 750
						JumpT ::temp101 _label231                                ;@line 750
						CompareEQ ::temp102 phase 1                              ;@line 750
						Not ::temp102 ::temp102                                  ;@line 750
						Cast ::temp101 ::temp102                                 ;@line 750
					_label231:
						Cast ::temp101 ::temp101                                 ;@line 750
						JumpT ::temp101 _label232                                ;@line 750
						CompareEQ ::temp102 shotTarget target                    ;@line 750
						Not ::temp102 ::temp102                                  ;@line 750
						Cast ::temp101 ::temp102                                 ;@line 750
					_label232:
						JumpF ::temp101 _label233                                ;@line 750
						Return None                                              ;@line 751
						Jump _label233                                           ;@line 751
					_label233:
						CallStatic utility GetCurrentRealTime ::temp103          ;@line 753
						Assign now ::temp103                                     ;@line 753
						CallMethod ShotPreflight self ::temp102 target expectedGeneration expectedToken  ;@line 756
						Assign safe ::temp102                                    ;@line 756
						CallMethod Current self ::temp101 expectedGeneration expectedToken  ;@line 757
						Not ::temp102 ::temp101                                  ;@line 757
						Cast ::temp102 ::temp102                                 ;@line 757
						JumpT ::temp102 _label234                                ;@line 757
						CompareEQ ::temp101 phase 1                              ;@line 757
						Not ::temp101 ::temp101                                  ;@line 757
						Cast ::temp102 ::temp101                                 ;@line 757
					_label234:
						Cast ::temp102 ::temp102                                 ;@line 757
						JumpT ::temp102 _label235                                ;@line 757
						CompareEQ ::temp101 shotTarget target                    ;@line 757
						Not ::temp101 ::temp101                                  ;@line 757
						Cast ::temp102 ::temp101                                 ;@line 757
					_label235:
						JumpF ::temp102 _label236                                ;@line 757
						Return None                                              ;@line 758
						Jump _label236                                           ;@line 758
					_label236:
						Not ::temp101 safe                                       ;@line 760
						Cast ::temp101 ::temp101                                 ;@line 760
						JumpT ::temp101 _label237                                ;@line 760
						CallMethod Finite self ::temp102 now 0.000000 1000000000.000000  ;@line 760
						Not ::temp102 ::temp102                                  ;@line 760
						Cast ::temp101 ::temp102                                 ;@line 760
					_label237:
						JumpF ::temp101 _label238                                ;@line 760
						CallMethod AbortShot self ::NoneVar expectedGeneration expectedToken  ;@line 761
						Return None                                              ;@line 762
						Jump _label238                                           ;@line 762
					_label238:
						Assign cadence ::CadenceSeconds_var                      ;@line 764
						CallMethod Finite self ::temp102 cadence 4.000000 60.000000  ;@line 765
						Not ::temp101 ::temp102                                  ;@line 765
						JumpF ::temp101 _label239                                ;@line 765
						Assign cadence 4.000000                                  ;@line 766
						Jump _label239                                           ;@line 766
					_label239:
						FAdd ::temp103 now cadence                               ;@line 768
						CompareLT ::temp102 nextShotAt ::temp103                 ;@line 768
						JumpF ::temp102 _label240                                ;@line 768
						FAdd ::temp103 now cadence                               ;@line 769
						Assign nextShotAt ::temp103                              ;@line 769
						Jump _label240                                           ;@line 769
					_label240:
						Assign phase 2                                           ;@line 773
						Assign phaseAt now                                       ;@line 774
						CallMethod Current self ::temp101 expectedGeneration expectedToken  ;@line 775
						Not ::temp102 ::temp101                                  ;@line 775
						Cast ::temp102 ::temp102                                 ;@line 775
						JumpT ::temp102 _label241                                ;@line 775
						CompareEQ ::temp101 phase 2                              ;@line 775
						Not ::temp101 ::temp101                                  ;@line 775
						Cast ::temp102 ::temp101                                 ;@line 775
					_label241:
						Cast ::temp102 ::temp102                                 ;@line 775
						JumpT ::temp102 _label242                                ;@line 775
						CompareEQ ::temp101 shotTarget target                    ;@line 775
						Not ::temp101 ::temp101                                  ;@line 775
						Cast ::temp102 ::temp101                                 ;@line 775
					_label242:
						JumpF ::temp102 _label243                                ;@line 775
						Return None                                              ;@line 776
						Jump _label243                                           ;@line 776
					_label243:
						Cast ::temp104 self                                      ;@line 778
						CallMethod Fire ::Launcher_var ::NoneVar ::temp104 ::ShotAmmo_var  ;@line 778
						CallMethod Current self ::temp101 expectedGeneration expectedToken  ;@line 779
						Not ::temp102 ::temp101                                  ;@line 779
						Cast ::temp102 ::temp102                                 ;@line 779
						JumpT ::temp102 _label244                                ;@line 779
						CompareEQ ::temp101 phase 2                              ;@line 779
						Not ::temp101 ::temp101                                  ;@line 779
						Cast ::temp102 ::temp101                                 ;@line 779
					_label244:
						JumpF ::temp102 _label245                                ;@line 779
						Return None                                              ;@line 780
						Jump _label245                                           ;@line 780
					_label245:
						CallStatic utility GetCurrentRealTime ::temp103          ;@line 784
						Assign launchedAt ::temp103                              ;@line 784
						CallMethod Current self ::temp101 expectedGeneration expectedToken  ;@line 785
						Not ::temp102 ::temp101                                  ;@line 785
						Cast ::temp102 ::temp102                                 ;@line 785
						JumpT ::temp102 _label246                                ;@line 785
						CompareEQ ::temp101 phase 2                              ;@line 785
						Not ::temp101 ::temp101                                  ;@line 785
						Cast ::temp102 ::temp101                                 ;@line 785
					_label246:
						JumpF ::temp102 _label247                                ;@line 785
						Return None                                              ;@line 786
						Jump _label247                                           ;@line 786
					_label247:
						CallMethod Finite self ::temp101 launchedAt 0.000000 1000000000.000000  ;@line 788
						Not ::temp102 ::temp101                                  ;@line 788
						JumpF ::temp102 _label248                                ;@line 788
						Assign faulted True                                      ;@line 789
						CallMethod Shutdown self ::NoneVar                       ;@line 790
						Return None                                              ;@line 791
						Jump _label248                                           ;@line 791
					_label248:
						Assign phaseAt launchedAt                                ;@line 793
						FAdd ::temp103 launchedAt cadence                        ;@line 794
						CompareLT ::temp101 nextShotAt ::temp103                 ;@line 794
						JumpF ::temp101 _label249                                ;@line 794
						FAdd ::temp103 launchedAt cadence                        ;@line 795
						Assign nextShotAt ::temp103                              ;@line 795
						Jump _label249                                           ;@line 795
					_label249:
						CallMethod SetVisualBolt self ::NoneVar 0.000000 expectedGeneration expectedToken  ;@line 797
						CallMethod Current self ::temp102 expectedGeneration expectedToken  ;@line 798
						Not ::temp101 ::temp102                                  ;@line 798
						Cast ::temp101 ::temp101                                 ;@line 798
						JumpT ::temp101 _label250                                ;@line 798
						CompareEQ ::temp102 phase 2                              ;@line 798
						Not ::temp102 ::temp102                                  ;@line 798
						Cast ::temp101 ::temp102                                 ;@line 798
					_label250:
						JumpF ::temp101 _label251                                ;@line 798
						Return None                                              ;@line 799
						Jump _label251                                           ;@line 799
					_label251:
						Cast ::temp105 None                                      ;@line 801
						CompareEQ ::temp102 ::ShotSound_var ::temp105            ;@line 801
						Not ::temp102 ::temp102                                  ;@line 801
						JumpF ::temp102 _label252                                ;@line 801
						Cast ::temp104 self                                      ;@line 802
						CallMethod Play ::ShotSound_var ::temp106 ::temp104      ;@line 802
						Jump _label252                                           ;@line 802
					_label252:
					.endCode
				.endFunction
				.function GuardReady
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp58 Bool
						.local ::temp59 actor
						.local ::temp60 Bool
						.local ::temp61 Float
						.local ready Bool
						.local distance Float
					.endLocalTable
					.code
						CallMethod Current self ::temp58 expectedGeneration expectedToken  ;@line 486
						Not ::temp58 ::temp58                                    ;@line 486
						Cast ::temp58 ::temp58                                   ;@line 486
						JumpT ::temp58 _label253                                 ;@line 486
						Cast ::temp59 None                                       ;@line 486
						CompareEQ ::temp60 ownedGuard ::temp59                   ;@line 486
						Cast ::temp58 ::temp60                                   ;@line 486
					_label253:
						Cast ::temp58 ::temp58                                   ;@line 486
						JumpT ::temp58 _label254                                 ;@line 486
						CompareEQ ::temp60 ownedGuard ::Artillero_var            ;@line 486
						Not ::temp60 ::temp60                                    ;@line 486
						Cast ::temp58 ::temp60                                   ;@line 486
					_label254:
						JumpF ::temp58 _label255                                 ;@line 486
						Return False                                             ;@line 487
						Jump _label255                                           ;@line 487
					_label255:
						CallMethod Is3DLoaded self ::temp60                      ;@line 489
						Cast ::temp60 ::temp60                                   ;@line 489
						JumpF ::temp60 _label256                                 ;@line 489
						CallMethod IsDisabled self ::temp58                      ;@line 489
						Not ::temp58 ::temp58                                    ;@line 489
						Cast ::temp60 ::temp58                                   ;@line 489
					_label256:
						Cast ::temp60 ::temp60                                   ;@line 489
						JumpF ::temp60 _label257                                 ;@line 489
						CallMethod Is3DLoaded ownedGuard ::temp58                ;@line 489
						Cast ::temp60 ::temp58                                   ;@line 489
					_label257:
						Cast ::temp60 ::temp60                                   ;@line 489
						JumpF ::temp60 _label258                                 ;@line 489
						CallMethod IsDead ownedGuard ::temp58                    ;@line 489
						Not ::temp58 ::temp58                                    ;@line 489
						Cast ::temp60 ::temp58                                   ;@line 489
					_label258:
						Cast ::temp60 ::temp60                                   ;@line 489
						JumpF ::temp60 _label259                                 ;@line 489
						CallMethod IsDisabled ownedGuard ::temp58                ;@line 489
						Not ::temp58 ::temp58                                    ;@line 489
						Cast ::temp60 ::temp58                                   ;@line 489
					_label259:
						Assign ready ::temp60                                    ;@line 489
						CallMethod GetDistance ownedGuard ::temp61 ::Puesto_var  ;@line 490
						Assign distance ::temp61                                 ;@line 490
						CallMethod Current self ::temp58 expectedGeneration expectedToken  ;@line 491
						Cast ::temp60 ::temp58                                   ;@line 491
						JumpF ::temp60 _label260                                 ;@line 491
						Cast ::temp60 ready                                      ;@line 491
					_label260:
						Cast ::temp60 ::temp60                                   ;@line 491
						JumpF ::temp60 _label261                                 ;@line 491
						CallMethod Finite self ::temp58 distance 0.000000 64.000000  ;@line 491
						Cast ::temp60 ::temp58                                   ;@line 491
					_label261:
						Return ::temp60                                          ;@line 491
					.endCode
				.endFunction
				.function PointNearSegment
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param px Float
						.param py Float
						.param pz Float
						.param ax Float
						.param ay Float
						.param az Float
						.param bx Float
						.param by Float
						.param bz Float
						.param radius Float
					.endParamTable
					.localTable
						.local ::temp83 Float
						.local ::temp84 Float
						.local ::temp85 Bool
						.local ::temp86 Bool
						.local dx Float
						.local dy Float
						.local dz Float
						.local lengthSquared Float
						.local along Float
					.endLocalTable
					.code
						FSubtract ::temp83 bx ax                                 ;@line 623
						Assign dx ::temp83                                       ;@line 623
						FSubtract ::temp83 by ay                                 ;@line 624
						Assign dy ::temp83                                       ;@line 624
						FSubtract ::temp83 bz az                                 ;@line 625
						Assign dz ::temp83                                       ;@line 625
						FMultiply ::temp83 dx dx                                 ;@line 626
						FMultiply ::temp84 dy dy                                 ;@line 626
						FAdd ::temp83 ::temp83 ::temp84                          ;@line 626
						FMultiply ::temp84 dz dz                                 ;@line 626
						FAdd ::temp83 ::temp83 ::temp84                          ;@line 626
						Assign lengthSquared ::temp83                            ;@line 626
						CompareLTE ::temp85 lengthSquared 0.000010               ;@line 627
						JumpF ::temp85 _label262                                 ;@line 627
						Return True                                              ;@line 628
						Jump _label262                                           ;@line 628
					_label262:
						FSubtract ::temp84 px ax                                 ;@line 630
						FMultiply ::temp83 ::temp84 dx                           ;@line 630
						FSubtract ::temp84 py ay                                 ;@line 630
						FMultiply ::temp84 ::temp84 dy                           ;@line 630
						FAdd ::temp83 ::temp83 ::temp84                          ;@line 630
						FSubtract ::temp84 pz az                                 ;@line 630
						FMultiply ::temp84 ::temp84 dz                           ;@line 630
						FAdd ::temp83 ::temp83 ::temp84                          ;@line 630
						FDivide ::temp84 ::temp83 lengthSquared                  ;@line 630
						Assign along ::temp84                                    ;@line 630
						CompareLT ::temp85 along 0.000000                        ;@line 631
						JumpF ::temp85 _label263                                 ;@line 631
						Assign along 0.000000                                    ;@line 632
						Jump _label264                                           ;@line 632
					_label263:
						CompareGT ::temp86 along 1.000000                        ;@line 633
						JumpF ::temp86 _label264                                 ;@line 633
						Assign along 1.000000                                    ;@line 634
						Jump _label264                                           ;@line 634
					_label264:
						FMultiply ::temp83 along dx                              ;@line 636
						FAdd ::temp84 ax ::temp83                                ;@line 636
						FSubtract ::temp83 px ::temp84                           ;@line 636
						Assign dx ::temp83                                       ;@line 636
						FMultiply ::temp84 along dy                              ;@line 637
						FAdd ::temp83 ay ::temp84                                ;@line 637
						FSubtract ::temp84 py ::temp83                           ;@line 637
						Assign dy ::temp84                                       ;@line 637
						FMultiply ::temp83 along dz                              ;@line 638
						FAdd ::temp84 az ::temp83                                ;@line 638
						FSubtract ::temp83 pz ::temp84                           ;@line 638
						Assign dz ::temp83                                       ;@line 638
						FMultiply ::temp84 dx dx                                 ;@line 639
						FMultiply ::temp83 dy dy                                 ;@line 639
						FAdd ::temp84 ::temp84 ::temp83                          ;@line 639
						FMultiply ::temp83 dz dz                                 ;@line 639
						FAdd ::temp84 ::temp84 ::temp83                          ;@line 639
						FMultiply ::temp83 radius radius                         ;@line 639
						CompareLTE ::temp86 ::temp84 ::temp83                    ;@line 639
						Return ::temp86                                          ;@line 639
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
						CallMethod Shutdown self ::NoneVar                       ;@line 78
					.endCode
				.endFunction
				.function ShotPreflight
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param target actor
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp94 Bool
						.local ::temp95 Float
						.local ::temp96 Float
						.local ::temp97 Bool
						.local yc Float
						.local ys Float
						.local pc Float
						.local ps Float
						.local lx Float
						.local ly Float
						.local wx Float
						.local wy Float
						.local wz Float
						.local poseDot Float
						.local targetDot Float
						.local clear Bool
						.local menuOpen Bool
						.local targetValid Bool
					.endLocalTable
					.code
						CallMethod SampleTarget self ::temp94 target expectedGeneration expectedToken  ;@line 700
						Not ::temp94 ::temp94                                    ;@line 700
						JumpF ::temp94 _label265                                 ;@line 700
						Return False                                             ;@line 701
						Jump _label265                                           ;@line 701
					_label265:
						CallStatic math Cos ::temp95 yaw                         ;@line 704
						Assign yc ::temp95                                       ;@line 704
						CallStatic math Sin ::temp95 yaw                         ;@line 705
						Assign ys ::temp95                                       ;@line 705
						CallStatic math Cos ::temp95 pitch                       ;@line 706
						Assign pc ::temp95                                       ;@line 706
						CallStatic math Sin ::temp95 pitch                       ;@line 707
						Assign ps ::temp95                                       ;@line 707
						FMultiply ::temp95 ys pc                                 ;@line 708
						Assign lx ::temp95                                       ;@line 708
						FNegate ::temp95 yc                                      ;@line 709
						FMultiply ::temp95 ::temp95 pc                           ;@line 709
						Assign ly ::temp95                                       ;@line 709
						ArrayGetElement ::temp95 rootWorldMatrix 0               ;@line 710
						FMultiply ::temp95 ::temp95 lx                           ;@line 710
						ArrayGetElement ::temp96 rootWorldMatrix 1               ;@line 710
						FMultiply ::temp96 ::temp96 ly                           ;@line 710
						FAdd ::temp95 ::temp95 ::temp96                          ;@line 710
						ArrayGetElement ::temp96 rootWorldMatrix 2               ;@line 710
						FMultiply ::temp96 ::temp96 ps                           ;@line 710
						FAdd ::temp95 ::temp95 ::temp96                          ;@line 710
						Assign wx ::temp95                                       ;@line 710
						ArrayGetElement ::temp96 rootWorldMatrix 3               ;@line 711
						FMultiply ::temp95 ::temp96 lx                           ;@line 711
						ArrayGetElement ::temp96 rootWorldMatrix 4               ;@line 711
						FMultiply ::temp96 ::temp96 ly                           ;@line 711
						FAdd ::temp95 ::temp95 ::temp96                          ;@line 711
						ArrayGetElement ::temp96 rootWorldMatrix 5               ;@line 711
						FMultiply ::temp96 ::temp96 ps                           ;@line 711
						FAdd ::temp95 ::temp95 ::temp96                          ;@line 711
						Assign wy ::temp95                                       ;@line 711
						ArrayGetElement ::temp96 rootWorldMatrix 6               ;@line 712
						FMultiply ::temp95 ::temp96 lx                           ;@line 712
						ArrayGetElement ::temp96 rootWorldMatrix 7               ;@line 712
						FMultiply ::temp96 ::temp96 ly                           ;@line 712
						FAdd ::temp95 ::temp95 ::temp96                          ;@line 712
						ArrayGetElement ::temp96 rootWorldMatrix 8               ;@line 712
						FMultiply ::temp96 ::temp96 ps                           ;@line 712
						FAdd ::temp95 ::temp95 ::temp96                          ;@line 712
						Assign wz ::temp95                                       ;@line 712
						ArrayGetElement ::temp96 muzzleWorldMatrix 1             ;@line 713
						FMultiply ::temp95 wx ::temp96                           ;@line 713
						ArrayGetElement ::temp96 muzzleWorldMatrix 4             ;@line 713
						FMultiply ::temp96 wy ::temp96                           ;@line 713
						FAdd ::temp95 ::temp95 ::temp96                          ;@line 713
						ArrayGetElement ::temp96 muzzleWorldMatrix 7             ;@line 713
						FMultiply ::temp96 wz ::temp96                           ;@line 713
						FAdd ::temp95 ::temp95 ::temp96                          ;@line 713
						Assign poseDot ::temp95                                  ;@line 713
						ArrayGetElement ::temp96 muzzleWorldMatrix 1             ;@line 714
						FMultiply ::temp95 aimX ::temp96                         ;@line 714
						ArrayGetElement ::temp96 muzzleWorldMatrix 4             ;@line 714
						FMultiply ::temp96 aimY ::temp96                         ;@line 714
						FAdd ::temp95 ::temp95 ::temp96                          ;@line 714
						ArrayGetElement ::temp96 muzzleWorldMatrix 7             ;@line 714
						FMultiply ::temp96 aimZ ::temp96                         ;@line 714
						FAdd ::temp95 ::temp95 ::temp96                          ;@line 714
						Assign targetDot ::temp95                                ;@line 714
						CallMethod Finite self ::temp94 poseDot 0.999950 1.002000  ;@line 715
						Not ::temp94 ::temp94                                    ;@line 715
						Cast ::temp94 ::temp94                                   ;@line 715
						JumpT ::temp94 _label266                                 ;@line 715
						CallMethod Finite self ::temp97 targetDot 0.999950 1.002000  ;@line 715
						Not ::temp97 ::temp97                                    ;@line 715
						Cast ::temp94 ::temp97                                   ;@line 715
					_label266:
						Cast ::temp94 ::temp94                                   ;@line 715
						JumpT ::temp94 _label267                                 ;@line 715
						CallMethod Current self ::temp97 expectedGeneration expectedToken  ;@line 715
						Not ::temp97 ::temp97                                    ;@line 715
						Cast ::temp94 ::temp97                                   ;@line 715
					_label267:
						JumpF ::temp94 _label268                                 ;@line 715
						Return False                                             ;@line 716
						Jump _label268                                           ;@line 716
					_label268:
						CallMethod PlayerClear self ::temp97 expectedGeneration expectedToken  ;@line 718
						Assign clear ::temp97                                    ;@line 718
						CallStatic utility IsInMenuMode ::temp94                 ;@line 719
						Assign menuOpen ::temp94                                 ;@line 719
						CallMethod ValidTarget self ::temp97 target expectedGeneration expectedToken  ;@line 720
						Assign targetValid ::temp97                              ;@line 720
						CallMethod Current self ::temp94 expectedGeneration expectedToken  ;@line 721
						Cast ::temp97 ::temp94                                   ;@line 721
						JumpF ::temp97 _label269                                 ;@line 721
						Cast ::temp97 clear                                      ;@line 721
					_label269:
						Cast ::temp97 ::temp97                                   ;@line 721
						JumpF ::temp97 _label270                                 ;@line 721
						Not ::temp94 menuOpen                                    ;@line 721
						Cast ::temp97 ::temp94                                   ;@line 721
					_label270:
						Cast ::temp94 ::temp97                                   ;@line 721
						JumpF ::temp94 _label271                                 ;@line 721
						Cast ::temp94 targetValid                                ;@line 721
					_label271:
						Return ::temp94                                          ;@line 721
					.endCode
				.endFunction
				.function QueueDeferredRecovery
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp22 Bool
						.local ::temp23 Bool
						.local queueGeneration Int
						.local loaded Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						Cast ::temp22 pinBusy                                    ;@line 310
						JumpT ::temp22 _label272                                 ;@line 310
						Cast ::temp22 sceneBusy                                  ;@line 310
					_label272:
						Cast ::temp22 ::temp22                                   ;@line 310
						JumpT ::temp22 _label273                                 ;@line 310
						Not ::temp23 recoveryRequested                           ;@line 310
						Cast ::temp22 ::temp23                                   ;@line 310
					_label273:
						Cast ::temp23 ::temp22                                   ;@line 310
						JumpT ::temp23 _label274                                 ;@line 310
						Cast ::temp23 destroyed                                  ;@line 310
					_label274:
						Cast ::temp22 ::temp23                                   ;@line 310
						JumpT ::temp22 _label275                                 ;@line 310
						Cast ::temp22 faulted                                    ;@line 310
					_label275:
						JumpF ::temp22 _label276                                 ;@line 310
						Return None                                              ;@line 311
						Jump _label276                                           ;@line 311
					_label276:
						Assign queueGeneration generation                        ;@line 313
						CallMethod Is3DLoaded self ::temp23                      ;@line 314
						Assign loaded ::temp23                                   ;@line 314
						CompareEQ ::temp22 generation queueGeneration            ;@line 315
						Not ::temp22 ::temp22                                    ;@line 315
						Cast ::temp23 ::temp22                                   ;@line 315
						JumpT ::temp23 _label277                                 ;@line 315
						Cast ::temp23 pinBusy                                    ;@line 315
					_label277:
						Cast ::temp22 ::temp23                                   ;@line 315
						JumpT ::temp22 _label278                                 ;@line 315
						Cast ::temp22 sceneBusy                                  ;@line 315
					_label278:
						Cast ::temp22 ::temp22                                   ;@line 315
						JumpT ::temp22 _label279                                 ;@line 315
						Not ::temp23 recoveryRequested                           ;@line 315
						Cast ::temp22 ::temp23                                   ;@line 315
					_label279:
						Cast ::temp23 ::temp22                                   ;@line 315
						JumpT ::temp23 _label280                                 ;@line 315
						Cast ::temp23 destroyed                                  ;@line 315
					_label280:
						Cast ::temp22 ::temp23                                   ;@line 315
						JumpT ::temp22 _label281                                 ;@line 315
						Cast ::temp22 faulted                                    ;@line 315
					_label281:
						JumpF ::temp22 _label282                                 ;@line 315
						Return None                                              ;@line 316
						Jump _label282                                           ;@line 316
					_label282:
						JumpF loaded _label283                                   ;@line 318
						CallMethod RegisterForSingleUpdate self ::NoneVar 0.200000  ;@line 319
						Jump _label283                                           ;@line 319
					_label283:
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
				.function PlayerClear
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp87 actor
						.local ::temp88 Bool
						.local ::temp89 Bool
						.local ::temp90 Float
						.local ::temp91 Float
						.local player actor
						.local playerLoaded Bool
						.local px Float
						.local py Float
						.local pz Float
						.local height Float
						.local radius Float
						.local bx Float
						.local by Float
						.local bz Float
						.local boreHorizontal Float
						.local totalTime Float
						.local ax Float
						.local ay Float
						.local az Float
						.local step Int
						.local t Float
						.local ex Float
						.local ey Float
						.local ez Float
						.local sample Int
						.local ::temp92 Bool
						.local ::temp93 Int
					.endLocalTable
					.code
						CallStatic game GetPlayer ::temp87                       ;@line 643
						Assign player ::temp87                                   ;@line 643
						CallMethod Current self ::temp88 expectedGeneration expectedToken  ;@line 644
						Not ::temp88 ::temp88                                    ;@line 644
						Cast ::temp88 ::temp88                                   ;@line 644
						JumpT ::temp88 _label284                                 ;@line 644
						Cast ::temp87 None                                       ;@line 644
						CompareEQ ::temp89 player ::temp87                       ;@line 644
						Cast ::temp88 ::temp89                                   ;@line 644
					_label284:
						JumpF ::temp88 _label285                                 ;@line 644
						Return False                                             ;@line 645
						Jump _label285                                           ;@line 645
					_label285:
						CallMethod Is3DLoaded player ::temp89                    ;@line 647
						Assign playerLoaded ::temp89                             ;@line 647
						CallMethod GetPositionX player ::temp90                  ;@line 648
						Assign px ::temp90                                       ;@line 648
						CallMethod GetPositionY player ::temp90                  ;@line 649
						Assign py ::temp90                                       ;@line 649
						CallMethod GetPositionZ player ::temp90                  ;@line 650
						Assign pz ::temp90                                       ;@line 650
						CallMethod GetHeight player ::temp90                     ;@line 651
						Assign height ::temp90                                   ;@line 651
						CallMethod Current self ::temp88 expectedGeneration expectedToken  ;@line 652
						Not ::temp89 ::temp88                                    ;@line 652
						Cast ::temp89 ::temp89                                   ;@line 652
						JumpT ::temp89 _label286                                 ;@line 652
						Not ::temp88 playerLoaded                                ;@line 652
						Cast ::temp89 ::temp88                                   ;@line 652
					_label286:
						Cast ::temp89 ::temp89                                   ;@line 652
						JumpT ::temp89 _label287                                 ;@line 652
						CallMethod Finite self ::temp88 px -1000000.000000 1000000.000000  ;@line 652
						Not ::temp88 ::temp88                                    ;@line 652
						Cast ::temp89 ::temp88                                   ;@line 652
					_label287:
						Cast ::temp89 ::temp89                                   ;@line 652
						JumpT ::temp89 _label288                                 ;@line 652
						CallMethod Finite self ::temp88 py -1000000.000000 1000000.000000  ;@line 652
						Not ::temp88 ::temp88                                    ;@line 652
						Cast ::temp89 ::temp88                                   ;@line 652
					_label288:
						Cast ::temp89 ::temp89                                   ;@line 652
						JumpT ::temp89 _label289                                 ;@line 652
						CallMethod Finite self ::temp88 pz -1000000.000000 1000000.000000  ;@line 652
						Not ::temp88 ::temp88                                    ;@line 652
						Cast ::temp89 ::temp88                                   ;@line 652
					_label289:
						Cast ::temp89 ::temp89                                   ;@line 652
						JumpT ::temp89 _label290                                 ;@line 652
						CallMethod Finite self ::temp88 height 1.000000 512.000000  ;@line 652
						Not ::temp88 ::temp88                                    ;@line 652
						Cast ::temp89 ::temp88                                   ;@line 652
					_label290:
						JumpF ::temp89 _label291                                 ;@line 652
						Return False                                             ;@line 653
						Jump _label291                                           ;@line 653
					_label291:
						CompareLT ::temp88 height 128.000000                     ;@line 655
						JumpF ::temp88 _label292                                 ;@line 655
						Assign height 128.000000                                 ;@line 656
						Jump _label292                                           ;@line 656
					_label292:
						FAdd ::temp90 height 64.000000                           ;@line 658
						Assign height ::temp90                                   ;@line 658
						FDivide ::temp90 height 8.000000                         ;@line 663
						FAdd ::temp90 80.000000 ::temp90                         ;@line 663
						Assign radius ::temp90                                   ;@line 663
						ArrayGetElement ::temp90 muzzleWorldMatrix 1             ;@line 664
						Assign bx ::temp90                                       ;@line 664
						ArrayGetElement ::temp90 muzzleWorldMatrix 4             ;@line 665
						Assign by ::temp90                                       ;@line 665
						ArrayGetElement ::temp90 muzzleWorldMatrix 7             ;@line 666
						Assign bz ::temp90                                       ;@line 666
						FMultiply ::temp90 bx bx                                 ;@line 667
						FMultiply ::temp91 by by                                 ;@line 667
						FAdd ::temp90 ::temp90 ::temp91                          ;@line 667
						CallStatic math Sqrt ::temp91 ::temp90                   ;@line 667
						Assign boreHorizontal ::temp91                           ;@line 667
						CompareLT ::temp89 boreHorizontal 0.010000               ;@line 668
						JumpF ::temp89 _label293                                 ;@line 668
						Return False                                             ;@line 669
						Jump _label293                                           ;@line 669
					_label293:
						FMultiply ::temp90 ::ProjectileSpeed_var boreHorizontal  ;@line 671
						FDivide ::temp91 targetHorizontal ::temp90               ;@line 671
						Assign totalTime ::temp91                                ;@line 671
						CallMethod Finite self ::temp88 totalTime 0.000010 30.000000  ;@line 672
						Not ::temp89 ::temp88                                    ;@line 672
						JumpF ::temp89 _label294                                 ;@line 672
						Return False                                             ;@line 673
						Jump _label294                                           ;@line 673
					_label294:
						ArrayGetElement ::temp90 muzzlePosition 0                ;@line 675
						Assign ax ::temp90                                       ;@line 675
						ArrayGetElement ::temp91 muzzlePosition 1                ;@line 676
						Assign ay ::temp91                                       ;@line 676
						ArrayGetElement ::temp90 muzzlePosition 2                ;@line 677
						Assign az ::temp90                                       ;@line 677
						Assign step 1                                            ;@line 678
					_label299:
						CompareLTE ::temp88 step 8                               ;@line 679
						JumpF ::temp88 _label295                                 ;@line 679
						Cast ::temp91 step                                       ;@line 680
						FMultiply ::temp90 totalTime ::temp91                    ;@line 680
						FDivide ::temp91 ::temp90 8.000000                       ;@line 680
						Assign t ::temp91                                        ;@line 680
						ArrayGetElement ::temp90 muzzlePosition 0                ;@line 681
						FMultiply ::temp91 bx ::ProjectileSpeed_var              ;@line 681
						FMultiply ::temp91 ::temp91 t                            ;@line 681
						FAdd ::temp90 ::temp90 ::temp91                          ;@line 681
						Assign ex ::temp90                                       ;@line 681
						ArrayGetElement ::temp91 muzzlePosition 1                ;@line 682
						FMultiply ::temp90 by ::ProjectileSpeed_var              ;@line 682
						FMultiply ::temp90 ::temp90 t                            ;@line 682
						FAdd ::temp91 ::temp91 ::temp90                          ;@line 682
						Assign ey ::temp91                                       ;@line 682
						ArrayGetElement ::temp90 muzzlePosition 2                ;@line 683
						FMultiply ::temp91 bz ::ProjectileSpeed_var              ;@line 683
						FMultiply ::temp91 ::temp91 t                            ;@line 683
						FAdd ::temp90 ::temp90 ::temp91                          ;@line 683
						FMultiply ::temp91 0.500000 ::ProjectileGravity_var      ;@line 683
						FMultiply ::temp91 ::temp91 t                            ;@line 683
						FMultiply ::temp91 ::temp91 t                            ;@line 683
						FSubtract ::temp90 ::temp90 ::temp91                     ;@line 683
						Assign ez ::temp90                                       ;@line 683
						Assign sample 0                                          ;@line 684
					_label298:
						CompareLTE ::temp89 sample 4                             ;@line 685
						JumpF ::temp89 _label296                                 ;@line 685
						Cast ::temp91 sample                                     ;@line 686
						FMultiply ::temp90 height ::temp91                       ;@line 686
						FDivide ::temp91 ::temp90 4.000000                       ;@line 686
						FAdd ::temp90 pz ::temp91                                ;@line 686
						CallMethod PointNearSegment self ::temp92 px py ::temp90 ax ay az ex ey ez radius  ;@line 686
						JumpF ::temp92 _label297                                 ;@line 686
						Return False                                             ;@line 687
						Jump _label297                                           ;@line 687
					_label297:
						IAdd ::temp93 sample 1                                   ;@line 689
						Assign sample ::temp93                                   ;@line 689
						Jump _label298                                           ;@line 689
					_label296:
						Assign ax ex                                             ;@line 691
						Assign ay ey                                             ;@line 692
						Assign az ez                                             ;@line 693
						IAdd ::temp93 step 1                                     ;@line 694
						Assign step ::temp93                                     ;@line 694
						Jump _label299                                           ;@line 694
					_label295:
						CallMethod Current self ::temp92 expectedGeneration expectedToken  ;@line 696
						Return ::temp92                                          ;@line 696
					.endCode
				.endFunction
			.endState
		.endStateTable
	.endObject
.endObjectTable
