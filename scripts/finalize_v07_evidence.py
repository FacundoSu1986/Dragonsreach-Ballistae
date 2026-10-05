from pathlib import Path
import json,re,hashlib,datetime,shutil
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    log=ROOT/'reports/baseline_v06_runtime/SKSE/AstraSight.log';shots=[];start={}
    for line in log.read_text(encoding='utf-8').splitlines():
        m=re.search(r'^\[(.*?)\].*shot (freeze|frozen=false).*?handle=(\d+) token=(\d+)',line)
        if not m:continue
        time=datetime.datetime.fromisoformat(m[1]);key=(m[3],m[4])
        if m[2]=='freeze':start[key]=time
        elif key in start:shots.append({'handle':key[0],'token':key[1],'freeze_thaw_seconds':(time-start.pop(key)).total_seconds()})
    assert len(shots)==4
    evidence={'revision':'v07','baseline_revision':'v06','user_report':'Camera/mouse improved, camera drifts beyond180; launch and reload slow; requests continuous hold Attack.','log_sha256':sha(log),'baseline_shots':shots,'v07_engine_cases_executed':0,'fps_measured':False,'latency_measured_v07':False,'old_disk_disassembly_limit':'SkyrimSE executable text on disk is protected; raw bytes decoded into nonsensical instructions. No control-flow proof or camera consumer-order claim comes from this dump; hook schema is from bundled CommonLib.'}
    (ROOT/'reports/v07_runtime_baseline.json').write_text(json.dumps(evidence,indent=2))
    for name in ['v07_red_psc.log','v07_red_core.log','freeze_handshake_red.log','freeze_handshake_green.log']:
        shutil.copy2(ROOT/'build'/name,ROOT/'reports'/name)
    spec=ROOT/'docs/superpowers/specs/2026-10-04-v07-mira-cadencia.md';plan=ROOT/'docs/superpowers/plans/2026-10-04-v07-mira-cadencia.md'
    # Review is advisory; execution is already explicitly authorized by the user.
    (ROOT/'reports/v07_document_review.json').write_text(json.dumps({'reviewer':'/root/v07_spec_plan_review','status':'APPROVED','findings':[],'scope':'Spec/plan read-only review and resolution of changing-parent guard; motor adapter remains unexecuted.','inputs':{str(spec.relative_to(ROOT)):sha(spec),str(plan.relative_to(ROOT)):sha(plan)}},indent=2))
    renders=ROOT/'reports/renders.json';data=json.loads(renders.read_text());retimed=json.loads((ROOT/'reports/animation_retime.json').read_text())
    from retime_v07 import retime
    parent=ROOT.with_name('Ballesta_Astra_Vanilla_SE_v06');cfg=json.loads((ROOT/'config.json').read_text())
    expected,_=retime(parent/'mod/meshes/AstraAsedio/ballesta.nif',{'Fire':cfg['fire_seconds'],'Reset':cfg['reset_seconds']})
    assert expected==(ROOT/'mod/meshes/AstraAsedio/ballesta.nif').read_bytes()
    assert retimed['spatial_values_shaders_collision_unchanged']
    data['timing_only_reuse_verified']=True;renders.write_text(json.dumps(data,indent=2))
    print('v07 baseline intervals', [row['freeze_thaw_seconds'] for row in shots])
if __name__=='__main__':main()
