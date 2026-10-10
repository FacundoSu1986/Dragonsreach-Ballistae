import json,sys,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
from parser_esm import Plugin
cfg=json.loads((ROOT/'config.json').read_text())
refs=json.loads((ROOT/'reports/whiterun_vanilla.json').read_text())['refs']
near=[r for r in refs if r['world']=='0000003C' and (r['data'][0]-19312)**2+(r['data'][1]+7424)**2<4000**2]
wanted={int(r['base'],16) for r in near if r['base']}
p=Plugin(str(Path(cfg['runtime'])/'Data/Skyrim.esm')); donors={}
for t,o,n,depth in p.recorrer():
    if t=='GRUP' or p.form_id(o)not in wanted:continue
    ss=dict(p.subrecords(p.datos(o)))
    donors[f'{p.form_id(o):08X}']={'edid':ss.get('EDID',b'').rstrip(b'\0').decode('cp1252'),
                                'model':ss.get('MODL',b'').rstrip(b'\0').decode('cp1252'),'type':t}
for r in near:r['donor']=donors.get(r['base'],{})
(ROOT/'reports/gate_models_v13.json').write_text(json.dumps(near,indent=2))
for r in near:
    if r['donor'].get('model'):print(r['id'],r['cellname'],r['data'][:3],r['donor']['model'])
