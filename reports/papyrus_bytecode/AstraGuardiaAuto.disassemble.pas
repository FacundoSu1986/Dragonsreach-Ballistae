.info
	.source "AstraGuardiaAuto.psc"
	.modifyTime 1791759002 ;Sun Oct 11 19:50:02 2026 Local
	.compileTime 1791759048 ;Sun Oct 11 19:50:48 2026 Local
	.user "AstraAsedio"
	.computer "Build"
.endInfo
.userFlagsRef
	.flag hidden 0	; 0x00000000
	.flag conditional 1	; 0x00000001
.endUserFlagsRef
.objectTable
	.object AstraGuardiaAuto ObjectReference
		.userFlags 0	; Flags: 0x00000000
		.docString ""
		.autoState 
		.variableTable
			.variable ::TickSegundos_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.120000
			.endVariable
			.variable ::MaxRafaga_var Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 3
			.endVariable
			.variable ::Launcher_var weapon
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ultimoTick Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::AlcanceMax_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 8400.000000
			.endVariable
			.variable guardia Actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::AlcanceMin_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 900.000000
			.endVariable
			.variable ::PitchMin_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue -5.000000
			.endVariable
			.variable ::ReleaseSegundos_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.100000
			.endVariable
			.variable ::PitchMax_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 80.000000
			.endVariable
			.variable ::YawNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "CTRL_GIRO_360"
			.endVariable
			.variable yawActual Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::MuzzleAdelante_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue -224.000000
			.endVariable
			.variable ::YawSpeed_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 40.000000
			.endVariable
			.variable ::ShotSound_var sound
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::GravedadProyectil_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 240.345001
			.endVariable
			.variable ::ArcMax_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 60.000000
			.endVariable
			.variable ::ShotAmmo_var ammo
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable fase Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable hayPosPrev Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::MargenImpacto_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 384.000000
			.endVariable
			.variable ::Anticipacion_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.500000
			.endVariable
			.variable xPrev Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable rafaga Int
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0
			.endVariable
			.variable blanco Actor
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::PitchNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "CTRL_ELEVACION"
			.endVariable
			.variable ::VisualBoltNode_var String
				.userFlags 0	; Flags: 0x00000000
				.initialValue "VIROTE_VISUAL"
			.endVariable
			.variable pitchActual Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable proximoIntento Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::VelocidadProyectil_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 5400.000000
			.endVariable
			.variable ::QALog_var Bool
				.userFlags 0	; Flags: 0x00000000
				.initialValue False
			.endVariable
			.variable ::OcupadaGuardia_var globalvariable
				.userFlags 0	; Flags: 0x00000000
				.initialValue None
			.endVariable
			.variable ::MuzzleAlto_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 136.600006
			.endVariable
			.variable ::MargenLinea_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 320.000000
			.endVariable
			.variable zPrev Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable yPrev Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 0.000000
			.endVariable
			.variable ::PitchSpeed_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 20.000000
			.endVariable
			.variable ::Enfriamiento_var Float
				.userFlags 0	; Flags: 0x00000000
				.initialValue 8.000000
			.endVariable
		.endVariableTable
		.propertyTable
			.property PitchSpeed Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchSpeed_var
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
			.property ShotSound sound auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ShotSound_var
			.endProperty
			.property Anticipacion Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Anticipacion_var
			.endProperty
			.property ReleaseSegundos Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ReleaseSegundos_var
			.endProperty
			.property MargenLinea Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::MargenLinea_var
			.endProperty
			.property OcupadaGuardia globalvariable auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::OcupadaGuardia_var
			.endProperty
			.property YawNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::YawNode_var
			.endProperty
			.property PitchNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchNode_var
			.endProperty
			.property MuzzleAdelante Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::MuzzleAdelante_var
			.endProperty
			.property TickSegundos Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::TickSegundos_var
			.endProperty
			.property VelocidadProyectil Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::VelocidadProyectil_var
			.endProperty
			.property MargenImpacto Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::MargenImpacto_var
			.endProperty
			.property Enfriamiento Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Enfriamiento_var
			.endProperty
			.property VisualBoltNode String auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::VisualBoltNode_var
			.endProperty
			.property PitchMax Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::PitchMax_var
			.endProperty
			.property GravedadProyectil Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::GravedadProyectil_var
			.endProperty
			.property ShotAmmo ammo auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ShotAmmo_var
			.endProperty
			.property Launcher weapon auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::Launcher_var
			.endProperty
			.property ArcMax Float auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::ArcMax_var
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
			.property QALog Bool auto
				.userFlags 0	; Flags: 0x00000000
				.docString ""
				.autoVar ::QALog_var
			.endProperty
		.endPropertyTable
		.stateTable
			.state 
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
				.function FaseRecarga
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 142
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
						.local ::temp8 Float
					.endLocalTable
					.code
						Cast ::temp8 0                                           ;@line 227
						Return ::temp8                                           ;@line 227
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
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 92
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
						.local ::temp5 Float
					.endLocalTable
					.code
						Cast ::temp5 0                                           ;@line 212
						Return ::temp5                                           ;@line 212
					.endCode
				.endFunction
				.function ReglaEnganche
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return String
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 160
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
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 122
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
						.local ::temp6 Float
					.endLocalTable
					.code
						Cast ::temp6 0                                           ;@line 217
						Return ::temp6                                           ;@line 217
					.endCode
				.endFunction
				.function ElegirBlanco
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 155
					.endCode
				.endFunction
				.function Ocupada
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Bool
					.paramTable
					.endParamTable
					.localTable
					.endLocalTable
					.code
						Return False                                             ;@line 197
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
					.endLocalTable
					.code
						Return False                                             ;@line 165
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
						.local ::temp0 ObjectReference
						.local ::temp1 astraasedioguard
						.local ::temp2 Bool
						.local stationRef ObjectReference
						.local controller astraasedioguard
						.local ::NoneVar None
					.endLocalTable
					.code
						Cast ::temp0 self                                        ;@line 105
						Assign stationRef ::temp0                                ;@line 105
						Cast ::temp1 stationRef                                  ;@line 106
						Assign controller ::temp1                                ;@line 106
						Cast ::temp1 None                                        ;@line 107
						CompareEQ ::temp2 controller ::temp1                     ;@line 107
						Not ::temp2 ::temp2                                      ;@line 107
						JumpF ::temp2 _label0                                    ;@line 107
						CallMethod NotifyCombatV23 controller ::NoneVar akBlanco  ;@line 108
						Jump _label0                                             ;@line 108
					_label0:
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 110
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
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 84
					.endCode
				.endFunction
				.function FaseLiberacion
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 137
					.endCode
				.endFunction
				.function CalmaCombat
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 115
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
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 97
					.endCode
				.endFunction
				.function LeerAnguloDeNodos
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 189
					.endCode
				.endFunction
				.function ResetSegundos
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return Float
					.paramTable
					.endParamTable
					.localTable
						.local ::temp3 Float
					.endLocalTable
					.code
						Cast ::temp3 0                                           ;@line 202
						Return ::temp3                                           ;@line 202
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
						.local ::temp4 Float
					.endLocalTable
					.code
						Cast ::temp4 0                                           ;@line 207
						Return ::temp4                                           ;@line 207
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
						.local ::temp7 Float
					.endLocalTable
					.code
						Cast ::temp7 0                                           ;@line 222
						Return ::temp7                                           ;@line 222
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
					.endLocalTable
					.code
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 127
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
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 88
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
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 147
					.endCode
				.endFunction
				.function FaseFuego
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 132
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
					.endLocalTable
					.code
						Return False                                             ;@line 174
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
				.function AplicarNodos
					.userFlags 0	; Flags: 0x00000000
					.docString ""
					.return None
					.paramTable
					.endParamTable
					.localTable
						.local ::NoneVar None
					.endLocalTable
					.code
						CallMethod UnregisterForUpdate self ::NoneVar            ;@line 184
					.endCode
				.endFunction
			.endState
		.endStateTable
	.endObject
.endObjectTable
