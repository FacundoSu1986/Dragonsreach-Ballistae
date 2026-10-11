.info
	.source "AstraAsedioGuard.psc"
	.modifyTime 1791657005 ;Sat Oct 10 15:30:05 2026 Local
	.compileTime 1791657006 ;Sat Oct 10 15:30:06 2026 Local
	.user "AstraAsedio"
	.computer "Build"
.endInfo
.userFlagsRef
	.flag hidden 0	; 0x00000000
	.flag conditional 1	; 0x00000001
.endUserFlagsRef
.objectTable
	.object AstraAsedioGuard ObjectReference
		.userFlags 0	; Flags: 0x00000000
		.docString ""
		.autoState 
		.variableTable
			.variable exitIdle Idle
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable rootWorldMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::ProjectileSpeed_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 5400.000000
			.endVariable
			.variable ::YawCenter_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable yaw Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable guardPoseStarted Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable sceneBusy Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable desiredPitch Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable serial Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable ::Puesto_var ObjectReference
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable shotTarget actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable guardPoseFireAt Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::VisualBoltNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "VIROTE_VISUAL"
			.endVariable
			.variable yawMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable aimY Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1.000000
			.endVariable
			.variable ::PitchMin_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue -20.000000
			.endVariable
			.variable aimZ Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable muzzlePosition Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::PitchNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "CTRL_ELEVACION"
			.endVariable
			.variable recoveryRequested Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::Standby_var ObjectReference
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::FireSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.200000
			.endVariable
			.variable desiredYaw Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable pitchBase Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable updating Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable pinBusy Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable aimX Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable phaseAt Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable playerReady Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::TurnRate_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 30.000000
			.endVariable
			.variable token Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1
			.endVariable
			.variable ::YawNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "CTRL_GIRO_360"
			.endVariable
			.variable guardPoseFiring Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable generation Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable ::TargetHeight_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 60.000000
			.endVariable
			.variable playerLease Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable muzzleWorldMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable holdIdle Idle
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::ShotSound_var sound
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::Launcher_var weapon
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable nextShotAt Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable running Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::AllowPlayerTakeover_var Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable pitchMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable destroyed Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable fireFaction Faction
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ownedGuard actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable matricesReady Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable visualScanAt Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::MuzzleNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "ProjectileNode"
			.endVariable
			.variable ::YawHalfSector_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 60.000000
			.endVariable
			.variable ::Artillero_var actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::ReleaseSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.066667
			.endVariable
			.variable playerReserved Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable recovering Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable yawBase Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable poseFaction Faction
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable stationRetired Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::ResetSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.800000
			.endVariable
			.variable ::ShotAmmo_var ammo
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable playerRestored Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::ProjectileGravity_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 240.345001
			.endVariable
			.variable phase Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable ::CadenceSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 2.500000
			.endVariable
			.variable ::PitchMax_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 45.000000
			.endVariable
			.variable rootPosition Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable targetHorizontal Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable lastTick Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable faulted Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable visualTarget actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable playerSerial Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable pitch Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable timingRevision Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
		.endVariableTable
		.propertyTable
			.property CadenceSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::CadenceSeconds_var
			.endProperty
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
			.property YawNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::YawNode_var
			.endProperty
			.property Artillero actor auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Artillero_var
			.endProperty
			.property VisualBoltNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::VisualBoltNode_var
			.endProperty
			.property ProjectileSpeed Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ProjectileSpeed_var
			.endProperty
			.property YawHalfSector Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::YawHalfSector_var
			.endProperty
			.property Launcher weapon auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Launcher_var
			.endProperty
			.property Puesto ObjectReference auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Puesto_var
			.endProperty
			.property YawCenter Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::YawCenter_var
			.endProperty
			.property Standby ObjectReference auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Standby_var
			.endProperty
			.property ReleaseSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ReleaseSeconds_var
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
			.property TargetHeight Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::TargetHeight_var
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
			.property FireSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::FireSeconds_var
			.endProperty
			.property PitchMax Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchMax_var
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
						.local ::temp13 Bool
						.local ::temp14 ObjectReference
						.local ::temp15 Bool
						.local ::temp16 actor
						.local ::temp17 Int
						.local ::NoneVar None
						.local player actor
						.local lease Int
					.endLocalTable
					.code
						Not ::temp13 ::AllowPlayerTakeover_var                   ;@line 167
						Cast ::temp13 ::temp13                                   ;@line 167
						JumpT ::temp13 _label0                                   ;@line 167
						Cast ::temp13 stationRetired                             ;@line 167
					_label0:
						Cast ::temp13 ::temp13                                   ;@line 167
						JumpT ::temp13 _label1                                   ;@line 167
						Cast ::temp13 destroyed                                  ;@line 167
					_label1:
						Cast ::temp13 ::temp13                                   ;@line 167
						JumpT ::temp13 _label2                                   ;@line 167
						Cast ::temp13 playerReserved                             ;@line 167
					_label2:
						Cast ::temp13 ::temp13                                   ;@line 167
						JumpT ::temp13 _label3                                   ;@line 167
						Cast ::temp14 None                                       ;@line 167
						CompareEQ ::temp15 ::Standby_var ::temp14                ;@line 167
						Cast ::temp13 ::temp15                                   ;@line 167
					_label3:
						Cast ::temp13 ::temp13                                   ;@line 167
						JumpT ::temp13 _label4                                   ;@line 167
						CompareGTE ::temp15 playerSerial 2000000000              ;@line 167
						Cast ::temp13 ::temp15                                   ;@line 167
					_label4:
						JumpF ::temp13 _label5                                   ;@line 167
						Return -1                                                ;@line 168
						Jump _label5                                             ;@line 168
					_label5:
						CallStatic game GetPlayer ::temp16                       ;@line 170
						Assign player ::temp16                                   ;@line 170
						Cast ::temp15 playerReserved                             ;@line 171
						JumpT ::temp15 _label6                                   ;@line 171
						Cast ::temp15 destroyed                                  ;@line 171
					_label6:
						Cast ::temp15 ::temp15                                   ;@line 171
						JumpT ::temp15 _label7                                   ;@line 171
						Not ::temp13 ::AllowPlayerTakeover_var                   ;@line 171
						Cast ::temp15 ::temp13                                   ;@line 171
					_label7:
						Cast ::temp15 ::temp15                                   ;@line 171
						JumpT ::temp15 _label8                                   ;@line 171
						Cast ::temp14 None                                       ;@line 171
						CompareEQ ::temp13 ::Standby_var ::temp14                ;@line 171
						Cast ::temp15 ::temp13                                   ;@line 171
					_label8:
						Cast ::temp15 ::temp15                                   ;@line 171
						JumpT ::temp15 _label9                                   ;@line 171
						CompareEQ ::temp13 ::Artillero_var player                ;@line 171
						Cast ::temp15 ::temp13                                   ;@line 171
					_label9:
						JumpF ::temp15 _label10                                  ;@line 171
						Return -1                                                ;@line 172
						Jump _label10                                            ;@line 172
					_label10:
						IAdd ::temp17 playerSerial 1                             ;@line 174
						Assign playerSerial ::temp17                             ;@line 174
						Assign lease playerSerial                                ;@line 175
						Assign playerLease lease                                 ;@line 176
						Assign playerReserved True                               ;@line 177
						Assign playerReady False                                 ;@line 178
						Assign playerRestored False                              ;@line 179
						CallMethod Shutdown self ::NoneVar                       ;@line 182
						CallMethod PlayerLeaseCurrent self ::temp13 lease        ;@line 183
						Not ::temp15 ::temp13                                    ;@line 183
						JumpF ::temp15 _label11                                  ;@line 183
						Return -1                                                ;@line 184
						Jump _label11                                            ;@line 184
					_label11:
						Return lease                                             ;@line 186
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
						.local ::temp175 Bool
						.local ::temp176 Bool
						.local ::temp177 Float
						.local ::temp178 Float
						.local dx Float
						.local dy Float
						.local distanceSquared Float
						.local lx Float
						.local ly Float
						.local angle Float
					.endLocalTable
					.code
						CallMethod VisualTargetValid self ::temp175 target expectedGeneration expectedToken  ;@line 1387
						Not ::temp175 ::temp175                                  ;@line 1387
						Cast ::temp175 ::temp175                                 ;@line 1387
						JumpT ::temp175 _label12                                 ;@line 1387
						CallMethod ReadPose self ::temp176 expectedGeneration expectedToken  ;@line 1387
						Not ::temp176 ::temp176                                  ;@line 1387
						Cast ::temp175 ::temp176                                 ;@line 1387
					_label12:
						JumpF ::temp175 _label13                                 ;@line 1387
						Return False                                             ;@line 1388
						Jump _label13                                            ;@line 1388
					_label13:
						CallMethod GetPositionX target ::temp177                 ;@line 1390
						ArrayGetElement ::temp178 rootPosition 0                 ;@line 1390
						FSubtract ::temp177 ::temp177 ::temp178                  ;@line 1390
						Assign dx ::temp177                                      ;@line 1390
						CallMethod GetPositionY target ::temp178                 ;@line 1391
						ArrayGetElement ::temp177 rootPosition 1                 ;@line 1391
						FSubtract ::temp178 ::temp178 ::temp177                  ;@line 1391
						Assign dy ::temp178                                      ;@line 1391
						FMultiply ::temp177 dx dx                                ;@line 1392
						FMultiply ::temp178 dy dy                                ;@line 1392
						FAdd ::temp177 ::temp177 ::temp178                       ;@line 1392
						Assign distanceSquared ::temp177                         ;@line 1392
						CallMethod Current self ::temp176 expectedGeneration expectedToken  ;@line 1393
						Not ::temp175 ::temp176                                  ;@line 1393
						Cast ::temp175 ::temp175                                 ;@line 1393
						JumpT ::temp175 _label14                                 ;@line 1393
						CallMethod Finite self ::temp176 distanceSquared 6400.000000 36000000.000000  ;@line 1393
						Not ::temp176 ::temp176                                  ;@line 1393
						Cast ::temp175 ::temp176                                 ;@line 1393
					_label14:
						JumpF ::temp175 _label15                                 ;@line 1393
						Return False                                             ;@line 1394
						Jump _label15                                            ;@line 1394
					_label15:
						ArrayGetElement ::temp178 rootWorldMatrix 0              ;@line 1396
						FMultiply ::temp177 ::temp178 dx                         ;@line 1396
						ArrayGetElement ::temp178 rootWorldMatrix 3              ;@line 1396
						FMultiply ::temp178 ::temp178 dy                         ;@line 1396
						FAdd ::temp177 ::temp177 ::temp178                       ;@line 1396
						Assign lx ::temp177                                      ;@line 1396
						ArrayGetElement ::temp178 rootWorldMatrix 1              ;@line 1397
						FMultiply ::temp177 ::temp178 dx                         ;@line 1397
						ArrayGetElement ::temp178 rootWorldMatrix 4              ;@line 1397
						FMultiply ::temp178 ::temp178 dy                         ;@line 1397
						FAdd ::temp177 ::temp177 ::temp178                       ;@line 1397
						Assign ly ::temp177                                      ;@line 1397
						FNegate ::temp178 ly                                     ;@line 1398
						CallMethod HeadingFromVector self ::temp177 lx ::temp178 yaw  ;@line 1398
						Assign angle ::temp177                                   ;@line 1398
						CompareGT ::temp176 angle 180.000000                     ;@line 1399
						JumpF ::temp176 _label16                                 ;@line 1399
						FSubtract ::temp178 angle 360.000000                     ;@line 1400
						Assign angle ::temp178                                   ;@line 1400
						Jump _label16                                            ;@line 1400
					_label16:
						CallMethod Finite self ::temp175 ::YawHalfSector_var 1.000000 60.000000  ;@line 1402
						Not ::temp176 ::temp175                                  ;@line 1402
						Cast ::temp176 ::temp176                                 ;@line 1402
						JumpT ::temp176 _label17                                 ;@line 1402
						FAdd ::temp177 -60.000000 ::YawHalfSector_var            ;@line 1402
						FSubtract ::temp178 60.000000 ::YawHalfSector_var        ;@line 1402
						CallMethod Finite self ::temp175 ::YawCenter_var ::temp177 ::temp178  ;@line 1402
						Not ::temp175 ::temp175                                  ;@line 1402
						Cast ::temp176 ::temp175                                 ;@line 1402
					_label17:
						Cast ::temp176 ::temp176                                 ;@line 1402
						JumpT ::temp176 _label18                                 ;@line 1402
						FSubtract ::temp177 ::YawCenter_var ::YawHalfSector_var  ;@line 1402
						FAdd ::temp178 ::YawCenter_var ::YawHalfSector_var       ;@line 1402
						CallMethod Finite self ::temp175 angle ::temp177 ::temp178  ;@line 1402
						Not ::temp175 ::temp175                                  ;@line 1402
						Cast ::temp176 ::temp175                                 ;@line 1402
					_label18:
						Cast ::temp176 ::temp176                                 ;@line 1402
						JumpT ::temp176 _label19                                 ;@line 1402
						CallMethod Current self ::temp175 expectedGeneration expectedToken  ;@line 1402
						Not ::temp175 ::temp175                                  ;@line 1402
						Cast ::temp176 ::temp175                                 ;@line 1402
					_label19:
						JumpF ::temp176 _label20                                 ;@line 1402
						Return False                                             ;@line 1403
						Jump _label20                                            ;@line 1403
					_label20:
						Assign desiredYaw angle                                  ;@line 1405
						Assign desiredPitch 0.000000                             ;@line 1406
						Return True                                              ;@line 1407
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
						.local ::temp179 actor
						.local ::temp180 Bool
						.local ::temp181 Bool
						.local ::temp182 Float
						.local enemy actor
						.local candidate actor
						.local attempt Int
						.local ::temp183 Float
						.local ::temp184 Float
						.local ::temp185 Int
					.endLocalTable
					.code
						CallMethod GetCombatTarget ::Artillero_var ::temp179     ;@line 1411
						Assign enemy ::temp179                                   ;@line 1411
						CallMethod ValidTarget self ::temp180 enemy expectedGeneration expectedToken  ;@line 1412
						Cast ::temp180 ::temp180                                 ;@line 1412
						JumpF ::temp180 _label21                                 ;@line 1412
						CallMethod SampleVisualTarget self ::temp181 enemy expectedGeneration expectedToken  ;@line 1412
						Cast ::temp180 ::temp181                                 ;@line 1412
					_label21:
						JumpF ::temp180 _label22                                 ;@line 1412
						Assign visualTarget enemy                                ;@line 1413
						Return enemy                                             ;@line 1414
						Jump _label22                                            ;@line 1414
					_label22:
						CallMethod SampleVisualTarget self ::temp181 visualTarget expectedGeneration expectedToken  ;@line 1416
						JumpF ::temp181 _label23                                 ;@line 1416
						Return visualTarget                                      ;@line 1417
						Jump _label23                                            ;@line 1417
					_label23:
						Cast ::temp179 None                                      ;@line 1419
						Assign visualTarget ::temp179                            ;@line 1419
						CompareLT ::temp180 now visualScanAt                     ;@line 1420
						Cast ::temp180 ::temp180                                 ;@line 1420
						JumpT ::temp180 _label24                                 ;@line 1420
						CallMethod Current self ::temp181 expectedGeneration expectedToken  ;@line 1420
						Not ::temp181 ::temp181                                  ;@line 1420
						Cast ::temp180 ::temp181                                 ;@line 1420
					_label24:
						JumpF ::temp180 _label25                                 ;@line 1420
						Cast ::temp179 None                                      ;@line 1421
						Return ::temp179                                         ;@line 1421
						Jump _label25                                            ;@line 1421
					_label25:
						FAdd ::temp182 now 1.000000                              ;@line 1423
						Assign visualScanAt ::temp182                            ;@line 1423
						CallStatic game GetPlayer ::temp179                      ;@line 1424
						Assign candidate ::temp179                               ;@line 1424
						CallMethod SampleVisualTarget self ::temp181 candidate expectedGeneration expectedToken  ;@line 1425
						JumpF ::temp181 _label26                                 ;@line 1425
						Assign visualTarget candidate                            ;@line 1426
						Return candidate                                         ;@line 1427
						Jump _label26                                            ;@line 1427
					_label26:
						Assign attempt 0                                         ;@line 1429
					_label30:
						CompareLT ::temp180 attempt 6                            ;@line 1430
						Cast ::temp180 ::temp180                                 ;@line 1430
						JumpF ::temp180 _label27                                 ;@line 1430
						CallMethod Current self ::temp181 expectedGeneration expectedToken  ;@line 1430
						Cast ::temp180 ::temp181                                 ;@line 1430
					_label27:
						JumpF ::temp180 _label28                                 ;@line 1430
						ArrayGetElement ::temp182 rootPosition 0                 ;@line 1431
						ArrayGetElement ::temp183 rootPosition 1                 ;@line 1431
						ArrayGetElement ::temp184 rootPosition 2                 ;@line 1431
						CallStatic game FindRandomActor ::temp179 ::temp182 ::temp183 ::temp184 6000.000000  ;@line 1431
						Assign candidate ::temp179                               ;@line 1431
						CallMethod SampleVisualTarget self ::temp181 candidate expectedGeneration expectedToken  ;@line 1432
						JumpF ::temp181 _label29                                 ;@line 1432
						Assign visualTarget candidate                            ;@line 1433
						Return candidate                                         ;@line 1434
						Jump _label29                                            ;@line 1434
					_label29:
						IAdd ::temp185 attempt 1                                 ;@line 1436
						Assign attempt ::temp185                                 ;@line 1436
						Jump _label30                                            ;@line 1436
					_label28:
						Cast ::temp179 None                                      ;@line 1438
						Return ::temp179                                         ;@line 1438
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
						.local ::temp97 Bool
						.local ::temp98 actor
						.local ::temp99 Bool
						.local ::temp100 Int
						.local ::temp101 ObjectReference
						.local player actor
						.local valid Bool
						.local visible Bool
						.local combatTarget actor
					.endLocalTable
					.code
						CallMethod GuardReady self ::temp97 expectedGeneration expectedToken  ;@line 823
						Not ::temp97 ::temp97                                    ;@line 823
						Cast ::temp97 ::temp97                                   ;@line 823
						JumpT ::temp97 _label31                                  ;@line 823
						Cast ::temp98 None                                       ;@line 823
						CompareEQ ::temp99 target ::temp98                       ;@line 823
						Cast ::temp97 ::temp99                                   ;@line 823
					_label31:
						Cast ::temp97 ::temp97                                   ;@line 823
						JumpT ::temp97 _label32                                  ;@line 823
						CompareEQ ::temp99 target ::Artillero_var                ;@line 823
						Cast ::temp97 ::temp99                                   ;@line 823
					_label32:
						JumpF ::temp97 _label33                                  ;@line 823
						Return False                                             ;@line 824
						Jump _label33                                            ;@line 824
					_label33:
						CallStatic game GetPlayer ::temp98                       ;@line 826
						Assign player ::temp98                                   ;@line 826
						CallMethod Current self ::temp99 expectedGeneration expectedToken  ;@line 827
						Not ::temp97 ::temp99                                    ;@line 827
						Cast ::temp97 ::temp97                                   ;@line 827
						JumpT ::temp97 _label34                                  ;@line 827
						CompareEQ ::temp99 target player                         ;@line 827
						Cast ::temp97 ::temp99                                   ;@line 827
					_label34:
						JumpF ::temp97 _label35                                  ;@line 827
						Return False                                             ;@line 828
						Jump _label35                                            ;@line 828
					_label35:
						CallMethod Is3DLoaded target ::temp99                    ;@line 830
						Cast ::temp99 ::temp99                                   ;@line 830
						JumpF ::temp99 _label36                                  ;@line 830
						CallMethod IsDisabled target ::temp97                    ;@line 830
						Not ::temp97 ::temp97                                    ;@line 830
						Cast ::temp99 ::temp97                                   ;@line 830
					_label36:
						Cast ::temp99 ::temp99                                   ;@line 830
						JumpF ::temp99 _label37                                  ;@line 830
						CallMethod IsDead target ::temp97                        ;@line 830
						Not ::temp97 ::temp97                                    ;@line 830
						Cast ::temp99 ::temp97                                   ;@line 830
					_label37:
						Cast ::temp99 ::temp99                                   ;@line 830
						JumpF ::temp99 _label38                                  ;@line 830
						CallMethod IsPlayerTeammate target ::temp97              ;@line 830
						Not ::temp97 ::temp97                                    ;@line 830
						Cast ::temp99 ::temp97                                   ;@line 830
					_label38:
						Cast ::temp99 ::temp99                                   ;@line 830
						JumpF ::temp99 _label39                                  ;@line 830
						CallMethod IsHostileToActor target ::temp97 ::Artillero_var  ;@line 830
						Cast ::temp99 ::temp97                                   ;@line 830
					_label39:
						Cast ::temp99 ::temp99                                   ;@line 830
						JumpF ::temp99 _label40                                  ;@line 830
						CallMethod GetCombatState target ::temp100               ;@line 830
						CompareGT ::temp97 ::temp100 0                           ;@line 830
						Cast ::temp99 ::temp97                                   ;@line 830
					_label40:
						Cast ::temp99 ::temp99                                   ;@line 830
						JumpF ::temp99 _label41                                  ;@line 830
						CallMethod GetCombatState ::Artillero_var ::temp100      ;@line 830
						CompareEQ ::temp97 ::temp100 1                           ;@line 830
						Cast ::temp99 ::temp97                                   ;@line 830
					_label41:
						Assign valid ::temp99                                    ;@line 830
						Cast ::temp101 target                                    ;@line 831
						CallMethod HasLOS ::Artillero_var ::temp97 ::temp101     ;@line 831
						Assign visible ::temp97                                  ;@line 831
						CallMethod GetCombatTarget ::Artillero_var ::temp98      ;@line 832
						Assign combatTarget ::temp98                             ;@line 832
						CallMethod Current self ::temp99 expectedGeneration expectedToken  ;@line 833
						Cast ::temp97 ::temp99                                   ;@line 833
						JumpF ::temp97 _label42                                  ;@line 833
						Cast ::temp97 valid                                      ;@line 833
					_label42:
						Cast ::temp99 ::temp97                                   ;@line 833
						JumpF ::temp99 _label43                                  ;@line 833
						Cast ::temp99 visible                                    ;@line 833
					_label43:
						Cast ::temp99 ::temp99                                   ;@line 833
						JumpF ::temp99 _label44                                  ;@line 833
						CompareEQ ::temp97 combatTarget target                   ;@line 833
						Cast ::temp99 ::temp97                                   ;@line 833
					_label44:
						Return ::temp99                                          ;@line 833
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
						.local ::temp92 Bool
						.local ::temp93 actor
						.local ::temp94 Bool
						.local ::temp95 ObjectReference
						.local ::temp96 Float
						.local ready Bool
						.local distance Float
					.endLocalTable
					.code
						CallMethod Current self ::temp92 expectedGeneration expectedToken  ;@line 814
						Not ::temp92 ::temp92                                    ;@line 814
						Cast ::temp92 ::temp92                                   ;@line 814
						JumpT ::temp92 _label45                                  ;@line 814
						Cast ::temp93 None                                       ;@line 814
						CompareEQ ::temp94 ownedGuard ::temp93                   ;@line 814
						Cast ::temp92 ::temp94                                   ;@line 814
					_label45:
						Cast ::temp92 ::temp92                                   ;@line 814
						JumpT ::temp92 _label46                                  ;@line 814
						CompareEQ ::temp94 ownedGuard ::Artillero_var            ;@line 814
						Not ::temp94 ::temp94                                    ;@line 814
						Cast ::temp92 ::temp94                                   ;@line 814
					_label46:
						JumpF ::temp92 _label47                                  ;@line 814
						Return False                                             ;@line 815
						Jump _label47                                            ;@line 815
					_label47:
						CallMethod Is3DLoaded self ::temp94                      ;@line 817
						Cast ::temp94 ::temp94                                   ;@line 817
						JumpF ::temp94 _label48                                  ;@line 817
						CallMethod IsDisabled self ::temp92                      ;@line 817
						Not ::temp92 ::temp92                                    ;@line 817
						Cast ::temp94 ::temp92                                   ;@line 817
					_label48:
						Cast ::temp94 ::temp94                                   ;@line 817
						JumpF ::temp94 _label49                                  ;@line 817
						CallMethod Is3DLoaded ownedGuard ::temp92                ;@line 817
						Cast ::temp94 ::temp92                                   ;@line 817
					_label49:
						Cast ::temp94 ::temp94                                   ;@line 817
						JumpF ::temp94 _label50                                  ;@line 817
						CallMethod IsDead ownedGuard ::temp92                    ;@line 817
						Not ::temp92 ::temp92                                    ;@line 817
						Cast ::temp94 ::temp92                                   ;@line 817
					_label50:
						Cast ::temp94 ::temp94                                   ;@line 817
						JumpF ::temp94 _label51                                  ;@line 817
						CallMethod IsDisabled ownedGuard ::temp92                ;@line 817
						Not ::temp92 ::temp92                                    ;@line 817
						Cast ::temp94 ::temp92                                   ;@line 817
					_label51:
						Assign ready ::temp94                                    ;@line 817
						Cast ::temp95 self                                       ;@line 818
						CallMethod GetDistance ownedGuard ::temp96 ::temp95      ;@line 818
						Assign distance ::temp96                                 ;@line 818
						CallMethod Current self ::temp92 expectedGeneration expectedToken  ;@line 819
						Cast ::temp94 ::temp92                                   ;@line 819
						JumpF ::temp94 _label52                                  ;@line 819
						Cast ::temp94 ready                                      ;@line 819
					_label52:
						Cast ::temp94 ::temp94                                   ;@line 819
						JumpF ::temp94 _label53                                  ;@line 819
						CallMethod Finite self ::temp92 distance 0.000000 240.000000  ;@line 819
						Cast ::temp94 ::temp92                                   ;@line 819
					_label53:
						Return ::temp94                                          ;@line 819
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
						.local ::temp27 Bool
						.local ::temp28 Bool
					.endLocalTable
					.code
						CompareEQ ::temp27 value value                           ;@line 296
						Cast ::temp27 ::temp27                                   ;@line 296
						JumpF ::temp27 _label54                                  ;@line 296
						CompareGTE ::temp28 value minimum                        ;@line 296
						Cast ::temp27 ::temp28                                   ;@line 296
					_label54:
						Cast ::temp27 ::temp27                                   ;@line 296
						JumpF ::temp27 _label55                                  ;@line 296
						CompareLTE ::temp28 value maximum                        ;@line 296
						Cast ::temp27 ::temp28                                   ;@line 296
					_label55:
						Return ::temp27                                          ;@line 296
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
						.local ::temp26 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod PlayerLeaseCurrent self ::temp26 lease        ;@line 284
						Not ::temp26 ::temp26                                    ;@line 284
						JumpF ::temp26 _label56                                  ;@line 284
						Return False                                             ;@line 285
						Jump _label56                                            ;@line 285
					_label56:
						CallMethod InvalidatePlayerLease self ::NoneVar          ;@line 287
						CallMethod Shutdown self ::NoneVar                       ;@line 288
						CallMethod BeginRecovery self ::NoneVar                  ;@line 291
						Return True                                              ;@line 292
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
						.local ::temp166 Bool
						.local ::temp167 Bool
						.local ::temp168 Float
						.local ::temp169 Float
						.local ::temp170 Float
						.local ::NoneVar None
						.local localX Float
						.local localY Float
						.local px Float
						.local py Float
						.local frontX Float
						.local frontY Float
						.local heading Float
						.local candidate actor
					.endLocalTable
					.code
						Cast ::temp166 pinBusy                                   ;@line 1354
						JumpT ::temp166 _label57                                 ;@line 1354
						CallMethod GuardReady self ::temp166 expectedGeneration expectedToken  ;@line 1354
						Not ::temp166 ::temp166                                  ;@line 1354
						Cast ::temp166 ::temp166                                 ;@line 1354
					_label57:
						Cast ::temp166 ::temp166                                 ;@line 1354
						JumpT ::temp166 _label58                                 ;@line 1354
						CallMethod ReadPose self ::temp167 expectedGeneration expectedToken  ;@line 1354
						Not ::temp167 ::temp167                                  ;@line 1354
						Cast ::temp166 ::temp167                                 ;@line 1354
					_label58:
						JumpF ::temp166 _label59                                 ;@line 1354
						Return False                                             ;@line 1355
						Jump _label59                                            ;@line 1355
					_label59:
						CallStatic math Sin ::temp168 yaw                        ;@line 1358
						FMultiply ::temp168 -151.000000 ::temp168                ;@line 1358
						Assign localX ::temp168                                  ;@line 1358
						CallStatic math Cos ::temp168 yaw                        ;@line 1359
						FMultiply ::temp168 151.000000 ::temp168                 ;@line 1359
						Assign localY ::temp168                                  ;@line 1359
						ArrayGetElement ::temp168 rootPosition 0                 ;@line 1360
						ArrayGetElement ::temp169 rootWorldMatrix 0              ;@line 1360
						FMultiply ::temp169 ::temp169 localX                     ;@line 1360
						FAdd ::temp168 ::temp168 ::temp169                       ;@line 1360
						ArrayGetElement ::temp169 rootWorldMatrix 1              ;@line 1360
						FMultiply ::temp169 ::temp169 localY                     ;@line 1360
						FAdd ::temp168 ::temp168 ::temp169                       ;@line 1360
						Assign px ::temp168                                      ;@line 1360
						ArrayGetElement ::temp169 rootPosition 1                 ;@line 1361
						ArrayGetElement ::temp168 rootWorldMatrix 3              ;@line 1361
						FMultiply ::temp168 ::temp168 localX                     ;@line 1361
						FAdd ::temp169 ::temp169 ::temp168                       ;@line 1361
						ArrayGetElement ::temp168 rootWorldMatrix 4              ;@line 1361
						FMultiply ::temp168 ::temp168 localY                     ;@line 1361
						FAdd ::temp169 ::temp169 ::temp168                       ;@line 1361
						Assign py ::temp169                                      ;@line 1361
						ArrayGetElement ::temp168 rootWorldMatrix 0              ;@line 1362
						CallStatic math Sin ::temp169 yaw                        ;@line 1362
						FMultiply ::temp168 ::temp168 ::temp169                  ;@line 1362
						ArrayGetElement ::temp169 rootWorldMatrix 1              ;@line 1362
						CallStatic math Cos ::temp170 yaw                        ;@line 1362
						FMultiply ::temp169 ::temp169 ::temp170                  ;@line 1362
						FSubtract ::temp170 ::temp168 ::temp169                  ;@line 1362
						Assign frontX ::temp170                                  ;@line 1362
						ArrayGetElement ::temp168 rootWorldMatrix 3              ;@line 1363
						CallStatic math Sin ::temp169 yaw                        ;@line 1363
						FMultiply ::temp170 ::temp168 ::temp169                  ;@line 1363
						ArrayGetElement ::temp168 rootWorldMatrix 4              ;@line 1363
						CallStatic math Cos ::temp169 yaw                        ;@line 1363
						FMultiply ::temp168 ::temp168 ::temp169                  ;@line 1363
						FSubtract ::temp169 ::temp170 ::temp168                  ;@line 1363
						Assign frontY ::temp169                                  ;@line 1363
						CallMethod HeadingFromVector self ::temp170 frontX frontY 0.000000  ;@line 1364
						Assign heading ::temp170                                 ;@line 1364
						CallMethod Current self ::temp167 expectedGeneration expectedToken  ;@line 1365
						Not ::temp166 ::temp167                                  ;@line 1365
						JumpF ::temp166 _label60                                 ;@line 1365
						Return False                                             ;@line 1366
						Jump _label60                                            ;@line 1366
					_label60:
						Assign candidate ownedGuard                              ;@line 1368
						Assign pinBusy True                                      ;@line 1369
						ArrayGetElement ::temp168 rootPosition 2                 ;@line 1370
						CallMethod SetPosition candidate ::NoneVar px py ::temp168  ;@line 1370
						CallMethod Current self ::temp167 expectedGeneration expectedToken  ;@line 1371
						JumpF ::temp167 _label61                                 ;@line 1371
						CallMethod SetAngle candidate ::NoneVar 0.000000 0.000000 heading  ;@line 1372
						Jump _label61                                            ;@line 1372
					_label61:
						CallMethod FinishGuardEffect self ::temp166 candidate expectedGeneration expectedToken  ;@line 1374
						Return ::temp166                                         ;@line 1374
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
						CompareGT ::temp0 aiCurrentStage 0                       ;@line 109
						JumpF ::temp0 _label62                                   ;@line 109
						Assign destroyed True                                    ;@line 110
						CallMethod Shutdown self ::NoneVar                       ;@line 111
						Jump _label62                                            ;@line 111
					_label62:
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
						.local ::temp86 Bool
						.local ::temp87 Bool
						.local ::temp88 ObjectReference
						.local rootRead Bool
						.local muzzleRead Bool
						.local rootPointRead Bool
						.local muzzlePointRead Bool
						.local i Int
						.local ::temp89 Float
						.local ::temp90 Bool
						.local ::temp91 Int
					.endLocalTable
					.code
						CallMethod Current self ::temp86 expectedGeneration expectedToken  ;@line 781
						Not ::temp86 ::temp86                                    ;@line 781
						Cast ::temp86 ::temp86                                   ;@line 781
						JumpT ::temp86 _label63                                  ;@line 781
						Not ::temp87 matricesReady                               ;@line 781
						Cast ::temp86 ::temp87                                   ;@line 781
					_label63:
						JumpF ::temp86 _label64                                  ;@line 781
						Return False                                             ;@line 782
						Jump _label64                                            ;@line 782
					_label64:
						Cast ::temp88 self                                       ;@line 784
						CallStatic netimmerse GetNodeWorldRotationMatrix ::temp87 ::temp88 "" rootWorldMatrix False  ;@line 784
						Assign rootRead ::temp87                                 ;@line 784
						CallMethod Current self ::temp86 expectedGeneration expectedToken  ;@line 785
						Not ::temp87 ::temp86                                    ;@line 785
						Cast ::temp87 ::temp87                                   ;@line 785
						JumpT ::temp87 _label65                                  ;@line 785
						Not ::temp86 rootRead                                    ;@line 785
						Cast ::temp87 ::temp86                                   ;@line 785
					_label65:
						JumpF ::temp87 _label66                                  ;@line 785
						Return False                                             ;@line 786
						Jump _label66                                            ;@line 786
					_label66:
						Cast ::temp88 self                                       ;@line 788
						CallStatic netimmerse GetNodeWorldRotationMatrix ::temp86 ::temp88 ::MuzzleNode_var muzzleWorldMatrix False  ;@line 788
						Assign muzzleRead ::temp86                               ;@line 788
						CallMethod Current self ::temp87 expectedGeneration expectedToken  ;@line 789
						Not ::temp86 ::temp87                                    ;@line 789
						Cast ::temp86 ::temp86                                   ;@line 789
						JumpT ::temp86 _label67                                  ;@line 789
						Not ::temp87 muzzleRead                                  ;@line 789
						Cast ::temp86 ::temp87                                   ;@line 789
					_label67:
						JumpF ::temp86 _label68                                  ;@line 789
						Return False                                             ;@line 790
						Jump _label68                                            ;@line 790
					_label68:
						Cast ::temp88 self                                       ;@line 792
						CallStatic netimmerse GetNodeWorldPosition ::temp87 ::temp88 "" rootPosition False  ;@line 792
						Assign rootPointRead ::temp87                            ;@line 792
						CallMethod Current self ::temp86 expectedGeneration expectedToken  ;@line 793
						Not ::temp87 ::temp86                                    ;@line 793
						Cast ::temp87 ::temp87                                   ;@line 793
						JumpT ::temp87 _label69                                  ;@line 793
						Not ::temp86 rootPointRead                               ;@line 793
						Cast ::temp87 ::temp86                                   ;@line 793
					_label69:
						JumpF ::temp87 _label70                                  ;@line 793
						Return False                                             ;@line 794
						Jump _label70                                            ;@line 794
					_label70:
						Cast ::temp88 self                                       ;@line 796
						CallStatic netimmerse GetNodeWorldPosition ::temp86 ::temp88 ::MuzzleNode_var muzzlePosition False  ;@line 796
						Assign muzzlePointRead ::temp86                          ;@line 796
						CallMethod Current self ::temp87 expectedGeneration expectedToken  ;@line 797
						Not ::temp86 ::temp87                                    ;@line 797
						Cast ::temp86 ::temp86                                   ;@line 797
						JumpT ::temp86 _label71                                  ;@line 797
						Not ::temp87 muzzlePointRead                             ;@line 797
						Cast ::temp86 ::temp87                                   ;@line 797
					_label71:
						JumpF ::temp86 _label72                                  ;@line 797
						Return False                                             ;@line 798
						Jump _label72                                            ;@line 798
					_label72:
						CallMethod RotationValid self ::temp87 rootWorldMatrix   ;@line 800
						Not ::temp86 ::temp87                                    ;@line 800
						Cast ::temp86 ::temp86                                   ;@line 800
						JumpT ::temp86 _label73                                  ;@line 800
						CallMethod RotationValid self ::temp87 muzzleWorldMatrix  ;@line 800
						Not ::temp87 ::temp87                                    ;@line 800
						Cast ::temp86 ::temp87                                   ;@line 800
					_label73:
						JumpF ::temp86 _label74                                  ;@line 800
						Return False                                             ;@line 801
						Jump _label74                                            ;@line 801
					_label74:
						Assign i 0                                               ;@line 803
					_label78:
						CompareLT ::temp87 i 3                                   ;@line 804
						JumpF ::temp87 _label75                                  ;@line 804
						ArrayGetElement ::temp89 rootPosition i                  ;@line 805
						CallMethod Finite self ::temp86 ::temp89 -1000000.000000 1000000.000000  ;@line 805
						Not ::temp86 ::temp86                                    ;@line 805
						Cast ::temp86 ::temp86                                   ;@line 805
						JumpT ::temp86 _label76                                  ;@line 805
						ArrayGetElement ::temp89 muzzlePosition i                ;@line 805
						CallMethod Finite self ::temp90 ::temp89 -1000000.000000 1000000.000000  ;@line 805
						Not ::temp90 ::temp90                                    ;@line 805
						Cast ::temp86 ::temp90                                   ;@line 805
					_label76:
						JumpF ::temp86 _label77                                  ;@line 805
						Return False                                             ;@line 806
						Jump _label77                                            ;@line 806
					_label77:
						IAdd ::temp91 i 1                                        ;@line 808
						Assign i ::temp91                                        ;@line 808
						Jump _label78                                            ;@line 808
					_label75:
						CallMethod Current self ::temp90 expectedGeneration expectedToken  ;@line 810
						Return ::temp90                                          ;@line 810
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
						.local ::temp78 Bool
						.local ::temp82 Float
						.local ::temp83 Float
						.local ::temp84 Float
						.local ::temp85 Float
						.local i Int
						.local ::temp79 Float
						.local ::temp80 Bool
						.local ::temp81 Int
						.local a Float
						.local b Float
						.local c Float
						.local ab Float
						.local ac Float
						.local bc Float
						.local determinant Float
					.endLocalTable
					.code
						Assign i 0                                               ;@line 763
					_label81:
						CompareLT ::temp78 i 9                                   ;@line 764
						JumpF ::temp78 _label79                                  ;@line 764
						ArrayGetElement ::temp79 matrix i                        ;@line 765
						CallMethod Finite self ::temp80 ::temp79 -1.050000 1.050000  ;@line 765
						Not ::temp80 ::temp80                                    ;@line 765
						JumpF ::temp80 _label80                                  ;@line 765
						Return False                                             ;@line 766
						Jump _label80                                            ;@line 766
					_label80:
						IAdd ::temp81 i 1                                        ;@line 768
						Assign i ::temp81                                        ;@line 768
						Jump _label81                                            ;@line 768
					_label79:
						ArrayGetElement ::temp79 matrix 0                        ;@line 770
						ArrayGetElement ::temp82 matrix 0                        ;@line 770
						FMultiply ::temp79 ::temp79 ::temp82                     ;@line 770
						ArrayGetElement ::temp82 matrix 3                        ;@line 770
						ArrayGetElement ::temp83 matrix 3                        ;@line 770
						FMultiply ::temp82 ::temp82 ::temp83                     ;@line 770
						FAdd ::temp83 ::temp79 ::temp82                          ;@line 770
						ArrayGetElement ::temp79 matrix 6                        ;@line 770
						ArrayGetElement ::temp82 matrix 6                        ;@line 770
						FMultiply ::temp79 ::temp79 ::temp82                     ;@line 770
						FAdd ::temp82 ::temp83 ::temp79                          ;@line 770
						Assign a ::temp82                                        ;@line 770
						ArrayGetElement ::temp83 matrix 1                        ;@line 771
						ArrayGetElement ::temp79 matrix 1                        ;@line 771
						FMultiply ::temp82 ::temp83 ::temp79                     ;@line 771
						ArrayGetElement ::temp83 matrix 4                        ;@line 771
						ArrayGetElement ::temp79 matrix 4                        ;@line 771
						FMultiply ::temp83 ::temp83 ::temp79                     ;@line 771
						FAdd ::temp79 ::temp82 ::temp83                          ;@line 771
						ArrayGetElement ::temp82 matrix 7                        ;@line 771
						ArrayGetElement ::temp83 matrix 7                        ;@line 771
						FMultiply ::temp82 ::temp82 ::temp83                     ;@line 771
						FAdd ::temp83 ::temp79 ::temp82                          ;@line 771
						Assign b ::temp83                                        ;@line 771
						ArrayGetElement ::temp79 matrix 2                        ;@line 772
						ArrayGetElement ::temp82 matrix 2                        ;@line 772
						FMultiply ::temp83 ::temp79 ::temp82                     ;@line 772
						ArrayGetElement ::temp79 matrix 5                        ;@line 772
						ArrayGetElement ::temp82 matrix 5                        ;@line 772
						FMultiply ::temp79 ::temp79 ::temp82                     ;@line 772
						FAdd ::temp82 ::temp83 ::temp79                          ;@line 772
						ArrayGetElement ::temp83 matrix 8                        ;@line 772
						ArrayGetElement ::temp79 matrix 8                        ;@line 772
						FMultiply ::temp83 ::temp83 ::temp79                     ;@line 772
						FAdd ::temp79 ::temp82 ::temp83                          ;@line 772
						Assign c ::temp79                                        ;@line 772
						ArrayGetElement ::temp82 matrix 0                        ;@line 773
						ArrayGetElement ::temp83 matrix 1                        ;@line 773
						FMultiply ::temp79 ::temp82 ::temp83                     ;@line 773
						ArrayGetElement ::temp82 matrix 3                        ;@line 773
						ArrayGetElement ::temp83 matrix 4                        ;@line 773
						FMultiply ::temp82 ::temp82 ::temp83                     ;@line 773
						FAdd ::temp83 ::temp79 ::temp82                          ;@line 773
						ArrayGetElement ::temp79 matrix 6                        ;@line 773
						ArrayGetElement ::temp82 matrix 7                        ;@line 773
						FMultiply ::temp79 ::temp79 ::temp82                     ;@line 773
						FAdd ::temp82 ::temp83 ::temp79                          ;@line 773
						Assign ab ::temp82                                       ;@line 773
						ArrayGetElement ::temp83 matrix 0                        ;@line 774
						ArrayGetElement ::temp79 matrix 2                        ;@line 774
						FMultiply ::temp82 ::temp83 ::temp79                     ;@line 774
						ArrayGetElement ::temp83 matrix 3                        ;@line 774
						ArrayGetElement ::temp79 matrix 5                        ;@line 774
						FMultiply ::temp83 ::temp83 ::temp79                     ;@line 774
						FAdd ::temp79 ::temp82 ::temp83                          ;@line 774
						ArrayGetElement ::temp82 matrix 6                        ;@line 774
						ArrayGetElement ::temp83 matrix 8                        ;@line 774
						FMultiply ::temp82 ::temp82 ::temp83                     ;@line 774
						FAdd ::temp83 ::temp79 ::temp82                          ;@line 774
						Assign ac ::temp83                                       ;@line 774
						ArrayGetElement ::temp79 matrix 1                        ;@line 775
						ArrayGetElement ::temp82 matrix 2                        ;@line 775
						FMultiply ::temp83 ::temp79 ::temp82                     ;@line 775
						ArrayGetElement ::temp79 matrix 4                        ;@line 775
						ArrayGetElement ::temp82 matrix 5                        ;@line 775
						FMultiply ::temp79 ::temp79 ::temp82                     ;@line 775
						FAdd ::temp82 ::temp83 ::temp79                          ;@line 775
						ArrayGetElement ::temp83 matrix 7                        ;@line 775
						ArrayGetElement ::temp79 matrix 8                        ;@line 775
						FMultiply ::temp83 ::temp83 ::temp79                     ;@line 775
						FAdd ::temp79 ::temp82 ::temp83                          ;@line 775
						Assign bc ::temp79                                       ;@line 775
						ArrayGetElement ::temp82 matrix 0                        ;@line 776
						ArrayGetElement ::temp83 matrix 4                        ;@line 776
						ArrayGetElement ::temp79 matrix 8                        ;@line 776
						FMultiply ::temp83 ::temp83 ::temp79                     ;@line 776
						ArrayGetElement ::temp79 matrix 5                        ;@line 776
						ArrayGetElement ::temp84 matrix 7                        ;@line 776
						FMultiply ::temp79 ::temp79 ::temp84                     ;@line 776
						FSubtract ::temp84 ::temp83 ::temp79                     ;@line 776
						FMultiply ::temp83 ::temp82 ::temp84                     ;@line 776
						ArrayGetElement ::temp79 matrix 1                        ;@line 776
						ArrayGetElement ::temp82 matrix 3                        ;@line 776
						ArrayGetElement ::temp84 matrix 8                        ;@line 776
						FMultiply ::temp82 ::temp82 ::temp84                     ;@line 776
						ArrayGetElement ::temp84 matrix 5                        ;@line 776
						ArrayGetElement ::temp85 matrix 6                        ;@line 776
						FMultiply ::temp84 ::temp84 ::temp85                     ;@line 776
						FSubtract ::temp85 ::temp82 ::temp84                     ;@line 776
						FMultiply ::temp82 ::temp79 ::temp85                     ;@line 776
						FSubtract ::temp84 ::temp83 ::temp82                     ;@line 776
						ArrayGetElement ::temp79 matrix 2                        ;@line 776
						ArrayGetElement ::temp85 matrix 3                        ;@line 776
						ArrayGetElement ::temp83 matrix 7                        ;@line 776
						FMultiply ::temp82 ::temp85 ::temp83                     ;@line 776
						ArrayGetElement ::temp85 matrix 4                        ;@line 776
						ArrayGetElement ::temp83 matrix 6                        ;@line 776
						FMultiply ::temp85 ::temp85 ::temp83                     ;@line 776
						FSubtract ::temp83 ::temp82 ::temp85                     ;@line 776
						FMultiply ::temp82 ::temp79 ::temp83                     ;@line 776
						FAdd ::temp85 ::temp84 ::temp82                          ;@line 776
						Assign determinant ::temp85                              ;@line 776
						FSubtract ::temp79 a 1.000000                            ;@line 777
						CallStatic math Abs ::temp83 ::temp79                    ;@line 777
						CompareLTE ::temp80 ::temp83 0.002000                    ;@line 777
						Cast ::temp80 ::temp80                                   ;@line 777
						JumpF ::temp80 _label82                                  ;@line 777
						FSubtract ::temp84 b 1.000000                            ;@line 777
						CallStatic math Abs ::temp82 ::temp84                    ;@line 777
						CompareLTE ::temp78 ::temp82 0.002000                    ;@line 777
						Cast ::temp80 ::temp78                                   ;@line 777
					_label82:
						Cast ::temp80 ::temp80                                   ;@line 777
						JumpF ::temp80 _label83                                  ;@line 777
						FSubtract ::temp85 c 1.000000                            ;@line 777
						CallStatic math Abs ::temp79 ::temp85                    ;@line 777
						CompareLTE ::temp78 ::temp79 0.002000                    ;@line 777
						Cast ::temp80 ::temp78                                   ;@line 777
					_label83:
						Cast ::temp80 ::temp80                                   ;@line 777
						JumpF ::temp80 _label84                                  ;@line 777
						CallStatic math Abs ::temp83 ab                          ;@line 777
						CompareLTE ::temp78 ::temp83 0.002000                    ;@line 777
						Cast ::temp80 ::temp78                                   ;@line 777
					_label84:
						Cast ::temp80 ::temp80                                   ;@line 777
						JumpF ::temp80 _label85                                  ;@line 777
						CallStatic math Abs ::temp84 ac                          ;@line 777
						CompareLTE ::temp78 ::temp84 0.002000                    ;@line 777
						Cast ::temp80 ::temp78                                   ;@line 777
					_label85:
						Cast ::temp80 ::temp80                                   ;@line 777
						JumpF ::temp80 _label86                                  ;@line 777
						CallStatic math Abs ::temp82 bc                          ;@line 777
						CompareLTE ::temp78 ::temp82 0.002000                    ;@line 777
						Cast ::temp80 ::temp78                                   ;@line 777
					_label86:
						Cast ::temp80 ::temp80                                   ;@line 777
						JumpF ::temp80 _label87                                  ;@line 777
						FSubtract ::temp85 determinant 1.000000                  ;@line 777
						CallStatic math Abs ::temp79 ::temp85                    ;@line 777
						CompareLTE ::temp78 ::temp79 0.004000                    ;@line 777
						Cast ::temp80 ::temp78                                   ;@line 777
					_label87:
						Return ::temp80                                          ;@line 777
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
						.local ::temp18 Bool
						.local ::temp19 Bool
						.local ::temp20 Int
						.local ::NoneVar None
						.local ::temp25 actor
						.local sceneFree Bool
						.local scenePluginVersion Int
						.local placed Bool
						.local ::temp21 ObjectReference
						.local ::temp22 Bool
						.local ::temp23 Float[]
						.local ::temp24 Float
						.local loaded Bool
						.local controls Bool
						.local rest Float[]
						.local settled Bool
						.local candidate actor
						.local player actor
						.local usable Bool
						.local waitPoint ObjectReference
					.endLocalTable
					.code
						CallMethod PlayerLeaseCurrent self ::temp18 lease        ;@line 190
						Not ::temp18 ::temp18                                    ;@line 190
						Cast ::temp18 ::temp18                                   ;@line 190
						JumpT ::temp18 _label88                                  ;@line 190
						Cast ::temp18 pinBusy                                    ;@line 190
					_label88:
						Cast ::temp18 ::temp18                                   ;@line 190
						JumpT ::temp18 _label89                                  ;@line 190
						Cast ::temp18 sceneBusy                                  ;@line 190
					_label89:
						Cast ::temp18 ::temp18                                   ;@line 190
						JumpT ::temp18 _label90                                  ;@line 190
						Cast ::temp18 recovering                                 ;@line 190
					_label90:
						Cast ::temp18 ::temp18                                   ;@line 190
						JumpT ::temp18 _label91                                  ;@line 190
						Cast ::temp18 running                                    ;@line 190
					_label91:
						JumpF ::temp18 _label92                                  ;@line 190
						Return False                                             ;@line 191
						Jump _label92                                            ;@line 191
					_label92:
						JumpF playerReady _label93                               ;@line 193
						Return True                                              ;@line 194
						Jump _label93                                            ;@line 194
					_label93:
						CallMethod StationSceneAvailable self ::temp18           ;@line 196
						Assign sceneFree ::temp18                                ;@line 196
						CallMethod PlayerLeaseCurrent self ::temp18 lease        ;@line 197
						Not ::temp18 ::temp18                                    ;@line 197
						Cast ::temp18 ::temp18                                   ;@line 197
						JumpT ::temp18 _label94                                  ;@line 197
						Cast ::temp18 pinBusy                                    ;@line 197
					_label94:
						Cast ::temp18 ::temp18                                   ;@line 197
						JumpT ::temp18 _label95                                  ;@line 197
						Cast ::temp18 sceneBusy                                  ;@line 197
					_label95:
						Cast ::temp18 ::temp18                                   ;@line 197
						JumpT ::temp18 _label96                                  ;@line 197
						Not ::temp19 sceneFree                                   ;@line 197
						Cast ::temp18 ::temp19                                   ;@line 197
					_label96:
						JumpF ::temp18 _label97                                  ;@line 197
						Return False                                             ;@line 198
						Jump _label97                                            ;@line 198
					_label97:
						CallStatic skse GetPluginVersion ::temp20 "AstraSight"   ;@line 200
						Assign scenePluginVersion ::temp20                       ;@line 200
						CallMethod PlayerLeaseCurrent self ::temp19 lease        ;@line 201
						Not ::temp18 ::temp19                                    ;@line 201
						Cast ::temp18 ::temp18                                   ;@line 201
						JumpT ::temp18 _label98                                  ;@line 201
						CompareLT ::temp19 scenePluginVersion 50659392           ;@line 201
						Cast ::temp18 ::temp19                                   ;@line 201
					_label98:
						JumpF ::temp18 _label99                                  ;@line 201
						Return False                                             ;@line 202
						Jump _label99                                            ;@line 202
					_label99:
						CallMethod ReleaseOwnedGuard self ::NoneVar              ;@line 204
						CallMethod PlayerLeaseCurrent self ::temp19 lease        ;@line 205
						Not ::temp18 ::temp19                                    ;@line 205
						Cast ::temp19 ::temp18                                   ;@line 205
						JumpT ::temp19 _label100                                 ;@line 205
						Cast ::temp19 pinBusy                                    ;@line 205
					_label100:
						Cast ::temp18 ::temp19                                   ;@line 205
						JumpT ::temp18 _label101                                 ;@line 205
						Cast ::temp18 sceneBusy                                  ;@line 205
					_label101:
						JumpF ::temp18 _label102                                 ;@line 205
						Return False                                             ;@line 206
						Jump _label102                                           ;@line 206
					_label102:
						CallMethod EnsureCityPlacement self ::temp19 generation lease  ;@line 208
						Assign placed ::temp19                                   ;@line 208
						CallMethod PlayerLeaseCurrent self ::temp18 lease        ;@line 209
						Not ::temp19 ::temp18                                    ;@line 209
						Cast ::temp18 ::temp19                                   ;@line 209
						JumpT ::temp18 _label103                                 ;@line 209
						Cast ::temp18 pinBusy                                    ;@line 209
					_label103:
						Cast ::temp19 ::temp18                                   ;@line 209
						JumpT ::temp19 _label104                                 ;@line 209
						Cast ::temp19 sceneBusy                                  ;@line 209
					_label104:
						Cast ::temp19 ::temp19                                   ;@line 209
						JumpT ::temp19 _label105                                 ;@line 209
						Not ::temp18 placed                                      ;@line 209
						Cast ::temp19 ::temp18                                   ;@line 209
					_label105:
						JumpF ::temp19 _label106                                 ;@line 209
						Return False                                             ;@line 210
						Jump _label106                                           ;@line 210
					_label106:
						Not ::temp18 playerRestored                              ;@line 212
						JumpF ::temp18 _label107                                 ;@line 212
						CallMethod Is3DLoaded self ::temp19                      ;@line 213
						Assign loaded ::temp19                                   ;@line 213
						Cast ::temp21 self                                       ;@line 214
						CallStatic netimmerse HasNode ::temp19 ::temp21 ::YawNode_var False  ;@line 214
						Cast ::temp19 ::temp19                                   ;@line 214
						JumpF ::temp19 _label108                                 ;@line 214
						Cast ::temp21 self                                       ;@line 214
						CallStatic netimmerse HasNode ::temp22 ::temp21 ::PitchNode_var False  ;@line 214
						Cast ::temp19 ::temp22                                   ;@line 214
					_label108:
						Assign controls ::temp19                                 ;@line 214
						CallMethod PlayerLeaseCurrent self ::temp22 lease        ;@line 215
						Not ::temp19 ::temp22                                    ;@line 215
						Cast ::temp22 ::temp19                                   ;@line 215
						JumpT ::temp22 _label109                                 ;@line 215
						Cast ::temp22 pinBusy                                    ;@line 215
					_label109:
						Cast ::temp19 ::temp22                                   ;@line 215
						JumpT ::temp19 _label110                                 ;@line 215
						Cast ::temp19 sceneBusy                                  ;@line 215
					_label110:
						Cast ::temp19 ::temp19                                   ;@line 215
						JumpT ::temp19 _label111                                 ;@line 215
						Not ::temp22 loaded                                      ;@line 215
						Cast ::temp19 ::temp22                                   ;@line 215
					_label111:
						Cast ::temp19 ::temp19                                   ;@line 215
						JumpT ::temp19 _label112                                 ;@line 215
						Not ::temp22 controls                                    ;@line 215
						Cast ::temp19 ::temp22                                   ;@line 215
					_label112:
						JumpF ::temp19 _label113                                 ;@line 215
						Return False                                             ;@line 216
						Jump _label113                                           ;@line 216
					_label113:
						ArrayCreate ::temp23 9                                   ;@line 220
						Assign rest ::temp23                                     ;@line 220
						Assign ::temp24 1.000000                                 ;@line 221
						ArraySetElement rest 0 ::temp24                          ;@line 221
						Assign ::temp24 1.000000                                 ;@line 222
						ArraySetElement rest 4 ::temp24                          ;@line 222
						Assign ::temp24 1.000000                                 ;@line 223
						ArraySetElement rest 8 ::temp24                          ;@line 223
						Assign sceneBusy True                                    ;@line 224
						Cast ::temp21 self                                       ;@line 225
						CallStatic astrasightnative ResetIdleScene ::temp22 ::temp21  ;@line 225
						Assign settled ::temp22                                  ;@line 225
						CallMethod PlayerLeaseCurrent self ::temp19 lease        ;@line 226
						Cast ::temp22 ::temp19                                   ;@line 226
						JumpF ::temp22 _label114                                 ;@line 226
						Cast ::temp22 settled                                    ;@line 226
					_label114:
						JumpF ::temp22 _label115                                 ;@line 226
						Cast ::temp21 self                                       ;@line 227
						CallStatic netimmerse SetNodeLocalRotationMatrix ::temp19 ::temp21 ::YawNode_var rest False  ;@line 227
						Jump _label115                                           ;@line 227
					_label115:
						CallMethod PlayerLeaseCurrent self ::temp19 lease        ;@line 229
						Cast ::temp22 ::temp19                                   ;@line 229
						JumpF ::temp22 _label116                                 ;@line 229
						Cast ::temp22 settled                                    ;@line 229
					_label116:
						JumpF ::temp22 _label117                                 ;@line 229
						Cast ::temp21 self                                       ;@line 230
						CallStatic netimmerse SetNodeLocalRotationMatrix ::temp19 ::temp21 ::PitchNode_var rest False  ;@line 230
						Jump _label117                                           ;@line 230
					_label117:
						Assign sceneBusy False                                   ;@line 232
						CallMethod PlayerLeaseCurrent self ::temp19 lease        ;@line 233
						Not ::temp22 ::temp19                                    ;@line 233
						JumpF ::temp22 _label118                                 ;@line 233
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 234
						Return False                                             ;@line 235
						Jump _label118                                           ;@line 235
					_label118:
						Not ::temp19 settled                                     ;@line 237
						JumpF ::temp19 _label119                                 ;@line 237
						Return False                                             ;@line 238
						Jump _label119                                           ;@line 238
					_label119:
						Assign yaw 0.000000                                      ;@line 240
						Assign pitch 0.000000                                    ;@line 241
						Assign playerRestored True                               ;@line 242
						Jump _label107                                           ;@line 242
					_label107:
						Assign candidate ::Artillero_var                         ;@line 244
						CallStatic game GetPlayer ::temp25                       ;@line 245
						Assign player ::temp25                                   ;@line 245
						CallMethod PlayerLeaseCurrent self ::temp22 lease        ;@line 246
						Not ::temp19 ::temp22                                    ;@line 246
						Cast ::temp18 ::temp19                                   ;@line 246
						JumpT ::temp18 _label120                                 ;@line 246
						Cast ::temp18 pinBusy                                    ;@line 246
					_label120:
						Cast ::temp22 ::temp18                                   ;@line 246
						JumpT ::temp22 _label121                                 ;@line 246
						Cast ::temp22 sceneBusy                                  ;@line 246
					_label121:
						Cast ::temp18 ::temp22                                   ;@line 246
						JumpT ::temp18 _label122                                 ;@line 246
						CompareEQ ::temp19 candidate player                      ;@line 246
						Cast ::temp18 ::temp19                                   ;@line 246
					_label122:
						JumpF ::temp18 _label123                                 ;@line 246
						Return False                                             ;@line 247
						Jump _label123                                           ;@line 247
					_label123:
						Cast ::temp25 None                                       ;@line 249
						CompareEQ ::temp22 candidate ::temp25                    ;@line 249
						Not ::temp22 ::temp22                                    ;@line 249
						JumpF ::temp22 _label124                                 ;@line 249
						CallMethod IsDead candidate ::temp19                     ;@line 250
						Not ::temp18 ::temp19                                    ;@line 250
						Cast ::temp18 ::temp18                                   ;@line 250
						JumpF ::temp18 _label125                                 ;@line 250
						CallMethod IsDisabled candidate ::temp19                 ;@line 250
						Not ::temp19 ::temp19                                    ;@line 250
						Cast ::temp18 ::temp19                                   ;@line 250
					_label125:
						Cast ::temp18 ::temp18                                   ;@line 250
						JumpF ::temp18 _label126                                 ;@line 250
						CallMethod Is3DLoaded candidate ::temp19                 ;@line 250
						Cast ::temp18 ::temp19                                   ;@line 250
					_label126:
						Assign usable ::temp18                                   ;@line 250
						CallMethod PlayerLeaseCurrent self ::temp19 lease        ;@line 251
						Not ::temp18 ::temp19                                    ;@line 251
						Cast ::temp19 ::temp18                                   ;@line 251
						JumpT ::temp19 _label127                                 ;@line 251
						Cast ::temp19 pinBusy                                    ;@line 251
					_label127:
						Cast ::temp18 ::temp19                                   ;@line 251
						JumpT ::temp18 _label128                                 ;@line 251
						Cast ::temp18 sceneBusy                                  ;@line 251
					_label128:
						JumpF ::temp18 _label129                                 ;@line 251
						Return False                                             ;@line 252
						Jump _label129                                           ;@line 252
					_label129:
						JumpF usable _label130                                   ;@line 254
						Assign waitPoint ::Standby_var                           ;@line 255
						Cast ::temp21 None                                       ;@line 256
						CompareEQ ::temp19 waitPoint ::temp21                    ;@line 256
						JumpF ::temp19 _label131                                 ;@line 256
						Return False                                             ;@line 257
						Jump _label131                                           ;@line 257
					_label131:
						Assign pinBusy True                                      ;@line 259
						CallMethod MoveTo candidate ::NoneVar waitPoint 0.000000 0.000000 0.000000 True  ;@line 260
						CallMethod PlayerLeaseCurrent self ::temp18 lease        ;@line 261
						JumpF ::temp18 _label132                                 ;@line 261
						CallMethod SetDontMove candidate ::NoneVar True          ;@line 262
						Jump _label132                                           ;@line 262
					_label132:
						CallMethod PlayerLeaseCurrent self ::temp19 lease        ;@line 264
						Not ::temp18 ::temp19                                    ;@line 264
						JumpF ::temp18 _label133                                 ;@line 264
						CallMethod SetDontMove candidate ::NoneVar False         ;@line 267
						Assign pinBusy False                                     ;@line 268
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 269
						Return False                                             ;@line 270
						Jump _label133                                           ;@line 270
					_label133:
						Assign ownedGuard candidate                              ;@line 272
						Assign pinBusy False                                     ;@line 273
						Jump _label130                                           ;@line 273
					_label130:
						Jump _label124                                           ;@line 273
					_label124:
						CallMethod PlayerLeaseCurrent self ::temp19 lease        ;@line 276
						Not ::temp18 ::temp19                                    ;@line 276
						Cast ::temp22 ::temp18                                   ;@line 276
						JumpT ::temp22 _label134                                 ;@line 276
						Cast ::temp22 pinBusy                                    ;@line 276
					_label134:
						Cast ::temp19 ::temp22                                   ;@line 276
						JumpT ::temp19 _label135                                 ;@line 276
						Cast ::temp19 sceneBusy                                  ;@line 276
					_label135:
						JumpF ::temp19 _label136                                 ;@line 276
						Return False                                             ;@line 277
						Jump _label136                                           ;@line 277
					_label136:
						Assign playerReady True                                  ;@line 279
						Return True                                              ;@line 280
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
						.local ::temp128 Bool
						.local ::temp129 Bool
						.local ::temp130 Float
						.local now Float
						.local bodyStarted Bool
						.local cadence Float
						.local started Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod Current self ::temp128 expectedGeneration expectedToken  ;@line 990
						Not ::temp128 ::temp128                                  ;@line 990
						Cast ::temp128 ::temp128                                 ;@line 990
						JumpT ::temp128 _label137                                ;@line 990
						CompareEQ ::temp129 phase 0                              ;@line 990
						Not ::temp129 ::temp129                                  ;@line 990
						Cast ::temp128 ::temp129                                 ;@line 990
					_label137:
						JumpF ::temp128 _label138                                ;@line 990
						Return None                                              ;@line 991
						Jump _label138                                           ;@line 991
					_label138:
						CallStatic utility GetCurrentRealTime ::temp130          ;@line 993
						Assign now ::temp130                                     ;@line 993
						CallMethod Current self ::temp129 expectedGeneration expectedToken  ;@line 994
						Not ::temp128 ::temp129                                  ;@line 994
						Cast ::temp128 ::temp128                                 ;@line 994
						JumpT ::temp128 _label139                                ;@line 994
						CompareEQ ::temp129 phase 0                              ;@line 994
						Not ::temp129 ::temp129                                  ;@line 994
						Cast ::temp128 ::temp129                                 ;@line 994
					_label139:
						Cast ::temp128 ::temp128                                 ;@line 994
						JumpT ::temp128 _label140                                ;@line 994
						CallMethod Finite self ::temp129 now 0.000000 1000000000.000000  ;@line 994
						Not ::temp129 ::temp129                                  ;@line 994
						Cast ::temp128 ::temp129                                 ;@line 994
					_label140:
						Cast ::temp128 ::temp128                                 ;@line 994
						JumpT ::temp128 _label141                                ;@line 994
						CompareLT ::temp129 now nextShotAt                       ;@line 994
						Cast ::temp128 ::temp129                                 ;@line 994
					_label141:
						JumpF ::temp128 _label142                                ;@line 994
						Return None                                              ;@line 995
						Jump _label142                                           ;@line 995
					_label142:
						CallMethod SetGuardFirePose self ::temp129 True expectedGeneration expectedToken  ;@line 997
						Assign bodyStarted ::temp129                             ;@line 997
						CallMethod Current self ::temp128 expectedGeneration expectedToken  ;@line 998
						Not ::temp129 ::temp128                                  ;@line 998
						Cast ::temp129 ::temp129                                 ;@line 998
						JumpT ::temp129 _label143                                ;@line 998
						Not ::temp128 bodyStarted                                ;@line 998
						Cast ::temp129 ::temp128                                 ;@line 998
					_label143:
						JumpF ::temp129 _label144                                ;@line 998
						Return None                                              ;@line 999
						Jump _label144                                           ;@line 999
					_label144:
						Assign guardPoseFireAt now                               ;@line 1001
						Assign phase 1                                           ;@line 1002
						Assign phaseAt now                                       ;@line 1003
						Assign shotTarget target                                 ;@line 1004
						CallMethod SafeCadenceSeconds self ::temp130             ;@line 1005
						Assign cadence ::temp130                                 ;@line 1005
						FAdd ::temp130 now cadence                               ;@line 1006
						Assign nextShotAt ::temp130                              ;@line 1006
						CallMethod PlaySceneAnimation self ::temp128 "Fire" expectedGeneration expectedToken  ;@line 1007
						Assign started ::temp128                                 ;@line 1007
						CallMethod Current self ::temp129 expectedGeneration expectedToken  ;@line 1008
						Not ::temp128 ::temp129                                  ;@line 1008
						Cast ::temp128 ::temp128                                 ;@line 1008
						JumpT ::temp128 _label145                                ;@line 1008
						CompareEQ ::temp129 phase 1                              ;@line 1008
						Not ::temp129 ::temp129                                  ;@line 1008
						Cast ::temp128 ::temp129                                 ;@line 1008
					_label145:
						Cast ::temp128 ::temp128                                 ;@line 1008
						JumpT ::temp128 _label146                                ;@line 1008
						CompareEQ ::temp129 shotTarget target                    ;@line 1008
						Not ::temp129 ::temp129                                  ;@line 1008
						Cast ::temp128 ::temp129                                 ;@line 1008
					_label146:
						JumpF ::temp128 _label147                                ;@line 1008
						Return None                                              ;@line 1009
						Jump _label147                                           ;@line 1009
					_label147:
						Not ::temp129 started                                    ;@line 1011
						JumpF ::temp129 _label148                                ;@line 1011
						CallMethod AbortShot self ::NoneVar expectedGeneration expectedToken  ;@line 1012
						Jump _label148                                           ;@line 1012
					_label148:
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
						.local ::temp131 Bool
						.local ::temp132 Bool
						.local ::temp133 Float
						.local ::temp134 ObjectReference
						.local ::temp135 sound
						.local now Float
						.local safe Bool
						.local ::NoneVar None
						.local cadence Float
						.local launchCurrent Bool
						.local launchedAt Float
						.local ::temp136 Int
					.endLocalTable
					.code
						Cast ::temp131 sceneBusy                                 ;@line 1017
						JumpT ::temp131 _label149                                ;@line 1017
						CallMethod Current self ::temp131 expectedGeneration expectedToken  ;@line 1017
						Not ::temp131 ::temp131                                  ;@line 1017
						Cast ::temp131 ::temp131                                 ;@line 1017
					_label149:
						Cast ::temp131 ::temp131                                 ;@line 1017
						JumpT ::temp131 _label150                                ;@line 1017
						CompareEQ ::temp132 phase 1                              ;@line 1017
						Not ::temp132 ::temp132                                  ;@line 1017
						Cast ::temp131 ::temp132                                 ;@line 1017
					_label150:
						Cast ::temp131 ::temp131                                 ;@line 1017
						JumpT ::temp131 _label151                                ;@line 1017
						CompareEQ ::temp132 shotTarget target                    ;@line 1017
						Not ::temp132 ::temp132                                  ;@line 1017
						Cast ::temp131 ::temp132                                 ;@line 1017
					_label151:
						JumpF ::temp131 _label152                                ;@line 1017
						Return None                                              ;@line 1018
						Jump _label152                                           ;@line 1018
					_label152:
						CallStatic utility GetCurrentRealTime ::temp133          ;@line 1020
						Assign now ::temp133                                     ;@line 1020
						CallMethod ShotPreflight self ::temp132 target expectedGeneration expectedToken  ;@line 1023
						Assign safe ::temp132                                    ;@line 1023
						CallMethod Current self ::temp131 expectedGeneration expectedToken  ;@line 1024
						Not ::temp132 ::temp131                                  ;@line 1024
						Cast ::temp132 ::temp132                                 ;@line 1024
						JumpT ::temp132 _label153                                ;@line 1024
						CompareEQ ::temp131 phase 1                              ;@line 1024
						Not ::temp131 ::temp131                                  ;@line 1024
						Cast ::temp132 ::temp131                                 ;@line 1024
					_label153:
						Cast ::temp132 ::temp132                                 ;@line 1024
						JumpT ::temp132 _label154                                ;@line 1024
						CompareEQ ::temp131 shotTarget target                    ;@line 1024
						Not ::temp131 ::temp131                                  ;@line 1024
						Cast ::temp132 ::temp131                                 ;@line 1024
					_label154:
						JumpF ::temp132 _label155                                ;@line 1024
						Return None                                              ;@line 1025
						Jump _label155                                           ;@line 1025
					_label155:
						Not ::temp131 safe                                       ;@line 1027
						Cast ::temp131 ::temp131                                 ;@line 1027
						JumpT ::temp131 _label156                                ;@line 1027
						CallMethod Finite self ::temp132 now 0.000000 1000000000.000000  ;@line 1027
						Not ::temp132 ::temp132                                  ;@line 1027
						Cast ::temp131 ::temp132                                 ;@line 1027
					_label156:
						JumpF ::temp131 _label157                                ;@line 1027
						CallMethod AbortShot self ::NoneVar expectedGeneration expectedToken  ;@line 1028
						Return None                                              ;@line 1029
						Jump _label157                                           ;@line 1029
					_label157:
						CallMethod SafeCadenceSeconds self ::temp133             ;@line 1031
						Assign cadence ::temp133                                 ;@line 1031
						FAdd ::temp133 now cadence                               ;@line 1032
						CompareLT ::temp132 nextShotAt ::temp133                 ;@line 1032
						JumpF ::temp132 _label158                                ;@line 1032
						FAdd ::temp133 now cadence                               ;@line 1033
						Assign nextShotAt ::temp133                              ;@line 1033
						Jump _label158                                           ;@line 1033
					_label158:
						Assign phase 2                                           ;@line 1037
						Assign phaseAt now                                       ;@line 1038
						CallMethod Current self ::temp131 expectedGeneration expectedToken  ;@line 1039
						Not ::temp132 ::temp131                                  ;@line 1039
						Cast ::temp132 ::temp132                                 ;@line 1039
						JumpT ::temp132 _label159                                ;@line 1039
						CompareEQ ::temp131 phase 2                              ;@line 1039
						Not ::temp131 ::temp131                                  ;@line 1039
						Cast ::temp132 ::temp131                                 ;@line 1039
					_label159:
						Cast ::temp132 ::temp132                                 ;@line 1039
						JumpT ::temp132 _label160                                ;@line 1039
						CompareEQ ::temp131 shotTarget target                    ;@line 1039
						Not ::temp131 ::temp131                                  ;@line 1039
						Cast ::temp132 ::temp131                                 ;@line 1039
					_label160:
						JumpF ::temp132 _label161                                ;@line 1039
						Return None                                              ;@line 1040
						Jump _label161                                           ;@line 1040
					_label161:
						Assign sceneBusy True                                    ;@line 1045
						Cast ::temp134 self                                      ;@line 1046
						CallMethod Fire ::Launcher_var ::NoneVar ::temp134 ::ShotAmmo_var  ;@line 1046
						CallMethod FinishSceneEffect self ::temp131 expectedGeneration expectedToken  ;@line 1047
						Assign launchCurrent ::temp131                           ;@line 1047
						Not ::temp132 launchCurrent                              ;@line 1048
						Cast ::temp132 ::temp132                                 ;@line 1048
						JumpT ::temp132 _label162                                ;@line 1048
						CallMethod Current self ::temp131 expectedGeneration expectedToken  ;@line 1048
						Not ::temp131 ::temp131                                  ;@line 1048
						Cast ::temp132 ::temp131                                 ;@line 1048
					_label162:
						Cast ::temp132 ::temp132                                 ;@line 1048
						JumpT ::temp132 _label163                                ;@line 1048
						CompareEQ ::temp131 phase 2                              ;@line 1048
						Not ::temp131 ::temp131                                  ;@line 1048
						Cast ::temp132 ::temp131                                 ;@line 1048
					_label163:
						JumpF ::temp132 _label164                                ;@line 1048
						Return None                                              ;@line 1049
						Jump _label164                                           ;@line 1049
					_label164:
						CallStatic utility GetCurrentRealTime ::temp133          ;@line 1053
						Assign launchedAt ::temp133                              ;@line 1053
						CallMethod Current self ::temp131 expectedGeneration expectedToken  ;@line 1054
						Not ::temp132 ::temp131                                  ;@line 1054
						Cast ::temp132 ::temp132                                 ;@line 1054
						JumpT ::temp132 _label165                                ;@line 1054
						CompareEQ ::temp131 phase 2                              ;@line 1054
						Not ::temp131 ::temp131                                  ;@line 1054
						Cast ::temp132 ::temp131                                 ;@line 1054
					_label165:
						JumpF ::temp132 _label166                                ;@line 1054
						Return None                                              ;@line 1055
						Jump _label166                                           ;@line 1055
					_label166:
						CallMethod Finite self ::temp131 launchedAt 0.000000 1000000000.000000  ;@line 1057
						Not ::temp132 ::temp131                                  ;@line 1057
						JumpF ::temp132 _label167                                ;@line 1057
						Assign faulted True                                      ;@line 1058
						CallMethod Shutdown self ::NoneVar                       ;@line 1059
						Return None                                              ;@line 1060
						Jump _label167                                           ;@line 1060
					_label167:
						Assign phaseAt launchedAt                                ;@line 1062
						FAdd ::temp133 launchedAt cadence                        ;@line 1063
						CompareLT ::temp131 nextShotAt ::temp133                 ;@line 1063
						JumpF ::temp131 _label168                                ;@line 1063
						FAdd ::temp133 launchedAt cadence                        ;@line 1064
						Assign nextShotAt ::temp133                              ;@line 1064
						Jump _label168                                           ;@line 1064
					_label168:
						CallMethod SetVisualBolt self ::NoneVar 0.000000 expectedGeneration expectedToken  ;@line 1066
						CallMethod Current self ::temp132 expectedGeneration expectedToken  ;@line 1067
						Not ::temp131 ::temp132                                  ;@line 1067
						Cast ::temp131 ::temp131                                 ;@line 1067
						JumpT ::temp131 _label169                                ;@line 1067
						CompareEQ ::temp132 phase 2                              ;@line 1067
						Not ::temp132 ::temp132                                  ;@line 1067
						Cast ::temp131 ::temp132                                 ;@line 1067
					_label169:
						JumpF ::temp131 _label170                                ;@line 1067
						Return None                                              ;@line 1068
						Jump _label170                                           ;@line 1068
					_label170:
						Cast ::temp135 None                                      ;@line 1070
						CompareEQ ::temp132 ::ShotSound_var ::temp135            ;@line 1070
						Not ::temp132 ::temp132                                  ;@line 1070
						JumpF ::temp132 _label171                                ;@line 1070
						Cast ::temp134 self                                      ;@line 1071
						CallMethod Play ::ShotSound_var ::temp136 ::temp134      ;@line 1071
						Jump _label171                                           ;@line 1071
					_label171:
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
						.local ::temp137 Bool
						.local ::temp138 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod Current self ::temp137 expectedGeneration expectedToken  ;@line 1076
						Not ::temp137 ::temp137                                  ;@line 1076
						Cast ::temp137 ::temp137                                 ;@line 1076
						JumpT ::temp137 _label172                                ;@line 1076
						CompareEQ ::temp138 phase 0                              ;@line 1076
						Cast ::temp137 ::temp138                                 ;@line 1076
					_label172:
						JumpF ::temp137 _label173                                ;@line 1076
						Return None                                              ;@line 1077
						Jump _label173                                           ;@line 1077
					_label173:
						CallMethod SetGuardFirePose self ::temp138 False expectedGeneration expectedToken  ;@line 1079
						CallMethod Current self ::temp137 expectedGeneration expectedToken  ;@line 1080
						JumpF ::temp137 _label174                                ;@line 1080
						CallMethod StartReset self ::NoneVar expectedGeneration expectedToken  ;@line 1081
						Jump _label174                                           ;@line 1081
					_label174:
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
						.local ::temp190 Bool
						.local ::temp191 Bool
						.local ::temp192 Float
						.local ::temp193 Float
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
						CallMethod ValidTarget self ::temp190 target expectedGeneration expectedToken  ;@line 1454
						Not ::temp190 ::temp190                                  ;@line 1454
						Cast ::temp190 ::temp190                                 ;@line 1454
						JumpT ::temp190 _label175                                ;@line 1454
						CallMethod ReadPose self ::temp191 expectedGeneration expectedToken  ;@line 1454
						Not ::temp191 ::temp191                                  ;@line 1454
						Cast ::temp190 ::temp191                                 ;@line 1454
					_label175:
						JumpF ::temp190 _label176                                ;@line 1454
						Return False                                             ;@line 1455
						Jump _label176                                           ;@line 1455
					_label176:
						CallMethod GetPositionX target ::temp192                 ;@line 1457
						ArrayGetElement ::temp193 muzzlePosition 0               ;@line 1457
						FSubtract ::temp192 ::temp192 ::temp193                  ;@line 1457
						Assign dx ::temp192                                      ;@line 1457
						CallMethod GetPositionY target ::temp193                 ;@line 1458
						ArrayGetElement ::temp192 muzzlePosition 1               ;@line 1458
						FSubtract ::temp193 ::temp193 ::temp192                  ;@line 1458
						Assign dy ::temp193                                      ;@line 1458
						FMultiply ::temp192 dx dx                                ;@line 1459
						FMultiply ::temp193 dy dy                                ;@line 1459
						FAdd ::temp192 ::temp192 ::temp193                       ;@line 1459
						CallStatic math Sqrt ::temp193 ::temp192                 ;@line 1459
						Assign horizontal ::temp193                              ;@line 1459
						CallMethod HorizontalReachable self ::temp191 target horizontal expectedGeneration expectedToken  ;@line 1460
						Not ::temp190 ::temp191                                  ;@line 1460
						JumpF ::temp190 _label177                                ;@line 1460
						Return False                                             ;@line 1461
						Jump _label177                                           ;@line 1461
					_label177:
						FDivide ::temp192 dx horizontal                          ;@line 1463
						Assign wx ::temp192                                      ;@line 1463
						FDivide ::temp193 dy horizontal                          ;@line 1464
						Assign wy ::temp193                                      ;@line 1464
						ArrayGetElement ::temp192 rootWorldMatrix 0              ;@line 1465
						FMultiply ::temp193 ::temp192 wx                         ;@line 1465
						ArrayGetElement ::temp192 rootWorldMatrix 3              ;@line 1465
						FMultiply ::temp192 ::temp192 wy                         ;@line 1465
						FAdd ::temp193 ::temp193 ::temp192                       ;@line 1465
						Assign lx ::temp193                                      ;@line 1465
						ArrayGetElement ::temp192 rootWorldMatrix 1              ;@line 1466
						FMultiply ::temp193 ::temp192 wx                         ;@line 1466
						ArrayGetElement ::temp192 rootWorldMatrix 4              ;@line 1466
						FMultiply ::temp192 ::temp192 wy                         ;@line 1466
						FAdd ::temp193 ::temp193 ::temp192                       ;@line 1466
						Assign ly ::temp193                                      ;@line 1466
						FNegate ::temp192 ly                                     ;@line 1467
						CallMethod HeadingFromVector self ::temp193 lx ::temp192 yaw  ;@line 1467
						Assign angle ::temp193                                   ;@line 1467
						CompareGT ::temp191 angle 180.000000                     ;@line 1468
						JumpF ::temp191 _label178                                ;@line 1468
						FSubtract ::temp192 angle 360.000000                     ;@line 1469
						Assign angle ::temp192                                   ;@line 1469
						Jump _label178                                           ;@line 1469
					_label178:
						FSubtract ::temp193 ::YawCenter_var ::YawHalfSector_var  ;@line 1471
						FAdd ::temp192 ::YawCenter_var ::YawHalfSector_var       ;@line 1471
						CallMethod Finite self ::temp190 angle ::temp193 ::temp192  ;@line 1471
						Not ::temp191 ::temp190                                  ;@line 1471
						Cast ::temp191 ::temp191                                 ;@line 1471
						JumpT ::temp191 _label179                                ;@line 1471
						CallMethod Current self ::temp190 expectedGeneration expectedToken  ;@line 1471
						Not ::temp190 ::temp190                                  ;@line 1471
						Cast ::temp191 ::temp190                                 ;@line 1471
					_label179:
						JumpF ::temp191 _label180                                ;@line 1471
						Return False                                             ;@line 1472
						Jump _label180                                           ;@line 1472
					_label180:
						Assign desiredYaw angle                                  ;@line 1474
						Assign desiredPitch 0.000000                             ;@line 1475
						Assign aimX wx                                           ;@line 1476
						Assign aimY wy                                           ;@line 1477
						Assign aimZ 0.000000                                     ;@line 1478
						Assign targetHorizontal horizontal                       ;@line 1479
						Return True                                              ;@line 1480
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
						.local ::temp162 Bool
						.local ::NoneVar None
						.local candidate actor
						.local started Bool
						.local ::temp163 Bool
						.local valid Bool
					.endLocalTable
					.code
						Cast ::temp162 pinBusy                                   ;@line 1308
						JumpT ::temp162 _label181                                ;@line 1308
						CallMethod GuardReady self ::temp162 expectedGeneration expectedToken  ;@line 1308
						Not ::temp162 ::temp162                                  ;@line 1308
						Cast ::temp162 ::temp162                                 ;@line 1308
					_label181:
						JumpF ::temp162 _label182                                ;@line 1308
						Return False                                             ;@line 1309
						Jump _label182                                           ;@line 1309
					_label182:
						Assign candidate ownedGuard                              ;@line 1311
						Assign pinBusy True                                      ;@line 1312
						CallMethod RemoveFromFaction candidate ::NoneVar fireFaction  ;@line 1313
						CallMethod Current self ::temp162 expectedGeneration expectedToken  ;@line 1314
						JumpF ::temp162 _label183                                ;@line 1314
						CallMethod SetFactionRank candidate ::NoneVar poseFaction 0  ;@line 1315
						Jump _label183                                           ;@line 1315
					_label183:
						CallMethod Current self ::temp162 expectedGeneration expectedToken  ;@line 1317
						JumpF ::temp162 _label184                                ;@line 1317
						CallMethod SetHeadTracking candidate ::NoneVar False     ;@line 1318
						Jump _label184                                           ;@line 1318
					_label184:
						CallMethod Current self ::temp162 expectedGeneration expectedToken  ;@line 1320
						JumpF ::temp162 _label185                                ;@line 1320
						CallMethod SheatheWeapon candidate ::NoneVar             ;@line 1321
						Jump _label185                                           ;@line 1321
					_label185:
						Assign started False                                     ;@line 1323
						CallMethod Current self ::temp162 expectedGeneration expectedToken  ;@line 1324
						JumpF ::temp162 _label186                                ;@line 1324
						CallMethod PlayIdle candidate ::temp163 holdIdle         ;@line 1325
						Assign started ::temp163                                 ;@line 1325
						Jump _label186                                           ;@line 1325
					_label186:
						CallMethod FinishGuardEffect self ::temp163 candidate expectedGeneration expectedToken  ;@line 1327
						Assign valid ::temp163                                   ;@line 1327
						JumpF valid _label187                                    ;@line 1328
						Assign guardPoseStarted started                          ;@line 1329
						Assign guardPoseFiring False                             ;@line 1330
						Jump _label187                                           ;@line 1330
					_label187:
						Cast ::temp162 valid                                     ;@line 1332
						JumpF ::temp162 _label188                                ;@line 1332
						Cast ::temp162 started                                   ;@line 1332
					_label188:
						Return ::temp162                                         ;@line 1332
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
						.local ::temp50 Bool
						.local ::temp51 Bool
						.local animationReady Bool
						.local ::NoneVar None
						.local candidate actor
					.endLocalTable
					.code
						Cast ::temp50 pinBusy                                    ;@line 582
						JumpT ::temp50 _label189                                 ;@line 582
						CompareEQ ::temp50 generation expectedGeneration         ;@line 582
						Not ::temp50 ::temp50                                    ;@line 582
						Cast ::temp50 ::temp50                                   ;@line 582
					_label189:
						Cast ::temp50 ::temp50                                   ;@line 582
						JumpT ::temp50 _label190                                 ;@line 582
						CompareEQ ::temp51 token -1                              ;@line 582
						Not ::temp51 ::temp51                                    ;@line 582
						Cast ::temp50 ::temp51                                   ;@line 582
					_label190:
						Cast ::temp50 ::temp50                                   ;@line 582
						JumpT ::temp50 _label191                                 ;@line 582
						Not ::temp51 recovering                                  ;@line 582
						Cast ::temp50 ::temp51                                   ;@line 582
					_label191:
						Cast ::temp51 ::temp50                                   ;@line 582
						JumpT ::temp51 _label192                                 ;@line 582
						Cast ::temp51 destroyed                                  ;@line 582
					_label192:
						Cast ::temp50 ::temp51                                   ;@line 582
						JumpT ::temp50 _label193                                 ;@line 582
						Cast ::temp50 faulted                                    ;@line 582
					_label193:
						JumpF ::temp50 _label194                                 ;@line 582
						Return False                                             ;@line 583
						Jump _label194                                           ;@line 583
					_label194:
						CallMethod LoadGuardAnimation self ::temp51              ;@line 585
						Assign animationReady ::temp51                           ;@line 585
						CompareEQ ::temp50 generation expectedGeneration         ;@line 586
						Not ::temp50 ::temp50                                    ;@line 586
						Cast ::temp50 ::temp50                                   ;@line 586
						JumpT ::temp50 _label195                                 ;@line 586
						Not ::temp51 animationReady                              ;@line 586
						Cast ::temp50 ::temp51                                   ;@line 586
					_label195:
						JumpF ::temp50 _label196                                 ;@line 586
						CallStatic debug Trace ::NoneVar "AstraAsedioGuard: enable OAR and AstraAsedio_GuardAnim.esp to operate the NPC." 0  ;@line 587
						Return False                                             ;@line 588
						Jump _label196                                           ;@line 588
					_label196:
						Assign candidate ::Artillero_var                         ;@line 590
						Assign pinBusy True                                      ;@line 591
						CallMethod SetDontMove candidate ::NoneVar True          ;@line 592
						CompareEQ ::temp51 generation expectedGeneration         ;@line 593
						Not ::temp51 ::temp51                                    ;@line 593
						Cast ::temp51 ::temp51                                   ;@line 593
						JumpT ::temp51 _label197                                 ;@line 593
						CompareEQ ::temp50 token -1                              ;@line 593
						Not ::temp50 ::temp50                                    ;@line 593
						Cast ::temp51 ::temp50                                   ;@line 593
					_label197:
						Cast ::temp51 ::temp51                                   ;@line 593
						JumpT ::temp51 _label198                                 ;@line 593
						Not ::temp50 recovering                                  ;@line 593
						Cast ::temp51 ::temp50                                   ;@line 593
					_label198:
						Cast ::temp50 ::temp51                                   ;@line 593
						JumpT ::temp50 _label199                                 ;@line 593
						Cast ::temp50 destroyed                                  ;@line 593
					_label199:
						Cast ::temp51 ::temp50                                   ;@line 593
						JumpT ::temp51 _label200                                 ;@line 593
						Cast ::temp51 faulted                                    ;@line 593
					_label200:
						JumpF ::temp51 _label201                                 ;@line 593
						CallMethod SetDontMove candidate ::NoneVar False         ;@line 597
						Assign pinBusy False                                     ;@line 598
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 599
						Return False                                             ;@line 600
						Jump _label201                                           ;@line 600
					_label201:
						Assign ownedGuard candidate                              ;@line 602
						Assign pinBusy False                                     ;@line 603
						Return True                                              ;@line 604
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
						CallMethod BlockActivation self ::NoneVar True           ;@line 87
						CallMethod BeginRecovery self ::NoneVar                  ;@line 88
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
						.local ::temp164 Bool
						.local ::temp165 Bool
						.local candidate actor
						.local ::NoneVar None
						.local valid Bool
					.endLocalTable
					.code
						Cast ::temp164 pinBusy                                   ;@line 1336
						JumpT ::temp164 _label202                                ;@line 1336
						CallMethod GuardReady self ::temp164 expectedGeneration expectedToken  ;@line 1336
						Not ::temp164 ::temp164                                  ;@line 1336
						Cast ::temp164 ::temp164                                 ;@line 1336
					_label202:
						Cast ::temp164 ::temp164                                 ;@line 1336
						JumpT ::temp164 _label203                                ;@line 1336
						Not ::temp165 guardPoseStarted                           ;@line 1336
						Cast ::temp164 ::temp165                                 ;@line 1336
					_label203:
						JumpF ::temp164 _label204                                ;@line 1336
						Return False                                             ;@line 1337
						Jump _label204                                           ;@line 1337
					_label204:
						Assign candidate ownedGuard                              ;@line 1339
						Assign pinBusy True                                      ;@line 1340
						JumpF Fire _label205                                     ;@line 1341
						CallMethod SetFactionRank candidate ::NoneVar fireFaction 0  ;@line 1342
						Jump _label206                                           ;@line 1342
					_label205:
						CallMethod RemoveFromFaction candidate ::NoneVar fireFaction  ;@line 1344
					_label206:
						CallMethod FinishGuardEffect self ::temp165 candidate expectedGeneration expectedToken  ;@line 1346
						Assign valid ::temp165                                   ;@line 1346
						JumpF valid _label207                                    ;@line 1347
						Assign guardPoseFiring Fire                              ;@line 1348
						Jump _label207                                           ;@line 1348
					_label207:
						Return valid                                             ;@line 1350
					.endCode
				.endFunction
				.function OnUpdate
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp142 Bool
						.local ::temp143 Float
						.local ::NoneVar None
						.local updateGeneration Int
						.local updateToken Int
						.local now Float
						.local dt Float
						.local ready Bool
						.local ::temp144 Bool
						.local ::temp145 Bool
						.local dead Bool
						.local guardLoaded Bool
						.local gunLoaded Bool
						.local menuOpen Bool
						.local releaseDelay Float
						.local fireDelay Float
						.local resetDelay Float
						.local ::temp146 Bool
						.local ::temp147 actor
						.local target actor
						.local sampled Bool
						.local positioned Bool
						.local aligned Bool
					.endLocalTable
					.code
						Cast ::temp142 updating                                  ;@line 1111
						JumpT ::temp142 _label208                                ;@line 1111
						Cast ::temp142 recovering                                ;@line 1111
					_label208:
						Cast ::temp142 ::temp142                                 ;@line 1111
						JumpT ::temp142 _label209                                ;@line 1111
						Cast ::temp142 pinBusy                                   ;@line 1111
					_label209:
						Cast ::temp142 ::temp142                                 ;@line 1111
						JumpT ::temp142 _label210                                ;@line 1111
						Cast ::temp142 sceneBusy                                 ;@line 1111
					_label210:
						Cast ::temp142 ::temp142                                 ;@line 1111
						JumpT ::temp142 _label211                                ;@line 1111
						Cast ::temp142 destroyed                                 ;@line 1111
					_label211:
						Cast ::temp142 ::temp142                                 ;@line 1111
						JumpT ::temp142 _label212                                ;@line 1111
						Cast ::temp142 faulted                                   ;@line 1111
					_label212:
						JumpF ::temp142 _label213                                ;@line 1111
						Return None                                              ;@line 1112
						Jump _label213                                           ;@line 1112
					_label213:
						Not ::temp142 running                                    ;@line 1114
						JumpF ::temp142 _label214                                ;@line 1114
						CallMethod BeginRecovery self ::NoneVar                  ;@line 1115
						Return None                                              ;@line 1116
						Jump _label214                                           ;@line 1116
					_label214:
						Assign updating True                                     ;@line 1118
						Assign updateGeneration generation                       ;@line 1119
						Assign updateToken token                                 ;@line 1120
						CallStatic utility GetCurrentRealTime ::temp143          ;@line 1121
						Assign now ::temp143                                     ;@line 1121
						CallMethod Current self ::temp142 updateGeneration updateToken  ;@line 1122
						Not ::temp142 ::temp142                                  ;@line 1122
						JumpF ::temp142 _label215                                ;@line 1122
						Return None                                              ;@line 1123
						Jump _label215                                           ;@line 1123
					_label215:
						CallMethod Finite self ::temp142 now 0.000000 1000000000.000000  ;@line 1125
						Not ::temp142 ::temp142                                  ;@line 1125
						JumpF ::temp142 _label216                                ;@line 1125
						Assign faulted True                                      ;@line 1126
						CallMethod Shutdown self ::NoneVar                       ;@line 1127
						Return None                                              ;@line 1128
						Jump _label216                                           ;@line 1128
					_label216:
						CompareLT ::temp142 now lastTick                         ;@line 1130
						JumpF ::temp142 _label217                                ;@line 1130
						CallMethod BeginRecovery self ::NoneVar                  ;@line 1133
						Return None                                              ;@line 1134
						Jump _label217                                           ;@line 1134
					_label217:
						FSubtract ::temp143 now lastTick                         ;@line 1136
						Assign dt ::temp143                                      ;@line 1136
						CompareGT ::temp142 dt 0.400000                          ;@line 1137
						JumpF ::temp142 _label218                                ;@line 1137
						Assign dt 0.400000                                       ;@line 1138
						Jump _label218                                           ;@line 1138
					_label218:
						Assign lastTick now                                      ;@line 1140
						CallMethod GuardReady self ::temp142 updateGeneration updateToken  ;@line 1141
						Assign ready ::temp142                                   ;@line 1141
						CallMethod Current self ::temp142 updateGeneration updateToken  ;@line 1142
						Not ::temp142 ::temp142                                  ;@line 1142
						JumpF ::temp142 _label219                                ;@line 1142
						Return None                                              ;@line 1143
						Jump _label219                                           ;@line 1143
					_label219:
						Not ::temp142 ready                                      ;@line 1145
						JumpF ::temp142 _label220                                ;@line 1145
						CallMethod IsDead ::Artillero_var ::temp144              ;@line 1146
						Assign dead ::temp144                                    ;@line 1146
						CallMethod Is3DLoaded ::Artillero_var ::temp144          ;@line 1147
						Assign guardLoaded ::temp144                             ;@line 1147
						CallMethod Is3DLoaded self ::temp144                     ;@line 1148
						Assign gunLoaded ::temp144                               ;@line 1148
						CallMethod Current self ::temp144 updateGeneration updateToken  ;@line 1149
						Not ::temp144 ::temp144                                  ;@line 1149
						JumpF ::temp144 _label221                                ;@line 1149
						Return None                                              ;@line 1150
						Jump _label221                                           ;@line 1150
					_label221:
						Cast ::temp144 dead                                      ;@line 1154
						JumpT ::temp144 _label222                                ;@line 1154
						Cast ::temp144 guardLoaded                               ;@line 1154
					_label222:
						Assign faulted ::temp144                                 ;@line 1154
						CallMethod Shutdown self ::NoneVar                       ;@line 1155
						Not ::temp144 faulted                                    ;@line 1156
						Cast ::temp144 ::temp144                                 ;@line 1156
						JumpF ::temp144 _label223                                ;@line 1156
						Cast ::temp144 gunLoaded                                 ;@line 1156
					_label223:
						Cast ::temp144 ::temp144                                 ;@line 1156
						JumpF ::temp144 _label224                                ;@line 1156
						Not ::temp145 destroyed                                  ;@line 1156
						Cast ::temp144 ::temp145                                 ;@line 1156
					_label224:
						JumpF ::temp144 _label225                                ;@line 1156
						CallMethod RegisterForSingleUpdate self ::NoneVar 1.000000  ;@line 1157
						Jump _label225                                           ;@line 1157
					_label225:
						Return None                                              ;@line 1159
						Jump _label220                                           ;@line 1159
					_label220:
						Cast ::temp144 guardPoseFiring                           ;@line 1161
						JumpF ::temp144 _label226                                ;@line 1161
						FAdd ::temp143 guardPoseFireAt 1.000000                  ;@line 1161
						CompareGTE ::temp145 now ::temp143                       ;@line 1161
						Cast ::temp144 ::temp145                                 ;@line 1161
					_label226:
						JumpF ::temp144 _label227                                ;@line 1161
						CallMethod SetGuardFirePose self ::temp142 False updateGeneration updateToken  ;@line 1162
						Jump _label227                                           ;@line 1162
					_label227:
						CallMethod Current self ::temp145 updateGeneration updateToken  ;@line 1164
						Not ::temp142 ::temp145                                  ;@line 1164
						JumpF ::temp142 _label228                                ;@line 1164
						Return None                                              ;@line 1165
						Jump _label228                                           ;@line 1165
					_label228:
						CallStatic utility IsInMenuMode ::temp144                ;@line 1167
						Assign menuOpen ::temp144                                ;@line 1167
						CallMethod Current self ::temp145 updateGeneration updateToken  ;@line 1168
						Not ::temp142 ::temp145                                  ;@line 1168
						JumpF ::temp142 _label229                                ;@line 1168
						Return None                                              ;@line 1169
						Jump _label229                                           ;@line 1169
					_label229:
						Cast ::temp144 menuOpen                                  ;@line 1171
						JumpF ::temp144 _label230                                ;@line 1171
						CompareEQ ::temp144 phase 1                              ;@line 1171
						Cast ::temp142 ::temp144                                 ;@line 1171
						JumpT ::temp142 _label231                                ;@line 1171
						CompareEQ ::temp145 phase 2                              ;@line 1171
						Cast ::temp142 ::temp145                                 ;@line 1171
					_label231:
						Cast ::temp144 ::temp142                                 ;@line 1171
					_label230:
						JumpF ::temp144 _label232                                ;@line 1171
						CallMethod AbortShot self ::NoneVar updateGeneration updateToken  ;@line 1172
						Jump _label232                                           ;@line 1172
					_label232:
						CallMethod Current self ::temp145 updateGeneration updateToken  ;@line 1174
						Not ::temp142 ::temp145                                  ;@line 1174
						JumpF ::temp142 _label233                                ;@line 1174
						Return None                                              ;@line 1175
						Jump _label233                                           ;@line 1175
					_label233:
						CompareEQ ::temp144 phase 1                              ;@line 1177
						JumpF ::temp144 _label234                                ;@line 1177
						Assign releaseDelay ::ReleaseSeconds_var                 ;@line 1179
						CallMethod Finite self ::temp145 releaseDelay 0.066667 1.000000  ;@line 1180
						Not ::temp142 ::temp145                                  ;@line 1180
						Cast ::temp142 ::temp142                                 ;@line 1180
						JumpT ::temp142 _label235                                ;@line 1180
						CompareGT ::temp145 releaseDelay ::FireSeconds_var       ;@line 1180
						Cast ::temp142 ::temp145                                 ;@line 1180
					_label235:
						JumpF ::temp142 _label236                                ;@line 1180
						Assign releaseDelay 0.066667                             ;@line 1181
						Jump _label236                                           ;@line 1181
					_label236:
						FAdd ::temp143 phaseAt releaseDelay                      ;@line 1183
						CompareGTE ::temp145 now ::temp143                       ;@line 1183
						JumpF ::temp145 _label237                                ;@line 1183
						CallMethod CommitShot self ::NoneVar shotTarget updateGeneration updateToken  ;@line 1184
						Jump _label237                                           ;@line 1184
					_label237:
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 0.050000  ;@line 1186
						Return None                                              ;@line 1187
						Jump _label238                                           ;@line 1187
					_label234:
						CompareEQ ::temp142 phase 2                              ;@line 1188
						JumpF ::temp142 _label239                                ;@line 1188
						Assign fireDelay ::FireSeconds_var                       ;@line 1189
						CallMethod Finite self ::temp145 fireDelay 0.200000 2.000000  ;@line 1190
						Not ::temp145 ::temp145                                  ;@line 1190
						JumpF ::temp145 _label240                                ;@line 1190
						Assign fireDelay 0.200000                                ;@line 1191
						Jump _label240                                           ;@line 1191
					_label240:
						FAdd ::temp143 phaseAt fireDelay                         ;@line 1193
						CompareGTE ::temp145 now ::temp143                       ;@line 1193
						JumpF ::temp145 _label241                                ;@line 1193
						CallMethod StartReset self ::NoneVar updateGeneration updateToken  ;@line 1194
						Jump _label241                                           ;@line 1194
					_label241:
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 0.050000  ;@line 1196
						Return None                                              ;@line 1197
						Jump _label238                                           ;@line 1197
					_label239:
						CompareEQ ::temp145 phase 3                              ;@line 1198
						JumpF ::temp145 _label238                                ;@line 1198
						Assign resetDelay ::ResetSeconds_var                     ;@line 1199
						CallMethod Finite self ::temp142 resetDelay 0.800000 5.000000  ;@line 1200
						Not ::temp142 ::temp142                                  ;@line 1200
						JumpF ::temp142 _label242                                ;@line 1200
						Assign resetDelay 0.800000                               ;@line 1201
						Jump _label242                                           ;@line 1201
					_label242:
						FAdd ::temp143 phaseAt resetDelay                        ;@line 1203
						CompareGTE ::temp142 now ::temp143                       ;@line 1203
						JumpF ::temp142 _label243                                ;@line 1203
						CallMethod SetVisualBolt self ::NoneVar 1.000000 updateGeneration updateToken  ;@line 1204
						CallMethod Current self ::temp146 updateGeneration updateToken  ;@line 1205
						Not ::temp146 ::temp146                                  ;@line 1205
						JumpF ::temp146 _label244                                ;@line 1205
						Return None                                              ;@line 1206
						Jump _label244                                           ;@line 1206
					_label244:
						Assign phase 0                                           ;@line 1208
						Cast ::temp147 None                                      ;@line 1209
						Assign shotTarget ::temp147                              ;@line 1209
						Jump _label243                                           ;@line 1209
					_label243:
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 0.050000  ;@line 1211
						Return None                                              ;@line 1212
						Jump _label238                                           ;@line 1212
					_label238:
						JumpF menuOpen _label245                                 ;@line 1214
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 1.000000  ;@line 1215
						Return None                                              ;@line 1216
						Jump _label245                                           ;@line 1216
					_label245:
						CallMethod ChooseVisualTarget self ::temp147 now updateGeneration updateToken  ;@line 1218
						Assign target ::temp147                                  ;@line 1218
						CallMethod SampleVisualTarget self ::temp146 target updateGeneration updateToken  ;@line 1219
						Assign sampled ::temp146                                 ;@line 1219
						CallMethod Current self ::temp142 updateGeneration updateToken  ;@line 1220
						Not ::temp145 ::temp142                                  ;@line 1220
						JumpF ::temp145 _label246                                ;@line 1220
						Return None                                              ;@line 1221
						Jump _label246                                           ;@line 1221
					_label246:
						Cast ::temp146 sampled                                   ;@line 1224
						JumpF ::temp146 _label247                                ;@line 1224
						CallMethod ValidTarget self ::temp144 target updateGeneration updateToken  ;@line 1224
						Cast ::temp146 ::temp144                                 ;@line 1224
					_label247:
						JumpF ::temp146 _label248                                ;@line 1224
						CallMethod SampleTarget self ::temp142 target updateGeneration updateToken  ;@line 1225
						Jump _label248                                           ;@line 1225
					_label248:
						CallMethod Current self ::temp145 updateGeneration updateToken  ;@line 1227
						Not ::temp144 ::temp145                                  ;@line 1227
						JumpF ::temp144 _label249                                ;@line 1227
						Return None                                              ;@line 1228
						Jump _label249                                           ;@line 1228
					_label249:
						JumpF sampled _label250                                  ;@line 1230
						CallMethod TurnToward self ::NoneVar dt updateGeneration updateToken  ;@line 1231
						Jump _label250                                           ;@line 1231
					_label250:
						CallMethod Current self ::temp142 updateGeneration updateToken  ;@line 1233
						Not ::temp146 ::temp142                                  ;@line 1233
						JumpF ::temp146 _label251                                ;@line 1233
						Return None                                              ;@line 1234
						Jump _label251                                           ;@line 1234
					_label251:
						CallMethod PositionOperator self ::temp145 updateGeneration updateToken  ;@line 1236
						Assign positioned ::temp145                              ;@line 1236
						CallMethod Current self ::temp144 updateGeneration updateToken  ;@line 1237
						Not ::temp142 ::temp144                                  ;@line 1237
						JumpF ::temp142 _label252                                ;@line 1237
						Return None                                              ;@line 1238
						Jump _label252                                           ;@line 1238
					_label252:
						Not ::temp146 positioned                                 ;@line 1240
						JumpF ::temp146 _label253                                ;@line 1240
						Assign faulted True                                      ;@line 1241
						CallMethod Shutdown self ::NoneVar                       ;@line 1242
						Return None                                              ;@line 1243
						Jump _label253                                           ;@line 1243
					_label253:
						CompareGTE ::temp145 now nextShotAt                      ;@line 1246
						JumpF ::temp145 _label254                                ;@line 1246
						CallMethod ShotPreflight self ::temp144 target updateGeneration updateToken  ;@line 1247
						Assign aligned ::temp144                                 ;@line 1247
						CallMethod Current self ::temp142 updateGeneration updateToken  ;@line 1248
						Not ::temp146 ::temp142                                  ;@line 1248
						JumpF ::temp146 _label255                                ;@line 1248
						Return None                                              ;@line 1249
						Jump _label255                                           ;@line 1249
					_label255:
						JumpF aligned _label256                                  ;@line 1251
						CallMethod BeginShot self ::NoneVar target updateGeneration updateToken  ;@line 1252
						Jump _label256                                           ;@line 1252
					_label256:
						Jump _label254                                           ;@line 1252
					_label254:
						CallMethod Current self ::temp144 updateGeneration updateToken  ;@line 1255
						JumpF ::temp144 _label257                                ;@line 1255
						CompareEQ ::temp142 phase 1                              ;@line 1256
						JumpF ::temp142 _label258                                ;@line 1256
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 0.020000  ;@line 1257
						Jump _label259                                           ;@line 1257
					_label258:
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 0.050000  ;@line 1259
					_label259:
						Jump _label257                                           ;@line 1259
					_label257:
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
						.local ::temp8 Bool
						.local ::temp9 Bool
					.endLocalTable
					.code
						Cast ::temp8 ::AllowPlayerTakeover_var                   ;@line 148
						JumpF ::temp8 _label260                                  ;@line 148
						Not ::temp8 stationRetired                               ;@line 148
						Cast ::temp8 ::temp8                                     ;@line 148
					_label260:
						Cast ::temp8 ::temp8                                     ;@line 148
						JumpF ::temp8 _label261                                  ;@line 148
						Not ::temp9 destroyed                                    ;@line 148
						Cast ::temp8 ::temp9                                     ;@line 148
					_label261:
						Cast ::temp9 ::temp8                                     ;@line 148
						JumpF ::temp9 _label262                                  ;@line 148
						Cast ::temp9 playerReserved                              ;@line 148
					_label262:
						Cast ::temp9 ::temp9                                     ;@line 148
						JumpF ::temp9 _label263                                  ;@line 148
						CompareGT ::temp8 lease 0                                ;@line 148
						Cast ::temp9 ::temp8                                     ;@line 148
					_label263:
						Cast ::temp9 ::temp9                                     ;@line 148
						JumpF ::temp9 _label264                                  ;@line 148
						CompareEQ ::temp8 playerLease lease                      ;@line 148
						Cast ::temp9 ::temp8                                     ;@line 148
					_label264:
						Return ::temp9                                           ;@line 148
					.endCode
				.endFunction
				.function StationSceneAvailable
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
					.localTable
						.local ::temp10 Bool
						.local ::temp11 Int
						.local ::temp12 ObjectReference
					.endLocalTable
					.code
						Not ::temp10 ::AllowPlayerTakeover_var                   ;@line 152
						JumpF ::temp10 _label265                                 ;@line 152
						Return True                                              ;@line 153
						Jump _label265                                           ;@line 153
					_label265:
						CallStatic skse GetPluginVersion ::temp11 "AstraSight"   ;@line 158
						CompareLT ::temp10 ::temp11 50659328                     ;@line 158
						JumpF ::temp10 _label266                                 ;@line 158
						Return True                                              ;@line 159
						Jump _label266                                           ;@line 159
					_label266:
						Cast ::temp12 self                                       ;@line 163
						CallStatic astrasightnative IsEffectsQuiescent ::temp10 ::temp12 0  ;@line 163
						Return ::temp10                                          ;@line 163
					.endCode
				.endFunction
				.function LoadGuardAnimation
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
					.localTable
						.local ::temp148 form
						.local ::temp149 Faction
						.local ::temp150 Idle
						.local ::temp151 Int
						.local ::temp152 Bool
						.local ::temp153 Bool
					.endLocalTable
					.code
						CallStatic game GetFormFromFile ::temp148 2048 "AstraAsedio_GuardAnim.esp"  ;@line 1266
						Cast ::temp149 ::temp148                                 ;@line 1266
						Assign poseFaction ::temp149                             ;@line 1266
						CallStatic game GetFormFromFile ::temp148 2049 "AstraAsedio_GuardAnim.esp"  ;@line 1267
						Cast ::temp149 ::temp148                                 ;@line 1267
						Assign fireFaction ::temp149                             ;@line 1267
						CallStatic game GetFormFromFile ::temp148 2050 "AstraAsedio_GuardAnim.esp"  ;@line 1268
						Cast ::temp150 ::temp148                                 ;@line 1268
						Assign holdIdle ::temp150                                ;@line 1268
						CallStatic game GetFormFromFile ::temp148 2051 "AstraAsedio_GuardAnim.esp"  ;@line 1269
						Cast ::temp150 ::temp148                                 ;@line 1269
						Assign exitIdle ::temp150                                ;@line 1269
						CallStatic skse GetPluginVersion ::temp151 "OpenAnimationReplacer"  ;@line 1270
						CompareGTE ::temp152 ::temp151 0                         ;@line 1270
						Cast ::temp152 ::temp152                                 ;@line 1270
						JumpF ::temp152 _label267                                ;@line 1270
						Cast ::temp149 None                                      ;@line 1270
						CompareEQ ::temp153 poseFaction ::temp149                ;@line 1270
						Not ::temp153 ::temp153                                  ;@line 1270
						Cast ::temp152 ::temp153                                 ;@line 1270
					_label267:
						Cast ::temp152 ::temp152                                 ;@line 1270
						JumpF ::temp152 _label268                                ;@line 1270
						Cast ::temp149 None                                      ;@line 1270
						CompareEQ ::temp153 fireFaction ::temp149                ;@line 1270
						Not ::temp153 ::temp153                                  ;@line 1270
						Cast ::temp152 ::temp153                                 ;@line 1270
					_label268:
						Cast ::temp152 ::temp152                                 ;@line 1270
						JumpF ::temp152 _label269                                ;@line 1270
						Cast ::temp150 None                                      ;@line 1270
						CompareEQ ::temp153 holdIdle ::temp150                   ;@line 1270
						Not ::temp153 ::temp153                                  ;@line 1270
						Cast ::temp152 ::temp153                                 ;@line 1270
					_label269:
						Cast ::temp152 ::temp152                                 ;@line 1270
						JumpF ::temp152 _label270                                ;@line 1270
						Cast ::temp150 None                                      ;@line 1270
						CompareEQ ::temp153 exitIdle ::temp150                   ;@line 1270
						Not ::temp153 ::temp153                                  ;@line 1270
						Cast ::temp152 ::temp153                                 ;@line 1270
					_label270:
						Return ::temp152                                         ;@line 1270
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
						.local ::temp72 Bool
						.local ::temp73 Bool
						.local ::temp74 Float
						.local ::NoneVar None
						.local yc Float
						.local ys Float
						.local pc Float
						.local ps Float
						.local j Int
						.local ::temp75 Float
						.local ::temp76 Int
						.local ::temp77 Float
					.endLocalTable
					.code
						CallMethod Current self ::temp72 expectedGeneration expectedToken  ;@line 733
						Not ::temp72 ::temp72                                    ;@line 733
						Cast ::temp72 ::temp72                                   ;@line 733
						JumpT ::temp72 _label271                                 ;@line 733
						Not ::temp73 matricesReady                               ;@line 733
						Cast ::temp72 ::temp73                                   ;@line 733
					_label271:
						JumpF ::temp72 _label272                                 ;@line 733
						Return None                                              ;@line 734
						Jump _label272                                           ;@line 734
					_label272:
						CallStatic math Cos ::temp74 yaw                         ;@line 736
						Assign yc ::temp74                                       ;@line 736
						CallStatic math Sin ::temp74 yaw                         ;@line 737
						Assign ys ::temp74                                       ;@line 737
						FNegate ::temp74 pitch                                   ;@line 738
						CallStatic math Cos ::temp74 ::temp74                    ;@line 738
						Assign pc ::temp74                                       ;@line 738
						FNegate ::temp74 pitch                                   ;@line 739
						CallStatic math Sin ::temp74 ::temp74                    ;@line 739
						Assign ps ::temp74                                       ;@line 739
						CallMethod Current self ::temp73 expectedGeneration expectedToken  ;@line 740
						Not ::temp72 ::temp73                                    ;@line 740
						JumpF ::temp72 _label273                                 ;@line 740
						Return None                                              ;@line 741
						Jump _label273                                           ;@line 741
					_label273:
						Assign j 0                                               ;@line 743
					_label275:
						CompareLT ::temp73 j 3                                   ;@line 744
						JumpF ::temp73 _label274                                 ;@line 744
						ArrayGetElement ::temp75 yawBase j                       ;@line 745
						FMultiply ::temp75 yc ::temp75                           ;@line 745
						IAdd ::temp76 j 3                                        ;@line 745
						ArrayGetElement ::temp77 yawBase ::temp76                ;@line 745
						FMultiply ::temp77 ys ::temp77                           ;@line 745
						FSubtract ::temp75 ::temp75 ::temp77                     ;@line 745
						Assign ::temp74 ::temp75                                 ;@line 745
						ArraySetElement yawMatrix j ::temp74                     ;@line 745
						ArrayGetElement ::temp74 yawBase j                       ;@line 746
						FMultiply ::temp75 ys ::temp74                           ;@line 746
						IAdd ::temp76 j 3                                        ;@line 746
						ArrayGetElement ::temp74 yawBase ::temp76                ;@line 746
						FMultiply ::temp74 yc ::temp74                           ;@line 746
						FAdd ::temp75 ::temp75 ::temp74                          ;@line 746
						Assign ::temp77 ::temp75                                 ;@line 746
						IAdd ::temp76 j 3                                        ;@line 746
						ArraySetElement yawMatrix ::temp76 ::temp77              ;@line 746
						IAdd ::temp76 j 6                                        ;@line 747
						ArrayGetElement ::temp77 yawBase ::temp76                ;@line 747
						Assign ::temp74 ::temp77                                 ;@line 747
						IAdd ::temp76 j 6                                        ;@line 747
						ArraySetElement yawMatrix ::temp76 ::temp74              ;@line 747
						ArrayGetElement ::temp74 pitchBase j                     ;@line 748
						Assign ::temp75 ::temp74                                 ;@line 748
						ArraySetElement pitchMatrix j ::temp75                   ;@line 748
						IAdd ::temp76 j 3                                        ;@line 749
						ArrayGetElement ::temp75 pitchBase ::temp76              ;@line 749
						FMultiply ::temp74 pc ::temp75                           ;@line 749
						IAdd ::temp76 j 6                                        ;@line 749
						ArrayGetElement ::temp75 pitchBase ::temp76              ;@line 749
						FMultiply ::temp75 ps ::temp75                           ;@line 749
						FSubtract ::temp74 ::temp74 ::temp75                     ;@line 749
						Assign ::temp77 ::temp74                                 ;@line 749
						IAdd ::temp76 j 3                                        ;@line 749
						ArraySetElement pitchMatrix ::temp76 ::temp77            ;@line 749
						IAdd ::temp76 j 3                                        ;@line 750
						ArrayGetElement ::temp77 pitchBase ::temp76              ;@line 750
						FMultiply ::temp74 ps ::temp77                           ;@line 750
						IAdd ::temp76 j 6                                        ;@line 750
						ArrayGetElement ::temp77 pitchBase ::temp76              ;@line 750
						FMultiply ::temp77 pc ::temp77                           ;@line 750
						FAdd ::temp74 ::temp74 ::temp77                          ;@line 750
						Assign ::temp75 ::temp74                                 ;@line 750
						IAdd ::temp76 j 6                                        ;@line 750
						ArraySetElement pitchMatrix ::temp76 ::temp75            ;@line 750
						IAdd ::temp76 j 1                                        ;@line 751
						Assign j ::temp76                                        ;@line 751
						Jump _label275                                           ;@line 751
					_label274:
						CallMethod WriteAimNode self ::NoneVar ::YawNode_var yawMatrix expectedGeneration expectedToken  ;@line 755
						CallMethod Current self ::temp72 expectedGeneration expectedToken  ;@line 756
						Not ::temp73 ::temp72                                    ;@line 756
						JumpF ::temp73 _label276                                 ;@line 756
						Return None                                              ;@line 757
						Jump _label276                                           ;@line 757
					_label276:
						CallMethod WriteAimNode self ::NoneVar ::PitchNode_var pitchMatrix expectedGeneration expectedToken  ;@line 759
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
						.local ::temp64 Bool
						.local ::temp65 ObjectReference
					.endLocalTable
					.code
						Cast ::temp64 sceneBusy                                  ;@line 692
						JumpT ::temp64 _label277                                 ;@line 692
						CallMethod Current self ::temp64 expectedGeneration expectedToken  ;@line 692
						Not ::temp64 ::temp64                                    ;@line 692
						Cast ::temp64 ::temp64                                   ;@line 692
					_label277:
						JumpF ::temp64 _label278                                 ;@line 692
						Return None                                              ;@line 693
						Jump _label278                                           ;@line 693
					_label278:
						Assign sceneBusy True                                    ;@line 695
						Cast ::temp65 self                                       ;@line 696
						CallStatic netimmerse SetNodeLocalRotationMatrix ::temp64 ::temp65 node matrix False  ;@line 696
						CallMethod FinishSceneEffect self ::temp64 expectedGeneration expectedToken  ;@line 697
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
						.local ::temp61 Bool
						.local started Bool
						.local valid Bool
					.endLocalTable
					.code
						Cast ::temp61 sceneBusy                                  ;@line 673
						JumpT ::temp61 _label279                                 ;@line 673
						CallMethod Current self ::temp61 expectedGeneration expectedToken  ;@line 673
						Not ::temp61 ::temp61                                    ;@line 673
						Cast ::temp61 ::temp61                                   ;@line 673
					_label279:
						JumpF ::temp61 _label280                                 ;@line 673
						Return False                                             ;@line 674
						Jump _label280                                           ;@line 674
					_label280:
						Assign sceneBusy True                                    ;@line 676
						CallMethod PlayGamebryoAnimation self ::temp61 name True 0.000000  ;@line 677
						Assign started ::temp61                                  ;@line 677
						CallMethod FinishSceneEffect self ::temp61 expectedGeneration expectedToken  ;@line 678
						Assign valid ::temp61                                    ;@line 678
						Cast ::temp61 valid                                      ;@line 679
						JumpF ::temp61 _label281                                 ;@line 679
						Cast ::temp61 started                                    ;@line 679
					_label281:
						Return ::temp61                                          ;@line 679
					.endCode
				.endFunction
				.function CaptureMatrices
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
					.localTable
						.local ::temp66 Int
						.local ::temp67 Bool
						.local ::temp68 Bool
						.local ::temp69 ObjectReference
						.local ::temp70 Float[]
						.local ::temp71 Float
						.local captureGeneration Int
					.endLocalTable
					.code
						Assign captureGeneration generation                      ;@line 701
						CallStatic skse GetVersion ::temp66                      ;@line 702
						CompareLT ::temp67 ::temp66 2                            ;@line 702
						Cast ::temp67 ::temp67                                   ;@line 702
						JumpT ::temp67 _label282                                 ;@line 702
						CallMethod Is3DLoaded self ::temp68                      ;@line 702
						Not ::temp68 ::temp68                                    ;@line 702
						Cast ::temp67 ::temp68                                   ;@line 702
					_label282:
						JumpF ::temp67 _label283                                 ;@line 702
						Return False                                             ;@line 703
						Jump _label283                                           ;@line 703
					_label283:
						Cast ::temp69 self                                       ;@line 705
						CallStatic netimmerse HasNode ::temp68 ::temp69 ::YawNode_var False  ;@line 705
						Not ::temp67 ::temp68                                    ;@line 705
						Cast ::temp67 ::temp67                                   ;@line 705
						JumpT ::temp67 _label284                                 ;@line 705
						Cast ::temp69 self                                       ;@line 705
						CallStatic netimmerse HasNode ::temp68 ::temp69 ::PitchNode_var False  ;@line 705
						Not ::temp68 ::temp68                                    ;@line 705
						Cast ::temp67 ::temp68                                   ;@line 705
					_label284:
						Cast ::temp67 ::temp67                                   ;@line 705
						JumpT ::temp67 _label285                                 ;@line 705
						Cast ::temp69 self                                       ;@line 705
						CallStatic netimmerse HasNode ::temp68 ::temp69 ::MuzzleNode_var False  ;@line 705
						Not ::temp68 ::temp68                                    ;@line 705
						Cast ::temp67 ::temp68                                   ;@line 705
					_label285:
						Cast ::temp67 ::temp67                                   ;@line 705
						JumpT ::temp67 _label286                                 ;@line 705
						Cast ::temp69 self                                       ;@line 705
						CallStatic netimmerse HasNode ::temp68 ::temp69 ::VisualBoltNode_var False  ;@line 705
						Not ::temp68 ::temp68                                    ;@line 705
						Cast ::temp67 ::temp68                                   ;@line 705
					_label286:
						JumpF ::temp67 _label287                                 ;@line 705
						Return False                                             ;@line 706
						Jump _label287                                           ;@line 706
					_label287:
						CompareEQ ::temp68 generation captureGeneration          ;@line 708
						Not ::temp68 ::temp68                                    ;@line 708
						Cast ::temp68 ::temp68                                   ;@line 708
						JumpT ::temp68 _label288                                 ;@line 708
						CompareEQ ::temp67 token -1                              ;@line 708
						Not ::temp67 ::temp67                                    ;@line 708
						Cast ::temp68 ::temp67                                   ;@line 708
					_label288:
						Cast ::temp68 ::temp68                                   ;@line 708
						JumpT ::temp68 _label289                                 ;@line 708
						Not ::temp67 recovering                                  ;@line 708
						Cast ::temp68 ::temp67                                   ;@line 708
					_label289:
						JumpF ::temp68 _label290                                 ;@line 708
						Return False                                             ;@line 709
						Jump _label290                                           ;@line 709
					_label290:
						ArrayCreate ::temp70 9                                   ;@line 714
						Assign yawBase ::temp70                                  ;@line 714
						ArrayCreate ::temp70 9                                   ;@line 715
						Assign pitchBase ::temp70                                ;@line 715
						ArrayCreate ::temp70 9                                   ;@line 716
						Assign yawMatrix ::temp70                                ;@line 716
						ArrayCreate ::temp70 9                                   ;@line 717
						Assign pitchMatrix ::temp70                              ;@line 717
						ArrayCreate ::temp70 9                                   ;@line 718
						Assign rootWorldMatrix ::temp70                          ;@line 718
						ArrayCreate ::temp70 9                                   ;@line 719
						Assign muzzleWorldMatrix ::temp70                        ;@line 719
						ArrayCreate ::temp70 3                                   ;@line 720
						Assign rootPosition ::temp70                             ;@line 720
						ArrayCreate ::temp70 3                                   ;@line 721
						Assign muzzlePosition ::temp70                           ;@line 721
						Assign ::temp71 1.000000                                 ;@line 722
						ArraySetElement yawBase 0 ::temp71                       ;@line 722
						Assign ::temp71 1.000000                                 ;@line 723
						ArraySetElement yawBase 4 ::temp71                       ;@line 723
						Assign ::temp71 1.000000                                 ;@line 724
						ArraySetElement yawBase 8 ::temp71                       ;@line 724
						Assign ::temp71 1.000000                                 ;@line 725
						ArraySetElement pitchBase 0 ::temp71                     ;@line 725
						Assign ::temp71 1.000000                                 ;@line 726
						ArraySetElement pitchBase 4 ::temp71                     ;@line 726
						Assign ::temp71 1.000000                                 ;@line 727
						ArraySetElement pitchBase 8 ::temp71                     ;@line 727
						Assign matricesReady True                                ;@line 728
						Return True                                              ;@line 729
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
						.local ::temp139 Float
						.local ::temp140 Bool
						.local now Float
						.local started Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallStatic utility GetCurrentRealTime ::temp139          ;@line 1086
						Assign now ::temp139                                     ;@line 1086
						CallMethod Current self ::temp140 expectedGeneration expectedToken  ;@line 1087
						Not ::temp140 ::temp140                                  ;@line 1087
						JumpF ::temp140 _label291                                ;@line 1087
						Return None                                              ;@line 1088
						Jump _label291                                           ;@line 1088
					_label291:
						Assign phase 3                                           ;@line 1090
						Assign phaseAt now                                       ;@line 1091
						CallMethod PlaySceneAnimation self ::temp140 "Reset" expectedGeneration expectedToken  ;@line 1092
						Assign started ::temp140                                 ;@line 1092
						CallMethod Current self ::temp140 expectedGeneration expectedToken  ;@line 1093
						Not ::temp140 ::temp140                                  ;@line 1093
						JumpF ::temp140 _label292                                ;@line 1093
						Return None                                              ;@line 1094
						Jump _label292                                           ;@line 1094
					_label292:
						Not ::temp140 started                                    ;@line 1096
						JumpF ::temp140 _label293                                ;@line 1096
						Assign faulted True                                      ;@line 1097
						CallMethod Shutdown self ::NoneVar                       ;@line 1098
						Jump _label293                                           ;@line 1098
					_label293:
					.endCode
				.endFunction
				.function RetireStation
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
					.localTable
						.local ::temp3 Bool
						.local ::temp4 Bool
						.local ::temp5 actor
						.local ::NoneVar None
					.endLocalTable
					.code
						Not ::temp3 stationRetired                               ;@line 124
						JumpF ::temp3 _label294                                  ;@line 124
						Assign stationRetired True                               ;@line 125
						CallMethod InvalidatePlayerLease self ::NoneVar          ;@line 126
						CallMethod Shutdown self ::NoneVar                       ;@line 127
						Jump _label294                                           ;@line 127
					_label294:
						Cast ::temp3 pinBusy                                     ;@line 129
						JumpT ::temp3 _label295                                  ;@line 129
						Cast ::temp3 sceneBusy                                   ;@line 129
					_label295:
						JumpF ::temp3 _label296                                  ;@line 129
						Return False                                             ;@line 130
						Jump _label296                                           ;@line 130
					_label296:
						CallMethod ReleaseOwnedGuard self ::NoneVar              ;@line 132
						Not ::temp3 pinBusy                                      ;@line 133
						Cast ::temp3 ::temp3                                     ;@line 133
						JumpF ::temp3 _label297                                  ;@line 133
						Not ::temp4 sceneBusy                                    ;@line 133
						Cast ::temp3 ::temp4                                     ;@line 133
					_label297:
						Cast ::temp3 ::temp3                                     ;@line 133
						JumpF ::temp3 _label298                                  ;@line 133
						Cast ::temp5 None                                        ;@line 133
						CompareEQ ::temp4 ownedGuard ::temp5                     ;@line 133
						Cast ::temp3 ::temp4                                     ;@line 133
					_label298:
						Return ::temp3                                           ;@line 133
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
						.local ::temp62 Bool
						.local ::temp63 ObjectReference
						.local ::NoneVar None
					.endLocalTable
					.code
						Cast ::temp62 sceneBusy                                  ;@line 683
						JumpT ::temp62 _label299                                 ;@line 683
						CallMethod Current self ::temp62 expectedGeneration expectedToken  ;@line 683
						Not ::temp62 ::temp62                                    ;@line 683
						Cast ::temp62 ::temp62                                   ;@line 683
					_label299:
						JumpF ::temp62 _label300                                 ;@line 683
						Return None                                              ;@line 684
						Jump _label300                                           ;@line 684
					_label300:
						Assign sceneBusy True                                    ;@line 686
						Cast ::temp63 self                                       ;@line 687
						CallStatic netimmerse SetNodeScale ::NoneVar ::temp63 ::VisualBoltNode_var scale False  ;@line 687
						CallMethod FinishSceneEffect self ::temp62 expectedGeneration expectedToken  ;@line 688
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
						.local ::temp60 Bool
						.local valid Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod Current self ::temp60 expectedGeneration expectedToken  ;@line 663
						Assign valid ::temp60                                    ;@line 663
						Not ::temp60 valid                                       ;@line 664
						JumpF ::temp60 _label301                                 ;@line 664
						CallMethod RestoreNeutralScene self ::NoneVar            ;@line 665
						Jump _label301                                           ;@line 665
					_label301:
						Assign sceneBusy False                                   ;@line 667
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 668
						Return valid                                             ;@line 669
					.endCode
				.endFunction
				.function InvalidatePlayerLease
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp6 Bool
						.local ::temp7 Int
					.endLocalTable
					.code
						Assign playerReserved False                              ;@line 138
						Assign playerReady False                                 ;@line 139
						Assign playerRestored False                              ;@line 140
						Assign playerLease 0                                     ;@line 141
						CompareLT ::temp6 playerSerial 2000000000                ;@line 142
						JumpF ::temp6 _label302                                  ;@line 142
						IAdd ::temp7 playerSerial 1                              ;@line 143
						Assign playerSerial ::temp7                              ;@line 143
						Jump _label302                                           ;@line 143
					_label302:
					.endCode
				.endFunction
				.function SafeCadenceSeconds
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Float
					.paramTable
					.endParamTable
					.localTable
						.local ::temp33 Bool
					.endLocalTable
					.code
						CallMethod Finite self ::temp33 ::CadenceSeconds_var 2.500000 60.000000  ;@line 330
						Not ::temp33 ::temp33                                    ;@line 330
						JumpF ::temp33 _label303                                 ;@line 330
						Return 2.500000                                          ;@line 331
						Jump _label303                                           ;@line 331
					_label303:
						Return ::CadenceSeconds_var                              ;@line 333
					.endCode
				.endFunction
				.function RestoreNeutralScene
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp56 Bool
						.local loaded Bool
						.local ::NoneVar None
						.local ::temp57 Int
						.local ::temp58 ObjectReference
						.local ::temp59 Bool
					.endLocalTable
					.code
						CallMethod StationSceneAvailable self ::temp56           ;@line 641
						Not ::temp56 ::temp56                                    ;@line 641
						JumpF ::temp56 _label304                                 ;@line 641
						Return None                                              ;@line 642
						Jump _label304                                           ;@line 642
					_label304:
						CallMethod Is3DLoaded self ::temp56                      ;@line 647
						Assign loaded ::temp56                                   ;@line 647
						JumpF loaded _label305                                   ;@line 648
						JumpF ::AllowPlayerTakeover_var _label306                ;@line 649
						CallStatic skse GetPluginVersion ::temp57 "AstraSight"   ;@line 652
						CompareGTE ::temp56 ::temp57 50659392                    ;@line 652
						JumpF ::temp56 _label307                                 ;@line 652
						Cast ::temp58 self                                       ;@line 653
						CallStatic astrasightnative ResetIdleScene ::temp59 ::temp58  ;@line 653
						Jump _label307                                           ;@line 653
					_label307:
						Jump _label308                                           ;@line 653
					_label306:
						CallMethod PlayGamebryoAnimation self ::temp59 "Reset" True 0.000000  ;@line 656
					_label308:
						Cast ::temp58 self                                       ;@line 658
						CallStatic netimmerse SetNodeScale ::NoneVar ::temp58 ::VisualBoltNode_var 1.000000 False  ;@line 658
						Jump _label305                                           ;@line 658
					_label305:
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
				.function ReleaseOwnedGuard
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp52 actor
						.local ::temp53 Bool
						.local previousGuard actor
						.local player actor
						.local ::NoneVar None
					.endLocalTable
					.code
						JumpF pinBusy _label309                                  ;@line 608
						Return None                                              ;@line 609
						Jump _label309                                           ;@line 609
					_label309:
						Assign previousGuard ownedGuard                          ;@line 611
						Cast ::temp52 None                                       ;@line 612
						Assign ownedGuard ::temp52                               ;@line 612
						Cast ::temp52 None                                       ;@line 613
						CompareEQ ::temp53 previousGuard ::temp52                ;@line 613
						JumpF ::temp53 _label310                                 ;@line 613
						Return None                                              ;@line 614
						Jump _label310                                           ;@line 614
					_label310:
						Assign pinBusy True                                      ;@line 616
						CallStatic game GetPlayer ::temp52                       ;@line 617
						Assign player ::temp52                                   ;@line 617
						CompareEQ ::temp53 previousGuard player                  ;@line 618
						Not ::temp53 ::temp53                                    ;@line 618
						JumpF ::temp53 _label311                                 ;@line 618
						CallMethod StopGuardPose self ::NoneVar previousGuard    ;@line 619
						CallMethod SetDontMove previousGuard ::NoneVar False     ;@line 620
						Jump _label311                                           ;@line 620
					_label311:
						Assign pinBusy False                                     ;@line 622
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 623
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
						.local ::temp111 Bool
						.local ::temp112 Float
						.local ::NoneVar None
						.local rate Float
						.local nextYaw Float
						.local nextPitch Float
					.endLocalTable
					.code
						Assign rate ::TurnRate_var                               ;@line 873
						CallMethod Finite self ::temp111 rate 1.000000 30.000000  ;@line 874
						Not ::temp111 ::temp111                                  ;@line 874
						JumpF ::temp111 _label312                                ;@line 874
						Assign rate 30.000000                                    ;@line 875
						Jump _label312                                           ;@line 875
					_label312:
						FMultiply ::temp112 rate dt                              ;@line 877
						CallMethod Approach self ::temp112 yaw desiredYaw ::temp112  ;@line 877
						Assign nextYaw ::temp112                                 ;@line 877
						Assign nextPitch 0.000000                                ;@line 878
						CallMethod Current self ::temp111 expectedGeneration expectedToken  ;@line 879
						Not ::temp111 ::temp111                                  ;@line 879
						JumpF ::temp111 _label313                                ;@line 879
						Return None                                              ;@line 880
						Jump _label313                                           ;@line 880
					_label313:
						Assign yaw nextYaw                                       ;@line 882
						Assign pitch nextPitch                                   ;@line 883
						CallMethod ApplyAim self ::NoneVar expectedGeneration expectedToken  ;@line 884
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
						.local ::temp34 Bool
						.local ::temp35 Bool
						.local ::temp36 Bool
					.endLocalTable
					.code
						Cast ::temp34 pinBusy                                    ;@line 340
						JumpT ::temp34 _label314                                 ;@line 340
						Cast ::temp34 sceneBusy                                  ;@line 340
					_label314:
						Cast ::temp34 ::temp34                                   ;@line 340
						JumpT ::temp34 _label315                                 ;@line 340
						CompareEQ ::temp35 generation expectedGeneration         ;@line 340
						Not ::temp35 ::temp35                                    ;@line 340
						Cast ::temp34 ::temp35                                   ;@line 340
					_label315:
						Cast ::temp35 ::temp34                                   ;@line 340
						JumpT ::temp35 _label316                                 ;@line 340
						Cast ::temp35 destroyed                                  ;@line 340
					_label316:
						Cast ::temp34 ::temp35                                   ;@line 340
						JumpT ::temp34 _label317                                 ;@line 340
						Cast ::temp34 stationRetired                             ;@line 340
					_label317:
						JumpF ::temp34 _label318                                 ;@line 340
						Return False                                             ;@line 341
						Jump _label318                                           ;@line 341
					_label318:
						Not ::temp35 ::AllowPlayerTakeover_var                   ;@line 343
						JumpF ::temp35 _label319                                 ;@line 343
						Return True                                              ;@line 344
						Jump _label319                                           ;@line 344
					_label319:
						CompareGT ::temp34 lease 0                               ;@line 346
						JumpF ::temp34 _label320                                 ;@line 346
						CallMethod PlayerLeaseCurrent self ::temp35 lease        ;@line 347
						Return ::temp35                                          ;@line 347
						Jump _label320                                           ;@line 347
					_label320:
						Cast ::temp34 recovering                                 ;@line 349
						JumpF ::temp34 _label321                                 ;@line 349
						Not ::temp34 playerReserved                              ;@line 349
						Cast ::temp34 ::temp34                                   ;@line 349
					_label321:
						Cast ::temp34 ::temp34                                   ;@line 349
						JumpF ::temp34 _label322                                 ;@line 349
						CompareEQ ::temp36 token -1                              ;@line 349
						Cast ::temp34 ::temp36                                   ;@line 349
					_label322:
						Cast ::temp34 ::temp34                                   ;@line 349
						JumpF ::temp34 _label323                                 ;@line 349
						Not ::temp36 faulted                                     ;@line 349
						Cast ::temp34 ::temp36                                   ;@line 349
					_label323:
						Return ::temp34                                          ;@line 349
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
						CallMethod BlockActivation self ::NoneVar True           ;@line 116
					.endCode
				.endFunction
				.function Shutdown
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp46 Int
						.local ::temp47 actor
						.local ::NoneVar None
						.local ::temp48 Bool
						.local ::temp49 Bool
						.local cleanupGeneration Int
					.endLocalTable
					.code
						Assign running False                                     ;@line 551
						IAdd ::temp46 generation 1                               ;@line 552
						Assign generation ::temp46                               ;@line 552
						Assign cleanupGeneration generation                      ;@line 553
						Assign token -1                                          ;@line 554
						Assign recovering False                                  ;@line 555
						Assign updating False                                    ;@line 556
						Assign phase 0                                           ;@line 557
						Cast ::temp47 None                                       ;@line 558
						Assign shotTarget ::temp47                               ;@line 558
						Cast ::temp47 None                                       ;@line 559
						Assign visualTarget ::temp47                             ;@line 559
						Assign visualScanAt 0.000000                             ;@line 560
						Assign matricesReady False                               ;@line 561
						Assign recoveryRequested False                           ;@line 562
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 563
						CompareEQ ::temp48 generation cleanupGeneration          ;@line 564
						Not ::temp48 ::temp48                                    ;@line 564
						Cast ::temp48 ::temp48                                   ;@line 564
						JumpT ::temp48 _label324                                 ;@line 564
						CompareEQ ::temp49 token -1                              ;@line 564
						Not ::temp49 ::temp49                                    ;@line 564
						Cast ::temp48 ::temp49                                   ;@line 564
					_label324:
						JumpF ::temp48 _label325                                 ;@line 564
						Return None                                              ;@line 565
						Jump _label325                                           ;@line 565
					_label325:
						CallMethod ReleaseOwnedGuard self ::NoneVar              ;@line 569
						CompareEQ ::temp49 generation cleanupGeneration          ;@line 570
						Not ::temp49 ::temp49                                    ;@line 570
						Cast ::temp49 ::temp49                                   ;@line 570
						JumpT ::temp49 _label326                                 ;@line 570
						CompareEQ ::temp48 token -1                              ;@line 570
						Not ::temp48 ::temp48                                    ;@line 570
						Cast ::temp49 ::temp48                                   ;@line 570
					_label326:
						JumpF ::temp49 _label327                                 ;@line 570
						Return None                                              ;@line 571
						Jump _label327                                           ;@line 571
					_label327:
						Not ::temp48 sceneBusy                                   ;@line 573
						JumpF ::temp48 _label328                                 ;@line 573
						Assign sceneBusy True                                    ;@line 574
						CallMethod RestoreNeutralScene self ::NoneVar            ;@line 575
						Assign sceneBusy False                                   ;@line 576
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 577
						Jump _label328                                           ;@line 577
					_label328:
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
						.local ::temp102 Float
						.local ::temp103 Float
						.local ::temp104 Bool
						.local ::temp105 Bool
						.local horizontal Float
						.local cosine Float
						.local angle Float
					.endLocalTable
					.code
						FMultiply ::temp102 vectorX vectorX                      ;@line 837
						FMultiply ::temp103 vectorY vectorY                      ;@line 837
						FAdd ::temp102 ::temp102 ::temp103                       ;@line 837
						CallStatic math Sqrt ::temp103 ::temp102                 ;@line 837
						Assign horizontal ::temp103                              ;@line 837
						CompareLT ::temp104 horizontal 0.000010                  ;@line 838
						JumpF ::temp104 _label329                                ;@line 838
						Return fallback                                          ;@line 839
						Jump _label329                                           ;@line 839
					_label329:
						FDivide ::temp102 vectorY horizontal                     ;@line 841
						Assign cosine ::temp102                                  ;@line 841
						CompareGT ::temp104 cosine 1.000000                      ;@line 842
						JumpF ::temp104 _label330                                ;@line 842
						Assign cosine 1.000000                                   ;@line 843
						Jump _label331                                           ;@line 843
					_label330:
						CompareLT ::temp105 cosine -1.000000                     ;@line 844
						JumpF ::temp105 _label331                                ;@line 844
						Assign cosine -1.000000                                  ;@line 845
						Jump _label331                                           ;@line 845
					_label331:
						CallStatic math ACos ::temp103 cosine                    ;@line 847
						Assign angle ::temp103                                   ;@line 847
						CompareLT ::temp105 vectorX 0.000000                     ;@line 848
						JumpF ::temp105 _label332                                ;@line 848
						FSubtract ::temp102 360.000000 angle                     ;@line 849
						Assign angle ::temp102                                   ;@line 849
						Jump _label332                                           ;@line 849
					_label332:
						CompareGTE ::temp104 angle 360.000000                    ;@line 851
						JumpF ::temp104 _label333                                ;@line 851
						FSubtract ::temp103 angle 360.000000                     ;@line 852
						Assign angle ::temp103                                   ;@line 852
						Jump _label333                                           ;@line 852
					_label333:
						Return angle                                             ;@line 854
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
						Cast ::temp1 running                                     ;@line 120
						JumpF ::temp1 _label334                                  ;@line 120
						Not ::temp1 stationRetired                               ;@line 120
						Cast ::temp1 ::temp1                                     ;@line 120
					_label334:
						Cast ::temp1 ::temp1                                     ;@line 120
						JumpF ::temp1 _label335                                  ;@line 120
						Not ::temp2 playerReserved                               ;@line 120
						Cast ::temp1 ::temp2                                     ;@line 120
					_label335:
						Cast ::temp1 ::temp1                                     ;@line 120
						JumpF ::temp1 _label336                                  ;@line 120
						Not ::temp2 recovering                                   ;@line 120
						Cast ::temp1 ::temp2                                     ;@line 120
					_label336:
						Cast ::temp1 ::temp1                                     ;@line 120
						JumpF ::temp1 _label337                                  ;@line 120
						Not ::temp2 destroyed                                    ;@line 120
						Cast ::temp1 ::temp2                                     ;@line 120
					_label337:
						Cast ::temp1 ::temp1                                     ;@line 120
						JumpF ::temp1 _label338                                  ;@line 120
						Not ::temp2 faulted                                      ;@line 120
						Cast ::temp1 ::temp2                                     ;@line 120
					_label338:
						Cast ::temp1 ::temp1                                     ;@line 120
						JumpF ::temp1 _label339                                  ;@line 120
						CompareEQ ::temp2 generation expectedGeneration          ;@line 120
						Cast ::temp1 ::temp2                                     ;@line 120
					_label339:
						Cast ::temp1 ::temp1                                     ;@line 120
						JumpF ::temp1 _label340                                  ;@line 120
						CompareEQ ::temp2 token expectedToken                    ;@line 120
						Cast ::temp1 ::temp2                                     ;@line 120
					_label340:
						Cast ::temp1 ::temp1                                     ;@line 120
						JumpF ::temp1 _label341                                  ;@line 120
						CompareGT ::temp2 token 0                                ;@line 120
						Cast ::temp1 ::temp2                                     ;@line 120
					_label341:
						Return ::temp1                                           ;@line 120
					.endCode
				.endFunction
				.function BeginRecovery
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp37 Bool
						.local ::temp42 ObjectReference
						.local ::temp43 weapon
						.local ::temp44 ammo
						.local ::temp45 Float
						.local probeGeneration Int
						.local sceneFree Bool
						.local ::temp38 Int
						.local ::temp39 actor
						.local ::temp40 Bool
						.local ::temp41 Bool
						.local deferredGeneration Int
						.local loaded Bool
						.local ::NoneVar None
						.local recoveryGeneration Int
						.local player actor
						.local gunLoaded Bool
						.local guardLoaded Bool
						.local guardDead Bool
						.local guardDisabled Bool
						.local placed Bool
						.local captured Bool
						.local distance Float
						.local movingGuard actor
						.local recoveryPoint ObjectReference
						.local moveCurrent Bool
						.local aliveAfterMove Bool
						.local pinAcquired Bool
						.local recoveryToken Int
						.local now Float
						.local resetStarted Bool
						.local positioned Bool
						.local posed Bool
					.endLocalTable
					.code
						Cast ::temp37 playerReserved                             ;@line 353
						JumpT ::temp37 _label342                                 ;@line 353
						Cast ::temp37 stationRetired                             ;@line 353
					_label342:
						JumpF ::temp37 _label343                                 ;@line 353
						Return None                                              ;@line 354
						Jump _label343                                           ;@line 354
					_label343:
						Assign probeGeneration generation                        ;@line 356
						CallMethod StationSceneAvailable self ::temp37           ;@line 357
						Assign sceneFree ::temp37                                ;@line 357
						CompareEQ ::temp37 generation probeGeneration            ;@line 358
						Not ::temp37 ::temp37                                    ;@line 358
						Cast ::temp37 ::temp37                                   ;@line 358
						JumpT ::temp37 _label344                                 ;@line 358
						Cast ::temp37 playerReserved                             ;@line 358
					_label344:
						JumpF ::temp37 _label345                                 ;@line 358
						Return None                                              ;@line 359
						Jump _label345                                           ;@line 359
					_label345:
						Not ::temp37 sceneFree                                   ;@line 361
						JumpF ::temp37 _label346                                 ;@line 361
						Assign running False                                     ;@line 362
						IAdd ::temp38 generation 1                               ;@line 363
						Assign generation ::temp38                               ;@line 363
						Assign deferredGeneration generation                     ;@line 364
						Assign token -1                                          ;@line 365
						Assign recovering False                                  ;@line 366
						Assign updating False                                    ;@line 367
						Assign phase 0                                           ;@line 368
						Cast ::temp39 None                                       ;@line 369
						Assign shotTarget ::temp39                               ;@line 369
						Assign matricesReady False                               ;@line 370
						Assign recoveryRequested True                            ;@line 371
						CallMethod Is3DLoaded self ::temp40                      ;@line 372
						Assign loaded ::temp40                                   ;@line 372
						Cast ::temp40 loaded                                     ;@line 373
						JumpF ::temp40 _label347                                 ;@line 373
						CompareEQ ::temp40 generation deferredGeneration         ;@line 373
						Cast ::temp40 ::temp40                                   ;@line 373
					_label347:
						Cast ::temp40 ::temp40                                   ;@line 373
						JumpF ::temp40 _label348                                 ;@line 373
						Not ::temp41 playerReserved                              ;@line 373
						Cast ::temp40 ::temp41                                   ;@line 373
					_label348:
						Cast ::temp40 ::temp40                                   ;@line 373
						JumpF ::temp40 _label349                                 ;@line 373
						Not ::temp41 pinBusy                                     ;@line 373
						Cast ::temp40 ::temp41                                   ;@line 373
					_label349:
						Cast ::temp40 ::temp40                                   ;@line 373
						JumpF ::temp40 _label350                                 ;@line 373
						Not ::temp41 sceneBusy                                   ;@line 373
						Cast ::temp40 ::temp41                                   ;@line 373
					_label350:
						JumpF ::temp40 _label351                                 ;@line 373
						CallMethod RegisterForSingleUpdate self ::NoneVar 0.200000  ;@line 374
						Jump _label351                                           ;@line 374
					_label351:
						Return None                                              ;@line 376
						Jump _label346                                           ;@line 376
					_label346:
						Assign running False                                     ;@line 378
						IAdd ::temp38 generation 1                               ;@line 379
						Assign generation ::temp38                               ;@line 379
						Assign recoveryGeneration generation                     ;@line 380
						Assign token -1                                          ;@line 381
						IAdd ::temp38 serial 1                                   ;@line 382
						Assign serial ::temp38                                   ;@line 382
						Assign recovering True                                   ;@line 383
						Assign updating False                                    ;@line 384
						Assign phase 0                                           ;@line 385
						Cast ::temp39 None                                       ;@line 386
						Assign shotTarget ::temp39                               ;@line 386
						Assign faulted False                                     ;@line 387
						Assign matricesReady False                               ;@line 388
						Assign recoveryRequested False                           ;@line 389
						CallMethod NormalizeTimingProperties self ::NoneVar      ;@line 391
						Cast ::temp41 pinBusy                                    ;@line 392
						JumpT ::temp41 _label352                                 ;@line 392
						Cast ::temp41 sceneBusy                                  ;@line 392
					_label352:
						JumpF ::temp41 _label353                                 ;@line 392
						Assign recoveryRequested True                            ;@line 395
						Assign recovering False                                  ;@line 396
						Return None                                              ;@line 397
						Jump _label353                                           ;@line 397
					_label353:
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 399
						CompareEQ ::temp40 generation recoveryGeneration         ;@line 400
						Not ::temp40 ::temp40                                    ;@line 400
						Cast ::temp41 ::temp40                                   ;@line 400
						JumpT ::temp41 _label354                                 ;@line 400
						CompareEQ ::temp37 token -1                              ;@line 400
						Not ::temp37 ::temp37                                    ;@line 400
						Cast ::temp41 ::temp37                                   ;@line 400
					_label354:
						JumpF ::temp41 _label355                                 ;@line 400
						Return None                                              ;@line 401
						Jump _label355                                           ;@line 401
					_label355:
						CallMethod ReleaseOwnedGuard self ::NoneVar              ;@line 403
						CompareEQ ::temp40 generation recoveryGeneration         ;@line 404
						Not ::temp40 ::temp40                                    ;@line 404
						Cast ::temp41 ::temp40                                   ;@line 404
						JumpT ::temp41 _label356                                 ;@line 404
						CompareEQ ::temp37 token -1                              ;@line 404
						Not ::temp37 ::temp37                                    ;@line 404
						Cast ::temp41 ::temp37                                   ;@line 404
					_label356:
						JumpF ::temp41 _label357                                 ;@line 404
						Return None                                              ;@line 405
						Jump _label357                                           ;@line 405
					_label357:
						CallStatic game GetPlayer ::temp39                       ;@line 407
						Assign player ::temp39                                   ;@line 407
						CompareEQ ::temp40 generation recoveryGeneration         ;@line 408
						Not ::temp40 ::temp40                                    ;@line 408
						Cast ::temp41 ::temp40                                   ;@line 408
						JumpT ::temp41 _label358                                 ;@line 408
						CompareEQ ::temp37 token -1                              ;@line 408
						Not ::temp37 ::temp37                                    ;@line 408
						Cast ::temp41 ::temp37                                   ;@line 408
					_label358:
						JumpF ::temp41 _label359                                 ;@line 408
						Return None                                              ;@line 409
						Jump _label359                                           ;@line 409
					_label359:
						CallMethod BlockActivation self ::NoneVar True           ;@line 411
						CompareEQ ::temp40 generation recoveryGeneration         ;@line 412
						Not ::temp40 ::temp40                                    ;@line 412
						Cast ::temp41 ::temp40                                   ;@line 412
						JumpT ::temp41 _label360                                 ;@line 412
						CompareEQ ::temp37 token -1                              ;@line 412
						Not ::temp37 ::temp37                                    ;@line 412
						Cast ::temp41 ::temp37                                   ;@line 412
					_label360:
						JumpF ::temp41 _label361                                 ;@line 412
						Return None                                              ;@line 413
						Jump _label361                                           ;@line 413
					_label361:
						Cast ::temp37 destroyed                                  ;@line 415
						JumpT ::temp37 _label362                                 ;@line 415
						Cast ::temp39 None                                       ;@line 415
						CompareEQ ::temp40 ::Artillero_var ::temp39              ;@line 415
						Cast ::temp37 ::temp40                                   ;@line 415
					_label362:
						Cast ::temp40 ::temp37                                   ;@line 415
						JumpT ::temp40 _label363                                 ;@line 415
						CompareEQ ::temp41 ::Artillero_var player                ;@line 415
						Cast ::temp40 ::temp41                                   ;@line 415
					_label363:
						Cast ::temp41 ::temp40                                   ;@line 415
						JumpT ::temp41 _label364                                 ;@line 415
						Cast ::temp42 None                                       ;@line 415
						CompareEQ ::temp37 ::Puesto_var ::temp42                 ;@line 415
						Cast ::temp41 ::temp37                                   ;@line 415
					_label364:
						Cast ::temp37 ::temp41                                   ;@line 415
						JumpT ::temp37 _label365                                 ;@line 415
						Cast ::temp43 None                                       ;@line 415
						CompareEQ ::temp40 ::Launcher_var ::temp43               ;@line 415
						Cast ::temp37 ::temp40                                   ;@line 415
					_label365:
						Cast ::temp40 ::temp37                                   ;@line 415
						JumpT ::temp40 _label366                                 ;@line 415
						Cast ::temp44 None                                       ;@line 415
						CompareEQ ::temp41 ::ShotAmmo_var ::temp44               ;@line 415
						Cast ::temp40 ::temp41                                   ;@line 415
					_label366:
						JumpF ::temp40 _label367                                 ;@line 415
						Assign faulted True                                      ;@line 416
						Assign recovering False                                  ;@line 417
						Return None                                              ;@line 418
						Jump _label367                                           ;@line 418
					_label367:
						CallMethod Is3DLoaded self ::temp37                      ;@line 420
						Assign gunLoaded ::temp37                                ;@line 420
						CallMethod Is3DLoaded ::Artillero_var ::temp41           ;@line 421
						Assign guardLoaded ::temp41                              ;@line 421
						CallMethod IsDead ::Artillero_var ::temp40               ;@line 422
						Assign guardDead ::temp40                                ;@line 422
						CallMethod IsDisabled ::Artillero_var ::temp37           ;@line 423
						Assign guardDisabled ::temp37                            ;@line 423
						CompareEQ ::temp41 generation recoveryGeneration         ;@line 424
						Not ::temp41 ::temp41                                    ;@line 424
						Cast ::temp37 ::temp41                                   ;@line 424
						JumpT ::temp37 _label368                                 ;@line 424
						CompareEQ ::temp40 token -1                              ;@line 424
						Not ::temp40 ::temp40                                    ;@line 424
						Cast ::temp37 ::temp40                                   ;@line 424
					_label368:
						JumpF ::temp37 _label369                                 ;@line 424
						Return None                                              ;@line 425
						Jump _label369                                           ;@line 425
					_label369:
						Cast ::temp41 guardDead                                  ;@line 427
						JumpT ::temp41 _label370                                 ;@line 427
						Cast ::temp41 guardDisabled                              ;@line 427
					_label370:
						Cast ::temp40 ::temp41                                   ;@line 427
						JumpT ::temp40 _label371                                 ;@line 427
						Cast ::temp40 destroyed                                  ;@line 427
					_label371:
						JumpF ::temp40 _label372                                 ;@line 427
						Assign faulted True                                      ;@line 428
						Assign recovering False                                  ;@line 429
						Return None                                              ;@line 430
						Jump _label372                                           ;@line 430
					_label372:
						Not ::temp37 gunLoaded                                   ;@line 432
						Cast ::temp40 ::temp37                                   ;@line 432
						JumpT ::temp40 _label373                                 ;@line 432
						Not ::temp41 guardLoaded                                 ;@line 432
						Cast ::temp40 ::temp41                                   ;@line 432
					_label373:
						JumpF ::temp40 _label374                                 ;@line 432
						Assign recovering False                                  ;@line 433
						JumpF gunLoaded _label375                                ;@line 434
						CallMethod RegisterForSingleUpdate self ::NoneVar 1.000000  ;@line 435
						Jump _label375                                           ;@line 435
					_label375:
						Return None                                              ;@line 437
						Jump _label374                                           ;@line 437
					_label374:
						CallMethod EnsureCityPlacement self ::temp37 recoveryGeneration 0  ;@line 439
						Assign placed ::temp37                                   ;@line 439
						CompareEQ ::temp41 generation recoveryGeneration         ;@line 440
						Not ::temp41 ::temp41                                    ;@line 440
						Cast ::temp37 ::temp41                                   ;@line 440
						JumpT ::temp37 _label376                                 ;@line 440
						CompareEQ ::temp40 token -1                              ;@line 440
						Not ::temp40 ::temp40                                    ;@line 440
						Cast ::temp37 ::temp40                                   ;@line 440
					_label376:
						JumpF ::temp37 _label377                                 ;@line 440
						Return None                                              ;@line 441
						Jump _label377                                           ;@line 441
					_label377:
						Not ::temp41 placed                                      ;@line 443
						JumpF ::temp41 _label378                                 ;@line 443
						Assign recovering False                                  ;@line 444
						Assign recoveryRequested True                            ;@line 445
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 446
						Return None                                              ;@line 447
						Jump _label378                                           ;@line 447
					_label378:
						CallMethod CaptureMatrices self ::temp40                 ;@line 449
						Assign captured ::temp40                                 ;@line 449
						CompareEQ ::temp37 generation recoveryGeneration         ;@line 450
						Not ::temp37 ::temp37                                    ;@line 450
						Cast ::temp40 ::temp37                                   ;@line 450
						JumpT ::temp40 _label379                                 ;@line 450
						CompareEQ ::temp41 token -1                              ;@line 450
						Not ::temp41 ::temp41                                    ;@line 450
						Cast ::temp40 ::temp41                                   ;@line 450
					_label379:
						JumpF ::temp40 _label380                                 ;@line 450
						Return None                                              ;@line 451
						Jump _label380                                           ;@line 451
					_label380:
						Not ::temp37 captured                                    ;@line 453
						JumpF ::temp37 _label381                                 ;@line 453
						Assign faulted True                                      ;@line 454
						Assign recovering False                                  ;@line 455
						CallStatic debug Trace ::NoneVar "AstraAsedioGuard: missing or invalid model controls; controller stopped." 0  ;@line 456
						Return None                                              ;@line 457
						Jump _label381                                           ;@line 457
					_label381:
						CallMethod GetDistance ::Artillero_var ::temp45 ::Puesto_var  ;@line 459
						Assign distance ::temp45                                 ;@line 459
						CompareEQ ::temp41 generation recoveryGeneration         ;@line 460
						Not ::temp41 ::temp41                                    ;@line 460
						Cast ::temp37 ::temp41                                   ;@line 460
						JumpT ::temp37 _label382                                 ;@line 460
						CompareEQ ::temp40 token -1                              ;@line 460
						Not ::temp40 ::temp40                                    ;@line 460
						Cast ::temp37 ::temp40                                   ;@line 460
					_label382:
						JumpF ::temp37 _label383                                 ;@line 460
						Return None                                              ;@line 461
						Jump _label383                                           ;@line 461
					_label383:
						CallMethod Finite self ::temp41 distance 0.000000 1000000.000000  ;@line 463
						Not ::temp40 ::temp41                                    ;@line 463
						JumpF ::temp40 _label384                                 ;@line 463
						Assign faulted True                                      ;@line 464
						Assign recovering False                                  ;@line 465
						Return None                                              ;@line 466
						Jump _label384                                           ;@line 466
					_label384:
						CompareGT ::temp37 distance 64.000000                    ;@line 468
						JumpF ::temp37 _label385                                 ;@line 468
						Assign movingGuard ::Artillero_var                       ;@line 472
						Assign recoveryPoint ::Puesto_var                        ;@line 473
						Assign pinBusy True                                      ;@line 474
						CallMethod MoveTo movingGuard ::NoneVar recoveryPoint 0.000000 0.000000 0.000000 True  ;@line 475
						CompareEQ ::temp41 generation recoveryGeneration         ;@line 476
						Cast ::temp41 ::temp41                                   ;@line 476
						JumpF ::temp41 _label386                                 ;@line 476
						CompareEQ ::temp40 token -1                              ;@line 476
						Cast ::temp41 ::temp40                                   ;@line 476
					_label386:
						Cast ::temp40 ::temp41                                   ;@line 476
						JumpF ::temp40 _label387                                 ;@line 476
						Cast ::temp40 recovering                                 ;@line 476
					_label387:
						Cast ::temp40 ::temp40                                   ;@line 476
						JumpF ::temp40 _label388                                 ;@line 476
						Not ::temp41 playerReserved                              ;@line 476
						Cast ::temp40 ::temp41                                   ;@line 476
					_label388:
						Cast ::temp40 ::temp40                                   ;@line 476
						JumpF ::temp40 _label389                                 ;@line 476
						Not ::temp41 destroyed                                   ;@line 476
						Cast ::temp40 ::temp41                                   ;@line 476
					_label389:
						Cast ::temp40 ::temp40                                   ;@line 476
						JumpF ::temp40 _label390                                 ;@line 476
						Not ::temp41 faulted                                     ;@line 476
						Cast ::temp40 ::temp41                                   ;@line 476
					_label390:
						Assign moveCurrent ::temp40                              ;@line 476
						Assign pinBusy False                                     ;@line 477
						Not ::temp41 moveCurrent                                 ;@line 478
						JumpF ::temp41 _label391                                 ;@line 478
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 479
						Return None                                              ;@line 480
						Jump _label391                                           ;@line 480
					_label391:
						Jump _label385                                           ;@line 480
					_label385:
						CallMethod IsDead ::Artillero_var ::temp40               ;@line 483
						Not ::temp41 ::temp40                                    ;@line 483
						Cast ::temp37 ::temp41                                   ;@line 483
						JumpF ::temp37 _label392                                 ;@line 483
						CallMethod IsDisabled ::Artillero_var ::temp37           ;@line 483
						Not ::temp40 ::temp37                                    ;@line 483
						Cast ::temp37 ::temp40                                   ;@line 483
					_label392:
						Cast ::temp40 ::temp37                                   ;@line 483
						JumpF ::temp40 _label393                                 ;@line 483
						CallMethod Is3DLoaded ::Artillero_var ::temp41           ;@line 483
						Cast ::temp40 ::temp41                                   ;@line 483
					_label393:
						Assign aliveAfterMove ::temp40                           ;@line 483
						CompareEQ ::temp37 generation recoveryGeneration         ;@line 484
						Not ::temp37 ::temp37                                    ;@line 484
						Cast ::temp40 ::temp37                                   ;@line 484
						JumpT ::temp40 _label394                                 ;@line 484
						CompareEQ ::temp41 token -1                              ;@line 484
						Not ::temp41 ::temp41                                    ;@line 484
						Cast ::temp40 ::temp41                                   ;@line 484
					_label394:
						JumpF ::temp40 _label395                                 ;@line 484
						Return None                                              ;@line 485
						Jump _label395                                           ;@line 485
					_label395:
						Not ::temp37 aliveAfterMove                              ;@line 487
						JumpF ::temp37 _label396                                 ;@line 487
						Assign faulted True                                      ;@line 488
						Assign recovering False                                  ;@line 489
						Return None                                              ;@line 490
						Jump _label396                                           ;@line 490
					_label396:
						CallMethod AcquirePin self ::temp41 recoveryGeneration   ;@line 492
						Assign pinAcquired ::temp41                              ;@line 492
						CompareEQ ::temp40 generation recoveryGeneration         ;@line 493
						Not ::temp40 ::temp40                                    ;@line 493
						Cast ::temp41 ::temp40                                   ;@line 493
						JumpT ::temp41 _label397                                 ;@line 493
						CompareEQ ::temp37 token -1                              ;@line 493
						Not ::temp37 ::temp37                                    ;@line 493
						Cast ::temp41 ::temp37                                   ;@line 493
					_label397:
						JumpF ::temp41 _label398                                 ;@line 493
						Return None                                              ;@line 494
						Jump _label398                                           ;@line 494
					_label398:
						Not ::temp40 pinAcquired                                 ;@line 496
						JumpF ::temp40 _label399                                 ;@line 496
						Assign faulted True                                      ;@line 497
						Assign recovering False                                  ;@line 498
						Return None                                              ;@line 499
						Jump _label399                                           ;@line 499
					_label399:
						Assign yaw 0.000000                                      ;@line 501
						Assign pitch 0.000000                                    ;@line 502
						Assign token serial                                      ;@line 503
						Assign running True                                      ;@line 504
						Assign recovering False                                  ;@line 505
						Assign recoveryToken token                               ;@line 506
						CallStatic utility GetCurrentRealTime ::temp45           ;@line 507
						Assign now ::temp45                                      ;@line 507
						CallMethod Current self ::temp37 recoveryGeneration recoveryToken  ;@line 508
						Not ::temp41 ::temp37                                    ;@line 508
						JumpF ::temp41 _label400                                 ;@line 508
						Return None                                              ;@line 509
						Jump _label400                                           ;@line 509
					_label400:
						CallMethod Finite self ::temp40 now 0.000000 1000000000.000000  ;@line 511
						Not ::temp37 ::temp40                                    ;@line 511
						JumpF ::temp37 _label401                                 ;@line 511
						Assign faulted True                                      ;@line 512
						CallMethod Shutdown self ::NoneVar                       ;@line 513
						Return None                                              ;@line 514
						Jump _label401                                           ;@line 514
					_label401:
						Assign lastTick now                                      ;@line 516
						CallMethod SafeCadenceSeconds self ::temp45              ;@line 517
						FAdd ::temp45 now ::temp45                               ;@line 517
						Assign nextShotAt ::temp45                               ;@line 517
						CallMethod PlaySceneAnimation self ::temp41 "Reset" recoveryGeneration recoveryToken  ;@line 518
						Assign resetStarted ::temp41                             ;@line 518
						CallMethod Current self ::temp40 recoveryGeneration recoveryToken  ;@line 519
						Not ::temp37 ::temp40                                    ;@line 519
						JumpF ::temp37 _label402                                 ;@line 519
						Return None                                              ;@line 520
						Jump _label402                                           ;@line 520
					_label402:
						Not ::temp41 resetStarted                                ;@line 522
						JumpF ::temp41 _label403                                 ;@line 522
						Assign faulted True                                      ;@line 523
						CallMethod Shutdown self ::NoneVar                       ;@line 524
						Return None                                              ;@line 525
						Jump _label403                                           ;@line 525
					_label403:
						CallMethod ApplyAim self ::NoneVar recoveryGeneration recoveryToken  ;@line 527
						CallMethod Current self ::temp40 recoveryGeneration recoveryToken  ;@line 528
						Not ::temp37 ::temp40                                    ;@line 528
						JumpF ::temp37 _label404                                 ;@line 528
						Return None                                              ;@line 529
						Jump _label404                                           ;@line 529
					_label404:
						CallMethod PositionOperator self ::temp41 recoveryGeneration recoveryToken  ;@line 531
						Assign positioned ::temp41                               ;@line 531
						CallMethod Current self ::temp40 recoveryGeneration recoveryToken  ;@line 532
						Not ::temp37 ::temp40                                    ;@line 532
						JumpF ::temp37 _label405                                 ;@line 532
						Return None                                              ;@line 533
						Jump _label405                                           ;@line 533
					_label405:
						Cast ::temp40 positioned                                 ;@line 535
						JumpF ::temp40 _label406                                 ;@line 535
						CallMethod StartGuardPose self ::temp41 recoveryGeneration recoveryToken  ;@line 535
						Cast ::temp40 ::temp41                                   ;@line 535
					_label406:
						Assign posed ::temp40                                    ;@line 535
						CallMethod Current self ::temp37 recoveryGeneration recoveryToken  ;@line 536
						Not ::temp41 ::temp37                                    ;@line 536
						JumpF ::temp41 _label407                                 ;@line 536
						Return None                                              ;@line 537
						Jump _label407                                           ;@line 537
					_label407:
						Not ::temp40 posed                                       ;@line 539
						JumpF ::temp40 _label408                                 ;@line 539
						Assign faulted True                                      ;@line 540
						CallMethod Shutdown self ::NoneVar                       ;@line 541
						Return None                                              ;@line 542
						Jump _label408                                           ;@line 542
					_label408:
						CallMethod SetVisualBolt self ::NoneVar 1.000000 recoveryGeneration recoveryToken  ;@line 544
						CallMethod Current self ::temp37 recoveryGeneration recoveryToken  ;@line 545
						JumpF ::temp37 _label409                                 ;@line 545
						CallMethod RegisterForSingleUpdate self ::NoneVar 0.200000  ;@line 546
						Jump _label409                                           ;@line 546
					_label409:
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
						.local ::temp117 actor
						.local ::temp118 Bool
						.local ::temp119 Bool
						.local ::temp120 Float
						.local ::temp121 Float
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
						.local ::temp122 Bool
						.local ::temp123 Int
					.endLocalTable
					.code
						CallStatic game GetPlayer ::temp117                      ;@line 908
						Assign player ::temp117                                  ;@line 908
						CallMethod Current self ::temp118 expectedGeneration expectedToken  ;@line 909
						Not ::temp118 ::temp118                                  ;@line 909
						Cast ::temp118 ::temp118                                 ;@line 909
						JumpT ::temp118 _label410                                ;@line 909
						Cast ::temp117 None                                      ;@line 909
						CompareEQ ::temp119 player ::temp117                     ;@line 909
						Cast ::temp118 ::temp119                                 ;@line 909
					_label410:
						JumpF ::temp118 _label411                                ;@line 909
						Return False                                             ;@line 910
						Jump _label411                                           ;@line 910
					_label411:
						CallMethod Is3DLoaded player ::temp119                   ;@line 912
						Assign playerLoaded ::temp119                            ;@line 912
						CallMethod GetPositionX player ::temp120                 ;@line 913
						Assign px ::temp120                                      ;@line 913
						CallMethod GetPositionY player ::temp120                 ;@line 914
						Assign py ::temp120                                      ;@line 914
						CallMethod GetPositionZ player ::temp120                 ;@line 915
						Assign pz ::temp120                                      ;@line 915
						CallMethod GetHeight player ::temp120                    ;@line 916
						Assign height ::temp120                                  ;@line 916
						CallMethod Current self ::temp118 expectedGeneration expectedToken  ;@line 917
						Not ::temp119 ::temp118                                  ;@line 917
						Cast ::temp119 ::temp119                                 ;@line 917
						JumpT ::temp119 _label412                                ;@line 917
						Not ::temp118 playerLoaded                               ;@line 917
						Cast ::temp119 ::temp118                                 ;@line 917
					_label412:
						Cast ::temp119 ::temp119                                 ;@line 917
						JumpT ::temp119 _label413                                ;@line 917
						CallMethod Finite self ::temp118 px -1000000.000000 1000000.000000  ;@line 917
						Not ::temp118 ::temp118                                  ;@line 917
						Cast ::temp119 ::temp118                                 ;@line 917
					_label413:
						Cast ::temp119 ::temp119                                 ;@line 917
						JumpT ::temp119 _label414                                ;@line 917
						CallMethod Finite self ::temp118 py -1000000.000000 1000000.000000  ;@line 917
						Not ::temp118 ::temp118                                  ;@line 917
						Cast ::temp119 ::temp118                                 ;@line 917
					_label414:
						Cast ::temp119 ::temp119                                 ;@line 917
						JumpT ::temp119 _label415                                ;@line 917
						CallMethod Finite self ::temp118 pz -1000000.000000 1000000.000000  ;@line 917
						Not ::temp118 ::temp118                                  ;@line 917
						Cast ::temp119 ::temp118                                 ;@line 917
					_label415:
						Cast ::temp119 ::temp119                                 ;@line 917
						JumpT ::temp119 _label416                                ;@line 917
						CallMethod Finite self ::temp118 height 1.000000 512.000000  ;@line 917
						Not ::temp118 ::temp118                                  ;@line 917
						Cast ::temp119 ::temp118                                 ;@line 917
					_label416:
						JumpF ::temp119 _label417                                ;@line 917
						Return False                                             ;@line 918
						Jump _label417                                           ;@line 918
					_label417:
						CompareLT ::temp118 height 128.000000                    ;@line 920
						JumpF ::temp118 _label418                                ;@line 920
						Assign height 128.000000                                 ;@line 921
						Jump _label418                                           ;@line 921
					_label418:
						FAdd ::temp120 height 64.000000                          ;@line 923
						Assign height ::temp120                                  ;@line 923
						FDivide ::temp120 height 8.000000                        ;@line 928
						FAdd ::temp120 80.000000 ::temp120                       ;@line 928
						Assign radius ::temp120                                  ;@line 928
						ArrayGetElement ::temp120 muzzleWorldMatrix 1            ;@line 929
						Assign bx ::temp120                                      ;@line 929
						ArrayGetElement ::temp120 muzzleWorldMatrix 4            ;@line 930
						Assign by ::temp120                                      ;@line 930
						ArrayGetElement ::temp120 muzzleWorldMatrix 7            ;@line 931
						Assign bz ::temp120                                      ;@line 931
						FMultiply ::temp120 bx bx                                ;@line 932
						FMultiply ::temp121 by by                                ;@line 932
						FAdd ::temp120 ::temp120 ::temp121                       ;@line 932
						CallStatic math Sqrt ::temp121 ::temp120                 ;@line 932
						Assign boreHorizontal ::temp121                          ;@line 932
						CompareLT ::temp119 boreHorizontal 0.010000              ;@line 933
						JumpF ::temp119 _label419                                ;@line 933
						Return False                                             ;@line 934
						Jump _label419                                           ;@line 934
					_label419:
						FMultiply ::temp120 ::ProjectileSpeed_var boreHorizontal  ;@line 936
						FDivide ::temp121 targetHorizontal ::temp120             ;@line 936
						Assign totalTime ::temp121                               ;@line 936
						CallMethod Finite self ::temp118 totalTime 0.000010 30.000000  ;@line 937
						Not ::temp119 ::temp118                                  ;@line 937
						JumpF ::temp119 _label420                                ;@line 937
						Return False                                             ;@line 938
						Jump _label420                                           ;@line 938
					_label420:
						ArrayGetElement ::temp120 muzzlePosition 0               ;@line 940
						Assign ax ::temp120                                      ;@line 940
						ArrayGetElement ::temp121 muzzlePosition 1               ;@line 941
						Assign ay ::temp121                                      ;@line 941
						ArrayGetElement ::temp120 muzzlePosition 2               ;@line 942
						Assign az ::temp120                                      ;@line 942
						Assign step 1                                            ;@line 943
					_label425:
						CompareLTE ::temp118 step 8                              ;@line 944
						JumpF ::temp118 _label421                                ;@line 944
						Cast ::temp121 step                                      ;@line 945
						FMultiply ::temp120 totalTime ::temp121                  ;@line 945
						FDivide ::temp121 ::temp120 8.000000                     ;@line 945
						Assign t ::temp121                                       ;@line 945
						ArrayGetElement ::temp120 muzzlePosition 0               ;@line 946
						FMultiply ::temp121 bx ::ProjectileSpeed_var             ;@line 946
						FMultiply ::temp121 ::temp121 t                          ;@line 946
						FAdd ::temp120 ::temp120 ::temp121                       ;@line 946
						Assign ex ::temp120                                      ;@line 946
						ArrayGetElement ::temp121 muzzlePosition 1               ;@line 947
						FMultiply ::temp120 by ::ProjectileSpeed_var             ;@line 947
						FMultiply ::temp120 ::temp120 t                          ;@line 947
						FAdd ::temp121 ::temp121 ::temp120                       ;@line 947
						Assign ey ::temp121                                      ;@line 947
						ArrayGetElement ::temp120 muzzlePosition 2               ;@line 948
						FMultiply ::temp121 bz ::ProjectileSpeed_var             ;@line 948
						FMultiply ::temp121 ::temp121 t                          ;@line 948
						FAdd ::temp120 ::temp120 ::temp121                       ;@line 948
						FMultiply ::temp121 0.500000 ::ProjectileGravity_var     ;@line 948
						FMultiply ::temp121 ::temp121 t                          ;@line 948
						FMultiply ::temp121 ::temp121 t                          ;@line 948
						FSubtract ::temp120 ::temp120 ::temp121                  ;@line 948
						Assign ez ::temp120                                      ;@line 948
						Assign sample 0                                          ;@line 949
					_label424:
						CompareLTE ::temp119 sample 4                            ;@line 950
						JumpF ::temp119 _label422                                ;@line 950
						Cast ::temp121 sample                                    ;@line 951
						FMultiply ::temp120 height ::temp121                     ;@line 951
						FDivide ::temp121 ::temp120 4.000000                     ;@line 951
						FAdd ::temp120 pz ::temp121                              ;@line 951
						CallMethod PointNearSegment self ::temp122 px py ::temp120 ax ay az ex ey ez radius  ;@line 951
						JumpF ::temp122 _label423                                ;@line 951
						Return False                                             ;@line 952
						Jump _label423                                           ;@line 952
					_label423:
						IAdd ::temp123 sample 1                                  ;@line 954
						Assign sample ::temp123                                  ;@line 954
						Jump _label424                                           ;@line 954
					_label422:
						Assign ax ex                                             ;@line 956
						Assign ay ey                                             ;@line 957
						Assign az ez                                             ;@line 958
						IAdd ::temp123 step 1                                    ;@line 959
						Assign step ::temp123                                    ;@line 959
						Jump _label425                                           ;@line 959
					_label421:
						CallMethod Current self ::temp122 expectedGeneration expectedToken  ;@line 961
						Return ::temp122                                         ;@line 961
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
						.local ::temp171 Bool
						.local ::temp172 actor
						.local ::temp173 Bool
						.local ::temp174 ObjectReference
						.local valid Bool
						.local visible Bool
					.endLocalTable
					.code
						CallMethod GuardReady self ::temp171 expectedGeneration expectedToken  ;@line 1378
						Not ::temp171 ::temp171                                  ;@line 1378
						Cast ::temp171 ::temp171                                 ;@line 1378
						JumpT ::temp171 _label426                                ;@line 1378
						Cast ::temp172 None                                      ;@line 1378
						CompareEQ ::temp173 target ::temp172                     ;@line 1378
						Cast ::temp171 ::temp173                                 ;@line 1378
					_label426:
						Cast ::temp171 ::temp171                                 ;@line 1378
						JumpT ::temp171 _label427                                ;@line 1378
						CompareEQ ::temp173 target ::Artillero_var               ;@line 1378
						Cast ::temp171 ::temp173                                 ;@line 1378
					_label427:
						JumpF ::temp171 _label428                                ;@line 1378
						Return False                                             ;@line 1379
						Jump _label428                                           ;@line 1379
					_label428:
						CallMethod Is3DLoaded target ::temp173                   ;@line 1381
						Cast ::temp173 ::temp173                                 ;@line 1381
						JumpF ::temp173 _label429                                ;@line 1381
						CallMethod IsDisabled target ::temp171                   ;@line 1381
						Not ::temp171 ::temp171                                  ;@line 1381
						Cast ::temp173 ::temp171                                 ;@line 1381
					_label429:
						Cast ::temp173 ::temp173                                 ;@line 1381
						JumpF ::temp173 _label430                                ;@line 1381
						CallMethod IsDead target ::temp171                       ;@line 1381
						Not ::temp171 ::temp171                                  ;@line 1381
						Cast ::temp173 ::temp171                                 ;@line 1381
					_label430:
						Assign valid ::temp173                                   ;@line 1381
						Cast ::temp174 target                                    ;@line 1382
						CallMethod HasLOS ::Artillero_var ::temp171 ::temp174    ;@line 1382
						Assign visible ::temp171                                 ;@line 1382
						CallMethod Current self ::temp173 expectedGeneration expectedToken  ;@line 1383
						Cast ::temp171 ::temp173                                 ;@line 1383
						JumpF ::temp171 _label431                                ;@line 1383
						Cast ::temp171 valid                                     ;@line 1383
					_label431:
						Cast ::temp173 ::temp171                                 ;@line 1383
						JumpF ::temp173 _label432                                ;@line 1383
						Cast ::temp173 visible                                   ;@line 1383
					_label432:
						Return ::temp173                                         ;@line 1383
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
						.local ::temp154 actor
						.local ::temp155 Bool
						.local ::temp156 Bool
						.local ::temp157 Faction
						.local ::temp158 Idle
						.local ::NoneVar None
					.endLocalTable
					.code
						Cast ::temp154 None                                      ;@line 1274
						CompareEQ ::temp155 candidate ::temp154                  ;@line 1274
						Cast ::temp155 ::temp155                                 ;@line 1274
						JumpT ::temp155 _label433                                ;@line 1274
						CallStatic game GetPlayer ::temp154                      ;@line 1274
						CompareEQ ::temp156 candidate ::temp154                  ;@line 1274
						Cast ::temp155 ::temp156                                 ;@line 1274
					_label433:
						JumpF ::temp155 _label434                                ;@line 1274
						Return None                                              ;@line 1275
						Jump _label434                                           ;@line 1275
					_label434:
						Cast ::temp157 None                                      ;@line 1277
						CompareEQ ::temp156 fireFaction ::temp157                ;@line 1277
						Not ::temp156 ::temp156                                  ;@line 1277
						JumpF ::temp156 _label435                                ;@line 1277
						CallMethod RemoveFromFaction candidate ::NoneVar fireFaction  ;@line 1278
						Jump _label435                                           ;@line 1278
					_label435:
						Cast ::temp157 None                                      ;@line 1280
						CompareEQ ::temp155 poseFaction ::temp157                ;@line 1280
						Not ::temp155 ::temp155                                  ;@line 1280
						JumpF ::temp155 _label436                                ;@line 1280
						CallMethod RemoveFromFaction candidate ::NoneVar poseFaction  ;@line 1281
						Jump _label436                                           ;@line 1281
					_label436:
						Cast ::temp158 None                                      ;@line 1283
						CompareEQ ::temp156 exitIdle ::temp158                   ;@line 1283
						Not ::temp156 ::temp156                                  ;@line 1283
						Cast ::temp156 ::temp156                                 ;@line 1283
						JumpF ::temp156 _label437                                ;@line 1283
						CallMethod Is3DLoaded candidate ::temp155                ;@line 1283
						Cast ::temp156 ::temp155                                 ;@line 1283
					_label437:
						Cast ::temp156 ::temp156                                 ;@line 1283
						JumpF ::temp156 _label438                                ;@line 1283
						CallMethod IsDead candidate ::temp155                    ;@line 1283
						Not ::temp155 ::temp155                                  ;@line 1283
						Cast ::temp156 ::temp155                                 ;@line 1283
					_label438:
						JumpF ::temp156 _label439                                ;@line 1283
						CallMethod PlayIdle candidate ::temp155 exitIdle         ;@line 1284
						Jump _label439                                           ;@line 1284
					_label439:
						CallMethod SetHeadTracking candidate ::NoneVar True      ;@line 1286
						Assign guardPoseFiring False                             ;@line 1287
						Assign guardPoseStarted False                            ;@line 1288
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
						.local ::temp113 Float
						.local ::temp114 Float
						.local ::temp115 Bool
						.local ::temp116 Bool
						.local dx Float
						.local dy Float
						.local dz Float
						.local lengthSquared Float
						.local along Float
					.endLocalTable
					.code
						FSubtract ::temp113 bx ax                                ;@line 888
						Assign dx ::temp113                                      ;@line 888
						FSubtract ::temp113 by ay                                ;@line 889
						Assign dy ::temp113                                      ;@line 889
						FSubtract ::temp113 bz az                                ;@line 890
						Assign dz ::temp113                                      ;@line 890
						FMultiply ::temp113 dx dx                                ;@line 891
						FMultiply ::temp114 dy dy                                ;@line 891
						FAdd ::temp113 ::temp113 ::temp114                       ;@line 891
						FMultiply ::temp114 dz dz                                ;@line 891
						FAdd ::temp113 ::temp113 ::temp114                       ;@line 891
						Assign lengthSquared ::temp113                           ;@line 891
						CompareLTE ::temp115 lengthSquared 0.000010              ;@line 892
						JumpF ::temp115 _label440                                ;@line 892
						Return True                                              ;@line 893
						Jump _label440                                           ;@line 893
					_label440:
						FSubtract ::temp114 px ax                                ;@line 895
						FMultiply ::temp113 ::temp114 dx                         ;@line 895
						FSubtract ::temp114 py ay                                ;@line 895
						FMultiply ::temp114 ::temp114 dy                         ;@line 895
						FAdd ::temp113 ::temp113 ::temp114                       ;@line 895
						FSubtract ::temp114 pz az                                ;@line 895
						FMultiply ::temp114 ::temp114 dz                         ;@line 895
						FAdd ::temp113 ::temp113 ::temp114                       ;@line 895
						FDivide ::temp114 ::temp113 lengthSquared                ;@line 895
						Assign along ::temp114                                   ;@line 895
						CompareLT ::temp115 along 0.000000                       ;@line 896
						JumpF ::temp115 _label441                                ;@line 896
						Assign along 0.000000                                    ;@line 897
						Jump _label442                                           ;@line 897
					_label441:
						CompareGT ::temp116 along 1.000000                       ;@line 898
						JumpF ::temp116 _label442                                ;@line 898
						Assign along 1.000000                                    ;@line 899
						Jump _label442                                           ;@line 899
					_label442:
						FMultiply ::temp113 along dx                             ;@line 901
						FAdd ::temp114 ax ::temp113                              ;@line 901
						FSubtract ::temp113 px ::temp114                         ;@line 901
						Assign dx ::temp113                                      ;@line 901
						FMultiply ::temp114 along dy                             ;@line 902
						FAdd ::temp113 ay ::temp114                              ;@line 902
						FSubtract ::temp114 py ::temp113                         ;@line 902
						Assign dy ::temp114                                      ;@line 902
						FMultiply ::temp113 along dz                             ;@line 903
						FAdd ::temp114 az ::temp113                              ;@line 903
						FSubtract ::temp113 pz ::temp114                         ;@line 903
						Assign dz ::temp113                                      ;@line 903
						FMultiply ::temp114 dx dx                                ;@line 904
						FMultiply ::temp113 dy dy                                ;@line 904
						FAdd ::temp114 ::temp114 ::temp113                       ;@line 904
						FMultiply ::temp113 dz dz                                ;@line 904
						FAdd ::temp114 ::temp114 ::temp113                       ;@line 904
						FMultiply ::temp113 radius radius                        ;@line 904
						CompareLTE ::temp116 ::temp114 ::temp113                 ;@line 904
						Return ::temp116                                         ;@line 904
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
						.local ::temp141 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod Current self ::temp141 expectedGeneration expectedToken  ;@line 1103
						Not ::temp141 ::temp141                                  ;@line 1103
						JumpF ::temp141 _label443                                ;@line 1103
						Return None                                              ;@line 1104
						Jump _label443                                           ;@line 1104
					_label443:
						Assign updating False                                    ;@line 1106
						CallMethod RegisterForSingleUpdate self ::NoneVar delay  ;@line 1107
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
						.local ::temp124 Bool
						.local ::temp125 Float
						.local ::temp126 Float
						.local ::temp127 Bool
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
						CallMethod SampleTarget self ::temp124 target expectedGeneration expectedToken  ;@line 965
						Not ::temp124 ::temp124                                  ;@line 965
						JumpF ::temp124 _label444                                ;@line 965
						Return False                                             ;@line 966
						Jump _label444                                           ;@line 966
					_label444:
						CallStatic math Cos ::temp125 yaw                        ;@line 969
						Assign yc ::temp125                                      ;@line 969
						CallStatic math Sin ::temp125 yaw                        ;@line 970
						Assign ys ::temp125                                      ;@line 970
						CallStatic math Cos ::temp125 pitch                      ;@line 971
						Assign pc ::temp125                                      ;@line 971
						CallStatic math Sin ::temp125 pitch                      ;@line 972
						Assign ps ::temp125                                      ;@line 972
						FMultiply ::temp125 ys pc                                ;@line 973
						Assign lx ::temp125                                      ;@line 973
						FNegate ::temp125 yc                                     ;@line 974
						FMultiply ::temp125 ::temp125 pc                         ;@line 974
						Assign ly ::temp125                                      ;@line 974
						ArrayGetElement ::temp125 rootWorldMatrix 0              ;@line 975
						FMultiply ::temp125 ::temp125 lx                         ;@line 975
						ArrayGetElement ::temp126 rootWorldMatrix 1              ;@line 975
						FMultiply ::temp126 ::temp126 ly                         ;@line 975
						FAdd ::temp125 ::temp125 ::temp126                       ;@line 975
						ArrayGetElement ::temp126 rootWorldMatrix 2              ;@line 975
						FMultiply ::temp126 ::temp126 ps                         ;@line 975
						FAdd ::temp125 ::temp125 ::temp126                       ;@line 975
						Assign wx ::temp125                                      ;@line 975
						ArrayGetElement ::temp126 rootWorldMatrix 3              ;@line 976
						FMultiply ::temp125 ::temp126 lx                         ;@line 976
						ArrayGetElement ::temp126 rootWorldMatrix 4              ;@line 976
						FMultiply ::temp126 ::temp126 ly                         ;@line 976
						FAdd ::temp125 ::temp125 ::temp126                       ;@line 976
						ArrayGetElement ::temp126 rootWorldMatrix 5              ;@line 976
						FMultiply ::temp126 ::temp126 ps                         ;@line 976
						FAdd ::temp125 ::temp125 ::temp126                       ;@line 976
						Assign wy ::temp125                                      ;@line 976
						ArrayGetElement ::temp126 rootWorldMatrix 6              ;@line 977
						FMultiply ::temp125 ::temp126 lx                         ;@line 977
						ArrayGetElement ::temp126 rootWorldMatrix 7              ;@line 977
						FMultiply ::temp126 ::temp126 ly                         ;@line 977
						FAdd ::temp125 ::temp125 ::temp126                       ;@line 977
						ArrayGetElement ::temp126 rootWorldMatrix 8              ;@line 977
						FMultiply ::temp126 ::temp126 ps                         ;@line 977
						FAdd ::temp125 ::temp125 ::temp126                       ;@line 977
						Assign wz ::temp125                                      ;@line 977
						ArrayGetElement ::temp126 muzzleWorldMatrix 1            ;@line 978
						FMultiply ::temp125 wx ::temp126                         ;@line 978
						ArrayGetElement ::temp126 muzzleWorldMatrix 4            ;@line 978
						FMultiply ::temp126 wy ::temp126                         ;@line 978
						FAdd ::temp125 ::temp125 ::temp126                       ;@line 978
						ArrayGetElement ::temp126 muzzleWorldMatrix 7            ;@line 978
						FMultiply ::temp126 wz ::temp126                         ;@line 978
						FAdd ::temp125 ::temp125 ::temp126                       ;@line 978
						Assign poseDot ::temp125                                 ;@line 978
						ArrayGetElement ::temp126 muzzleWorldMatrix 1            ;@line 979
						FMultiply ::temp125 aimX ::temp126                       ;@line 979
						ArrayGetElement ::temp126 muzzleWorldMatrix 4            ;@line 979
						FMultiply ::temp126 aimY ::temp126                       ;@line 979
						FAdd ::temp125 ::temp125 ::temp126                       ;@line 979
						ArrayGetElement ::temp126 muzzleWorldMatrix 7            ;@line 979
						FMultiply ::temp126 aimZ ::temp126                       ;@line 979
						FAdd ::temp125 ::temp125 ::temp126                       ;@line 979
						Assign targetDot ::temp125                               ;@line 979
						CallMethod Finite self ::temp124 poseDot 0.999950 1.002000  ;@line 980
						Not ::temp124 ::temp124                                  ;@line 980
						Cast ::temp124 ::temp124                                 ;@line 980
						JumpT ::temp124 _label445                                ;@line 980
						CallMethod Finite self ::temp127 targetDot 0.999950 1.002000  ;@line 980
						Not ::temp127 ::temp127                                  ;@line 980
						Cast ::temp124 ::temp127                                 ;@line 980
					_label445:
						Cast ::temp124 ::temp124                                 ;@line 980
						JumpT ::temp124 _label446                                ;@line 980
						CallMethod Current self ::temp127 expectedGeneration expectedToken  ;@line 980
						Not ::temp127 ::temp127                                  ;@line 980
						Cast ::temp124 ::temp127                                 ;@line 980
					_label446:
						JumpF ::temp124 _label447                                ;@line 980
						Return False                                             ;@line 981
						Jump _label447                                           ;@line 981
					_label447:
						CallMethod PlayerClear self ::temp127 expectedGeneration expectedToken  ;@line 983
						Assign clear ::temp127                                   ;@line 983
						CallStatic utility IsInMenuMode ::temp124                ;@line 984
						Assign menuOpen ::temp124                                ;@line 984
						CallMethod ValidTarget self ::temp127 target expectedGeneration expectedToken  ;@line 985
						Assign targetValid ::temp127                             ;@line 985
						CallMethod Current self ::temp124 expectedGeneration expectedToken  ;@line 986
						Cast ::temp127 ::temp124                                 ;@line 986
						JumpF ::temp127 _label448                                ;@line 986
						Cast ::temp127 clear                                     ;@line 986
					_label448:
						Cast ::temp127 ::temp127                                 ;@line 986
						JumpF ::temp127 _label449                                ;@line 986
						Not ::temp124 menuOpen                                   ;@line 986
						Cast ::temp127 ::temp124                                 ;@line 986
					_label449:
						Cast ::temp124 ::temp127                                 ;@line 986
						JumpF ::temp124 _label450                                ;@line 986
						Cast ::temp124 targetValid                               ;@line 986
					_label450:
						Return ::temp124                                         ;@line 986
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
						.local ::temp186 Bool
						.local ::temp187 Bool
						.local ::temp188 Float
						.local ::temp189 Float
						.local baseZ Float
						.local height Float
						.local travel Float
						.local boltZ Float
						.local validHeights Bool
					.endLocalTable
					.code
						CallMethod Current self ::temp186 expectedGeneration expectedToken  ;@line 1442
						Not ::temp186 ::temp186                                  ;@line 1442
						Cast ::temp186 ::temp186                                 ;@line 1442
						JumpT ::temp186 _label451                                ;@line 1442
						CallMethod Finite self ::temp187 horizontal 80.000000 6000.000000  ;@line 1442
						Not ::temp187 ::temp187                                  ;@line 1442
						Cast ::temp186 ::temp187                                 ;@line 1442
					_label451:
						Cast ::temp186 ::temp186                                 ;@line 1442
						JumpT ::temp186 _label452                                ;@line 1442
						CallMethod Finite self ::temp187 ::ProjectileSpeed_var 1.000000 100000.000000  ;@line 1442
						Not ::temp187 ::temp187                                  ;@line 1442
						Cast ::temp186 ::temp187                                 ;@line 1442
					_label452:
						Cast ::temp186 ::temp186                                 ;@line 1442
						JumpT ::temp186 _label453                                ;@line 1442
						CallMethod Finite self ::temp187 ::ProjectileGravity_var 0.000000 5000.000000  ;@line 1442
						Not ::temp187 ::temp187                                  ;@line 1442
						Cast ::temp186 ::temp187                                 ;@line 1442
					_label453:
						JumpF ::temp186 _label454                                ;@line 1442
						Return False                                             ;@line 1443
						Jump _label454                                           ;@line 1443
					_label454:
						CallMethod GetPositionZ target ::temp188                 ;@line 1445
						Assign baseZ ::temp188                                   ;@line 1445
						CallMethod GetHeight target ::temp188                    ;@line 1446
						Assign height ::temp188                                  ;@line 1446
						FDivide ::temp188 horizontal ::ProjectileSpeed_var       ;@line 1447
						Assign travel ::temp188                                  ;@line 1447
						ArrayGetElement ::temp188 muzzlePosition 2               ;@line 1448
						FMultiply ::temp189 0.500000 ::ProjectileGravity_var     ;@line 1448
						FMultiply ::temp189 ::temp189 travel                     ;@line 1448
						FMultiply ::temp189 ::temp189 travel                     ;@line 1448
						FSubtract ::temp188 ::temp188 ::temp189                  ;@line 1448
						Assign boltZ ::temp188                                   ;@line 1448
						CallMethod Finite self ::temp187 baseZ -1000000.000000 1000000.000000  ;@line 1449
						Cast ::temp187 ::temp187                                 ;@line 1449
						JumpF ::temp187 _label455                                ;@line 1449
						CallMethod Finite self ::temp186 height 24.000000 8192.000000  ;@line 1449
						Cast ::temp187 ::temp186                                 ;@line 1449
					_label455:
						Assign validHeights ::temp187                            ;@line 1449
						CallMethod Current self ::temp186 expectedGeneration expectedToken  ;@line 1450
						Cast ::temp187 ::temp186                                 ;@line 1450
						JumpF ::temp187 _label456                                ;@line 1450
						Cast ::temp187 validHeights                              ;@line 1450
					_label456:
						Cast ::temp187 ::temp187                                 ;@line 1450
						JumpF ::temp187 _label457                                ;@line 1450
						FAdd ::temp189 baseZ 8.000000                            ;@line 1450
						CompareGTE ::temp186 boltZ ::temp189                     ;@line 1450
						Cast ::temp187 ::temp186                                 ;@line 1450
					_label457:
						Cast ::temp187 ::temp187                                 ;@line 1450
						JumpF ::temp187 _label458                                ;@line 1450
						FAdd ::temp188 baseZ height                              ;@line 1450
						FSubtract ::temp189 ::temp188 8.000000                   ;@line 1450
						CompareLTE ::temp186 boltZ ::temp189                     ;@line 1450
						Cast ::temp187 ::temp186                                 ;@line 1450
					_label458:
						Return ::temp187                                         ;@line 1450
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
						CallMethod InvalidatePlayerLease self ::NoneVar          ;@line 104
						CallMethod Shutdown self ::NoneVar                       ;@line 105
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
						.local ::temp106 Bool
					.endLocalTable
					.code
						CallMethod SampleHorizontalTarget self ::temp106 target expectedGeneration expectedToken  ;@line 858
						Return ::temp106                                         ;@line 858
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
						.local ::temp107 Float
						.local ::temp108 Bool
						.local ::temp109 Float
						.local ::temp110 Bool
						.local difference Float
					.endLocalTable
					.code
						FSubtract ::temp107 goal value                           ;@line 862
						Assign difference ::temp107                              ;@line 862
						CompareGT ::temp108 difference maximumStep               ;@line 863
						JumpF ::temp108 _label459                                ;@line 863
						FAdd ::temp107 value maximumStep                         ;@line 864
						Return ::temp107                                         ;@line 864
						Jump _label460                                           ;@line 864
					_label459:
						FNegate ::temp109 maximumStep                            ;@line 865
						CompareLT ::temp110 difference ::temp109                 ;@line 865
						JumpF ::temp110 _label460                                ;@line 865
						FSubtract ::temp109 value maximumStep                    ;@line 866
						Return ::temp109                                         ;@line 866
						Jump _label460                                           ;@line 866
					_label460:
						Return goal                                              ;@line 868
					.endCode
				.endFunction
				.function QueueDeferredRecovery
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp54 Bool
						.local ::temp55 Bool
						.local queueGeneration Int
						.local loaded Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						Cast ::temp54 playerReserved                             ;@line 627
						JumpT ::temp54 _label461                                 ;@line 627
						Cast ::temp54 pinBusy                                    ;@line 627
					_label461:
						Cast ::temp54 ::temp54                                   ;@line 627
						JumpT ::temp54 _label462                                 ;@line 627
						Cast ::temp54 sceneBusy                                  ;@line 627
					_label462:
						Cast ::temp54 ::temp54                                   ;@line 627
						JumpT ::temp54 _label463                                 ;@line 627
						Not ::temp55 recoveryRequested                           ;@line 627
						Cast ::temp54 ::temp55                                   ;@line 627
					_label463:
						Cast ::temp55 ::temp54                                   ;@line 627
						JumpT ::temp55 _label464                                 ;@line 627
						Cast ::temp55 destroyed                                  ;@line 627
					_label464:
						Cast ::temp54 ::temp55                                   ;@line 627
						JumpT ::temp54 _label465                                 ;@line 627
						Cast ::temp54 faulted                                    ;@line 627
					_label465:
						JumpF ::temp54 _label466                                 ;@line 627
						Return None                                              ;@line 628
						Jump _label466                                           ;@line 628
					_label466:
						Assign queueGeneration generation                        ;@line 630
						CallMethod Is3DLoaded self ::temp55                      ;@line 631
						Assign loaded ::temp55                                   ;@line 631
						CompareEQ ::temp54 generation queueGeneration            ;@line 632
						Not ::temp54 ::temp54                                    ;@line 632
						Cast ::temp55 ::temp54                                   ;@line 632
						JumpT ::temp55 _label467                                 ;@line 632
						Cast ::temp55 pinBusy                                    ;@line 632
					_label467:
						Cast ::temp54 ::temp55                                   ;@line 632
						JumpT ::temp54 _label468                                 ;@line 632
						Cast ::temp54 sceneBusy                                  ;@line 632
					_label468:
						Cast ::temp54 ::temp54                                   ;@line 632
						JumpT ::temp54 _label469                                 ;@line 632
						Not ::temp55 recoveryRequested                           ;@line 632
						Cast ::temp54 ::temp55                                   ;@line 632
					_label469:
						Cast ::temp55 ::temp54                                   ;@line 632
						JumpT ::temp55 _label470                                 ;@line 632
						Cast ::temp55 destroyed                                  ;@line 632
					_label470:
						Cast ::temp54 ::temp55                                   ;@line 632
						JumpT ::temp54 _label471                                 ;@line 632
						Cast ::temp54 faulted                                    ;@line 632
					_label471:
						JumpF ::temp54 _label472                                 ;@line 632
						Return None                                              ;@line 633
						Jump _label472                                           ;@line 633
					_label472:
						JumpF loaded _label473                                   ;@line 635
						CallMethod RegisterForSingleUpdate self ::NoneVar 0.200000  ;@line 636
						Jump _label473                                           ;@line 636
					_label473:
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
						CallMethod InvalidatePlayerLease self ::NoneVar          ;@line 99
						CallMethod Shutdown self ::NoneVar                       ;@line 100
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
						CallMethod InvalidatePlayerLease self ::NoneVar          ;@line 92
						CallMethod BeginRecovery self ::NoneVar                  ;@line 95
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
						.local ::temp159 Bool
						.local ::temp160 Bool
						.local valid Bool
						.local ::NoneVar None
						.local ::temp161 actor
					.endLocalTable
					.code
						CallMethod Current self ::temp159 expectedGeneration expectedToken  ;@line 1294
						Cast ::temp159 ::temp159                                 ;@line 1294
						JumpF ::temp159 _label474                                ;@line 1294
						CompareEQ ::temp160 ownedGuard candidate                 ;@line 1294
						Cast ::temp159 ::temp160                                 ;@line 1294
					_label474:
						Assign valid ::temp159                                   ;@line 1294
						Not ::temp160 valid                                      ;@line 1295
						JumpF ::temp160 _label475                                ;@line 1295
						CallMethod StopGuardPose self ::NoneVar candidate        ;@line 1296
						CallMethod SetDontMove candidate ::NoneVar False         ;@line 1297
						CompareEQ ::temp159 ownedGuard candidate                 ;@line 1298
						JumpF ::temp159 _label476                                ;@line 1298
						Cast ::temp161 None                                      ;@line 1299
						Assign ownedGuard ::temp161                              ;@line 1299
						Jump _label476                                           ;@line 1299
					_label476:
						Jump _label475                                           ;@line 1299
					_label475:
						Assign pinBusy False                                     ;@line 1302
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 1303
						Return valid                                             ;@line 1304
					.endCode
				.endFunction
				.function NormalizeTimingProperties
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp29 Bool
						.local ::temp32 Float
						.local ::temp30 Bool
						.local ::temp31 Bool
					.endLocalTable
					.code
						CompareLT ::temp29 timingRevision 14                     ;@line 302
						JumpF ::temp29 _label477                                 ;@line 302
						CompareGTE ::temp30 ::FireSeconds_var 0.299990           ;@line 303
						Cast ::temp30 ::temp30                                   ;@line 303
						JumpF ::temp30 _label478                                 ;@line 303
						CompareLTE ::temp31 ::FireSeconds_var 0.300010           ;@line 303
						Cast ::temp30 ::temp31                                   ;@line 303
					_label478:
						JumpF ::temp30 _label479                                 ;@line 303
						Assign ::FireSeconds_var 0.200000                        ;@line 304
						Jump _label479                                           ;@line 304
					_label479:
						CompareGTE ::temp31 ::ReleaseSeconds_var 0.099990        ;@line 306
						Cast ::temp31 ::temp31                                   ;@line 306
						JumpF ::temp31 _label480                                 ;@line 306
						CompareLTE ::temp30 ::ReleaseSeconds_var 0.100010        ;@line 306
						Cast ::temp31 ::temp30                                   ;@line 306
					_label480:
						JumpF ::temp31 _label481                                 ;@line 306
						Assign ::ReleaseSeconds_var 0.066667                     ;@line 307
						Jump _label481                                           ;@line 307
					_label481:
						CompareGTE ::temp30 ::ResetSeconds_var 1.199990          ;@line 309
						Cast ::temp30 ::temp30                                   ;@line 309
						JumpF ::temp30 _label482                                 ;@line 309
						CompareLTE ::temp31 ::ResetSeconds_var 1.200010          ;@line 309
						Cast ::temp30 ::temp31                                   ;@line 309
					_label482:
						JumpF ::temp30 _label483                                 ;@line 309
						Assign ::ResetSeconds_var 0.800000                       ;@line 310
						Jump _label483                                           ;@line 310
					_label483:
						CompareGTE ::temp31 ::CadenceSeconds_var 3.999990        ;@line 312
						Cast ::temp31 ::temp31                                   ;@line 312
						JumpF ::temp31 _label484                                 ;@line 312
						CompareLTE ::temp30 ::CadenceSeconds_var 4.000010        ;@line 312
						Cast ::temp31 ::temp30                                   ;@line 312
					_label484:
						JumpF ::temp31 _label485                                 ;@line 312
						Assign ::CadenceSeconds_var 2.500000                     ;@line 313
						Jump _label485                                           ;@line 313
					_label485:
						Assign timingRevision 14                                 ;@line 315
						Jump _label477                                           ;@line 315
					_label477:
						CallMethod Finite self ::temp30 ::FireSeconds_var 0.200000 2.000000  ;@line 317
						Not ::temp31 ::temp30                                    ;@line 317
						JumpF ::temp31 _label486                                 ;@line 317
						Assign ::FireSeconds_var 0.200000                        ;@line 318
						Jump _label486                                           ;@line 318
					_label486:
						CallMethod Finite self ::temp29 ::ReleaseSeconds_var 0.066667 1.000000  ;@line 320
						Not ::temp30 ::temp29                                    ;@line 320
						Cast ::temp29 ::temp30                                   ;@line 320
						JumpT ::temp29 _label487                                 ;@line 320
						CompareGT ::temp31 ::ReleaseSeconds_var ::FireSeconds_var  ;@line 320
						Cast ::temp29 ::temp31                                   ;@line 320
					_label487:
						JumpF ::temp29 _label488                                 ;@line 320
						Assign ::ReleaseSeconds_var 0.066667                     ;@line 321
						Jump _label488                                           ;@line 321
					_label488:
						CallMethod Finite self ::temp30 ::ResetSeconds_var 0.800000 5.000000  ;@line 323
						Not ::temp31 ::temp30                                    ;@line 323
						JumpF ::temp31 _label489                                 ;@line 323
						Assign ::ResetSeconds_var 0.800000                       ;@line 324
						Jump _label489                                           ;@line 324
					_label489:
						CallMethod SafeCadenceSeconds self ::temp32              ;@line 326
						Assign ::CadenceSeconds_var ::temp32                     ;@line 326
					.endCode
				.endFunction
			.endState
		.endStateTable
	.endObject
.endObjectTable
