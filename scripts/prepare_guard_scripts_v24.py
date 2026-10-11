"""Retain persisted v23 field/API names while upgrading migration to 24."""
from pathlib import Path
import prepare_guard_scripts_v23 as V23

ROOT=Path(__file__).resolve().parents[1]


def main(runtime_include=None,revision=24):
    V23.main(runtime_include or ROOT/'scripts/guard_runtime_v24.pscinc')
    alias=ROOT/'mod/scripts/source/AstraAsedioPlayerAlias.psc'
    text=V23.function(alias.read_text(),'BootstrapGuardV23','''    Quest sensors = Game.GetFormFromFile(0x00000806, "AstraAsedio_GuardAnim.esp") as Quest
    if sensors != None && !sensors.IsRunning()
        sensors.Start()
    endif
    int index = 0
    while index < 2
        int formID = 0x00000B70+index*16
        AstraAsedioGuard controller = Game.GetFormFromFile(formID, "AstraAsedio_WhiterunTorres.esp") as AstraAsedioGuard
        if controller != None
            ; Revoke the old token before changing alias/package state. The
            ; controller waits for its effects barrier before relocating.
            controller.StartV23()
            Actor operatorRef = Game.GetFormFromFile(formID+1, "AstraAsedio_WhiterunTorres.esp") as Actor
            if sensors != None && sensors.IsRunning() && operatorRef != None
                ReferenceAlias operatorAlias = sensors.GetAlias(index) as ReferenceAlias
                if operatorAlias != None
                    ; These two v24 aliases are Optional, so Clear is legal.
                    ; Refilling reapplies ALPC to FF bases restored from saves.
                    operatorAlias.Clear()
                    operatorAlias.ForceRefTo(operatorRef)
                    operatorRef.EvaluatePackage()
                endif
            endif
        endif
        index += 1
    endwhile''')
    alias.write_text(text,encoding='utf-8',newline='\n')
    print(f'V{revision}_GUARD_MIGRATION_PREPARED')


if __name__=='__main__':main()
