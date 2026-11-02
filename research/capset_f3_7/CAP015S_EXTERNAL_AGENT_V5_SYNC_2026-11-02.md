# CAP-015S — Minimal-fix synchronization of external-agent Campaign 001 v5.0 (2026-11-02)

## Scope and import decision
**Keep the other agent's mathematics and 4-group research architecture.** The Drive v5.0 sources contain useful conditional/global structure, but not all of their exhaustive classification and orbit claims have independent GitHub certificates. The scope is importing source/evidence, fixing two audit deficiencies and small portability details, **not** asserting r3(7) solved.

Source files (preserved unchanged on Drive):
- Original v5 Python: https://drive.google.com/file/d/1DpIvdoPFbw253UZ1Ko6LHC6I9KqG3Y45/view — SHA256 `28549c6306091b832c352a718845cecce67052e2f577a39b6ec49f185d724ea1`.
- Original v5 JSON: https://drive.google.com/file/d/1M9FSNowfaxI3jnxwQD0ODjYjpWCsw5oz/view — SHA256 `f1619bb1fa4ef812e52415dda5af2e94d85f81027abb44d8da9a793b4a826f37`.

Imported GitHub copies:
- `external_agent_v5/capset_swarm_v5_fixed.py` — original script with minimal edits only.
- `external_agent_v5/capset_swarm_v5_corrected_evidence.json` — source-derived complete witness bundle; specifically corrected three CAP-011A boolean flags using direct independent arithmetic replay, with correction metadata. Other complex claims **remain source claims**, not automatically proven by this import.
- `test_cap015_external_agent_v5_sync.py` — standalone, no-GPU, no-OR-Tools independent arithmetic regression.

## Minimal fixes made
1. **CAP-011A real error**: replace `Q = centered.T @ centered mod3` by **`Q = -centered.T @ centered mod3`**, since after centroid translation `a1=a2` and `a1+a2=\sum(d.y)^2\pmod3`. Add `assert paired_ok and quad_formula_exact` so false audit booleans cannot silently pass. Update only corresponding three previously false flags in the imported JSON (n7=236, n8=496, n8=512). The n6=112 zero-Q case remains true.
2. **CAP-010B evidence scope**: the original script's SVD/eigvalsh still uses floating point and must be named *numerical diagnostics*, not an exact proof on its own. The separate existing `cap010b_exact_psd_certificate.py` now supplies exact integer PSD/rank certificate for the **fixed classical H/H' pair only**; this independently passed CI (run 41449380778). Its `425/576` spectral bound may be used only with that scope; arbitrary relative GL(6,3) alignments remain unproved from this.
3. **Portability**: replace an unavailable `/working_dir/...` output path with a relative file beside the source. Optional OR-Tools import permits arithmetic imports without installing a solver; orbit solving still explicitly requires OR-Tools.
4. **Audit honesty**: correct the CAP-012 audit text implying original v5 code had eliminated all floating-point reliance; retain all substantive research methods and published classifications.

## Independent bounded verification
Commands (local Python 3, stdlib plus already installed NumPy for the one function call; no GPU or paid compute):
```bash
python -m py_compile research/capset_f3_7/external_agent_v5/capset_swarm_v5_fixed.py
python -m unittest discover -s research/capset_f3_7 -p 'test_cap015_external_agent_v5_sync.py' -v
python research/capset_f3_7/cap010b_exact_psd_certificate.py
```
Independent standalone test (local import-path mirror): **4 tests passed in 4.366s**. Tested direct mod-3 cap/no-collinear-pair arithmetic for all 112-,236-,496-,512-point witnesses; exact majority-residue quadratic law at **all 8,017 projective directions** (364 + 1093 + 3280 + 3280); exact codimension-2 moments for hypothetical M=237: `23572731, 639439983, 17775438687`; Python source AST and corrected sign assertions. A direct isolated call to the patched original `prove_wave2_universal_quadric_and_codim2_hierarchy` also returned true for all 4 previously false/true cases.

A blank CI status **must not** be interpreted as green; see the recent branch `Cap Set F3-7 Verifier` workflow for final outcome of new `test_cap015...`. CI green for the independent CAP-014 exact PSD checker is already recorded. Do not claim all v5 exhaustive GO6 52,254,720-class or CAP-014C GL6 constraints were independently replayed in this import.

## Mathematical status / strategic audit
- **Confirmed**: CAP-011A signed formula correction; CAP-011B exact incidence moment data; CAP-011C matching lemma; CAP-014 exact restricted spectral certificate.
- **Still needs independent replay**: CAP-013A/B GO6 orbit enumeration (648), CAP-014A/B/C global group/overlap/DFS claims, CAP-015A 12-class census; literature novelty also unresolved.
- Critical global branch: any hypothetical 237-cap with **no 112-point affine hyperplane section** remains unexcluded. Restricted fixed-pair deletion obstacles cannot prove global r3(7) optimality.
- No independent >=237 witness, no new globally rigorous upper bound, no external literature novelty priority claimed. Target r3(7) remains **OPEN**.
