.info
	.source "AstraAsedioGuard.psc"
	.modifyTime 1791759002 ;Sun Oct 11 19:50:02 2026 Local
	.compileTime 1791759044 ;Sun Oct 11 19:50:44 2026 Local
	.user "AstraAsedio"
	.computer "Build"
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
			.variable timingRevision Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable ::TurnRate_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 30.000000
			.endVariable
			.variable phaseAt Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::VisualBoltNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "VIROTE_VISUAL"
			.endVariable
			.variable v23Wanted Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable v27WarnedRefs Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable yaw Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable matricesReady Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable muzzleWorldMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::PitchMax_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 45.000000
			.endVariable
			.variable ::ReleaseSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.066667
			.endVariable
			.variable pitch Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable guardPoseStarted Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable v23PlacementVersion Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable rootWorldMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::AllowPlayerTakeover_var Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable playerLease Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable ::YawNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "CTRL_GIRO_360"
			.endVariable
			.variable stationRetired Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ownedGuard actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable playerReady Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable fireFaction Faction
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable running Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable playerRestored Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::ShotSound_var sound
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable v23Generation Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable recoveryRequested Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable v23PumpOwner Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable ::Puesto_var ObjectReference
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable guardPoseFireAt Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable v23LastStatus Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue -99
			.endVariable
			.variable ::ShotAmmo_var ammo
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable nextShotAt Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable guardPoseFiring Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::CadenceSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 2.500000
			.endVariable
			.variable rootPosition Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::ProjectileSpeed_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 5400.000000
			.endVariable
			.variable ::Launcher_var weapon
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable pitchMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable desiredYaw Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable v23Serial Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable playerReserved Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable sceneBusy Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable recovering Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::YawHalfSector_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 60.000000
			.endVariable
			.variable visualTarget actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable yawMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::TargetHeight_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 60.000000
			.endVariable
			.variable lastTick Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable yawBase Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable desiredPitch Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::FireSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.200000
			.endVariable
			.variable pinBusy Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable exitIdle Idle
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable serial Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable holdIdle Idle
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable updating Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable shotTarget actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable pitchBase Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable phase Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable token Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1
			.endVariable
			.variable ::YawCenter_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::ProjectileGravity_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 240.345001
			.endVariable
			.variable v27Faults Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable targetHorizontal Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable faulted Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable poseFaction Faction
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::ResetSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.800000
			.endVariable
			.variable muzzlePosition Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable v28RetryWaited Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable destroyed Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable playerSerial Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable ::Artillero_var actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable aimZ Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::MuzzleNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "ProjectileNode"
			.endVariable
			.variable generation Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable aimX Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::PitchMin_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue -20.000000
			.endVariable
			.variable ::Standby_var ObjectReference
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::PitchNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "CTRL_ELEVACION"
			.endVariable
			.variable aimY Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1.000000
			.endVariable
			.variable v23Token Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable visualScanAt Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable v23Warned Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
		.endVariableTable
		.propertyTable
			.property YawNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::YawNode_var
			.endProperty
			.property YawCenter Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::YawCenter_var
			.endProperty
			.property YawHalfSector Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::YawHalfSector_var
			.endProperty
			.property PitchNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchNode_var
			.endProperty
			.property ResetSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ResetSeconds_var
			.endProperty
			.property ShotAmmo ammo auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ShotAmmo_var
			.endProperty
			.property FireSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::FireSeconds_var
			.endProperty
			.property Artillero actor auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Artillero_var
			.endProperty
			.property Puesto ObjectReference auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Puesto_var
			.endProperty
			.property ProjectileSpeed Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ProjectileSpeed_var
			.endProperty
			.property TargetHeight Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::TargetHeight_var
			.endProperty
			.property CadenceSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::CadenceSeconds_var
			.endProperty
			.property Standby ObjectReference auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Standby_var
			.endProperty
			.property AllowPlayerTakeover Bool auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::AllowPlayerTakeover_var
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
			.property MuzzleNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::MuzzleNode_var
			.endProperty
			.property ShotSound sound auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ShotSound_var
			.endProperty
			.property ReleaseSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ReleaseSeconds_var
			.endProperty
			.property TurnRate Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::TurnRate_var
			.endProperty
			.property ProjectileGravity Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ProjectileGravity_var
			.endProperty
			.property PitchMax Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchMax_var
			.endProperty
			.property VisualBoltNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::VisualBoltNode_var
			.endProperty
		.endPropertyTable
		.stateTable
			.state 
				.function ReservePlayerLease
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Int
					.paramTable
					.endParamTable
					.localTable
					.endLocalTable
					.code
						Return -1                                                ;@line 182
					.endCode
				.endFunction
				.function ReleaseOwnedGuard
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
					.endLocalTable
					.code
						Return None                                              ;@line 273
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
						.local ::temp13 Bool
						.local ::temp14 Bool
					.endLocalTable
					.code
						CompareEQ ::temp13 value value                           ;@line 202
						Cast ::temp13 ::temp13                                   ;@line 202
						JumpF ::temp13 _label0                                   ;@line 202
						CompareGTE ::temp14 value minimum                        ;@line 202
						Cast ::temp13 ::temp14                                   ;@line 202
					_label0:
						Cast ::temp13 ::temp13                                   ;@line 202
						JumpF ::temp13 _label1                                   ;@line 202
						CompareLTE ::temp14 value maximum                        ;@line 202
						Cast ::temp13 ::temp14                                   ;@line 202
					_label1:
						Return ::temp13                                          ;@line 202
					.endCode
				.endFunction
				.function ReleasePlayerLease
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param lease Int
					.endParamTable
					.localTable
						.local ::temp12 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod PlayerLeaseCurrent self ::temp12 lease        ;@line 190
						Not ::temp12 ::temp12                                    ;@line 190
						JumpF ::temp12 _label2                                   ;@line 190
						Return False                                             ;@line 191
						Jump _label2                                             ;@line 191
					_label2:
						CallMethod InvalidatePlayerLease self ::NoneVar          ;@line 193
						CallMethod Shutdown self ::NoneVar                       ;@line 194
						CallMethod BeginRecovery self ::NoneVar                  ;@line 197
						Return True                                              ;@line 198
					.endCode
				.endFunction
				.function PreparePlayerLease
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param lease Int
					.endParamTable
					.localTable
					.endLocalTable
					.code
						Return False                                             ;@line 186
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
					.endLocalTable
					.code
						Return None                                              ;@line 613
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
						.local ::temp85 Bool
						.local ::temp86 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod Current self ::temp85 expectedGeneration expectedToken  ;@line 617
						Not ::temp85 ::temp85                                    ;@line 617
						Cast ::temp85 ::temp85                                   ;@line 617
						JumpT ::temp85 _label3                                   ;@line 617
						CompareEQ ::temp86 phase 0                               ;@line 617
						Cast ::temp85 ::temp86                                   ;@line 617
					_label3:
						JumpF ::temp85 _label4                                   ;@line 617
						Return None                                              ;@line 618
						Jump _label4                                             ;@line 618
					_label4:
						CallMethod SetGuardFirePose self ::temp86 False expectedGeneration expectedToken  ;@line 620
						CallMethod Current self ::temp85 expectedGeneration expectedToken  ;@line 621
						JumpF ::temp85 _label5                                   ;@line 621
						CallMethod StartReset self ::NoneVar expectedGeneration expectedToken  ;@line 622
						Jump _label5                                             ;@line 622
					_label5:
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
						.local ::temp82 Bool
						.local ::temp83 Bool
						.local ::temp84 Float
						.local now Float
						.local bodyStarted Bool
						.local cadence Float
						.local started Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod Current self ::temp82 expectedGeneration expectedToken  ;@line 585
						Not ::temp82 ::temp82                                    ;@line 585
						Cast ::temp82 ::temp82                                   ;@line 585
						JumpT ::temp82 _label6                                   ;@line 585
						CompareEQ ::temp83 phase 0                               ;@line 585
						Not ::temp83 ::temp83                                    ;@line 585
						Cast ::temp82 ::temp83                                   ;@line 585
					_label6:
						JumpF ::temp82 _label7                                   ;@line 585
						Return None                                              ;@line 586
						Jump _label7                                             ;@line 586
					_label7:
						CallStatic utility GetCurrentRealTime ::temp84           ;@line 588
						Assign now ::temp84                                      ;@line 588
						CallMethod Current self ::temp83 expectedGeneration expectedToken  ;@line 589
						Not ::temp82 ::temp83                                    ;@line 589
						Cast ::temp82 ::temp82                                   ;@line 589
						JumpT ::temp82 _label8                                   ;@line 589
						CompareEQ ::temp83 phase 0                               ;@line 589
						Not ::temp83 ::temp83                                    ;@line 589
						Cast ::temp82 ::temp83                                   ;@line 589
					_label8:
						Cast ::temp82 ::temp82                                   ;@line 589
						JumpT ::temp82 _label9                                   ;@line 589
						CallMethod Finite self ::temp83 now 0.000000 1000000000.000000  ;@line 589
						Not ::temp83 ::temp83                                    ;@line 589
						Cast ::temp82 ::temp83                                   ;@line 589
					_label9:
						Cast ::temp82 ::temp82                                   ;@line 589
						JumpT ::temp82 _label10                                  ;@line 589
						CompareLT ::temp83 now nextShotAt                        ;@line 589
						Cast ::temp82 ::temp83                                   ;@line 589
					_label10:
						JumpF ::temp82 _label11                                  ;@line 589
						Return None                                              ;@line 590
						Jump _label11                                            ;@line 590
					_label11:
						CallMethod SetGuardFirePose self ::temp83 True expectedGeneration expectedToken  ;@line 592
						Assign bodyStarted ::temp83                              ;@line 592
						CallMethod Current self ::temp82 expectedGeneration expectedToken  ;@line 593
						Not ::temp83 ::temp82                                    ;@line 593
						Cast ::temp83 ::temp83                                   ;@line 593
						JumpT ::temp83 _label12                                  ;@line 593
						Not ::temp82 bodyStarted                                 ;@line 593
						Cast ::temp83 ::temp82                                   ;@line 593
					_label12:
						JumpF ::temp83 _label13                                  ;@line 593
						Return None                                              ;@line 594
						Jump _label13                                            ;@line 594
					_label13:
						Assign guardPoseFireAt now                               ;@line 596
						Assign phase 1                                           ;@line 597
						Assign phaseAt now                                       ;@line 598
						Assign shotTarget target                                 ;@line 599
						CallMethod SafeCadenceSeconds self ::temp84              ;@line 600
						Assign cadence ::temp84                                  ;@line 600
						FAdd ::temp84 now cadence                                ;@line 601
						Assign nextShotAt ::temp84                               ;@line 601
						CallMethod PlaySceneAnimation self ::temp82 "Fire" expectedGeneration expectedToken  ;@line 602
						Assign started ::temp82                                  ;@line 602
						CallMethod Current self ::temp83 expectedGeneration expectedToken  ;@line 603
						Not ::temp82 ::temp83                                    ;@line 603
						Cast ::temp82 ::temp82                                   ;@line 603
						JumpT ::temp82 _label14                                  ;@line 603
						CompareEQ ::temp83 phase 1                               ;@line 603
						Not ::temp83 ::temp83                                    ;@line 603
						Cast ::temp82 ::temp83                                   ;@line 603
					_label14:
						Cast ::temp82 ::temp82                                   ;@line 603
						JumpT ::temp82 _label15                                  ;@line 603
						CompareEQ ::temp83 shotTarget target                     ;@line 603
						Not ::temp83 ::temp83                                    ;@line 603
						Cast ::temp82 ::temp83                                   ;@line 603
					_label15:
						JumpF ::temp82 _label16                                  ;@line 603
						Return None                                              ;@line 604
						Jump _label16                                            ;@line 604
					_label16:
						Not ::temp83 started                                     ;@line 606
						JumpF ::temp83 _label17                                  ;@line 606
						CallMethod AbortShot self ::NoneVar expectedGeneration expectedToken  ;@line 607
						Jump _label17                                            ;@line 607
					_label17:
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
						CallMethod BlockActivation self ::NoneVar True           ;@line 109
						CallMethod StartV23 self ::NoneVar                       ;@line 110
					.endCode
				.endFunction
				.function FinishPumpV23
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param expected Int
						.param delay Float
					.endParamTable
					.localTable
						.local ::temp162 Bool
						.local ::temp163 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CompareEQ ::temp162 v23PumpOwner expected                ;@line 1060
						Not ::temp162 ::temp162                                  ;@line 1060
						JumpF ::temp162 _label18                                 ;@line 1060
						Return None                                              ;@line 1061
						Jump _label18                                            ;@line 1061
					_label18:
						Assign v23PumpOwner 0                                    ;@line 1063
						CompareGT ::temp162 delay 0.000000                       ;@line 1064
						Cast ::temp162 ::temp162                                 ;@line 1064
						JumpF ::temp162 _label19                                 ;@line 1064
						CallMethod V23Current self ::temp163 expected            ;@line 1064
						Cast ::temp162 ::temp163                                 ;@line 1064
					_label19:
						JumpF ::temp162 _label20                                 ;@line 1064
						CallMethod RegisterForSingleUpdate self ::NoneVar delay  ;@line 1065
						Jump _label20                                            ;@line 1065
					_label20:
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
					.endLocalTable
					.code
						Return None                                              ;@line 317
					.endCode
				.endFunction
				.function PlayerLeaseCurrent
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param lease Int
					.endParamTable
					.localTable
						.local ::temp7 Bool
						.local ::temp8 Bool
					.endLocalTable
					.code
						Cast ::temp7 ::AllowPlayerTakeover_var                   ;@line 162
						JumpF ::temp7 _label21                                   ;@line 162
						Not ::temp7 stationRetired                               ;@line 162
						Cast ::temp7 ::temp7                                     ;@line 162
					_label21:
						Cast ::temp7 ::temp7                                     ;@line 162
						JumpF ::temp7 _label22                                   ;@line 162
						Not ::temp8 destroyed                                    ;@line 162
						Cast ::temp7 ::temp8                                     ;@line 162
					_label22:
						Cast ::temp8 ::temp7                                     ;@line 162
						JumpF ::temp8 _label23                                   ;@line 162
						Cast ::temp8 playerReserved                              ;@line 162
					_label23:
						Cast ::temp8 ::temp8                                     ;@line 162
						JumpF ::temp8 _label24                                   ;@line 162
						CompareGT ::temp7 lease 0                                ;@line 162
						Cast ::temp8 ::temp7                                     ;@line 162
					_label24:
						Cast ::temp8 ::temp8                                     ;@line 162
						JumpF ::temp8 _label25                                   ;@line 162
						CompareEQ ::temp7 playerLease lease                      ;@line 162
						Cast ::temp8 ::temp7                                     ;@line 162
					_label25:
						Return ::temp8                                           ;@line 162
					.endCode
				.endFunction
				.function StationSceneAvailable
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
					.localTable
						.local ::temp9 Bool
						.local ::temp10 Int
						.local ::temp11 ObjectReference
					.endLocalTable
					.code
						Not ::temp9 ::AllowPlayerTakeover_var                    ;@line 166
						JumpF ::temp9 _label26                                   ;@line 166
						Return True                                              ;@line 167
						Jump _label26                                            ;@line 167
					_label26:
						CallStatic skse GetPluginVersion ::temp10 "AstraSight"   ;@line 172
						CompareLT ::temp9 ::temp10 50659328                      ;@line 172
						JumpF ::temp9 _label27                                   ;@line 172
						Return True                                              ;@line 173
						Jump _label27                                            ;@line 173
					_label27:
						Cast ::temp11 self                                       ;@line 177
						CallStatic astrasightnative IsEffectsQuiescent ::temp9 ::temp11 0  ;@line 177
						Return ::temp9                                           ;@line 177
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
					.endLocalTable
					.code
						Return None                                              ;@line 312
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
					.endLocalTable
					.code
						Return False                                             ;@line 307
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
						.local ::temp87 Float
						.local ::temp88 Bool
						.local now Float
						.local started Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallStatic utility GetCurrentRealTime ::temp87           ;@line 627
						Assign now ::temp87                                      ;@line 627
						CallMethod Current self ::temp88 expectedGeneration expectedToken  ;@line 628
						Not ::temp88 ::temp88                                    ;@line 628
						JumpF ::temp88 _label28                                  ;@line 628
						Return None                                              ;@line 629
						Jump _label28                                            ;@line 629
					_label28:
						Assign phase 3                                           ;@line 631
						Assign phaseAt now                                       ;@line 632
						CallMethod PlaySceneAnimation self ::temp88 "Reset" expectedGeneration expectedToken  ;@line 633
						Assign started ::temp88                                  ;@line 633
						CallMethod Current self ::temp88 expectedGeneration expectedToken  ;@line 634
						Not ::temp88 ::temp88                                    ;@line 634
						JumpF ::temp88 _label29                                  ;@line 634
						Return None                                              ;@line 635
						Jump _label29                                            ;@line 635
					_label29:
						Not ::temp88 started                                     ;@line 637
						JumpF ::temp88 _label30                                  ;@line 637
						Assign faulted True                                      ;@line 638
						CallMethod Shutdown self ::NoneVar                       ;@line 639
						Jump _label30                                            ;@line 639
					_label30:
					.endCode
				.endFunction
				.function MigrateV23
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param actorRef actor
						.param expected Int
					.endParamTable
					.localTable
						.local ::temp135 Bool
						.local ::temp136 actor
						.local ::temp137 Bool
						.local ::temp138 ObjectReference
						.local ::temp139 Float
						.local ::temp140 Float
						.local ::NoneVar None
						.local ::temp145 Idle
						.local ::temp146 String
						.local ::temp147 String
						.local angle Float
						.local px Float
						.local py Float
						.local pz Float
						.local index Int
						.local ::temp141 Bool
						.local ::temp142 Int
						.local ::temp143 form
						.local ::temp144 Faction
						.local privateFlag Faction
						.local previousExit Idle
					.endLocalTable
					.code
						CallMethod V23Current self ::temp135 expected            ;@line 840
						Not ::temp135 ::temp135                                  ;@line 840
						Cast ::temp135 ::temp135                                 ;@line 840
						JumpT ::temp135 _label31                                 ;@line 840
						Cast ::temp136 None                                      ;@line 840
						CompareEQ ::temp137 actorRef ::temp136                   ;@line 840
						Cast ::temp135 ::temp137                                 ;@line 840
					_label31:
						Cast ::temp135 ::temp135                                 ;@line 840
						JumpT ::temp135 _label32                                 ;@line 840
						Cast ::temp138 None                                      ;@line 840
						CompareEQ ::temp137 ::Puesto_var ::temp138               ;@line 840
						Cast ::temp135 ::temp137                                 ;@line 840
					_label32:
						JumpF ::temp135 _label33                                 ;@line 840
						Return False                                             ;@line 841
						Jump _label33                                            ;@line 841
					_label33:
						CallMethod Is3DLoaded self ::temp137                     ;@line 843
						Not ::temp135 ::temp137                                  ;@line 843
						Cast ::temp135 ::temp135                                 ;@line 843
						JumpT ::temp135 _label34                                 ;@line 843
						CallMethod Is3DLoaded actorRef ::temp137                 ;@line 843
						Not ::temp137 ::temp137                                  ;@line 843
						Cast ::temp135 ::temp137                                 ;@line 843
					_label34:
						Cast ::temp135 ::temp135                                 ;@line 843
						JumpT ::temp135 _label35                                 ;@line 843
						CallMethod IsDead actorRef ::temp137                     ;@line 843
						Cast ::temp135 ::temp137                                 ;@line 843
					_label35:
						JumpF ::temp135 _label36                                 ;@line 843
						Return False                                             ;@line 844
						Jump _label36                                            ;@line 844
					_label36:
						CallMethod GetAngleZ self ::temp139                      ;@line 847
						Assign angle ::temp139                                   ;@line 847
						CallMethod GetPositionX self ::temp139                   ;@line 848
						CallStatic math Sin ::temp140 angle                      ;@line 848
						FMultiply ::temp140 151.000000 ::temp140                 ;@line 848
						FSubtract ::temp139 ::temp139 ::temp140                  ;@line 848
						Assign px ::temp139                                      ;@line 848
						CallMethod GetPositionY self ::temp140                   ;@line 849
						CallStatic math Cos ::temp139 angle                      ;@line 849
						FMultiply ::temp139 151.000000 ::temp139                 ;@line 849
						FAdd ::temp140 ::temp140 ::temp139                       ;@line 849
						Assign py ::temp140                                      ;@line 849
						CallMethod GetPositionZ self ::temp139                   ;@line 850
						Assign pz ::temp139                                      ;@line 850
						CallMethod V23Current self ::temp137 expected            ;@line 851
						Not ::temp135 ::temp137                                  ;@line 851
						JumpF ::temp135 _label37                                 ;@line 851
						Return False                                             ;@line 852
						Jump _label37                                            ;@line 852
					_label37:
						CallMethod SetPosition ::Puesto_var ::NoneVar px py pz   ;@line 854
						CallMethod V23Current self ::temp137 expected            ;@line 855
						Not ::temp135 ::temp137                                  ;@line 855
						JumpF ::temp135 _label38                                 ;@line 855
						Return False                                             ;@line 856
						Jump _label38                                            ;@line 856
					_label38:
						FAdd ::temp140 angle 180.000000                          ;@line 858
						CallMethod SetAngle ::Puesto_var ::NoneVar 0.000000 0.000000 ::temp140  ;@line 858
						Assign index 0                                           ;@line 859
					_label46:
						CompareLT ::temp137 index 6                              ;@line 860
						Cast ::temp137 ::temp137                                 ;@line 860
						JumpF ::temp137 _label39                                 ;@line 860
						CallMethod V23Current self ::temp135 expected            ;@line 860
						Cast ::temp137 ::temp135                                 ;@line 860
					_label39:
						JumpF ::temp137 _label40                                 ;@line 860
						CompareEQ ::temp135 index 0                              ;@line 861
						Cast ::temp135 ::temp135                                 ;@line 861
						JumpT ::temp135 _label41                                 ;@line 861
						CompareEQ ::temp141 index 1                              ;@line 861
						Cast ::temp135 ::temp141                                 ;@line 861
					_label41:
						Cast ::temp135 ::temp135                                 ;@line 861
						JumpT ::temp135 _label42                                 ;@line 861
						CompareEQ ::temp141 index 4                              ;@line 861
						Cast ::temp135 ::temp141                                 ;@line 861
					_label42:
						Cast ::temp135 ::temp135                                 ;@line 861
						JumpT ::temp135 _label43                                 ;@line 861
						CompareEQ ::temp141 index 5                              ;@line 861
						Cast ::temp135 ::temp141                                 ;@line 861
					_label43:
						JumpF ::temp135 _label44                                 ;@line 861
						IAdd ::temp142 2048 index                                ;@line 862
						CallStatic game GetFormFromFile ::temp143 ::temp142 "AstraAsedio_GuardAnim.esp"  ;@line 862
						Cast ::temp144 ::temp143                                 ;@line 862
						Assign privateFlag ::temp144                             ;@line 862
						Cast ::temp144 None                                      ;@line 863
						CompareEQ ::temp141 privateFlag ::temp144                ;@line 863
						Not ::temp141 ::temp141                                  ;@line 863
						JumpF ::temp141 _label45                                 ;@line 863
						CallMethod RemoveFromFaction actorRef ::NoneVar privateFlag  ;@line 864
						Jump _label45                                            ;@line 864
					_label45:
						Jump _label44                                            ;@line 864
					_label44:
						IAdd ::temp142 index 1                                   ;@line 867
						Assign index ::temp142                                   ;@line 867
						Jump _label46                                            ;@line 867
					_label40:
						CallMethod V23Current self ::temp141 expected            ;@line 869
						Not ::temp135 ::temp141                                  ;@line 869
						JumpF ::temp135 _label47                                 ;@line 869
						Return False                                             ;@line 870
						Jump _label47                                            ;@line 870
					_label47:
						CallMethod SetDontMove actorRef ::NoneVar False          ;@line 872
						CallMethod V23Current self ::temp137 expected            ;@line 873
						Not ::temp141 ::temp137                                  ;@line 873
						JumpF ::temp141 _label48                                 ;@line 873
						Return False                                             ;@line 874
						Jump _label48                                            ;@line 874
					_label48:
						CallMethod SetHeadTracking actorRef ::NoneVar True       ;@line 876
						CallMethod V23Current self ::temp135 expected            ;@line 877
						Not ::temp137 ::temp135                                  ;@line 877
						JumpF ::temp137 _label49                                 ;@line 877
						Return False                                             ;@line 878
						Jump _label49                                            ;@line 878
					_label49:
						Cast ::temp138 actorRef                                  ;@line 881
						CallStatic debug SendAnimationEvent ::NoneVar ::temp138 "IdleForceDefaultState"  ;@line 881
						CallMethod V23Current self ::temp141 expected            ;@line 882
						Not ::temp135 ::temp141                                  ;@line 882
						JumpF ::temp135 _label50                                 ;@line 882
						Return False                                             ;@line 883
						Jump _label50                                            ;@line 883
					_label50:
						CallStatic game GetFormFromFile ::temp143 2051 "AstraAsedio_GuardAnim.esp"  ;@line 885
						Cast ::temp145 ::temp143                                 ;@line 885
						Assign previousExit ::temp145                            ;@line 885
						Cast ::temp145 None                                      ;@line 886
						CompareEQ ::temp137 previousExit ::temp145               ;@line 886
						Not ::temp137 ::temp137                                  ;@line 886
						JumpF ::temp137 _label51                                 ;@line 886
						CallMethod PlayIdle actorRef ::temp141 previousExit      ;@line 887
						Jump _label51                                            ;@line 887
					_label51:
						CallMethod V23Current self ::temp135 expected            ;@line 889
						Not ::temp141 ::temp135                                  ;@line 889
						JumpF ::temp141 _label52                                 ;@line 889
						Return False                                             ;@line 890
						Jump _label52                                            ;@line 890
					_label52:
						CallMethod SetPosition actorRef ::NoneVar px py pz       ;@line 892
						CallMethod V23Current self ::temp137 expected            ;@line 893
						Not ::temp135 ::temp137                                  ;@line 893
						JumpF ::temp135 _label53                                 ;@line 893
						Return False                                             ;@line 894
						Jump _label53                                            ;@line 894
					_label53:
						FAdd ::temp139 angle 180.000000                          ;@line 896
						CallMethod SetAngle actorRef ::NoneVar 0.000000 0.000000 ::temp139  ;@line 896
						CallMethod V23Current self ::temp141 expected            ;@line 897
						Not ::temp137 ::temp141                                  ;@line 897
						JumpF ::temp137 _label54                                 ;@line 897
						Return False                                             ;@line 898
						Jump _label54                                            ;@line 898
					_label54:
						CallMethod StopCombat actorRef ::NoneVar                 ;@line 901
						CallMethod V23Current self ::temp135 expected            ;@line 902
						Not ::temp141 ::temp135                                  ;@line 902
						JumpF ::temp141 _label55                                 ;@line 902
						Return False                                             ;@line 903
						Jump _label55                                            ;@line 903
					_label55:
						CallMethod SheatheWeapon actorRef ::NoneVar              ;@line 905
						CallMethod V23Current self ::temp137 expected            ;@line 906
						Not ::temp135 ::temp137                                  ;@line 906
						JumpF ::temp135 _label56                                 ;@line 906
						Return False                                             ;@line 907
						Jump _label56                                            ;@line 907
					_label56:
						CallMethod EvaluatePackage actorRef ::NoneVar            ;@line 909
						CallMethod V23Current self ::temp141 expected            ;@line 910
						Not ::temp137 ::temp141                                  ;@line 910
						JumpF ::temp137 _label57                                 ;@line 910
						Return False                                             ;@line 911
						Jump _label57                                            ;@line 911
					_label57:
						Assign ::Artillero_var actorRef                          ;@line 913
						Cast ::temp136 None                                      ;@line 914
						Assign ownedGuard ::temp136                              ;@line 914
						Assign pinBusy False                                     ;@line 915
						Assign sceneBusy False                                   ;@line 916
						Assign phase 0                                           ;@line 917
						Cast ::temp136 None                                      ;@line 918
						Assign shotTarget ::temp136                              ;@line 918
						Assign guardPoseStarted False                            ;@line 919
						Assign guardPoseFiring False                             ;@line 920
						Assign v23PlacementVersion 26                            ;@line 921
						Cast ::temp146 actorRef                                  ;@line 922
						StrCat ::temp146 "Astra guard v26 migrated ref=" ::temp146  ;@line 922
						StrCat ::temp146 ::temp146 " station="                   ;@line 922
						Cast ::temp147 self                                      ;@line 922
						StrCat ::temp147 ::temp146 ::temp147                     ;@line 922
						CallStatic debug Trace ::NoneVar ::temp147 0             ;@line 922
						Return True                                              ;@line 923
					.endCode
				.endFunction
				.function PumpV23
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp153 Bool
						.local ::temp154 Bool
						.local ::temp155 Int
						.local ::temp156 actor
						.local expected Int
						.local available Bool
						.local ::NoneVar None
						.local actorRef actor
						.local ::temp157 Bool
						.local ::temp158 String
						.local ::temp159 ObjectReference
						.local migratedBeforeAvailability Bool
						.local status Int
						.local ::temp160 String
						.local ::temp161 Bool
						.local drained Bool
						.local backoff Float
						.local migrated Bool
						.local candidate Int
						.local accepted Bool
					.endLocalTable
					.code
						CompareEQ ::temp153 v23PumpOwner v23Generation           ;@line 944
						Cast ::temp153 ::temp153                                 ;@line 944
						JumpT ::temp153 _label58                                 ;@line 944
						Not ::temp154 v23Wanted                                  ;@line 944
						Cast ::temp153 ::temp154                                 ;@line 944
					_label58:
						Cast ::temp154 ::temp153                                 ;@line 944
						JumpT ::temp154 _label59                                 ;@line 944
						Cast ::temp154 stationRetired                            ;@line 944
					_label59:
						Cast ::temp153 ::temp154                                 ;@line 944
						JumpT ::temp153 _label60                                 ;@line 944
						Cast ::temp153 destroyed                                 ;@line 944
					_label60:
						JumpF ::temp153 _label61                                 ;@line 944
						Return None                                              ;@line 945
						Jump _label61                                            ;@line 945
					_label61:
						Assign expected v23Generation                            ;@line 947
						Assign v23PumpOwner expected                             ;@line 948
						CallStatic astraguardnative IsAvailable ::temp154        ;@line 949
						Cast ::temp154 ::temp154                                 ;@line 949
						JumpF ::temp154 _label62                                 ;@line 949
						CallStatic astraguardnative GetAPIVersion ::temp155      ;@line 949
						CompareEQ ::temp153 ::temp155 1                          ;@line 949
						Cast ::temp154 ::temp153                                 ;@line 949
					_label62:
						Assign available ::temp154                               ;@line 949
						CallMethod V23Current self ::temp153 expected            ;@line 950
						Not ::temp154 ::temp153                                  ;@line 950
						JumpF ::temp154 _label63                                 ;@line 950
						CallMethod FinishPumpV23 self ::NoneVar expected 0.000000  ;@line 951
						Return None                                              ;@line 952
						Jump _label63                                            ;@line 952
					_label63:
						CallMethod ResolveV23Operator self ::temp156             ;@line 954
						Assign actorRef ::temp156                                ;@line 954
						CallMethod V23Current self ::temp153 expected            ;@line 955
						Not ::temp154 ::temp153                                  ;@line 955
						JumpF ::temp154 _label64                                 ;@line 955
						CallMethod FinishPumpV23 self ::NoneVar expected 0.000000  ;@line 956
						Return None                                              ;@line 957
						Jump _label64                                            ;@line 957
					_label64:
						Cast ::temp156 None                                      ;@line 959
						CompareEQ ::temp153 actorRef ::temp156                   ;@line 959
						Cast ::temp153 ::temp153                                 ;@line 959
						JumpT ::temp153 _label65                                 ;@line 959
						CallMethod Is3DLoaded self ::temp154                     ;@line 959
						Not ::temp154 ::temp154                                  ;@line 959
						Cast ::temp153 ::temp154                                 ;@line 959
					_label65:
						Cast ::temp153 ::temp153                                 ;@line 959
						JumpT ::temp153 _label66                                 ;@line 959
						CallMethod Is3DLoaded actorRef ::temp154                 ;@line 959
						Not ::temp154 ::temp154                                  ;@line 959
						Cast ::temp153 ::temp154                                 ;@line 959
					_label66:
						Cast ::temp153 ::temp153                                 ;@line 959
						JumpT ::temp153 _label67                                 ;@line 959
						CallMethod IsDead actorRef ::temp154                     ;@line 959
						Cast ::temp153 ::temp154                                 ;@line 959
					_label67:
						JumpF ::temp153 _label68                                 ;@line 959
						Cast ::temp156 None                                      ;@line 960
						CompareEQ ::temp154 actorRef ::temp156                   ;@line 960
						Cast ::temp154 ::temp154                                 ;@line 960
						JumpF ::temp154 _label69                                 ;@line 960
						Not ::temp157 v27WarnedRefs                              ;@line 960
						Cast ::temp154 ::temp157                                 ;@line 960
					_label69:
						JumpF ::temp154 _label70                                 ;@line 960
						Cast ::temp158 self                                      ;@line 963
						StrCat ::temp158 "Astra guard v27: operator refs missing; enable AstraAsedio_WhiterunTorres.esp (B70/B71, B80/B81). station=" ::temp158  ;@line 963
						CallStatic debug Trace ::NoneVar ::temp158 0             ;@line 963
						Assign v27WarnedRefs True                                ;@line 964
						Jump _label70                                            ;@line 964
					_label70:
						CompareGT ::temp157 v23Token 0                           ;@line 966
						Cast ::temp154 ::temp157                                 ;@line 966
						JumpF ::temp154 _label71                                 ;@line 966
						Cast ::temp154 available                                 ;@line 966
					_label71:
						JumpF ::temp154 _label72                                 ;@line 966
						Cast ::temp159 self                                      ;@line 967
						CallStatic astraguardnative EndOperation ::temp157 ::temp159 v23Token  ;@line 967
						Jump _label72                                            ;@line 967
					_label72:
						CallMethod FinishPumpV23 self ::NoneVar expected 1.000000  ;@line 969
						Return None                                              ;@line 970
						Jump _label68                                            ;@line 970
					_label68:
						CompareLT ::temp157 v23PlacementVersion 26               ;@line 974
						Cast ::temp153 ::temp157                                 ;@line 974
						JumpF ::temp153 _label73                                 ;@line 974
						CompareEQ ::temp154 v23Token 0                           ;@line 974
						Cast ::temp153 ::temp154                                 ;@line 974
					_label73:
						JumpF ::temp153 _label74                                 ;@line 974
						CallMethod MigrateV23 self ::temp157 actorRef expected   ;@line 975
						Assign migratedBeforeAvailability ::temp157              ;@line 975
						Jump _label74                                            ;@line 975
					_label74:
						CallMethod V23Current self ::temp154 expected            ;@line 977
						Not ::temp157 ::temp154                                  ;@line 977
						JumpF ::temp157 _label75                                 ;@line 977
						CallMethod FinishPumpV23 self ::NoneVar expected 0.000000  ;@line 978
						Return None                                              ;@line 979
						Jump _label75                                            ;@line 979
					_label75:
						Not ::temp153 available                                  ;@line 981
						JumpF ::temp153 _label76                                 ;@line 981
						Not ::temp154 v23Warned                                  ;@line 982
						JumpF ::temp154 _label77                                 ;@line 982
						CallStatic debug Trace ::NoneVar "Astra guard v26: NPC runtime/OAR unavailable; firing disabled." 0  ;@line 983
						Assign v23Warned True                                    ;@line 984
						Jump _label77                                            ;@line 984
					_label77:
						CallMethod FinishPumpV23 self ::NoneVar expected 2.000000  ;@line 986
						Return None                                              ;@line 987
						Jump _label76                                            ;@line 987
					_label76:
						CompareGT ::temp157 v23Token 0                           ;@line 989
						JumpF ::temp157 _label78                                 ;@line 989
						Cast ::temp159 self                                      ;@line 990
						CallStatic astraguardnative GetStatus ::temp155 ::temp159 v23Token  ;@line 990
						Assign status ::temp155                                  ;@line 990
						CallMethod V23Current self ::temp154 expected            ;@line 991
						Not ::temp153 ::temp154                                  ;@line 991
						JumpF ::temp153 _label79                                 ;@line 991
						CallMethod FinishPumpV23 self ::NoneVar expected 0.000000  ;@line 992
						Return None                                              ;@line 993
						Jump _label79                                            ;@line 993
					_label79:
						CompareEQ ::temp154 status v23LastStatus                 ;@line 995
						Not ::temp154 ::temp154                                  ;@line 995
						JumpF ::temp154 _label80                                 ;@line 995
						Cast ::temp158 status                                    ;@line 996
						StrCat ::temp158 "Astra guard v26 status=" ::temp158     ;@line 996
						StrCat ::temp158 ::temp158 " station="                   ;@line 996
						Cast ::temp160 self                                      ;@line 996
						StrCat ::temp160 ::temp158 ::temp160                     ;@line 996
						StrCat ::temp158 ::temp160 " token="                     ;@line 996
						Cast ::temp160 v23Token                                  ;@line 996
						StrCat ::temp160 ::temp158 ::temp160                     ;@line 996
						CallStatic debug Trace ::NoneVar ::temp160 0             ;@line 996
						Assign v23LastStatus status                              ;@line 997
						Jump _label80                                            ;@line 997
					_label80:
						CompareEQ ::temp153 status 1                             ;@line 999
						Cast ::temp153 ::temp153                                 ;@line 999
						JumpT ::temp153 _label81                                 ;@line 999
						CompareEQ ::temp154 status 2                             ;@line 999
						Cast ::temp153 ::temp154                                 ;@line 999
					_label81:
						Cast ::temp153 ::temp153                                 ;@line 999
						JumpT ::temp153 _label82                                 ;@line 999
						CompareEQ ::temp154 status 3                             ;@line 999
						Cast ::temp153 ::temp154                                 ;@line 999
					_label82:
						JumpF ::temp153 _label83                                 ;@line 999
						Assign v27Faults 0                                       ;@line 1000
						Assign v28RetryWaited False                              ;@line 1001
						Jump _label83                                            ;@line 1001
					_label83:
						CompareEQ ::temp154 status -1                            ;@line 1003
						JumpF ::temp154 _label84                                 ;@line 1003
						Assign v27Faults 0                                       ;@line 1005
						Assign v28RetryWaited False                              ;@line 1006
						Assign v23Token 0                                        ;@line 1007
						Jump _label85                                            ;@line 1007
					_label84:
						CompareEQ ::temp153 status -2                            ;@line 1008
						JumpF ::temp153 _label85                                 ;@line 1008
						Cast ::temp159 self                                      ;@line 1009
						CallStatic astraguardnative EndOperation ::temp161 ::temp159 v23Token  ;@line 1009
						Assign drained ::temp161                                 ;@line 1009
						CallMethod V23Current self ::temp161 expected            ;@line 1010
						Cast ::temp161 ::temp161                                 ;@line 1010
						JumpF ::temp161 _label86                                 ;@line 1010
						Cast ::temp161 drained                                   ;@line 1010
					_label86:
						JumpF ::temp161 _label87                                 ;@line 1010
						Assign v23Token 0                                        ;@line 1011
						IAdd ::temp155 v27Faults 1                               ;@line 1012
						Assign v27Faults ::temp155                               ;@line 1012
						Assign v28RetryWaited False                              ;@line 1013
						Jump _label87                                            ;@line 1013
					_label87:
						Jump _label85                                            ;@line 1013
					_label85:
						Jump _label78                                            ;@line 1013
					_label78:
						CallMethod V23Current self ::temp161 expected            ;@line 1017
						Cast ::temp154 ::temp161                                 ;@line 1017
						JumpF ::temp154 _label88                                 ;@line 1017
						CompareEQ ::temp153 v23Token 0                           ;@line 1017
						Cast ::temp154 ::temp153                                 ;@line 1017
					_label88:
						JumpF ::temp154 _label89                                 ;@line 1017
						CompareGT ::temp157 v27Faults 0                          ;@line 1018
						Cast ::temp153 ::temp157                                 ;@line 1018
						JumpF ::temp153 _label90                                 ;@line 1018
						Not ::temp161 v28RetryWaited                             ;@line 1018
						Cast ::temp153 ::temp161                                 ;@line 1018
					_label90:
						JumpF ::temp153 _label91                                 ;@line 1018
						Assign backoff 5.000000                                  ;@line 1023
						CompareGT ::temp157 v27Faults 3                          ;@line 1024
						JumpF ::temp157 _label92                                 ;@line 1024
						Assign backoff 30.000000                                 ;@line 1025
						Jump _label92                                            ;@line 1025
					_label92:
						Cast ::temp158 backoff                                   ;@line 1027
						StrCat ::temp160 "Astra guard v27: backoff " ::temp158   ;@line 1027
						StrCat ::temp158 ::temp160 "s after "                    ;@line 1027
						Cast ::temp160 v27Faults                                 ;@line 1027
						StrCat ::temp160 ::temp158 ::temp160                     ;@line 1027
						StrCat ::temp158 ::temp160 " faulted acquisition(s); first clause is logged in AstraSight.log. station="  ;@line 1027
						Cast ::temp160 self                                      ;@line 1027
						StrCat ::temp160 ::temp158 ::temp160                     ;@line 1027
						CallStatic debug Trace ::NoneVar ::temp160 0             ;@line 1027
						Assign v28RetryWaited True                               ;@line 1028
						CallMethod FinishPumpV23 self ::NoneVar expected backoff  ;@line 1029
						Return None                                              ;@line 1030
						Jump _label91                                            ;@line 1030
					_label91:
						CompareGTE ::temp161 v23PlacementVersion 26              ;@line 1032
						Assign migrated ::temp161                                ;@line 1032
						Not ::temp157 migrated                                   ;@line 1033
						JumpF ::temp157 _label93                                 ;@line 1033
						CallMethod MigrateV23 self ::temp153 actorRef expected   ;@line 1034
						Assign migrated ::temp153                                ;@line 1034
						Jump _label93                                            ;@line 1034
					_label93:
						Cast ::temp153 migrated                                  ;@line 1036
						JumpF ::temp153 _label94                                 ;@line 1036
						CallMethod V23Current self ::temp161 expected            ;@line 1036
						Cast ::temp153 ::temp161                                 ;@line 1036
					_label94:
						Cast ::temp161 ::temp153                                 ;@line 1036
						JumpF ::temp161 _label95                                 ;@line 1036
						CompareLT ::temp157 v23Serial 2000000000                 ;@line 1036
						Cast ::temp161 ::temp157                                 ;@line 1036
					_label95:
						JumpF ::temp161 _label96                                 ;@line 1036
						CallMethod PrepareShieldV26 self ::temp153 actorRef expected  ;@line 1037
						Not ::temp157 ::temp153                                  ;@line 1037
						JumpF ::temp157 _label97                                 ;@line 1037
						CallMethod FinishPumpV23 self ::NoneVar expected 0.200000  ;@line 1038
						Return None                                              ;@line 1039
						Jump _label97                                            ;@line 1039
					_label97:
						CallMethod V23Current self ::temp153 expected            ;@line 1041
						Not ::temp157 ::temp153                                  ;@line 1041
						JumpF ::temp157 _label98                                 ;@line 1041
						CallMethod FinishPumpV23 self ::NoneVar expected 0.000000  ;@line 1042
						Return None                                              ;@line 1043
						Jump _label98                                            ;@line 1043
					_label98:
						IAdd ::temp155 v23Serial 1                               ;@line 1045
						Assign v23Serial ::temp155                               ;@line 1045
						Assign candidate v23Serial                               ;@line 1046
						Cast ::temp159 self                                      ;@line 1047
						CallStatic astraguardnative BeginOperation ::temp153 ::temp159 actorRef candidate ::Launcher_var ::ShotAmmo_var ::ShotSound_var  ;@line 1047
						Assign accepted ::temp153                                ;@line 1047
						CallMethod V23Current self ::temp157 expected            ;@line 1048
						Cast ::temp153 ::temp157                                 ;@line 1048
						JumpF ::temp153 _label99                                 ;@line 1048
						Cast ::temp153 accepted                                  ;@line 1048
					_label99:
						JumpF ::temp153 _label100                                ;@line 1048
						Assign v23Token candidate                                ;@line 1049
						Assign v23Warned False                                   ;@line 1050
						Jump _label101                                           ;@line 1050
					_label100:
						JumpF accepted _label101                                 ;@line 1051
						Cast ::temp159 self                                      ;@line 1052
						CallStatic astraguardnative EndOperation ::temp157 ::temp159 candidate  ;@line 1052
						Jump _label101                                           ;@line 1052
					_label101:
						Jump _label96                                            ;@line 1052
					_label96:
						Jump _label89                                            ;@line 1052
					_label89:
						CallMethod FinishPumpV23 self ::NoneVar expected 1.000000  ;@line 1056
					.endCode
				.endFunction
				.function RestoreNeutralScene
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
					.endLocalTable
					.code
						Return None                                              ;@line 292
					.endCode
				.endFunction
				.function CaptureMatrices
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
					.localTable
						.local ::temp26 Int
						.local ::temp27 Bool
						.local ::temp28 Bool
						.local ::temp29 ObjectReference
						.local ::temp30 Float[]
						.local ::temp31 Float
						.local captureGeneration Int
					.endLocalTable
					.code
						Assign captureGeneration generation                      ;@line 321
						CallStatic skse GetVersion ::temp26                      ;@line 322
						CompareLT ::temp27 ::temp26 2                            ;@line 322
						Cast ::temp27 ::temp27                                   ;@line 322
						JumpT ::temp27 _label102                                 ;@line 322
						CallMethod Is3DLoaded self ::temp28                      ;@line 322
						Not ::temp28 ::temp28                                    ;@line 322
						Cast ::temp27 ::temp28                                   ;@line 322
					_label102:
						JumpF ::temp27 _label103                                 ;@line 322
						Return False                                             ;@line 323
						Jump _label103                                           ;@line 323
					_label103:
						Cast ::temp29 self                                       ;@line 325
						CallStatic netimmerse HasNode ::temp28 ::temp29 ::YawNode_var False  ;@line 325
						Not ::temp27 ::temp28                                    ;@line 325
						Cast ::temp27 ::temp27                                   ;@line 325
						JumpT ::temp27 _label104                                 ;@line 325
						Cast ::temp29 self                                       ;@line 325
						CallStatic netimmerse HasNode ::temp28 ::temp29 ::PitchNode_var False  ;@line 325
						Not ::temp28 ::temp28                                    ;@line 325
						Cast ::temp27 ::temp28                                   ;@line 325
					_label104:
						Cast ::temp27 ::temp27                                   ;@line 325
						JumpT ::temp27 _label105                                 ;@line 325
						Cast ::temp29 self                                       ;@line 325
						CallStatic netimmerse HasNode ::temp28 ::temp29 ::MuzzleNode_var False  ;@line 325
						Not ::temp28 ::temp28                                    ;@line 325
						Cast ::temp27 ::temp28                                   ;@line 325
					_label105:
						Cast ::temp27 ::temp27                                   ;@line 325
						JumpT ::temp27 _label106                                 ;@line 325
						Cast ::temp29 self                                       ;@line 325
						CallStatic netimmerse HasNode ::temp28 ::temp29 ::VisualBoltNode_var False  ;@line 325
						Not ::temp28 ::temp28                                    ;@line 325
						Cast ::temp27 ::temp28                                   ;@line 325
					_label106:
						JumpF ::temp27 _label107                                 ;@line 325
						Return False                                             ;@line 326
						Jump _label107                                           ;@line 326
					_label107:
						CompareEQ ::temp28 generation captureGeneration          ;@line 328
						Not ::temp28 ::temp28                                    ;@line 328
						Cast ::temp28 ::temp28                                   ;@line 328
						JumpT ::temp28 _label108                                 ;@line 328
						CompareEQ ::temp27 token -1                              ;@line 328
						Not ::temp27 ::temp27                                    ;@line 328
						Cast ::temp28 ::temp27                                   ;@line 328
					_label108:
						Cast ::temp28 ::temp28                                   ;@line 328
						JumpT ::temp28 _label109                                 ;@line 328
						Not ::temp27 recovering                                  ;@line 328
						Cast ::temp28 ::temp27                                   ;@line 328
					_label109:
						JumpF ::temp28 _label110                                 ;@line 328
						Return False                                             ;@line 329
						Jump _label110                                           ;@line 329
					_label110:
						ArrayCreate ::temp30 9                                   ;@line 334
						Assign yawBase ::temp30                                  ;@line 334
						ArrayCreate ::temp30 9                                   ;@line 335
						Assign pitchBase ::temp30                                ;@line 335
						ArrayCreate ::temp30 9                                   ;@line 336
						Assign yawMatrix ::temp30                                ;@line 336
						ArrayCreate ::temp30 9                                   ;@line 337
						Assign pitchMatrix ::temp30                              ;@line 337
						ArrayCreate ::temp30 9                                   ;@line 338
						Assign rootWorldMatrix ::temp30                          ;@line 338
						ArrayCreate ::temp30 9                                   ;@line 339
						Assign muzzleWorldMatrix ::temp30                        ;@line 339
						ArrayCreate ::temp30 3                                   ;@line 340
						Assign rootPosition ::temp30                             ;@line 340
						ArrayCreate ::temp30 3                                   ;@line 341
						Assign muzzlePosition ::temp30                           ;@line 341
						Assign ::temp31 1.000000                                 ;@line 342
						ArraySetElement yawBase 0 ::temp31                       ;@line 342
						Assign ::temp31 1.000000                                 ;@line 343
						ArraySetElement yawBase 4 ::temp31                       ;@line 343
						Assign ::temp31 1.000000                                 ;@line 344
						ArraySetElement yawBase 8 ::temp31                       ;@line 344
						Assign ::temp31 1.000000                                 ;@line 345
						ArraySetElement pitchBase 0 ::temp31                     ;@line 345
						Assign ::temp31 1.000000                                 ;@line 346
						ArraySetElement pitchBase 4 ::temp31                     ;@line 346
						Assign ::temp31 1.000000                                 ;@line 347
						ArraySetElement pitchBase 8 ::temp31                     ;@line 347
						Assign matricesReady True                                ;@line 348
						Return True                                              ;@line 349
					.endCode
				.endFunction
				.function NotifyCombatV23
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param target actor
					.endParamTable
					.localTable
						.local ::temp164 Bool
						.local ::temp165 Bool
						.local ::temp166 ObjectReference
					.endLocalTable
					.code
						Cast ::temp164 v23Wanted                                 ;@line 1070
						JumpF ::temp164 _label111                                ;@line 1070
						CompareGT ::temp164 v23Token 0                           ;@line 1070
						Cast ::temp164 ::temp164                                 ;@line 1070
					_label111:
						Cast ::temp164 ::temp164                                 ;@line 1070
						JumpF ::temp164 _label112                                ;@line 1070
						CallStatic astraguardnative IsAvailable ::temp165        ;@line 1070
						Cast ::temp164 ::temp165                                 ;@line 1070
					_label112:
						JumpF ::temp164 _label113                                ;@line 1070
						Cast ::temp166 self                                      ;@line 1071
						CallStatic astraguardnative NotifyCombat ::temp165 ::temp166 v23Token target  ;@line 1071
						Jump _label113                                           ;@line 1071
					_label113:
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
					.endLocalTable
					.code
						Return False                                             ;@line 268
					.endCode
				.endFunction
				.function QueueDeferredRecovery
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp23 Bool
						.local ::temp24 Bool
						.local queueGeneration Int
						.local loaded Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						Cast ::temp23 playerReserved                             ;@line 277
						JumpT ::temp23 _label114                                 ;@line 277
						Cast ::temp23 pinBusy                                    ;@line 277
					_label114:
						Cast ::temp23 ::temp23                                   ;@line 277
						JumpT ::temp23 _label115                                 ;@line 277
						Cast ::temp23 sceneBusy                                  ;@line 277
					_label115:
						Cast ::temp23 ::temp23                                   ;@line 277
						JumpT ::temp23 _label116                                 ;@line 277
						Not ::temp24 recoveryRequested                           ;@line 277
						Cast ::temp23 ::temp24                                   ;@line 277
					_label116:
						Cast ::temp24 ::temp23                                   ;@line 277
						JumpT ::temp24 _label117                                 ;@line 277
						Cast ::temp24 destroyed                                  ;@line 277
					_label117:
						Cast ::temp23 ::temp24                                   ;@line 277
						JumpT ::temp23 _label118                                 ;@line 277
						Cast ::temp23 faulted                                    ;@line 277
					_label118:
						JumpF ::temp23 _label119                                 ;@line 277
						Return None                                              ;@line 278
						Jump _label119                                           ;@line 278
					_label119:
						Assign queueGeneration generation                        ;@line 280
						CallMethod Is3DLoaded self ::temp24                      ;@line 281
						Assign loaded ::temp24                                   ;@line 281
						CompareEQ ::temp23 generation queueGeneration            ;@line 282
						Not ::temp23 ::temp23                                    ;@line 282
						Cast ::temp24 ::temp23                                   ;@line 282
						JumpT ::temp24 _label120                                 ;@line 282
						Cast ::temp24 pinBusy                                    ;@line 282
					_label120:
						Cast ::temp23 ::temp24                                   ;@line 282
						JumpT ::temp23 _label121                                 ;@line 282
						Cast ::temp23 sceneBusy                                  ;@line 282
					_label121:
						Cast ::temp23 ::temp23                                   ;@line 282
						JumpT ::temp23 _label122                                 ;@line 282
						Not ::temp24 recoveryRequested                           ;@line 282
						Cast ::temp23 ::temp24                                   ;@line 282
					_label122:
						Cast ::temp24 ::temp23                                   ;@line 282
						JumpT ::temp24 _label123                                 ;@line 282
						Cast ::temp24 destroyed                                  ;@line 282
					_label123:
						Cast ::temp23 ::temp24                                   ;@line 282
						JumpT ::temp23 _label124                                 ;@line 282
						Cast ::temp23 faulted                                    ;@line 282
					_label124:
						JumpF ::temp23 _label125                                 ;@line 282
						Return None                                              ;@line 283
						Jump _label125                                           ;@line 283
					_label125:
						JumpF loaded _label126                                   ;@line 285
						CallMethod RegisterForSingleUpdate self ::NoneVar 0.200000  ;@line 286
						Jump _label126                                           ;@line 286
					_label126:
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
						.local ::temp65 Bool
						.local ::temp66 Float
						.local ::NoneVar None
						.local rate Float
						.local nextYaw Float
						.local nextPitch Float
					.endLocalTable
					.code
						Assign rate ::TurnRate_var                               ;@line 468
						CallMethod Finite self ::temp65 rate 1.000000 30.000000  ;@line 469
						Not ::temp65 ::temp65                                    ;@line 469
						JumpF ::temp65 _label127                                 ;@line 469
						Assign rate 30.000000                                    ;@line 470
						Jump _label127                                           ;@line 470
					_label127:
						FMultiply ::temp66 rate dt                               ;@line 472
						CallMethod Approach self ::temp66 yaw desiredYaw ::temp66  ;@line 472
						Assign nextYaw ::temp66                                  ;@line 472
						Assign nextPitch 0.000000                                ;@line 473
						CallMethod Current self ::temp65 expectedGeneration expectedToken  ;@line 474
						Not ::temp65 ::temp65                                    ;@line 474
						JumpF ::temp65 _label128                                 ;@line 474
						Return None                                              ;@line 475
						Jump _label128                                           ;@line 475
					_label128:
						Assign yaw nextYaw                                       ;@line 477
						Assign pitch nextPitch                                   ;@line 478
						CallMethod ApplyAim self ::NoneVar expectedGeneration expectedToken  ;@line 479
					.endCode
				.endFunction
				.function V23Current
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param expected Int
					.endParamTable
					.localTable
						.local ::temp133 Bool
						.local ::temp134 Bool
					.endLocalTable
					.code
						CompareEQ ::temp133 v23Generation expected               ;@line 836
						Cast ::temp133 ::temp133                                 ;@line 836
						JumpF ::temp133 _label129                                ;@line 836
						Cast ::temp133 v23Wanted                                 ;@line 836
					_label129:
						Cast ::temp133 ::temp133                                 ;@line 836
						JumpF ::temp133 _label130                                ;@line 836
						Not ::temp134 stationRetired                             ;@line 836
						Cast ::temp133 ::temp134                                 ;@line 836
					_label130:
						Cast ::temp133 ::temp133                                 ;@line 836
						JumpF ::temp133 _label131                                ;@line 836
						Not ::temp134 destroyed                                  ;@line 836
						Cast ::temp133 ::temp134                                 ;@line 836
					_label131:
						Return ::temp133                                         ;@line 836
					.endCode
				.endFunction
				.function StopV23
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp123 Int
						.local ::NoneVar None
						.local ::temp124 Bool
						.local ::temp125 Bool
						.local ::temp126 ObjectReference
					.endLocalTable
					.code
						IAdd ::temp123 generation 1                              ;@line 813
						Assign generation ::temp123                              ;@line 813
						Assign running False                                     ;@line 814
						IAdd ::temp123 v23Generation 1                           ;@line 815
						Assign v23Generation ::temp123                           ;@line 815
						Assign v23Wanted False                                   ;@line 816
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 817
						CompareGT ::temp124 v23Token 0                           ;@line 818
						Cast ::temp124 ::temp124                                 ;@line 818
						JumpF ::temp124 _label132                                ;@line 818
						CallStatic astraguardnative IsAvailable ::temp125        ;@line 818
						Cast ::temp124 ::temp125                                 ;@line 818
					_label132:
						JumpF ::temp124 _label133                                ;@line 818
						Cast ::temp126 self                                      ;@line 819
						CallStatic astraguardnative EndOperation ::temp125 ::temp126 v23Token  ;@line 819
						Jump _label133                                           ;@line 819
					_label133:
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
						.local ::temp51 Bool
						.local ::temp52 actor
						.local ::temp53 Bool
						.local ::temp54 Int
						.local ::temp55 ObjectReference
						.local player actor
						.local valid Bool
						.local visible Bool
						.local combatTarget actor
					.endLocalTable
					.code
						CallMethod GuardReady self ::temp51 expectedGeneration expectedToken  ;@line 418
						Not ::temp51 ::temp51                                    ;@line 418
						Cast ::temp51 ::temp51                                   ;@line 418
						JumpT ::temp51 _label134                                 ;@line 418
						Cast ::temp52 None                                       ;@line 418
						CompareEQ ::temp53 target ::temp52                       ;@line 418
						Cast ::temp51 ::temp53                                   ;@line 418
					_label134:
						Cast ::temp51 ::temp51                                   ;@line 418
						JumpT ::temp51 _label135                                 ;@line 418
						CompareEQ ::temp53 target ::Artillero_var                ;@line 418
						Cast ::temp51 ::temp53                                   ;@line 418
					_label135:
						JumpF ::temp51 _label136                                 ;@line 418
						Return False                                             ;@line 419
						Jump _label136                                           ;@line 419
					_label136:
						CallStatic game GetPlayer ::temp52                       ;@line 421
						Assign player ::temp52                                   ;@line 421
						CallMethod Current self ::temp53 expectedGeneration expectedToken  ;@line 422
						Not ::temp51 ::temp53                                    ;@line 422
						Cast ::temp51 ::temp51                                   ;@line 422
						JumpT ::temp51 _label137                                 ;@line 422
						CompareEQ ::temp53 target player                         ;@line 422
						Cast ::temp51 ::temp53                                   ;@line 422
					_label137:
						JumpF ::temp51 _label138                                 ;@line 422
						Return False                                             ;@line 423
						Jump _label138                                           ;@line 423
					_label138:
						CallMethod Is3DLoaded target ::temp53                    ;@line 425
						Cast ::temp53 ::temp53                                   ;@line 425
						JumpF ::temp53 _label139                                 ;@line 425
						CallMethod IsDisabled target ::temp51                    ;@line 425
						Not ::temp51 ::temp51                                    ;@line 425
						Cast ::temp53 ::temp51                                   ;@line 425
					_label139:
						Cast ::temp53 ::temp53                                   ;@line 425
						JumpF ::temp53 _label140                                 ;@line 425
						CallMethod IsDead target ::temp51                        ;@line 425
						Not ::temp51 ::temp51                                    ;@line 425
						Cast ::temp53 ::temp51                                   ;@line 425
					_label140:
						Cast ::temp53 ::temp53                                   ;@line 425
						JumpF ::temp53 _label141                                 ;@line 425
						CallMethod IsPlayerTeammate target ::temp51              ;@line 425
						Not ::temp51 ::temp51                                    ;@line 425
						Cast ::temp53 ::temp51                                   ;@line 425
					_label141:
						Cast ::temp53 ::temp53                                   ;@line 425
						JumpF ::temp53 _label142                                 ;@line 425
						CallMethod IsHostileToActor target ::temp51 ::Artillero_var  ;@line 425
						Cast ::temp53 ::temp51                                   ;@line 425
					_label142:
						Cast ::temp53 ::temp53                                   ;@line 425
						JumpF ::temp53 _label143                                 ;@line 425
						CallMethod GetCombatState target ::temp54                ;@line 425
						CompareGT ::temp51 ::temp54 0                            ;@line 425
						Cast ::temp53 ::temp51                                   ;@line 425
					_label143:
						Cast ::temp53 ::temp53                                   ;@line 425
						JumpF ::temp53 _label144                                 ;@line 425
						CallMethod GetCombatState ::Artillero_var ::temp54       ;@line 425
						CompareEQ ::temp51 ::temp54 1                            ;@line 425
						Cast ::temp53 ::temp51                                   ;@line 425
					_label144:
						Assign valid ::temp53                                    ;@line 425
						Cast ::temp55 target                                     ;@line 426
						CallMethod HasLOS ::Artillero_var ::temp51 ::temp55      ;@line 426
						Assign visible ::temp51                                  ;@line 426
						CallMethod GetCombatTarget ::Artillero_var ::temp52      ;@line 427
						Assign combatTarget ::temp52                             ;@line 427
						CallMethod Current self ::temp53 expectedGeneration expectedToken  ;@line 428
						Cast ::temp51 ::temp53                                   ;@line 428
						JumpF ::temp51 _label145                                 ;@line 428
						Cast ::temp51 valid                                      ;@line 428
					_label145:
						Cast ::temp53 ::temp51                                   ;@line 428
						JumpF ::temp53 _label146                                 ;@line 428
						Cast ::temp53 visible                                    ;@line 428
					_label146:
						Cast ::temp53 ::temp53                                   ;@line 428
						JumpF ::temp53 _label147                                 ;@line 428
						CompareEQ ::temp51 combatTarget target                   ;@line 428
						Cast ::temp53 ::temp51                                   ;@line 428
					_label147:
						Return ::temp53                                          ;@line 428
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
						.local ::temp46 Bool
						.local ::temp47 actor
						.local ::temp48 Bool
						.local ::temp49 ObjectReference
						.local ::temp50 Float
						.local ready Bool
						.local distance Float
					.endLocalTable
					.code
						CallMethod Current self ::temp46 expectedGeneration expectedToken  ;@line 409
						Not ::temp46 ::temp46                                    ;@line 409
						Cast ::temp46 ::temp46                                   ;@line 409
						JumpT ::temp46 _label148                                 ;@line 409
						Cast ::temp47 None                                       ;@line 409
						CompareEQ ::temp48 ownedGuard ::temp47                   ;@line 409
						Cast ::temp46 ::temp48                                   ;@line 409
					_label148:
						Cast ::temp46 ::temp46                                   ;@line 409
						JumpT ::temp46 _label149                                 ;@line 409
						CompareEQ ::temp48 ownedGuard ::Artillero_var            ;@line 409
						Not ::temp48 ::temp48                                    ;@line 409
						Cast ::temp46 ::temp48                                   ;@line 409
					_label149:
						JumpF ::temp46 _label150                                 ;@line 409
						Return False                                             ;@line 410
						Jump _label150                                           ;@line 410
					_label150:
						CallMethod Is3DLoaded self ::temp48                      ;@line 412
						Cast ::temp48 ::temp48                                   ;@line 412
						JumpF ::temp48 _label151                                 ;@line 412
						CallMethod IsDisabled self ::temp46                      ;@line 412
						Not ::temp46 ::temp46                                    ;@line 412
						Cast ::temp48 ::temp46                                   ;@line 412
					_label151:
						Cast ::temp48 ::temp48                                   ;@line 412
						JumpF ::temp48 _label152                                 ;@line 412
						CallMethod Is3DLoaded ownedGuard ::temp46                ;@line 412
						Cast ::temp48 ::temp46                                   ;@line 412
					_label152:
						Cast ::temp48 ::temp48                                   ;@line 412
						JumpF ::temp48 _label153                                 ;@line 412
						CallMethod IsDead ownedGuard ::temp46                    ;@line 412
						Not ::temp46 ::temp46                                    ;@line 412
						Cast ::temp48 ::temp46                                   ;@line 412
					_label153:
						Cast ::temp48 ::temp48                                   ;@line 412
						JumpF ::temp48 _label154                                 ;@line 412
						CallMethod IsDisabled ownedGuard ::temp46                ;@line 412
						Not ::temp46 ::temp46                                    ;@line 412
						Cast ::temp48 ::temp46                                   ;@line 412
					_label154:
						Assign ready ::temp48                                    ;@line 412
						Cast ::temp49 self                                       ;@line 413
						CallMethod GetDistance ownedGuard ::temp50 ::temp49      ;@line 413
						Assign distance ::temp50                                 ;@line 413
						CallMethod Current self ::temp46 expectedGeneration expectedToken  ;@line 414
						Cast ::temp48 ::temp46                                   ;@line 414
						JumpF ::temp48 _label155                                 ;@line 414
						Cast ::temp48 ready                                      ;@line 414
					_label155:
						Cast ::temp48 ::temp48                                   ;@line 414
						JumpF ::temp48 _label156                                 ;@line 414
						CallMethod Finite self ::temp46 distance 0.000000 240.000000  ;@line 414
						Cast ::temp48 ::temp46                                   ;@line 414
					_label156:
						Return ::temp48                                          ;@line 414
					.endCode
				.endFunction
				.function PositionOperator
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
					.endLocalTable
					.code
						Return False                                             ;@line 688
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
						.local ::temp40 Bool
						.local ::temp41 Bool
						.local ::temp42 ObjectReference
						.local rootRead Bool
						.local muzzleRead Bool
						.local rootPointRead Bool
						.local muzzlePointRead Bool
						.local i Int
						.local ::temp43 Float
						.local ::temp44 Bool
						.local ::temp45 Int
					.endLocalTable
					.code
						CallMethod Current self ::temp40 expectedGeneration expectedToken  ;@line 376
						Not ::temp40 ::temp40                                    ;@line 376
						Cast ::temp40 ::temp40                                   ;@line 376
						JumpT ::temp40 _label157                                 ;@line 376
						Not ::temp41 matricesReady                               ;@line 376
						Cast ::temp40 ::temp41                                   ;@line 376
					_label157:
						JumpF ::temp40 _label158                                 ;@line 376
						Return False                                             ;@line 377
						Jump _label158                                           ;@line 377
					_label158:
						Cast ::temp42 self                                       ;@line 379
						CallStatic netimmerse GetNodeWorldRotationMatrix ::temp41 ::temp42 "" rootWorldMatrix False  ;@line 379
						Assign rootRead ::temp41                                 ;@line 379
						CallMethod Current self ::temp40 expectedGeneration expectedToken  ;@line 380
						Not ::temp41 ::temp40                                    ;@line 380
						Cast ::temp41 ::temp41                                   ;@line 380
						JumpT ::temp41 _label159                                 ;@line 380
						Not ::temp40 rootRead                                    ;@line 380
						Cast ::temp41 ::temp40                                   ;@line 380
					_label159:
						JumpF ::temp41 _label160                                 ;@line 380
						Return False                                             ;@line 381
						Jump _label160                                           ;@line 381
					_label160:
						Cast ::temp42 self                                       ;@line 383
						CallStatic netimmerse GetNodeWorldRotationMatrix ::temp40 ::temp42 ::MuzzleNode_var muzzleWorldMatrix False  ;@line 383
						Assign muzzleRead ::temp40                               ;@line 383
						CallMethod Current self ::temp41 expectedGeneration expectedToken  ;@line 384
						Not ::temp40 ::temp41                                    ;@line 384
						Cast ::temp40 ::temp40                                   ;@line 384
						JumpT ::temp40 _label161                                 ;@line 384
						Not ::temp41 muzzleRead                                  ;@line 384
						Cast ::temp40 ::temp41                                   ;@line 384
					_label161:
						JumpF ::temp40 _label162                                 ;@line 384
						Return False                                             ;@line 385
						Jump _label162                                           ;@line 385
					_label162:
						Cast ::temp42 self                                       ;@line 387
						CallStatic netimmerse GetNodeWorldPosition ::temp41 ::temp42 "" rootPosition False  ;@line 387
						Assign rootPointRead ::temp41                            ;@line 387
						CallMethod Current self ::temp40 expectedGeneration expectedToken  ;@line 388
						Not ::temp41 ::temp40                                    ;@line 388
						Cast ::temp41 ::temp41                                   ;@line 388
						JumpT ::temp41 _label163                                 ;@line 388
						Not ::temp40 rootPointRead                               ;@line 388
						Cast ::temp41 ::temp40                                   ;@line 388
					_label163:
						JumpF ::temp41 _label164                                 ;@line 388
						Return False                                             ;@line 389
						Jump _label164                                           ;@line 389
					_label164:
						Cast ::temp42 self                                       ;@line 391
						CallStatic netimmerse GetNodeWorldPosition ::temp40 ::temp42 ::MuzzleNode_var muzzlePosition False  ;@line 391
						Assign muzzlePointRead ::temp40                          ;@line 391
						CallMethod Current self ::temp41 expectedGeneration expectedToken  ;@line 392
						Not ::temp40 ::temp41                                    ;@line 392
						Cast ::temp40 ::temp40                                   ;@line 392
						JumpT ::temp40 _label165                                 ;@line 392
						Not ::temp41 muzzlePointRead                             ;@line 392
						Cast ::temp40 ::temp41                                   ;@line 392
					_label165:
						JumpF ::temp40 _label166                                 ;@line 392
						Return False                                             ;@line 393
						Jump _label166                                           ;@line 393
					_label166:
						CallMethod RotationValid self ::temp41 rootWorldMatrix   ;@line 395
						Not ::temp40 ::temp41                                    ;@line 395
						Cast ::temp40 ::temp40                                   ;@line 395
						JumpT ::temp40 _label167                                 ;@line 395
						CallMethod RotationValid self ::temp41 muzzleWorldMatrix  ;@line 395
						Not ::temp41 ::temp41                                    ;@line 395
						Cast ::temp40 ::temp41                                   ;@line 395
					_label167:
						JumpF ::temp40 _label168                                 ;@line 395
						Return False                                             ;@line 396
						Jump _label168                                           ;@line 396
					_label168:
						Assign i 0                                               ;@line 398
					_label172:
						CompareLT ::temp41 i 3                                   ;@line 399
						JumpF ::temp41 _label169                                 ;@line 399
						ArrayGetElement ::temp43 rootPosition i                  ;@line 400
						CallMethod Finite self ::temp40 ::temp43 -1000000.000000 1000000.000000  ;@line 400
						Not ::temp40 ::temp40                                    ;@line 400
						Cast ::temp40 ::temp40                                   ;@line 400
						JumpT ::temp40 _label170                                 ;@line 400
						ArrayGetElement ::temp43 muzzlePosition i                ;@line 400
						CallMethod Finite self ::temp44 ::temp43 -1000000.000000 1000000.000000  ;@line 400
						Not ::temp44 ::temp44                                    ;@line 400
						Cast ::temp40 ::temp44                                   ;@line 400
					_label170:
						JumpF ::temp40 _label171                                 ;@line 400
						Return False                                             ;@line 401
						Jump _label171                                           ;@line 401
					_label171:
						IAdd ::temp45 i 1                                        ;@line 403
						Assign i ::temp45                                        ;@line 403
						Jump _label172                                           ;@line 403
					_label169:
						CallMethod Current self ::temp44 expectedGeneration expectedToken  ;@line 405
						Return ::temp44                                          ;@line 405
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
						.local ::temp32 Bool
						.local ::temp36 Float
						.local ::temp37 Float
						.local ::temp38 Float
						.local ::temp39 Float
						.local i Int
						.local ::temp33 Float
						.local ::temp34 Bool
						.local ::temp35 Int
						.local a Float
						.local b Float
						.local c Float
						.local ab Float
						.local ac Float
						.local bc Float
						.local determinant Float
					.endLocalTable
					.code
						Assign i 0                                               ;@line 358
					_label175:
						CompareLT ::temp32 i 9                                   ;@line 359
						JumpF ::temp32 _label173                                 ;@line 359
						ArrayGetElement ::temp33 matrix i                        ;@line 360
						CallMethod Finite self ::temp34 ::temp33 -1.050000 1.050000  ;@line 360
						Not ::temp34 ::temp34                                    ;@line 360
						JumpF ::temp34 _label174                                 ;@line 360
						Return False                                             ;@line 361
						Jump _label174                                           ;@line 361
					_label174:
						IAdd ::temp35 i 1                                        ;@line 363
						Assign i ::temp35                                        ;@line 363
						Jump _label175                                           ;@line 363
					_label173:
						ArrayGetElement ::temp33 matrix 0                        ;@line 365
						ArrayGetElement ::temp36 matrix 0                        ;@line 365
						FMultiply ::temp33 ::temp33 ::temp36                     ;@line 365
						ArrayGetElement ::temp36 matrix 3                        ;@line 365
						ArrayGetElement ::temp37 matrix 3                        ;@line 365
						FMultiply ::temp36 ::temp36 ::temp37                     ;@line 365
						FAdd ::temp37 ::temp33 ::temp36                          ;@line 365
						ArrayGetElement ::temp33 matrix 6                        ;@line 365
						ArrayGetElement ::temp36 matrix 6                        ;@line 365
						FMultiply ::temp33 ::temp33 ::temp36                     ;@line 365
						FAdd ::temp36 ::temp37 ::temp33                          ;@line 365
						Assign a ::temp36                                        ;@line 365
						ArrayGetElement ::temp37 matrix 1                        ;@line 366
						ArrayGetElement ::temp33 matrix 1                        ;@line 366
						FMultiply ::temp36 ::temp37 ::temp33                     ;@line 366
						ArrayGetElement ::temp37 matrix 4                        ;@line 366
						ArrayGetElement ::temp33 matrix 4                        ;@line 366
						FMultiply ::temp37 ::temp37 ::temp33                     ;@line 366
						FAdd ::temp33 ::temp36 ::temp37                          ;@line 366
						ArrayGetElement ::temp36 matrix 7                        ;@line 366
						ArrayGetElement ::temp37 matrix 7                        ;@line 366
						FMultiply ::temp36 ::temp36 ::temp37                     ;@line 366
						FAdd ::temp37 ::temp33 ::temp36                          ;@line 366
						Assign b ::temp37                                        ;@line 366
						ArrayGetElement ::temp33 matrix 2                        ;@line 367
						ArrayGetElement ::temp36 matrix 2                        ;@line 367
						FMultiply ::temp37 ::temp33 ::temp36                     ;@line 367
						ArrayGetElement ::temp33 matrix 5                        ;@line 367
						ArrayGetElement ::temp36 matrix 5                        ;@line 367
						FMultiply ::temp33 ::temp33 ::temp36                     ;@line 367
						FAdd ::temp36 ::temp37 ::temp33                          ;@line 367
						ArrayGetElement ::temp37 matrix 8                        ;@line 367
						ArrayGetElement ::temp33 matrix 8                        ;@line 367
						FMultiply ::temp37 ::temp37 ::temp33                     ;@line 367
						FAdd ::temp33 ::temp36 ::temp37                          ;@line 367
						Assign c ::temp33                                        ;@line 367
						ArrayGetElement ::temp36 matrix 0                        ;@line 368
						ArrayGetElement ::temp37 matrix 1                        ;@line 368
						FMultiply ::temp33 ::temp36 ::temp37                     ;@line 368
						ArrayGetElement ::temp36 matrix 3                        ;@line 368
						ArrayGetElement ::temp37 matrix 4                        ;@line 368
						FMultiply ::temp36 ::temp36 ::temp37                     ;@line 368
						FAdd ::temp37 ::temp33 ::temp36                          ;@line 368
						ArrayGetElement ::temp33 matrix 6                        ;@line 368
						ArrayGetElement ::temp36 matrix 7                        ;@line 368
						FMultiply ::temp33 ::temp33 ::temp36                     ;@line 368
						FAdd ::temp36 ::temp37 ::temp33                          ;@line 368
						Assign ab ::temp36                                       ;@line 368
						ArrayGetElement ::temp37 matrix 0                        ;@line 369
						ArrayGetElement ::temp33 matrix 2                        ;@line 369
						FMultiply ::temp36 ::temp37 ::temp33                     ;@line 369
						ArrayGetElement ::temp37 matrix 3                        ;@line 369
						ArrayGetElement ::temp33 matrix 5                        ;@line 369
						FMultiply ::temp37 ::temp37 ::temp33                     ;@line 369
						FAdd ::temp33 ::temp36 ::temp37                          ;@line 369
						ArrayGetElement ::temp36 matrix 6                        ;@line 369
						ArrayGetElement ::temp37 matrix 8                        ;@line 369
						FMultiply ::temp36 ::temp36 ::temp37                     ;@line 369
						FAdd ::temp37 ::temp33 ::temp36                          ;@line 369
						Assign ac ::temp37                                       ;@line 369
						ArrayGetElement ::temp33 matrix 1                        ;@line 370
						ArrayGetElement ::temp36 matrix 2                        ;@line 370
						FMultiply ::temp37 ::temp33 ::temp36                     ;@line 370
						ArrayGetElement ::temp33 matrix 4                        ;@line 370
						ArrayGetElement ::temp36 matrix 5                        ;@line 370
						FMultiply ::temp33 ::temp33 ::temp36                     ;@line 370
						FAdd ::temp36 ::temp37 ::temp33                          ;@line 370
						ArrayGetElement ::temp37 matrix 7                        ;@line 370
						ArrayGetElement ::temp33 matrix 8                        ;@line 370
						FMultiply ::temp37 ::temp37 ::temp33                     ;@line 370
						FAdd ::temp33 ::temp36 ::temp37                          ;@line 370
						Assign bc ::temp33                                       ;@line 370
						ArrayGetElement ::temp36 matrix 0                        ;@line 371
						ArrayGetElement ::temp37 matrix 4                        ;@line 371
						ArrayGetElement ::temp33 matrix 8                        ;@line 371
						FMultiply ::temp37 ::temp37 ::temp33                     ;@line 371
						ArrayGetElement ::temp33 matrix 5                        ;@line 371
						ArrayGetElement ::temp38 matrix 7                        ;@line 371
						FMultiply ::temp33 ::temp33 ::temp38                     ;@line 371
						FSubtract ::temp38 ::temp37 ::temp33                     ;@line 371
						FMultiply ::temp37 ::temp36 ::temp38                     ;@line 371
						ArrayGetElement ::temp33 matrix 1                        ;@line 371
						ArrayGetElement ::temp36 matrix 3                        ;@line 371
						ArrayGetElement ::temp38 matrix 8                        ;@line 371
						FMultiply ::temp36 ::temp36 ::temp38                     ;@line 371
						ArrayGetElement ::temp38 matrix 5                        ;@line 371
						ArrayGetElement ::temp39 matrix 6                        ;@line 371
						FMultiply ::temp38 ::temp38 ::temp39                     ;@line 371
						FSubtract ::temp39 ::temp36 ::temp38                     ;@line 371
						FMultiply ::temp36 ::temp33 ::temp39                     ;@line 371
						FSubtract ::temp38 ::temp37 ::temp36                     ;@line 371
						ArrayGetElement ::temp33 matrix 2                        ;@line 371
						ArrayGetElement ::temp39 matrix 3                        ;@line 371
						ArrayGetElement ::temp37 matrix 7                        ;@line 371
						FMultiply ::temp36 ::temp39 ::temp37                     ;@line 371
						ArrayGetElement ::temp39 matrix 4                        ;@line 371
						ArrayGetElement ::temp37 matrix 6                        ;@line 371
						FMultiply ::temp39 ::temp39 ::temp37                     ;@line 371
						FSubtract ::temp37 ::temp36 ::temp39                     ;@line 371
						FMultiply ::temp36 ::temp33 ::temp37                     ;@line 371
						FAdd ::temp39 ::temp38 ::temp36                          ;@line 371
						Assign determinant ::temp39                              ;@line 371
						FSubtract ::temp33 a 1.000000                            ;@line 372
						CallStatic math Abs ::temp37 ::temp33                    ;@line 372
						CompareLTE ::temp34 ::temp37 0.002000                    ;@line 372
						Cast ::temp34 ::temp34                                   ;@line 372
						JumpF ::temp34 _label176                                 ;@line 372
						FSubtract ::temp38 b 1.000000                            ;@line 372
						CallStatic math Abs ::temp36 ::temp38                    ;@line 372
						CompareLTE ::temp32 ::temp36 0.002000                    ;@line 372
						Cast ::temp34 ::temp32                                   ;@line 372
					_label176:
						Cast ::temp34 ::temp34                                   ;@line 372
						JumpF ::temp34 _label177                                 ;@line 372
						FSubtract ::temp39 c 1.000000                            ;@line 372
						CallStatic math Abs ::temp33 ::temp39                    ;@line 372
						CompareLTE ::temp32 ::temp33 0.002000                    ;@line 372
						Cast ::temp34 ::temp32                                   ;@line 372
					_label177:
						Cast ::temp34 ::temp34                                   ;@line 372
						JumpF ::temp34 _label178                                 ;@line 372
						CallStatic math Abs ::temp37 ab                          ;@line 372
						CompareLTE ::temp32 ::temp37 0.002000                    ;@line 372
						Cast ::temp34 ::temp32                                   ;@line 372
					_label178:
						Cast ::temp34 ::temp34                                   ;@line 372
						JumpF ::temp34 _label179                                 ;@line 372
						CallStatic math Abs ::temp38 ac                          ;@line 372
						CompareLTE ::temp32 ::temp38 0.002000                    ;@line 372
						Cast ::temp34 ::temp32                                   ;@line 372
					_label179:
						Cast ::temp34 ::temp34                                   ;@line 372
						JumpF ::temp34 _label180                                 ;@line 372
						CallStatic math Abs ::temp36 bc                          ;@line 372
						CompareLTE ::temp32 ::temp36 0.002000                    ;@line 372
						Cast ::temp34 ::temp32                                   ;@line 372
					_label180:
						Cast ::temp34 ::temp34                                   ;@line 372
						JumpF ::temp34 _label181                                 ;@line 372
						FSubtract ::temp39 determinant 1.000000                  ;@line 372
						CallStatic math Abs ::temp33 ::temp39                    ;@line 372
						CompareLTE ::temp32 ::temp33 0.004000                    ;@line 372
						Cast ::temp34 ::temp32                                   ;@line 372
					_label181:
						Return ::temp34                                          ;@line 372
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
						CallMethod StopV23 self ::NoneVar                        ;@line 118
					.endCode
				.endFunction
				.function SampleHorizontalTarget
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param target actor
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp115 Bool
						.local ::temp116 Bool
						.local ::temp117 Float
						.local ::temp118 Float
						.local dx Float
						.local dy Float
						.local horizontal Float
						.local wx Float
						.local wy Float
						.local lx Float
						.local ly Float
						.local angle Float
					.endLocalTable
					.code
						CallMethod ValidTarget self ::temp115 target expectedGeneration expectedToken  ;@line 768
						Not ::temp115 ::temp115                                  ;@line 768
						Cast ::temp115 ::temp115                                 ;@line 768
						JumpT ::temp115 _label182                                ;@line 768
						CallMethod ReadPose self ::temp116 expectedGeneration expectedToken  ;@line 768
						Not ::temp116 ::temp116                                  ;@line 768
						Cast ::temp115 ::temp116                                 ;@line 768
					_label182:
						JumpF ::temp115 _label183                                ;@line 768
						Return False                                             ;@line 769
						Jump _label183                                           ;@line 769
					_label183:
						CallMethod GetPositionX target ::temp117                 ;@line 771
						ArrayGetElement ::temp118 muzzlePosition 0               ;@line 771
						FSubtract ::temp117 ::temp117 ::temp118                  ;@line 771
						Assign dx ::temp117                                      ;@line 771
						CallMethod GetPositionY target ::temp118                 ;@line 772
						ArrayGetElement ::temp117 muzzlePosition 1               ;@line 772
						FSubtract ::temp118 ::temp118 ::temp117                  ;@line 772
						Assign dy ::temp118                                      ;@line 772
						FMultiply ::temp117 dx dx                                ;@line 773
						FMultiply ::temp118 dy dy                                ;@line 773
						FAdd ::temp117 ::temp117 ::temp118                       ;@line 773
						CallStatic math Sqrt ::temp118 ::temp117                 ;@line 773
						Assign horizontal ::temp118                              ;@line 773
						CallMethod HorizontalReachable self ::temp116 target horizontal expectedGeneration expectedToken  ;@line 774
						Not ::temp115 ::temp116                                  ;@line 774
						JumpF ::temp115 _label184                                ;@line 774
						Return False                                             ;@line 775
						Jump _label184                                           ;@line 775
					_label184:
						FDivide ::temp117 dx horizontal                          ;@line 777
						Assign wx ::temp117                                      ;@line 777
						FDivide ::temp118 dy horizontal                          ;@line 778
						Assign wy ::temp118                                      ;@line 778
						ArrayGetElement ::temp117 rootWorldMatrix 0              ;@line 779
						FMultiply ::temp118 ::temp117 wx                         ;@line 779
						ArrayGetElement ::temp117 rootWorldMatrix 3              ;@line 779
						FMultiply ::temp117 ::temp117 wy                         ;@line 779
						FAdd ::temp118 ::temp118 ::temp117                       ;@line 779
						Assign lx ::temp118                                      ;@line 779
						ArrayGetElement ::temp117 rootWorldMatrix 1              ;@line 780
						FMultiply ::temp118 ::temp117 wx                         ;@line 780
						ArrayGetElement ::temp117 rootWorldMatrix 4              ;@line 780
						FMultiply ::temp117 ::temp117 wy                         ;@line 780
						FAdd ::temp118 ::temp118 ::temp117                       ;@line 780
						Assign ly ::temp118                                      ;@line 780
						FNegate ::temp117 ly                                     ;@line 781
						CallMethod HeadingFromVector self ::temp118 lx ::temp117 yaw  ;@line 781
						Assign angle ::temp118                                   ;@line 781
						CompareGT ::temp116 angle 180.000000                     ;@line 782
						JumpF ::temp116 _label185                                ;@line 782
						FSubtract ::temp117 angle 360.000000                     ;@line 783
						Assign angle ::temp117                                   ;@line 783
						Jump _label185                                           ;@line 783
					_label185:
						FSubtract ::temp118 ::YawCenter_var ::YawHalfSector_var  ;@line 785
						FAdd ::temp117 ::YawCenter_var ::YawHalfSector_var       ;@line 785
						CallMethod Finite self ::temp115 angle ::temp118 ::temp117  ;@line 785
						Not ::temp116 ::temp115                                  ;@line 785
						Cast ::temp116 ::temp116                                 ;@line 785
						JumpT ::temp116 _label186                                ;@line 785
						CallMethod Current self ::temp115 expectedGeneration expectedToken  ;@line 785
						Not ::temp115 ::temp115                                  ;@line 785
						Cast ::temp116 ::temp115                                 ;@line 785
					_label186:
						JumpF ::temp116 _label187                                ;@line 785
						Return False                                             ;@line 786
						Jump _label187                                           ;@line 786
					_label187:
						Assign desiredYaw angle                                  ;@line 788
						Assign desiredPitch 0.000000                             ;@line 789
						Assign aimX wx                                           ;@line 790
						Assign aimY wy                                           ;@line 791
						Assign aimZ 0.000000                                     ;@line 792
						Assign targetHorizontal horizontal                       ;@line 793
						Return True                                              ;@line 794
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
					.endLocalTable
					.code
						Return None                                              ;@line 354
					.endCode
				.endFunction
				.function VisualTargetValid
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param target actor
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp96 Bool
						.local ::temp97 actor
						.local ::temp98 Bool
						.local ::temp99 ObjectReference
						.local valid Bool
						.local visible Bool
					.endLocalTable
					.code
						CallMethod GuardReady self ::temp96 expectedGeneration expectedToken  ;@line 692
						Not ::temp96 ::temp96                                    ;@line 692
						Cast ::temp96 ::temp96                                   ;@line 692
						JumpT ::temp96 _label188                                 ;@line 692
						Cast ::temp97 None                                       ;@line 692
						CompareEQ ::temp98 target ::temp97                       ;@line 692
						Cast ::temp96 ::temp98                                   ;@line 692
					_label188:
						Cast ::temp96 ::temp96                                   ;@line 692
						JumpT ::temp96 _label189                                 ;@line 692
						CompareEQ ::temp98 target ::Artillero_var                ;@line 692
						Cast ::temp96 ::temp98                                   ;@line 692
					_label189:
						JumpF ::temp96 _label190                                 ;@line 692
						Return False                                             ;@line 693
						Jump _label190                                           ;@line 693
					_label190:
						CallMethod Is3DLoaded target ::temp98                    ;@line 695
						Cast ::temp98 ::temp98                                   ;@line 695
						JumpF ::temp98 _label191                                 ;@line 695
						CallMethod IsDisabled target ::temp96                    ;@line 695
						Not ::temp96 ::temp96                                    ;@line 695
						Cast ::temp98 ::temp96                                   ;@line 695
					_label191:
						Cast ::temp98 ::temp98                                   ;@line 695
						JumpF ::temp98 _label192                                 ;@line 695
						CallMethod IsDead target ::temp96                        ;@line 695
						Not ::temp96 ::temp96                                    ;@line 695
						Cast ::temp98 ::temp96                                   ;@line 695
					_label192:
						Assign valid ::temp98                                    ;@line 695
						Cast ::temp99 target                                     ;@line 696
						CallMethod HasLOS ::Artillero_var ::temp96 ::temp99      ;@line 696
						Assign visible ::temp96                                  ;@line 696
						CallMethod Current self ::temp98 expectedGeneration expectedToken  ;@line 697
						Cast ::temp96 ::temp98                                   ;@line 697
						JumpF ::temp96 _label193                                 ;@line 697
						Cast ::temp96 valid                                      ;@line 697
					_label193:
						Cast ::temp98 ::temp96                                   ;@line 697
						JumpF ::temp98 _label194                                 ;@line 697
						Cast ::temp98 visible                                    ;@line 697
					_label194:
						Return ::temp98                                          ;@line 697
					.endCode
				.endFunction
				.function OnUpdate
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod PumpV23 self ::NoneVar                        ;@line 652
					.endCode
				.endFunction
				.function ChooseVisualTarget
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return actor
					.paramTable
						.param now Float
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp104 actor
						.local ::temp105 Bool
						.local ::temp106 Bool
						.local ::temp107 Float
						.local enemy actor
						.local candidate actor
						.local attempt Int
						.local ::temp108 Float
						.local ::temp109 Float
						.local ::temp110 Int
					.endLocalTable
					.code
						CallMethod GetCombatTarget ::Artillero_var ::temp104     ;@line 725
						Assign enemy ::temp104                                   ;@line 725
						CallMethod ValidTarget self ::temp105 enemy expectedGeneration expectedToken  ;@line 726
						Cast ::temp105 ::temp105                                 ;@line 726
						JumpF ::temp105 _label195                                ;@line 726
						CallMethod SampleVisualTarget self ::temp106 enemy expectedGeneration expectedToken  ;@line 726
						Cast ::temp105 ::temp106                                 ;@line 726
					_label195:
						JumpF ::temp105 _label196                                ;@line 726
						Assign visualTarget enemy                                ;@line 727
						Return enemy                                             ;@line 728
						Jump _label196                                           ;@line 728
					_label196:
						CallMethod SampleVisualTarget self ::temp106 visualTarget expectedGeneration expectedToken  ;@line 730
						JumpF ::temp106 _label197                                ;@line 730
						Return visualTarget                                      ;@line 731
						Jump _label197                                           ;@line 731
					_label197:
						Cast ::temp104 None                                      ;@line 733
						Assign visualTarget ::temp104                            ;@line 733
						CompareLT ::temp105 now visualScanAt                     ;@line 734
						Cast ::temp105 ::temp105                                 ;@line 734
						JumpT ::temp105 _label198                                ;@line 734
						CallMethod Current self ::temp106 expectedGeneration expectedToken  ;@line 734
						Not ::temp106 ::temp106                                  ;@line 734
						Cast ::temp105 ::temp106                                 ;@line 734
					_label198:
						JumpF ::temp105 _label199                                ;@line 734
						Cast ::temp104 None                                      ;@line 735
						Return ::temp104                                         ;@line 735
						Jump _label199                                           ;@line 735
					_label199:
						FAdd ::temp107 now 1.000000                              ;@line 737
						Assign visualScanAt ::temp107                            ;@line 737
						CallStatic game GetPlayer ::temp104                      ;@line 738
						Assign candidate ::temp104                               ;@line 738
						CallMethod SampleVisualTarget self ::temp106 candidate expectedGeneration expectedToken  ;@line 739
						JumpF ::temp106 _label200                                ;@line 739
						Assign visualTarget candidate                            ;@line 740
						Return candidate                                         ;@line 741
						Jump _label200                                           ;@line 741
					_label200:
						Assign attempt 0                                         ;@line 743
					_label204:
						CompareLT ::temp105 attempt 6                            ;@line 744
						Cast ::temp105 ::temp105                                 ;@line 744
						JumpF ::temp105 _label201                                ;@line 744
						CallMethod Current self ::temp106 expectedGeneration expectedToken  ;@line 744
						Cast ::temp105 ::temp106                                 ;@line 744
					_label201:
						JumpF ::temp105 _label202                                ;@line 744
						ArrayGetElement ::temp107 rootPosition 0                 ;@line 745
						ArrayGetElement ::temp108 rootPosition 1                 ;@line 745
						ArrayGetElement ::temp109 rootPosition 2                 ;@line 745
						CallStatic game FindRandomActor ::temp104 ::temp107 ::temp108 ::temp109 6000.000000  ;@line 745
						Assign candidate ::temp104                               ;@line 745
						CallMethod SampleVisualTarget self ::temp106 candidate expectedGeneration expectedToken  ;@line 746
						JumpF ::temp106 _label203                                ;@line 746
						Assign visualTarget candidate                            ;@line 747
						Return candidate                                         ;@line 748
						Jump _label203                                           ;@line 748
					_label203:
						IAdd ::temp110 attempt 1                                 ;@line 750
						Assign attempt ::temp110                                 ;@line 750
						Jump _label204                                           ;@line 750
					_label202:
						Cast ::temp104 None                                      ;@line 752
						Return ::temp104                                         ;@line 752
					.endCode
				.endFunction
				.function RetireStation
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
						.local ::temp1 Bool
						.local ::temp2 Bool
						.local ::temp4 ObjectReference
						.local ::temp3 Bool
					.endLocalTable
					.code
						Assign stationRetired True                               ;@line 142
						CallMethod StopV23 self ::NoneVar                        ;@line 143
						CompareLTE ::temp1 v23Token 0                            ;@line 144
						Cast ::temp1 ::temp1                                     ;@line 144
						JumpT ::temp1 _label205                                  ;@line 144
						CallStatic astraguardnative IsAvailable ::temp2          ;@line 144
						Not ::temp2 ::temp2                                      ;@line 144
						Cast ::temp1 ::temp2                                     ;@line 144
					_label205:
						JumpF ::temp1 _label206                                  ;@line 144
						Not ::temp2 sceneBusy                                    ;@line 145
						Cast ::temp2 ::temp2                                     ;@line 145
						JumpF ::temp2 _label207                                  ;@line 145
						Not ::temp3 pinBusy                                      ;@line 145
						Cast ::temp2 ::temp3                                     ;@line 145
					_label207:
						Return ::temp2                                           ;@line 145
						Jump _label206                                           ;@line 145
					_label206:
						Cast ::temp4 self                                        ;@line 147
						CallStatic astraguardnative EndOperation ::temp3 ::temp4 v23Token  ;@line 147
						Return ::temp3                                           ;@line 147
					.endCode
				.endFunction
				.function StopGuardPose
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param candidate actor
					.endParamTable
					.localTable
					.endLocalTable
					.code
						Return None                                              ;@line 666
					.endCode
				.endFunction
				.function StartGuardPose
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
					.endLocalTable
					.code
						Return False                                             ;@line 678
					.endCode
				.endFunction
				.function InvalidatePlayerLease
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp5 Bool
						.local ::temp6 Int
					.endLocalTable
					.code
						Assign playerReserved False                              ;@line 152
						Assign playerReady False                                 ;@line 153
						Assign playerRestored False                              ;@line 154
						Assign playerLease 0                                     ;@line 155
						CompareLT ::temp5 playerSerial 2000000000                ;@line 156
						JumpF ::temp5 _label208                                  ;@line 156
						IAdd ::temp6 playerSerial 1                              ;@line 157
						Assign playerSerial ::temp6                              ;@line 157
						Jump _label208                                           ;@line 157
					_label208:
					.endCode
				.endFunction
				.function SafeCadenceSeconds
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Float
					.paramTable
					.endParamTable
					.localTable
						.local ::temp19 Bool
					.endLocalTable
					.code
						CallMethod Finite self ::temp19 ::CadenceSeconds_var 2.500000 60.000000  ;@line 236
						Not ::temp19 ::temp19                                    ;@line 236
						JumpF ::temp19 _label209                                 ;@line 236
						Return 2.500000                                          ;@line 237
						Jump _label209                                           ;@line 237
					_label209:
						Return ::CadenceSeconds_var                              ;@line 239
					.endCode
				.endFunction
				.function SampleVisualTarget
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param target actor
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp100 Bool
						.local ::temp101 Bool
						.local ::temp102 Float
						.local ::temp103 Float
						.local dx Float
						.local dy Float
						.local distanceSquared Float
						.local lx Float
						.local ly Float
						.local angle Float
					.endLocalTable
					.code
						CallMethod VisualTargetValid self ::temp100 target expectedGeneration expectedToken  ;@line 701
						Not ::temp100 ::temp100                                  ;@line 701
						Cast ::temp100 ::temp100                                 ;@line 701
						JumpT ::temp100 _label210                                ;@line 701
						CallMethod ReadPose self ::temp101 expectedGeneration expectedToken  ;@line 701
						Not ::temp101 ::temp101                                  ;@line 701
						Cast ::temp100 ::temp101                                 ;@line 701
					_label210:
						JumpF ::temp100 _label211                                ;@line 701
						Return False                                             ;@line 702
						Jump _label211                                           ;@line 702
					_label211:
						CallMethod GetPositionX target ::temp102                 ;@line 704
						ArrayGetElement ::temp103 rootPosition 0                 ;@line 704
						FSubtract ::temp102 ::temp102 ::temp103                  ;@line 704
						Assign dx ::temp102                                      ;@line 704
						CallMethod GetPositionY target ::temp103                 ;@line 705
						ArrayGetElement ::temp102 rootPosition 1                 ;@line 705
						FSubtract ::temp103 ::temp103 ::temp102                  ;@line 705
						Assign dy ::temp103                                      ;@line 705
						FMultiply ::temp102 dx dx                                ;@line 706
						FMultiply ::temp103 dy dy                                ;@line 706
						FAdd ::temp102 ::temp102 ::temp103                       ;@line 706
						Assign distanceSquared ::temp102                         ;@line 706
						CallMethod Current self ::temp101 expectedGeneration expectedToken  ;@line 707
						Not ::temp100 ::temp101                                  ;@line 707
						Cast ::temp100 ::temp100                                 ;@line 707
						JumpT ::temp100 _label212                                ;@line 707
						CallMethod Finite self ::temp101 distanceSquared 6400.000000 36000000.000000  ;@line 707
						Not ::temp101 ::temp101                                  ;@line 707
						Cast ::temp100 ::temp101                                 ;@line 707
					_label212:
						JumpF ::temp100 _label213                                ;@line 707
						Return False                                             ;@line 708
						Jump _label213                                           ;@line 708
					_label213:
						ArrayGetElement ::temp103 rootWorldMatrix 0              ;@line 710
						FMultiply ::temp102 ::temp103 dx                         ;@line 710
						ArrayGetElement ::temp103 rootWorldMatrix 3              ;@line 710
						FMultiply ::temp103 ::temp103 dy                         ;@line 710
						FAdd ::temp102 ::temp102 ::temp103                       ;@line 710
						Assign lx ::temp102                                      ;@line 710
						ArrayGetElement ::temp103 rootWorldMatrix 1              ;@line 711
						FMultiply ::temp102 ::temp103 dx                         ;@line 711
						ArrayGetElement ::temp103 rootWorldMatrix 4              ;@line 711
						FMultiply ::temp103 ::temp103 dy                         ;@line 711
						FAdd ::temp102 ::temp102 ::temp103                       ;@line 711
						Assign ly ::temp102                                      ;@line 711
						FNegate ::temp103 ly                                     ;@line 712
						CallMethod HeadingFromVector self ::temp102 lx ::temp103 yaw  ;@line 712
						Assign angle ::temp102                                   ;@line 712
						CompareGT ::temp101 angle 180.000000                     ;@line 713
						JumpF ::temp101 _label214                                ;@line 713
						FSubtract ::temp103 angle 360.000000                     ;@line 714
						Assign angle ::temp103                                   ;@line 714
						Jump _label214                                           ;@line 714
					_label214:
						CallMethod Finite self ::temp100 ::YawHalfSector_var 1.000000 60.000000  ;@line 716
						Not ::temp101 ::temp100                                  ;@line 716
						Cast ::temp101 ::temp101                                 ;@line 716
						JumpT ::temp101 _label215                                ;@line 716
						FAdd ::temp102 -60.000000 ::YawHalfSector_var            ;@line 716
						FSubtract ::temp103 60.000000 ::YawHalfSector_var        ;@line 716
						CallMethod Finite self ::temp100 ::YawCenter_var ::temp102 ::temp103  ;@line 716
						Not ::temp100 ::temp100                                  ;@line 716
						Cast ::temp101 ::temp100                                 ;@line 716
					_label215:
						Cast ::temp101 ::temp101                                 ;@line 716
						JumpT ::temp101 _label216                                ;@line 716
						FSubtract ::temp102 ::YawCenter_var ::YawHalfSector_var  ;@line 716
						FAdd ::temp103 ::YawCenter_var ::YawHalfSector_var       ;@line 716
						CallMethod Finite self ::temp100 angle ::temp102 ::temp103  ;@line 716
						Not ::temp100 ::temp100                                  ;@line 716
						Cast ::temp101 ::temp100                                 ;@line 716
					_label216:
						Cast ::temp101 ::temp101                                 ;@line 716
						JumpT ::temp101 _label217                                ;@line 716
						CallMethod Current self ::temp100 expectedGeneration expectedToken  ;@line 716
						Not ::temp100 ::temp100                                  ;@line 716
						Cast ::temp101 ::temp100                                 ;@line 716
					_label217:
						JumpF ::temp101 _label218                                ;@line 716
						Return False                                             ;@line 717
						Jump _label218                                           ;@line 717
					_label218:
						Assign desiredYaw angle                                  ;@line 719
						Assign desiredPitch 0.000000                             ;@line 720
						Return True                                              ;@line 721
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
						CompareGT ::temp0 aiCurrentStage 0                       ;@line 126
						JumpF ::temp0 _label219                                  ;@line 126
						Assign destroyed True                                    ;@line 127
						CallMethod StopV23 self ::NoneVar                        ;@line 128
						Jump _label219                                           ;@line 128
					_label219:
					.endCode
				.endFunction
				.function ResolveV23Operator
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return actor
					.paramTable
					.endParamTable
					.localTable
						.local ::temp127 form
						.local ::temp128 ObjectReference
						.local ::temp129 Bool
						.local ::temp132 actor
						.local east ObjectReference
						.local ::temp130 actor
						.local west ObjectReference
						.local ::temp131 actor
					.endLocalTable
					.code
						CallStatic game GetFormFromFile ::temp127 2928 "AstraAsedio_WhiterunTorres.esp"  ;@line 824
						Cast ::temp128 ::temp127                                 ;@line 824
						Assign east ::temp128                                    ;@line 824
						Cast ::temp128 self                                      ;@line 825
						CompareEQ ::temp129 ::temp128 east                       ;@line 825
						JumpF ::temp129 _label220                                ;@line 825
						CallStatic game GetFormFromFile ::temp127 2929 "AstraAsedio_WhiterunTorres.esp"  ;@line 826
						Cast ::temp130 ::temp127                                 ;@line 826
						Return ::temp130                                         ;@line 826
						Jump _label220                                           ;@line 826
					_label220:
						CallStatic game GetFormFromFile ::temp127 2944 "AstraAsedio_WhiterunTorres.esp"  ;@line 828
						Cast ::temp128 ::temp127                                 ;@line 828
						Assign west ::temp128                                    ;@line 828
						Cast ::temp128 self                                      ;@line 829
						CompareEQ ::temp129 ::temp128 west                       ;@line 829
						JumpF ::temp129 _label221                                ;@line 829
						CallStatic game GetFormFromFile ::temp127 2945 "AstraAsedio_WhiterunTorres.esp"  ;@line 830
						Cast ::temp131 ::temp127                                 ;@line 830
						Return ::temp131                                         ;@line 830
						Jump _label221                                           ;@line 830
					_label221:
						Cast ::temp132 None                                      ;@line 832
						Return ::temp132                                         ;@line 832
					.endCode
				.endFunction
				.function EnsureCityPlacement
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param expectedGeneration Int
						.param lease Int
					.endParamTable
					.localTable
						.local ::temp20 Bool
						.local ::temp21 Bool
						.local ::temp22 Bool
					.endLocalTable
					.code
						Cast ::temp20 pinBusy                                    ;@line 246
						JumpT ::temp20 _label222                                 ;@line 246
						Cast ::temp20 sceneBusy                                  ;@line 246
					_label222:
						Cast ::temp20 ::temp20                                   ;@line 246
						JumpT ::temp20 _label223                                 ;@line 246
						CompareEQ ::temp21 generation expectedGeneration         ;@line 246
						Not ::temp21 ::temp21                                    ;@line 246
						Cast ::temp20 ::temp21                                   ;@line 246
					_label223:
						Cast ::temp21 ::temp20                                   ;@line 246
						JumpT ::temp21 _label224                                 ;@line 246
						Cast ::temp21 destroyed                                  ;@line 246
					_label224:
						Cast ::temp20 ::temp21                                   ;@line 246
						JumpT ::temp20 _label225                                 ;@line 246
						Cast ::temp20 stationRetired                             ;@line 246
					_label225:
						JumpF ::temp20 _label226                                 ;@line 246
						Return False                                             ;@line 247
						Jump _label226                                           ;@line 247
					_label226:
						Not ::temp21 ::AllowPlayerTakeover_var                   ;@line 249
						JumpF ::temp21 _label227                                 ;@line 249
						Return True                                              ;@line 250
						Jump _label227                                           ;@line 250
					_label227:
						CompareGT ::temp20 lease 0                               ;@line 252
						JumpF ::temp20 _label228                                 ;@line 252
						CallMethod PlayerLeaseCurrent self ::temp21 lease        ;@line 253
						Return ::temp21                                          ;@line 253
						Jump _label228                                           ;@line 253
					_label228:
						Cast ::temp20 recovering                                 ;@line 255
						JumpF ::temp20 _label229                                 ;@line 255
						Not ::temp20 playerReserved                              ;@line 255
						Cast ::temp20 ::temp20                                   ;@line 255
					_label229:
						Cast ::temp20 ::temp20                                   ;@line 255
						JumpF ::temp20 _label230                                 ;@line 255
						CompareEQ ::temp22 token -1                              ;@line 255
						Cast ::temp20 ::temp22                                   ;@line 255
					_label230:
						Cast ::temp20 ::temp20                                   ;@line 255
						JumpF ::temp20 _label231                                 ;@line 255
						Not ::temp22 faulted                                     ;@line 255
						Cast ::temp20 ::temp22                                   ;@line 255
					_label231:
						Return ::temp20                                          ;@line 255
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
						CallMethod BlockActivation self ::NoneVar True           ;@line 133
					.endCode
				.endFunction
				.function Shutdown
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod StopV23 self ::NoneVar                        ;@line 263
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
						.local ::temp25 Bool
						.local valid Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod Current self ::temp25 expectedGeneration expectedToken  ;@line 296
						Assign valid ::temp25                                    ;@line 296
						Not ::temp25 valid                                       ;@line 297
						JumpF ::temp25 _label232                                 ;@line 297
						CallMethod RestoreNeutralScene self ::NoneVar            ;@line 298
						Jump _label232                                           ;@line 298
					_label232:
						Assign sceneBusy False                                   ;@line 300
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 301
						Return valid                                             ;@line 302
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
					.endLocalTable
					.code
						Return False                                             ;@line 138
					.endCode
				.endFunction
				.function BeginRecovery
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod StartV23 self ::NoneVar                       ;@line 259
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
						.local ::temp71 actor
						.local ::temp72 Bool
						.local ::temp73 Bool
						.local ::temp74 Float
						.local ::temp75 Float
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
						.local ::temp76 Bool
						.local ::temp77 Int
					.endLocalTable
					.code
						CallStatic game GetPlayer ::temp71                       ;@line 503
						Assign player ::temp71                                   ;@line 503
						CallMethod Current self ::temp72 expectedGeneration expectedToken  ;@line 504
						Not ::temp72 ::temp72                                    ;@line 504
						Cast ::temp72 ::temp72                                   ;@line 504
						JumpT ::temp72 _label233                                 ;@line 504
						Cast ::temp71 None                                       ;@line 504
						CompareEQ ::temp73 player ::temp71                       ;@line 504
						Cast ::temp72 ::temp73                                   ;@line 504
					_label233:
						JumpF ::temp72 _label234                                 ;@line 504
						Return False                                             ;@line 505
						Jump _label234                                           ;@line 505
					_label234:
						CallMethod Is3DLoaded player ::temp73                    ;@line 507
						Assign playerLoaded ::temp73                             ;@line 507
						CallMethod GetPositionX player ::temp74                  ;@line 508
						Assign px ::temp74                                       ;@line 508
						CallMethod GetPositionY player ::temp74                  ;@line 509
						Assign py ::temp74                                       ;@line 509
						CallMethod GetPositionZ player ::temp74                  ;@line 510
						Assign pz ::temp74                                       ;@line 510
						CallMethod GetHeight player ::temp74                     ;@line 511
						Assign height ::temp74                                   ;@line 511
						CallMethod Current self ::temp72 expectedGeneration expectedToken  ;@line 512
						Not ::temp73 ::temp72                                    ;@line 512
						Cast ::temp73 ::temp73                                   ;@line 512
						JumpT ::temp73 _label235                                 ;@line 512
						Not ::temp72 playerLoaded                                ;@line 512
						Cast ::temp73 ::temp72                                   ;@line 512
					_label235:
						Cast ::temp73 ::temp73                                   ;@line 512
						JumpT ::temp73 _label236                                 ;@line 512
						CallMethod Finite self ::temp72 px -1000000.000000 1000000.000000  ;@line 512
						Not ::temp72 ::temp72                                    ;@line 512
						Cast ::temp73 ::temp72                                   ;@line 512
					_label236:
						Cast ::temp73 ::temp73                                   ;@line 512
						JumpT ::temp73 _label237                                 ;@line 512
						CallMethod Finite self ::temp72 py -1000000.000000 1000000.000000  ;@line 512
						Not ::temp72 ::temp72                                    ;@line 512
						Cast ::temp73 ::temp72                                   ;@line 512
					_label237:
						Cast ::temp73 ::temp73                                   ;@line 512
						JumpT ::temp73 _label238                                 ;@line 512
						CallMethod Finite self ::temp72 pz -1000000.000000 1000000.000000  ;@line 512
						Not ::temp72 ::temp72                                    ;@line 512
						Cast ::temp73 ::temp72                                   ;@line 512
					_label238:
						Cast ::temp73 ::temp73                                   ;@line 512
						JumpT ::temp73 _label239                                 ;@line 512
						CallMethod Finite self ::temp72 height 1.000000 512.000000  ;@line 512
						Not ::temp72 ::temp72                                    ;@line 512
						Cast ::temp73 ::temp72                                   ;@line 512
					_label239:
						JumpF ::temp73 _label240                                 ;@line 512
						Return False                                             ;@line 513
						Jump _label240                                           ;@line 513
					_label240:
						CompareLT ::temp72 height 128.000000                     ;@line 515
						JumpF ::temp72 _label241                                 ;@line 515
						Assign height 128.000000                                 ;@line 516
						Jump _label241                                           ;@line 516
					_label241:
						FAdd ::temp74 height 64.000000                           ;@line 518
						Assign height ::temp74                                   ;@line 518
						FDivide ::temp74 height 8.000000                         ;@line 523
						FAdd ::temp74 80.000000 ::temp74                         ;@line 523
						Assign radius ::temp74                                   ;@line 523
						ArrayGetElement ::temp74 muzzleWorldMatrix 1             ;@line 524
						Assign bx ::temp74                                       ;@line 524
						ArrayGetElement ::temp74 muzzleWorldMatrix 4             ;@line 525
						Assign by ::temp74                                       ;@line 525
						ArrayGetElement ::temp74 muzzleWorldMatrix 7             ;@line 526
						Assign bz ::temp74                                       ;@line 526
						FMultiply ::temp74 bx bx                                 ;@line 527
						FMultiply ::temp75 by by                                 ;@line 527
						FAdd ::temp74 ::temp74 ::temp75                          ;@line 527
						CallStatic math Sqrt ::temp75 ::temp74                   ;@line 527
						Assign boreHorizontal ::temp75                           ;@line 527
						CompareLT ::temp73 boreHorizontal 0.010000               ;@line 528
						JumpF ::temp73 _label242                                 ;@line 528
						Return False                                             ;@line 529
						Jump _label242                                           ;@line 529
					_label242:
						FMultiply ::temp74 ::ProjectileSpeed_var boreHorizontal  ;@line 531
						FDivide ::temp75 targetHorizontal ::temp74               ;@line 531
						Assign totalTime ::temp75                                ;@line 531
						CallMethod Finite self ::temp72 totalTime 0.000010 30.000000  ;@line 532
						Not ::temp73 ::temp72                                    ;@line 532
						JumpF ::temp73 _label243                                 ;@line 532
						Return False                                             ;@line 533
						Jump _label243                                           ;@line 533
					_label243:
						ArrayGetElement ::temp74 muzzlePosition 0                ;@line 535
						Assign ax ::temp74                                       ;@line 535
						ArrayGetElement ::temp75 muzzlePosition 1                ;@line 536
						Assign ay ::temp75                                       ;@line 536
						ArrayGetElement ::temp74 muzzlePosition 2                ;@line 537
						Assign az ::temp74                                       ;@line 537
						Assign step 1                                            ;@line 538
					_label248:
						CompareLTE ::temp72 step 8                               ;@line 539
						JumpF ::temp72 _label244                                 ;@line 539
						Cast ::temp75 step                                       ;@line 540
						FMultiply ::temp74 totalTime ::temp75                    ;@line 540
						FDivide ::temp75 ::temp74 8.000000                       ;@line 540
						Assign t ::temp75                                        ;@line 540
						ArrayGetElement ::temp74 muzzlePosition 0                ;@line 541
						FMultiply ::temp75 bx ::ProjectileSpeed_var              ;@line 541
						FMultiply ::temp75 ::temp75 t                            ;@line 541
						FAdd ::temp74 ::temp74 ::temp75                          ;@line 541
						Assign ex ::temp74                                       ;@line 541
						ArrayGetElement ::temp75 muzzlePosition 1                ;@line 542
						FMultiply ::temp74 by ::ProjectileSpeed_var              ;@line 542
						FMultiply ::temp74 ::temp74 t                            ;@line 542
						FAdd ::temp75 ::temp75 ::temp74                          ;@line 542
						Assign ey ::temp75                                       ;@line 542
						ArrayGetElement ::temp74 muzzlePosition 2                ;@line 543
						FMultiply ::temp75 bz ::ProjectileSpeed_var              ;@line 543
						FMultiply ::temp75 ::temp75 t                            ;@line 543
						FAdd ::temp74 ::temp74 ::temp75                          ;@line 543
						FMultiply ::temp75 0.500000 ::ProjectileGravity_var      ;@line 543
						FMultiply ::temp75 ::temp75 t                            ;@line 543
						FMultiply ::temp75 ::temp75 t                            ;@line 543
						FSubtract ::temp74 ::temp74 ::temp75                     ;@line 543
						Assign ez ::temp74                                       ;@line 543
						Assign sample 0                                          ;@line 544
					_label247:
						CompareLTE ::temp73 sample 4                             ;@line 545
						JumpF ::temp73 _label245                                 ;@line 545
						Cast ::temp75 sample                                     ;@line 546
						FMultiply ::temp74 height ::temp75                       ;@line 546
						FDivide ::temp75 ::temp74 4.000000                       ;@line 546
						FAdd ::temp74 pz ::temp75                                ;@line 546
						CallMethod PointNearSegment self ::temp76 px py ::temp74 ax ay az ex ey ez radius  ;@line 546
						JumpF ::temp76 _label246                                 ;@line 546
						Return False                                             ;@line 547
						Jump _label246                                           ;@line 547
					_label246:
						IAdd ::temp77 sample 1                                   ;@line 549
						Assign sample ::temp77                                   ;@line 549
						Jump _label247                                           ;@line 549
					_label245:
						Assign ax ex                                             ;@line 551
						Assign ay ey                                             ;@line 552
						Assign az ez                                             ;@line 553
						IAdd ::temp77 step 1                                     ;@line 554
						Assign step ::temp77                                     ;@line 554
						Jump _label248                                           ;@line 554
					_label244:
						CallMethod Current self ::temp76 expectedGeneration expectedToken  ;@line 556
						Return ::temp76                                          ;@line 556
					.endCode
				.endFunction
				.function FinishGuardEffect
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param candidate actor
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
					.endLocalTable
					.code
						Return False                                             ;@line 673
					.endCode
				.endFunction
				.function LoadGuardAnimation
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
					.localTable
						.local ::temp90 form
						.local ::temp91 Faction
						.local ::temp92 Idle
						.local ::temp93 Int
						.local ::temp94 Bool
						.local ::temp95 Bool
					.endLocalTable
					.code
						CallStatic game GetFormFromFile ::temp90 2048 "AstraAsedio_GuardAnim.esp"  ;@line 657
						Cast ::temp91 ::temp90                                   ;@line 657
						Assign poseFaction ::temp91                              ;@line 657
						CallStatic game GetFormFromFile ::temp90 2049 "AstraAsedio_GuardAnim.esp"  ;@line 658
						Cast ::temp91 ::temp90                                   ;@line 658
						Assign fireFaction ::temp91                              ;@line 658
						CallStatic game GetFormFromFile ::temp90 2050 "AstraAsedio_GuardAnim.esp"  ;@line 659
						Cast ::temp92 ::temp90                                   ;@line 659
						Assign holdIdle ::temp92                                 ;@line 659
						CallStatic game GetFormFromFile ::temp90 2051 "AstraAsedio_GuardAnim.esp"  ;@line 660
						Cast ::temp92 ::temp90                                   ;@line 660
						Assign exitIdle ::temp92                                 ;@line 660
						CallStatic skse GetPluginVersion ::temp93 "OpenAnimationReplacer"  ;@line 661
						CompareGTE ::temp94 ::temp93 0                           ;@line 661
						Cast ::temp94 ::temp94                                   ;@line 661
						JumpF ::temp94 _label249                                 ;@line 661
						Cast ::temp91 None                                       ;@line 661
						CompareEQ ::temp95 poseFaction ::temp91                  ;@line 661
						Not ::temp95 ::temp95                                    ;@line 661
						Cast ::temp94 ::temp95                                   ;@line 661
					_label249:
						Cast ::temp94 ::temp94                                   ;@line 661
						JumpF ::temp94 _label250                                 ;@line 661
						Cast ::temp91 None                                       ;@line 661
						CompareEQ ::temp95 fireFaction ::temp91                  ;@line 661
						Not ::temp95 ::temp95                                    ;@line 661
						Cast ::temp94 ::temp95                                   ;@line 661
					_label250:
						Cast ::temp94 ::temp94                                   ;@line 661
						JumpF ::temp94 _label251                                 ;@line 661
						Cast ::temp92 None                                       ;@line 661
						CompareEQ ::temp95 holdIdle ::temp92                     ;@line 661
						Not ::temp95 ::temp95                                    ;@line 661
						Cast ::temp94 ::temp95                                   ;@line 661
					_label251:
						Cast ::temp94 ::temp94                                   ;@line 661
						JumpF ::temp94 _label252                                 ;@line 661
						Cast ::temp92 None                                       ;@line 661
						CompareEQ ::temp95 exitIdle ::temp92                     ;@line 661
						Not ::temp95 ::temp95                                    ;@line 661
						Cast ::temp94 ::temp95                                   ;@line 661
					_label252:
						Return ::temp94                                          ;@line 661
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
						.local ::temp67 Float
						.local ::temp68 Float
						.local ::temp69 Bool
						.local ::temp70 Bool
						.local dx Float
						.local dy Float
						.local dz Float
						.local lengthSquared Float
						.local along Float
					.endLocalTable
					.code
						FSubtract ::temp67 bx ax                                 ;@line 483
						Assign dx ::temp67                                       ;@line 483
						FSubtract ::temp67 by ay                                 ;@line 484
						Assign dy ::temp67                                       ;@line 484
						FSubtract ::temp67 bz az                                 ;@line 485
						Assign dz ::temp67                                       ;@line 485
						FMultiply ::temp67 dx dx                                 ;@line 486
						FMultiply ::temp68 dy dy                                 ;@line 486
						FAdd ::temp67 ::temp67 ::temp68                          ;@line 486
						FMultiply ::temp68 dz dz                                 ;@line 486
						FAdd ::temp67 ::temp67 ::temp68                          ;@line 486
						Assign lengthSquared ::temp67                            ;@line 486
						CompareLTE ::temp69 lengthSquared 0.000010               ;@line 487
						JumpF ::temp69 _label253                                 ;@line 487
						Return True                                              ;@line 488
						Jump _label253                                           ;@line 488
					_label253:
						FSubtract ::temp68 px ax                                 ;@line 490
						FMultiply ::temp67 ::temp68 dx                           ;@line 490
						FSubtract ::temp68 py ay                                 ;@line 490
						FMultiply ::temp68 ::temp68 dy                           ;@line 490
						FAdd ::temp67 ::temp67 ::temp68                          ;@line 490
						FSubtract ::temp68 pz az                                 ;@line 490
						FMultiply ::temp68 ::temp68 dz                           ;@line 490
						FAdd ::temp67 ::temp67 ::temp68                          ;@line 490
						FDivide ::temp68 ::temp67 lengthSquared                  ;@line 490
						Assign along ::temp68                                    ;@line 490
						CompareLT ::temp69 along 0.000000                        ;@line 491
						JumpF ::temp69 _label254                                 ;@line 491
						Assign along 0.000000                                    ;@line 492
						Jump _label255                                           ;@line 492
					_label254:
						CompareGT ::temp70 along 1.000000                        ;@line 493
						JumpF ::temp70 _label255                                 ;@line 493
						Assign along 1.000000                                    ;@line 494
						Jump _label255                                           ;@line 494
					_label255:
						FMultiply ::temp67 along dx                              ;@line 496
						FAdd ::temp68 ax ::temp67                                ;@line 496
						FSubtract ::temp67 px ::temp68                           ;@line 496
						Assign dx ::temp67                                       ;@line 496
						FMultiply ::temp68 along dy                              ;@line 497
						FAdd ::temp67 ay ::temp68                                ;@line 497
						FSubtract ::temp68 py ::temp67                           ;@line 497
						Assign dy ::temp68                                       ;@line 497
						FMultiply ::temp67 along dz                              ;@line 498
						FAdd ::temp68 az ::temp67                                ;@line 498
						FSubtract ::temp67 pz ::temp68                           ;@line 498
						Assign dz ::temp67                                       ;@line 498
						FMultiply ::temp68 dx dx                                 ;@line 499
						FMultiply ::temp67 dy dy                                 ;@line 499
						FAdd ::temp68 ::temp68 ::temp67                          ;@line 499
						FMultiply ::temp67 dz dz                                 ;@line 499
						FAdd ::temp68 ::temp68 ::temp67                          ;@line 499
						FMultiply ::temp67 radius radius                         ;@line 499
						CompareLTE ::temp70 ::temp68 ::temp67                    ;@line 499
						Return ::temp70                                          ;@line 499
					.endCode
				.endFunction
				.function HorizontalReachable
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param target actor
						.param horizontal Float
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
						.local ::temp111 Bool
						.local ::temp112 Bool
						.local ::temp113 Float
						.local ::temp114 Float
						.local baseZ Float
						.local height Float
						.local travel Float
						.local boltZ Float
						.local validHeights Bool
					.endLocalTable
					.code
						CallMethod Current self ::temp111 expectedGeneration expectedToken  ;@line 756
						Not ::temp111 ::temp111                                  ;@line 756
						Cast ::temp111 ::temp111                                 ;@line 756
						JumpT ::temp111 _label256                                ;@line 756
						CallMethod Finite self ::temp112 horizontal 80.000000 6000.000000  ;@line 756
						Not ::temp112 ::temp112                                  ;@line 756
						Cast ::temp111 ::temp112                                 ;@line 756
					_label256:
						Cast ::temp111 ::temp111                                 ;@line 756
						JumpT ::temp111 _label257                                ;@line 756
						CallMethod Finite self ::temp112 ::ProjectileSpeed_var 1.000000 100000.000000  ;@line 756
						Not ::temp112 ::temp112                                  ;@line 756
						Cast ::temp111 ::temp112                                 ;@line 756
					_label257:
						Cast ::temp111 ::temp111                                 ;@line 756
						JumpT ::temp111 _label258                                ;@line 756
						CallMethod Finite self ::temp112 ::ProjectileGravity_var 0.000000 5000.000000  ;@line 756
						Not ::temp112 ::temp112                                  ;@line 756
						Cast ::temp111 ::temp112                                 ;@line 756
					_label258:
						JumpF ::temp111 _label259                                ;@line 756
						Return False                                             ;@line 757
						Jump _label259                                           ;@line 757
					_label259:
						CallMethod GetPositionZ target ::temp113                 ;@line 759
						Assign baseZ ::temp113                                   ;@line 759
						CallMethod GetHeight target ::temp113                    ;@line 760
						Assign height ::temp113                                  ;@line 760
						FDivide ::temp113 horizontal ::ProjectileSpeed_var       ;@line 761
						Assign travel ::temp113                                  ;@line 761
						ArrayGetElement ::temp113 muzzlePosition 2               ;@line 762
						FMultiply ::temp114 0.500000 ::ProjectileGravity_var     ;@line 762
						FMultiply ::temp114 ::temp114 travel                     ;@line 762
						FMultiply ::temp114 ::temp114 travel                     ;@line 762
						FSubtract ::temp113 ::temp113 ::temp114                  ;@line 762
						Assign boltZ ::temp113                                   ;@line 762
						CallMethod Finite self ::temp112 baseZ -1000000.000000 1000000.000000  ;@line 763
						Cast ::temp112 ::temp112                                 ;@line 763
						JumpF ::temp112 _label260                                ;@line 763
						CallMethod Finite self ::temp111 height 24.000000 8192.000000  ;@line 763
						Cast ::temp112 ::temp111                                 ;@line 763
					_label260:
						Assign validHeights ::temp112                            ;@line 763
						CallMethod Current self ::temp111 expectedGeneration expectedToken  ;@line 764
						Cast ::temp112 ::temp111                                 ;@line 764
						JumpF ::temp112 _label261                                ;@line 764
						Cast ::temp112 validHeights                              ;@line 764
					_label261:
						Cast ::temp112 ::temp112                                 ;@line 764
						JumpF ::temp112 _label262                                ;@line 764
						FAdd ::temp114 baseZ 8.000000                            ;@line 764
						CompareGTE ::temp111 boltZ ::temp114                     ;@line 764
						Cast ::temp112 ::temp111                                 ;@line 764
					_label262:
						Cast ::temp112 ::temp112                                 ;@line 764
						JumpF ::temp112 _label263                                ;@line 764
						FAdd ::temp113 baseZ height                              ;@line 764
						FSubtract ::temp114 ::temp113 8.000000                   ;@line 764
						CompareLTE ::temp111 boltZ ::temp114                     ;@line 764
						Cast ::temp112 ::temp111                                 ;@line 764
					_label263:
						Return ::temp112                                         ;@line 764
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
						.local ::temp78 Bool
						.local ::temp79 Float
						.local ::temp80 Float
						.local ::temp81 Bool
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
						CallMethod SampleTarget self ::temp78 target expectedGeneration expectedToken  ;@line 560
						Not ::temp78 ::temp78                                    ;@line 560
						JumpF ::temp78 _label264                                 ;@line 560
						Return False                                             ;@line 561
						Jump _label264                                           ;@line 561
					_label264:
						CallStatic math Cos ::temp79 yaw                         ;@line 564
						Assign yc ::temp79                                       ;@line 564
						CallStatic math Sin ::temp79 yaw                         ;@line 565
						Assign ys ::temp79                                       ;@line 565
						CallStatic math Cos ::temp79 pitch                       ;@line 566
						Assign pc ::temp79                                       ;@line 566
						CallStatic math Sin ::temp79 pitch                       ;@line 567
						Assign ps ::temp79                                       ;@line 567
						FMultiply ::temp79 ys pc                                 ;@line 568
						Assign lx ::temp79                                       ;@line 568
						FNegate ::temp79 yc                                      ;@line 569
						FMultiply ::temp79 ::temp79 pc                           ;@line 569
						Assign ly ::temp79                                       ;@line 569
						ArrayGetElement ::temp79 rootWorldMatrix 0               ;@line 570
						FMultiply ::temp79 ::temp79 lx                           ;@line 570
						ArrayGetElement ::temp80 rootWorldMatrix 1               ;@line 570
						FMultiply ::temp80 ::temp80 ly                           ;@line 570
						FAdd ::temp79 ::temp79 ::temp80                          ;@line 570
						ArrayGetElement ::temp80 rootWorldMatrix 2               ;@line 570
						FMultiply ::temp80 ::temp80 ps                           ;@line 570
						FAdd ::temp79 ::temp79 ::temp80                          ;@line 570
						Assign wx ::temp79                                       ;@line 570
						ArrayGetElement ::temp80 rootWorldMatrix 3               ;@line 571
						FMultiply ::temp79 ::temp80 lx                           ;@line 571
						ArrayGetElement ::temp80 rootWorldMatrix 4               ;@line 571
						FMultiply ::temp80 ::temp80 ly                           ;@line 571
						FAdd ::temp79 ::temp79 ::temp80                          ;@line 571
						ArrayGetElement ::temp80 rootWorldMatrix 5               ;@line 571
						FMultiply ::temp80 ::temp80 ps                           ;@line 571
						FAdd ::temp79 ::temp79 ::temp80                          ;@line 571
						Assign wy ::temp79                                       ;@line 571
						ArrayGetElement ::temp80 rootWorldMatrix 6               ;@line 572
						FMultiply ::temp79 ::temp80 lx                           ;@line 572
						ArrayGetElement ::temp80 rootWorldMatrix 7               ;@line 572
						FMultiply ::temp80 ::temp80 ly                           ;@line 572
						FAdd ::temp79 ::temp79 ::temp80                          ;@line 572
						ArrayGetElement ::temp80 rootWorldMatrix 8               ;@line 572
						FMultiply ::temp80 ::temp80 ps                           ;@line 572
						FAdd ::temp79 ::temp79 ::temp80                          ;@line 572
						Assign wz ::temp79                                       ;@line 572
						ArrayGetElement ::temp80 muzzleWorldMatrix 1             ;@line 573
						FMultiply ::temp79 wx ::temp80                           ;@line 573
						ArrayGetElement ::temp80 muzzleWorldMatrix 4             ;@line 573
						FMultiply ::temp80 wy ::temp80                           ;@line 573
						FAdd ::temp79 ::temp79 ::temp80                          ;@line 573
						ArrayGetElement ::temp80 muzzleWorldMatrix 7             ;@line 573
						FMultiply ::temp80 wz ::temp80                           ;@line 573
						FAdd ::temp79 ::temp79 ::temp80                          ;@line 573
						Assign poseDot ::temp79                                  ;@line 573
						ArrayGetElement ::temp80 muzzleWorldMatrix 1             ;@line 574
						FMultiply ::temp79 aimX ::temp80                         ;@line 574
						ArrayGetElement ::temp80 muzzleWorldMatrix 4             ;@line 574
						FMultiply ::temp80 aimY ::temp80                         ;@line 574
						FAdd ::temp79 ::temp79 ::temp80                          ;@line 574
						ArrayGetElement ::temp80 muzzleWorldMatrix 7             ;@line 574
						FMultiply ::temp80 aimZ ::temp80                         ;@line 574
						FAdd ::temp79 ::temp79 ::temp80                          ;@line 574
						Assign targetDot ::temp79                                ;@line 574
						CallMethod Finite self ::temp78 poseDot 0.999950 1.002000  ;@line 575
						Not ::temp78 ::temp78                                    ;@line 575
						Cast ::temp78 ::temp78                                   ;@line 575
						JumpT ::temp78 _label265                                 ;@line 575
						CallMethod Finite self ::temp81 targetDot 0.999950 1.002000  ;@line 575
						Not ::temp81 ::temp81                                    ;@line 575
						Cast ::temp78 ::temp81                                   ;@line 575
					_label265:
						Cast ::temp78 ::temp78                                   ;@line 575
						JumpT ::temp78 _label266                                 ;@line 575
						CallMethod Current self ::temp81 expectedGeneration expectedToken  ;@line 575
						Not ::temp81 ::temp81                                    ;@line 575
						Cast ::temp78 ::temp81                                   ;@line 575
					_label266:
						JumpF ::temp78 _label267                                 ;@line 575
						Return False                                             ;@line 576
						Jump _label267                                           ;@line 576
					_label267:
						CallMethod PlayerClear self ::temp81 expectedGeneration expectedToken  ;@line 578
						Assign clear ::temp81                                    ;@line 578
						CallStatic utility IsInMenuMode ::temp78                 ;@line 579
						Assign menuOpen ::temp78                                 ;@line 579
						CallMethod ValidTarget self ::temp81 target expectedGeneration expectedToken  ;@line 580
						Assign targetValid ::temp81                              ;@line 580
						CallMethod Current self ::temp78 expectedGeneration expectedToken  ;@line 581
						Cast ::temp81 ::temp78                                   ;@line 581
						JumpF ::temp81 _label268                                 ;@line 581
						Cast ::temp81 clear                                      ;@line 581
					_label268:
						Cast ::temp81 ::temp81                                   ;@line 581
						JumpF ::temp81 _label269                                 ;@line 581
						Not ::temp78 menuOpen                                    ;@line 581
						Cast ::temp81 ::temp78                                   ;@line 581
					_label269:
						Cast ::temp78 ::temp81                                   ;@line 581
						JumpF ::temp78 _label270                                 ;@line 581
						Cast ::temp78 targetValid                                ;@line 581
					_label270:
						Return ::temp78                                          ;@line 581
					.endCode
				.endFunction
				.function StartV23
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp119 Int
						.local ::temp120 Bool
						.local ::temp121 Bool
						.local ::NoneVar None
						.local ::temp122 ObjectReference
					.endLocalTable
					.code
						Assign v27WarnedRefs False                               ;@line 798
						Assign v28RetryWaited False                              ;@line 799
						IAdd ::temp119 generation 1                              ;@line 800
						Assign generation ::temp119                              ;@line 800
						Assign running False                                     ;@line 801
						Assign recovering False                                  ;@line 802
						IAdd ::temp119 v23Generation 1                           ;@line 803
						Assign v23Generation ::temp119                           ;@line 803
						Not ::temp120 stationRetired                             ;@line 804
						Cast ::temp120 ::temp120                                 ;@line 804
						JumpF ::temp120 _label271                                ;@line 804
						Not ::temp121 destroyed                                  ;@line 804
						Cast ::temp120 ::temp121                                 ;@line 804
					_label271:
						Assign v23Wanted ::temp120                               ;@line 804
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 805
						CompareGT ::temp121 v23Token 0                           ;@line 806
						Cast ::temp121 ::temp121                                 ;@line 806
						JumpF ::temp121 _label272                                ;@line 806
						CallStatic astraguardnative IsAvailable ::temp120        ;@line 806
						Cast ::temp121 ::temp120                                 ;@line 806
					_label272:
						JumpF ::temp121 _label273                                ;@line 806
						Cast ::temp122 self                                      ;@line 807
						CallStatic astraguardnative EndOperation ::temp120 ::temp122 v23Token  ;@line 807
						Jump _label273                                           ;@line 807
					_label273:
						CallMethod RegisterForSingleUpdate self ::NoneVar 0.200000  ;@line 809
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
						CallMethod StopV23 self ::NoneVar                        ;@line 122
					.endCode
				.endFunction
				.function PrepareShieldV26
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param actorRef actor
						.param expected Int
					.endParamTable
					.localTable
						.local ::temp148 Bool
						.local ::temp149 actor
						.local ::temp150 Bool
						.local ::temp151 armor
						.local shield armor
						.local ::temp152 form
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod V23Current self ::temp148 expected            ;@line 927
						Not ::temp148 ::temp148                                  ;@line 927
						Cast ::temp148 ::temp148                                 ;@line 927
						JumpT ::temp148 _label274                                ;@line 927
						Cast ::temp149 None                                      ;@line 927
						CompareEQ ::temp150 actorRef ::temp149                   ;@line 927
						Cast ::temp148 ::temp150                                 ;@line 927
					_label274:
						Cast ::temp148 ::temp148                                 ;@line 927
						JumpT ::temp148 _label275                                ;@line 927
						CallMethod ResolveV23Operator self ::temp149             ;@line 927
						CompareEQ ::temp150 actorRef ::temp149                   ;@line 927
						Not ::temp150 ::temp150                                  ;@line 927
						Cast ::temp148 ::temp150                                 ;@line 927
					_label275:
						JumpF ::temp148 _label276                                ;@line 927
						Return False                                             ;@line 928
						Jump _label276                                           ;@line 928
					_label276:
						CallMethod GetEquippedShield actorRef ::temp151          ;@line 930
						Assign shield ::temp151                                  ;@line 930
						CallMethod V23Current self ::temp150 expected            ;@line 931
						Not ::temp148 ::temp150                                  ;@line 931
						JumpF ::temp148 _label277                                ;@line 931
						Return False                                             ;@line 932
						Jump _label277                                           ;@line 932
					_label277:
						Cast ::temp151 None                                      ;@line 934
						CompareEQ ::temp150 shield ::temp151                     ;@line 934
						Not ::temp150 ::temp150                                  ;@line 934
						JumpF ::temp150 _label278                                ;@line 934
						Cast ::temp152 shield                                    ;@line 937
						CallMethod UnequipItem actorRef ::NoneVar ::temp152 True True  ;@line 937
						Return False                                             ;@line 938
						Jump _label278                                           ;@line 938
					_label278:
						Return True                                              ;@line 940
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
						.local ::temp61 Float
						.local ::temp62 Bool
						.local ::temp63 Float
						.local ::temp64 Bool
						.local difference Float
					.endLocalTable
					.code
						FSubtract ::temp61 goal value                            ;@line 457
						Assign difference ::temp61                               ;@line 457
						CompareGT ::temp62 difference maximumStep                ;@line 458
						JumpF ::temp62 _label279                                 ;@line 458
						FAdd ::temp61 value maximumStep                          ;@line 459
						Return ::temp61                                          ;@line 459
						Jump _label280                                           ;@line 459
					_label279:
						FNegate ::temp63 maximumStep                             ;@line 460
						CompareLT ::temp64 difference ::temp63                   ;@line 460
						JumpF ::temp64 _label280                                 ;@line 460
						FSubtract ::temp63 value maximumStep                     ;@line 461
						Return ::temp63                                          ;@line 461
						Jump _label280                                           ;@line 461
					_label280:
						Return goal                                              ;@line 463
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
						.local ::temp56 Float
						.local ::temp57 Float
						.local ::temp58 Bool
						.local ::temp59 Bool
						.local horizontal Float
						.local cosine Float
						.local angle Float
					.endLocalTable
					.code
						FMultiply ::temp56 vectorX vectorX                       ;@line 432
						FMultiply ::temp57 vectorY vectorY                       ;@line 432
						FAdd ::temp56 ::temp56 ::temp57                          ;@line 432
						CallStatic math Sqrt ::temp57 ::temp56                   ;@line 432
						Assign horizontal ::temp57                               ;@line 432
						CompareLT ::temp58 horizontal 0.000010                   ;@line 433
						JumpF ::temp58 _label281                                 ;@line 433
						Return fallback                                          ;@line 434
						Jump _label281                                           ;@line 434
					_label281:
						FDivide ::temp56 vectorY horizontal                      ;@line 436
						Assign cosine ::temp56                                   ;@line 436
						CompareGT ::temp58 cosine 1.000000                       ;@line 437
						JumpF ::temp58 _label282                                 ;@line 437
						Assign cosine 1.000000                                   ;@line 438
						Jump _label283                                           ;@line 438
					_label282:
						CompareLT ::temp59 cosine -1.000000                      ;@line 439
						JumpF ::temp59 _label283                                 ;@line 439
						Assign cosine -1.000000                                  ;@line 440
						Jump _label283                                           ;@line 440
					_label283:
						CallStatic math ACos ::temp57 cosine                     ;@line 442
						Assign angle ::temp57                                    ;@line 442
						CompareLT ::temp59 vectorX 0.000000                      ;@line 443
						JumpF ::temp59 _label284                                 ;@line 443
						FSubtract ::temp56 360.000000 angle                      ;@line 444
						Assign angle ::temp56                                    ;@line 444
						Jump _label284                                           ;@line 444
					_label284:
						CompareGTE ::temp58 angle 360.000000                     ;@line 446
						JumpF ::temp58 _label285                                 ;@line 446
						FSubtract ::temp57 angle 360.000000                      ;@line 447
						Assign angle ::temp57                                    ;@line 447
						Jump _label285                                           ;@line 447
					_label285:
						Return angle                                             ;@line 449
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
						.local ::temp89 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod Current self ::temp89 expectedGeneration expectedToken  ;@line 644
						Not ::temp89 ::temp89                                    ;@line 644
						JumpF ::temp89 _label286                                 ;@line 644
						Return None                                              ;@line 645
						Jump _label286                                           ;@line 645
					_label286:
						Assign updating False                                    ;@line 647
						CallMethod RegisterForSingleUpdate self ::NoneVar delay  ;@line 648
					.endCode
				.endFunction
				.function SetGuardFirePose
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param Fire Bool
						.param expectedGeneration Int
						.param expectedToken Int
					.endParamTable
					.localTable
					.endLocalTable
					.code
						Return False                                             ;@line 683
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
						CallMethod StartV23 self ::NoneVar                       ;@line 114
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
						.local ::temp60 Bool
					.endLocalTable
					.code
						CallMethod SampleHorizontalTarget self ::temp60 target expectedGeneration expectedToken  ;@line 453
						Return ::temp60                                          ;@line 453
					.endCode
				.endFunction
				.function NormalizeTimingProperties
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp15 Bool
						.local ::temp18 Float
						.local ::temp16 Bool
						.local ::temp17 Bool
					.endLocalTable
					.code
						CompareLT ::temp15 timingRevision 14                     ;@line 208
						JumpF ::temp15 _label287                                 ;@line 208
						CompareGTE ::temp16 ::FireSeconds_var 0.299990           ;@line 209
						Cast ::temp16 ::temp16                                   ;@line 209
						JumpF ::temp16 _label288                                 ;@line 209
						CompareLTE ::temp17 ::FireSeconds_var 0.300010           ;@line 209
						Cast ::temp16 ::temp17                                   ;@line 209
					_label288:
						JumpF ::temp16 _label289                                 ;@line 209
						Assign ::FireSeconds_var 0.200000                        ;@line 210
						Jump _label289                                           ;@line 210
					_label289:
						CompareGTE ::temp17 ::ReleaseSeconds_var 0.099990        ;@line 212
						Cast ::temp17 ::temp17                                   ;@line 212
						JumpF ::temp17 _label290                                 ;@line 212
						CompareLTE ::temp16 ::ReleaseSeconds_var 0.100010        ;@line 212
						Cast ::temp17 ::temp16                                   ;@line 212
					_label290:
						JumpF ::temp17 _label291                                 ;@line 212
						Assign ::ReleaseSeconds_var 0.066667                     ;@line 213
						Jump _label291                                           ;@line 213
					_label291:
						CompareGTE ::temp16 ::ResetSeconds_var 1.199990          ;@line 215
						Cast ::temp16 ::temp16                                   ;@line 215
						JumpF ::temp16 _label292                                 ;@line 215
						CompareLTE ::temp17 ::ResetSeconds_var 1.200010          ;@line 215
						Cast ::temp16 ::temp17                                   ;@line 215
					_label292:
						JumpF ::temp16 _label293                                 ;@line 215
						Assign ::ResetSeconds_var 0.800000                       ;@line 216
						Jump _label293                                           ;@line 216
					_label293:
						CompareGTE ::temp17 ::CadenceSeconds_var 3.999990        ;@line 218
						Cast ::temp17 ::temp17                                   ;@line 218
						JumpF ::temp17 _label294                                 ;@line 218
						CompareLTE ::temp16 ::CadenceSeconds_var 4.000010        ;@line 218
						Cast ::temp17 ::temp16                                   ;@line 218
					_label294:
						JumpF ::temp17 _label295                                 ;@line 218
						Assign ::CadenceSeconds_var 2.500000                     ;@line 219
						Jump _label295                                           ;@line 219
					_label295:
						Assign timingRevision 14                                 ;@line 221
						Jump _label287                                           ;@line 221
					_label287:
						CallMethod Finite self ::temp16 ::FireSeconds_var 0.200000 2.000000  ;@line 223
						Not ::temp17 ::temp16                                    ;@line 223
						JumpF ::temp17 _label296                                 ;@line 223
						Assign ::FireSeconds_var 0.200000                        ;@line 224
						Jump _label296                                           ;@line 224
					_label296:
						CallMethod Finite self ::temp15 ::ReleaseSeconds_var 0.066667 1.000000  ;@line 226
						Not ::temp16 ::temp15                                    ;@line 226
						Cast ::temp15 ::temp16                                   ;@line 226
						JumpT ::temp15 _label297                                 ;@line 226
						CompareGT ::temp17 ::ReleaseSeconds_var ::FireSeconds_var  ;@line 226
						Cast ::temp15 ::temp17                                   ;@line 226
					_label297:
						JumpF ::temp15 _label298                                 ;@line 226
						Assign ::ReleaseSeconds_var 0.066667                     ;@line 227
						Jump _label298                                           ;@line 227
					_label298:
						CallMethod Finite self ::temp16 ::ResetSeconds_var 0.800000 5.000000  ;@line 229
						Not ::temp17 ::temp16                                    ;@line 229
						JumpF ::temp17 _label299                                 ;@line 229
						Assign ::ResetSeconds_var 0.800000                       ;@line 230
						Jump _label299                                           ;@line 230
					_label299:
						CallMethod SafeCadenceSeconds self ::temp18              ;@line 232
						Assign ::CadenceSeconds_var ::temp18                     ;@line 232
					.endCode
				.endFunction
			.endState
		.endStateTable
	.endObject
.endObjectTable
