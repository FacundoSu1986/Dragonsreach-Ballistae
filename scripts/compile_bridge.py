"""Compile the bridged guard script and verify the FROZEN .pex is a faithful compile.

Portado desde Ballesta_Astra_Unificado_v01/scripts/compile_bridge.py, con dos cambios.

1. El compilador de Papyrus NO es determinista. Dos corridas identicas sobre el mismo
   .psc producen .pex con bytes distintos: se reordena la tabla de variables, se
   renumeran las etiquetas y cambian los timestamps. Medido en esta maquina:
   5d747153... y 48c05732... para el mismo fuente. Por eso el repo CONGELA el .pex y su
   desensamblado (`mod/scripts/AstraAsedioGuard.pex` y
   `reports/papyrus_bytecode/AstraAsedioGuard.disassemble.pas`): el sha del paquete
   tiene que ser estable.
2. En consecuencia este script ya no copia el .pex compilado encima del congelado.
   Compila en un temporal y exige que el resultado sea SEMANTICAMENTE identico al
   congelado. La comparacion normaliza lo unico que varia (timestamps, numero de
   etiqueta y anotacion `;@line`) y exige que el multiconjunto de instrucciones coincida.

Requiere el runtime del juego en G:/Modding/Skyrim_Runtime_1.6.1170 (dependencia
externa, no se versiona).
"""
import hashlib, json, re, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from pex_metadata import anonymize
from compile_papyrus import validate_assembly

FROZEN_PEX=ROOT/'mod/scripts/AstraAsedioGuard.pex'
FROZEN_PAS=ROOT/'reports/papyrus_bytecode/AstraAsedioGuard.disassemble.pas'


def normalize(text):
    """Deja solo lo que el compilador no puede reordenar sin cambiar la semantica."""
    text=re.sub(r'^\s*\.(modify|compile)Time .*$','',text,flags=re.M)
    text=re.sub(r'_label\d+','_label',text)
    text=re.sub(r';@line \d+','',text)
    return sorted(line.rstrip() for line in text.splitlines() if line.strip())


def main():
    runtime=Path(r'G:\Modding\Skyrim_Runtime_1.6.1170')
    src=ROOT/'mod/scripts/source';p=src/'AstraAsedioGuard.psc';digest=hashlib.sha256(p.read_bytes()).hexdigest()
    compiler=runtime/'Papyrus Compiler/PapyrusCompiler.exe';assembler=runtime/'Papyrus Compiler/PapyrusAssembler.exe'
    imports=';'.join(str(q) for q in (src,runtime/'Data/Scripts/Source',runtime/'Data/Source/Scripts'))
    stage_root=ROOT/'build';stage_root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='astra_guard_',dir=stage_root) as td:
        stage=Path(td)
        args=[str(compiler),str(p),'-f='+str(runtime/'Data/Source/Scripts/TESV_Papyrus_Flags.flg'),'-i='+imports,'-o='+str(stage)]
        r=subprocess.run(args,capture_output=True,text=True);print(r.stdout+r.stderr)
        assert r.returncode==0,'Papyrus compile failed'
        q=stage/'AstraAsedioGuard.pex';q.write_bytes(anonymize(q.read_bytes()))
        a=subprocess.run([str(assembler),'AstraAsedioGuard','-D'],cwd=stage,capture_output=True,text=True);print(a.stdout+a.stderr)
        assert a.returncode==0
        pas=stage/'AstraAsedioGuard.disassemble.pas';safety=validate_assembly(pas.read_text(encoding='utf-8-sig'))
        assert digest==hashlib.sha256(p.read_bytes()).hexdigest(),'el .psc cambio durante la compilacion'
        assert FROZEN_PEX.is_file() and FROZEN_PAS.is_file(),'faltan los artefactos congelados'
        faithful=normalize(pas.read_text(encoding='utf-8-sig'))==normalize(FROZEN_PAS.read_text(encoding='utf-8-sig'))
        assert faithful,'el .pex congelado NO es un compilado fiel del .psc actual'
        report={'success':True,'source_sha256':digest,
                'pex_sha256':hashlib.sha256(FROZEN_PEX.read_bytes()).hexdigest(),
                'disassembly_sha256':hashlib.sha256(FROZEN_PAS.read_bytes()).hexdigest(),
                'pex_recompiled_sha256':hashlib.sha256(q.read_bytes()).hexdigest(),
                'disassembly_recompiled_sha256':hashlib.sha256(pas.read_bytes()).hexdigest(),
                'compiler_deterministic':False,
                'frozen_pex_is_faithful_compile':faithful,
                'bytecode_safety':safety,
                'other_scripts_recompiled':False}
        (ROOT/'reports/guard_compile.json').write_text(json.dumps(report,indent=2))
        print('GUARD_VERIFIED',report['pex_sha256'],report['pex_recompiled_sha256'])


if __name__=='__main__':main()
