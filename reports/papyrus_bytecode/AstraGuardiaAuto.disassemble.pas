.info
	.source "AstraGuardiaAuto.psc"
	.modifyTime 1791677332 ;Sat Oct 10 21:08:52 2026 Local
	.compileTime 1791679488 ;Sat Oct 10 21:44:48 2026 Local
	.user "AstraAsedio"
	.computer "Build"
.endInfo
.userFlagsRef
	.flag conditional 1	; 0x00000001
	.flag hidden 0	; 0x00000000
.endUserFlagsRef
.objectTable
	.object AstraGuardiaAuto ObjectReference
		.userFlags 0	; Flags: 0x00000000
		.docString ""
		.autoState 
		.variableTable
			.variable ::PitchSpeed_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 20.000000
			.endVariable
			.variable ::MuzzleAdelante_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue -224.000000
			.endVariable
			.variable yawActual Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::OcupadaGuardia_var globalvariable
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable blanco Actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable yPrev Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::AlcanceMin_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 900.000000
			.endVariable
			.variable ::ShotAmmo_var ammo
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable proximoIntento Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::GravedadProyectil_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 240.345001
			.endVariable
			.variable ::ShotSound_var sound
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable pitchActual Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::MargenImpacto_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 384.000000
			.endVariable
			.variable ::MargenLinea_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 320.000000
			.endVariable
			.variable ::QALog_var Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::AlcanceMax_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 8400.000000
			.endVariable
			.variable fase Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable xPrev Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::ReleaseSegundos_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.100000
			.endVariable
			.variable ::Enfriamiento_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 8.000000
			.endVariable
			.variable ::PitchNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "CTRL_ELEVACION"
			.endVariable
			.variable ::PitchMin_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue -5.000000
			.endVariable
			.variable ::ArcMax_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 60.000000
			.endVariable
			.variable rafaga Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable ::MaxRafaga_var Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 3
			.endVariable
			.variable hayPosPrev Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ultimoTick Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::PitchMax_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 80.000000
			.endVariable
			.variable ::VisualBoltNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "VIROTE_VISUAL"
			.endVariable
			.variable ::Anticipacion_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.500000
			.endVariable
			.variable guardia Actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::Launcher_var weapon
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable zPrev Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::MuzzleAlto_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 136.600006
			.endVariable
			.variable ::YawNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "CTRL_GIRO_360"
			.endVariable
			.variable ::YawSpeed_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 40.000000
			.endVariable
			.variable ::VelocidadProyectil_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 5400.000000
			.endVariable
			.variable ::TickSegundos_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.120000
			.endVariable
		.endVariableTable
		.propertyTable
			.property MuzzleAlto Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::MuzzleAlto_var
			.endProperty
			.property AlcanceMax Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::AlcanceMax_var
			.endProperty
			.property AlcanceMin Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::AlcanceMin_var
			.endProperty
			.property YawSpeed Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::YawSpeed_var
			.endProperty
			.property YawNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::YawNode_var
			.endProperty
			.property MuzzleAdelante Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::MuzzleAdelante_var
			.endProperty
			.property PitchSpeed Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchSpeed_var
			.endProperty
			.property ShotSound sound auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ShotSound_var
			.endProperty
			.property ArcMax Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ArcMax_var
			.endProperty
			.property ShotAmmo ammo auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ShotAmmo_var
			.endProperty
			.property PitchNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchNode_var
			.endProperty
			.property QALog Bool auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::QALog_var
			.endProperty
			.property TickSegundos Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::TickSegundos_var
			.endProperty
			.property GravedadProyectil Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::GravedadProyectil_var
			.endProperty
			.property MargenImpacto Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::MargenImpacto_var
			.endProperty
			.property ReleaseSegundos Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ReleaseSegundos_var
			.endProperty
			.property Anticipacion Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Anticipacion_var
			.endProperty
			.property OcupadaGuardia globalvariable auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::OcupadaGuardia_var
			.endProperty
			.property MargenLinea Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::MargenLinea_var
			.endProperty
			.property VelocidadProyectil Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::VelocidadProyectil_var
			.endProperty
			.property VisualBoltNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::VisualBoltNode_var
			.endProperty
			.property Enfriamiento Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Enfriamiento_var
			.endProperty
			.property PitchMin Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchMin_var
			.endProperty
			.property MaxRafaga Int auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::MaxRafaga_var
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
		.endPropertyTable
		.stateTable
			.state 
				.function FaseLiberacion
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp28 weapon
						.local ::temp29 Bool
						.local ::temp30 ammo
						.local ::temp31 Bool
						.local ::temp32 ObjectReference
						.local ::NoneVar None
						.local ::temp33 Int
					.endLocalTable
					.code
						Cast ::temp28 None                                       ;@line 303
						CompareEQ ::temp29 ::Launcher_var ::temp28               ;@line 303
						Cast ::temp29 ::temp29                                   ;@line 303
						JumpT ::temp29 _label0                                   ;@line 303
						Cast ::temp30 None                                       ;@line 303
						CompareEQ ::temp31 ::ShotAmmo_var ::temp30               ;@line 303
						Cast ::temp29 ::temp31                                   ;@line 303
					_label0:
						JumpF ::temp29 _label1                                   ;@line 303
						CallStatic debug Trace ::NoneVar "AstraGuardiaAuto PROPIEDADES_FALTAN: Launcher/ShotAmmo sin llenar (Â¿ESP sin regenerar?)" 0  ;@line 304
						Assign fase 0                                            ;@line 305
						Return None                                              ;@line 306
						Jump _label1                                             ;@line 306
					_label1:
						Cast ::temp32 self                                       ;@line 308
						CallMethod Fire ::Launcher_var ::NoneVar ::temp32 ::ShotAmmo_var  ;@line 308
						Cast ::temp32 self                                       ;@line 309
						CallStatic netimmerse SetNodeScale ::NoneVar ::temp32 ::VisualBoltNode_var 0.000000 False  ;@line 309
						JumpF ::ShotSound_var _label2                            ;@line 310
						Cast ::temp32 self                                       ;@line 311
						CallMethod Play ::ShotSound_var ::temp33 ::temp32        ;@line 311
						Jump _label2                                             ;@line 311
					_label2:
						IAdd ::temp33 rafaga 1                                   ;@line 313
						Assign rafaga ::temp33                                   ;@line 313
						Assign fase 5                                            ;@line 314
						CallMethod RegisterForSingleUpdate self ::NoneVar 0.050000  ;@line 319
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
				.function DormirSiCalma
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param ahora Float
					.endParamTable
					.localTable
						.local ::temp38 Actor
						.local ::temp39 Bool
						.local ::temp40 Bool
						.local ::temp41 Float
						.local ::NoneVar None
					.endLocalTable
					.code
						Cast ::temp38 None                                       ;@line 343
						CompareEQ ::temp39 guardia ::temp38                      ;@line 343
						Cast ::temp39 ::temp39                                   ;@line 343
						JumpT ::temp39 _label3                                   ;@line 343
						CallMethod IsInCombat guardia ::temp40                   ;@line 343
						Not ::temp40 ::temp40                                    ;@line 343
						Cast ::temp39 ::temp40                                   ;@line 343
					_label3:
						JumpF ::temp39 _label4                                   ;@line 343
						Assign fase 0                                            ;@line 344
						Cast ::temp38 None                                       ;@line 345
						Assign blanco ::temp38                                   ;@line 345
						Jump _label5                                             ;@line 345
					_label4:
						CompareLT ::temp40 ahora proximoIntento                  ;@line 346
						JumpF ::temp40 _label6                                   ;@line 346
						FSubtract ::temp41 proximoIntento ahora                  ;@line 347
						FAdd ::temp41 ::temp41 0.250000                          ;@line 347
						CallMethod RegisterForSingleUpdate self ::NoneVar ::temp41  ;@line 347
						Jump _label5                                             ;@line 347
					_label6:
						FAdd ::temp41 ahora 1.000000                             ;@line 349
						Assign proximoIntento ::temp41                           ;@line 349
						CallMethod RegisterForSingleUpdate self ::NoneVar 1.250000  ;@line 350
					_label5:
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
						.local ::temp0 ObjectReference
						.local ::temp1 Bool
						.local ::temp2 Actor
					.endLocalTable
					.code
						CallMethod Inicializar self ::NoneVar "OnLoad"           ;@line 90
						Cast ::temp0 self                                        ;@line 93
						CallStatic netimmerse SetNodeScale ::NoneVar ::temp0 ::VisualBoltNode_var 1.000000 False  ;@line 93
						Cast ::temp1 guardia                                     ;@line 94
						JumpF ::temp1 _label7                                    ;@line 94
						CallMethod IsInCombat guardia ::temp1                    ;@line 94
						Cast ::temp1 ::temp1                                     ;@line 94
					_label7:
						JumpF ::temp1 _label8                                    ;@line 94
						CallMethod GetCombatTarget guardia ::temp2               ;@line 95
						CallMethod AlertaCombat self ::NoneVar ::temp2           ;@line 95
						Jump _label8                                             ;@line 95
					_label8:
					.endCode
				.endFunction
				.function FaseRastreo
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param ahora Float
						.param dt Float
					.endParamTable
					.localTable
						.local ::NoneVar None
						.local ::temp21 String
						.local ::temp22 Bool
						.local ::temp23 Float[]
						.local ::temp24 Float
						.local ::temp25 Bool
						.local razon String
						.local sol Float[]
						.local solYaw Float
						.local solPitch Float
						.local dtSlew Float
						.local dyaw Float
						.local dpitch Float
						.local pasoYaw Float
						.local pasoPitch Float
					.endLocalTable
					.code
						CallMethod ElegirBlanco self ::NoneVar                   ;@line 228
						CallMethod ReglaEnganche self ::temp21                   ;@line 229
						Assign razon ::temp21                                    ;@line 229
						CompareEQ ::temp22 razon ""                              ;@line 230
						Not ::temp22 ::temp22                                    ;@line 230
						JumpF ::temp22 _label9                                   ;@line 230
						JumpF ::QALog_var _label10                               ;@line 231
						StrCat ::temp21 "AstraGuardiaAuto no engancha: " razon   ;@line 232
						CallStatic debug Trace ::NoneVar ::temp21 0              ;@line 232
						Jump _label10                                            ;@line 232
					_label10:
						CallMethod DormirSiCalma self ::NoneVar ahora            ;@line 234
						Return None                                              ;@line 235
						Jump _label9                                             ;@line 235
					_label9:
						ArrayCreate ::temp23 2                                   ;@line 237
						Assign sol ::temp23                                      ;@line 237
						CallMethod ResolverBlanco self ::temp22 dt sol           ;@line 238
						Not ::temp22 ::temp22                                    ;@line 238
						JumpF ::temp22 _label11                                  ;@line 238
						CallMethod DormirSiCalma self ::NoneVar ahora            ;@line 239
						Return None                                              ;@line 240
						Jump _label11                                            ;@line 240
					_label11:
						ArrayGetElement ::temp24 sol 0                           ;@line 242
						Assign solYaw ::temp24                                   ;@line 242
						ArrayGetElement ::temp24 sol 1                           ;@line 243
						Assign solPitch ::temp24                                 ;@line 243
						Assign dtSlew dt                                         ;@line 248
						CompareGT ::temp22 dtSlew ::TickSegundos_var             ;@line 249
						JumpF ::temp22 _label12                                  ;@line 249
						Assign dtSlew ::TickSegundos_var                         ;@line 250
						Jump _label12                                            ;@line 250
					_label12:
						FSubtract ::temp24 solYaw yawActual                      ;@line 252
						CallMethod Envolver self ::temp24 ::temp24               ;@line 252
						Assign dyaw ::temp24                                     ;@line 252
						FSubtract ::temp24 solPitch pitchActual                  ;@line 253
						Assign dpitch ::temp24                                   ;@line 253
						FMultiply ::temp24 ::YawSpeed_var dtSlew                 ;@line 254
						Assign pasoYaw ::temp24                                  ;@line 254
						FMultiply ::temp24 ::PitchSpeed_var dtSlew               ;@line 255
						Assign pasoPitch ::temp24                                ;@line 255
						CallStatic math Abs ::temp24 dyaw                        ;@line 256
						CompareLTE ::temp22 ::temp24 pasoYaw                     ;@line 256
						JumpF ::temp22 _label13                                  ;@line 256
						Assign yawActual solYaw                                  ;@line 257
						Jump _label14                                            ;@line 257
					_label13:
						CallMethod Signo self ::temp24 dyaw                      ;@line 259
						FMultiply ::temp24 pasoYaw ::temp24                      ;@line 259
						FAdd ::temp24 yawActual ::temp24                         ;@line 259
						Assign yawActual ::temp24                                ;@line 259
					_label14:
						CallStatic math Abs ::temp24 dpitch                      ;@line 261
						CompareLTE ::temp22 ::temp24 pasoPitch                   ;@line 261
						JumpF ::temp22 _label15                                  ;@line 261
						Assign pitchActual solPitch                              ;@line 262
						Jump _label16                                            ;@line 262
					_label15:
						CallMethod Signo self ::temp24 dpitch                    ;@line 264
						FMultiply ::temp24 pasoPitch ::temp24                    ;@line 264
						FAdd ::temp24 pitchActual ::temp24                       ;@line 264
						Assign pitchActual ::temp24                              ;@line 264
					_label16:
						CallMethod AplicarNodos self ::NoneVar                   ;@line 266
						FSubtract ::temp24 solYaw yawActual                      ;@line 267
						CallMethod Envolver self ::temp24 ::temp24               ;@line 267
						CallStatic math Abs ::temp24 ::temp24                    ;@line 267
						CompareLT ::temp22 ::temp24 1.500000                     ;@line 267
						Cast ::temp22 ::temp22                                   ;@line 267
						JumpF ::temp22 _label17                                  ;@line 267
						FSubtract ::temp24 solPitch pitchActual                  ;@line 267
						CallStatic math Abs ::temp24 ::temp24                    ;@line 267
						CompareLT ::temp25 ::temp24 1.500000                     ;@line 267
						Cast ::temp22 ::temp25                                   ;@line 267
					_label17:
						JumpF ::temp22 _label18                                  ;@line 267
						Assign fase 2                                            ;@line 272
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSegundos_var  ;@line 273
						Jump _label19                                            ;@line 273
					_label18:
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSegundos_var  ;@line 275
					_label19:
					.endCode
				.endFunction
				.function OnUpdate
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp15 Bool
						.local ::temp16 Bool
						.local ::temp17 Bool
						.local ::temp19 Actor
						.local ::temp20 Float
						.local ::NoneVar None
						.local ::temp18 ObjectReference
						.local ahora Float
						.local dt Float
					.endLocalTable
					.code
						CallMethod Ocupada self ::temp15                         ;@line 167
						JumpF ::temp15 _label20                                  ;@line 167
						CompareEQ ::temp16 fase 4                                ;@line 171
						JumpF ::temp16 _label21                                  ;@line 171
						CallMethod FaseLiberacion self ::NoneVar                 ;@line 174
						Jump _label21                                            ;@line 174
					_label21:
						CompareEQ ::temp16 fase 4                                ;@line 176
						Cast ::temp16 ::temp16                                   ;@line 176
						JumpT ::temp16 _label22                                  ;@line 176
						CompareEQ ::temp17 fase 5                                ;@line 176
						Cast ::temp16 ::temp17                                   ;@line 176
					_label22:
						JumpF ::temp16 _label23                                  ;@line 176
						CallMethod PlayGamebryoAnimation self ::temp17 "Reset" True 0.000000  ;@line 180
						Cast ::temp18 self                                       ;@line 181
						CallStatic netimmerse SetNodeScale ::NoneVar ::temp18 ::VisualBoltNode_var 1.000000 False  ;@line 181
						Jump _label23                                            ;@line 181
					_label23:
						Assign fase 0                                            ;@line 183
						Cast ::temp19 None                                       ;@line 184
						Assign blanco ::temp19                                   ;@line 184
						Assign hayPosPrev False                                  ;@line 185
						CallStatic utility GetCurrentRealTime ::temp20           ;@line 186
						FAdd ::temp20 ::temp20 8.000000                          ;@line 186
						Assign proximoIntento ::temp20                           ;@line 186
						Cast ::temp16 guardia                                    ;@line 187
						JumpF ::temp16 _label24                                  ;@line 187
						CallMethod IsInCombat guardia ::temp17                   ;@line 187
						Cast ::temp16 ::temp17                                   ;@line 187
					_label24:
						JumpF ::temp16 _label25                                  ;@line 187
						CallMethod RegisterForSingleUpdate self ::NoneVar 8.500000  ;@line 188
						Jump _label25                                            ;@line 188
					_label25:
						Return None                                              ;@line 190
						Jump _label20                                            ;@line 190
					_label20:
						CallStatic utility GetCurrentRealTime ::temp20           ;@line 192
						Assign ahora ::temp20                                    ;@line 192
						FSubtract ::temp20 ahora ultimoTick                      ;@line 193
						Assign dt ::temp20                                       ;@line 193
						CompareLT ::temp17 dt 0.000000                           ;@line 194
						JumpF ::temp17 _label26                                  ;@line 194
						Assign dt 0.000000                                       ;@line 195
						Jump _label26                                            ;@line 195
					_label26:
						Assign ultimoTick ahora                                  ;@line 197
						CompareEQ ::temp16 fase 0                                ;@line 198
						JumpF ::temp16 _label27                                  ;@line 198
						Cast ::temp17 guardia                                    ;@line 203
						JumpF ::temp17 _label28                                  ;@line 203
						CallMethod IsInCombat guardia ::temp15                   ;@line 203
						Cast ::temp17 ::temp15                                   ;@line 203
					_label28:
						Cast ::temp17 ::temp17                                   ;@line 203
						JumpF ::temp17 _label29                                  ;@line 203
						CompareGTE ::temp15 ahora proximoIntento                 ;@line 203
						Cast ::temp17 ::temp15                                   ;@line 203
					_label29:
						JumpF ::temp17 _label30                                  ;@line 203
						CallMethod GetCombatTarget guardia ::temp19              ;@line 204
						CallMethod AlertaCombat self ::NoneVar ::temp19          ;@line 204
						Jump _label30                                            ;@line 204
					_label30:
						Return None                                              ;@line 206
						Jump _label27                                            ;@line 206
					_label27:
						CompareEQ ::temp15 fase 1                                ;@line 208
						JumpF ::temp15 _label31                                  ;@line 208
						CallMethod FaseRastreo self ::NoneVar ahora dt           ;@line 209
						Jump _label32                                            ;@line 209
					_label31:
						CompareEQ ::temp17 fase 2                                ;@line 210
						JumpF ::temp17 _label33                                  ;@line 210
						Assign fase 3                                            ;@line 211
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSegundos_var  ;@line 212
						Jump _label32                                            ;@line 212
					_label33:
						CompareEQ ::temp16 fase 3                                ;@line 213
						JumpF ::temp16 _label34                                  ;@line 213
						CallMethod FaseFuego self ::NoneVar                      ;@line 214
						Jump _label32                                            ;@line 214
					_label34:
						CompareEQ ::temp17 fase 4                                ;@line 215
						JumpF ::temp17 _label35                                  ;@line 215
						CallMethod FaseLiberacion self ::NoneVar                 ;@line 216
						Jump _label32                                            ;@line 216
					_label35:
						CompareEQ ::temp16 fase 5                                ;@line 217
						JumpF ::temp16 _label36                                  ;@line 217
						CallMethod FaseRecarga self ::NoneVar                    ;@line 218
						Jump _label32                                            ;@line 218
					_label36:
						CompareEQ ::temp17 fase 6                                ;@line 219
						JumpF ::temp17 _label32                                  ;@line 219
						Assign rafaga 0                                          ;@line 220
						Assign fase 1                                            ;@line 221
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSegundos_var  ;@line 222
						Jump _label32                                            ;@line 222
					_label32:
					.endCode
				.endFunction
				.function ResetSegundos
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Float
					.paramTable
					.endParamTable
					.localTable
						.local ::temp84 Float
					.endLocalTable
					.code
						FAdd ::temp84 1.200000 ::TickSegundos_var                ;@line 613
						Return ::temp84                                          ;@line 613
					.endCode
				.endFunction
				.function CalmaCombat
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp12 Bool
						.local ::temp13 Bool
						.local ::temp14 Actor
						.local ::NoneVar None
					.endLocalTable
					.code
						CompareGT ::temp12 fase 0                                ;@line 154
						Cast ::temp12 ::temp12                                   ;@line 154
						JumpF ::temp12 _label37                                  ;@line 154
						CompareLT ::temp13 fase 3                                ;@line 154
						Cast ::temp12 ::temp13                                   ;@line 154
					_label37:
						JumpF ::temp12 _label38                                  ;@line 154
						Assign fase 0                                            ;@line 155
						Cast ::temp14 None                                       ;@line 156
						Assign blanco ::temp14                                   ;@line 156
						JumpF ::QALog_var _label39                               ;@line 157
						CallStatic debug Trace ::NoneVar "AstraGuardiaAuto a dormir: fin del combate del guardia" 0  ;@line 158
						Jump _label39                                            ;@line 158
					_label39:
						Jump _label38                                            ;@line 158
					_label38:
					.endCode
				.endFunction
				.function ElegirBlanco
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp42 Actor
						.local ::temp43 Bool
						.local ::temp45 Bool
						.local ::temp44 ObjectReference
						.local objetivo Actor
						.local ::temp46 String
						.local ::NoneVar None
					.endLocalTable
					.code
						Cast ::temp42 None                                       ;@line 358
						CompareEQ ::temp43 guardia ::temp42                      ;@line 358
						JumpF ::temp43 _label40                                  ;@line 358
						CallMethod GetLinkedRef self ::temp44 None               ;@line 359
						Cast ::temp42 ::temp44                                   ;@line 359
						Assign guardia ::temp42                                  ;@line 359
						Jump _label40                                            ;@line 359
					_label40:
						CallMethod GetCombatTarget guardia ::temp42              ;@line 361
						Assign objetivo ::temp42                                 ;@line 361
						Cast ::temp42 None                                       ;@line 362
						CompareEQ ::temp43 objetivo ::temp42                     ;@line 362
						Not ::temp43 ::temp43                                    ;@line 362
						Cast ::temp43 ::temp43                                   ;@line 362
						JumpF ::temp43 _label41                                  ;@line 362
						CompareEQ ::temp45 objetivo blanco                       ;@line 362
						Not ::temp45 ::temp45                                    ;@line 362
						Cast ::temp43 ::temp45                                   ;@line 362
					_label41:
						JumpF ::temp43 _label42                                  ;@line 362
						Assign blanco objetivo                                   ;@line 363
						Assign hayPosPrev False                                  ;@line 364
						JumpF ::QALog_var _label43                               ;@line 365
						Cast ::temp46 blanco                                     ;@line 366
						StrCat ::temp46 "AstraGuardiaAuto nuevo blanco del guardia: " ::temp46  ;@line 366
						CallStatic debug Trace ::NoneVar ::temp46 0              ;@line 366
						Jump _label43                                            ;@line 366
					_label43:
						Jump _label42                                            ;@line 366
					_label42:
						Cast ::temp42 None                                       ;@line 369
						CompareEQ ::temp45 blanco ::temp42                       ;@line 369
						Not ::temp45 ::temp45                                    ;@line 369
						Cast ::temp45 ::temp45                                   ;@line 369
						JumpF ::temp45 _label44                                  ;@line 369
						CallMethod IsDead blanco ::temp43                        ;@line 369
						Cast ::temp45 ::temp43                                   ;@line 369
					_label44:
						JumpF ::temp45 _label45                                  ;@line 369
						Assign blanco objetivo                                   ;@line 370
						Assign hayPosPrev False                                  ;@line 371
						Jump _label45                                            ;@line 371
					_label45:
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
						CallMethod Inicializar self ::NoneVar "OnInit"           ;@line 84
					.endCode
				.endFunction
				.function Inicializar
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param origen String
					.endParamTable
					.localTable
						.local ::temp4 ObjectReference
						.local ::temp5 Actor
						.local ::temp6 String
						.local ::temp7 String
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod GetLinkedRef self ::temp4 None                ;@line 112
						Cast ::temp5 ::temp4                                     ;@line 112
						Assign guardia ::temp5                                   ;@line 112
						JumpF ::QALog_var _label46                               ;@line 113
						StrCat ::temp6 "AstraGuardiaAuto " origen                ;@line 114
						StrCat ::temp6 ::temp6 " guardia="                       ;@line 114
						Cast ::temp7 guardia                                     ;@line 114
						StrCat ::temp7 ::temp6 ::temp7                           ;@line 114
						CallStatic debug Trace ::NoneVar ::temp7 0               ;@line 114
						Jump _label46                                            ;@line 114
					_label46:
						CallMethod LeerAnguloDeNodos self ::NoneVar              ;@line 116
						Assign fase 0                                            ;@line 117
						Assign rafaga 0                                          ;@line 118
						Assign proximoIntento 0.000000                           ;@line 119
					.endCode
				.endFunction
				.function LineaSegura
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param quien Actor
					.endParamTable
					.localTable
						.local ::temp53 Float
						.local ::temp54 Float
						.local ::temp55 Bool
						.local ::temp56 Bool
						.local ::temp57 ObjectReference
						.local ax Float
						.local ay Float
						.local bx Float
						.local by Float
						.local px Float
						.local py Float
						.local abx Float
						.local aby Float
						.local ab2 Float
						.local t Float
						.local cx Float
						.local cy Float
						.local dx Float
						.local dy Float
					.endLocalTable
					.code
						CallMethod GetPositionX self ::temp53                    ;@line 446
						Assign ax ::temp53                                       ;@line 446
						CallMethod GetPositionY self ::temp53                    ;@line 447
						Assign ay ::temp53                                       ;@line 447
						CallMethod GetPositionX blanco ::temp53                  ;@line 448
						Assign bx ::temp53                                       ;@line 448
						CallMethod GetPositionY blanco ::temp53                  ;@line 449
						Assign by ::temp53                                       ;@line 449
						CallMethod GetPositionX quien ::temp53                   ;@line 450
						Assign px ::temp53                                       ;@line 450
						CallMethod GetPositionY quien ::temp53                   ;@line 451
						Assign py ::temp53                                       ;@line 451
						FSubtract ::temp53 bx ax                                 ;@line 452
						Assign abx ::temp53                                      ;@line 452
						FSubtract ::temp53 by ay                                 ;@line 453
						Assign aby ::temp53                                      ;@line 453
						FMultiply ::temp53 abx abx                               ;@line 454
						FMultiply ::temp54 aby aby                               ;@line 454
						FAdd ::temp53 ::temp53 ::temp54                          ;@line 454
						Assign ab2 ::temp53                                      ;@line 454
						Assign t 0.000000                                        ;@line 455
						CompareGT ::temp55 ab2 0.000100                          ;@line 456
						JumpF ::temp55 _label47                                  ;@line 456
						FSubtract ::temp54 px ax                                 ;@line 457
						FMultiply ::temp53 ::temp54 abx                          ;@line 457
						FSubtract ::temp54 py ay                                 ;@line 457
						FMultiply ::temp54 ::temp54 aby                          ;@line 457
						FAdd ::temp53 ::temp53 ::temp54                          ;@line 457
						FDivide ::temp54 ::temp53 ab2                            ;@line 457
						Assign t ::temp54                                        ;@line 457
						Jump _label47                                            ;@line 457
					_label47:
						CompareLT ::temp55 t 0.000000                            ;@line 459
						JumpF ::temp55 _label48                                  ;@line 459
						Assign t 0.000000                                        ;@line 460
						Jump _label49                                            ;@line 460
					_label48:
						CompareGT ::temp56 t 1.000000                            ;@line 461
						JumpF ::temp56 _label49                                  ;@line 461
						Assign t 1.000000                                        ;@line 462
						Jump _label49                                            ;@line 462
					_label49:
						FMultiply ::temp53 abx t                                 ;@line 464
						FAdd ::temp54 ax ::temp53                                ;@line 464
						Assign cx ::temp54                                       ;@line 464
						FMultiply ::temp53 aby t                                 ;@line 465
						FAdd ::temp54 ay ::temp53                                ;@line 465
						Assign cy ::temp54                                       ;@line 465
						FSubtract ::temp53 px cx                                 ;@line 466
						Assign dx ::temp53                                       ;@line 466
						FSubtract ::temp54 py cy                                 ;@line 467
						Assign dy ::temp54                                       ;@line 467
						FMultiply ::temp53 dx dx                                 ;@line 468
						FMultiply ::temp54 dy dy                                 ;@line 468
						FAdd ::temp53 ::temp53 ::temp54                          ;@line 468
						CallStatic math Sqrt ::temp54 ::temp53                   ;@line 468
						CompareGT ::temp56 ::temp54 ::MargenLinea_var            ;@line 468
						Cast ::temp56 ::temp56                                   ;@line 468
						JumpF ::temp56 _label50                                  ;@line 468
						Cast ::temp57 blanco                                     ;@line 468
						CallMethod GetDistance quien ::temp53 ::temp57           ;@line 468
						CompareGT ::temp55 ::temp53 200.000000                   ;@line 468
						Cast ::temp56 ::temp55                                   ;@line 468
					_label50:
						Return ::temp56                                          ;@line 468
					.endCode
				.endFunction
				.function Ocupada
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
					.localTable
						.local ::temp79 globalvariable
						.local ::temp80 Bool
						.local ::temp81 Float
						.local ::temp82 Float
						.local ::temp83 Bool
					.endLocalTable
					.code
						Cast ::temp79 None                                       ;@line 608
						CompareEQ ::temp80 ::OcupadaGuardia_var ::temp79         ;@line 608
						Not ::temp80 ::temp80                                    ;@line 608
						Cast ::temp80 ::temp80                                   ;@line 608
						JumpF ::temp80 _label51                                  ;@line 608
						CallMethod GetValue ::OcupadaGuardia_var ::temp81        ;@line 608
						Cast ::temp82 1                                          ;@line 608
						CompareEQ ::temp83 ::temp81 ::temp82                     ;@line 608
						Cast ::temp80 ::temp83                                   ;@line 608
					_label51:
						Return ::temp80                                          ;@line 608
					.endCode
				.endFunction
				.function Envolver
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Float
					.paramTable
						.param angulo Float
					.endParamTable
					.localTable
						.local ::temp85 Bool
						.local ::temp86 Float
					.endLocalTable
					.code
					_label53:
						CompareGT ::temp85 angulo 180.000000                     ;@line 618
						JumpF ::temp85 _label52                                  ;@line 618
						FSubtract ::temp86 angulo 360.000000                     ;@line 619
						Assign angulo ::temp86                                   ;@line 619
						Jump _label53                                            ;@line 619
					_label52:
						CompareLTE ::temp85 angulo -180.000000                   ;@line 621
						JumpF ::temp85 _label54                                  ;@line 621
						FAdd ::temp86 angulo 360.000000                          ;@line 622
						Assign angulo ::temp86                                   ;@line 622
						Jump _label52                                            ;@line 622
					_label54:
						Return angulo                                            ;@line 624
					.endCode
				.endFunction
				.function Grados
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Float
					.paramTable
						.param rad Float
					.endParamTable
					.localTable
						.local ::temp88 Float
					.endLocalTable
					.code
						FMultiply ::temp88 rad 57.295780                         ;@line 635
						Return ::temp88                                          ;@line 635
					.endCode
				.endFunction
				.function ResolverBlanco
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
						.param dt Float
						.param sol Float[]
					.endParamTable
					.localTable
						.local ::temp58 Float
						.local ::temp59 Bool
						.local tx Float
						.local ty Float
						.local tz Float
						.local ::temp60 Bool
						.local ::temp61 Float
						.local ::temp62 Float
						.local vx Float
						.local vy Float
						.local vz Float
						.local dist Float
						.local tVuelo Float
						.local mx Float
						.local my Float
						.local mz Float
						.local dx Float
						.local dy Float
						.local d Float
						.local dzRel Float
						.local v2 Float
						.local disc Float
						.local ::NoneVar None
						.local tanP Float
						.local solPitch Float
						.local ::temp63 String
						.local ::temp64 String
					.endLocalTable
					.code
						CallMethod GetPositionX blanco ::temp58                  ;@line 484
						Assign tx ::temp58                                       ;@line 484
						CallMethod GetPositionY blanco ::temp58                  ;@line 485
						Assign ty ::temp58                                       ;@line 485
						CallMethod GetPositionZ blanco ::temp58                  ;@line 486
						Assign tz ::temp58                                       ;@line 486
						CompareGT ::temp59 ::Anticipacion_var 0.000000           ;@line 487
						JumpF ::temp59 _label55                                  ;@line 487
						Assign vx 0.000000                                       ;@line 488
						Assign vy 0.000000                                       ;@line 489
						Assign vz 0.000000                                       ;@line 490
						Cast ::temp60 hayPosPrev                                 ;@line 491
						JumpF ::temp60 _label56                                  ;@line 491
						CompareGT ::temp60 dt 0.016000                           ;@line 491
						Cast ::temp60 ::temp60                                   ;@line 491
					_label56:
						JumpF ::temp60 _label57                                  ;@line 491
						FSubtract ::temp58 tx xPrev                              ;@line 492
						FDivide ::temp58 ::temp58 dt                             ;@line 492
						Assign vx ::temp58                                       ;@line 492
						FSubtract ::temp58 ty yPrev                              ;@line 493
						FDivide ::temp58 ::temp58 dt                             ;@line 493
						Assign vy ::temp58                                       ;@line 493
						FSubtract ::temp58 tz zPrev                              ;@line 494
						FDivide ::temp58 ::temp58 dt                             ;@line 494
						Assign vz ::temp58                                       ;@line 494
						Jump _label57                                            ;@line 494
					_label57:
						Assign xPrev tx                                          ;@line 496
						Assign yPrev ty                                          ;@line 497
						Assign zPrev tz                                          ;@line 498
						Assign hayPosPrev True                                   ;@line 499
						CallMethod GetPositionX self ::temp58                    ;@line 500
						FSubtract ::temp58 tx ::temp58                           ;@line 500
						CallMethod GetPositionX self ::temp61                    ;@line 500
						FSubtract ::temp61 tx ::temp61                           ;@line 500
						FMultiply ::temp58 ::temp58 ::temp61                     ;@line 500
						CallMethod GetPositionY self ::temp61                    ;@line 500
						FSubtract ::temp61 ty ::temp61                           ;@line 500
						CallMethod GetPositionY self ::temp62                    ;@line 500
						FSubtract ::temp62 ty ::temp62                           ;@line 500
						FMultiply ::temp61 ::temp61 ::temp62                     ;@line 500
						FAdd ::temp62 ::temp58 ::temp61                          ;@line 500
						CallStatic math Sqrt ::temp58 ::temp62                   ;@line 500
						Assign dist ::temp58                                     ;@line 500
						FMultiply ::temp61 ::VelocidadProyectil_var 0.990000     ;@line 501
						FDivide ::temp62 dist ::temp61                           ;@line 501
						Assign tVuelo ::temp62                                   ;@line 501
						FMultiply ::temp58 vx tVuelo                             ;@line 502
						FMultiply ::temp61 ::temp58 ::Anticipacion_var           ;@line 502
						FAdd ::temp62 tx ::temp61                                ;@line 502
						Assign tx ::temp62                                       ;@line 502
						FMultiply ::temp58 vy tVuelo                             ;@line 503
						FMultiply ::temp61 ::temp58 ::Anticipacion_var           ;@line 503
						FAdd ::temp62 ty ::temp61                                ;@line 503
						Assign ty ::temp62                                       ;@line 503
						FMultiply ::temp58 vz tVuelo                             ;@line 504
						FMultiply ::temp61 ::temp58 ::Anticipacion_var           ;@line 504
						FAdd ::temp62 tz ::temp61                                ;@line 504
						Assign tz ::temp62                                       ;@line 504
						Jump _label55                                            ;@line 504
					_label55:
						CallMethod GetPositionX self ::temp58                    ;@line 508
						Assign mx ::temp58                                       ;@line 508
						CallMethod GetPositionY self ::temp61                    ;@line 509
						FAdd ::temp62 ::temp61 ::MuzzleAdelante_var              ;@line 509
						Assign my ::temp62                                       ;@line 509
						CallMethod GetPositionZ self ::temp58                    ;@line 510
						FAdd ::temp61 ::temp58 ::MuzzleAlto_var                  ;@line 510
						Assign mz ::temp61                                       ;@line 510
						FSubtract ::temp62 tx mx                                 ;@line 511
						Assign dx ::temp62                                       ;@line 511
						FSubtract ::temp58 ty my                                 ;@line 512
						Assign dy ::temp58                                       ;@line 512
						FMultiply ::temp61 dx dx                                 ;@line 513
						FMultiply ::temp62 dy dy                                 ;@line 513
						FAdd ::temp58 ::temp61 ::temp62                          ;@line 513
						CallStatic math Sqrt ::temp61 ::temp58                   ;@line 513
						Assign d ::temp61                                        ;@line 513
						CompareLT ::temp60 d 1.000000                            ;@line 514
						JumpF ::temp60 _label58                                  ;@line 514
						Return False                                             ;@line 515
						Jump _label58                                            ;@line 515
					_label58:
						FSubtract ::temp62 tz mz                                 ;@line 525
						Assign dzRel ::temp62                                    ;@line 525
						FMultiply ::temp58 ::VelocidadProyectil_var ::VelocidadProyectil_var  ;@line 526
						Assign v2 ::temp58                                       ;@line 526
						FMultiply ::temp61 v2 v2                                 ;@line 527
						FMultiply ::temp62 ::GravedadProyectil_var d             ;@line 527
						FMultiply ::temp58 ::temp62 d                            ;@line 527
						FMultiply ::temp62 2.000000 dzRel                        ;@line 527
						FMultiply ::temp62 ::temp62 v2                           ;@line 527
						FAdd ::temp58 ::temp58 ::temp62                          ;@line 527
						FMultiply ::temp62 ::GravedadProyectil_var ::temp58      ;@line 527
						FSubtract ::temp58 ::temp61 ::temp62                     ;@line 527
						Assign disc ::temp58                                     ;@line 527
						CompareLT ::temp59 disc 0.000000                         ;@line 528
						JumpF ::temp59 _label59                                  ;@line 528
						JumpF ::QALog_var _label60                               ;@line 529
						CallStatic debug Trace ::NoneVar "AstraGuardiaAuto fuera de alcance balÃ­stico" 0  ;@line 530
						Jump _label60                                            ;@line 530
					_label60:
						Return False                                             ;@line 532
						Jump _label59                                            ;@line 532
					_label59:
						CallStatic math Sqrt ::temp61 disc                       ;@line 534
						FSubtract ::temp62 v2 ::temp61                           ;@line 534
						FMultiply ::temp58 ::GravedadProyectil_var d             ;@line 534
						FDivide ::temp61 ::temp62 ::temp58                       ;@line 534
						Assign tanP ::temp61                                     ;@line 534
						CallStatic math Atan ::temp62 tanP                       ;@line 535
						CallMethod Grados self ::temp58 ::temp62                 ;@line 535
						Assign solPitch ::temp58                                 ;@line 535
						CompareLT ::temp60 solPitch ::PitchMin_var               ;@line 536
						Cast ::temp60 ::temp60                                   ;@line 536
						JumpT ::temp60 _label61                                  ;@line 536
						CompareGT ::temp59 solPitch ::PitchMax_var               ;@line 536
						Cast ::temp60 ::temp59                                   ;@line 536
					_label61:
						JumpF ::temp60 _label62                                  ;@line 536
						JumpF ::QALog_var _label63                               ;@line 537
						Cast ::temp63 solPitch                                   ;@line 538
						StrCat ::temp63 "AstraGuardiaAuto elevaciÃ³n " ::temp63  ;@line 538
						StrCat ::temp63 ::temp63 " fuera de ("                   ;@line 538
						Cast ::temp64 ::PitchMin_var                             ;@line 538
						StrCat ::temp64 ::temp63 ::temp64                        ;@line 538
						StrCat ::temp63 ::temp64 ", "                            ;@line 538
						Cast ::temp64 ::PitchMax_var                             ;@line 538
						StrCat ::temp64 ::temp63 ::temp64                        ;@line 538
						StrCat ::temp63 ::temp64 ")"                             ;@line 538
						CallStatic debug Trace ::NoneVar ::temp63 0              ;@line 538
						Jump _label63                                            ;@line 538
					_label63:
						Return False                                             ;@line 540
						Jump _label62                                            ;@line 540
					_label62:
						FNegate ::temp62 dy                                      ;@line 544
						CallMethod Atan2 self ::temp58 dx ::temp62               ;@line 544
						CallMethod Grados self ::temp62 ::temp58                 ;@line 544
						Assign ::temp61 ::temp62                                 ;@line 544
						ArraySetElement sol 0 ::temp61                           ;@line 544
						Assign ::temp58 solPitch                                 ;@line 545
						ArraySetElement sol 1 ::temp58                           ;@line 545
						Return True                                              ;@line 546
					.endCode
				.endFunction
				.function ReglaEnganche
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return String
					.paramTable
					.endParamTable
					.localTable
						.local ::temp47 Actor
						.local ::temp48 Bool
						.local ::temp49 Bool
						.local ::temp50 ObjectReference
						.local ::temp51 Float
						.local ::temp52 Float
						.local jugador Actor
						.local dx Float
						.local dy Float
						.local dist Float
						.local rumbo Float
					.endLocalTable
					.code
						Cast ::temp47 None                                       ;@line 376
						CompareEQ ::temp48 blanco ::temp47                       ;@line 376
						JumpF ::temp48 _label64                                  ;@line 376
						Return "SIN_BLANCO"                                      ;@line 377
						Jump _label64                                            ;@line 377
					_label64:
						CallMethod IsDead blanco ::temp48                        ;@line 379
						JumpF ::temp48 _label65                                  ;@line 379
						Return "BLANCO_MUERTO"                                   ;@line 380
						Jump _label65                                            ;@line 380
					_label65:
						CallStatic game GetPlayer ::temp47                       ;@line 382
						Assign jugador ::temp47                                  ;@line 382
						CompareEQ ::temp48 blanco jugador                        ;@line 387
						JumpF ::temp48 _label66                                  ;@line 387
						Return "BLANCO_JUGADOR"                                  ;@line 388
						Jump _label66                                            ;@line 388
					_label66:
						CallMethod IsHostileToActor blanco ::temp48 jugador      ;@line 392
						Not ::temp48 ::temp48                                    ;@line 392
						Cast ::temp48 ::temp48                                   ;@line 392
						JumpF ::temp48 _label67                                  ;@line 392
						Cast ::temp49 guardia                                    ;@line 392
						JumpF ::temp49 _label68                                  ;@line 392
						CallMethod IsHostileToActor blanco ::temp49 guardia      ;@line 392
						Cast ::temp49 ::temp49                                   ;@line 392
					_label68:
						Not ::temp49 ::temp49                                    ;@line 392
						Cast ::temp48 ::temp49                                   ;@line 392
					_label67:
						JumpF ::temp48 _label69                                  ;@line 392
						Return "NO_HOSTIL"                                       ;@line 393
						Jump _label69                                            ;@line 393
					_label69:
						Cast ::temp48 guardia                                    ;@line 398
						JumpF ::temp48 _label70                                  ;@line 398
						CallMethod IsDead guardia ::temp49                       ;@line 398
						Cast ::temp48 ::temp49                                   ;@line 398
					_label70:
						JumpF ::temp48 _label71                                  ;@line 398
						Cast ::temp47 None                                       ;@line 399
						Assign guardia ::temp47                                  ;@line 399
						Jump _label71                                            ;@line 399
					_label71:
						JumpF guardia _label72                                   ;@line 401
						CallMethod IsDetectedBy blanco ::temp49 guardia          ;@line 402
						Not ::temp48 ::temp49                                    ;@line 402
						JumpF ::temp48 _label73                                  ;@line 402
						Return "SIN_LINEA_GUARDIA"                               ;@line 403
						Jump _label73                                            ;@line 403
					_label73:
						Jump _label74                                            ;@line 403
					_label72:
						Cast ::temp50 self                                       ;@line 405
						CallMethod GetDistance blanco ::temp51 ::temp50          ;@line 405
						CompareGT ::temp49 ::temp51 4000.000000                  ;@line 405
						JumpF ::temp49 _label74                                  ;@line 405
						Return "SIN_GUARDIA_LEJOS"                               ;@line 406
						Jump _label74                                            ;@line 406
					_label74:
						CallMethod GetPositionX blanco ::temp51                  ;@line 408
						CallMethod GetPositionX self ::temp52                    ;@line 408
						FSubtract ::temp51 ::temp51 ::temp52                     ;@line 408
						Assign dx ::temp51                                       ;@line 408
						CallMethod GetPositionY blanco ::temp52                  ;@line 409
						CallMethod GetPositionY self ::temp51                    ;@line 409
						FSubtract ::temp52 ::temp52 ::temp51                     ;@line 409
						Assign dy ::temp52                                       ;@line 409
						FMultiply ::temp51 dx dx                                 ;@line 410
						FMultiply ::temp52 dy dy                                 ;@line 410
						FAdd ::temp51 ::temp51 ::temp52                          ;@line 410
						CallStatic math Sqrt ::temp52 ::temp51                   ;@line 410
						Assign dist ::temp52                                     ;@line 410
						CompareLT ::temp48 dist ::AlcanceMin_var                 ;@line 411
						JumpF ::temp48 _label75                                  ;@line 411
						Return "DEMASIADO_CERCA"                                 ;@line 412
						Jump _label75                                            ;@line 412
					_label75:
						CompareGT ::temp49 dist ::AlcanceMax_var                 ;@line 414
						JumpF ::temp49 _label76                                  ;@line 414
						Return "DEMASIADO_LEJOS"                                 ;@line 415
						Jump _label76                                            ;@line 415
					_label76:
						FNegate ::temp51 dy                                      ;@line 419
						CallMethod Atan2 self ::temp52 dx ::temp51               ;@line 419
						CallMethod Grados self ::temp51 ::temp52                 ;@line 419
						CallMethod Envolver self ::temp52 ::temp51               ;@line 419
						CallStatic math Abs ::temp51 ::temp52                    ;@line 419
						Assign rumbo ::temp51                                    ;@line 419
						CompareGT ::temp48 rumbo ::ArcMax_var                    ;@line 420
						JumpF ::temp48 _label77                                  ;@line 420
						Return "FUERA_DE_ARCO"                                   ;@line 421
						Jump _label77                                            ;@line 421
					_label77:
						CallMethod LineaSegura self ::temp49 jugador             ;@line 425
						Not ::temp48 ::temp49                                    ;@line 425
						JumpF ::temp48 _label78                                  ;@line 425
						Return "JUGADOR_EN_LINEA"                                ;@line 426
						Jump _label78                                            ;@line 426
					_label78:
						Cast ::temp49 guardia                                    ;@line 428
						JumpF ::temp49 _label79                                  ;@line 428
						CallMethod LineaSegura self ::temp49 guardia             ;@line 428
						Not ::temp48 ::temp49                                    ;@line 428
						Cast ::temp49 ::temp48                                   ;@line 428
					_label79:
						JumpF ::temp49 _label80                                  ;@line 428
						Return "GUARDIA_EN_LINEA"                                ;@line 429
						Jump _label80                                            ;@line 429
					_label80:
						Cast ::temp50 blanco                                     ;@line 431
						CallMethod GetDistance jugador ::temp52 ::temp50         ;@line 431
						CompareLT ::temp48 ::temp52 ::MargenImpacto_var          ;@line 431
						JumpF ::temp48 _label81                                  ;@line 431
						Return "JUGADOR_CERCA_DEL_BLANCO"                        ;@line 432
						Jump _label81                                            ;@line 432
					_label81:
						Cast ::temp48 guardia                                    ;@line 434
						JumpF ::temp48 _label82                                  ;@line 434
						Cast ::temp50 blanco                                     ;@line 434
						CallMethod GetDistance guardia ::temp51 ::temp50         ;@line 434
						CompareLT ::temp49 ::temp51 ::MargenImpacto_var          ;@line 434
						Cast ::temp48 ::temp49                                   ;@line 434
					_label82:
						JumpF ::temp48 _label83                                  ;@line 434
						Return "GUARDIA_CERCA_DEL_BLANCO"                        ;@line 435
						Jump _label83                                            ;@line 435
					_label83:
						Return ""                                                ;@line 437
					.endCode
				.endFunction
				.function Signo
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Float
					.paramTable
						.param v Float
					.endParamTable
					.localTable
						.local ::temp87 Bool
					.endLocalTable
					.code
						CompareLT ::temp87 v 0.000000                            ;@line 628
						JumpF ::temp87 _label84                                  ;@line 628
						Return -1.000000                                         ;@line 629
						Jump _label84                                            ;@line 629
					_label84:
						Return 1.000000                                          ;@line 631
					.endCode
				.endFunction
				.function OnCellDetach
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp3 Actor
						.local ::NoneVar None
					.endLocalTable
					.code
						Assign fase 0                                            ;@line 103
						Cast ::temp3 None                                        ;@line 104
						Assign blanco ::temp3                                    ;@line 104
						Assign hayPosPrev False                                  ;@line 105
						JumpF ::QALog_var _label85                               ;@line 106
						CallStatic debug Trace ::NoneVar "AstraGuardiaAuto OnCellDetach: torre dormida" 0  ;@line 107
						Jump _label85                                            ;@line 107
					_label85:
					.endCode
				.endFunction
				.function LeerAnguloDeNodos
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp70 Float[]
						.local ::temp71 ObjectReference
						.local ::temp72 Bool
						.local ::temp73 Int
						.local ::temp74 Bool
						.local m Float[]
						.local ::temp75 Float
						.local ::temp76 Float
						.local ::temp77 String
						.local ::temp78 String
						.local ::NoneVar None
					.endLocalTable
					.code
						ArrayCreate ::temp70 9                                   ;@line 587
						Assign m ::temp70                                        ;@line 587
						Cast ::temp71 self                                       ;@line 588
						CallStatic netimmerse GetNodeLocalRotationMatrix ::temp72 ::temp71 ::YawNode_var m False  ;@line 588
						Cast ::temp72 ::temp72                                   ;@line 588
						JumpF ::temp72 _label86                                  ;@line 588
						ArrayLength ::temp73 m                                   ;@line 588
						CompareEQ ::temp74 ::temp73 9                            ;@line 588
						Cast ::temp72 ::temp74                                   ;@line 588
					_label86:
						JumpF ::temp72 _label87                                  ;@line 588
						ArrayGetElement ::temp75 m 3                             ;@line 591
						ArrayGetElement ::temp76 m 0                             ;@line 591
						CallMethod Atan2 self ::temp75 ::temp75 ::temp76         ;@line 591
						CallMethod Grados self ::temp76 ::temp75                 ;@line 591
						Assign yawActual ::temp76                                ;@line 591
						Jump _label87                                            ;@line 591
					_label87:
						Cast ::temp71 self                                       ;@line 593
						CallStatic netimmerse GetNodeLocalRotationMatrix ::temp74 ::temp71 ::PitchNode_var m False  ;@line 593
						Cast ::temp74 ::temp74                                   ;@line 593
						JumpF ::temp74 _label88                                  ;@line 593
						ArrayLength ::temp73 m                                   ;@line 593
						CompareEQ ::temp72 ::temp73 9                            ;@line 593
						Cast ::temp74 ::temp72                                   ;@line 593
					_label88:
						JumpF ::temp74 _label89                                  ;@line 593
						ArrayGetElement ::temp75 m 5                             ;@line 597
						ArrayGetElement ::temp76 m 4                             ;@line 597
						CallMethod Atan2 self ::temp75 ::temp75 ::temp76         ;@line 597
						CallMethod Grados self ::temp76 ::temp75                 ;@line 597
						Assign pitchActual ::temp76                              ;@line 597
						Jump _label89                                            ;@line 597
					_label89:
						JumpF ::QALog_var _label90                               ;@line 599
						Cast ::temp77 yawActual                                  ;@line 600
						StrCat ::temp77 "AstraGuardiaAuto Ã¡ngulos de nodo: yaw=" ::temp77  ;@line 600
						StrCat ::temp77 ::temp77 " pitch="                       ;@line 600
						Cast ::temp78 pitchActual                                ;@line 600
						StrCat ::temp78 ::temp77 ::temp78                        ;@line 600
						CallStatic debug Trace ::NoneVar ::temp78 0              ;@line 600
						Jump _label90                                            ;@line 600
					_label90:
					.endCode
				.endFunction
				.function Atan2
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Float
					.paramTable
						.param dy Float
						.param dx Float
					.endParamTable
					.localTable
						.local ::temp90 Bool
						.local ::temp92 Bool
						.local ::temp91 Float
						.local ::temp93 Bool
						.local ::temp94 Float
						.local ::temp95 Float
					.endLocalTable
					.code
						CompareGT ::temp90 dx 0.000000                           ;@line 644
						JumpF ::temp90 _label91                                  ;@line 644
						FDivide ::temp91 dy dx                                   ;@line 645
						CallStatic math Atan ::temp91 ::temp91                   ;@line 645
						Return ::temp91                                          ;@line 645
						Jump _label92                                            ;@line 645
					_label91:
						CompareLT ::temp92 dx 0.000000                           ;@line 646
						JumpF ::temp92 _label93                                  ;@line 646
						CompareGTE ::temp93 dy 0.000000                          ;@line 647
						JumpF ::temp93 _label94                                  ;@line 647
						FDivide ::temp94 dy dx                                   ;@line 648
						CallStatic math Atan ::temp94 ::temp94                   ;@line 648
						FAdd ::temp94 ::temp94 3.141593                          ;@line 648
						Return ::temp94                                          ;@line 648
						Jump _label95                                            ;@line 648
					_label94:
						FDivide ::temp95 dy dx                                   ;@line 650
						CallStatic math Atan ::temp95 ::temp95                   ;@line 650
						FSubtract ::temp95 ::temp95 3.141593                     ;@line 650
						Return ::temp95                                          ;@line 650
					_label95:
						Jump _label92                                            ;@line 650
					_label93:
						CompareGTE ::temp93 dy 0.000000                          ;@line 652
						JumpF ::temp93 _label96                                  ;@line 652
						Return 1.570796                                          ;@line 653
						Jump _label92                                            ;@line 653
					_label96:
						Return -1.570796                                         ;@line 655
					_label92:
					.endCode
				.endFunction
				.function FaseFuego
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp26 String
						.local ::temp27 Bool
						.local razon String
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod ReglaEnganche self ::temp26                   ;@line 280
						Assign razon ::temp26                                    ;@line 280
						CompareEQ ::temp27 razon ""                              ;@line 281
						Not ::temp27 ::temp27                                    ;@line 281
						JumpF ::temp27 _label97                                  ;@line 281
						JumpF ::QALog_var _label98                               ;@line 282
						StrCat ::temp26 "AstraGuardiaAuto disparo abortado: " razon  ;@line 283
						CallStatic debug Trace ::NoneVar ::temp26 0              ;@line 283
						Jump _label98                                            ;@line 283
					_label98:
						Assign fase 1                                            ;@line 285
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSegundos_var  ;@line 286
						Return None                                              ;@line 287
						Jump _label97                                            ;@line 287
					_label97:
						CallMethod PlayGamebryoAnimation self ::temp27 "Fire" True 0.000000  ;@line 289
						Not ::temp27 ::temp27                                    ;@line 289
						JumpF ::temp27 _label99                                  ;@line 289
						CallStatic debug Trace ::NoneVar "AstraGuardiaAuto FIRE_ANIMATION_FAILED" 0  ;@line 290
						Assign fase 1                                            ;@line 291
						CallMethod RegisterForSingleUpdate self ::NoneVar 1.000000  ;@line 292
						Return None                                              ;@line 293
						Jump _label99                                            ;@line 293
					_label99:
						Assign fase 4                                            ;@line 295
						CallMethod RegisterForSingleUpdate self ::NoneVar ::ReleaseSegundos_var  ;@line 296
					.endCode
				.endFunction
				.function FaseRecarga
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp34 Bool
						.local ::temp35 ObjectReference
						.local ::NoneVar None
						.local ::temp36 String
						.local ::temp37 Float
					.endLocalTable
					.code
						CallMethod PlayGamebryoAnimation self ::temp34 "Reset" True 0.000000  ;@line 328
						Cast ::temp35 self                                       ;@line 329
						CallStatic netimmerse SetNodeScale ::NoneVar ::temp35 ::VisualBoltNode_var 1.000000 False  ;@line 329
						CompareGTE ::temp34 rafaga ::MaxRafaga_var               ;@line 330
						JumpF ::temp34 _label100                                 ;@line 330
						Assign fase 6                                            ;@line 331
						CallMethod RegisterForSingleUpdate self ::NoneVar ::Enfriamiento_var  ;@line 332
						JumpF ::QALog_var _label101                              ;@line 333
						Cast ::temp36 rafaga                                     ;@line 334
						StrCat ::temp36 "AstraGuardiaAuto rÃ¡faga completa (" ::temp36  ;@line 334
						StrCat ::temp36 ::temp36 "): enfriando"                  ;@line 334
						CallStatic debug Trace ::NoneVar ::temp36 0              ;@line 334
						Jump _label101                                           ;@line 334
					_label101:
						Jump _label102                                           ;@line 334
					_label100:
						Assign fase 1                                            ;@line 337
						CallMethod ResetSegundos self ::temp37                   ;@line 338
						FAdd ::temp37 ::temp37 ::TickSegundos_var                ;@line 338
						CallMethod RegisterForSingleUpdate self ::NoneVar ::temp37  ;@line 338
					_label102:
					.endCode
				.endFunction
				.function Radianes
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Float
					.paramTable
						.param deg Float
					.endParamTable
					.localTable
						.local ::temp89 Float
					.endLocalTable
					.code
						FMultiply ::temp89 deg 0.017453                          ;@line 639
						Return ::temp89                                          ;@line 639
					.endCode
				.endFunction
				.function AplicarNodos
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::temp65 Float[]
						.local ::temp66 Float
						.local ::temp67 Float
						.local ::temp68 ObjectReference
						.local ::temp69 Bool
						.local m Float[]
						.local r Float
						.local c Float
						.local S Float
					.endLocalTable
					.code
						ArrayCreate ::temp65 9                                   ;@line 555
						Assign m ::temp65                                        ;@line 555
						CallMethod Radianes self ::temp66 yawActual              ;@line 556
						Assign r ::temp66                                        ;@line 556
						CallStatic math Cos ::temp66 r                           ;@line 557
						Assign c ::temp66                                        ;@line 557
						CallStatic math Sin ::temp66 r                           ;@line 558
						Assign S ::temp66                                        ;@line 558
						Assign ::temp66 c                                        ;@line 559
						ArraySetElement m 0 ::temp66                             ;@line 559
						FNegate ::temp67 S                                       ;@line 560
						Assign ::temp66 ::temp67                                 ;@line 560
						ArraySetElement m 1 ::temp66                             ;@line 560
						Assign ::temp66 0.000000                                 ;@line 561
						ArraySetElement m 2 ::temp66                             ;@line 561
						Assign ::temp67 S                                        ;@line 562
						ArraySetElement m 3 ::temp67                             ;@line 562
						Assign ::temp66 c                                        ;@line 563
						ArraySetElement m 4 ::temp66                             ;@line 563
						Assign ::temp67 0.000000                                 ;@line 564
						ArraySetElement m 5 ::temp67                             ;@line 564
						Assign ::temp66 0.000000                                 ;@line 565
						ArraySetElement m 6 ::temp66                             ;@line 565
						Assign ::temp67 0.000000                                 ;@line 566
						ArraySetElement m 7 ::temp67                             ;@line 566
						Assign ::temp66 1.000000                                 ;@line 567
						ArraySetElement m 8 ::temp66                             ;@line 567
						Cast ::temp68 self                                       ;@line 568
						CallStatic netimmerse SetNodeLocalRotationMatrix ::temp69 ::temp68 ::YawNode_var m False  ;@line 568
						FNegate ::temp67 pitchActual                             ;@line 569
						CallMethod Radianes self ::temp66 ::temp67               ;@line 569
						Assign r ::temp66                                        ;@line 569
						CallStatic math Cos ::temp67 r                           ;@line 570
						Assign c ::temp67                                        ;@line 570
						CallStatic math Sin ::temp66 r                           ;@line 571
						Assign S ::temp66                                        ;@line 571
						Assign ::temp67 1.000000                                 ;@line 572
						ArraySetElement m 0 ::temp67                             ;@line 572
						Assign ::temp66 0.000000                                 ;@line 573
						ArraySetElement m 1 ::temp66                             ;@line 573
						Assign ::temp67 0.000000                                 ;@line 574
						ArraySetElement m 2 ::temp67                             ;@line 574
						Assign ::temp66 0.000000                                 ;@line 575
						ArraySetElement m 3 ::temp66                             ;@line 575
						Assign ::temp67 c                                        ;@line 576
						ArraySetElement m 4 ::temp67                             ;@line 576
						FNegate ::temp67 S                                       ;@line 577
						Assign ::temp66 ::temp67                                 ;@line 577
						ArraySetElement m 5 ::temp66                             ;@line 577
						Assign ::temp66 0.000000                                 ;@line 578
						ArraySetElement m 6 ::temp66                             ;@line 578
						Assign ::temp67 S                                        ;@line 579
						ArraySetElement m 7 ::temp67                             ;@line 579
						Assign ::temp66 c                                        ;@line 580
						ArraySetElement m 8 ::temp66                             ;@line 580
						Cast ::temp68 self                                       ;@line 581
						CallStatic netimmerse SetNodeLocalRotationMatrix ::temp69 ::temp68 ::PitchNode_var m False  ;@line 581
					.endCode
				.endFunction
				.function AlertaCombat
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
						.param akBlanco Actor
					.endParamTable
					.localTable
						.local ::temp8 Bool
						.local ::temp10 Actor
						.local ::temp9 Float
						.local ::NoneVar None
						.local ::temp11 String
					.endLocalTable
					.code
						CallMethod Ocupada self ::temp8                          ;@line 128
						JumpF ::temp8 _label103                                  ;@line 128
						CallStatic utility GetCurrentRealTime ::temp9            ;@line 129
						FAdd ::temp9 ::temp9 8.000000                            ;@line 129
						Assign proximoIntento ::temp9                            ;@line 129
						JumpF ::QALog_var _label104                              ;@line 130
						CallStatic debug Trace ::NoneVar "AstraGuardiaAuto alerta pospuesta: ballesta ocupada" 0  ;@line 131
						Jump _label104                                           ;@line 131
					_label104:
						CallMethod RegisterForSingleUpdate self ::NoneVar 8.500000  ;@line 133
						Return None                                              ;@line 134
						Jump _label103                                           ;@line 134
					_label103:
						Cast ::temp10 None                                       ;@line 136
						CompareEQ ::temp8 akBlanco ::temp10                      ;@line 136
						Not ::temp8 ::temp8                                      ;@line 136
						JumpF ::temp8 _label105                                  ;@line 136
						Assign blanco akBlanco                                   ;@line 137
						Jump _label105                                           ;@line 137
					_label105:
						CompareEQ ::temp8 fase 0                                 ;@line 139
						JumpF ::temp8 _label106                                  ;@line 139
						Assign fase 1                                            ;@line 140
						Assign rafaga 0                                          ;@line 141
						Assign hayPosPrev False                                  ;@line 142
						CallStatic utility GetCurrentRealTime ::temp9            ;@line 143
						Assign ultimoTick ::temp9                                ;@line 143
						CallMethod RegisterForSingleUpdate self ::NoneVar ::TickSegundos_var  ;@line 144
						JumpF ::QALog_var _label107                              ;@line 145
						Cast ::temp11 blanco                                     ;@line 146
						StrCat ::temp11 "AstraGuardiaAuto despierta, blanco=" ::temp11  ;@line 146
						CallStatic debug Trace ::NoneVar ::temp11 0              ;@line 146
						Jump _label107                                           ;@line 146
					_label107:
						Jump _label106                                           ;@line 146
					_label106:
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
			.endState
		.endStateTable
	.endObject
.endObjectTable
