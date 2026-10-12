"""Build the v23 bridge from immutable 46bfbf7 records; never run v22 writers.

Only own operator transforms, NPC pitch properties and the retired high-station
Auto attachment change. Existing placed-reference IDs and world geometry survive.
"""
import hashlib
import json
import math
from pathlib import Path
import shutil
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import escritor_plugin as W
import build_plugin as B
import colocar_escudos as C
import patch_plugin_v12 as P


def frozen(relative):
    data = subprocess.check_output(['git','show','46bfbf7:'+relative],cwd=ROOT)
    path = ROOT/'build/guard-v23/baseline'/relative
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(data)
    return Plugin(path)


def serialize_script(item):
    props = {}
    for name,p in item['properties'].items():
        v = p['value']
        if p['type'] == 1:
            assert v['alias'] == -1
            v = v['form_id']
        props[name] = (p['type'],v)
    return item['name'],props


def patch_file(relative,changes):
    p = frozen(relative)
    groups = []
    cursor = p.inicio_datos
    while cursor < len(p.d):
        assert p.d[cursor:cursor+4] == b'GRUP'
        size = struct.unpack_from('<I',p.d,cursor+4)[0]
        groups.append(P.transform_groups(p.d[cursor:cursor+size],changes,set(),{}))
        cursor += size
    assert cursor == len(p.d)
    header_size = 24+struct.unpack_from('<I',p.d,4)[0]
    output = ROOT/relative
    output.write_bytes(p.d[:header_size]+b''.join(groups))
    # Re-read all nested records and every subrecord to reject bad serialization.
    checked = Plugin(output)
    for typ,off,n,depth in checked.recorrer():
        if typ != 'GRUP': checked.subrecords(checked.datos(off))
    return checked


