"""Constructed LTL witness visualization; not external benchmark data."""
import json
import os
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
from xml.sax.saxutils import escape
from src.assumption_lasso_witness import find_counterexample, parse, _truth

def main():
    out = Path("artifacts/constructed_ltl"); out.mkdir(parents=True, exist_ok=True)
    a = find_counterexample("G prop_0", "G prop_1", max_states=3, max_propositions=2)
    b = find_counterexample("G prop_0", "G prop_1", max_states=3, max_propositions=2,
                            equalities=(("prop_0", "prop_1"),))
    assert a["status"] == "witness" and a["witness_states"] == 1 and a["loop_start"] == 0, a
    assert b["status"] == "no_witness_within_bound", b
    # Independently verify the concrete one-state constructed valuation using evaluator.
    vals = {"prop_0": 1, "prop_1": 0}
    left = bool(_truth(parse("G prop_0"), vals, 1, 0) & 1)
    right = bool(_truth(parse("G prop_1"), vals, 1, 0) & 1)
    assert left is True and right is False
    # Under identity, both formula satisfaction values must match on each 1-state valuation.
    for bit in (0, 1):
        v = {"prop_0": bit, "prop_1": bit}
        assert bool(_truth(parse("G prop_0"), v, 1, 0) & 1) == bool(_truth(parse("G prop_1"), v, 1, 0) & 1)
    record = {"protocol":"028","data_kind":"constructed_fixture_not_external_AI",
              "formulas":["G prop_0","G prop_1"],"unconstrained":a,
              "assumed_equal":b,"example":{"states":1,"loop_start":0,"prop_0":True,
              "prop_1":False,"G_prop_0":left,"G_prop_1":right},
              "caveat":"Finite no-witness result is not proof of unrestricted equivalence."}
    raw=json.dumps(record,indent=2,sort_keys=True)+"\n"
    (out/"result.json").write_text(raw)
    svg='''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="560" viewBox="0 0 1000 560">
<rect width="1000" height="560" fill="white"/>
<g font-family="DejaVu Sans,Arial,sans-serif" fill="#161616">
<text x="48" y="55" font-size="26" font-weight="bold">Constructed LTL witness: proposition identity matters</text>
<text x="48" y="87" font-size="15">Formulas: G prop_0 versus G prop_1 · bounded infinite-lasso checker · protocol 028</text>
<line x1="48" y1="105" x2="952" y2="105" stroke="#999"/>
<text x="48" y="148" font-size="19" font-weight="bold">A · Unconstrained propositions</text>
<text x="48" y="180" font-size="16">One-state infinite lasso (state 0 loops to itself)</text>
<rect x="60" y="206" width="290" height="148" rx="8" fill="#f6f6f6" stroke="#555"/>
<text x="82" y="241" font-size="18">state 0</text>
<text x="82" y="277" font-size="17">prop_0 = true</text>
<text x="82" y="310" font-size="17">prop_1 = false</text>
<path d="M 350 256 C 430 195, 430 355, 350 310" fill="none" stroke="#444" stroke-width="2"/>
<path d="M 352 310 l 12 -1 l -7 -10" fill="none" stroke="#444" stroke-width="2"/>
<text x="455" y="248" font-size="17">G prop_0 = true</text>
<text x="455" y="281" font-size="17">G prop_1 = false</text>
<text x="455" y="322" font-size="17" font-weight="bold">Result: counterexample found</text>
<line x1="48" y1="380" x2="952" y2="380" stroke="#bbb"/>
<text x="48" y="420" font-size="19" font-weight="bold">B · Assume prop_0 = prop_1 at every state</text>
<text x="48" y="456" font-size="17">Result: no witness within 3 states (bounded search)</text>
<text x="48" y="488" font-size="15">Identity is an imposed assumption, not a measured physical fact.</text>
<text x="48" y="526" font-size="13">Constructed example only · not external AI evaluation or validated physical dynamics</text>
</g></svg>'''
    (out/"witness.svg").write_text(svg)
    # SVG is an original vector research output, directly emitted by this program.
    manifest={"generated_utc":datetime.now(timezone.utc).isoformat(),"commit":os.getenv("GITHUB_SHA","unknown"),
              "command":"python3 -m src.render_constructed_ltl","protocol":"028",
              "files":{p.name:sha256(p.read_bytes()).hexdigest() for p in (out/"result.json",out/"witness.svg")}}
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(json.dumps({"unconstrained":a,"assumed_equal":b,"output":str(out),"sha256":manifest["files"]},indent=2))

if __name__=="__main__": main()
