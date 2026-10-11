.info
	.source "AstraAsedioGuard.psc"
	.modifyTime 1791645499 ;Sat Oct 10 12:18:19 2026 Local
	.compileTime 1791678044 ;Sat Oct 10 21:20:44 2026 Local
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
			.variable yawMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable matricesReady Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::VisualBoltNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "VIROTE_VISUAL"
			.endVariable
			.variable ::FireSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.200000
			.endVariable
			.variable ::AllowPlayerTakeover_var Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable rootPosition Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable playerReady Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::YawNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "CTRL_GIRO_360"
			.endVariable
			.variable ::ShotSound_var sound
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::MuzzleNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "ProjectileNode"
			.endVariable
			.variable recoveryRequested Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable yaw Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable nextShotAt Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::ReleaseSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.066667
			.endVariable
			.variable ::Launcher_var weapon
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::PitchMax_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 45.000000
			.endVariable
			.variable aimZ Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable updating Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::ProjectileGravity_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 240.345001
			.endVariable
			.variable stationRetired Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable serial Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable ::TargetHeight_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 60.000000
			.endVariable
			.variable targetHorizontal Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable phase Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable shotTarget actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable desiredYaw Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable playerRestored Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable pitch Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable token Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1
			.endVariable
			.variable ::YawHalfSector_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 60.000000
			.endVariable
			.variable lastTick Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable phaseAt Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable rootWorldMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable destroyed Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable yawBase Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable desiredPitch Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable timingRevision Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable ::Standby_var ObjectReference
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable aimX Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable muzzleWorldMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::ResetSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.800000
			.endVariable
			.variable playerReserved Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable running Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::YawCenter_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable pitchMatrix Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::Artillero_var actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable generation Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable pinBusy Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable playerSerial Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable ::TurnRate_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 30.000000
			.endVariable
			.variable sceneBusy Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::Puesto_var ObjectReference
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable playerLease Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable ::PitchMin_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue -20.000000
			.endVariable
			.variable ::ProjectileSpeed_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 5400.000000
			.endVariable
			.variable pitchBase Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable recovering Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::ShotAmmo_var ammo
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::CadenceSeconds_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 2.500000
			.endVariable
			.variable ::PitchNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "CTRL_ELEVACION"
			.endVariable
			.variable muzzlePosition Float[]
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable faulted Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ownedGuard actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable aimY Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1.000000
			.endVariable
		.endVariableTable
		.propertyTable
			.property ProjectileSpeed Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ProjectileSpeed_var
			.endProperty
			.property ResetSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ResetSeconds_var
			.endProperty
			.property ReleaseSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ReleaseSeconds_var
			.endProperty
			.property MuzzleNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::MuzzleNode_var
			.endProperty
			.property Artillero actor auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Artillero_var
			.endProperty
			.property PitchMin Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchMin_var
			.endProperty
			.property PitchNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchNode_var
			.endProperty
			.property Launcher weapon auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Launcher_var
			.endProperty
			.property Standby ObjectReference auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Standby_var
			.endProperty
			.property ShotAmmo ammo auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ShotAmmo_var
			.endProperty
			.property ProjectileGravity Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ProjectileGravity_var
			.endProperty
			.property TargetHeight Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::TargetHeight_var
			.endProperty
			.property YawCenter Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::YawCenter_var
			.endProperty
			.property FireSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::FireSeconds_var
			.endProperty
			.property TurnRate Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::TurnRate_var
			.endProperty
			.property CadenceSeconds Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::CadenceSeconds_var
			.endProperty
			.property Puesto ObjectReference auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Puesto_var
			.endProperty
			.property VisualBoltNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::VisualBoltNode_var
			.endProperty
			.property YawHalfSector Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::YawHalfSector_var
			.endProperty
			.property YawNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::YawNode_var
			.endProperty
			.property PitchMax Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchMax_var
			.endProperty
			.property ShotSound sound auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ShotSound_var
			.endProperty
			.property AllowPlayerTakeover Bool auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::AllowPlayerTakeover_var
			.endProperty
		.endPropertyTable
		.stateTable
			.state 
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
						.local ::temp96 Bool
						.local ::temp97 actor
						.local ::temp98 Bool
						.local ::temp99 Int
						.local ::temp100 ObjectReference
						.local player actor
						.local valid Bool
						.local visible Bool
						.local combatTarget actor
					.endLocalTable
					.code
						CallMethod GuardReady self ::temp96 expectedGeneration expectedToken  ;@line 791
						Not ::temp96 ::temp96                                    ;@line 791
						Cast ::temp96 ::temp96                                   ;@line 791
						JumpT ::temp96 _label0                                   ;@line 791
						Cast ::temp97 None                                       ;@line 791
						CompareEQ ::temp98 target ::temp97                       ;@line 791
						Cast ::temp96 ::temp98                                   ;@line 791
					_label0:
						Cast ::temp96 ::temp96                                   ;@line 791
						JumpT ::temp96 _label1                                   ;@line 791
						CompareEQ ::temp98 target ::Artillero_var                ;@line 791
						Cast ::temp96 ::temp98                                   ;@line 791
					_label1:
						JumpF ::temp96 _label2                                   ;@line 791
						Return False                                             ;@line 792
						Jump _label2                                             ;@line 792
					_label2:
						CallStatic game GetPlayer ::temp97                       ;@line 794
						Assign player ::temp97                                   ;@line 794
						CallMethod Current self ::temp98 expectedGeneration expectedToken  ;@line 795
						Not ::temp96 ::temp98                                    ;@line 795
						Cast ::temp96 ::temp96                                   ;@line 795
						JumpT ::temp96 _label3                                   ;@line 795
						CompareEQ ::temp98 target player                         ;@line 795
						Cast ::temp96 ::temp98                                   ;@line 795
					_label3:
						JumpF ::temp96 _label4                                   ;@line 795
						Return False                                             ;@line 796
						Jump _label4                                             ;@line 796
					_label4:
						CallMethod Is3DLoaded target ::temp98                    ;@line 798
						Cast ::temp98 ::temp98                                   ;@line 798
						JumpF ::temp98 _label5                                   ;@line 798
						CallMethod IsDisabled target ::temp96                    ;@line 798
						Not ::temp96 ::temp96                                    ;@line 798
						Cast ::temp98 ::temp96                                   ;@line 798
					_label5:
						Cast ::temp98 ::temp98                                   ;@line 798
						JumpF ::temp98 _label6                                   ;@line 798
						CallMethod IsDead target ::temp96                        ;@line 798
						Not ::temp96 ::temp96                                    ;@line 798
						Cast ::temp98 ::temp96                                   ;@line 798
					_label6:
						Cast ::temp98 ::temp98                                   ;@line 798
						JumpF ::temp98 _label7                                   ;@line 798
						CallMethod IsPlayerTeammate target ::temp96              ;@line 798
						Not ::temp96 ::temp96                                    ;@line 798
						Cast ::temp98 ::temp96                                   ;@line 798
					_label7:
						Cast ::temp98 ::temp98                                   ;@line 798
						JumpF ::temp98 _label8                                   ;@line 798
						CallMethod IsHostileToActor target ::temp96 ::Artillero_var  ;@line 798
						Cast ::temp98 ::temp96                                   ;@line 798
					_label8:
						Cast ::temp98 ::temp98                                   ;@line 798
						JumpF ::temp98 _label9                                   ;@line 798
						CallMethod GetCombatState target ::temp99                ;@line 798
						CompareGT ::temp96 ::temp99 0                            ;@line 798
						Cast ::temp98 ::temp96                                   ;@line 798
					_label9:
						Cast ::temp98 ::temp98                                   ;@line 798
						JumpF ::temp98 _label10                                  ;@line 798
						CallMethod GetCombatState ::Artillero_var ::temp99       ;@line 798
						CompareEQ ::temp96 ::temp99 1                            ;@line 798
						Cast ::temp98 ::temp96                                   ;@line 798
					_label10:
						Assign valid ::temp98                                    ;@line 798
						Cast ::temp100 target                                    ;@line 799
						CallMethod HasLOS ::Artillero_var ::temp96 ::temp100     ;@line 799
						Assign visible ::temp96                                  ;@line 799
						CallMethod GetCombatTarget ::Artillero_var ::temp97      ;@line 800
						Assign combatTarget ::temp97                             ;@line 800
						CallMethod Current self ::temp98 expectedGeneration expectedToken  ;@line 801
						Cast ::temp96 ::temp98                                   ;@line 801
						JumpF ::temp96 _label11                                  ;@line 801
						Cast ::temp96 valid                                      ;@line 801
					_label11:
						Cast ::temp98 ::temp96                                   ;@line 801
						JumpF ::temp98 _label12                                  ;@line 801
						Cast ::temp98 visible                                    ;@line 801
					_label12:
						Cast ::temp98 ::temp98                                   ;@line 801
						JumpF ::temp98 _label13                                  ;@line 801
						CompareEQ ::temp96 combatTarget target                   ;@line 801
						Cast ::temp98 ::temp96                                   ;@line 801
					_label13:
						Return ::temp98                                          ;@line 801
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
						.local ::temp101 Float
						.local ::temp102 Float
						.local ::temp103 Bool
						.local ::temp104 Bool
						.local horizontal Float
						.local cosine Float
						.local angle Float
					.endLocalTable
					.code
						FMultiply ::temp101 vectorX vectorX                      ;@line 805
						FMultiply ::temp102 vectorY vectorY                      ;@line 805
						FAdd ::temp101 ::temp101 ::temp102                       ;@line 805
						CallStatic math Sqrt ::temp102 ::temp101                 ;@line 805
						Assign horizontal ::temp102                              ;@line 805
						CompareLT ::temp103 horizontal 0.000010                  ;@line 806
						JumpF ::temp103 _label14                                 ;@line 806
						Return fallback                                          ;@line 807
						Jump _label14                                            ;@line 807
					_label14:
						FDivide ::temp101 vectorY horizontal                     ;@line 809
						Assign cosine ::temp101                                  ;@line 809
						CompareGT ::temp103 cosine 1.000000                      ;@line 810
						JumpF ::temp103 _label15                                 ;@line 810
						Assign cosine 1.000000                                   ;@line 811
						Jump _label16                                            ;@line 811
					_label15:
						CompareLT ::temp104 cosine -1.000000                     ;@line 812
						JumpF ::temp104 _label16                                 ;@line 812
						Assign cosine -1.000000                                  ;@line 813
						Jump _label16                                            ;@line 813
					_label16:
						CallStatic math ACos ::temp102 cosine                    ;@line 815
						Assign angle ::temp102                                   ;@line 815
						CompareLT ::temp104 vectorX 0.000000                     ;@line 816
						JumpF ::temp104 _label17                                 ;@line 816
						FSubtract ::temp101 360.000000 angle                     ;@line 817
						Assign angle ::temp101                                   ;@line 817
						Jump _label17                                            ;@line 817
					_label17:
						CompareGTE ::temp103 angle 360.000000                    ;@line 819
						JumpF ::temp103 _label18                                 ;@line 819
						FSubtract ::temp102 angle 360.000000                     ;@line 820
						Assign angle ::temp102                                   ;@line 820
						Jump _label18                                            ;@line 820
					_label18:
						Return angle                                             ;@line 822
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
						.local ::temp115 Bool
						.local ::temp116 Float
						.local ::NoneVar None
						.local rate Float
						.local nextYaw Float
						.local nextPitch Float
					.endLocalTable
					.code
						Assign rate ::TurnRate_var                               ;@line 915
						CallMethod Finite self ::temp115 rate 1.000000 30.000000  ;@line 916
						Not ::temp115 ::temp115                                  ;@line 916
						JumpF ::temp115 _label19                                 ;@line 916
						Assign rate 30.000000                                    ;@line 917
						Jump _label19                                            ;@line 917
					_label19:
						FMultiply ::temp116 rate dt                              ;@line 919
						CallMethod Approach self ::temp116 yaw desiredYaw ::temp116  ;@line 919
						Assign nextYaw ::temp116                                 ;@line 919
						FMultiply ::temp116 rate dt                              ;@line 920
						CallMethod Approach self ::temp116 pitch desiredPitch ::temp116  ;@line 920
						Assign nextPitch ::temp116                               ;@line 920
						CallMethod Current self ::temp115 expectedGeneration expectedToken  ;@line 921
						Not ::temp115 ::temp115                                  ;@line 921
						JumpF ::temp115 _label20                                 ;@line 921
						Return None                                              ;@line 922
						Jump _label20                                            ;@line 922
					_label20:
						Assign yaw nextYaw                                       ;@line 924
						Assign pitch nextPitch                                   ;@line 925
						CallMethod ApplyAim self ::NoneVar expectedGeneration expectedToken  ;@line 926
					.endCode
				.endFunction
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
						Not ::temp13 ::AllowPlayerTakeover_var                   ;@line 156
						Cast ::temp13 ::temp13                                   ;@line 156
						JumpT ::temp13 _label21                                  ;@line 156
						Cast ::temp13 stationRetired                             ;@line 156
					_label21:
						Cast ::temp13 ::temp13                                   ;@line 156
						JumpT ::temp13 _label22                                  ;@line 156
						Cast ::temp13 destroyed                                  ;@line 156
					_label22:
						Cast ::temp13 ::temp13                                   ;@line 156
						JumpT ::temp13 _label23                                  ;@line 156
						Cast ::temp13 playerReserved                             ;@line 156
					_label23:
						Cast ::temp13 ::temp13                                   ;@line 156
						JumpT ::temp13 _label24                                  ;@line 156
						Cast ::temp14 None                                       ;@line 156
						CompareEQ ::temp15 ::Standby_var ::temp14                ;@line 156
						Cast ::temp13 ::temp15                                   ;@line 156
					_label24:
						Cast ::temp13 ::temp13                                   ;@line 156
						JumpT ::temp13 _label25                                  ;@line 156
						CompareGTE ::temp15 playerSerial 2000000000              ;@line 156
						Cast ::temp13 ::temp15                                   ;@line 156
					_label25:
						JumpF ::temp13 _label26                                  ;@line 156
						Return -1                                                ;@line 157
						Jump _label26                                            ;@line 157
					_label26:
						CallStatic game GetPlayer ::temp16                       ;@line 159
						Assign player ::temp16                                   ;@line 159
						Cast ::temp15 playerReserved                             ;@line 160
						JumpT ::temp15 _label27                                  ;@line 160
						Cast ::temp15 destroyed                                  ;@line 160
					_label27:
						Cast ::temp15 ::temp15                                   ;@line 160
						JumpT ::temp15 _label28                                  ;@line 160
						Not ::temp13 ::AllowPlayerTakeover_var                   ;@line 160
						Cast ::temp15 ::temp13                                   ;@line 160
					_label28:
						Cast ::temp15 ::temp15                                   ;@line 160
						JumpT ::temp15 _label29                                  ;@line 160
						Cast ::temp14 None                                       ;@line 160
						CompareEQ ::temp13 ::Standby_var ::temp14                ;@line 160
						Cast ::temp15 ::temp13                                   ;@line 160
					_label29:
						Cast ::temp15 ::temp15                                   ;@line 160
						JumpT ::temp15 _label30                                  ;@line 160
						CompareEQ ::temp13 ::Artillero_var player                ;@line 160
						Cast ::temp15 ::temp13                                   ;@line 160
					_label30:
						JumpF ::temp15 _label31                                  ;@line 160
						Return -1                                                ;@line 161
						Jump _label31                                            ;@line 161
					_label31:
						IAdd ::temp17 playerSerial 1                             ;@line 163
						Assign playerSerial ::temp17                             ;@line 163
						Assign lease playerSerial                                ;@line 164
						Assign playerLease lease                                 ;@line 165
						Assign playerReserved True                               ;@line 166
						Assign playerReady False                                 ;@line 167
						Assign playerRestored False                              ;@line 168
						CallMethod Shutdown self ::NoneVar                       ;@line 171
						CallMethod PlayerLeaseCurrent self ::temp13 lease        ;@line 172
						Not ::temp15 ::temp13                                    ;@line 172
						JumpF ::temp15 _label32                                  ;@line 172
						Return -1                                                ;@line 173
						Jump _label32                                            ;@line 173
					_label32:
						Return lease                                             ;@line 175
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
						CallMethod InvalidatePlayerLease self ::NoneVar          ;@line 88
						CallMethod Shutdown self ::NoneVar                       ;@line 89
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
						Assign i 0                                               ;@line 731
					_label35:
						CompareLT ::temp78 i 9                                   ;@line 732
						JumpF ::temp78 _label33                                  ;@line 732
						ArrayGetElement ::temp79 matrix i                        ;@line 733
						CallMethod Finite self ::temp80 ::temp79 -1.050000 1.050000  ;@line 733
						Not ::temp80 ::temp80                                    ;@line 733
						JumpF ::temp80 _label34                                  ;@line 733
						Return False                                             ;@line 734
						Jump _label34                                            ;@line 734
					_label34:
						IAdd ::temp81 i 1                                        ;@line 736
						Assign i ::temp81                                        ;@line 736
						Jump _label35                                            ;@line 736
					_label33:
						ArrayGetElement ::temp79 matrix 0                        ;@line 738
						ArrayGetElement ::temp82 matrix 0                        ;@line 738
						FMultiply ::temp79 ::temp79 ::temp82                     ;@line 738
						ArrayGetElement ::temp82 matrix 3                        ;@line 738
						ArrayGetElement ::temp83 matrix 3                        ;@line 738
						FMultiply ::temp82 ::temp82 ::temp83                     ;@line 738
						FAdd ::temp83 ::temp79 ::temp82                          ;@line 738
						ArrayGetElement ::temp79 matrix 6                        ;@line 738
						ArrayGetElement ::temp82 matrix 6                        ;@line 738
						FMultiply ::temp79 ::temp79 ::temp82                     ;@line 738
						FAdd ::temp82 ::temp83 ::temp79                          ;@line 738
						Assign a ::temp82                                        ;@line 738
						ArrayGetElement ::temp83 matrix 1                        ;@line 739
						ArrayGetElement ::temp79 matrix 1                        ;@line 739
						FMultiply ::temp82 ::temp83 ::temp79                     ;@line 739
						ArrayGetElement ::temp83 matrix 4                        ;@line 739
						ArrayGetElement ::temp79 matrix 4                        ;@line 739
						FMultiply ::temp83 ::temp83 ::temp79                     ;@line 739
						FAdd ::temp79 ::temp82 ::temp83                          ;@line 739
						ArrayGetElement ::temp82 matrix 7                        ;@line 739
						ArrayGetElement ::temp83 matrix 7                        ;@line 739
						FMultiply ::temp82 ::temp82 ::temp83                     ;@line 739
						FAdd ::temp83 ::temp79 ::temp82                          ;@line 739
						Assign b ::temp83                                        ;@line 739
						ArrayGetElement ::temp79 matrix 2                        ;@line 740
						ArrayGetElement ::temp82 matrix 2                        ;@line 740
						FMultiply ::temp83 ::temp79 ::temp82                     ;@line 740
						ArrayGetElement ::temp79 matrix 5                        ;@line 740
						ArrayGetElement ::temp82 matrix 5                        ;@line 740
						FMultiply ::temp79 ::temp79 ::temp82                     ;@line 740
						FAdd ::temp82 ::temp83 ::temp79                          ;@line 740
						ArrayGetElement ::temp83 matrix 8                        ;@line 740
						ArrayGetElement ::temp79 matrix 8                        ;@line 740
						FMultiply ::temp83 ::temp83 ::temp79                     ;@line 740
						FAdd ::temp79 ::temp82 ::temp83                          ;@line 740
						Assign c ::temp79                                        ;@line 740
						ArrayGetElement ::temp82 matrix 0                        ;@line 741
						ArrayGetElement ::temp83 matrix 1                        ;@line 741
						FMultiply ::temp79 ::temp82 ::temp83                     ;@line 741
						ArrayGetElement ::temp82 matrix 3                        ;@line 741
						ArrayGetElement ::temp83 matrix 4                        ;@line 741
						FMultiply ::temp82 ::temp82 ::temp83                     ;@line 741
						FAdd ::temp83 ::temp79 ::temp82                          ;@line 741
						ArrayGetElement ::temp79 matrix 6                        ;@line 741
						ArrayGetElement ::temp82 matrix 7                        ;@line 741
						FMultiply ::temp79 ::temp79 ::temp82                     ;@line 741
						FAdd ::temp82 ::temp83 ::temp79                          ;@line 741
						Assign ab ::temp82                                       ;@line 741
						ArrayGetElement ::temp83 matrix 0                        ;@line 742
						ArrayGetElement ::temp79 matrix 2                        ;@line 742
						FMultiply ::temp82 ::temp83 ::temp79                     ;@line 742
						ArrayGetElement ::temp83 matrix 3                        ;@line 742
						ArrayGetElement ::temp79 matrix 5                        ;@line 742
						FMultiply ::temp83 ::temp83 ::temp79                     ;@line 742
						FAdd ::temp79 ::temp82 ::temp83                          ;@line 742
						ArrayGetElement ::temp82 matrix 6                        ;@line 742
						ArrayGetElement ::temp83 matrix 8                        ;@line 742
						FMultiply ::temp82 ::temp82 ::temp83                     ;@line 742
						FAdd ::temp83 ::temp79 ::temp82                          ;@line 742
						Assign ac ::temp83                                       ;@line 742
						ArrayGetElement ::temp79 matrix 1                        ;@line 743
						ArrayGetElement ::temp82 matrix 2                        ;@line 743
						FMultiply ::temp83 ::temp79 ::temp82                     ;@line 743
						ArrayGetElement ::temp79 matrix 4                        ;@line 743
						ArrayGetElement ::temp82 matrix 5                        ;@line 743
						FMultiply ::temp79 ::temp79 ::temp82                     ;@line 743
						FAdd ::temp82 ::temp83 ::temp79                          ;@line 743
						ArrayGetElement ::temp83 matrix 7                        ;@line 743
						ArrayGetElement ::temp79 matrix 8                        ;@line 743
						FMultiply ::temp83 ::temp83 ::temp79                     ;@line 743
						FAdd ::temp79 ::temp82 ::temp83                          ;@line 743
						Assign bc ::temp79                                       ;@line 743
						ArrayGetElement ::temp82 matrix 0                        ;@line 744
						ArrayGetElement ::temp83 matrix 4                        ;@line 744
						ArrayGetElement ::temp79 matrix 8                        ;@line 744
						FMultiply ::temp83 ::temp83 ::temp79                     ;@line 744
						ArrayGetElement ::temp79 matrix 5                        ;@line 744
						ArrayGetElement ::temp84 matrix 7                        ;@line 744
						FMultiply ::temp79 ::temp79 ::temp84                     ;@line 744
						FSubtract ::temp84 ::temp83 ::temp79                     ;@line 744
						FMultiply ::temp83 ::temp82 ::temp84                     ;@line 744
						ArrayGetElement ::temp79 matrix 1                        ;@line 744
						ArrayGetElement ::temp82 matrix 3                        ;@line 744
						ArrayGetElement ::temp84 matrix 8                        ;@line 744
						FMultiply ::temp82 ::temp82 ::temp84                     ;@line 744
						ArrayGetElement ::temp84 matrix 5                        ;@line 744
						ArrayGetElement ::temp85 matrix 6                        ;@line 744
						FMultiply ::temp84 ::temp84 ::temp85                     ;@line 744
						FSubtract ::temp85 ::temp82 ::temp84                     ;@line 744
						FMultiply ::temp82 ::temp79 ::temp85                     ;@line 744
						FSubtract ::temp84 ::temp83 ::temp82                     ;@line 744
						ArrayGetElement ::temp79 matrix 2                        ;@line 744
						ArrayGetElement ::temp85 matrix 3                        ;@line 744
						ArrayGetElement ::temp83 matrix 7                        ;@line 744
						FMultiply ::temp82 ::temp85 ::temp83                     ;@line 744
						ArrayGetElement ::temp85 matrix 4                        ;@line 744
						ArrayGetElement ::temp83 matrix 6                        ;@line 744
						FMultiply ::temp85 ::temp85 ::temp83                     ;@line 744
						FSubtract ::temp83 ::temp82 ::temp85                     ;@line 744
						FMultiply ::temp82 ::temp79 ::temp83                     ;@line 744
						FAdd ::temp85 ::temp84 ::temp82                          ;@line 744
						Assign determinant ::temp85                              ;@line 744
						FSubtract ::temp79 a 1.000000                            ;@line 745
						CallStatic math Abs ::temp83 ::temp79                    ;@line 745
						CompareLTE ::temp80 ::temp83 0.002000                    ;@line 745
						Cast ::temp80 ::temp80                                   ;@line 745
						JumpF ::temp80 _label36                                  ;@line 745
						FSubtract ::temp84 b 1.000000                            ;@line 745
						CallStatic math Abs ::temp82 ::temp84                    ;@line 745
						CompareLTE ::temp78 ::temp82 0.002000                    ;@line 745
						Cast ::temp80 ::temp78                                   ;@line 745
					_label36:
						Cast ::temp80 ::temp80                                   ;@line 745
						JumpF ::temp80 _label37                                  ;@line 745
						FSubtract ::temp85 c 1.000000                            ;@line 745
						CallStatic math Abs ::temp79 ::temp85                    ;@line 745
						CompareLTE ::temp78 ::temp79 0.002000                    ;@line 745
						Cast ::temp80 ::temp78                                   ;@line 745
					_label37:
						Cast ::temp80 ::temp80                                   ;@line 745
						JumpF ::temp80 _label38                                  ;@line 745
						CallStatic math Abs ::temp83 ab                          ;@line 745
						CompareLTE ::temp78 ::temp83 0.002000                    ;@line 745
						Cast ::temp80 ::temp78                                   ;@line 745
					_label38:
						Cast ::temp80 ::temp80                                   ;@line 745
						JumpF ::temp80 _label39                                  ;@line 745
						CallStatic math Abs ::temp84 ac                          ;@line 745
						CompareLTE ::temp78 ::temp84 0.002000                    ;@line 745
						Cast ::temp80 ::temp78                                   ;@line 745
					_label39:
						Cast ::temp80 ::temp80                                   ;@line 745
						JumpF ::temp80 _label40                                  ;@line 745
						CallStatic math Abs ::temp82 bc                          ;@line 745
						CompareLTE ::temp78 ::temp82 0.002000                    ;@line 745
						Cast ::temp80 ::temp78                                   ;@line 745
					_label40:
						Cast ::temp80 ::temp80                                   ;@line 745
						JumpF ::temp80 _label41                                  ;@line 745
						FSubtract ::temp85 determinant 1.000000                  ;@line 745
						CallStatic math Abs ::temp79 ::temp85                    ;@line 745
						CompareLTE ::temp78 ::temp79 0.004000                    ;@line 745
						Cast ::temp80 ::temp78                                   ;@line 745
					_label41:
						Return ::temp80                                          ;@line 745
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
						CallMethod Current self ::temp86 expectedGeneration expectedToken  ;@line 749
						Not ::temp86 ::temp86                                    ;@line 749
						Cast ::temp86 ::temp86                                   ;@line 749
						JumpT ::temp86 _label42                                  ;@line 749
						Not ::temp87 matricesReady                               ;@line 749
						Cast ::temp86 ::temp87                                   ;@line 749
					_label42:
						JumpF ::temp86 _label43                                  ;@line 749
						Return False                                             ;@line 750
						Jump _label43                                            ;@line 750
					_label43:
						Cast ::temp88 self                                       ;@line 752
						CallStatic netimmerse GetNodeWorldRotationMatrix ::temp87 ::temp88 "" rootWorldMatrix False  ;@line 752
						Assign rootRead ::temp87                                 ;@line 752
						CallMethod Current self ::temp86 expectedGeneration expectedToken  ;@line 753
						Not ::temp87 ::temp86                                    ;@line 753
						Cast ::temp87 ::temp87                                   ;@line 753
						JumpT ::temp87 _label44                                  ;@line 753
						Not ::temp86 rootRead                                    ;@line 753
						Cast ::temp87 ::temp86                                   ;@line 753
					_label44:
						JumpF ::temp87 _label45                                  ;@line 753
						Return False                                             ;@line 754
						Jump _label45                                            ;@line 754
					_label45:
						Cast ::temp88 self                                       ;@line 756
						CallStatic netimmerse GetNodeWorldRotationMatrix ::temp86 ::temp88 ::MuzzleNode_var muzzleWorldMatrix False  ;@line 756
						Assign muzzleRead ::temp86                               ;@line 756
						CallMethod Current self ::temp87 expectedGeneration expectedToken  ;@line 757
						Not ::temp86 ::temp87                                    ;@line 757
						Cast ::temp86 ::temp86                                   ;@line 757
						JumpT ::temp86 _label46                                  ;@line 757
						Not ::temp87 muzzleRead                                  ;@line 757
						Cast ::temp86 ::temp87                                   ;@line 757
					_label46:
						JumpF ::temp86 _label47                                  ;@line 757
						Return False                                             ;@line 758
						Jump _label47                                            ;@line 758
					_label47:
						Cast ::temp88 self                                       ;@line 760
						CallStatic netimmerse GetNodeWorldPosition ::temp87 ::temp88 "" rootPosition False  ;@line 760
						Assign rootPointRead ::temp87                            ;@line 760
						CallMethod Current self ::temp86 expectedGeneration expectedToken  ;@line 761
						Not ::temp87 ::temp86                                    ;@line 761
						Cast ::temp87 ::temp87                                   ;@line 761
						JumpT ::temp87 _label48                                  ;@line 761
						Not ::temp86 rootPointRead                               ;@line 761
						Cast ::temp87 ::temp86                                   ;@line 761
					_label48:
						JumpF ::temp87 _label49                                  ;@line 761
						Return False                                             ;@line 762
						Jump _label49                                            ;@line 762
					_label49:
						Cast ::temp88 self                                       ;@line 764
						CallStatic netimmerse GetNodeWorldPosition ::temp86 ::temp88 ::MuzzleNode_var muzzlePosition False  ;@line 764
						Assign muzzlePointRead ::temp86                          ;@line 764
						CallMethod Current self ::temp87 expectedGeneration expectedToken  ;@line 765
						Not ::temp86 ::temp87                                    ;@line 765
						Cast ::temp86 ::temp86                                   ;@line 765
						JumpT ::temp86 _label50                                  ;@line 765
						Not ::temp87 muzzlePointRead                             ;@line 765
						Cast ::temp86 ::temp87                                   ;@line 765
					_label50:
						JumpF ::temp86 _label51                                  ;@line 765
						Return False                                             ;@line 766
						Jump _label51                                            ;@line 766
					_label51:
						CallMethod RotationValid self ::temp87 rootWorldMatrix   ;@line 768
						Not ::temp86 ::temp87                                    ;@line 768
						Cast ::temp86 ::temp86                                   ;@line 768
						JumpT ::temp86 _label52                                  ;@line 768
						CallMethod RotationValid self ::temp87 muzzleWorldMatrix  ;@line 768
						Not ::temp87 ::temp87                                    ;@line 768
						Cast ::temp86 ::temp87                                   ;@line 768
					_label52:
						JumpF ::temp86 _label53                                  ;@line 768
						Return False                                             ;@line 769
						Jump _label53                                            ;@line 769
					_label53:
						Assign i 0                                               ;@line 771
					_label57:
						CompareLT ::temp87 i 3                                   ;@line 772
						JumpF ::temp87 _label54                                  ;@line 772
						ArrayGetElement ::temp89 rootPosition i                  ;@line 773
						CallMethod Finite self ::temp86 ::temp89 -1000000.000000 1000000.000000  ;@line 773
						Not ::temp86 ::temp86                                    ;@line 773
						Cast ::temp86 ::temp86                                   ;@line 773
						JumpT ::temp86 _label55                                  ;@line 773
						ArrayGetElement ::temp89 muzzlePosition i                ;@line 773
						CallMethod Finite self ::temp90 ::temp89 -1000000.000000 1000000.000000  ;@line 773
						Not ::temp90 ::temp90                                    ;@line 773
						Cast ::temp86 ::temp90                                   ;@line 773
					_label55:
						JumpF ::temp86 _label56                                  ;@line 773
						Return False                                             ;@line 774
						Jump _label56                                            ;@line 774
					_label56:
						IAdd ::temp91 i 1                                        ;@line 776
						Assign i ::temp91                                        ;@line 776
						Jump _label57                                            ;@line 776
					_label54:
						CallMethod Current self ::temp90 expectedGeneration expectedToken  ;@line 778
						Return ::temp90                                          ;@line 778
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
						CallMethod PlayerLeaseCurrent self ::temp26 lease        ;@line 273
						Not ::temp26 ::temp26                                    ;@line 273
						JumpF ::temp26 _label58                                  ;@line 273
						Return False                                             ;@line 274
						Jump _label58                                            ;@line 274
					_label58:
						CallMethod InvalidatePlayerLease self ::NoneVar          ;@line 276
						CallMethod Shutdown self ::NoneVar                       ;@line 277
						CallMethod BeginRecovery self ::NoneVar                  ;@line 280
						Return True                                              ;@line 281
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
						CompareEQ ::temp27 value value                           ;@line 285
						Cast ::temp27 ::temp27                                   ;@line 285
						JumpF ::temp27 _label59                                  ;@line 285
						CompareGTE ::temp28 value minimum                        ;@line 285
						Cast ::temp27 ::temp28                                   ;@line 285
					_label59:
						Cast ::temp27 ::temp27                                   ;@line 285
						JumpF ::temp27 _label60                                  ;@line 285
						CompareLTE ::temp28 value maximum                        ;@line 285
						Cast ::temp27 ::temp28                                   ;@line 285
					_label60:
						Return ::temp27                                          ;@line 285
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
						JumpF pinBusy _label61                                   ;@line 577
						Return None                                              ;@line 578
						Jump _label61                                            ;@line 578
					_label61:
						Assign previousGuard ownedGuard                          ;@line 580
						Cast ::temp52 None                                       ;@line 581
						Assign ownedGuard ::temp52                               ;@line 581
						Cast ::temp52 None                                       ;@line 582
						CompareEQ ::temp53 previousGuard ::temp52                ;@line 582
						JumpF ::temp53 _label62                                  ;@line 582
						Return None                                              ;@line 583
						Jump _label62                                            ;@line 583
					_label62:
						Assign pinBusy True                                      ;@line 585
						CallStatic game GetPlayer ::temp52                       ;@line 586
						Assign player ::temp52                                   ;@line 586
						CompareEQ ::temp53 previousGuard player                  ;@line 587
						Not ::temp53 ::temp53                                    ;@line 587
						JumpF ::temp53 _label63                                  ;@line 587
						CallMethod SetDontMove previousGuard ::NoneVar False     ;@line 588
						Jump _label63                                            ;@line 588
					_label63:
						Assign pinBusy False                                     ;@line 590
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 591
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
						CallMethod BlockActivation self ::NoneVar True           ;@line 76
						CallMethod BeginRecovery self ::NoneVar                  ;@line 77
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
						.local ::temp132 Bool
						.local ::temp133 Bool
						.local ::temp134 Float
						.local now Float
						.local cadence Float
						.local started Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod Current self ::temp132 expectedGeneration expectedToken  ;@line 1032
						Not ::temp132 ::temp132                                  ;@line 1032
						Cast ::temp132 ::temp132                                 ;@line 1032
						JumpT ::temp132 _label64                                 ;@line 1032
						CompareEQ ::temp133 phase 0                              ;@line 1032
						Not ::temp133 ::temp133                                  ;@line 1032
						Cast ::temp132 ::temp133                                 ;@line 1032
					_label64:
						JumpF ::temp132 _label65                                 ;@line 1032
						Return None                                              ;@line 1033
						Jump _label65                                            ;@line 1033
					_label65:
						CallStatic utility GetCurrentRealTime ::temp134          ;@line 1035
						Assign now ::temp134                                     ;@line 1035
						CallMethod Current self ::temp133 expectedGeneration expectedToken  ;@line 1036
						Not ::temp132 ::temp133                                  ;@line 1036
						Cast ::temp132 ::temp132                                 ;@line 1036
						JumpT ::temp132 _label66                                 ;@line 1036
						CompareEQ ::temp133 phase 0                              ;@line 1036
						Not ::temp133 ::temp133                                  ;@line 1036
						Cast ::temp132 ::temp133                                 ;@line 1036
					_label66:
						Cast ::temp132 ::temp132                                 ;@line 1036
						JumpT ::temp132 _label67                                 ;@line 1036
						CallMethod Finite self ::temp133 now 0.000000 1000000000.000000  ;@line 1036
						Not ::temp133 ::temp133                                  ;@line 1036
						Cast ::temp132 ::temp133                                 ;@line 1036
					_label67:
						Cast ::temp132 ::temp132                                 ;@line 1036
						JumpT ::temp132 _label68                                 ;@line 1036
						CompareLT ::temp133 now nextShotAt                       ;@line 1036
						Cast ::temp132 ::temp133                                 ;@line 1036
					_label68:
						JumpF ::temp132 _label69                                 ;@line 1036
						Return None                                              ;@line 1037
						Jump _label69                                            ;@line 1037
					_label69:
						Assign phase 1                                           ;@line 1039
						Assign phaseAt now                                       ;@line 1040
						Assign shotTarget target                                 ;@line 1041
						CallMethod SafeCadenceSeconds self ::temp134             ;@line 1042
						Assign cadence ::temp134                                 ;@line 1042
						FAdd ::temp134 now cadence                               ;@line 1043
						Assign nextShotAt ::temp134                              ;@line 1043
						CallMethod PlaySceneAnimation self ::temp133 "Fire" expectedGeneration expectedToken  ;@line 1044
						Assign started ::temp133                                 ;@line 1044
						CallMethod Current self ::temp132 expectedGeneration expectedToken  ;@line 1045
						Not ::temp133 ::temp132                                  ;@line 1045
						Cast ::temp133 ::temp133                                 ;@line 1045
						JumpT ::temp133 _label70                                 ;@line 1045
						CompareEQ ::temp132 phase 1                              ;@line 1045
						Not ::temp132 ::temp132                                  ;@line 1045
						Cast ::temp133 ::temp132                                 ;@line 1045
					_label70:
						Cast ::temp133 ::temp133                                 ;@line 1045
						JumpT ::temp133 _label71                                 ;@line 1045
						CompareEQ ::temp132 shotTarget target                    ;@line 1045
						Not ::temp132 ::temp132                                  ;@line 1045
						Cast ::temp133 ::temp132                                 ;@line 1045
					_label71:
						JumpF ::temp133 _label72                                 ;@line 1045
						Return None                                              ;@line 1046
						Jump _label72                                            ;@line 1046
					_label72:
						Not ::temp132 started                                    ;@line 1048
						JumpF ::temp132 _label73                                 ;@line 1048
						CallMethod AbortShot self ::NoneVar expectedGeneration expectedToken  ;@line 1049
						Jump _label73                                            ;@line 1049
					_label73:
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
						.local ::temp141 Bool
						.local ::temp142 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod Current self ::temp141 expectedGeneration expectedToken  ;@line 1113
						Not ::temp141 ::temp141                                  ;@line 1113
						Cast ::temp141 ::temp141                                 ;@line 1113
						JumpT ::temp141 _label74                                 ;@line 1113
						CompareEQ ::temp142 phase 0                              ;@line 1113
						Cast ::temp141 ::temp142                                 ;@line 1113
					_label74:
						JumpF ::temp141 _label75                                 ;@line 1113
						Return None                                              ;@line 1114
						Jump _label75                                            ;@line 1114
					_label75:
						CallMethod StartReset self ::NoneVar expectedGeneration expectedToken  ;@line 1116
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
						.local ::temp135 Bool
						.local ::temp136 Bool
						.local ::temp137 Float
						.local ::temp138 ObjectReference
						.local ::temp139 sound
						.local now Float
						.local safe Bool
						.local ::NoneVar None
						.local cadence Float
						.local launchCurrent Bool
						.local launchedAt Float
						.local ::temp140 Int
					.endLocalTable
					.code
						Cast ::temp135 sceneBusy                                 ;@line 1054
						JumpT ::temp135 _label76                                 ;@line 1054
						CallMethod Current self ::temp135 expectedGeneration expectedToken  ;@line 1054
						Not ::temp135 ::temp135                                  ;@line 1054
						Cast ::temp135 ::temp135                                 ;@line 1054
					_label76:
						Cast ::temp135 ::temp135                                 ;@line 1054
						JumpT ::temp135 _label77                                 ;@line 1054
						CompareEQ ::temp136 phase 1                              ;@line 1054
						Not ::temp136 ::temp136                                  ;@line 1054
						Cast ::temp135 ::temp136                                 ;@line 1054
					_label77:
						Cast ::temp135 ::temp135                                 ;@line 1054
						JumpT ::temp135 _label78                                 ;@line 1054
						CompareEQ ::temp136 shotTarget target                    ;@line 1054
						Not ::temp136 ::temp136                                  ;@line 1054
						Cast ::temp135 ::temp136                                 ;@line 1054
					_label78:
						JumpF ::temp135 _label79                                 ;@line 1054
						Return None                                              ;@line 1055
						Jump _label79                                            ;@line 1055
					_label79:
						CallStatic utility GetCurrentRealTime ::temp137          ;@line 1057
						Assign now ::temp137                                     ;@line 1057
						CallMethod ShotPreflight self ::temp136 target expectedGeneration expectedToken  ;@line 1060
						Assign safe ::temp136                                    ;@line 1060
						CallMethod Current self ::temp135 expectedGeneration expectedToken  ;@line 1061
						Not ::temp136 ::temp135                                  ;@line 1061
						Cast ::temp136 ::temp136                                 ;@line 1061
						JumpT ::temp136 _label80                                 ;@line 1061
						CompareEQ ::temp135 phase 1                              ;@line 1061
						Not ::temp135 ::temp135                                  ;@line 1061
						Cast ::temp136 ::temp135                                 ;@line 1061
					_label80:
						Cast ::temp136 ::temp136                                 ;@line 1061
						JumpT ::temp136 _label81                                 ;@line 1061
						CompareEQ ::temp135 shotTarget target                    ;@line 1061
						Not ::temp135 ::temp135                                  ;@line 1061
						Cast ::temp136 ::temp135                                 ;@line 1061
					_label81:
						JumpF ::temp136 _label82                                 ;@line 1061
						Return None                                              ;@line 1062
						Jump _label82                                            ;@line 1062
					_label82:
						Not ::temp135 safe                                       ;@line 1064
						Cast ::temp135 ::temp135                                 ;@line 1064
						JumpT ::temp135 _label83                                 ;@line 1064
						CallMethod Finite self ::temp136 now 0.000000 1000000000.000000  ;@line 1064
						Not ::temp136 ::temp136                                  ;@line 1064
						Cast ::temp135 ::temp136                                 ;@line 1064
					_label83:
						JumpF ::temp135 _label84                                 ;@line 1064
						CallMethod AbortShot self ::NoneVar expectedGeneration expectedToken  ;@line 1065
						Return None                                              ;@line 1066
						Jump _label84                                            ;@line 1066
					_label84:
						CallMethod SafeCadenceSeconds self ::temp137             ;@line 1068
						Assign cadence ::temp137                                 ;@line 1068
						FAdd ::temp137 now cadence                               ;@line 1069
						CompareLT ::temp136 nextShotAt ::temp137                 ;@line 1069
						JumpF ::temp136 _label85                                 ;@line 1069
						FAdd ::temp137 now cadence                               ;@line 1070
						Assign nextShotAt ::temp137                              ;@line 1070
						Jump _label85                                            ;@line 1070
					_label85:
						Assign phase 2                                           ;@line 1074
						Assign phaseAt now                                       ;@line 1075
						CallMethod Current self ::temp135 expectedGeneration expectedToken  ;@line 1076
						Not ::temp136 ::temp135                                  ;@line 1076
						Cast ::temp136 ::temp136                                 ;@line 1076
						JumpT ::temp136 _label86                                 ;@line 1076
						CompareEQ ::temp135 phase 2                              ;@line 1076
						Not ::temp135 ::temp135                                  ;@line 1076
						Cast ::temp136 ::temp135                                 ;@line 1076
					_label86:
						Cast ::temp136 ::temp136                                 ;@line 1076
						JumpT ::temp136 _label87                                 ;@line 1076
						CompareEQ ::temp135 shotTarget target                    ;@line 1076
						Not ::temp135 ::temp135                                  ;@line 1076
						Cast ::temp136 ::temp135                                 ;@line 1076
					_label87:
						JumpF ::temp136 _label88                                 ;@line 1076
						Return None                                              ;@line 1077
						Jump _label88                                            ;@line 1077
					_label88:
						Assign sceneBusy True                                    ;@line 1082
						Cast ::temp138 self                                      ;@line 1083
						CallMethod Fire ::Launcher_var ::NoneVar ::temp138 ::ShotAmmo_var  ;@line 1083
						CallMethod FinishSceneEffect self ::temp135 expectedGeneration expectedToken  ;@line 1084
						Assign launchCurrent ::temp135                           ;@line 1084
						Not ::temp136 launchCurrent                              ;@line 1085
						Cast ::temp136 ::temp136                                 ;@line 1085
						JumpT ::temp136 _label89                                 ;@line 1085
						CallMethod Current self ::temp135 expectedGeneration expectedToken  ;@line 1085
						Not ::temp135 ::temp135                                  ;@line 1085
						Cast ::temp136 ::temp135                                 ;@line 1085
					_label89:
						Cast ::temp136 ::temp136                                 ;@line 1085
						JumpT ::temp136 _label90                                 ;@line 1085
						CompareEQ ::temp135 phase 2                              ;@line 1085
						Not ::temp135 ::temp135                                  ;@line 1085
						Cast ::temp136 ::temp135                                 ;@line 1085
					_label90:
						JumpF ::temp136 _label91                                 ;@line 1085
						Return None                                              ;@line 1086
						Jump _label91                                            ;@line 1086
					_label91:
						CallStatic utility GetCurrentRealTime ::temp137          ;@line 1090
						Assign launchedAt ::temp137                              ;@line 1090
						CallMethod Current self ::temp135 expectedGeneration expectedToken  ;@line 1091
						Not ::temp136 ::temp135                                  ;@line 1091
						Cast ::temp136 ::temp136                                 ;@line 1091
						JumpT ::temp136 _label92                                 ;@line 1091
						CompareEQ ::temp135 phase 2                              ;@line 1091
						Not ::temp135 ::temp135                                  ;@line 1091
						Cast ::temp136 ::temp135                                 ;@line 1091
					_label92:
						JumpF ::temp136 _label93                                 ;@line 1091
						Return None                                              ;@line 1092
						Jump _label93                                            ;@line 1092
					_label93:
						CallMethod Finite self ::temp135 launchedAt 0.000000 1000000000.000000  ;@line 1094
						Not ::temp136 ::temp135                                  ;@line 1094
						JumpF ::temp136 _label94                                 ;@line 1094
						Assign faulted True                                      ;@line 1095
						CallMethod Shutdown self ::NoneVar                       ;@line 1096
						Return None                                              ;@line 1097
						Jump _label94                                            ;@line 1097
					_label94:
						Assign phaseAt launchedAt                                ;@line 1099
						FAdd ::temp137 launchedAt cadence                        ;@line 1100
						CompareLT ::temp135 nextShotAt ::temp137                 ;@line 1100
						JumpF ::temp135 _label95                                 ;@line 1100
						FAdd ::temp137 launchedAt cadence                        ;@line 1101
						Assign nextShotAt ::temp137                              ;@line 1101
						Jump _label95                                            ;@line 1101
					_label95:
						CallMethod SetVisualBolt self ::NoneVar 0.000000 expectedGeneration expectedToken  ;@line 1103
						CallMethod Current self ::temp136 expectedGeneration expectedToken  ;@line 1104
						Not ::temp135 ::temp136                                  ;@line 1104
						Cast ::temp135 ::temp135                                 ;@line 1104
						JumpT ::temp135 _label96                                 ;@line 1104
						CompareEQ ::temp136 phase 2                              ;@line 1104
						Not ::temp136 ::temp136                                  ;@line 1104
						Cast ::temp135 ::temp136                                 ;@line 1104
					_label96:
						JumpF ::temp135 _label97                                 ;@line 1104
						Return None                                              ;@line 1105
						Jump _label97                                            ;@line 1105
					_label97:
						Cast ::temp139 None                                      ;@line 1107
						CompareEQ ::temp136 ::ShotSound_var ::temp139            ;@line 1107
						Not ::temp136 ::temp136                                  ;@line 1107
						JumpF ::temp136 _label98                                 ;@line 1107
						Cast ::temp138 self                                      ;@line 1108
						CallMethod Play ::ShotSound_var ::temp140 ::temp138      ;@line 1108
						Jump _label98                                            ;@line 1108
					_label98:
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
						Cast ::temp61 sceneBusy                                  ;@line 641
						JumpT ::temp61 _label99                                  ;@line 641
						CallMethod Current self ::temp61 expectedGeneration expectedToken  ;@line 641
						Not ::temp61 ::temp61                                    ;@line 641
						Cast ::temp61 ::temp61                                   ;@line 641
					_label99:
						JumpF ::temp61 _label100                                 ;@line 641
						Return False                                             ;@line 642
						Jump _label100                                           ;@line 642
					_label100:
						Assign sceneBusy True                                    ;@line 644
						CallMethod PlayGamebryoAnimation self ::temp61 name True 0.000000  ;@line 645
						Assign started ::temp61                                  ;@line 645
						CallMethod FinishSceneEffect self ::temp61 expectedGeneration expectedToken  ;@line 646
						Assign valid ::temp61                                    ;@line 646
						Cast ::temp61 valid                                      ;@line 647
						JumpF ::temp61 _label101                                 ;@line 647
						Cast ::temp61 started                                    ;@line 647
					_label101:
						Return ::temp61                                          ;@line 647
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
						Cast ::temp62 sceneBusy                                  ;@line 651
						JumpT ::temp62 _label102                                 ;@line 651
						CallMethod Current self ::temp62 expectedGeneration expectedToken  ;@line 651
						Not ::temp62 ::temp62                                    ;@line 651
						Cast ::temp62 ::temp62                                   ;@line 651
					_label102:
						JumpF ::temp62 _label103                                 ;@line 651
						Return None                                              ;@line 652
						Jump _label103                                           ;@line 652
					_label103:
						Assign sceneBusy True                                    ;@line 654
						Cast ::temp63 self                                       ;@line 655
						CallStatic netimmerse SetNodeScale ::NoneVar ::temp63 ::VisualBoltNode_var scale False  ;@line 655
						CallMethod FinishSceneEffect self ::temp62 expectedGeneration expectedToken  ;@line 656
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
						Not ::temp10 ::AllowPlayerTakeover_var                   ;@line 141
						JumpF ::temp10 _label104                                 ;@line 141
						Return True                                              ;@line 142
						Jump _label104                                           ;@line 142
					_label104:
						CallStatic skse GetPluginVersion ::temp11 "AstraSight"   ;@line 147
						CompareLT ::temp10 ::temp11 50659328                     ;@line 147
						JumpF ::temp10 _label105                                 ;@line 147
						Return True                                              ;@line 148
						Jump _label105                                           ;@line 148
					_label105:
						Cast ::temp12 self                                       ;@line 152
						CallStatic astrasightnative IsEffectsQuiescent ::temp10 ::temp12 0  ;@line 152
						Return ::temp10                                          ;@line 152
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
						Cast ::temp8 ::AllowPlayerTakeover_var                   ;@line 137
						JumpF ::temp8 _label106                                  ;@line 137
						Not ::temp8 stationRetired                               ;@line 137
						Cast ::temp8 ::temp8                                     ;@line 137
					_label106:
						Cast ::temp8 ::temp8                                     ;@line 137
						JumpF ::temp8 _label107                                  ;@line 137
						Not ::temp9 destroyed                                    ;@line 137
						Cast ::temp8 ::temp9                                     ;@line 137
					_label107:
						Cast ::temp9 ::temp8                                     ;@line 137
						JumpF ::temp9 _label108                                  ;@line 137
						Cast ::temp9 playerReserved                              ;@line 137
					_label108:
						Cast ::temp9 ::temp9                                     ;@line 137
						JumpF ::temp9 _label109                                  ;@line 137
						CompareGT ::temp8 lease 0                                ;@line 137
						Cast ::temp9 ::temp8                                     ;@line 137
					_label109:
						Cast ::temp9 ::temp9                                     ;@line 137
						JumpF ::temp9 _label110                                  ;@line 137
						CompareEQ ::temp8 playerLease lease                      ;@line 137
						Cast ::temp9 ::temp8                                     ;@line 137
					_label110:
						Return ::temp9                                           ;@line 137
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
						.local ::temp145 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod Current self ::temp145 expectedGeneration expectedToken  ;@line 1137
						Not ::temp145 ::temp145                                  ;@line 1137
						JumpF ::temp145 _label111                                ;@line 1137
						Return None                                              ;@line 1138
						Jump _label111                                           ;@line 1138
					_label111:
						Assign updating False                                    ;@line 1140
						CallMethod RegisterForSingleUpdate self ::NoneVar delay  ;@line 1141
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
						CallMethod StationSceneAvailable self ::temp56           ;@line 609
						Not ::temp56 ::temp56                                    ;@line 609
						JumpF ::temp56 _label112                                 ;@line 609
						Return None                                              ;@line 610
						Jump _label112                                           ;@line 610
					_label112:
						CallMethod Is3DLoaded self ::temp56                      ;@line 615
						Assign loaded ::temp56                                   ;@line 615
						JumpF loaded _label113                                   ;@line 616
						JumpF ::AllowPlayerTakeover_var _label114                ;@line 617
						CallStatic skse GetPluginVersion ::temp57 "AstraSight"   ;@line 620
						CompareGTE ::temp56 ::temp57 50659392                    ;@line 620
						JumpF ::temp56 _label115                                 ;@line 620
						Cast ::temp58 self                                       ;@line 621
						CallStatic astrasightnative ResetIdleScene ::temp59 ::temp58  ;@line 621
						Jump _label115                                           ;@line 621
					_label115:
						Jump _label116                                           ;@line 621
					_label114:
						CallMethod PlayGamebryoAnimation self ::temp59 "Reset" True 0.000000  ;@line 624
					_label116:
						Cast ::temp58 self                                       ;@line 626
						CallStatic netimmerse SetNodeScale ::NoneVar ::temp58 ::VisualBoltNode_var 1.000000 False  ;@line 626
						Jump _label113                                           ;@line 626
					_label113:
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
						CallMethod Finite self ::temp33 ::CadenceSeconds_var 2.500000 60.000000  ;@line 319
						Not ::temp33 ::temp33                                    ;@line 319
						JumpF ::temp33 _label117                                 ;@line 319
						Return 2.500000                                          ;@line 320
						Jump _label117                                           ;@line 320
					_label117:
						Return ::CadenceSeconds_var                              ;@line 322
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
						Assign playerReserved False                              ;@line 127
						Assign playerReady False                                 ;@line 128
						Assign playerRestored False                              ;@line 129
						Assign playerLease 0                                     ;@line 130
						CompareLT ::temp6 playerSerial 2000000000                ;@line 131
						JumpF ::temp6 _label118                                  ;@line 131
						IAdd ::temp7 playerSerial 1                              ;@line 132
						Assign playerSerial ::temp7                              ;@line 132
						Jump _label118                                           ;@line 132
					_label118:
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
						CallMethod Current self ::temp60 expectedGeneration expectedToken  ;@line 631
						Assign valid ::temp60                                    ;@line 631
						Not ::temp60 valid                                       ;@line 632
						JumpF ::temp60 _label119                                 ;@line 632
						CallMethod RestoreNeutralScene self ::NoneVar            ;@line 633
						Jump _label119                                           ;@line 633
					_label119:
						Assign sceneBusy False                                   ;@line 635
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 636
						Return valid                                             ;@line 637
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
						Not ::temp3 stationRetired                               ;@line 113
						JumpF ::temp3 _label120                                  ;@line 113
						Assign stationRetired True                               ;@line 114
						CallMethod InvalidatePlayerLease self ::NoneVar          ;@line 115
						CallMethod Shutdown self ::NoneVar                       ;@line 116
						Jump _label120                                           ;@line 116
					_label120:
						Cast ::temp3 pinBusy                                     ;@line 118
						JumpT ::temp3 _label121                                  ;@line 118
						Cast ::temp3 sceneBusy                                   ;@line 118
					_label121:
						JumpF ::temp3 _label122                                  ;@line 118
						Return False                                             ;@line 119
						Jump _label122                                           ;@line 119
					_label122:
						CallMethod ReleaseOwnedGuard self ::NoneVar              ;@line 121
						Not ::temp3 pinBusy                                      ;@line 122
						Cast ::temp3 ::temp3                                     ;@line 122
						JumpF ::temp3 _label123                                  ;@line 122
						Not ::temp4 sceneBusy                                    ;@line 122
						Cast ::temp3 ::temp4                                     ;@line 122
					_label123:
						Cast ::temp3 ::temp3                                     ;@line 122
						JumpF ::temp3 _label124                                  ;@line 122
						Cast ::temp5 None                                        ;@line 122
						CompareEQ ::temp4 ownedGuard ::temp5                     ;@line 122
						Cast ::temp3 ::temp4                                     ;@line 122
					_label124:
						Return ::temp3                                           ;@line 122
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
						.local ::temp143 Float
						.local ::temp144 Bool
						.local now Float
						.local started Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						CallStatic utility GetCurrentRealTime ::temp143          ;@line 1120
						Assign now ::temp143                                     ;@line 1120
						CallMethod Current self ::temp144 expectedGeneration expectedToken  ;@line 1121
						Not ::temp144 ::temp144                                  ;@line 1121
						JumpF ::temp144 _label125                                ;@line 1121
						Return None                                              ;@line 1122
						Jump _label125                                           ;@line 1122
					_label125:
						Assign phase 3                                           ;@line 1124
						Assign phaseAt now                                       ;@line 1125
						CallMethod PlaySceneAnimation self ::temp144 "Reset" expectedGeneration expectedToken  ;@line 1126
						Assign started ::temp144                                 ;@line 1126
						CallMethod Current self ::temp144 expectedGeneration expectedToken  ;@line 1127
						Not ::temp144 ::temp144                                  ;@line 1127
						JumpF ::temp144 _label126                                ;@line 1127
						Return None                                              ;@line 1128
						Jump _label126                                           ;@line 1128
					_label126:
						Not ::temp144 started                                    ;@line 1130
						JumpF ::temp144 _label127                                ;@line 1130
						Assign faulted True                                      ;@line 1131
						CallMethod Shutdown self ::NoneVar                       ;@line 1132
						Jump _label127                                           ;@line 1132
					_label127:
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
					.endLocalTable
					.code
						Cast ::temp37 playerReserved                             ;@line 342
						JumpT ::temp37 _label128                                 ;@line 342
						Cast ::temp37 stationRetired                             ;@line 342
					_label128:
						JumpF ::temp37 _label129                                 ;@line 342
						Return None                                              ;@line 343
						Jump _label129                                           ;@line 343
					_label129:
						Assign probeGeneration generation                        ;@line 345
						CallMethod StationSceneAvailable self ::temp37           ;@line 346
						Assign sceneFree ::temp37                                ;@line 346
						CompareEQ ::temp37 generation probeGeneration            ;@line 347
						Not ::temp37 ::temp37                                    ;@line 347
						Cast ::temp37 ::temp37                                   ;@line 347
						JumpT ::temp37 _label130                                 ;@line 347
						Cast ::temp37 playerReserved                             ;@line 347
					_label130:
						JumpF ::temp37 _label131                                 ;@line 347
						Return None                                              ;@line 348
						Jump _label131                                           ;@line 348
					_label131:
						Not ::temp37 sceneFree                                   ;@line 350
						JumpF ::temp37 _label132                                 ;@line 350
						Assign running False                                     ;@line 351
						IAdd ::temp38 generation 1                               ;@line 352
						Assign generation ::temp38                               ;@line 352
						Assign deferredGeneration generation                     ;@line 353
						Assign token -1                                          ;@line 354
						Assign recovering False                                  ;@line 355
						Assign updating False                                    ;@line 356
						Assign phase 0                                           ;@line 357
						Cast ::temp39 None                                       ;@line 358
						Assign shotTarget ::temp39                               ;@line 358
						Assign matricesReady False                               ;@line 359
						Assign recoveryRequested True                            ;@line 360
						CallMethod Is3DLoaded self ::temp40                      ;@line 361
						Assign loaded ::temp40                                   ;@line 361
						Cast ::temp40 loaded                                     ;@line 362
						JumpF ::temp40 _label133                                 ;@line 362
						CompareEQ ::temp40 generation deferredGeneration         ;@line 362
						Cast ::temp40 ::temp40                                   ;@line 362
					_label133:
						Cast ::temp40 ::temp40                                   ;@line 362
						JumpF ::temp40 _label134                                 ;@line 362
						Not ::temp41 playerReserved                              ;@line 362
						Cast ::temp40 ::temp41                                   ;@line 362
					_label134:
						Cast ::temp40 ::temp40                                   ;@line 362
						JumpF ::temp40 _label135                                 ;@line 362
						Not ::temp41 pinBusy                                     ;@line 362
						Cast ::temp40 ::temp41                                   ;@line 362
					_label135:
						Cast ::temp40 ::temp40                                   ;@line 362
						JumpF ::temp40 _label136                                 ;@line 362
						Not ::temp41 sceneBusy                                   ;@line 362
						Cast ::temp40 ::temp41                                   ;@line 362
					_label136:
						JumpF ::temp40 _label137                                 ;@line 362
						CallMethod RegisterForSingleUpdate self ::NoneVar 0.200000  ;@line 363
						Jump _label137                                           ;@line 363
					_label137:
						Return None                                              ;@line 365
						Jump _label132                                           ;@line 365
					_label132:
						Assign running False                                     ;@line 367
						IAdd ::temp38 generation 1                               ;@line 368
						Assign generation ::temp38                               ;@line 368
						Assign recoveryGeneration generation                     ;@line 369
						Assign token -1                                          ;@line 370
						IAdd ::temp38 serial 1                                   ;@line 371
						Assign serial ::temp38                                   ;@line 371
						Assign recovering True                                   ;@line 372
						Assign updating False                                    ;@line 373
						Assign phase 0                                           ;@line 374
						Cast ::temp39 None                                       ;@line 375
						Assign shotTarget ::temp39                               ;@line 375
						Assign faulted False                                     ;@line 376
						Assign matricesReady False                               ;@line 377
						Assign recoveryRequested False                           ;@line 378
						CallMethod NormalizeTimingProperties self ::NoneVar      ;@line 380
						Cast ::temp41 pinBusy                                    ;@line 381
						JumpT ::temp41 _label138                                 ;@line 381
						Cast ::temp41 sceneBusy                                  ;@line 381
					_label138:
						JumpF ::temp41 _label139                                 ;@line 381
						Assign recoveryRequested True                            ;@line 384
						Assign recovering False                                  ;@line 385
						Return None                                              ;@line 386
						Jump _label139                                           ;@line 386
					_label139:
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 388
						CompareEQ ::temp40 generation recoveryGeneration         ;@line 389
						Not ::temp40 ::temp40                                    ;@line 389
						Cast ::temp41 ::temp40                                   ;@line 389
						JumpT ::temp41 _label140                                 ;@line 389
						CompareEQ ::temp37 token -1                              ;@line 389
						Not ::temp37 ::temp37                                    ;@line 389
						Cast ::temp41 ::temp37                                   ;@line 389
					_label140:
						JumpF ::temp41 _label141                                 ;@line 389
						Return None                                              ;@line 390
						Jump _label141                                           ;@line 390
					_label141:
						CallMethod ReleaseOwnedGuard self ::NoneVar              ;@line 392
						CompareEQ ::temp40 generation recoveryGeneration         ;@line 393
						Not ::temp40 ::temp40                                    ;@line 393
						Cast ::temp41 ::temp40                                   ;@line 393
						JumpT ::temp41 _label142                                 ;@line 393
						CompareEQ ::temp37 token -1                              ;@line 393
						Not ::temp37 ::temp37                                    ;@line 393
						Cast ::temp41 ::temp37                                   ;@line 393
					_label142:
						JumpF ::temp41 _label143                                 ;@line 393
						Return None                                              ;@line 394
						Jump _label143                                           ;@line 394
					_label143:
						CallStatic game GetPlayer ::temp39                       ;@line 396
						Assign player ::temp39                                   ;@line 396
						CompareEQ ::temp40 generation recoveryGeneration         ;@line 397
						Not ::temp40 ::temp40                                    ;@line 397
						Cast ::temp41 ::temp40                                   ;@line 397
						JumpT ::temp41 _label144                                 ;@line 397
						CompareEQ ::temp37 token -1                              ;@line 397
						Not ::temp37 ::temp37                                    ;@line 397
						Cast ::temp41 ::temp37                                   ;@line 397
					_label144:
						JumpF ::temp41 _label145                                 ;@line 397
						Return None                                              ;@line 398
						Jump _label145                                           ;@line 398
					_label145:
						CallMethod BlockActivation self ::NoneVar True           ;@line 400
						CompareEQ ::temp40 generation recoveryGeneration         ;@line 401
						Not ::temp40 ::temp40                                    ;@line 401
						Cast ::temp41 ::temp40                                   ;@line 401
						JumpT ::temp41 _label146                                 ;@line 401
						CompareEQ ::temp37 token -1                              ;@line 401
						Not ::temp37 ::temp37                                    ;@line 401
						Cast ::temp41 ::temp37                                   ;@line 401
					_label146:
						JumpF ::temp41 _label147                                 ;@line 401
						Return None                                              ;@line 402
						Jump _label147                                           ;@line 402
					_label147:
						Cast ::temp37 destroyed                                  ;@line 404
						JumpT ::temp37 _label148                                 ;@line 404
						Cast ::temp39 None                                       ;@line 404
						CompareEQ ::temp40 ::Artillero_var ::temp39              ;@line 404
						Cast ::temp37 ::temp40                                   ;@line 404
					_label148:
						Cast ::temp40 ::temp37                                   ;@line 404
						JumpT ::temp40 _label149                                 ;@line 404
						CompareEQ ::temp41 ::Artillero_var player                ;@line 404
						Cast ::temp40 ::temp41                                   ;@line 404
					_label149:
						Cast ::temp41 ::temp40                                   ;@line 404
						JumpT ::temp41 _label150                                 ;@line 404
						Cast ::temp42 None                                       ;@line 404
						CompareEQ ::temp37 ::Puesto_var ::temp42                 ;@line 404
						Cast ::temp41 ::temp37                                   ;@line 404
					_label150:
						Cast ::temp37 ::temp41                                   ;@line 404
						JumpT ::temp37 _label151                                 ;@line 404
						Cast ::temp43 None                                       ;@line 404
						CompareEQ ::temp40 ::Launcher_var ::temp43               ;@line 404
						Cast ::temp37 ::temp40                                   ;@line 404
					_label151:
						Cast ::temp40 ::temp37                                   ;@line 404
						JumpT ::temp40 _label152                                 ;@line 404
						Cast ::temp44 None                                       ;@line 404
						CompareEQ ::temp41 ::ShotAmmo_var ::temp44               ;@line 404
						Cast ::temp40 ::temp41                                   ;@line 404
					_label152:
						JumpF ::temp40 _label153                                 ;@line 404
						Assign faulted True                                      ;@line 405
						Assign recovering False                                  ;@line 406
						Return None                                              ;@line 407
						Jump _label153                                           ;@line 407
					_label153:
						CallMethod Is3DLoaded self ::temp37                      ;@line 409
						Assign gunLoaded ::temp37                                ;@line 409
						CallMethod Is3DLoaded ::Artillero_var ::temp41           ;@line 410
						Assign guardLoaded ::temp41                              ;@line 410
						CallMethod IsDead ::Artillero_var ::temp40               ;@line 411
						Assign guardDead ::temp40                                ;@line 411
						CallMethod IsDisabled ::Artillero_var ::temp37           ;@line 412
						Assign guardDisabled ::temp37                            ;@line 412
						CompareEQ ::temp41 generation recoveryGeneration         ;@line 413
						Not ::temp41 ::temp41                                    ;@line 413
						Cast ::temp37 ::temp41                                   ;@line 413
						JumpT ::temp37 _label154                                 ;@line 413
						CompareEQ ::temp40 token -1                              ;@line 413
						Not ::temp40 ::temp40                                    ;@line 413
						Cast ::temp37 ::temp40                                   ;@line 413
					_label154:
						JumpF ::temp37 _label155                                 ;@line 413
						Return None                                              ;@line 414
						Jump _label155                                           ;@line 414
					_label155:
						Cast ::temp41 guardDead                                  ;@line 416
						JumpT ::temp41 _label156                                 ;@line 416
						Cast ::temp41 guardDisabled                              ;@line 416
					_label156:
						Cast ::temp40 ::temp41                                   ;@line 416
						JumpT ::temp40 _label157                                 ;@line 416
						Cast ::temp40 destroyed                                  ;@line 416
					_label157:
						JumpF ::temp40 _label158                                 ;@line 416
						Assign faulted True                                      ;@line 417
						Assign recovering False                                  ;@line 418
						Return None                                              ;@line 419
						Jump _label158                                           ;@line 419
					_label158:
						Not ::temp37 gunLoaded                                   ;@line 421
						Cast ::temp40 ::temp37                                   ;@line 421
						JumpT ::temp40 _label159                                 ;@line 421
						Not ::temp41 guardLoaded                                 ;@line 421
						Cast ::temp40 ::temp41                                   ;@line 421
					_label159:
						JumpF ::temp40 _label160                                 ;@line 421
						Assign recovering False                                  ;@line 422
						JumpF gunLoaded _label161                                ;@line 423
						CallMethod RegisterForSingleUpdate self ::NoneVar 1.000000  ;@line 424
						Jump _label161                                           ;@line 424
					_label161:
						Return None                                              ;@line 426
						Jump _label160                                           ;@line 426
					_label160:
						CallMethod EnsureCityPlacement self ::temp37 recoveryGeneration 0  ;@line 428
						Assign placed ::temp37                                   ;@line 428
						CompareEQ ::temp41 generation recoveryGeneration         ;@line 429
						Not ::temp41 ::temp41                                    ;@line 429
						Cast ::temp37 ::temp41                                   ;@line 429
						JumpT ::temp37 _label162                                 ;@line 429
						CompareEQ ::temp40 token -1                              ;@line 429
						Not ::temp40 ::temp40                                    ;@line 429
						Cast ::temp37 ::temp40                                   ;@line 429
					_label162:
						JumpF ::temp37 _label163                                 ;@line 429
						Return None                                              ;@line 430
						Jump _label163                                           ;@line 430
					_label163:
						Not ::temp41 placed                                      ;@line 432
						JumpF ::temp41 _label164                                 ;@line 432
						Assign recovering False                                  ;@line 433
						Assign recoveryRequested True                            ;@line 434
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 435
						Return None                                              ;@line 436
						Jump _label164                                           ;@line 436
					_label164:
						CallMethod CaptureMatrices self ::temp40                 ;@line 438
						Assign captured ::temp40                                 ;@line 438
						CompareEQ ::temp37 generation recoveryGeneration         ;@line 439
						Not ::temp37 ::temp37                                    ;@line 439
						Cast ::temp40 ::temp37                                   ;@line 439
						JumpT ::temp40 _label165                                 ;@line 439
						CompareEQ ::temp41 token -1                              ;@line 439
						Not ::temp41 ::temp41                                    ;@line 439
						Cast ::temp40 ::temp41                                   ;@line 439
					_label165:
						JumpF ::temp40 _label166                                 ;@line 439
						Return None                                              ;@line 440
						Jump _label166                                           ;@line 440
					_label166:
						Not ::temp37 captured                                    ;@line 442
						JumpF ::temp37 _label167                                 ;@line 442
						Assign faulted True                                      ;@line 443
						Assign recovering False                                  ;@line 444
						CallStatic debug Trace ::NoneVar "AstraAsedioGuard: missing or invalid model controls; controller stopped." 0  ;@line 445
						Return None                                              ;@line 446
						Jump _label167                                           ;@line 446
					_label167:
						CallMethod GetDistance ::Artillero_var ::temp45 ::Puesto_var  ;@line 448
						Assign distance ::temp45                                 ;@line 448
						CompareEQ ::temp41 generation recoveryGeneration         ;@line 449
						Not ::temp41 ::temp41                                    ;@line 449
						Cast ::temp37 ::temp41                                   ;@line 449
						JumpT ::temp37 _label168                                 ;@line 449
						CompareEQ ::temp40 token -1                              ;@line 449
						Not ::temp40 ::temp40                                    ;@line 449
						Cast ::temp37 ::temp40                                   ;@line 449
					_label168:
						JumpF ::temp37 _label169                                 ;@line 449
						Return None                                              ;@line 450
						Jump _label169                                           ;@line 450
					_label169:
						CallMethod Finite self ::temp41 distance 0.000000 1000000.000000  ;@line 452
						Not ::temp40 ::temp41                                    ;@line 452
						JumpF ::temp40 _label170                                 ;@line 452
						Assign faulted True                                      ;@line 453
						Assign recovering False                                  ;@line 454
						Return None                                              ;@line 455
						Jump _label170                                           ;@line 455
					_label170:
						CompareGT ::temp37 distance 64.000000                    ;@line 457
						JumpF ::temp37 _label171                                 ;@line 457
						Assign movingGuard ::Artillero_var                       ;@line 461
						Assign recoveryPoint ::Puesto_var                        ;@line 462
						Assign pinBusy True                                      ;@line 463
						CallMethod MoveTo movingGuard ::NoneVar recoveryPoint 0.000000 0.000000 0.000000 True  ;@line 464
						CompareEQ ::temp41 generation recoveryGeneration         ;@line 465
						Cast ::temp41 ::temp41                                   ;@line 465
						JumpF ::temp41 _label172                                 ;@line 465
						CompareEQ ::temp40 token -1                              ;@line 465
						Cast ::temp41 ::temp40                                   ;@line 465
					_label172:
						Cast ::temp40 ::temp41                                   ;@line 465
						JumpF ::temp40 _label173                                 ;@line 465
						Cast ::temp40 recovering                                 ;@line 465
					_label173:
						Cast ::temp40 ::temp40                                   ;@line 465
						JumpF ::temp40 _label174                                 ;@line 465
						Not ::temp41 playerReserved                              ;@line 465
						Cast ::temp40 ::temp41                                   ;@line 465
					_label174:
						Cast ::temp40 ::temp40                                   ;@line 465
						JumpF ::temp40 _label175                                 ;@line 465
						Not ::temp41 destroyed                                   ;@line 465
						Cast ::temp40 ::temp41                                   ;@line 465
					_label175:
						Cast ::temp40 ::temp40                                   ;@line 465
						JumpF ::temp40 _label176                                 ;@line 465
						Not ::temp41 faulted                                     ;@line 465
						Cast ::temp40 ::temp41                                   ;@line 465
					_label176:
						Assign moveCurrent ::temp40                              ;@line 465
						Assign pinBusy False                                     ;@line 466
						Not ::temp41 moveCurrent                                 ;@line 467
						JumpF ::temp41 _label177                                 ;@line 467
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 468
						Return None                                              ;@line 469
						Jump _label177                                           ;@line 469
					_label177:
						Jump _label171                                           ;@line 469
					_label171:
						CallMethod IsDead ::Artillero_var ::temp40               ;@line 472
						Not ::temp41 ::temp40                                    ;@line 472
						Cast ::temp37 ::temp41                                   ;@line 472
						JumpF ::temp37 _label178                                 ;@line 472
						CallMethod IsDisabled ::Artillero_var ::temp37           ;@line 472
						Not ::temp40 ::temp37                                    ;@line 472
						Cast ::temp37 ::temp40                                   ;@line 472
					_label178:
						Cast ::temp40 ::temp37                                   ;@line 472
						JumpF ::temp40 _label179                                 ;@line 472
						CallMethod Is3DLoaded ::Artillero_var ::temp41           ;@line 472
						Cast ::temp40 ::temp41                                   ;@line 472
					_label179:
						Assign aliveAfterMove ::temp40                           ;@line 472
						CompareEQ ::temp37 generation recoveryGeneration         ;@line 473
						Not ::temp37 ::temp37                                    ;@line 473
						Cast ::temp40 ::temp37                                   ;@line 473
						JumpT ::temp40 _label180                                 ;@line 473
						CompareEQ ::temp41 token -1                              ;@line 473
						Not ::temp41 ::temp41                                    ;@line 473
						Cast ::temp40 ::temp41                                   ;@line 473
					_label180:
						JumpF ::temp40 _label181                                 ;@line 473
						Return None                                              ;@line 474
						Jump _label181                                           ;@line 474
					_label181:
						Not ::temp37 aliveAfterMove                              ;@line 476
						JumpF ::temp37 _label182                                 ;@line 476
						Assign faulted True                                      ;@line 477
						Assign recovering False                                  ;@line 478
						Return None                                              ;@line 479
						Jump _label182                                           ;@line 479
					_label182:
						CallMethod AcquirePin self ::temp41 recoveryGeneration   ;@line 481
						Assign pinAcquired ::temp41                              ;@line 481
						CompareEQ ::temp40 generation recoveryGeneration         ;@line 482
						Not ::temp40 ::temp40                                    ;@line 482
						Cast ::temp41 ::temp40                                   ;@line 482
						JumpT ::temp41 _label183                                 ;@line 482
						CompareEQ ::temp37 token -1                              ;@line 482
						Not ::temp37 ::temp37                                    ;@line 482
						Cast ::temp41 ::temp37                                   ;@line 482
					_label183:
						JumpF ::temp41 _label184                                 ;@line 482
						Return None                                              ;@line 483
						Jump _label184                                           ;@line 483
					_label184:
						Not ::temp40 pinAcquired                                 ;@line 485
						JumpF ::temp40 _label185                                 ;@line 485
						Assign faulted True                                      ;@line 486
						Assign recovering False                                  ;@line 487
						Return None                                              ;@line 488
						Jump _label185                                           ;@line 488
					_label185:
						Assign yaw 0.000000                                      ;@line 490
						Assign pitch 0.000000                                    ;@line 491
						Assign token serial                                      ;@line 492
						Assign running True                                      ;@line 493
						Assign recovering False                                  ;@line 494
						Assign recoveryToken token                               ;@line 495
						CallStatic utility GetCurrentRealTime ::temp45           ;@line 496
						Assign now ::temp45                                      ;@line 496
						CallMethod Current self ::temp37 recoveryGeneration recoveryToken  ;@line 497
						Not ::temp41 ::temp37                                    ;@line 497
						JumpF ::temp41 _label186                                 ;@line 497
						Return None                                              ;@line 498
						Jump _label186                                           ;@line 498
					_label186:
						CallMethod Finite self ::temp40 now 0.000000 1000000000.000000  ;@line 500
						Not ::temp37 ::temp40                                    ;@line 500
						JumpF ::temp37 _label187                                 ;@line 500
						Assign faulted True                                      ;@line 501
						CallMethod Shutdown self ::NoneVar                       ;@line 502
						Return None                                              ;@line 503
						Jump _label187                                           ;@line 503
					_label187:
						Assign lastTick now                                      ;@line 505
						CallMethod SafeCadenceSeconds self ::temp45              ;@line 506
						FAdd ::temp45 now ::temp45                               ;@line 506
						Assign nextShotAt ::temp45                               ;@line 506
						CallMethod PlaySceneAnimation self ::temp41 "Reset" recoveryGeneration recoveryToken  ;@line 507
						Assign resetStarted ::temp41                             ;@line 507
						CallMethod Current self ::temp40 recoveryGeneration recoveryToken  ;@line 508
						Not ::temp37 ::temp40                                    ;@line 508
						JumpF ::temp37 _label188                                 ;@line 508
						Return None                                              ;@line 509
						Jump _label188                                           ;@line 509
					_label188:
						Not ::temp41 resetStarted                                ;@line 511
						JumpF ::temp41 _label189                                 ;@line 511
						Assign faulted True                                      ;@line 512
						CallMethod Shutdown self ::NoneVar                       ;@line 513
						Return None                                              ;@line 514
						Jump _label189                                           ;@line 514
					_label189:
						CallMethod ApplyAim self ::NoneVar recoveryGeneration recoveryToken  ;@line 516
						CallMethod Current self ::temp40 recoveryGeneration recoveryToken  ;@line 517
						Not ::temp37 ::temp40                                    ;@line 517
						JumpF ::temp37 _label190                                 ;@line 517
						Return None                                              ;@line 518
						Jump _label190                                           ;@line 518
					_label190:
						CallMethod SetVisualBolt self ::NoneVar 1.000000 recoveryGeneration recoveryToken  ;@line 520
						CallMethod Current self ::temp41 recoveryGeneration recoveryToken  ;@line 521
						JumpF ::temp41 _label191                                 ;@line 521
						CallMethod RegisterForSingleUpdate self ::NoneVar 0.200000  ;@line 522
						Jump _label191                                           ;@line 522
					_label191:
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
						Cast ::temp1 running                                     ;@line 109
						JumpF ::temp1 _label192                                  ;@line 109
						Not ::temp1 stationRetired                               ;@line 109
						Cast ::temp1 ::temp1                                     ;@line 109
					_label192:
						Cast ::temp1 ::temp1                                     ;@line 109
						JumpF ::temp1 _label193                                  ;@line 109
						Not ::temp2 playerReserved                               ;@line 109
						Cast ::temp1 ::temp2                                     ;@line 109
					_label193:
						Cast ::temp1 ::temp1                                     ;@line 109
						JumpF ::temp1 _label194                                  ;@line 109
						Not ::temp2 recovering                                   ;@line 109
						Cast ::temp1 ::temp2                                     ;@line 109
					_label194:
						Cast ::temp1 ::temp1                                     ;@line 109
						JumpF ::temp1 _label195                                  ;@line 109
						Not ::temp2 destroyed                                    ;@line 109
						Cast ::temp1 ::temp2                                     ;@line 109
					_label195:
						Cast ::temp1 ::temp1                                     ;@line 109
						JumpF ::temp1 _label196                                  ;@line 109
						Not ::temp2 faulted                                      ;@line 109
						Cast ::temp1 ::temp2                                     ;@line 109
					_label196:
						Cast ::temp1 ::temp1                                     ;@line 109
						JumpF ::temp1 _label197                                  ;@line 109
						CompareEQ ::temp2 generation expectedGeneration          ;@line 109
						Cast ::temp1 ::temp2                                     ;@line 109
					_label197:
						Cast ::temp1 ::temp1                                     ;@line 109
						JumpF ::temp1 _label198                                  ;@line 109
						CompareEQ ::temp2 token expectedToken                    ;@line 109
						Cast ::temp1 ::temp2                                     ;@line 109
					_label198:
						Cast ::temp1 ::temp1                                     ;@line 109
						JumpF ::temp1 _label199                                  ;@line 109
						CompareGT ::temp2 token 0                                ;@line 109
						Cast ::temp1 ::temp2                                     ;@line 109
					_label199:
						Return ::temp1                                           ;@line 109
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
						Assign running False                                     ;@line 527
						IAdd ::temp46 generation 1                               ;@line 528
						Assign generation ::temp46                               ;@line 528
						Assign cleanupGeneration generation                      ;@line 529
						Assign token -1                                          ;@line 530
						Assign recovering False                                  ;@line 531
						Assign updating False                                    ;@line 532
						Assign phase 0                                           ;@line 533
						Cast ::temp47 None                                       ;@line 534
						Assign shotTarget ::temp47                               ;@line 534
						Assign matricesReady False                               ;@line 535
						Assign recoveryRequested False                           ;@line 536
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 537
						CompareEQ ::temp48 generation cleanupGeneration          ;@line 538
						Not ::temp48 ::temp48                                    ;@line 538
						Cast ::temp48 ::temp48                                   ;@line 538
						JumpT ::temp48 _label200                                 ;@line 538
						CompareEQ ::temp49 token -1                              ;@line 538
						Not ::temp49 ::temp49                                    ;@line 538
						Cast ::temp48 ::temp49                                   ;@line 538
					_label200:
						JumpF ::temp48 _label201                                 ;@line 538
						Return None                                              ;@line 539
						Jump _label201                                           ;@line 539
					_label201:
						CallMethod ReleaseOwnedGuard self ::NoneVar              ;@line 543
						CompareEQ ::temp49 generation cleanupGeneration          ;@line 544
						Not ::temp49 ::temp49                                    ;@line 544
						Cast ::temp49 ::temp49                                   ;@line 544
						JumpT ::temp49 _label202                                 ;@line 544
						CompareEQ ::temp48 token -1                              ;@line 544
						Not ::temp48 ::temp48                                    ;@line 544
						Cast ::temp49 ::temp48                                   ;@line 544
					_label202:
						JumpF ::temp49 _label203                                 ;@line 544
						Return None                                              ;@line 545
						Jump _label203                                           ;@line 545
					_label203:
						Not ::temp48 sceneBusy                                   ;@line 547
						JumpF ::temp48 _label204                                 ;@line 547
						Assign sceneBusy True                                    ;@line 548
						CallMethod RestoreNeutralScene self ::NoneVar            ;@line 549
						Assign sceneBusy False                                   ;@line 550
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 551
						Jump _label204                                           ;@line 551
					_label204:
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
						CallMethod BlockActivation self ::NoneVar True           ;@line 105
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
						Assign captureGeneration generation                      ;@line 669
						CallStatic skse GetVersion ::temp66                      ;@line 670
						CompareLT ::temp67 ::temp66 2                            ;@line 670
						Cast ::temp67 ::temp67                                   ;@line 670
						JumpT ::temp67 _label205                                 ;@line 670
						CallMethod Is3DLoaded self ::temp68                      ;@line 670
						Not ::temp68 ::temp68                                    ;@line 670
						Cast ::temp67 ::temp68                                   ;@line 670
					_label205:
						JumpF ::temp67 _label206                                 ;@line 670
						Return False                                             ;@line 671
						Jump _label206                                           ;@line 671
					_label206:
						Cast ::temp69 self                                       ;@line 673
						CallStatic netimmerse HasNode ::temp68 ::temp69 ::YawNode_var False  ;@line 673
						Not ::temp67 ::temp68                                    ;@line 673
						Cast ::temp67 ::temp67                                   ;@line 673
						JumpT ::temp67 _label207                                 ;@line 673
						Cast ::temp69 self                                       ;@line 673
						CallStatic netimmerse HasNode ::temp68 ::temp69 ::PitchNode_var False  ;@line 673
						Not ::temp68 ::temp68                                    ;@line 673
						Cast ::temp67 ::temp68                                   ;@line 673
					_label207:
						Cast ::temp67 ::temp67                                   ;@line 673
						JumpT ::temp67 _label208                                 ;@line 673
						Cast ::temp69 self                                       ;@line 673
						CallStatic netimmerse HasNode ::temp68 ::temp69 ::MuzzleNode_var False  ;@line 673
						Not ::temp68 ::temp68                                    ;@line 673
						Cast ::temp67 ::temp68                                   ;@line 673
					_label208:
						Cast ::temp67 ::temp67                                   ;@line 673
						JumpT ::temp67 _label209                                 ;@line 673
						Cast ::temp69 self                                       ;@line 673
						CallStatic netimmerse HasNode ::temp68 ::temp69 ::VisualBoltNode_var False  ;@line 673
						Not ::temp68 ::temp68                                    ;@line 673
						Cast ::temp67 ::temp68                                   ;@line 673
					_label209:
						JumpF ::temp67 _label210                                 ;@line 673
						Return False                                             ;@line 674
						Jump _label210                                           ;@line 674
					_label210:
						CompareEQ ::temp68 generation captureGeneration          ;@line 676
						Not ::temp68 ::temp68                                    ;@line 676
						Cast ::temp68 ::temp68                                   ;@line 676
						JumpT ::temp68 _label211                                 ;@line 676
						CompareEQ ::temp67 token -1                              ;@line 676
						Not ::temp67 ::temp67                                    ;@line 676
						Cast ::temp68 ::temp67                                   ;@line 676
					_label211:
						Cast ::temp68 ::temp68                                   ;@line 676
						JumpT ::temp68 _label212                                 ;@line 676
						Not ::temp67 recovering                                  ;@line 676
						Cast ::temp68 ::temp67                                   ;@line 676
					_label212:
						JumpF ::temp68 _label213                                 ;@line 676
						Return False                                             ;@line 677
						Jump _label213                                           ;@line 677
					_label213:
						ArrayCreate ::temp70 9                                   ;@line 682
						Assign yawBase ::temp70                                  ;@line 682
						ArrayCreate ::temp70 9                                   ;@line 683
						Assign pitchBase ::temp70                                ;@line 683
						ArrayCreate ::temp70 9                                   ;@line 684
						Assign yawMatrix ::temp70                                ;@line 684
						ArrayCreate ::temp70 9                                   ;@line 685
						Assign pitchMatrix ::temp70                              ;@line 685
						ArrayCreate ::temp70 9                                   ;@line 686
						Assign rootWorldMatrix ::temp70                          ;@line 686
						ArrayCreate ::temp70 9                                   ;@line 687
						Assign muzzleWorldMatrix ::temp70                        ;@line 687
						ArrayCreate ::temp70 3                                   ;@line 688
						Assign rootPosition ::temp70                             ;@line 688
						ArrayCreate ::temp70 3                                   ;@line 689
						Assign muzzlePosition ::temp70                           ;@line 689
						Assign ::temp71 1.000000                                 ;@line 690
						ArraySetElement yawBase 0 ::temp71                       ;@line 690
						Assign ::temp71 1.000000                                 ;@line 691
						ArraySetElement yawBase 4 ::temp71                       ;@line 691
						Assign ::temp71 1.000000                                 ;@line 692
						ArraySetElement yawBase 8 ::temp71                       ;@line 692
						Assign ::temp71 1.000000                                 ;@line 693
						ArraySetElement pitchBase 0 ::temp71                     ;@line 693
						Assign ::temp71 1.000000                                 ;@line 694
						ArraySetElement pitchBase 4 ::temp71                     ;@line 694
						Assign ::temp71 1.000000                                 ;@line 695
						ArraySetElement pitchBase 8 ::temp71                     ;@line 695
						Assign matricesReady True                                ;@line 696
						Return True                                              ;@line 697
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
						CallMethod Current self ::temp72 expectedGeneration expectedToken  ;@line 701
						Not ::temp72 ::temp72                                    ;@line 701
						Cast ::temp72 ::temp72                                   ;@line 701
						JumpT ::temp72 _label214                                 ;@line 701
						Not ::temp73 matricesReady                               ;@line 701
						Cast ::temp72 ::temp73                                   ;@line 701
					_label214:
						JumpF ::temp72 _label215                                 ;@line 701
						Return None                                              ;@line 702
						Jump _label215                                           ;@line 702
					_label215:
						CallStatic math Cos ::temp74 yaw                         ;@line 704
						Assign yc ::temp74                                       ;@line 704
						CallStatic math Sin ::temp74 yaw                         ;@line 705
						Assign ys ::temp74                                       ;@line 705
						FNegate ::temp74 pitch                                   ;@line 706
						CallStatic math Cos ::temp74 ::temp74                    ;@line 706
						Assign pc ::temp74                                       ;@line 706
						FNegate ::temp74 pitch                                   ;@line 707
						CallStatic math Sin ::temp74 ::temp74                    ;@line 707
						Assign ps ::temp74                                       ;@line 707
						CallMethod Current self ::temp73 expectedGeneration expectedToken  ;@line 708
						Not ::temp72 ::temp73                                    ;@line 708
						JumpF ::temp72 _label216                                 ;@line 708
						Return None                                              ;@line 709
						Jump _label216                                           ;@line 709
					_label216:
						Assign j 0                                               ;@line 711
					_label218:
						CompareLT ::temp73 j 3                                   ;@line 712
						JumpF ::temp73 _label217                                 ;@line 712
						ArrayGetElement ::temp75 yawBase j                       ;@line 713
						FMultiply ::temp75 yc ::temp75                           ;@line 713
						IAdd ::temp76 j 3                                        ;@line 713
						ArrayGetElement ::temp77 yawBase ::temp76                ;@line 713
						FMultiply ::temp77 ys ::temp77                           ;@line 713
						FSubtract ::temp75 ::temp75 ::temp77                     ;@line 713
						Assign ::temp74 ::temp75                                 ;@line 713
						ArraySetElement yawMatrix j ::temp74                     ;@line 713
						ArrayGetElement ::temp74 yawBase j                       ;@line 714
						FMultiply ::temp75 ys ::temp74                           ;@line 714
						IAdd ::temp76 j 3                                        ;@line 714
						ArrayGetElement ::temp74 yawBase ::temp76                ;@line 714
						FMultiply ::temp74 yc ::temp74                           ;@line 714
						FAdd ::temp75 ::temp75 ::temp74                          ;@line 714
						Assign ::temp77 ::temp75                                 ;@line 714
						IAdd ::temp76 j 3                                        ;@line 714
						ArraySetElement yawMatrix ::temp76 ::temp77              ;@line 714
						IAdd ::temp76 j 6                                        ;@line 715
						ArrayGetElement ::temp77 yawBase ::temp76                ;@line 715
						Assign ::temp74 ::temp77                                 ;@line 715
						IAdd ::temp76 j 6                                        ;@line 715
						ArraySetElement yawMatrix ::temp76 ::temp74              ;@line 715
						ArrayGetElement ::temp74 pitchBase j                     ;@line 716
						Assign ::temp75 ::temp74                                 ;@line 716
						ArraySetElement pitchMatrix j ::temp75                   ;@line 716
						IAdd ::temp76 j 3                                        ;@line 717
						ArrayGetElement ::temp75 pitchBase ::temp76              ;@line 717
						FMultiply ::temp74 pc ::temp75                           ;@line 717
						IAdd ::temp76 j 6                                        ;@line 717
						ArrayGetElement ::temp75 pitchBase ::temp76              ;@line 717
						FMultiply ::temp75 ps ::temp75                           ;@line 717
						FSubtract ::temp74 ::temp74 ::temp75                     ;@line 717
						Assign ::temp77 ::temp74                                 ;@line 717
						IAdd ::temp76 j 3                                        ;@line 717
						ArraySetElement pitchMatrix ::temp76 ::temp77            ;@line 717
						IAdd ::temp76 j 3                                        ;@line 718
						ArrayGetElement ::temp77 pitchBase ::temp76              ;@line 718
						FMultiply ::temp74 ps ::temp77                           ;@line 718
						IAdd ::temp76 j 6                                        ;@line 718
						ArrayGetElement ::temp77 pitchBase ::temp76              ;@line 718
						FMultiply ::temp77 pc ::temp77                           ;@line 718
						FAdd ::temp74 ::temp74 ::temp77                          ;@line 718
						Assign ::temp75 ::temp74                                 ;@line 718
						IAdd ::temp76 j 6                                        ;@line 718
						ArraySetElement pitchMatrix ::temp76 ::temp75            ;@line 718
						IAdd ::temp76 j 1                                        ;@line 719
						Assign j ::temp76                                        ;@line 719
						Jump _label218                                           ;@line 719
					_label217:
						CallMethod WriteAimNode self ::NoneVar ::YawNode_var yawMatrix expectedGeneration expectedToken  ;@line 723
						CallMethod Current self ::temp72 expectedGeneration expectedToken  ;@line 724
						Not ::temp73 ::temp72                                    ;@line 724
						JumpF ::temp73 _label219                                 ;@line 724
						Return None                                              ;@line 725
						Jump _label219                                           ;@line 725
					_label219:
						CallMethod WriteAimNode self ::NoneVar ::PitchNode_var pitchMatrix expectedGeneration expectedToken  ;@line 727
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
						.local ::NoneVar None
						.local candidate actor
					.endLocalTable
					.code
						Cast ::temp50 pinBusy                                    ;@line 556
						JumpT ::temp50 _label220                                 ;@line 556
						CompareEQ ::temp50 generation expectedGeneration         ;@line 556
						Not ::temp50 ::temp50                                    ;@line 556
						Cast ::temp50 ::temp50                                   ;@line 556
					_label220:
						Cast ::temp50 ::temp50                                   ;@line 556
						JumpT ::temp50 _label221                                 ;@line 556
						CompareEQ ::temp51 token -1                              ;@line 556
						Not ::temp51 ::temp51                                    ;@line 556
						Cast ::temp50 ::temp51                                   ;@line 556
					_label221:
						Cast ::temp50 ::temp50                                   ;@line 556
						JumpT ::temp50 _label222                                 ;@line 556
						Not ::temp51 recovering                                  ;@line 556
						Cast ::temp50 ::temp51                                   ;@line 556
					_label222:
						Cast ::temp51 ::temp50                                   ;@line 556
						JumpT ::temp51 _label223                                 ;@line 556
						Cast ::temp51 destroyed                                  ;@line 556
					_label223:
						Cast ::temp50 ::temp51                                   ;@line 556
						JumpT ::temp50 _label224                                 ;@line 556
						Cast ::temp50 faulted                                    ;@line 556
					_label224:
						JumpF ::temp50 _label225                                 ;@line 556
						Return False                                             ;@line 557
						Jump _label225                                           ;@line 557
					_label225:
						Assign candidate ::Artillero_var                         ;@line 559
						Assign pinBusy True                                      ;@line 560
						CallMethod SetDontMove candidate ::NoneVar True          ;@line 561
						CompareEQ ::temp51 generation expectedGeneration         ;@line 562
						Not ::temp51 ::temp51                                    ;@line 562
						Cast ::temp51 ::temp51                                   ;@line 562
						JumpT ::temp51 _label226                                 ;@line 562
						CompareEQ ::temp50 token -1                              ;@line 562
						Not ::temp50 ::temp50                                    ;@line 562
						Cast ::temp51 ::temp50                                   ;@line 562
					_label226:
						Cast ::temp51 ::temp51                                   ;@line 562
						JumpT ::temp51 _label227                                 ;@line 562
						Not ::temp50 recovering                                  ;@line 562
						Cast ::temp51 ::temp50                                   ;@line 562
					_label227:
						Cast ::temp50 ::temp51                                   ;@line 562
						JumpT ::temp50 _label228                                 ;@line 562
						Cast ::temp50 destroyed                                  ;@line 562
					_label228:
						Cast ::temp51 ::temp50                                   ;@line 562
						JumpT ::temp51 _label229                                 ;@line 562
						Cast ::temp51 faulted                                    ;@line 562
					_label229:
						JumpF ::temp51 _label230                                 ;@line 562
						CallMethod SetDontMove candidate ::NoneVar False         ;@line 566
						Assign pinBusy False                                     ;@line 567
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 568
						Return False                                             ;@line 569
						Jump _label230                                           ;@line 569
					_label230:
						Assign ownedGuard candidate                              ;@line 571
						Assign pinBusy False                                     ;@line 572
						Return True                                              ;@line 573
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
						CallMethod InvalidatePlayerLease self ::NoneVar          ;@line 93
						CallMethod Shutdown self ::NoneVar                       ;@line 94
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
						CompareGT ::temp0 aiCurrentStage 0                       ;@line 98
						JumpF ::temp0 _label231                                  ;@line 98
						Assign destroyed True                                    ;@line 99
						CallMethod Shutdown self ::NoneVar                       ;@line 100
						Jump _label231                                           ;@line 100
					_label231:
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
						.local ::temp128 Bool
						.local ::temp129 Float
						.local ::temp130 Float
						.local ::temp131 Bool
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
						CallMethod SampleTarget self ::temp128 target expectedGeneration expectedToken  ;@line 1007
						Not ::temp128 ::temp128                                  ;@line 1007
						JumpF ::temp128 _label232                                ;@line 1007
						Return False                                             ;@line 1008
						Jump _label232                                           ;@line 1008
					_label232:
						CallStatic math Cos ::temp129 yaw                        ;@line 1011
						Assign yc ::temp129                                      ;@line 1011
						CallStatic math Sin ::temp129 yaw                        ;@line 1012
						Assign ys ::temp129                                      ;@line 1012
						CallStatic math Cos ::temp129 pitch                      ;@line 1013
						Assign pc ::temp129                                      ;@line 1013
						CallStatic math Sin ::temp129 pitch                      ;@line 1014
						Assign ps ::temp129                                      ;@line 1014
						FMultiply ::temp129 ys pc                                ;@line 1015
						Assign lx ::temp129                                      ;@line 1015
						FNegate ::temp129 yc                                     ;@line 1016
						FMultiply ::temp129 ::temp129 pc                         ;@line 1016
						Assign ly ::temp129                                      ;@line 1016
						ArrayGetElement ::temp129 rootWorldMatrix 0              ;@line 1017
						FMultiply ::temp129 ::temp129 lx                         ;@line 1017
						ArrayGetElement ::temp130 rootWorldMatrix 1              ;@line 1017
						FMultiply ::temp130 ::temp130 ly                         ;@line 1017
						FAdd ::temp129 ::temp129 ::temp130                       ;@line 1017
						ArrayGetElement ::temp130 rootWorldMatrix 2              ;@line 1017
						FMultiply ::temp130 ::temp130 ps                         ;@line 1017
						FAdd ::temp129 ::temp129 ::temp130                       ;@line 1017
						Assign wx ::temp129                                      ;@line 1017
						ArrayGetElement ::temp130 rootWorldMatrix 3              ;@line 1018
						FMultiply ::temp129 ::temp130 lx                         ;@line 1018
						ArrayGetElement ::temp130 rootWorldMatrix 4              ;@line 1018
						FMultiply ::temp130 ::temp130 ly                         ;@line 1018
						FAdd ::temp129 ::temp129 ::temp130                       ;@line 1018
						ArrayGetElement ::temp130 rootWorldMatrix 5              ;@line 1018
						FMultiply ::temp130 ::temp130 ps                         ;@line 1018
						FAdd ::temp129 ::temp129 ::temp130                       ;@line 1018
						Assign wy ::temp129                                      ;@line 1018
						ArrayGetElement ::temp130 rootWorldMatrix 6              ;@line 1019
						FMultiply ::temp129 ::temp130 lx                         ;@line 1019
						ArrayGetElement ::temp130 rootWorldMatrix 7              ;@line 1019
						FMultiply ::temp130 ::temp130 ly                         ;@line 1019
						FAdd ::temp129 ::temp129 ::temp130                       ;@line 1019
						ArrayGetElement ::temp130 rootWorldMatrix 8              ;@line 1019
						FMultiply ::temp130 ::temp130 ps                         ;@line 1019
						FAdd ::temp129 ::temp129 ::temp130                       ;@line 1019
						Assign wz ::temp129                                      ;@line 1019
						ArrayGetElement ::temp130 muzzleWorldMatrix 1            ;@line 1020
						FMultiply ::temp129 wx ::temp130                         ;@line 1020
						ArrayGetElement ::temp130 muzzleWorldMatrix 4            ;@line 1020
						FMultiply ::temp130 wy ::temp130                         ;@line 1020
						FAdd ::temp129 ::temp129 ::temp130                       ;@line 1020
						ArrayGetElement ::temp130 muzzleWorldMatrix 7            ;@line 1020
						FMultiply ::temp130 wz ::temp130                         ;@line 1020
						FAdd ::temp129 ::temp129 ::temp130                       ;@line 1020
						Assign poseDot ::temp129                                 ;@line 1020
						ArrayGetElement ::temp130 muzzleWorldMatrix 1            ;@line 1021
						FMultiply ::temp129 aimX ::temp130                       ;@line 1021
						ArrayGetElement ::temp130 muzzleWorldMatrix 4            ;@line 1021
						FMultiply ::temp130 aimY ::temp130                       ;@line 1021
						FAdd ::temp129 ::temp129 ::temp130                       ;@line 1021
						ArrayGetElement ::temp130 muzzleWorldMatrix 7            ;@line 1021
						FMultiply ::temp130 aimZ ::temp130                       ;@line 1021
						FAdd ::temp129 ::temp129 ::temp130                       ;@line 1021
						Assign targetDot ::temp129                               ;@line 1021
						CallMethod Finite self ::temp128 poseDot 0.999950 1.002000  ;@line 1022
						Not ::temp128 ::temp128                                  ;@line 1022
						Cast ::temp128 ::temp128                                 ;@line 1022
						JumpT ::temp128 _label233                                ;@line 1022
						CallMethod Finite self ::temp131 targetDot 0.999950 1.002000  ;@line 1022
						Not ::temp131 ::temp131                                  ;@line 1022
						Cast ::temp128 ::temp131                                 ;@line 1022
					_label233:
						Cast ::temp128 ::temp128                                 ;@line 1022
						JumpT ::temp128 _label234                                ;@line 1022
						CallMethod Current self ::temp131 expectedGeneration expectedToken  ;@line 1022
						Not ::temp131 ::temp131                                  ;@line 1022
						Cast ::temp128 ::temp131                                 ;@line 1022
					_label234:
						JumpF ::temp128 _label235                                ;@line 1022
						Return False                                             ;@line 1023
						Jump _label235                                           ;@line 1023
					_label235:
						CallMethod PlayerClear self ::temp131 expectedGeneration expectedToken  ;@line 1025
						Assign clear ::temp131                                   ;@line 1025
						CallStatic utility IsInMenuMode ::temp128                ;@line 1026
						Assign menuOpen ::temp128                                ;@line 1026
						CallMethod ValidTarget self ::temp131 target expectedGeneration expectedToken  ;@line 1027
						Assign targetValid ::temp131                             ;@line 1027
						CallMethod Current self ::temp128 expectedGeneration expectedToken  ;@line 1028
						Cast ::temp131 ::temp128                                 ;@line 1028
						JumpF ::temp131 _label236                                ;@line 1028
						Cast ::temp131 clear                                     ;@line 1028
					_label236:
						Cast ::temp131 ::temp131                                 ;@line 1028
						JumpF ::temp131 _label237                                ;@line 1028
						Not ::temp128 menuOpen                                   ;@line 1028
						Cast ::temp131 ::temp128                                 ;@line 1028
					_label237:
						Cast ::temp128 ::temp131                                 ;@line 1028
						JumpF ::temp128 _label238                                ;@line 1028
						Cast ::temp128 targetValid                               ;@line 1028
					_label238:
						Return ::temp128                                         ;@line 1028
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
						.local ::temp95 Float
						.local ready Bool
						.local distance Float
					.endLocalTable
					.code
						CallMethod Current self ::temp92 expectedGeneration expectedToken  ;@line 782
						Not ::temp92 ::temp92                                    ;@line 782
						Cast ::temp92 ::temp92                                   ;@line 782
						JumpT ::temp92 _label239                                 ;@line 782
						Cast ::temp93 None                                       ;@line 782
						CompareEQ ::temp94 ownedGuard ::temp93                   ;@line 782
						Cast ::temp92 ::temp94                                   ;@line 782
					_label239:
						Cast ::temp92 ::temp92                                   ;@line 782
						JumpT ::temp92 _label240                                 ;@line 782
						CompareEQ ::temp94 ownedGuard ::Artillero_var            ;@line 782
						Not ::temp94 ::temp94                                    ;@line 782
						Cast ::temp92 ::temp94                                   ;@line 782
					_label240:
						JumpF ::temp92 _label241                                 ;@line 782
						Return False                                             ;@line 783
						Jump _label241                                           ;@line 783
					_label241:
						CallMethod Is3DLoaded self ::temp94                      ;@line 785
						Cast ::temp94 ::temp94                                   ;@line 785
						JumpF ::temp94 _label242                                 ;@line 785
						CallMethod IsDisabled self ::temp92                      ;@line 785
						Not ::temp92 ::temp92                                    ;@line 785
						Cast ::temp94 ::temp92                                   ;@line 785
					_label242:
						Cast ::temp94 ::temp94                                   ;@line 785
						JumpF ::temp94 _label243                                 ;@line 785
						CallMethod Is3DLoaded ownedGuard ::temp92                ;@line 785
						Cast ::temp94 ::temp92                                   ;@line 785
					_label243:
						Cast ::temp94 ::temp94                                   ;@line 785
						JumpF ::temp94 _label244                                 ;@line 785
						CallMethod IsDead ownedGuard ::temp92                    ;@line 785
						Not ::temp92 ::temp92                                    ;@line 785
						Cast ::temp94 ::temp92                                   ;@line 785
					_label244:
						Cast ::temp94 ::temp94                                   ;@line 785
						JumpF ::temp94 _label245                                 ;@line 785
						CallMethod IsDisabled ownedGuard ::temp92                ;@line 785
						Not ::temp92 ::temp92                                    ;@line 785
						Cast ::temp94 ::temp92                                   ;@line 785
					_label245:
						Assign ready ::temp94                                    ;@line 785
						CallMethod GetDistance ownedGuard ::temp95 ::Puesto_var  ;@line 786
						Assign distance ::temp95                                 ;@line 786
						CallMethod Current self ::temp92 expectedGeneration expectedToken  ;@line 787
						Cast ::temp94 ::temp92                                   ;@line 787
						JumpF ::temp94 _label246                                 ;@line 787
						Cast ::temp94 ready                                      ;@line 787
					_label246:
						Cast ::temp94 ::temp94                                   ;@line 787
						JumpF ::temp94 _label247                                 ;@line 787
						CallMethod Finite self ::temp92 distance 0.000000 64.000000  ;@line 787
						Cast ::temp94 ::temp92                                   ;@line 787
					_label247:
						Return ::temp94                                          ;@line 787
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
						.local ::temp117 Float
						.local ::temp118 Float
						.local ::temp119 Bool
						.local ::temp120 Bool
						.local dx Float
						.local dy Float
						.local dz Float
						.local lengthSquared Float
						.local along Float
					.endLocalTable
					.code
						FSubtract ::temp117 bx ax                                ;@line 930
						Assign dx ::temp117                                      ;@line 930
						FSubtract ::temp117 by ay                                ;@line 931
						Assign dy ::temp117                                      ;@line 931
						FSubtract ::temp117 bz az                                ;@line 932
						Assign dz ::temp117                                      ;@line 932
						FMultiply ::temp117 dx dx                                ;@line 933
						FMultiply ::temp118 dy dy                                ;@line 933
						FAdd ::temp117 ::temp117 ::temp118                       ;@line 933
						FMultiply ::temp118 dz dz                                ;@line 933
						FAdd ::temp117 ::temp117 ::temp118                       ;@line 933
						Assign lengthSquared ::temp117                           ;@line 933
						CompareLTE ::temp119 lengthSquared 0.000010              ;@line 934
						JumpF ::temp119 _label248                                ;@line 934
						Return True                                              ;@line 935
						Jump _label248                                           ;@line 935
					_label248:
						FSubtract ::temp118 px ax                                ;@line 937
						FMultiply ::temp117 ::temp118 dx                         ;@line 937
						FSubtract ::temp118 py ay                                ;@line 937
						FMultiply ::temp118 ::temp118 dy                         ;@line 937
						FAdd ::temp117 ::temp117 ::temp118                       ;@line 937
						FSubtract ::temp118 pz az                                ;@line 937
						FMultiply ::temp118 ::temp118 dz                         ;@line 937
						FAdd ::temp117 ::temp117 ::temp118                       ;@line 937
						FDivide ::temp118 ::temp117 lengthSquared                ;@line 937
						Assign along ::temp118                                   ;@line 937
						CompareLT ::temp119 along 0.000000                       ;@line 938
						JumpF ::temp119 _label249                                ;@line 938
						Assign along 0.000000                                    ;@line 939
						Jump _label250                                           ;@line 939
					_label249:
						CompareGT ::temp120 along 1.000000                       ;@line 940
						JumpF ::temp120 _label250                                ;@line 940
						Assign along 1.000000                                    ;@line 941
						Jump _label250                                           ;@line 941
					_label250:
						FMultiply ::temp117 along dx                             ;@line 943
						FAdd ::temp118 ax ::temp117                              ;@line 943
						FSubtract ::temp117 px ::temp118                         ;@line 943
						Assign dx ::temp117                                      ;@line 943
						FMultiply ::temp118 along dy                             ;@line 944
						FAdd ::temp117 ay ::temp118                              ;@line 944
						FSubtract ::temp118 py ::temp117                         ;@line 944
						Assign dy ::temp118                                      ;@line 944
						FMultiply ::temp117 along dz                             ;@line 945
						FAdd ::temp118 az ::temp117                              ;@line 945
						FSubtract ::temp117 pz ::temp118                         ;@line 945
						Assign dz ::temp117                                      ;@line 945
						FMultiply ::temp118 dx dx                                ;@line 946
						FMultiply ::temp117 dy dy                                ;@line 946
						FAdd ::temp118 ::temp118 ::temp117                       ;@line 946
						FMultiply ::temp117 dz dz                                ;@line 946
						FAdd ::temp118 ::temp118 ::temp117                       ;@line 946
						FMultiply ::temp117 radius radius                        ;@line 946
						CompareLTE ::temp120 ::temp118 ::temp117                 ;@line 946
						Return ::temp120                                         ;@line 946
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
						CompareLT ::temp29 timingRevision 14                     ;@line 291
						JumpF ::temp29 _label251                                 ;@line 291
						CompareGTE ::temp30 ::FireSeconds_var 0.299990           ;@line 292
						Cast ::temp30 ::temp30                                   ;@line 292
						JumpF ::temp30 _label252                                 ;@line 292
						CompareLTE ::temp31 ::FireSeconds_var 0.300010           ;@line 292
						Cast ::temp30 ::temp31                                   ;@line 292
					_label252:
						JumpF ::temp30 _label253                                 ;@line 292
						Assign ::FireSeconds_var 0.200000                        ;@line 293
						Jump _label253                                           ;@line 293
					_label253:
						CompareGTE ::temp31 ::ReleaseSeconds_var 0.099990        ;@line 295
						Cast ::temp31 ::temp31                                   ;@line 295
						JumpF ::temp31 _label254                                 ;@line 295
						CompareLTE ::temp30 ::ReleaseSeconds_var 0.100010        ;@line 295
						Cast ::temp31 ::temp30                                   ;@line 295
					_label254:
						JumpF ::temp31 _label255                                 ;@line 295
						Assign ::ReleaseSeconds_var 0.066667                     ;@line 296
						Jump _label255                                           ;@line 296
					_label255:
						CompareGTE ::temp30 ::ResetSeconds_var 1.199990          ;@line 298
						Cast ::temp30 ::temp30                                   ;@line 298
						JumpF ::temp30 _label256                                 ;@line 298
						CompareLTE ::temp31 ::ResetSeconds_var 1.200010          ;@line 298
						Cast ::temp30 ::temp31                                   ;@line 298
					_label256:
						JumpF ::temp30 _label257                                 ;@line 298
						Assign ::ResetSeconds_var 0.800000                       ;@line 299
						Jump _label257                                           ;@line 299
					_label257:
						CompareGTE ::temp31 ::CadenceSeconds_var 3.999990        ;@line 301
						Cast ::temp31 ::temp31                                   ;@line 301
						JumpF ::temp31 _label258                                 ;@line 301
						CompareLTE ::temp30 ::CadenceSeconds_var 4.000010        ;@line 301
						Cast ::temp31 ::temp30                                   ;@line 301
					_label258:
						JumpF ::temp31 _label259                                 ;@line 301
						Assign ::CadenceSeconds_var 2.500000                     ;@line 302
						Jump _label259                                           ;@line 302
					_label259:
						Assign timingRevision 14                                 ;@line 304
						Jump _label251                                           ;@line 304
					_label251:
						CallMethod Finite self ::temp30 ::FireSeconds_var 0.200000 2.000000  ;@line 306
						Not ::temp31 ::temp30                                    ;@line 306
						JumpF ::temp31 _label260                                 ;@line 306
						Assign ::FireSeconds_var 0.200000                        ;@line 307
						Jump _label260                                           ;@line 307
					_label260:
						CallMethod Finite self ::temp29 ::ReleaseSeconds_var 0.066667 1.000000  ;@line 309
						Not ::temp30 ::temp29                                    ;@line 309
						Cast ::temp29 ::temp30                                   ;@line 309
						JumpT ::temp29 _label261                                 ;@line 309
						CompareGT ::temp31 ::ReleaseSeconds_var ::FireSeconds_var  ;@line 309
						Cast ::temp29 ::temp31                                   ;@line 309
					_label261:
						JumpF ::temp29 _label262                                 ;@line 309
						Assign ::ReleaseSeconds_var 0.066667                     ;@line 310
						Jump _label262                                           ;@line 310
					_label262:
						CallMethod Finite self ::temp30 ::ResetSeconds_var 0.800000 5.000000  ;@line 312
						Not ::temp31 ::temp30                                    ;@line 312
						JumpF ::temp31 _label263                                 ;@line 312
						Assign ::ResetSeconds_var 0.800000                       ;@line 313
						Jump _label263                                           ;@line 313
					_label263:
						CallMethod SafeCadenceSeconds self ::temp32              ;@line 315
						Assign ::CadenceSeconds_var ::temp32                     ;@line 315
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
						Cast ::temp34 pinBusy                                    ;@line 329
						JumpT ::temp34 _label264                                 ;@line 329
						Cast ::temp34 sceneBusy                                  ;@line 329
					_label264:
						Cast ::temp34 ::temp34                                   ;@line 329
						JumpT ::temp34 _label265                                 ;@line 329
						CompareEQ ::temp35 generation expectedGeneration         ;@line 329
						Not ::temp35 ::temp35                                    ;@line 329
						Cast ::temp34 ::temp35                                   ;@line 329
					_label265:
						Cast ::temp35 ::temp34                                   ;@line 329
						JumpT ::temp35 _label266                                 ;@line 329
						Cast ::temp35 destroyed                                  ;@line 329
					_label266:
						Cast ::temp34 ::temp35                                   ;@line 329
						JumpT ::temp34 _label267                                 ;@line 329
						Cast ::temp34 stationRetired                             ;@line 329
					_label267:
						JumpF ::temp34 _label268                                 ;@line 329
						Return False                                             ;@line 330
						Jump _label268                                           ;@line 330
					_label268:
						Not ::temp35 ::AllowPlayerTakeover_var                   ;@line 332
						JumpF ::temp35 _label269                                 ;@line 332
						Return True                                              ;@line 333
						Jump _label269                                           ;@line 333
					_label269:
						CompareGT ::temp34 lease 0                               ;@line 335
						JumpF ::temp34 _label270                                 ;@line 335
						CallMethod PlayerLeaseCurrent self ::temp35 lease        ;@line 336
						Return ::temp35                                          ;@line 336
						Jump _label270                                           ;@line 336
					_label270:
						Cast ::temp34 recovering                                 ;@line 338
						JumpF ::temp34 _label271                                 ;@line 338
						Not ::temp34 playerReserved                              ;@line 338
						Cast ::temp34 ::temp34                                   ;@line 338
					_label271:
						Cast ::temp34 ::temp34                                   ;@line 338
						JumpF ::temp34 _label272                                 ;@line 338
						CompareEQ ::temp36 token -1                              ;@line 338
						Cast ::temp34 ::temp36                                   ;@line 338
					_label272:
						Cast ::temp34 ::temp34                                   ;@line 338
						JumpF ::temp34 _label273                                 ;@line 338
						Not ::temp36 faulted                                     ;@line 338
						Cast ::temp34 ::temp36                                   ;@line 338
					_label273:
						Return ::temp34                                          ;@line 338
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
						.local ::temp121 actor
						.local ::temp122 Bool
						.local ::temp123 Bool
						.local ::temp124 Float
						.local ::temp125 Float
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
						.local ::temp126 Bool
						.local ::temp127 Int
					.endLocalTable
					.code
						CallStatic game GetPlayer ::temp121                      ;@line 950
						Assign player ::temp121                                  ;@line 950
						CallMethod Current self ::temp122 expectedGeneration expectedToken  ;@line 951
						Not ::temp122 ::temp122                                  ;@line 951
						Cast ::temp122 ::temp122                                 ;@line 951
						JumpT ::temp122 _label274                                ;@line 951
						Cast ::temp121 None                                      ;@line 951
						CompareEQ ::temp123 player ::temp121                     ;@line 951
						Cast ::temp122 ::temp123                                 ;@line 951
					_label274:
						JumpF ::temp122 _label275                                ;@line 951
						Return False                                             ;@line 952
						Jump _label275                                           ;@line 952
					_label275:
						CallMethod Is3DLoaded player ::temp123                   ;@line 954
						Assign playerLoaded ::temp123                            ;@line 954
						CallMethod GetPositionX player ::temp124                 ;@line 955
						Assign px ::temp124                                      ;@line 955
						CallMethod GetPositionY player ::temp124                 ;@line 956
						Assign py ::temp124                                      ;@line 956
						CallMethod GetPositionZ player ::temp124                 ;@line 957
						Assign pz ::temp124                                      ;@line 957
						CallMethod GetHeight player ::temp124                    ;@line 958
						Assign height ::temp124                                  ;@line 958
						CallMethod Current self ::temp122 expectedGeneration expectedToken  ;@line 959
						Not ::temp123 ::temp122                                  ;@line 959
						Cast ::temp123 ::temp123                                 ;@line 959
						JumpT ::temp123 _label276                                ;@line 959
						Not ::temp122 playerLoaded                               ;@line 959
						Cast ::temp123 ::temp122                                 ;@line 959
					_label276:
						Cast ::temp123 ::temp123                                 ;@line 959
						JumpT ::temp123 _label277                                ;@line 959
						CallMethod Finite self ::temp122 px -1000000.000000 1000000.000000  ;@line 959
						Not ::temp122 ::temp122                                  ;@line 959
						Cast ::temp123 ::temp122                                 ;@line 959
					_label277:
						Cast ::temp123 ::temp123                                 ;@line 959
						JumpT ::temp123 _label278                                ;@line 959
						CallMethod Finite self ::temp122 py -1000000.000000 1000000.000000  ;@line 959
						Not ::temp122 ::temp122                                  ;@line 959
						Cast ::temp123 ::temp122                                 ;@line 959
					_label278:
						Cast ::temp123 ::temp123                                 ;@line 959
						JumpT ::temp123 _label279                                ;@line 959
						CallMethod Finite self ::temp122 pz -1000000.000000 1000000.000000  ;@line 959
						Not ::temp122 ::temp122                                  ;@line 959
						Cast ::temp123 ::temp122                                 ;@line 959
					_label279:
						Cast ::temp123 ::temp123                                 ;@line 959
						JumpT ::temp123 _label280                                ;@line 959
						CallMethod Finite self ::temp122 height 1.000000 512.000000  ;@line 959
						Not ::temp122 ::temp122                                  ;@line 959
						Cast ::temp123 ::temp122                                 ;@line 959
					_label280:
						JumpF ::temp123 _label281                                ;@line 959
						Return False                                             ;@line 960
						Jump _label281                                           ;@line 960
					_label281:
						CompareLT ::temp122 height 128.000000                    ;@line 962
						JumpF ::temp122 _label282                                ;@line 962
						Assign height 128.000000                                 ;@line 963
						Jump _label282                                           ;@line 963
					_label282:
						FAdd ::temp124 height 64.000000                          ;@line 965
						Assign height ::temp124                                  ;@line 965
						FDivide ::temp124 height 8.000000                        ;@line 970
						FAdd ::temp124 80.000000 ::temp124                       ;@line 970
						Assign radius ::temp124                                  ;@line 970
						ArrayGetElement ::temp124 muzzleWorldMatrix 1            ;@line 971
						Assign bx ::temp124                                      ;@line 971
						ArrayGetElement ::temp124 muzzleWorldMatrix 4            ;@line 972
						Assign by ::temp124                                      ;@line 972
						ArrayGetElement ::temp124 muzzleWorldMatrix 7            ;@line 973
						Assign bz ::temp124                                      ;@line 973
						FMultiply ::temp124 bx bx                                ;@line 974
						FMultiply ::temp125 by by                                ;@line 974
						FAdd ::temp124 ::temp124 ::temp125                       ;@line 974
						CallStatic math Sqrt ::temp125 ::temp124                 ;@line 974
						Assign boreHorizontal ::temp125                          ;@line 974
						CompareLT ::temp123 boreHorizontal 0.010000              ;@line 975
						JumpF ::temp123 _label283                                ;@line 975
						Return False                                             ;@line 976
						Jump _label283                                           ;@line 976
					_label283:
						FMultiply ::temp124 ::ProjectileSpeed_var boreHorizontal  ;@line 978
						FDivide ::temp125 targetHorizontal ::temp124             ;@line 978
						Assign totalTime ::temp125                               ;@line 978
						CallMethod Finite self ::temp122 totalTime 0.000010 30.000000  ;@line 979
						Not ::temp123 ::temp122                                  ;@line 979
						JumpF ::temp123 _label284                                ;@line 979
						Return False                                             ;@line 980
						Jump _label284                                           ;@line 980
					_label284:
						ArrayGetElement ::temp124 muzzlePosition 0               ;@line 982
						Assign ax ::temp124                                      ;@line 982
						ArrayGetElement ::temp125 muzzlePosition 1               ;@line 983
						Assign ay ::temp125                                      ;@line 983
						ArrayGetElement ::temp124 muzzlePosition 2               ;@line 984
						Assign az ::temp124                                      ;@line 984
						Assign step 1                                            ;@line 985
					_label289:
						CompareLTE ::temp122 step 8                              ;@line 986
						JumpF ::temp122 _label285                                ;@line 986
						Cast ::temp125 step                                      ;@line 987
						FMultiply ::temp124 totalTime ::temp125                  ;@line 987
						FDivide ::temp125 ::temp124 8.000000                     ;@line 987
						Assign t ::temp125                                       ;@line 987
						ArrayGetElement ::temp124 muzzlePosition 0               ;@line 988
						FMultiply ::temp125 bx ::ProjectileSpeed_var             ;@line 988
						FMultiply ::temp125 ::temp125 t                          ;@line 988
						FAdd ::temp124 ::temp124 ::temp125                       ;@line 988
						Assign ex ::temp124                                      ;@line 988
						ArrayGetElement ::temp125 muzzlePosition 1               ;@line 989
						FMultiply ::temp124 by ::ProjectileSpeed_var             ;@line 989
						FMultiply ::temp124 ::temp124 t                          ;@line 989
						FAdd ::temp125 ::temp125 ::temp124                       ;@line 989
						Assign ey ::temp125                                      ;@line 989
						ArrayGetElement ::temp124 muzzlePosition 2               ;@line 990
						FMultiply ::temp125 bz ::ProjectileSpeed_var             ;@line 990
						FMultiply ::temp125 ::temp125 t                          ;@line 990
						FAdd ::temp124 ::temp124 ::temp125                       ;@line 990
						FMultiply ::temp125 0.500000 ::ProjectileGravity_var     ;@line 990
						FMultiply ::temp125 ::temp125 t                          ;@line 990
						FMultiply ::temp125 ::temp125 t                          ;@line 990
						FSubtract ::temp124 ::temp124 ::temp125                  ;@line 990
						Assign ez ::temp124                                      ;@line 990
						Assign sample 0                                          ;@line 991
					_label288:
						CompareLTE ::temp123 sample 4                            ;@line 992
						JumpF ::temp123 _label286                                ;@line 992
						Cast ::temp125 sample                                    ;@line 993
						FMultiply ::temp124 height ::temp125                     ;@line 993
						FDivide ::temp125 ::temp124 4.000000                     ;@line 993
						FAdd ::temp124 pz ::temp125                              ;@line 993
						CallMethod PointNearSegment self ::temp126 px py ::temp124 ax ay az ex ey ez radius  ;@line 993
						JumpF ::temp126 _label287                                ;@line 993
						Return False                                             ;@line 994
						Jump _label287                                           ;@line 994
					_label287:
						IAdd ::temp127 sample 1                                  ;@line 996
						Assign sample ::temp127                                  ;@line 996
						Jump _label288                                           ;@line 996
					_label286:
						Assign ax ex                                             ;@line 998
						Assign ay ey                                             ;@line 999
						Assign az ez                                             ;@line 1000
						IAdd ::temp127 step 1                                    ;@line 1001
						Assign step ::temp127                                    ;@line 1001
						Jump _label289                                           ;@line 1001
					_label285:
						CallMethod Current self ::temp126 expectedGeneration expectedToken  ;@line 1003
						Return ::temp126                                         ;@line 1003
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
						.local ::temp105 Bool
						.local ::temp106 Bool
						.local ::temp107 Float
						.local ::temp108 Float
						.local tx Float
						.local ty Float
						.local tz Float
						.local dx Float
						.local dy Float
						.local dz Float
						.local rangeSquared Float
						.local horizontal Float
						.local tangent Float
						.local ::temp109 Float
						.local ::temp110 Bool
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
						.local certifiedPitchMax Float
					.endLocalTable
					.code
						CallMethod ValidTarget self ::temp105 target expectedGeneration expectedToken  ;@line 826
						Not ::temp105 ::temp105                                  ;@line 826
						Cast ::temp105 ::temp105                                 ;@line 826
						JumpT ::temp105 _label290                                ;@line 826
						CallMethod ReadPose self ::temp106 expectedGeneration expectedToken  ;@line 826
						Not ::temp106 ::temp106                                  ;@line 826
						Cast ::temp105 ::temp106                                 ;@line 826
					_label290:
						JumpF ::temp105 _label291                                ;@line 826
						Return False                                             ;@line 827
						Jump _label291                                           ;@line 827
					_label291:
						CallMethod GetPositionX target ::temp107                 ;@line 829
						Assign tx ::temp107                                      ;@line 829
						CallMethod GetPositionY target ::temp107                 ;@line 830
						Assign ty ::temp107                                      ;@line 830
						CallMethod GetPositionZ target ::temp107                 ;@line 831
						FAdd ::temp107 ::temp107 ::TargetHeight_var              ;@line 831
						Assign tz ::temp107                                      ;@line 831
						CallMethod Current self ::temp106 expectedGeneration expectedToken  ;@line 832
						Not ::temp105 ::temp106                                  ;@line 832
						Cast ::temp105 ::temp105                                 ;@line 832
						JumpT ::temp105 _label292                                ;@line 832
						CallMethod Finite self ::temp106 tx -1000000.000000 1000000.000000  ;@line 832
						Not ::temp106 ::temp106                                  ;@line 832
						Cast ::temp105 ::temp106                                 ;@line 832
					_label292:
						Cast ::temp105 ::temp105                                 ;@line 832
						JumpT ::temp105 _label293                                ;@line 832
						CallMethod Finite self ::temp106 ty -1000000.000000 1000000.000000  ;@line 832
						Not ::temp106 ::temp106                                  ;@line 832
						Cast ::temp105 ::temp106                                 ;@line 832
					_label293:
						Cast ::temp105 ::temp105                                 ;@line 832
						JumpT ::temp105 _label294                                ;@line 832
						CallMethod Finite self ::temp106 tz -1000000.000000 1000000.000000  ;@line 832
						Not ::temp106 ::temp106                                  ;@line 832
						Cast ::temp105 ::temp106                                 ;@line 832
					_label294:
						JumpF ::temp105 _label295                                ;@line 832
						Return False                                             ;@line 833
						Jump _label295                                           ;@line 833
					_label295:
						ArrayGetElement ::temp107 muzzlePosition 0               ;@line 835
						FSubtract ::temp107 tx ::temp107                         ;@line 835
						Assign dx ::temp107                                      ;@line 835
						ArrayGetElement ::temp107 muzzlePosition 1               ;@line 836
						FSubtract ::temp107 ty ::temp107                         ;@line 836
						Assign dy ::temp107                                      ;@line 836
						ArrayGetElement ::temp107 muzzlePosition 2               ;@line 837
						FSubtract ::temp107 tz ::temp107                         ;@line 837
						Assign dz ::temp107                                      ;@line 837
						FMultiply ::temp107 dx dx                                ;@line 838
						FMultiply ::temp108 dy dy                                ;@line 838
						FAdd ::temp107 ::temp107 ::temp108                       ;@line 838
						FMultiply ::temp108 dz dz                                ;@line 838
						FAdd ::temp107 ::temp107 ::temp108                       ;@line 838
						Assign rangeSquared ::temp107                            ;@line 838
						CallMethod Finite self ::temp106 rangeSquared 6400.000000 36000000.000000  ;@line 839
						Not ::temp105 ::temp106                                  ;@line 839
						Cast ::temp105 ::temp105                                 ;@line 839
						JumpT ::temp105 _label296                                ;@line 839
						CallMethod Finite self ::temp106 ::ProjectileSpeed_var 1.000000 100000.000000  ;@line 839
						Not ::temp106 ::temp106                                  ;@line 839
						Cast ::temp105 ::temp106                                 ;@line 839
					_label296:
						Cast ::temp105 ::temp105                                 ;@line 839
						JumpT ::temp105 _label297                                ;@line 839
						CallMethod Finite self ::temp106 ::ProjectileGravity_var 0.000000 5000.000000  ;@line 839
						Not ::temp106 ::temp106                                  ;@line 839
						Cast ::temp105 ::temp106                                 ;@line 839
					_label297:
						JumpF ::temp105 _label298                                ;@line 839
						Return False                                             ;@line 840
						Jump _label298                                           ;@line 840
					_label298:
						FMultiply ::temp108 dx dx                                ;@line 842
						FMultiply ::temp107 dy dy                                ;@line 842
						FAdd ::temp108 ::temp108 ::temp107                       ;@line 842
						CallStatic math Sqrt ::temp107 ::temp108                 ;@line 842
						Assign horizontal ::temp107                              ;@line 842
						CompareLT ::temp106 horizontal 0.010000                  ;@line 843
						JumpF ::temp106 _label299                                ;@line 843
						Return False                                             ;@line 844
						Jump _label299                                           ;@line 844
					_label299:
						FDivide ::temp108 dz horizontal                          ;@line 846
						Assign tangent ::temp108                                 ;@line 846
						CompareGT ::temp105 ::ProjectileGravity_var 0.000000     ;@line 847
						JumpF ::temp105 _label300                                ;@line 847
						FMultiply ::temp107 ::ProjectileSpeed_var ::ProjectileSpeed_var  ;@line 851
						Assign speedSquared ::temp107                            ;@line 851
						FMultiply ::temp108 speedSquared speedSquared            ;@line 852
						FMultiply ::temp107 ::ProjectileGravity_var horizontal   ;@line 852
						FMultiply ::temp107 ::temp107 horizontal                 ;@line 852
						FMultiply ::temp109 2.000000 dz                          ;@line 852
						FMultiply ::temp109 ::temp109 speedSquared               ;@line 852
						FAdd ::temp107 ::temp107 ::temp109                       ;@line 852
						FMultiply ::temp109 ::ProjectileGravity_var ::temp107    ;@line 852
						FSubtract ::temp107 ::temp108 ::temp109                  ;@line 852
						Assign discriminant ::temp107                            ;@line 852
						CompareLT ::temp106 discriminant 0.000000                ;@line 853
						Cast ::temp106 ::temp106                                 ;@line 853
						JumpT ::temp106 _label301                                ;@line 853
						CompareEQ ::temp110 discriminant discriminant            ;@line 853
						Not ::temp110 ::temp110                                  ;@line 853
						Cast ::temp106 ::temp110                                 ;@line 853
					_label301:
						JumpF ::temp106 _label302                                ;@line 853
						Return False                                             ;@line 854
						Jump _label302                                           ;@line 854
					_label302:
						FMultiply ::temp108 ::ProjectileGravity_var horizontal   ;@line 856
						FMultiply ::temp109 ::temp108 horizontal                 ;@line 856
						FMultiply ::temp107 2.000000 dz                          ;@line 856
						FMultiply ::temp108 ::temp107 speedSquared               ;@line 856
						FAdd ::temp107 ::temp109 ::temp108                       ;@line 856
						CallStatic math Sqrt ::temp109 discriminant              ;@line 856
						FAdd ::temp108 speedSquared ::temp109                    ;@line 856
						FMultiply ::temp109 horizontal ::temp108                 ;@line 856
						FDivide ::temp108 ::temp107 ::temp109                    ;@line 856
						Assign tangent ::temp108                                 ;@line 856
						Jump _label300                                           ;@line 856
					_label300:
						FMultiply ::temp107 tangent tangent                      ;@line 858
						FAdd ::temp109 1.000000 ::temp107                        ;@line 858
						CallStatic math Sqrt ::temp108 ::temp109                 ;@line 858
						FDivide ::temp107 1.000000 ::temp108                     ;@line 858
						Assign horizontalFactor ::temp107                        ;@line 858
						FDivide ::temp109 dx horizontal                          ;@line 859
						FMultiply ::temp108 ::temp109 horizontalFactor           ;@line 859
						Assign wx ::temp108                                      ;@line 859
						FDivide ::temp107 dy horizontal                          ;@line 860
						FMultiply ::temp109 ::temp107 horizontalFactor           ;@line 860
						Assign wy ::temp109                                      ;@line 860
						FMultiply ::temp108 tangent horizontalFactor             ;@line 861
						Assign wz ::temp108                                      ;@line 861
						ArrayGetElement ::temp107 rootWorldMatrix 0              ;@line 863
						FMultiply ::temp109 ::temp107 wx                         ;@line 863
						ArrayGetElement ::temp108 rootWorldMatrix 3              ;@line 863
						FMultiply ::temp107 ::temp108 wy                         ;@line 863
						FAdd ::temp108 ::temp109 ::temp107                       ;@line 863
						ArrayGetElement ::temp109 rootWorldMatrix 6              ;@line 863
						FMultiply ::temp107 ::temp109 wz                         ;@line 863
						FAdd ::temp109 ::temp108 ::temp107                       ;@line 863
						Assign lx ::temp109                                      ;@line 863
						ArrayGetElement ::temp108 rootWorldMatrix 1              ;@line 864
						FMultiply ::temp107 ::temp108 wx                         ;@line 864
						ArrayGetElement ::temp109 rootWorldMatrix 4              ;@line 864
						FMultiply ::temp108 ::temp109 wy                         ;@line 864
						FAdd ::temp109 ::temp107 ::temp108                       ;@line 864
						ArrayGetElement ::temp107 rootWorldMatrix 7              ;@line 864
						FMultiply ::temp108 ::temp107 wz                         ;@line 864
						FAdd ::temp107 ::temp109 ::temp108                       ;@line 864
						Assign ly ::temp107                                      ;@line 864
						ArrayGetElement ::temp109 rootWorldMatrix 2              ;@line 865
						FMultiply ::temp108 ::temp109 wx                         ;@line 865
						ArrayGetElement ::temp107 rootWorldMatrix 5              ;@line 865
						FMultiply ::temp109 ::temp107 wy                         ;@line 865
						FAdd ::temp107 ::temp108 ::temp109                       ;@line 865
						ArrayGetElement ::temp108 rootWorldMatrix 8              ;@line 865
						FMultiply ::temp109 ::temp108 wz                         ;@line 865
						FAdd ::temp108 ::temp107 ::temp109                       ;@line 865
						Assign lz ::temp108                                      ;@line 865
						CompareGT ::temp110 lz 1.000000                          ;@line 866
						JumpF ::temp110 _label303                                ;@line 866
						Assign lz 1.000000                                       ;@line 867
						Jump _label304                                           ;@line 867
					_label303:
						CompareLT ::temp106 lz -1.000000                         ;@line 868
						JumpF ::temp106 _label304                                ;@line 868
						Assign lz -1.000000                                      ;@line 869
						Jump _label304                                           ;@line 869
					_label304:
						FNegate ::temp107 ly                                     ;@line 871
						CallMethod HeadingFromVector self ::temp109 lx ::temp107 yaw  ;@line 871
						Assign nextYaw ::temp109                                 ;@line 871
						CompareGT ::temp105 nextYaw 180.000000                   ;@line 872
						JumpF ::temp105 _label305                                ;@line 872
						FSubtract ::temp108 nextYaw 360.000000                   ;@line 873
						Assign nextYaw ::temp108                                 ;@line 873
						Jump _label305                                           ;@line 873
					_label305:
						CallStatic math ASin ::temp107 lz                        ;@line 875
						Assign nextPitch ::temp107                               ;@line 875
						Assign certifiedPitchMax 45.000000                       ;@line 877
						JumpF ::AllowPlayerTakeover_var _label306                ;@line 878
						Assign certifiedPitchMax 80.000000                       ;@line 880
						Jump _label306                                           ;@line 880
					_label306:
						CallMethod Finite self ::temp106 ::PitchMin_var -20.000000 certifiedPitchMax  ;@line 882
						Not ::temp110 ::temp106                                  ;@line 882
						Cast ::temp105 ::temp110                                 ;@line 882
						JumpT ::temp105 _label307                                ;@line 882
						CallMethod Finite self ::temp105 ::PitchMax_var -20.000000 certifiedPitchMax  ;@line 882
						Not ::temp106 ::temp105                                  ;@line 882
						Cast ::temp105 ::temp106                                 ;@line 882
					_label307:
						Cast ::temp106 ::temp105                                 ;@line 882
						JumpT ::temp106 _label308                                ;@line 882
						CompareGTE ::temp110 ::PitchMin_var ::PitchMax_var       ;@line 882
						Cast ::temp106 ::temp110                                 ;@line 882
					_label308:
						JumpF ::temp106 _label309                                ;@line 882
						Return False                                             ;@line 883
						Jump _label309                                           ;@line 883
					_label309:
						CallMethod Finite self ::temp105 ::YawHalfSector_var 1.000000 60.000000  ;@line 885
						Not ::temp110 ::temp105                                  ;@line 885
						JumpF ::temp110 _label310                                ;@line 885
						Return False                                             ;@line 886
						Jump _label310                                           ;@line 886
					_label310:
						FAdd ::temp109 -60.000000 ::YawHalfSector_var            ;@line 888
						FSubtract ::temp108 60.000000 ::YawHalfSector_var        ;@line 888
						CallMethod Finite self ::temp106 ::YawCenter_var ::temp109 ::temp108  ;@line 888
						Not ::temp105 ::temp106                                  ;@line 888
						JumpF ::temp105 _label311                                ;@line 888
						Return False                                             ;@line 889
						Jump _label311                                           ;@line 889
					_label311:
						FSubtract ::temp107 ::YawCenter_var ::YawHalfSector_var  ;@line 891
						FAdd ::temp109 ::YawCenter_var ::YawHalfSector_var       ;@line 891
						CallMethod Finite self ::temp110 nextYaw ::temp107 ::temp109  ;@line 891
						Not ::temp106 ::temp110                                  ;@line 891
						Cast ::temp105 ::temp106                                 ;@line 891
						JumpT ::temp105 _label312                                ;@line 891
						CallMethod Finite self ::temp105 nextPitch ::PitchMin_var ::PitchMax_var  ;@line 891
						Not ::temp110 ::temp105                                  ;@line 891
						Cast ::temp105 ::temp110                                 ;@line 891
					_label312:
						Cast ::temp106 ::temp105                                 ;@line 891
						JumpT ::temp106 _label313                                ;@line 891
						CallMethod Current self ::temp106 expectedGeneration expectedToken  ;@line 891
						Not ::temp110 ::temp106                                  ;@line 891
						Cast ::temp106 ::temp110                                 ;@line 891
					_label313:
						JumpF ::temp106 _label314                                ;@line 891
						Return False                                             ;@line 892
						Jump _label314                                           ;@line 892
					_label314:
						Assign desiredYaw nextYaw                                ;@line 894
						Assign desiredPitch nextPitch                            ;@line 895
						Assign aimX wx                                           ;@line 896
						Assign aimY wy                                           ;@line 897
						Assign aimZ wz                                           ;@line 898
						Assign targetHorizontal horizontal                       ;@line 899
						Return True                                              ;@line 900
					.endCode
				.endFunction
				.function OnUpdate
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp146 Bool
						.local ::temp147 Float
						.local ::NoneVar None
						.local updateGeneration Int
						.local updateToken Int
						.local now Float
						.local dt Float
						.local ready Bool
						.local ::temp148 Bool
						.local ::temp149 Bool
						.local dead Bool
						.local guardLoaded Bool
						.local gunLoaded Bool
						.local menuOpen Bool
						.local releaseDelay Float
						.local fireDelay Float
						.local resetDelay Float
						.local ::temp150 Bool
						.local ::temp151 actor
						.local target actor
						.local sampled Bool
						.local poseRead Bool
						.local ::temp152 Float
						.local heading Float
						.local aligned Bool
					.endLocalTable
					.code
						Cast ::temp146 updating                                  ;@line 1145
						JumpT ::temp146 _label315                                ;@line 1145
						Cast ::temp146 recovering                                ;@line 1145
					_label315:
						Cast ::temp146 ::temp146                                 ;@line 1145
						JumpT ::temp146 _label316                                ;@line 1145
						Cast ::temp146 pinBusy                                   ;@line 1145
					_label316:
						Cast ::temp146 ::temp146                                 ;@line 1145
						JumpT ::temp146 _label317                                ;@line 1145
						Cast ::temp146 sceneBusy                                 ;@line 1145
					_label317:
						Cast ::temp146 ::temp146                                 ;@line 1145
						JumpT ::temp146 _label318                                ;@line 1145
						Cast ::temp146 destroyed                                 ;@line 1145
					_label318:
						Cast ::temp146 ::temp146                                 ;@line 1145
						JumpT ::temp146 _label319                                ;@line 1145
						Cast ::temp146 faulted                                   ;@line 1145
					_label319:
						JumpF ::temp146 _label320                                ;@line 1145
						Return None                                              ;@line 1146
						Jump _label320                                           ;@line 1146
					_label320:
						Not ::temp146 running                                    ;@line 1148
						JumpF ::temp146 _label321                                ;@line 1148
						CallMethod BeginRecovery self ::NoneVar                  ;@line 1149
						Return None                                              ;@line 1150
						Jump _label321                                           ;@line 1150
					_label321:
						Assign updating True                                     ;@line 1152
						Assign updateGeneration generation                       ;@line 1153
						Assign updateToken token                                 ;@line 1154
						CallStatic utility GetCurrentRealTime ::temp147          ;@line 1155
						Assign now ::temp147                                     ;@line 1155
						CallMethod Current self ::temp146 updateGeneration updateToken  ;@line 1156
						Not ::temp146 ::temp146                                  ;@line 1156
						JumpF ::temp146 _label322                                ;@line 1156
						Return None                                              ;@line 1157
						Jump _label322                                           ;@line 1157
					_label322:
						CallMethod Finite self ::temp146 now 0.000000 1000000000.000000  ;@line 1159
						Not ::temp146 ::temp146                                  ;@line 1159
						JumpF ::temp146 _label323                                ;@line 1159
						Assign faulted True                                      ;@line 1160
						CallMethod Shutdown self ::NoneVar                       ;@line 1161
						Return None                                              ;@line 1162
						Jump _label323                                           ;@line 1162
					_label323:
						CompareLT ::temp146 now lastTick                         ;@line 1164
						JumpF ::temp146 _label324                                ;@line 1164
						CallMethod BeginRecovery self ::NoneVar                  ;@line 1167
						Return None                                              ;@line 1168
						Jump _label324                                           ;@line 1168
					_label324:
						FSubtract ::temp147 now lastTick                         ;@line 1170
						Assign dt ::temp147                                      ;@line 1170
						CompareGT ::temp146 dt 0.400000                          ;@line 1171
						JumpF ::temp146 _label325                                ;@line 1171
						Assign dt 0.400000                                       ;@line 1172
						Jump _label325                                           ;@line 1172
					_label325:
						Assign lastTick now                                      ;@line 1174
						CallMethod GuardReady self ::temp146 updateGeneration updateToken  ;@line 1175
						Assign ready ::temp146                                   ;@line 1175
						CallMethod Current self ::temp146 updateGeneration updateToken  ;@line 1176
						Not ::temp146 ::temp146                                  ;@line 1176
						JumpF ::temp146 _label326                                ;@line 1176
						Return None                                              ;@line 1177
						Jump _label326                                           ;@line 1177
					_label326:
						Not ::temp146 ready                                      ;@line 1179
						JumpF ::temp146 _label327                                ;@line 1179
						CallMethod IsDead ::Artillero_var ::temp148              ;@line 1180
						Assign dead ::temp148                                    ;@line 1180
						CallMethod Is3DLoaded ::Artillero_var ::temp148          ;@line 1181
						Assign guardLoaded ::temp148                             ;@line 1181
						CallMethod Is3DLoaded self ::temp148                     ;@line 1182
						Assign gunLoaded ::temp148                               ;@line 1182
						CallMethod Current self ::temp148 updateGeneration updateToken  ;@line 1183
						Not ::temp148 ::temp148                                  ;@line 1183
						JumpF ::temp148 _label328                                ;@line 1183
						Return None                                              ;@line 1184
						Jump _label328                                           ;@line 1184
					_label328:
						Cast ::temp148 dead                                      ;@line 1188
						JumpT ::temp148 _label329                                ;@line 1188
						Cast ::temp148 guardLoaded                               ;@line 1188
					_label329:
						Assign faulted ::temp148                                 ;@line 1188
						CallMethod Shutdown self ::NoneVar                       ;@line 1189
						Not ::temp148 faulted                                    ;@line 1190
						Cast ::temp148 ::temp148                                 ;@line 1190
						JumpF ::temp148 _label330                                ;@line 1190
						Cast ::temp148 gunLoaded                                 ;@line 1190
					_label330:
						Cast ::temp148 ::temp148                                 ;@line 1190
						JumpF ::temp148 _label331                                ;@line 1190
						Not ::temp149 destroyed                                  ;@line 1190
						Cast ::temp148 ::temp149                                 ;@line 1190
					_label331:
						JumpF ::temp148 _label332                                ;@line 1190
						CallMethod RegisterForSingleUpdate self ::NoneVar 1.000000  ;@line 1191
						Jump _label332                                           ;@line 1191
					_label332:
						Return None                                              ;@line 1193
						Jump _label327                                           ;@line 1193
					_label327:
						CallStatic utility IsInMenuMode ::temp149                ;@line 1195
						Assign menuOpen ::temp149                                ;@line 1195
						CallMethod Current self ::temp148 updateGeneration updateToken  ;@line 1196
						Not ::temp146 ::temp148                                  ;@line 1196
						JumpF ::temp146 _label333                                ;@line 1196
						Return None                                              ;@line 1197
						Jump _label333                                           ;@line 1197
					_label333:
						Cast ::temp149 menuOpen                                  ;@line 1199
						JumpF ::temp149 _label334                                ;@line 1199
						CompareEQ ::temp149 phase 1                              ;@line 1199
						Cast ::temp146 ::temp149                                 ;@line 1199
						JumpT ::temp146 _label335                                ;@line 1199
						CompareEQ ::temp148 phase 2                              ;@line 1199
						Cast ::temp146 ::temp148                                 ;@line 1199
					_label335:
						Cast ::temp149 ::temp146                                 ;@line 1199
					_label334:
						JumpF ::temp149 _label336                                ;@line 1199
						CallMethod AbortShot self ::NoneVar updateGeneration updateToken  ;@line 1200
						Jump _label336                                           ;@line 1200
					_label336:
						CallMethod Current self ::temp148 updateGeneration updateToken  ;@line 1202
						Not ::temp146 ::temp148                                  ;@line 1202
						JumpF ::temp146 _label337                                ;@line 1202
						Return None                                              ;@line 1203
						Jump _label337                                           ;@line 1203
					_label337:
						CompareEQ ::temp149 phase 1                              ;@line 1205
						JumpF ::temp149 _label338                                ;@line 1205
						Assign releaseDelay ::ReleaseSeconds_var                 ;@line 1207
						CallMethod Finite self ::temp148 releaseDelay 0.066667 1.000000  ;@line 1208
						Not ::temp146 ::temp148                                  ;@line 1208
						Cast ::temp146 ::temp146                                 ;@line 1208
						JumpT ::temp146 _label339                                ;@line 1208
						CompareGT ::temp148 releaseDelay ::FireSeconds_var       ;@line 1208
						Cast ::temp146 ::temp148                                 ;@line 1208
					_label339:
						JumpF ::temp146 _label340                                ;@line 1208
						Assign releaseDelay 0.066667                             ;@line 1209
						Jump _label340                                           ;@line 1209
					_label340:
						FAdd ::temp147 phaseAt releaseDelay                      ;@line 1211
						CompareGTE ::temp148 now ::temp147                       ;@line 1211
						JumpF ::temp148 _label341                                ;@line 1211
						CallMethod CommitShot self ::NoneVar shotTarget updateGeneration updateToken  ;@line 1212
						Jump _label341                                           ;@line 1212
					_label341:
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 0.200000  ;@line 1214
						Return None                                              ;@line 1215
						Jump _label342                                           ;@line 1215
					_label338:
						CompareEQ ::temp146 phase 2                              ;@line 1216
						JumpF ::temp146 _label343                                ;@line 1216
						Assign fireDelay ::FireSeconds_var                       ;@line 1217
						CallMethod Finite self ::temp148 fireDelay 0.200000 2.000000  ;@line 1218
						Not ::temp148 ::temp148                                  ;@line 1218
						JumpF ::temp148 _label344                                ;@line 1218
						Assign fireDelay 0.200000                                ;@line 1219
						Jump _label344                                           ;@line 1219
					_label344:
						FAdd ::temp147 phaseAt fireDelay                         ;@line 1221
						CompareGTE ::temp148 now ::temp147                       ;@line 1221
						JumpF ::temp148 _label345                                ;@line 1221
						CallMethod StartReset self ::NoneVar updateGeneration updateToken  ;@line 1222
						Jump _label345                                           ;@line 1222
					_label345:
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 0.200000  ;@line 1224
						Return None                                              ;@line 1225
						Jump _label342                                           ;@line 1225
					_label343:
						CompareEQ ::temp148 phase 3                              ;@line 1226
						JumpF ::temp148 _label342                                ;@line 1226
						Assign resetDelay ::ResetSeconds_var                     ;@line 1227
						CallMethod Finite self ::temp146 resetDelay 0.800000 5.000000  ;@line 1228
						Not ::temp146 ::temp146                                  ;@line 1228
						JumpF ::temp146 _label346                                ;@line 1228
						Assign resetDelay 0.800000                               ;@line 1229
						Jump _label346                                           ;@line 1229
					_label346:
						FAdd ::temp147 phaseAt resetDelay                        ;@line 1231
						CompareGTE ::temp146 now ::temp147                       ;@line 1231
						JumpF ::temp146 _label347                                ;@line 1231
						CallMethod SetVisualBolt self ::NoneVar 1.000000 updateGeneration updateToken  ;@line 1232
						CallMethod Current self ::temp150 updateGeneration updateToken  ;@line 1233
						Not ::temp150 ::temp150                                  ;@line 1233
						JumpF ::temp150 _label348                                ;@line 1233
						Return None                                              ;@line 1234
						Jump _label348                                           ;@line 1234
					_label348:
						Assign phase 0                                           ;@line 1236
						Cast ::temp151 None                                      ;@line 1237
						Assign shotTarget ::temp151                              ;@line 1237
						Jump _label347                                           ;@line 1237
					_label347:
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 0.200000  ;@line 1239
						Return None                                              ;@line 1240
						Jump _label342                                           ;@line 1240
					_label342:
						JumpF menuOpen _label349                                 ;@line 1242
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 1.000000  ;@line 1243
						Return None                                              ;@line 1244
						Jump _label349                                           ;@line 1244
					_label349:
						CallMethod GetCombatTarget ::Artillero_var ::temp151     ;@line 1246
						Assign target ::temp151                                  ;@line 1246
						CallMethod SampleTarget self ::temp150 target updateGeneration updateToken  ;@line 1247
						Assign sampled ::temp150                                 ;@line 1247
						CallMethod Current self ::temp146 updateGeneration updateToken  ;@line 1248
						Not ::temp148 ::temp146                                  ;@line 1248
						JumpF ::temp148 _label350                                ;@line 1248
						Return None                                              ;@line 1249
						Jump _label350                                           ;@line 1249
					_label350:
						Not ::temp149 sampled                                    ;@line 1251
						JumpF ::temp149 _label351                                ;@line 1251
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 1.000000  ;@line 1252
						Return None                                              ;@line 1253
						Jump _label351                                           ;@line 1253
					_label351:
						CallMethod TurnToward self ::NoneVar dt updateGeneration updateToken  ;@line 1255
						CallMethod Current self ::temp150 updateGeneration updateToken  ;@line 1256
						Not ::temp146 ::temp150                                  ;@line 1256
						JumpF ::temp146 _label352                                ;@line 1256
						Return None                                              ;@line 1257
						Jump _label352                                           ;@line 1257
					_label352:
						CallMethod ReadPose self ::temp148 updateGeneration updateToken  ;@line 1259
						Assign poseRead ::temp148                                ;@line 1259
						CallMethod Current self ::temp149 updateGeneration updateToken  ;@line 1260
						Not ::temp150 ::temp149                                  ;@line 1260
						JumpF ::temp150 _label353                                ;@line 1260
						Return None                                              ;@line 1261
						Jump _label353                                           ;@line 1261
					_label353:
						JumpF poseRead _label354                                 ;@line 1263
						ArrayGetElement ::temp147 muzzleWorldMatrix 1            ;@line 1264
						ArrayGetElement ::temp152 muzzleWorldMatrix 4            ;@line 1264
						CallMethod HeadingFromVector self ::temp147 ::temp147 ::temp152 0.000000  ;@line 1264
						Assign heading ::temp147                                 ;@line 1264
						CallMethod Current self ::temp146 updateGeneration updateToken  ;@line 1265
						Not ::temp148 ::temp146                                  ;@line 1265
						JumpF ::temp148 _label355                                ;@line 1265
						Return None                                              ;@line 1266
						Jump _label355                                           ;@line 1266
					_label355:
						CallMethod SetAngle ::Artillero_var ::NoneVar 0.000000 0.000000 heading  ;@line 1268
						Jump _label354                                           ;@line 1268
					_label354:
						CompareGTE ::temp149 now nextShotAt                      ;@line 1271
						JumpF ::temp149 _label356                                ;@line 1271
						CallMethod ShotPreflight self ::temp150 target updateGeneration updateToken  ;@line 1272
						Assign aligned ::temp150                                 ;@line 1272
						CallMethod Current self ::temp146 updateGeneration updateToken  ;@line 1273
						Not ::temp148 ::temp146                                  ;@line 1273
						JumpF ::temp148 _label357                                ;@line 1273
						Return None                                              ;@line 1274
						Jump _label357                                           ;@line 1274
					_label357:
						JumpF aligned _label358                                  ;@line 1276
						CallMethod BeginShot self ::NoneVar target updateGeneration updateToken  ;@line 1277
						Jump _label358                                           ;@line 1277
					_label358:
						Jump _label356                                           ;@line 1277
					_label356:
						CallMethod Current self ::temp150 updateGeneration updateToken  ;@line 1280
						JumpF ::temp150 _label359                                ;@line 1280
						CompareEQ ::temp146 phase 1                              ;@line 1281
						JumpF ::temp146 _label360                                ;@line 1281
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 0.100000  ;@line 1282
						Jump _label361                                           ;@line 1282
					_label360:
						CallMethod FinishUpdate self ::NoneVar updateGeneration updateToken 0.200000  ;@line 1284
					_label361:
						Jump _label359                                           ;@line 1284
					_label359:
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
						CallMethod InvalidatePlayerLease self ::NoneVar          ;@line 81
						CallMethod BeginRecovery self ::NoneVar                  ;@line 84
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
						CallMethod PlayerLeaseCurrent self ::temp18 lease        ;@line 179
						Not ::temp18 ::temp18                                    ;@line 179
						Cast ::temp18 ::temp18                                   ;@line 179
						JumpT ::temp18 _label362                                 ;@line 179
						Cast ::temp18 pinBusy                                    ;@line 179
					_label362:
						Cast ::temp18 ::temp18                                   ;@line 179
						JumpT ::temp18 _label363                                 ;@line 179
						Cast ::temp18 sceneBusy                                  ;@line 179
					_label363:
						Cast ::temp18 ::temp18                                   ;@line 179
						JumpT ::temp18 _label364                                 ;@line 179
						Cast ::temp18 recovering                                 ;@line 179
					_label364:
						Cast ::temp18 ::temp18                                   ;@line 179
						JumpT ::temp18 _label365                                 ;@line 179
						Cast ::temp18 running                                    ;@line 179
					_label365:
						JumpF ::temp18 _label366                                 ;@line 179
						Return False                                             ;@line 180
						Jump _label366                                           ;@line 180
					_label366:
						JumpF playerReady _label367                              ;@line 182
						Return True                                              ;@line 183
						Jump _label367                                           ;@line 183
					_label367:
						CallMethod StationSceneAvailable self ::temp18           ;@line 185
						Assign sceneFree ::temp18                                ;@line 185
						CallMethod PlayerLeaseCurrent self ::temp18 lease        ;@line 186
						Not ::temp18 ::temp18                                    ;@line 186
						Cast ::temp18 ::temp18                                   ;@line 186
						JumpT ::temp18 _label368                                 ;@line 186
						Cast ::temp18 pinBusy                                    ;@line 186
					_label368:
						Cast ::temp18 ::temp18                                   ;@line 186
						JumpT ::temp18 _label369                                 ;@line 186
						Cast ::temp18 sceneBusy                                  ;@line 186
					_label369:
						Cast ::temp18 ::temp18                                   ;@line 186
						JumpT ::temp18 _label370                                 ;@line 186
						Not ::temp19 sceneFree                                   ;@line 186
						Cast ::temp18 ::temp19                                   ;@line 186
					_label370:
						JumpF ::temp18 _label371                                 ;@line 186
						Return False                                             ;@line 187
						Jump _label371                                           ;@line 187
					_label371:
						CallStatic skse GetPluginVersion ::temp20 "AstraSight"   ;@line 189
						Assign scenePluginVersion ::temp20                       ;@line 189
						CallMethod PlayerLeaseCurrent self ::temp19 lease        ;@line 190
						Not ::temp18 ::temp19                                    ;@line 190
						Cast ::temp18 ::temp18                                   ;@line 190
						JumpT ::temp18 _label372                                 ;@line 190
						CompareLT ::temp19 scenePluginVersion 50659392           ;@line 190
						Cast ::temp18 ::temp19                                   ;@line 190
					_label372:
						JumpF ::temp18 _label373                                 ;@line 190
						Return False                                             ;@line 191
						Jump _label373                                           ;@line 191
					_label373:
						CallMethod ReleaseOwnedGuard self ::NoneVar              ;@line 193
						CallMethod PlayerLeaseCurrent self ::temp19 lease        ;@line 194
						Not ::temp18 ::temp19                                    ;@line 194
						Cast ::temp19 ::temp18                                   ;@line 194
						JumpT ::temp19 _label374                                 ;@line 194
						Cast ::temp19 pinBusy                                    ;@line 194
					_label374:
						Cast ::temp18 ::temp19                                   ;@line 194
						JumpT ::temp18 _label375                                 ;@line 194
						Cast ::temp18 sceneBusy                                  ;@line 194
					_label375:
						JumpF ::temp18 _label376                                 ;@line 194
						Return False                                             ;@line 195
						Jump _label376                                           ;@line 195
					_label376:
						CallMethod EnsureCityPlacement self ::temp19 generation lease  ;@line 197
						Assign placed ::temp19                                   ;@line 197
						CallMethod PlayerLeaseCurrent self ::temp18 lease        ;@line 198
						Not ::temp19 ::temp18                                    ;@line 198
						Cast ::temp18 ::temp19                                   ;@line 198
						JumpT ::temp18 _label377                                 ;@line 198
						Cast ::temp18 pinBusy                                    ;@line 198
					_label377:
						Cast ::temp19 ::temp18                                   ;@line 198
						JumpT ::temp19 _label378                                 ;@line 198
						Cast ::temp19 sceneBusy                                  ;@line 198
					_label378:
						Cast ::temp19 ::temp19                                   ;@line 198
						JumpT ::temp19 _label379                                 ;@line 198
						Not ::temp18 placed                                      ;@line 198
						Cast ::temp19 ::temp18                                   ;@line 198
					_label379:
						JumpF ::temp19 _label380                                 ;@line 198
						Return False                                             ;@line 199
						Jump _label380                                           ;@line 199
					_label380:
						Not ::temp18 playerRestored                              ;@line 201
						JumpF ::temp18 _label381                                 ;@line 201
						CallMethod Is3DLoaded self ::temp19                      ;@line 202
						Assign loaded ::temp19                                   ;@line 202
						Cast ::temp21 self                                       ;@line 203
						CallStatic netimmerse HasNode ::temp19 ::temp21 ::YawNode_var False  ;@line 203
						Cast ::temp19 ::temp19                                   ;@line 203
						JumpF ::temp19 _label382                                 ;@line 203
						Cast ::temp21 self                                       ;@line 203
						CallStatic netimmerse HasNode ::temp22 ::temp21 ::PitchNode_var False  ;@line 203
						Cast ::temp19 ::temp22                                   ;@line 203
					_label382:
						Assign controls ::temp19                                 ;@line 203
						CallMethod PlayerLeaseCurrent self ::temp22 lease        ;@line 204
						Not ::temp19 ::temp22                                    ;@line 204
						Cast ::temp22 ::temp19                                   ;@line 204
						JumpT ::temp22 _label383                                 ;@line 204
						Cast ::temp22 pinBusy                                    ;@line 204
					_label383:
						Cast ::temp19 ::temp22                                   ;@line 204
						JumpT ::temp19 _label384                                 ;@line 204
						Cast ::temp19 sceneBusy                                  ;@line 204
					_label384:
						Cast ::temp19 ::temp19                                   ;@line 204
						JumpT ::temp19 _label385                                 ;@line 204
						Not ::temp22 loaded                                      ;@line 204
						Cast ::temp19 ::temp22                                   ;@line 204
					_label385:
						Cast ::temp19 ::temp19                                   ;@line 204
						JumpT ::temp19 _label386                                 ;@line 204
						Not ::temp22 controls                                    ;@line 204
						Cast ::temp19 ::temp22                                   ;@line 204
					_label386:
						JumpF ::temp19 _label387                                 ;@line 204
						Return False                                             ;@line 205
						Jump _label387                                           ;@line 205
					_label387:
						ArrayCreate ::temp23 9                                   ;@line 209
						Assign rest ::temp23                                     ;@line 209
						Assign ::temp24 1.000000                                 ;@line 210
						ArraySetElement rest 0 ::temp24                          ;@line 210
						Assign ::temp24 1.000000                                 ;@line 211
						ArraySetElement rest 4 ::temp24                          ;@line 211
						Assign ::temp24 1.000000                                 ;@line 212
						ArraySetElement rest 8 ::temp24                          ;@line 212
						Assign sceneBusy True                                    ;@line 213
						Cast ::temp21 self                                       ;@line 214
						CallStatic astrasightnative ResetIdleScene ::temp22 ::temp21  ;@line 214
						Assign settled ::temp22                                  ;@line 214
						CallMethod PlayerLeaseCurrent self ::temp19 lease        ;@line 215
						Cast ::temp22 ::temp19                                   ;@line 215
						JumpF ::temp22 _label388                                 ;@line 215
						Cast ::temp22 settled                                    ;@line 215
					_label388:
						JumpF ::temp22 _label389                                 ;@line 215
						Cast ::temp21 self                                       ;@line 216
						CallStatic netimmerse SetNodeLocalRotationMatrix ::temp19 ::temp21 ::YawNode_var rest False  ;@line 216
						Jump _label389                                           ;@line 216
					_label389:
						CallMethod PlayerLeaseCurrent self ::temp19 lease        ;@line 218
						Cast ::temp22 ::temp19                                   ;@line 218
						JumpF ::temp22 _label390                                 ;@line 218
						Cast ::temp22 settled                                    ;@line 218
					_label390:
						JumpF ::temp22 _label391                                 ;@line 218
						Cast ::temp21 self                                       ;@line 219
						CallStatic netimmerse SetNodeLocalRotationMatrix ::temp19 ::temp21 ::PitchNode_var rest False  ;@line 219
						Jump _label391                                           ;@line 219
					_label391:
						Assign sceneBusy False                                   ;@line 221
						CallMethod PlayerLeaseCurrent self ::temp19 lease        ;@line 222
						Not ::temp22 ::temp19                                    ;@line 222
						JumpF ::temp22 _label392                                 ;@line 222
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 223
						Return False                                             ;@line 224
						Jump _label392                                           ;@line 224
					_label392:
						Not ::temp19 settled                                     ;@line 226
						JumpF ::temp19 _label393                                 ;@line 226
						Return False                                             ;@line 227
						Jump _label393                                           ;@line 227
					_label393:
						Assign yaw 0.000000                                      ;@line 229
						Assign pitch 0.000000                                    ;@line 230
						Assign playerRestored True                               ;@line 231
						Jump _label381                                           ;@line 231
					_label381:
						Assign candidate ::Artillero_var                         ;@line 233
						CallStatic game GetPlayer ::temp25                       ;@line 234
						Assign player ::temp25                                   ;@line 234
						CallMethod PlayerLeaseCurrent self ::temp22 lease        ;@line 235
						Not ::temp19 ::temp22                                    ;@line 235
						Cast ::temp18 ::temp19                                   ;@line 235
						JumpT ::temp18 _label394                                 ;@line 235
						Cast ::temp18 pinBusy                                    ;@line 235
					_label394:
						Cast ::temp22 ::temp18                                   ;@line 235
						JumpT ::temp22 _label395                                 ;@line 235
						Cast ::temp22 sceneBusy                                  ;@line 235
					_label395:
						Cast ::temp18 ::temp22                                   ;@line 235
						JumpT ::temp18 _label396                                 ;@line 235
						CompareEQ ::temp19 candidate player                      ;@line 235
						Cast ::temp18 ::temp19                                   ;@line 235
					_label396:
						JumpF ::temp18 _label397                                 ;@line 235
						Return False                                             ;@line 236
						Jump _label397                                           ;@line 236
					_label397:
						Cast ::temp25 None                                       ;@line 238
						CompareEQ ::temp22 candidate ::temp25                    ;@line 238
						Not ::temp22 ::temp22                                    ;@line 238
						JumpF ::temp22 _label398                                 ;@line 238
						CallMethod IsDead candidate ::temp19                     ;@line 239
						Not ::temp18 ::temp19                                    ;@line 239
						Cast ::temp18 ::temp18                                   ;@line 239
						JumpF ::temp18 _label399                                 ;@line 239
						CallMethod IsDisabled candidate ::temp19                 ;@line 239
						Not ::temp19 ::temp19                                    ;@line 239
						Cast ::temp18 ::temp19                                   ;@line 239
					_label399:
						Cast ::temp18 ::temp18                                   ;@line 239
						JumpF ::temp18 _label400                                 ;@line 239
						CallMethod Is3DLoaded candidate ::temp19                 ;@line 239
						Cast ::temp18 ::temp19                                   ;@line 239
					_label400:
						Assign usable ::temp18                                   ;@line 239
						CallMethod PlayerLeaseCurrent self ::temp19 lease        ;@line 240
						Not ::temp18 ::temp19                                    ;@line 240
						Cast ::temp19 ::temp18                                   ;@line 240
						JumpT ::temp19 _label401                                 ;@line 240
						Cast ::temp19 pinBusy                                    ;@line 240
					_label401:
						Cast ::temp18 ::temp19                                   ;@line 240
						JumpT ::temp18 _label402                                 ;@line 240
						Cast ::temp18 sceneBusy                                  ;@line 240
					_label402:
						JumpF ::temp18 _label403                                 ;@line 240
						Return False                                             ;@line 241
						Jump _label403                                           ;@line 241
					_label403:
						JumpF usable _label404                                   ;@line 243
						Assign waitPoint ::Standby_var                           ;@line 244
						Cast ::temp21 None                                       ;@line 245
						CompareEQ ::temp19 waitPoint ::temp21                    ;@line 245
						JumpF ::temp19 _label405                                 ;@line 245
						Return False                                             ;@line 246
						Jump _label405                                           ;@line 246
					_label405:
						Assign pinBusy True                                      ;@line 248
						CallMethod MoveTo candidate ::NoneVar waitPoint 0.000000 0.000000 0.000000 True  ;@line 249
						CallMethod PlayerLeaseCurrent self ::temp18 lease        ;@line 250
						JumpF ::temp18 _label406                                 ;@line 250
						CallMethod SetDontMove candidate ::NoneVar True          ;@line 251
						Jump _label406                                           ;@line 251
					_label406:
						CallMethod PlayerLeaseCurrent self ::temp19 lease        ;@line 253
						Not ::temp18 ::temp19                                    ;@line 253
						JumpF ::temp18 _label407                                 ;@line 253
						CallMethod SetDontMove candidate ::NoneVar False         ;@line 256
						Assign pinBusy False                                     ;@line 257
						CallMethod QueueDeferredRecovery self ::NoneVar          ;@line 258
						Return False                                             ;@line 259
						Jump _label407                                           ;@line 259
					_label407:
						Assign ownedGuard candidate                              ;@line 261
						Assign pinBusy False                                     ;@line 262
						Jump _label404                                           ;@line 262
					_label404:
						Jump _label398                                           ;@line 262
					_label398:
						CallMethod PlayerLeaseCurrent self ::temp19 lease        ;@line 265
						Not ::temp18 ::temp19                                    ;@line 265
						Cast ::temp22 ::temp18                                   ;@line 265
						JumpT ::temp22 _label408                                 ;@line 265
						Cast ::temp22 pinBusy                                    ;@line 265
					_label408:
						Cast ::temp19 ::temp22                                   ;@line 265
						JumpT ::temp19 _label409                                 ;@line 265
						Cast ::temp19 sceneBusy                                  ;@line 265
					_label409:
						JumpF ::temp19 _label410                                 ;@line 265
						Return False                                             ;@line 266
						Jump _label410                                           ;@line 266
					_label410:
						Assign playerReady True                                  ;@line 268
						Return True                                              ;@line 269
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
						Cast ::temp54 playerReserved                             ;@line 595
						JumpT ::temp54 _label411                                 ;@line 595
						Cast ::temp54 pinBusy                                    ;@line 595
					_label411:
						Cast ::temp54 ::temp54                                   ;@line 595
						JumpT ::temp54 _label412                                 ;@line 595
						Cast ::temp54 sceneBusy                                  ;@line 595
					_label412:
						Cast ::temp54 ::temp54                                   ;@line 595
						JumpT ::temp54 _label413                                 ;@line 595
						Not ::temp55 recoveryRequested                           ;@line 595
						Cast ::temp54 ::temp55                                   ;@line 595
					_label413:
						Cast ::temp55 ::temp54                                   ;@line 595
						JumpT ::temp55 _label414                                 ;@line 595
						Cast ::temp55 destroyed                                  ;@line 595
					_label414:
						Cast ::temp54 ::temp55                                   ;@line 595
						JumpT ::temp54 _label415                                 ;@line 595
						Cast ::temp54 faulted                                    ;@line 595
					_label415:
						JumpF ::temp54 _label416                                 ;@line 595
						Return None                                              ;@line 596
						Jump _label416                                           ;@line 596
					_label416:
						Assign queueGeneration generation                        ;@line 598
						CallMethod Is3DLoaded self ::temp55                      ;@line 599
						Assign loaded ::temp55                                   ;@line 599
						CompareEQ ::temp54 generation queueGeneration            ;@line 600
						Not ::temp54 ::temp54                                    ;@line 600
						Cast ::temp55 ::temp54                                   ;@line 600
						JumpT ::temp55 _label417                                 ;@line 600
						Cast ::temp55 pinBusy                                    ;@line 600
					_label417:
						Cast ::temp54 ::temp55                                   ;@line 600
						JumpT ::temp54 _label418                                 ;@line 600
						Cast ::temp54 sceneBusy                                  ;@line 600
					_label418:
						Cast ::temp54 ::temp54                                   ;@line 600
						JumpT ::temp54 _label419                                 ;@line 600
						Not ::temp55 recoveryRequested                           ;@line 600
						Cast ::temp54 ::temp55                                   ;@line 600
					_label419:
						Cast ::temp55 ::temp54                                   ;@line 600
						JumpT ::temp55 _label420                                 ;@line 600
						Cast ::temp55 destroyed                                  ;@line 600
					_label420:
						Cast ::temp54 ::temp55                                   ;@line 600
						JumpT ::temp54 _label421                                 ;@line 600
						Cast ::temp54 faulted                                    ;@line 600
					_label421:
						JumpF ::temp54 _label422                                 ;@line 600
						Return None                                              ;@line 601
						Jump _label422                                           ;@line 601
					_label422:
						JumpF loaded _label423                                   ;@line 603
						CallMethod RegisterForSingleUpdate self ::NoneVar 0.200000  ;@line 604
						Jump _label423                                           ;@line 604
					_label423:
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
						.local ::temp111 Float
						.local ::temp112 Bool
						.local ::temp113 Float
						.local ::temp114 Bool
						.local difference Float
					.endLocalTable
					.code
						FSubtract ::temp111 goal value                           ;@line 904
						Assign difference ::temp111                              ;@line 904
						CompareGT ::temp112 difference maximumStep               ;@line 905
						JumpF ::temp112 _label424                                ;@line 905
						FAdd ::temp111 value maximumStep                         ;@line 906
						Return ::temp111                                         ;@line 906
						Jump _label425                                           ;@line 906
					_label424:
						FNegate ::temp113 maximumStep                            ;@line 907
						CompareLT ::temp114 difference ::temp113                 ;@line 907
						JumpF ::temp114 _label425                                ;@line 907
						FSubtract ::temp113 value maximumStep                    ;@line 908
						Return ::temp113                                         ;@line 908
						Jump _label425                                           ;@line 908
					_label425:
						Return goal                                              ;@line 910
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
						Cast ::temp64 sceneBusy                                  ;@line 660
						JumpT ::temp64 _label426                                 ;@line 660
						CallMethod Current self ::temp64 expectedGeneration expectedToken  ;@line 660
						Not ::temp64 ::temp64                                    ;@line 660
						Cast ::temp64 ::temp64                                   ;@line 660
					_label426:
						JumpF ::temp64 _label427                                 ;@line 660
						Return None                                              ;@line 661
						Jump _label427                                           ;@line 661
					_label427:
						Assign sceneBusy True                                    ;@line 663
						Cast ::temp65 self                                       ;@line 664
						CallStatic netimmerse SetNodeLocalRotationMatrix ::temp64 ::temp65 node matrix False  ;@line 664
						CallMethod FinishSceneEffect self ::temp64 expectedGeneration expectedToken  ;@line 665
					.endCode
				.endFunction
			.endState
		.endStateTable
	.endObject
.endObjectTable
