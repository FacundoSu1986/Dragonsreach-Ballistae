"""Preserve the low v12 layout and add the measured depression envelope."""
import json
import math
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.with_name('Ballesta_Astra_Vanilla_SE_v12')
def main():
    cfg = json.loads((BASE/'config.json').read_text(encoding='utf-8'))
    cfg['source'] = str(ROOT/'source/Torre_Ballesta_lowpoly_v04.blend')
    cfg['pitch_min'] = -20.0
    cfg['tower_v11']['note'] = 'v13: low tower, railing fitted below the -20 degree firing envelope.'
    cfg['revision_v13'] = {'base':str(BASE), 'depression':-20.0, 'game_tested':False,
                          'core_has_world_placements':False, 'city_placements_optional':True}
    import v11_layout as L
    from verify_shot_clearance_v12 import Aim
    muzzle,bore = Aim(cfg).pose(0,-20)
    V,_ = L.nif_triangles(Path(cfg['extracted'])/'meshes'/cfg['tower_v11']['escudos']['modl'])
    for item in cfg['tower_v11']['escudos']['items']:
        m = L.transform_matrix(item['pos'],item['rot_deg'],1,*L.engine_convention())
        points = [L.apply(m,v) for v in V]
        required = max(z-(muzzle[2]+(math.hypot(x,y)-math.hypot(*muzzle[:2]))*bore[2]/math.hypot(*bore[:2])-12)
                       for x,y,z in points)
        item['pos'][2] -= max(0,float(required))
        item.pop('wood_contact_units',None)
    (ROOT/'config.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
    print('V13_CONFIG',cfg['pitch_min'],cfg['tower_top_units'])
if __name__=='__main__':main()
