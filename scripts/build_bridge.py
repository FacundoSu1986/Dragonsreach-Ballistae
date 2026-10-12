"""Build the guard-pose bridge (v22) from the frozen v21 ZIP that ships with this repo.

Portado desde Ballesta_Astra_Unificado_v01/scripts/build_bridge.py. Diferencias:
el baseline v21 no es un proyecto hermano sino el propio
`dist/AstraAsedio_QA_v21_Completo_MO2.zip` (sha 0a60c61f..., pinneado en
reports/base_archive.json), y los clips ya horneados viven en `source/anim/`.
Las salidas van al core (`mod/scripts/source/AstraAsedioGuard.psc`) y al addon
(`addons/GuardAnim/`). El .psc pre-puente no se edita nunca: se lee del ZIP.

Dependencias externas, referenciadas y nunca copiadas a un paquete:
  - G:/Modding/Skyrim_Runtime_1.6.1170/Data/Skyrim.esm  (donantes de los IDLE)
  - source/anim/*.hkx   horneados por scripts/build_guard_bajada.py (Blender + blender-hkx.exe)
"""
import hashlib, json, shutil, struct, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT
ANIM = ROOT/'source/anim'
sys.path.insert(0, str(BASE/'scripts/vendor'))
from parser_esm import Plugin
import escritor_plugin as W

def replace_once(text, before, after):
    assert text.count(before) == 1, (before[:120], text.count(before))
    return text.replace(before, after, 1)

