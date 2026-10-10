"""Retime animation bytes only, retaining every spatial/shader/collision byte.

Supports the exported SSE 20.2.0.7/BS100 layout, checked against PyNifly.
Quadratic tangents are interval-normalized in PyNifly, so values stay intact.
"""
from pathlib import Path
import json,sys,struct,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts/vendor'))
import nif_nodos
def sha(data):return hashlib.sha256(data).hexdigest()

def transform_times(raw,off,size):
    """Return only time offsets; fail closed on unsupported key layouts."""
    pos=off;times=[]
    def count():
        nonlocal pos
        n=struct.unpack_from('<I',raw,pos)[0];pos+=4;return n
    def group(dims):
        nonlocal pos
        n=count()
        if not n:return
        kind=count();assert kind in (1,2),kind
        stride=4+4*dims*(3 if kind==2 else 1)
        for _ in range(n):times.append(pos);pos+=stride
    n=count()
    if n:
        kind=count()
        if kind==4:
            assert n==1
            for _ in range(3):group(1)
        else:
            assert kind in (1,2),kind
            for _ in range(n):times.append(pos);pos+=20
    group(3);group(1)
    assert pos==off+size,(pos,off+size)
    return times

def retime(path,durations):
    binary=nif_nodos.leer(str(path));raw=binary['datos'];out=bytearray(raw);patches={};sequences={};data_owners={}
    assert binary['bs']==100
    def change(offset,value):
        assert offset not in patches or abs(patches[offset]-value)<1e-6
        patches[offset]=value;struct.pack_into('<f',out,offset,value)
    for typ,off,size in binary['bloques']:
        if typ!='NiControllerSequence':continue
        name=binary['strings'][struct.unpack_from('<I',raw,off)[0]]
        count=struct.unpack_from('<I',raw,off+4)[0]
        # NiSequence header: name,count,arrayGrowBy; SSE ControlledBlock=29 bytes.
        cursor=off+12+count*29
        start_offset=cursor+16;start,stop=struct.unpack_from('<ff',raw,start_offset)
        assert start==0 and stop>0 and name in durations
        factor=durations[name]/stop
        change(start_offset+4,durations[name])
        for i in range(count):
            interp=struct.unpack_from('<i',raw,off+12+i*29)[0]
            it,io,sz=binary['bloques'][interp];assert it=='NiTransformInterpolator' and sz==36
            data=struct.unpack_from('<i',raw,io+32)[0]
            assert data not in data_owners or data_owners[data]==name
            data_owners[data]=name
            dt,do,ds=binary['bloques'][data];assert dt=='NiTransformData'
            for offset in transform_times(raw,do,ds):
                old=struct.unpack_from('<f',raw,offset)[0];assert math.isfinite(old) and 0<=old<=stop+.001
                change(offset,old*factor)
        text=struct.unpack_from('<i',raw,cursor+4)[0]
        assert text==-1,'Text keys require an explicit retimer'
        sequences[name]={'old_seconds':stop,'new_seconds':durations[name],'factor':factor}
    assert set(sequences)=={'Fire','Reset'}
    # Shared controller time bounds are +/- infinity, intentionally unchanged.
    for typ,off,size in binary['bloques']:
        if typ in ('NiControllerManager','NiMultiTargetTransformController'):
            assert struct.unpack_from('<ff',raw,off+14)==(float('inf'),float('-inf'))
    masked=bytearray(out)
    for off in patches:masked[off:off+4]=raw[off:off+4]
    assert masked==raw,'Only registered timing floats may differ'
    return bytes(out),{'sequences':sequences,'timing_floats':len(patches),'spatial_values_shaders_collision_unchanged':True,'before_sha256':sha(raw),'after_sha256':sha(out)}

def main():
    cfg=json.loads((ROOT/'config.json').read_text());old=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v06')/'mod/meshes/AstraAsedio/ballesta.nif'
    baseline=json.loads((ROOT/'reports/v07_baseline.json').read_text())
    assert sha(old.read_bytes())==baseline['parent_sha256']['mod\\meshes\\AstraAsedio\\ballesta.nif']
    data,report=retime(old,{'Fire':cfg['fire_seconds'],'Reset':cfg['reset_seconds']})
    (ROOT/'mod/meshes/AstraAsedio/ballesta.nif').write_bytes(data)
    (ROOT/'reports/animation_retime.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
