"""Keep v23 persisted state and v24 exclusive aliases; reanchor once for v25."""
from pathlib import Path
import prepare_guard_scripts_v24 as V24

ROOT=Path(__file__).resolve().parents[1]


def main():
    V24.main(ROOT/'scripts/guard_runtime_v25.pscinc',revision=25)


if __name__=='__main__':main()
