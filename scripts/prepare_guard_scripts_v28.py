"""Regenerate v28 lifecycle using unchanged persistent placement revision 26."""
from pathlib import Path
import prepare_guard_scripts_v24 as V24
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':V24.main(ROOT/'scripts/guard_runtime_v28.pscinc',revision=26)
