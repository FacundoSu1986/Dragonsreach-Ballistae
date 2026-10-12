"""Build exclusive AI for owned operators without modifying vanilla NPCs."""
from pathlib import Path
import hashlib
import json
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import build_guard_bridge_v23 as V23
import patch_plugin_v12 as P
import escritor_plugin as W


def rebuild(path, changes, extra_group=None):
    p = Plugin(path)
    groups = []
    cursor = p.inicio_datos
    while cursor < len(p.d):
        size = struct.unpack_from('<I',p.d,cursor+4)[0]
        groups.append(P.transform_groups(p.d[cursor:cursor+size],changes,set(),{}))
        cursor += size
    assert cursor == len(p.d)
    if extra_group:groups.append(extra_group)
    size = 24+struct.unpack_from('<I',p.d,4)[0]
    next_id = struct.unpack_from('<I',dict(p.subrecords(p.datos(0)))['HEDR'],8)[0]
    header = P.update_header(p.d[:size],W.contar_bloques(groups),max(next_id,0xB91))
    path.write_bytes(header+b''.join(groups))
    check = Plugin(path)
    for typ,off,n,depth in check.recorrer():
        if typ!='GRUP':check.subrecords(check.datos(off))


def replace_subs(raw,subs):
    body = b''.join(W.sub(k,v) for k,v in subs)
    return raw[:4]+struct.pack('<I',len(body))+raw[8:24]+body


def main():
    V23.main()
    vanilla = Plugin(Path(r'G:\Modding\Skyrim_Runtime_1.6.1170\Data\Skyrim.esm'))
    donor = next(vanilla.subrecords(vanilla.datos(o)) for t,o,n,d in vanilla.recorrer()
                 if t=='PACK' and vanilla.form_id(o)==0x0002AC7B)
    assert dict(donor)['EDID'].rstrip(b'\0')==b'DefaultStayAtCurrentLocation'
    assert dict(donor)['PKCU']==struct.pack('<III',3,0x00016FAA,3)
    subs = []
    for key,value in donor:
        if key in ('CTDA','CIS1','CIS2','VMAD'):continue
        if key=='EDID':value=W.zstr('AstraGuardStayAtBallista')
        if key=='PKDT':
            data=bytearray(value)
            flags=struct.unpack_from('<I',data)[0]
            flags=(flags|(1<<20)|(1<<21)|(1<<27))&~(1<<23)
            struct.pack_into('<I',data,0,flags)
            struct.pack_into('<H',data,8,0)
            value=bytes(data)
        subs.append((key,value))
    package=0x04000B90
    pack=W.record('PACK',package,[W.sub(k,v) for k,v in subs])
    city=ROOT/'addons/WhiterunTorres/AstraAsedio_WhiterunTorres.esp'
    records=P.record_map(Plugin(city))
    changes={}
    for fid in (0x04000B00,0x04000B01):
        raw=records[fid]
        ss=Plugin.subrecords(raw[24:])
        assert not any(k=='PKID' for k,v in ss)
        # The operator bases already do not inherit AI packages (bit 0x20).
        assert not struct.unpack_from('<H',dict(ss)['ACBS'],18)[0]&0x20
        index=next(i for i,(k,v) in enumerate(ss) if k=='AIDT')+1
        ss.insert(index,('PKID',struct.pack('<I',package)))
        changes[fid]=replace_subs(raw,ss)
    rebuild(city,changes,W.grupo('PACK',[pack]))

    anim=ROOT/'addons/GuardAnim/AstraAsedio_GuardAnim.esp'
    records=P.record_map(Plugin(anim))
    qid=0x03000806
    raw=records[qid]
    ss=[]
    for key,value in Plugin.subrecords(raw[24:]):
        if key=='DNAM':
            data=bytearray(value);data[2]=100;value=bytes(data)
        if key=='FNAM':
            # Optional / Allow Dead / Allow Disabled: refresh is legal even for
            # existing saves, and one dead operator cannot stop both sensors.
            value=struct.pack('<I',0x92)
        # ALPC is package data; ALSP means alias spells in TES5.
        if key=='ALED':ss.append(('ALPC',struct.pack('<I',0x02000B90)))
        ss.append((key,value))
    assert sum(k=='ALPC' for k,v in ss)==2
    rebuild(anim,{qid:replace_subs(raw,ss)})
    report={'revision':24,'success':True,'game_tested':False,
            'donor':'Skyrim.esm:0002AC7B','template':'Skyrim.esm:00016FAA',
            'package':'AstraAsedio_WhiterunTorres.esp:000B90',
            'owned_npcs':['000B00','000B01'],'aliases':['000B71','000B81'],
            'alias_package_subrecord':'ALPC','quest_priority':100,
            'ignore_combat':True,'weapons_unequipped':True,'no_combat_alert':True,
            'files_sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in (city,anim)}}
    (ROOT/'reports/bridge_v24.json').write_text(json.dumps(report,indent=2)+'\n')
    print('V24_EXCLUSIVE_OPERATOR_AI_BUILT')


if __name__=='__main__':main()
