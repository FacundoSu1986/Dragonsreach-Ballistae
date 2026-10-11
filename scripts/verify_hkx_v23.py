"""Decode final four HKXs independently, including source and clip seams."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = Path('E:/Sectores/Sector_Modelado_3D/Ballesta_Astra_Animacion_Guardia_v01/scripts/verify_hkx.py')


def main():
    spec = importlib.util.spec_from_file_location('independent_hkx_validator',REFERENCE)
    v = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v)
    reader = v.load_reader(v.DEFAULT_PARSER)
    skeleton = reader.load_skyrim_skeleton(str(v.DEFAULT_SKELETON))
    report = {'success':True,'clips':{},'continuity':{},'game_tested':False,
              'reader':'independent PyNifly HKX reader, Read40Quat center corrected to 2047',
              'validator_sha256':v.sha256(REFERENCE),'skeleton_sha256':v.sha256(v.DEFAULT_SKELETON)}
    hold = reader.load_skyrim_animation(str(ROOT/'source/anim/astra_guard_operate.hkx'))
    for name,duration in [('operate',2.),('fire',1.),('turn_left',.8),('turn_right',.8)]:
        clip = ROOT/'source/anim'/f'astra_guard_{name}.hkx'
        xml = ROOT/'build/guard-v23/animations'/clip.with_suffix('.xml').name
        result = v.validate_clip(clip,reader,skeleton,duration,round(duration*30)+1,xml)
        cont = v.endpoint_continuity(hold,reader.load_skyrim_animation(str(clip)),skeleton)
        report['clips'][name] = result
        report['continuity'][name] = cont
        report['success'] &= result['passed'] and all(x['passed'] for x in cont.values())
        print(name,'PASS' if result['passed'] and all(x['passed'] for x in cont.values()) else 'FAIL')
    (ROOT/'reports/hkx_validation_v23.json').write_text(json.dumps(v.json_safe(report),indent=2,allow_nan=False)+'\n')
    return 0 if report['success'] else 1


if __name__ == '__main__':raise SystemExit(main())