def main():
    receipt = json.loads((ROOT/'reports/base_archive.json').read_text())
    archive = Path(receipt['path'])
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == receipt['sha256']
    with zipfile.ZipFile(archive) as z:
        key = next(n for n in z.namelist() if n.replace('\\','/') == 'scripts/source/AstraAsedioGuard.psc')
        pre_bridge = z.read(key)
        source = pre_bridge.decode('utf-8-sig').replace('\r\n','\n')
    source = replace_once(source, 'bool running = false', '''; GuardAnim v01: private OAR bridge; player controller remains byte-identical.
Faction poseFaction
Faction fireFaction
Idle holdIdle
Idle exitIdle
Actor visualTarget
float visualScanAt = 0.0
bool guardPoseStarted = false
bool guardPoseFiring = false
float guardPoseFireAt = 0.0

bool running = false''')
    source = replace_once(source, '    Actor candidate = Artillero\n    pinBusy = true\n    candidate.SetDontMove(true)', '''    bool animationReady = LoadGuardAnimation()
    if generation != expectedGeneration || !animationReady
        Debug.Trace("AstraAsedioGuard: enable OAR and AstraAsedio_GuardAnim.esp to operate the NPC.")
        return false
    endif
    Actor candidate = Artillero
    pinBusy = true
    candidate.SetDontMove(true)''')
    source = replace_once(source, '        previousGuard.SetDontMove(false)', '        StopGuardPose(previousGuard)\n        previousGuard.SetDontMove(false)')
    source = replace_once(source, '    shotTarget = None\n    matricesReady = false', '    shotTarget = None\n    visualTarget = None\n    visualScanAt = 0.0\n    matricesReady = false')
    source = replace_once(source, '    SetVisualBolt(1.0, recoveryGeneration, recoveryToken)', '''    bool positioned = PositionOperator(recoveryGeneration, recoveryToken)
    if !Current(recoveryGeneration, recoveryToken)
        return
    endif
    bool posed = positioned && StartGuardPose(recoveryGeneration, recoveryToken)
    if !Current(recoveryGeneration, recoveryToken)
        return
    endif
    if !posed
        faulted = true
        Shutdown()
        return
    endif
    SetVisualBolt(1.0, recoveryGeneration, recoveryToken)''')
    source = replace_once(source, '    float distance = ownedGuard.GetDistance(Puesto)\n    return Current(expectedGeneration, expectedToken) && ready && Finite(distance, 0.0, 64.0)', '    float distance = ownedGuard.GetDistance(Self)\n    return Current(expectedGeneration, expectedToken) && ready && Finite(distance, 0.0, 240.0)')
    start = source.index('bool Function SampleTarget(')
    end = source.index('\nfloat Function Approach(', start)
    source = source[:start] + '''bool Function SampleTarget(Actor target, int expectedGeneration, int expectedToken)
    return SampleHorizontalTarget(target, expectedGeneration, expectedToken)
EndFunction
''' + source[end:]
    source = replace_once(source, '    float nextPitch = Approach(pitch, desiredPitch, rate*dt)', '    float nextPitch = 0.0')
    source = replace_once(source, '    phase = 1\n    phaseAt = now\n    shotTarget = target', '''    bool bodyStarted = SetGuardFirePose(true, expectedGeneration, expectedToken)
    if !Current(expectedGeneration, expectedToken) || !bodyStarted
        return
    endif
    guardPoseFireAt = now
    phase = 1
    phaseAt = now
    shotTarget = target''')
    source = replace_once(source, '    StartReset(expectedGeneration, expectedToken)\nEndFunction', '''    SetGuardFirePose(false, expectedGeneration, expectedToken)
    if Current(expectedGeneration, expectedToken)
        StartReset(expectedGeneration, expectedToken)
    endif
EndFunction''')
    source = replace_once(source, '    bool menuOpen = Utility.IsInMenuMode()\n    if !Current(updateGeneration, updateToken)', '''    if guardPoseFiring && now >= guardPoseFireAt+1.0
        SetGuardFirePose(false, updateGeneration, updateToken)
    endif
    if !Current(updateGeneration, updateToken)
        return
    endif
    bool menuOpen = Utility.IsInMenuMode()
    if !Current(updateGeneration, updateToken)''')
    source = source.replace('FinishUpdate(updateGeneration, updateToken, 0.2)', 'FinishUpdate(updateGeneration, updateToken, 0.05)')
    source = source.replace('FinishUpdate(updateGeneration, updateToken, 0.1)', 'FinishUpdate(updateGeneration, updateToken, 0.02)')
    a = source.index('    Actor target = Artillero.GetCombatTarget()\n    bool sampled = SampleTarget(target, updateGeneration, updateToken)')
    b = source.index('    ; The bounded player trajectory check', a)
    source = source[:a] + '''    Actor target = ChooseVisualTarget(now, updateGeneration, updateToken)
    bool sampled = SampleVisualTarget(target, updateGeneration, updateToken)
    if !Current(updateGeneration, updateToken)
        return
    endif
    ; A reachable enemy refines yaw from the actual muzzle rather than root.
    if sampled && ValidTarget(target, updateGeneration, updateToken)
        SampleTarget(target, updateGeneration, updateToken)
    endif
    if !Current(updateGeneration, updateToken)
        return
    endif
    if sampled
        TurnToward(dt, updateGeneration, updateToken)
    endif
    if !Current(updateGeneration, updateToken)
        return
    endif
    bool positioned = PositionOperator(updateGeneration, updateToken)
    if !Current(updateGeneration, updateToken)
        return
    endif
    if !positioned
        faulted = true
        Shutdown()
        return
    endif
''' + source[b:]
    source += '\n' + (ROOT/'scripts/guard_pose.pscinc').read_text()
    (ROOT/'mod/scripts/source/AstraAsedioGuard.psc').write_text(source, encoding='utf-8', newline='\n')

    vanilla = Plugin(r'G:\Modding\Skyrim_Runtime_1.6.1170\Data\Skyrim.esm')
    donors = {}
    for t,o,n,d in vanilla.recorrer():
        if t == 'IDLE' and vanilla.form_id(o) in (0xb240a, 0x86840):
            donors[vanilla.form_id(o)] = vanilla.subrecords(vanilla.datos(o))
    facts = [W.record('FACT',0x02000800+i,[W.sub('EDID',W.zstr(name)),W.sub('DATA',b'\0'*4)])
             for i,name in enumerate(('AstraGuardPoseOwnedFaction','AstraGuardFireVisualFaction'))]
    idles = []
    for i,(donor,name) in enumerate(((0xb240a,'AstraGuardOperateIdle'),(0x86840,'AstraGuardExitIdle'))):
        ss = [(k, W.zstr(name) if k=='EDID' else v) for k,v in donors[donor] if k not in ('CTDA','CIS1','CIS2')]
        ss = [(k, b'\0'*8 if k=='ANAM' else v) for k,v in ss]
        idles.append(W.record('IDLE',0x02000802+i,[W.sub(k,v) for k,v in ss]))
    W.escribir(ROOT/'addons/GuardAnim/AstraAsedio_GuardAnim.esp', ['Skyrim.esm','AstraAsedio.esp'],
               [W.grupo('FACT',facts),W.grupo('IDLE',idles)],range(0x02000800,0x02000804),
               autor='Astra',esl=False,descripcion='Private OAR bridge for Astra siege operators')
    oar = ROOT/'addons/GuardAnim/meshes/actors/character/animations/OpenAnimationReplacer/AstraAsedioGuard'
    oar.mkdir(parents=True,exist_ok=True)
    (oar/'config.json').write_text(json.dumps({'name':'AstraAsedio Guard','author':'Astra','description':'Owned NPC operators only; hold and visual fire. Requires OAR.'},indent=2))
    actor_exclusion={'condition':'IsActorBase','requiredVersion':'1.0.0','negated':True,'Actor base':{'pluginName':'Skyrim.esm','formID':'000007'}}
    owned={'condition':'IsInFaction','requiredVersion':'1.0.0','Faction':{'pluginName':'AstraAsedio_GuardAnim.esp','formID':'000800'}}
    fire={'condition':'IsInFaction','requiredVersion':'1.0.0','Faction':{'pluginName':'AstraAsedio_GuardAnim.esp','formID':'000801'}}
    for n,clip,priority,conditions in [('Operate','operate',1185250,[owned,actor_exclusion]),('Fire','fire',1185251,[owned,fire,actor_exclusion])]:
        q=oar/n;q.mkdir(exist_ok=True)
        config={'name':'Astra Guard '+n,'description':'Private faction gate; releases with station ownership.','priority':priority,'conditions':conditions,
                'interruptible':True,'hasCustomBlendTimeOnInterrupt':True,'blendTimeOnInterrupt':0.0,'replaceOnLoop':True,
                'hasCustomBlendTimeOnLoop':True,'blendTimeOnLoop':0.0}
        (q/'config.json').write_text(json.dumps(config,indent=2))
        for slot in ('IdleHandsBehindBack.hkx','IdleHandsBehindBack_Enter.hkx'):
            shutil.copy2(ANIM/f'astra_guard_{clip}.hkx',q/slot)
    canonical=ROOT/'addons/GuardAnim/meshes/actors/character/animations/AstraAsedio/Guard';canonical.mkdir(parents=True,exist_ok=True)
    for clip in ('operate','fire'):
        shutil.copy2(ANIM/f'astra_guard_{clip}.hkx',canonical/f'astra_guard_{clip}.hkx')
    report = {'success': True,
              'baseline_zip': receipt['path'], 'baseline_sha256': receipt['sha256'],
              'guard_psc_sha256_pre_bridge': hashlib.sha256(pre_bridge).hexdigest(),
              'guard_psc_sha256': hashlib.sha256((ROOT/'mod/scripts/source/AstraAsedioGuard.psc').read_bytes()).hexdigest(),
              'addon_esp_sha256': hashlib.sha256((ROOT/'addons/GuardAnim/AstraAsedio_GuardAnim.esp').read_bytes()).hexdigest(),
              'clips': {clip: hashlib.sha256((ANIM/f'astra_guard_{clip}.hkx').read_bytes()).hexdigest()
                        for clip in ('operate','fire')},
              'requires_open_animation_replacer': True,
              'bundles_open_animation_replacer': False,
              'runtime_integrated': False}
    (ROOT/'reports').mkdir(exist_ok=True)
    (ROOT/'reports/bridge_v22.json').write_text(json.dumps(report, indent=2))
    print('BRIDGE_BUILT', report['guard_psc_sha256'], report['addon_esp_sha256'])

if __name__=='__main__':main()
