# Operadores sujetos a los mandos: v25

El usuario autoriza mantener a B71/B81 permanentemente en las ballestas bajas, apuntar en horizontal a visitantes y disparar únicamente a enemigos. Se conserva la protección del jugador y el virote normal. La animación aprobada y los puestos altos del jugador no cambian.

## Causa medida

La prueba v24 del 11 de octubre muestra paquete 14000B90 activo, weaponDrawn=false y actorScale=1.03 en ambos operadores. Todos los rechazos específicos muestran `station / actor scale differs from 1`: el controlador exige GetScale()==1 antes de solicitar el clip. No se ha observado aún ejecución de las verificaciones posteriores en esa partida. CommonLib TESNPC::GetHeight calcula race.height[sex] * NPC.height; el tamaño natural no equivale necesariamente a la escala de referencia.

## Decisiones

Se valida por separado escala de referencia 1, altura natural de la base y escala efectiva igual a esa altura. No se modifica ninguna raza ni se redimensiona al guardia. La escala efectiva se captura durante el contrato y un cambio posterior cancela efectos. La estación y los clips conservan escala 1.

La sujeción conserva el radio 151, orientación respecto al arma y altura adquirida mediante el controlador físico real. Se verifica y reafirma la pose en cada actualización mientras el contrato esté activo, con los mismos límites de desplazamiento y suelo. El agarre se corrige después del muestreo del esqueleto mediante IK de brazo, usando las muñecas canónicas de la escena aprobada (±33.6,143.8,100.5) y el pequeño desplazamiento de gatillo de Fire. No se cambia escala de huesos; solo se acepta una corrección pequeña y alcanzable. El movimiento usa los pasos ya aprobados. IK se aplica exclusivamente con una observación canónica OAR vigente de epoch, clip esperado, duración, peso y frame; usa la fase observada. Durante entrada o transición se da la gracia vigente del controlador sin intentar corregir una pose vanilla. El disparo exige agarre confirmado reciente, además de la preparación del clip y todas las comprobaciones físicas anteriores.

El usuario confirmó ignorar habitantes y guardias locales. Los locales no hostiles quedan fuera del apuntado visual: facciones reales TownWhiterunFaction 28172 o GuardFactionWhiterun 2BE39; no se infiere residencia por prefijo de FormID. El jugador y visitantes siguen siendo elegibles, los enemigos mantienen prioridad y se excluyen operadores propios. Un enemigo no alcanzable en altura puede recibir seguimiento visual dentro de 2100 unidades. Solo enemigos alcanzables pueden ampliar ese rango hasta 6000. La trayectoria horizontal se valida antes del gesto de disparo y nuevamente antes del lanzamiento.

La migración incrementa a 25 conservando variables v23, y recoloca los dos operadores una vez drenado el dueño anterior. Se conserva IA exclusiva, protección de neutrales/aliados y seguimiento sin homing. No se relajan comprobaciones de disparo para superar una falla de animación.

## Entrega y límites

Se reproduce primero el rechazo 1.03 en tests portables y se añaden contratos de escala, pin, agarre y selección local. Se recompilan PEX y DLL y se verifican los artefactos finales. ZIP v25 separado; v23/v24 originales intactos. La prueba del usuario certifica la causa v24, pero no se contará como reproducción de OAR o disparo en v25: esa prueba jugable sigue pendiente.
