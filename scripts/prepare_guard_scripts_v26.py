"""Keep persisted v23 state and exclusive aliases; prepare shield-free v26 operators."""
from pathlib import Path
import prepare_guard_scripts_v24 as V24
ROOT=Path(__file__).resolve().parents[1]
def main():
    V24.main(ROOT/'scripts/guard_runtime_v26.pscinc',revision=26)
if __name__=='__main__':main()
