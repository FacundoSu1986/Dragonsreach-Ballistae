"""Keep the initial task receipt and link it to verified final integration."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    verification=ROOT/'reports/verification_v14.json';v=json.loads(verification.read_text());assert v['success']
    current=ROOT/'reports/v14_cadence_verification.json';initial=ROOT/'reports/v14_cadence_verification_initial.json'
    if not initial.exists():initial.write_bytes(current.read_bytes())
    r=json.loads(initial.read_text())
    r['initial_stage_receipt']={'path':str(initial.relative_to(ROOT)),'sha256':sha(initial)}
    r['initial_stage_source_regression_green']=r.pop('fresh_source_regression_green')
    r['status']='Final cadence/VMAD/PEX integration verified; initial source-stage tests preserved separately'
    r['integration_checks_pending']=[];r['final_pex_written']=True
    r['final_verification']={'path':str(verification.relative_to(ROOT)),'sha256':sha(verification),'output':v['output']}
    r['v14_after_sha256']={n:sha(ROOT/n) for n in r['v14_after_sha256']}
    r['additional_sector_properties']={'YawCenter':0.,'YawHalfSector':60.,'measured_per_reference':True}
    current.write_text(json.dumps(r,indent=2))
    md=ROOT/'reports/v14_cadence.md';body=md.read_text(encoding='utf-8')
    if not body.startswith('# Cierre de integración v14'):
        md.write_text('# Cierre de integración v14\n\nLa integración final ya está verificada: 359 pruebas y 162 subtests, VMAD temporal nuevo y cinco PSC/PEX/desensamblados Bethesda coherentes. `verification_v14.json` describe la entrega; `v14_cadence_verification_initial.json` conserva el recibo de la etapa inicial. El texto de abajo describe esa etapa histórica (incluidas sus comprobaciones entonces pendientes). Después se agregaron los sectores medidos YawCenter/YawHalfSector.\n\n'+body,encoding='utf-8')
    print('V14_CADENCE_INTEGRATION_CLOSED')
if __name__=='__main__':main()
