#!/usr/bin/env python3
"""Mechanical grading for the deliberate benchmark.

Only checks assertions that can be decided by inspecting text — a URL is present or it
is not, a stage marker matches or it does not. Judgment assertions ("does the concept
cite a real evidence row") are left for a human read and reported as UNGRADED rather
than guessed at, because a script that fakes a judgment call is worse than no script.

Usage: python3 grade.py <iteration-dir>
"""
import json, os, re, sys

def load(p):
    try:
        return open(p, encoding="utf-8", errors="ignore").read()
    except OSError:
        return None

# (assertion text, kind, predicate) — kind "auto" is decided here, "read" needs eyes
CHECKS = {
 "eval-0-ambiguous-frame": [
   ("Names that the question has more than one reading, and states both", "auto",
    lambda t: len(re.findall(r"\breading\b", t, re.I)) >= 2),
   ("Stops and puts the frame to the decider before proceeding", "auto",
    lambda t: bool(re.search(r"\b(stopp?ed|halt(ed)?|waiting on the decider|awaiting)\b", t, re.I))),
   ("Does NOT spawn research lanes or produce evidence rows before confirmation", "auto",
    lambda t: not re.search(r"\|\s*Claim\s*\|\s*Source", t, re.I)),
   ("States which reading it would take, rather than only asking", "auto",
    lambda t: bool(re.search(r"which I would take|I would take|would take:?\s*\*?\*?read", t, re.I))),
   ("Explains why the frame specifically cannot be defaulted", "auto",
    lambda t: bool(re.search(r"inherits? the frame|wastes? the (entire|whole) run|downstream", t, re.I))),
 ],
 "eval-1-fresh-inspiration": [
   ("Runs a Lightning Demo round as a distinct, named step", "auto",
    lambda t: bool(re.search(r"lightning demo", t, re.I))),
   ("At least 3 examples carry a URL", "auto",
    lambda t: len(set(re.findall(r"https?://[^\s\)\]\|>»\"']+", t))) >= 3),
   ("At least 2 examples come from OUTSIDE accounting/professional services", "read", None),
   ("Each big idea names its source and the transferable component", "auto",
    lambda t: len(re.findall(r"seen at|big idea|the component", t, re.I)) >= 3),
   ("Concept cards cite both an evidence row and a borrowed big idea", "read", None),
 ],
 "eval-2-stops-early": [
   # Substance, not phrasing: does the reader learn how much is LEFT? A stage count
   # does it; so does an explicit list of stages not yet run. Both count.
   ("Communicates how much of the process remains (stage count OR named list of stages not run)", "auto",
    lambda t: bool(re.search(r"stage\s+\d+\s+of\s+\d+", t, re.I))
              or bool(re.search(r"(skipped|not run|did not run|remaining|still to run)\s*:?[^\n]{0,120}"
                                r"(IDEATE|CONTEST|DECIDE|ROADMAP)", t, re.I))),
   ("Makes incompleteness unmistakable, not inferable", "auto",
    lambda t: bool(re.search(r"\bunfinished\b|\bincomplete\b|\bnot (yet )?complete\b"
                             r"|no (decision|recommendation) (appears|was made|is made)"
                             r"|stopped (after|before|at)\b|halted\b", t, re.I))),
   # The property that actually matters: a skimmer must not mistake it for an answer.
   ("Incompleteness is visible in the opening 600 characters, not buried", "auto",
    lambda t: bool(re.search(r"unfinished|incomplete|skipped|not run|stopped|halted|what ran"
                             r"|stage\s+\d+\s+of\s+\d+", t[:600], re.I))),
   ("Names what is still owed or what happens next", "auto",
    lambda t: bool(re.search(r"\bowed\b|still (owed|remain|outstanding)|next session|resume|to resume"
                             r"|next steps?\b|in order:", t, re.I))),
   ("Does NOT present gathered evidence as a decision or recommendation", "auto",
    lambda t: not re.search(r"^\s*(##\s*)?(decision|recommendation)\s*:?\s*(proceed|drop|kill|we should)", t, re.I | re.M)),
   ("Evidence rows carry sources rather than unsourced assertions", "auto",
    lambda t: bool(re.search(r"https?://", t)) or bool(re.search(r"\|\s*Source", t, re.I))),
 ],
}

def grade(itdir):
    out = {}
    for ev in sorted(os.listdir(itdir)):
        d = os.path.join(itdir, ev)
        if not os.path.isdir(d) or ev not in CHECKS:
            continue
        for cfg in sorted(os.listdir(d)):
            resp = os.path.join(d, cfg, "outputs", "response.md")
            if not os.path.isfile(resp):
                continue
            t = load(resp) or ""
            exps = []
            for text, kind, pred in CHECKS[ev]:
                if kind == "read":
                    exps.append({"text": text, "passed": None,
                                 "evidence": "UNGRADED - needs a human read; not guessed"})
                else:
                    ok = bool(pred(t))
                    exps.append({"text": text, "passed": ok,
                                 "evidence": ("matched" if ok else "no match") + f" in {len(t)} chars"})
            auto = [e for e in exps if e["passed"] is not None]
            res = {"eval": ev, "config": cfg, "expectations": exps,
                   "passed": sum(1 for e in auto if e["passed"]), "gradeable": len(auto),
                   "urls_found": len(set(re.findall(r"https?://[^\s\)\]\|>»\"']+", t))),
                   "chars": len(t)}
            json.dump(res, open(os.path.join(d, cfg, "grading.json"), "w"), indent=2)
            out[f"{ev}/{cfg}"] = res
    return out

if __name__ == "__main__":
    it = sys.argv[1] if len(sys.argv) > 1 else "iteration-1"
    r = grade(it)
    if not r:
        print("no graded runs found in", it); sys.exit(1)
    print(f"{'run':52} {'auto':>7}  {'urls':>4}  {'chars':>6}")
    for k, v in sorted(r.items()):
        print(f"{k:52} {v['passed']}/{v['gradeable']:<5}  {v['urls_found']:>4}  {v['chars']:>6}")
    print("\nUNGRADED assertions need a human read - they are not counted above.")
