"""Stable REFR identities; remove obsolete terrain/vanilla-object overrides."""
import sys,json,struct,math,hashlib
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
import escritor_plugin as W
import colocar_escudos as C
import patch_plugin_v12 as P
import mundo_v11 as M
import v11_layout as L
from build_modular_v13 import subs,clone,save_plugin
from atalaya_v20_geometry import Surface

def main():
    parent=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v19');rel='addons/Atalaya/AstraAsedio_Atalaya.esp'
    p=Plugin(str(parent/rel));old=P.record_map(p);oldsite=json.loads((parent/'config.json').read_text())['tower_v11']['mundo']
    surface=Surface();site=surface.site
    src=M.matriz_colocacion(oldsite);dst=M.matriz_colocacion(site);rs=np.array(src['r']);rd=np.array(dst['r']);changes={}
    removed={fid for fid,raw in old.items() if raw[:4]==b'LAND' or (raw[:4]==b'REFR' and fid>>24<4)}
    assert removed=={0xa63d,0xc9c74,0x39619,0x39617,0x39615}
    for fid,raw in old.items():
        if fid>>24!=4 or raw[:4]!=b'REFR':continue
        ss=subs(raw);data=struct.unpack('<6f',ss['DATA'])
        local=rs.T@(np.array(data[:3])-np.array(src['t']));rot=L.transform_matrix((0,0,0),[math.degrees(v) for v in data[3:]],1,*L.engine_convention())['r']
        newpos=rd@local+np.array(dst['t']);newrot=L.euler_from_matrix((rd@rs.T@np.array(rot)).tolist())
        # The chest is outside the roof footprint. Seat it on the untouched
        # terrain, instead of retaining the former flattened datum.
        if fid==0x04000A02:newpos[2]=site['z']+surface.z(local[0],local[1])+2
        update={'DATA':struct.pack('<6f',*newpos,*(math.radians(v) for v in newrot))}
        if fid==0x04000A01:update['NAME']=struct.pack('<I',0x04000A50)
        changes[fid]=P.modify_subs(raw,update)
    core=P.record_map(Plugin(str(ROOT/'mod/AstraAsedio.esp')));receipt=json.loads((ROOT/'reports/atalaya_build_v20.json').read_text())
    box=receipt['bbox'];obnd=[math.floor(v) for v in box['min']]+[math.ceil(v) for v in box['max']]
    stat=clone(core[0x03000800],0x04000A50,{'EDID':W.zstr('AstraAtalayaTerrenoV20'),'MODL':W.zstr('AstraAsedio\\torre_atalaya_v20.nif'),'OBND':struct.pack('<6h',*obnd)})
    groups=[W.grupo('STAT',[stat])];off=p.inicio_datos
    while off<len(p.d):
        size=struct.unpack_from('<I',p.d,off+4)[0];groups.append(P.transform_groups(p.d[off:off+size],changes,removed,{}));off+=size
    masters=[v.rstrip(b'\0').decode('cp1252') for k,v in Plugin.subrecords(p.datos(0)) if k=='MAST']
    result=save_plugin(ROOT/rel,groups,masters,0xA51)
    written=Plugin(str(ROOT/rel));header=P.modify_subs(written.d[:written.inicio_datos],{'SNAM':W.zstr('QA v20: Atalaya reubicada sin LAND ni NAVM')})
    (ROOT/rel).write_bytes(header+written.d[written.inicio_datos:])
    result['sha256']=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest();result['bytes']=(ROOT/rel).stat().st_size
    after=P.record_map(Plugin(str(ROOT/rel)));assert after.keys()==old.keys()-removed|{0x04000A50}
    for fid,raw in old.items():
        if fid not in removed|changes.keys():assert after[fid]==raw
    cfg=L.load_cfg();cfg['tower_v11']['mundo']=site
    # Terrain maps are research inputs, not required by core runtime config.
    cfg['tower_v11']['mundo'].pop('heightmaps',None)
    cfg['source']=str(ROOT/'source/Torre_Ballesta_lowpoly_v04.blend')
    (ROOT/'config.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=1))
    result.update({'source_sha256':hashlib.sha256(p.d).hexdigest(),'site':cfg['tower_v11']['mundo'],'removed_overrides':[f'{fid:08X}' for fid in sorted(removed)],'moved_owned_refs':[f'{fid:08X}' for fid in sorted(changes)],'stable_form_ids':True,'LAND_edits':0,'NAVM_edits':0,'vanilla_refs_edited':0,'game_tested':False})
    (ROOT/'reports/atalaya_placement_v20.json').write_text(json.dumps(result,indent=2));print('ATALAYA_PLACED',len(changes),'stable refs',result)
if __name__=='__main__':main()