def main():
    core_rel = 'mod/AstraAsedio.esp'
    p = frozen(core_rel)
    raw = P.record_map(p)[0x03000801]
    ss = Plugin.subrecords(raw[24:])
    vm = B.read_vmad(dict(ss)['VMAD'])
    keep = [serialize_script(s) for s in vm['scripts'] if s['name'] != 'AstraGuardiaAuto']
    assert [n for n,_ in keep] == ['AstraAsedioActi']
    patch_file(core_rel,{0x03000801:P.modify_subs(raw,{'VMAD':B.vmad_multi(keep)})})

    city_rel = 'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp'
    p = frozen(city_rel)
    records = P.record_map(p)
    changes = {}
    positions = {}
    for gun,guard,marker in ((0xB70,0xB71,0xB72),(0xB80,0xB81,0xB82)):
        gunfid = 0x04000000+gun
        raw = records[gunfid]
        ss = Plugin.subrecords(raw[24:])
        xyz = struct.unpack('<6f',dict(ss)['DATA'])
        x,y,z,rx,ry,yaw = xyz
        pose = (x-151*math.sin(yaw),y+151*math.cos(yaw),z,0.,0.,yaw+math.pi)
        for local in (guard,marker):
            fid = 0x04000000+local
            changes[fid] = P.modify_subs(records[fid],{'DATA':struct.pack('<6f',*pose)})
        vm = B.read_vmad(dict(ss)['VMAD'])
        for script in vm['scripts']:
            if script['name'] == 'AstraAsedioGuard':
                for key in ('PitchMin','PitchMax'):
                    script['properties'][key]['value'] = 0.
        changes[gunfid] = P.modify_subs(raw,{'VMAD':B.vmad_multi([serialize_script(s) for s in vm['scripts']])})
        positions[hex(guard)] = list(pose)
    patch_file(city_rel,changes)

    old = frozen('addons/GuardAnim/AstraAsedio_GuardAnim.esp')
    oldrecords = P.record_map(old)
    facts = [W.record('FACT',0x03000800+i,[W.sub('EDID',W.zstr(name)),W.sub('DATA',bytes(4))])
             for i,name in ((0,'AstraGuardPoseOwnedFaction'),(1,'AstraGuardFireVisualFaction'),
                            (4,'AstraGuardTurnLeftFaction'),(5,'AstraGuardTurnRightFaction'))]
    idles = []
    for local in (0x802,0x803):
        raw = oldrecords[0x02000000+local]
        # Copied owned IDLE has zero ANAM and no CTDA/form references to remap.
        ss = Plugin.subrecords(raw[24:])
        assert dict(ss)['ANAM'] == bytes(8)
        idles.append(W.record('IDLE',0x03000000+local,[W.sub(k,v) for k,v in ss]))
    qid = 0x03000806
    vm = B.vmad_multi([])+struct.pack('<BHHH',2,0,0,2)
    for alias_id,gun in enumerate((0xB70,0xB80)):
        vm += struct.pack('<HhIHHH',0,alias_id,qid,5,2,1)
        vm += B.script('AstraGuardOperatorAlias',{'Controller':(1,0x02000000+gun)})
    assert len(B.read_vmad(vm,quest=True)['aliases']) == 2
    quest = [W.sub('EDID',W.zstr('AstraGuardOperatorSensorsQuest')),W.sub('VMAD',vm),
             W.sub('DNAM',struct.pack('<HBBII',0x101,50,0,0,0)),W.sub('NEXT',b''),W.sub('ANAM',B.U(2))]
    for alias_id,actor in enumerate((0xB71,0xB81)):
        quest += [W.sub('ALST',B.U(alias_id)),W.sub('ALID',W.zstr(('East','West')[alias_id])),
                  W.sub('FNAM',B.U(4)),W.sub('ALFR',B.U(0x02000000+actor)),W.sub('ALED',b'')]
    addon = ROOT/'addons/GuardAnim'
    W.escribir(addon/'AstraAsedio_GuardAnim.esp',
        ['Skyrim.esm','AstraAsedio.esp','AstraAsedio_WhiterunTorres.esp'],
        [W.grupo('FACT',facts),W.grupo('IDLE',idles),W.grupo('QUST',[W.record('QUST',qid,quest)])],
        [0x03000800+i for i in range(7)],autor='Astra',esl=False,
        descripcion='v23 owned guard animation gates and persistent operator sensors')
    (addon/'seq').mkdir(exist_ok=True)
    (addon/'seq/AstraAsedio_GuardAnim.seq').write_bytes(B.U(qid))

    oar = addon/'meshes/actors/character/animations/OpenAnimationReplacer/AstraAsedioGuard'
    (oar/'config.json').write_text(json.dumps({'name':'AstraAsedio Guard','author':'Astra',
        'description':'Owned low ballista operators. Fixed height and horizontal aim.'},indent=2)+'\n')
    exclusion = {'condition':'IsActorBase','requiredVersion':'1.0.0','negated':True,
                 'Actor base':{'pluginName':'Skyrim.esm','formID':'000007'}}
    def gate(local):
        return {'condition':'IsInFaction','requiredVersion':'1.0.0',
                'Faction':{'pluginName':'AstraAsedio_GuardAnim.esp','formID':f'{local:06X}'}}
    canonical = addon/'meshes/actors/character/animations/AstraAsedio/Guard'
    canonical.mkdir(parents=True,exist_ok=True)
    clips = {}
    for name,kind,faction,priority in [('Operate','operate',None,1185250),
            ('Fire','fire',0x801,1185253),('TurnLeft','turn_left',0x804,1185251),
            ('TurnRight','turn_right',0x805,1185252)]:
        folder = oar/name
        folder.mkdir(exist_ok=True)
        conditions = [gate(0x800),exclusion]
        if faction: conditions.insert(1,gate(faction))
        config = {'name':'Astra Guard '+name,'priority':priority,'conditions':conditions,
                  'interruptible':True,'hasCustomBlendTimeOnInterrupt':True,
                  'blendTimeOnInterrupt':0.,'replaceOnLoop':True,
                  'hasCustomBlendTimeOnLoop':True,'blendTimeOnLoop':0.}
        (folder/'config.json').write_text(json.dumps(config,indent=2)+'\n')
        clip = ROOT/'source/anim'/f'astra_guard_{kind}.hkx'
        for leaf in ('IdleHandsBehindBack.hkx','IdleHandsBehindBack_Enter.hkx'):
            shutil.copy2(clip,folder/leaf)
        shutil.copy2(clip,canonical/clip.name)
        clips[kind] = hashlib.sha256(clip.read_bytes()).hexdigest()
    report = {'success':True,'baseline_commit':'46bfbf7','guard_positions':positions,
              'operator_local_offset':[0,151,0],'fixed_npc_pitch':0,
              'guard_anim_masters':['Skyrim.esm','AstraAsedio.esp','AstraAsedio_WhiterunTorres.esp'],
              'sensor_quest_local':'000806','clips':clips,'game_tested':False,
              'changed_city_forms':[f'{f:08X}' for f in sorted(changes)]}
    (ROOT/'reports/bridge_v23.json').write_text(json.dumps(report,indent=2)+'\n')
    print('V23_BRIDGE_BUILT')


if __name__ == '__main__':main()
