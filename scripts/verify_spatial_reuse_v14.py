"""Bind existing v13 spatial evidence to v14's proven timing-only changes."""
import hashlib,json,sys
from pathlib import Path
from retime_v14 import retime_parent
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v13')
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
from patch_plugin_v12 import record_map
from build_plugin import IDS,read_vmad
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    old=json.loads((BASE/'config.json').read_text());new=json.loads((ROOT/'config.json').read_text())
    changed={k for k in old.keys()|new.keys() if old.get(k)!=new.get(k)}
    assert changed=={'source','fire_seconds','release_seconds','reset_seconds','cycle_seconds'}
    gun='mod/meshes/AstraAsedio/ballesta.nif'
    output,retime=retime_parent(BASE/gun,{'Fire':new['fire_seconds'],'Reset':new['reset_seconds']})
    assert output==(ROOT/gun).read_bytes()
    certificates=[]
    for name in ['shot_clearance_v12.json','sight_path_verified.json','sight_anchor_verified.json']:
        path=BASE/'reports'/name;report=json.loads(path.read_text())
        assert report.get('ok',report.get('success'))
        bindings={**report.get('inputs_sha256',{})}
        nif=report.get('nif_sha256',{})
        if isinstance(nif,str):bindings[gun]=nif
        else:bindings.update({'mod/meshes/AstraAsedio/'+k+'.nif':v for k,v in nif.items()})
        for key,digest in bindings.items():
            assert sha(BASE/key)==digest,('Stale parent spatial evidence',key)
            if key not in ('config.json',gun):assert sha(ROOT/key)==digest,('Changed spatial input',key)
        certificates.append({'parent_report':str(path),'parent_report_sha256':sha(path),
                             'parent_samples':report.get('shots',report.get('poses')) if not isinstance(report.get('poses'),list) else len(report['poses']),
                             'reused_spatial_result':True,'new_spatial_run':False})
    report={'success':True,'scope':'Player laboratory/Atalaya spatial geometry only; new city positions require towers_v14.json.',
            'config_changes':sorted(changed),'normalized_animation_spatial_keys_identical':True,
            'registered_timing_only':retime['spatial_values_shaders_collision_unchanged'],
            'v13_ballista_sha256':sha(BASE/gun),'v14_ballista_sha256':sha(ROOT/gun),
            'config_sha256':sha(ROOT/'config.json'),'certificates':certificates,
            'verifier_sha256':sha(Path(__file__)),'in_game_verified':False}
    oldrecords=record_map(Plugin(str(BASE/'mod/AstraAsedio.esp')))
    newrecords=record_map(Plugin(str(ROOT/'mod/AstraAsedio.esp')))
    assert oldrecords.keys()==newrecords.keys()
    for fid,raw in oldrecords.items():
        if fid!=IDS['ballesta']:assert raw==newrecords[fid]
        else:
            a=dict(Plugin.subrecords(raw[24:]));b=dict(Plugin.subrecords(newrecords[fid][24:]))
            assert {k:v for k,v in a.items() if k!='VMAD'}=={k:v for k,v in b.items() if k!='VMAD'}
            pa=read_vmad(a['VMAD'])['scripts'][0]['properties'];pb=read_vmad(b['VMAD'])['scripts'][0]['properties']
            allowed={'FireSeconds','ReleaseSeconds','ResetSeconds','CycleSeconds'}
            assert {k:v for k,v in pa.items() if k not in allowed}=={k:v for k,v in pb.items() if k not in allowed}
    route_path=BASE/'reports/route_v12.json';route=json.loads(route_path.read_text())
    assert route['ok'] and route['esp_sha256']==sha(BASE/'mod/AstraAsedio.esp')
    assert route['torre_sha256']==sha(ROOT/'mod/meshes/AstraAsedio/torre.nif')
    report['laboratory_route_reuse']={'parent_report_sha256':sha(route_path),'parent_samples':route['route_samples'],
                                    'core_only_timing_vmad_changed':True,'new_route_run':False}
    (ROOT/'reports/spatial_reuse_v14.json').write_text(json.dumps(report,indent=2))
    print('V14_SPATIAL_REUSE_PROVEN',[(c['parent_report'],c['parent_samples']) for c in certificates])
if __name__=='__main__':main()
