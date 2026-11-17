import sys; from pathlib import Path
HERE = Path(__file__).parent; sys.path.insert(0, str(HERE.parents[1] / "scripts"))
import glow_short as g, logo_sting as ls
if "--quer" in sys.argv: g.querformat()
html, code = ls.szene(querformat="--quer" in sys.argv)
g.build(HERE, [(0.0, ls.DAUER, html, code)], ls.sounds(0.0), dauer=ls.DAUER, drift=False)
