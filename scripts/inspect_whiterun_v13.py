"""Read vanilla location/actor data; do not modify the game installation."""
import sys,json,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/vendor')]
from parser_esm import Plugin

def main():
    cfg=json.loads((ROOT/'config.json').read_text()); out={'cells':[],'doors':[],'guards':[],'refs':[]}
    p=Plugin(str(Path(cfg['runtime'])/'Data/Skyrim.esm'))
    cell=0; cellname=''; world=0; stack=[]
    for t,o,n,depth in p.recorrer():
        if t=='GRUP':
            typ,label=struct.unpack_from('<i',p.d,o+12)[0],struct.unpack_from('<I',p.d,o+8)[0]
            stack[depth:]=[(typ,label)]
            continue
        if t not in ('CELL','WRLD','DOOR','NPC_','REFR','ACHR','LAND'):continue
        ss=dict(p.subrecords(p.datos(o))); fid=p.form_id(o)
        ed=ss.get('EDID',b'').rstrip(b'\0').decode('cp1252')
        if t=='WRLD':world=fid
        if t=='CELL':
            cell=fid;cellname=ed
            if ed.startswith('Whiterun'):
                out['cells'].append({'id':f'{fid:08X}','edid':ed,'world':f'{world:08X}',
                                     'grid':list(struct.unpack('<2i',ss['XCLC'][:8])) if 'XCLC'in ss else None,'chain':stack[:depth]})
        if t=='DOOR' and ('Whiterun' in ed or 'WR' in ed):out['doors'].append({'id':f'{fid:08X}','edid':ed})
        if t=='NPC_' and 'Whiterun' in ed and 'Guard' in ed:
            out['guards'].append({'id':f'{fid:08X}','edid':ed,'subs':{k:len(v) for k,v in ss.items()},
                                  'template':ss.get('TPLT',b'').hex(),'acbs':ss.get('ACBS',b'').hex()})
        if t in ('REFR','ACHR') and (cellname.startswith('WhiterunExterior') or cellname.startswith('WhiterunGate') or 'Whiterun' in ed or
                                  ('DATA' in ss and abs(struct.unpack_from('<f',ss['DATA'])[0]-19312)<1800 and abs(struct.unpack_from('<f',ss['DATA'],4)[0]+7424)<1800)):
            if 'DATA'not in ss:continue
            refworld=next((label for typ,label in stack[:depth] if typ==1),0)
            out['refs'].append({'id':f'{fid:08X}','type':t,'edid':ed,'cell':f'{cell:08X}','cellname':cellname,'world':f'{refworld:08X}',
                                'scale':struct.unpack('<f',ss['XSCL'])[0] if 'XSCL'in ss else 1.0,
                                'base':f'{struct.unpack("<I",ss["NAME"])[0]:08X}' if 'NAME'in ss else '',
                                'data':list(struct.unpack('<6f',ss['DATA']))})
    (ROOT/'reports/whiterun_vanilla.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({k:v for k,v in out.items() if k!='refs'},indent=2))
    print('Refs',len(out['refs']))
if __name__=='__main__':main()
