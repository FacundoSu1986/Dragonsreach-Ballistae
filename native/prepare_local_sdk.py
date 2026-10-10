"""Extract cached official SDK inputs locally; performs no global SDK repair/install."""
from pathlib import Path
import subprocess,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'build/native/windows_sdk'
PACKAGES=[
 Path(r'C:\ProgramData\Package Cache\{2BBE2DFA-6106-03E7-2F10-974C16AF6F63}v10.1.26100.8249\Installers\Universal CRT Headers Libraries and Sources-x86_en-us.msi'),
 Path(r'C:\ProgramData\Package Cache\{28C90E10-A917-28CE-DC76-63B86B801968}v10.1.26100.8249\Installers\Windows SDK Desktop Headers x64-x86_en-us.msi'),
 Path(r'C:\ProgramData\Package Cache\{2C985DD5-2B48-49A4-11B4-22EAF4B77565}v10.1.26100.8249\Installers\Windows SDK for Windows Store Apps Headers-x86_en-us.msi'),
]
def main():
 TARGET.mkdir(parents=True,exist_ok=True)
 receipt=[]
 for index,package in enumerate(PACKAGES):
  if not package.is_file():raise RuntimeError(f'Existing SDK cache unavailable: {package}')
  subprocess.run(['msiexec.exe','/a',str(package),'/qn',f'TARGETDIR={TARGET}','/L*v',str(TARGET/f'extract_{index}.log')],check=True)
  receipt.append({'package':str(package),'sha256':hashlib.sha256(package.read_bytes()).hexdigest(),'operation':'administrative extraction to project only'})
 (ROOT/'reports/native_sdk_receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
if __name__=='__main__':main()
