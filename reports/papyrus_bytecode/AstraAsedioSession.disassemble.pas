.info
	.source "AstraAsedioSession.psc"
	.modifyTime 1791137621 ;Sun Oct 04 15:13:41 2026 Local
	.compileTime 1791224422 ;Mon Oct 05 15:20:22 2026 Local
	.user "Facu2"
	.computer "DESKTOP-DF3S14S"
.endInfo
.userFlagsRef
	.flag hidden 0	; 0x00000000
	.flag conditional 1	; 0x00000001
.endUserFlagsRef
.objectTable
	.object AstraAsedioSession Quest
		.userFlags 0	; Flags: 0x00000000
		.docString ""
		.autoState 
		.variableTable
			.variable acquiredFighting Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable generation Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable changedPerspective Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable cleanupRequested Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable savedCamera Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue -1
			.endVariable
			.variable acquiring Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable acquiredCamSwitch Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable activeGun AstraAsedioActi
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable releasing Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable acquiredMovement Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
		.endVariableTable
		.propertyTable
		.endPropertyTable
		.stateTable
			.state 
				.function FinishCancelledAcquire
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp18 AstraAsedioActi
					.endLocalTable
					.code
						Assign acquiredMovement False                            ;@line 116
						Assign acquiredFighting False                            ;@line 117
						Assign acquiredCamSwitch False                           ;@line 118
						Assign savedCamera -1                                    ;@line 119
						Assign changedPerspective False                          ;@line 120
						Cast ::temp18 None                                       ;@line 121
						Assign activeGun ::temp18                                ;@line 121
						Assign cleanupRequested False                            ;@line 122
						Assign acquiring False                                   ;@line 124
					.endCode
				.endFunction
				.function IsCurrent
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param gun AstraAsedioActi
						.param token Int
					.endParamTable
					.localTable
						.local ::temp15 AstraAsedioActi
						.local ::temp16 Bool
						.local ::temp17 Bool
					.endLocalTable
					.code
						Cast ::temp15 None                                       ;@line 112
						CompareEQ ::temp16 gun ::temp15                          ;@line 112
						Not ::temp16 ::temp16                                    ;@line 112
						Cast ::temp16 ::temp16                                   ;@line 112
						JumpF ::temp16 _label0                                   ;@line 112
						Not ::temp17 acquiring                                   ;@line 112
						Cast ::temp16 ::temp17                                   ;@line 112
					_label0:
						Cast ::temp16 ::temp16                                   ;@line 112
						JumpF ::temp16 _label1                                   ;@line 112
						Not ::temp17 releasing                                   ;@line 112
						Cast ::temp16 ::temp17                                   ;@line 112
					_label1:
						Cast ::temp16 ::temp16                                   ;@line 112
						JumpF ::temp16 _label2                                   ;@line 112
						Not ::temp17 cleanupRequested                            ;@line 112
						Cast ::temp16 ::temp17                                   ;@line 112
					_label2:
						Cast ::temp16 ::temp16                                   ;@line 112
						JumpF ::temp16 _label3                                   ;@line 112
						CompareEQ ::temp17 activeGun gun                         ;@line 112
						Cast ::temp16 ::temp17                                   ;@line 112
					_label3:
						Cast ::temp16 ::temp16                                   ;@line 112
						JumpF ::temp16 _label4                                   ;@line 112
						CompareEQ ::temp17 generation token                      ;@line 112
						Cast ::temp16 ::temp17                                   ;@line 112
					_label4:
						Return ::temp16                                          ;@line 112
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
				.function OnInit
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp0 Bool
						.local ::temp1 String
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod IsRunning self ::temp0                        ;@line 15
						Cast ::temp1 ::temp0                                     ;@line 15
						StrCat ::temp1 "AstraAsedio session quest initialized running=" ::temp1  ;@line 15
						CallStatic debug Trace ::NoneVar ::temp1 0               ;@line 15
					.endCode
				.endFunction
				.function Release
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param gun AstraAsedioActi
						.param token Int
					.endParamTable
					.localTable
						.local ::temp19 Bool
						.local ::temp20 AstraAsedioActi
						.local ::temp21 Bool
						.local ::temp22 Bool
						.local ::NoneVar None
					.endLocalTable
					.code
						Cast ::temp19 acquiring                                  ;@line 128
						JumpF ::temp19 _label5                                   ;@line 128
						CompareEQ ::temp19 activeGun gun                         ;@line 128
						Cast ::temp19 ::temp19                                   ;@line 128
					_label5:
						Cast ::temp19 ::temp19                                   ;@line 128
						JumpF ::temp19 _label6                                   ;@line 128
						Cast ::temp20 None                                       ;@line 128
						CompareEQ ::temp21 gun ::temp20                          ;@line 128
						Not ::temp21 ::temp21                                    ;@line 128
						Cast ::temp19 ::temp21                                   ;@line 128
					_label6:
						Cast ::temp22 ::temp19                                   ;@line 128
						JumpF ::temp22 _label7                                   ;@line 128
						CompareLT ::temp21 token 0                               ;@line 128
						Cast ::temp21 ::temp21                                   ;@line 128
						JumpT ::temp21 _label8                                   ;@line 128
						CompareEQ ::temp22 token generation                      ;@line 128
						Cast ::temp21 ::temp22                                   ;@line 128
					_label8:
						Cast ::temp22 ::temp21                                   ;@line 128
					_label7:
						JumpF ::temp22 _label9                                   ;@line 128
						CallMethod RestoreControls self ::NoneVar                ;@line 129
						Return None                                              ;@line 130
						Jump _label9                                             ;@line 130
					_label9:
						CallMethod IsCurrent self ::temp19 gun token             ;@line 132
						Not ::temp21 ::temp19                                    ;@line 132
						JumpF ::temp21 _label10                                  ;@line 132
						Return None                                              ;@line 133
						Jump _label10                                            ;@line 133
					_label10:
						CallMethod RestoreControls self ::NoneVar                ;@line 135
					.endCode
				.endFunction
				.function restorePerspective
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param previousCamera Int
						.param restorePerspective Bool
					.endParamTable
					.localTable
						.local ::temp10 Bool
						.local ::temp11 Bool
						.local ::temp12 Bool
						.local ::temp13 actor
						.local ::temp14 Int
						.local operator actor
						.local ::NoneVar None
					.endLocalTable
					.code
						Not ::temp10 restorePerspective                          ;@line 97
						Cast ::temp12 ::temp10                                   ;@line 97
						JumpT ::temp12 _label11                                  ;@line 97
						CompareEQ ::temp11 previousCamera 8                      ;@line 97
						Not ::temp11 ::temp11                                    ;@line 97
						Cast ::temp11 ::temp11                                   ;@line 97
						JumpF ::temp11 _label12                                  ;@line 97
						CompareEQ ::temp12 previousCamera 9                      ;@line 97
						Not ::temp12 ::temp12                                    ;@line 97
						Cast ::temp11 ::temp12                                   ;@line 97
					_label12:
						Cast ::temp12 ::temp11                                   ;@line 97
					_label11:
						JumpF ::temp12 _label13                                  ;@line 97
						Return None                                              ;@line 98
						Jump _label13                                            ;@line 98
					_label13:
						CallStatic game GetPlayer ::temp13                       ;@line 100
						Assign operator ::temp13                                 ;@line 100
						Cast ::temp13 None                                       ;@line 101
						CompareEQ ::temp10 operator ::temp13                     ;@line 101
						Cast ::temp12 ::temp10                                   ;@line 101
						JumpT ::temp12 _label14                                  ;@line 101
						CallMethod IsDead operator ::temp11                      ;@line 101
						Cast ::temp12 ::temp11                                   ;@line 101
					_label14:
						Cast ::temp11 ::temp12                                   ;@line 101
						JumpT ::temp11 _label15                                  ;@line 101
						CallStatic utility IsInMenuMode ::temp10                 ;@line 101
						Cast ::temp11 ::temp10                                   ;@line 101
					_label15:
						JumpF ::temp11 _label16                                  ;@line 101
						Return None                                              ;@line 102
						Jump _label16                                            ;@line 102
					_label16:
						CallMethod ReadCameraState self ::temp14                 ;@line 106
						CompareEQ ::temp12 ::temp14 0                            ;@line 106
						JumpF ::temp12 _label17                                  ;@line 106
						CallStatic game ForceThirdPerson ::NoneVar               ;@line 107
						Jump _label17                                            ;@line 107
					_label17:
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
				.function EmergencyCleanup
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
						.local ::temp28 AstraAsedioActi
						.local ::temp29 Bool
						.local gun AstraAsedioActi
					.endLocalTable
					.code
						Assign gun activeGun                                     ;@line 178
						CallMethod RestoreControls self ::NoneVar                ;@line 179
						Cast ::temp28 None                                       ;@line 180
						CompareEQ ::temp29 gun ::temp28                          ;@line 180
						Not ::temp29 ::temp29                                    ;@line 180
						JumpF ::temp29 _label18                                  ;@line 180
						CallMethod EndSession gun ::NoneVar                      ;@line 181
						Jump _label18                                            ;@line 181
					_label18:
					.endCode
				.endFunction
				.function Acquire
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Int
					.paramTable
						.param gun AstraAsedioActi
					.endParamTable
					.localTable
						.local ::temp2 AstraAsedioActi
						.local ::temp3 Bool
						.local ::temp4 Bool
						.local ::temp5 Int
						.local ::temp6 Bool
						.local leaseGeneration Int
						.local questRunning Bool
						.local ::NoneVar None
						.local movementSnapshot Bool
						.local fightingSnapshot Bool
						.local camSwitchSnapshot Bool
						.local lookingSnapshot Bool
						.local cameraSnapshot Int
						.local currentCamera Int
					.endLocalTable
					.code
						Cast ::temp2 None                                        ;@line 19
						CompareEQ ::temp3 gun ::temp2                            ;@line 19
						JumpF ::temp3 _label19                                   ;@line 19
						Return -1                                                ;@line 20
						Jump _label19                                            ;@line 20
					_label19:
						Cast ::temp3 acquiring                                   ;@line 22
						JumpT ::temp3 _label20                                   ;@line 22
						Cast ::temp3 releasing                                   ;@line 22
					_label20:
						Cast ::temp3 ::temp3                                     ;@line 22
						JumpT ::temp3 _label21                                   ;@line 22
						Cast ::temp2 None                                        ;@line 22
						CompareEQ ::temp4 activeGun ::temp2                      ;@line 22
						Not ::temp4 ::temp4                                      ;@line 22
						Cast ::temp3 ::temp4                                     ;@line 22
					_label21:
						JumpF ::temp3 _label22                                   ;@line 22
						Return -1                                                ;@line 23
						Jump _label22                                            ;@line 23
					_label22:
						Assign acquiring True                                    ;@line 26
						Assign cleanupRequested False                            ;@line 27
						IAdd ::temp5 generation 1                                ;@line 28
						Assign generation ::temp5                                ;@line 28
						Assign leaseGeneration generation                        ;@line 29
						CallMethod IsRunning self ::temp4                        ;@line 30
						Assign questRunning ::temp4                              ;@line 30
						Not ::temp3 questRunning                                 ;@line 31
						Cast ::temp4 ::temp3                                     ;@line 31
						JumpT ::temp4 _label23                                   ;@line 31
						Cast ::temp4 cleanupRequested                            ;@line 31
					_label23:
						Cast ::temp4 ::temp4                                     ;@line 31
						JumpT ::temp4 _label24                                   ;@line 31
						CompareEQ ::temp3 generation leaseGeneration             ;@line 31
						Not ::temp3 ::temp3                                      ;@line 31
						Cast ::temp4 ::temp3                                     ;@line 31
					_label24:
						JumpF ::temp4 _label25                                   ;@line 31
						CallMethod FinishCancelledAcquire self ::NoneVar         ;@line 32
						Return -1                                                ;@line 33
						Jump _label25                                            ;@line 33
					_label25:
						Assign activeGun gun                                     ;@line 35
						CallStatic game IsMovementControlsEnabled ::temp3        ;@line 37
						Assign movementSnapshot ::temp3                          ;@line 37
						CallStatic game IsFightingControlsEnabled ::temp4        ;@line 38
						Assign fightingSnapshot ::temp4                          ;@line 38
						CallStatic game IsCamSwitchControlsEnabled ::temp3       ;@line 39
						Assign camSwitchSnapshot ::temp3                         ;@line 39
						CallStatic game IsLookingControlsEnabled ::temp4         ;@line 40
						Assign lookingSnapshot ::temp4                           ;@line 40
						CallMethod ReadCameraState self ::temp5                  ;@line 41
						Assign cameraSnapshot ::temp5                            ;@line 41
						Cast ::temp4 cleanupRequested                            ;@line 42
						JumpT ::temp4 _label26                                   ;@line 42
						CompareEQ ::temp3 generation leaseGeneration             ;@line 42
						Not ::temp3 ::temp3                                      ;@line 42
						Cast ::temp4 ::temp3                                     ;@line 42
					_label26:
						Cast ::temp4 ::temp4                                     ;@line 42
						JumpT ::temp4 _label27                                   ;@line 42
						CompareEQ ::temp3 activeGun gun                          ;@line 42
						Not ::temp3 ::temp3                                      ;@line 42
						Cast ::temp4 ::temp3                                     ;@line 42
					_label27:
						Cast ::temp4 ::temp4                                     ;@line 42
						JumpT ::temp4 _label28                                   ;@line 42
						Not ::temp3 lookingSnapshot                              ;@line 42
						Cast ::temp4 ::temp3                                     ;@line 42
					_label28:
						Cast ::temp6 ::temp4                                     ;@line 42
						JumpT ::temp6 _label29                                   ;@line 42
						CompareEQ ::temp3 cameraSnapshot 0                       ;@line 42
						Not ::temp3 ::temp3                                      ;@line 42
						Cast ::temp3 ::temp3                                     ;@line 42
						JumpF ::temp3 _label30                                   ;@line 42
						CompareEQ ::temp6 cameraSnapshot 8                       ;@line 42
						Not ::temp6 ::temp6                                      ;@line 42
						Cast ::temp3 ::temp6                                     ;@line 42
					_label30:
						Cast ::temp3 ::temp3                                     ;@line 42
						JumpF ::temp3 _label31                                   ;@line 42
						CompareEQ ::temp6 cameraSnapshot 9                       ;@line 42
						Not ::temp6 ::temp6                                      ;@line 42
						Cast ::temp3 ::temp6                                     ;@line 42
					_label31:
						Cast ::temp6 ::temp3                                     ;@line 42
					_label29:
						JumpF ::temp6 _label32                                   ;@line 42
						CallMethod FinishCancelledAcquire self ::NoneVar         ;@line 43
						Return -1                                                ;@line 44
						Jump _label32                                            ;@line 44
					_label32:
						Assign acquiredMovement movementSnapshot                 ;@line 46
						Assign acquiredFighting fightingSnapshot                 ;@line 47
						Assign acquiredCamSwitch camSwitchSnapshot               ;@line 48
						Assign savedCamera cameraSnapshot                        ;@line 49
						CallStatic game DisablePlayerControls ::NoneVar acquiredMovement acquiredFighting acquiredCamSwitch False False False False False 0  ;@line 51
						Cast ::temp3 cleanupRequested                            ;@line 53
						JumpT ::temp3 _label33                                   ;@line 53
						CompareEQ ::temp4 generation leaseGeneration             ;@line 53
						Not ::temp4 ::temp4                                      ;@line 53
						Cast ::temp3 ::temp4                                     ;@line 53
					_label33:
						Cast ::temp4 ::temp3                                     ;@line 53
						JumpT ::temp4 _label34                                   ;@line 53
						CompareEQ ::temp6 activeGun gun                          ;@line 53
						Not ::temp6 ::temp6                                      ;@line 53
						Cast ::temp4 ::temp6                                     ;@line 53
					_label34:
						JumpF ::temp4 _label35                                   ;@line 53
						CallMethod RollbackAcquire self ::NoneVar movementSnapshot fightingSnapshot camSwitchSnapshot cameraSnapshot False  ;@line 54
						Return -1                                                ;@line 55
						Jump _label35                                            ;@line 55
					_label35:
						CallMethod ReadCameraState self ::temp5                  ;@line 57
						Assign currentCamera ::temp5                             ;@line 57
						Cast ::temp6 cleanupRequested                            ;@line 58
						JumpT ::temp6 _label36                                   ;@line 58
						CompareEQ ::temp3 generation leaseGeneration             ;@line 58
						Not ::temp3 ::temp3                                      ;@line 58
						Cast ::temp6 ::temp3                                     ;@line 58
					_label36:
						Cast ::temp3 ::temp6                                     ;@line 58
						JumpT ::temp3 _label37                                   ;@line 58
						CompareEQ ::temp4 activeGun gun                          ;@line 58
						Not ::temp4 ::temp4                                      ;@line 58
						Cast ::temp3 ::temp4                                     ;@line 58
					_label37:
						Cast ::temp4 ::temp3                                     ;@line 58
						JumpT ::temp4 _label38                                   ;@line 58
						CompareEQ ::temp6 currentCamera 0                        ;@line 58
						Not ::temp6 ::temp6                                      ;@line 58
						Cast ::temp6 ::temp6                                     ;@line 58
						JumpF ::temp6 _label39                                   ;@line 58
						CompareEQ ::temp4 currentCamera 8                        ;@line 58
						Not ::temp4 ::temp4                                      ;@line 58
						Cast ::temp6 ::temp4                                     ;@line 58
					_label39:
						Cast ::temp6 ::temp6                                     ;@line 58
						JumpF ::temp6 _label40                                   ;@line 58
						CompareEQ ::temp4 currentCamera 9                        ;@line 58
						Not ::temp4 ::temp4                                      ;@line 58
						Cast ::temp6 ::temp4                                     ;@line 58
					_label40:
						Cast ::temp4 ::temp6                                     ;@line 58
					_label38:
						JumpF ::temp4 _label41                                   ;@line 58
						CallMethod RollbackAcquire self ::NoneVar movementSnapshot fightingSnapshot camSwitchSnapshot cameraSnapshot False  ;@line 59
						Return -1                                                ;@line 60
						Jump _label41                                            ;@line 60
					_label41:
						CompareEQ ::temp3 currentCamera 0                        ;@line 62
						Not ::temp3 ::temp3                                      ;@line 62
						JumpF ::temp3 _label42                                   ;@line 62
						CompareEQ ::temp6 cameraSnapshot 8                       ;@line 65
						Cast ::temp6 ::temp6                                     ;@line 65
						JumpT ::temp6 _label43                                   ;@line 65
						CompareEQ ::temp4 cameraSnapshot 9                       ;@line 65
						Cast ::temp6 ::temp4                                     ;@line 65
					_label43:
						Assign changedPerspective ::temp6                        ;@line 65
						CallStatic game ForceFirstPerson ::NoneVar               ;@line 66
						Jump _label42                                            ;@line 66
					_label42:
						Cast ::temp6 cleanupRequested                            ;@line 68
						JumpT ::temp6 _label44                                   ;@line 68
						CompareEQ ::temp4 generation leaseGeneration             ;@line 68
						Not ::temp4 ::temp4                                      ;@line 68
						Cast ::temp6 ::temp4                                     ;@line 68
					_label44:
						Cast ::temp4 ::temp6                                     ;@line 68
						JumpT ::temp4 _label45                                   ;@line 68
						CompareEQ ::temp3 activeGun gun                          ;@line 68
						Not ::temp3 ::temp3                                      ;@line 68
						Cast ::temp4 ::temp3                                     ;@line 68
					_label45:
						JumpF ::temp4 _label46                                   ;@line 68
						CallMethod RollbackAcquire self ::NoneVar movementSnapshot fightingSnapshot camSwitchSnapshot cameraSnapshot changedPerspective  ;@line 69
						Return -1                                                ;@line 70
						Jump _label46                                            ;@line 70
					_label46:
						Assign acquiring False                                   ;@line 72
						Return leaseGeneration                                   ;@line 73
					.endCode
				.endFunction
				.function RestoreControls
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp24 AstraAsedioActi
						.local ::temp25 Bool
						.local ::temp26 Bool
						.local ::NoneVar None
						.local ::temp23 Int
						.local restoreMovement Bool
						.local restoreFighting Bool
						.local restoreCamSwitch Bool
						.local previousCamera Int
						.local restorePerspective Bool
						.local oldGun AstraAsedioActi
						.local oldToken Int
						.local ::temp27 objectreference
					.endLocalTable
					.code
						JumpF acquiring _label47                                 ;@line 139
						Assign cleanupRequested True                             ;@line 141
						IAdd ::temp23 generation 1                               ;@line 142
						Assign generation ::temp23                               ;@line 142
						Return None                                              ;@line 143
						Jump _label47                                            ;@line 143
					_label47:
						JumpF releasing _label48                                 ;@line 145
						Return None                                              ;@line 146
						Jump _label48                                            ;@line 146
					_label48:
						Cast ::temp24 None                                       ;@line 148
						CompareEQ ::temp25 activeGun ::temp24                    ;@line 148
						Cast ::temp25 ::temp25                                   ;@line 148
						JumpF ::temp25 _label49                                  ;@line 148
						Not ::temp26 acquiredMovement                            ;@line 148
						Cast ::temp25 ::temp26                                   ;@line 148
					_label49:
						Cast ::temp25 ::temp25                                   ;@line 148
						JumpF ::temp25 _label50                                  ;@line 148
						Not ::temp26 acquiredFighting                            ;@line 148
						Cast ::temp25 ::temp26                                   ;@line 148
					_label50:
						Cast ::temp25 ::temp25                                   ;@line 148
						JumpF ::temp25 _label51                                  ;@line 148
						Not ::temp26 acquiredCamSwitch                           ;@line 148
						Cast ::temp25 ::temp26                                   ;@line 148
					_label51:
						Cast ::temp25 ::temp25                                   ;@line 148
						JumpF ::temp25 _label52                                  ;@line 148
						Not ::temp26 changedPerspective                          ;@line 148
						Cast ::temp25 ::temp26                                   ;@line 148
					_label52:
						JumpF ::temp25 _label53                                  ;@line 148
						Return None                                              ;@line 149
						Jump _label53                                            ;@line 149
					_label53:
						Assign releasing True                                    ;@line 151
						Assign restoreMovement acquiredMovement                  ;@line 152
						Assign restoreFighting acquiredFighting                  ;@line 153
						Assign restoreCamSwitch acquiredCamSwitch                ;@line 154
						Assign previousCamera savedCamera                        ;@line 155
						Assign restorePerspective changedPerspective             ;@line 156
						Assign oldGun activeGun                                  ;@line 157
						Assign oldToken generation                               ;@line 158
						Assign acquiredMovement False                            ;@line 159
						Assign acquiredFighting False                            ;@line 160
						Assign acquiredCamSwitch False                           ;@line 161
						Assign savedCamera -1                                    ;@line 162
						Assign changedPerspective False                          ;@line 163
						Cast ::temp24 None                                       ;@line 164
						Assign activeGun ::temp24                                ;@line 164
						IAdd ::temp23 generation 1                               ;@line 165
						Assign generation ::temp23                               ;@line 165
						Cast ::temp24 None                                       ;@line 168
						CompareEQ ::temp26 oldGun ::temp24                       ;@line 168
						Not ::temp26 ::temp26                                    ;@line 168
						Cast ::temp26 ::temp26                                   ;@line 168
						JumpF ::temp26 _label54                                  ;@line 168
						PropGet UseSightCamera oldGun ::temp25                   ;@line 168
						Cast ::temp26 ::temp25                                   ;@line 168
					_label54:
						Cast ::temp26 ::temp26                                   ;@line 168
						JumpF ::temp26 _label55                                  ;@line 168
						CallStatic skse GetPluginVersion ::temp23 "AstraSight"   ;@line 168
						CompareGTE ::temp25 ::temp23 1                           ;@line 168
						Cast ::temp26 ::temp25                                   ;@line 168
					_label55:
						JumpF ::temp26 _label56                                  ;@line 168
						Cast ::temp27 oldGun                                     ;@line 169
						CallStatic astrasightnative EndSight ::temp25 ::temp27 oldToken  ;@line 169
						Jump _label56                                            ;@line 169
					_label56:
						CallStatic game EnablePlayerControls ::NoneVar restoreMovement restoreFighting restoreCamSwitch False False False False False 0  ;@line 171
						CallMethod restorePerspective self ::NoneVar previousCamera restorePerspective  ;@line 172
						Assign releasing False                                   ;@line 174
					.endCode
				.endFunction
				.function RollbackAcquire
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param restoreMovement Bool
						.param restoreFighting Bool
						.param restoreCamSwitch Bool
						.param previousCamera Int
						.param restorePerspective Bool
					.endParamTable
					.localTable
						.local ::temp7 AstraAsedioActi
						.local ::NoneVar None
					.endLocalTable
					.code
						Assign acquiredMovement False                            ;@line 77
						Assign acquiredFighting False                            ;@line 78
						Assign acquiredCamSwitch False                           ;@line 79
						Assign changedPerspective False                          ;@line 80
						Assign savedCamera -1                                    ;@line 81
						Cast ::temp7 None                                        ;@line 82
						Assign activeGun ::temp7                                 ;@line 82
						CallStatic game EnablePlayerControls ::NoneVar restoreMovement restoreFighting restoreCamSwitch False False False False False 0  ;@line 83
						CallMethod restorePerspective self ::NoneVar previousCamera restorePerspective  ;@line 84
						CallMethod FinishCancelledAcquire self ::NoneVar         ;@line 85
					.endCode
				.endFunction
				.function ReadCameraState
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Int
					.paramTable
					.endParamTable
					.localTable
						.local ::temp8 Int
						.local ::temp9 Bool
					.endLocalTable
					.code
						CallStatic skse GetPluginVersion ::temp8 "AstraSight"    ;@line 90
						CompareLT ::temp9 ::temp8 33554432                       ;@line 90
						JumpF ::temp9 _label57                                   ;@line 90
						Return -1                                                ;@line 91
						Jump _label57                                            ;@line 91
					_label57:
						CallStatic astrasightnative GetCameraState ::temp8       ;@line 93
						Return ::temp8                                           ;@line 93
					.endCode
				.endFunction
			.endState
		.endStateTable
	.endObject
.endObjectTable
