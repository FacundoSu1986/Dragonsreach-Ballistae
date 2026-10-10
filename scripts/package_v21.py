"""One complete QA install: core, city addon and the relocated Atalaya together."""
import json,hashlib,sys,subprocess,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from package_v19 import archive,SUFFIXES

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    # Require fresh tests and the exact files actually reimported/checked.
    subprocess.run([sys.executable,'-m','unittest','discover','-s',str(ROOT/'tests'),'-p','test_v21_release.py','-v'],check=True,cwd=ROOT)
    placed=json.loads((ROOT/'reports/atalaya_placement_v21.json').read_text())
    assert placed['site']=={'x':4665.54,'y':-14922.81,'z':-5217.81,'rot_z_deg':187.63,'cell':'0000963D','grid':[1,-4]}
    assert sha(ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp')==placed['sha256']
    assert sha(ROOT/'addons/Atalaya/meshes/AstraAsedio/torre_atalaya_v20.nif')==placed['nif_sha256']
    native=json.loads((ROOT/'reports/native_build_receipt.json').read_text())
    for n,h in native['files_sha256'].items():assert sha(ROOT/n)==h,n
    core={p.relative_to(ROOT/'mod').as_posix():p for p in (ROOT/'mod').rglob('*') if p.is_file() and p.suffix.lower() in SUFFIXES}
    city={p.relative_to(ROOT/'addons/WhiterunTorres').as_posix():p for p in (ROOT/'addons/WhiterunTorres').rglob('*') if p.is_file() and p.suffix.lower() in ('.esp','.nif')}
    atalaya={'AstraAsedio_Atalaya.esp':ROOT/'addons/Atalaya/AstraAsedio_Atalaya.esp','meshes/AstraAsedio/torre_atalaya_v20.nif':ROOT/'addons/Atalaya/meshes/AstraAsedio/torre_atalaya_v20.nif'}
    assert set(core).isdisjoint(city) and set(core).isdisjoint(atalaya) and set(city).isdisjoint(atalaya)
    docs={'Docs/AstraAsedio/README_v21.md':ROOT/'docs/README_v21.md'}
    docs.update({'Docs/AstraAsedio/Licenses/'+p.name:p for p in (ROOT/'native/licenses').iterdir() if p.is_file()})
    assert len(docs)==5
    entries={**core,**city,**atalaya,**docs}
    assert {n for n in entries if n.endswith('.esp')}=={'AstraAsedio.esp','AstraAsedio_WhiterunTorres.esp','AstraAsedio_Atalaya.esp'}
    package=archive('AstraAsedio_QA_v21_Completo_MO2.zip',entries)
    verified={'revision':21,'success':True,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tests':13,'site':placed['site'],'mesh':'meshes/AstraAsedio/torre_atalaya_v20.nif','written_aim_poses':1512,'walk_samples':244,'navigation_proxy_radius':24,'navigation_proxy_height':144,'navigation_obstructions_at_this_site':json.loads((ROOT/'reports/nav_regression_v20.json').read_text())['obstructions'],'native_recompiled':False,'native_version':'3.5.4','core_and_city_byte_identical_to_v20':False,'combat_target_retained_on_mount':True,'stair_rubble_disabled':['000E4396','000E4397'],'game_tested':False,'nexus_uploaded':False,'live_installation_modified':False,'package':package}
    tracked=['docs/README_v21.md','scripts/audit_site_v21.py','scripts/research_atalaya_v21.py','scripts/research_havok_atalaya_v21.py','scripts/atalaya_v21_geometry.py','scripts/build_atalaya_v21.py','scripts/place_atalaya_v21.py','scripts/verify_atalaya_v21.py','scripts/nav_clearance_v21.py','scripts/verify_site_v21.py','scripts/package_v21.py','tests/test_v21_release.py','reports/atalaya_verified_v21.json','reports/site_verified_v21.json','reports/native_build_receipt.json']
    verified['inputs_sha256']={n:sha(ROOT/n) for n in tracked}
    (ROOT/'reports/verification_v21.json').write_text(json.dumps(verified,indent=2))
    (ROOT/'dist/MANIFEST_v21.json').write_text(json.dumps(verified,indent=2))
    print('PACKAGE_OK',package['path'],package['bytes'],package['sha256'],package['entries'])

if __name__=='__main__':main()
