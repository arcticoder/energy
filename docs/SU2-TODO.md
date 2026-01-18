# SU(2) 3n-j Series — Cross-Repo TODO (Q1–Q2 2026)

Date: 2026-01-18

This TODO is the cross-repository execution plan for the SU(2) 3n-j series:

- `su2-3nj-closedform`
- `su2-3nj-uniform-closed-form`
- `su2-3nj-recurrences`
- `su2-3nj-generating-functional`
- `su2-node-matrix-elements`

The goal is to turn the existing (already substantial) derivations + scripts into a **rigorous, reproducible, publication-ready package** (2–3 paper series or one 20–30 page JMP-style paper) with:

- Clear assumptions/edge cases (half-integers, triangle/parity constraints, large spins)
- Verified identities and cross-checks (SymPy Wigner, independent implementations, numeric vs exact)
- Reproducible reference datasets and deterministic scripts
- Tight narrative: closed forms → uniform form → finite recurrences → generating functional → node matrix elements

---

## 0) High-level deliverables

### D0.1 — Reproducible validation harness (code + data)
Acceptance criteria:
- Each repo that claims a formula has a **single command** that regenerates key tables/figures and checks invariants.
- Reference datasets are versioned (JSON/CSV) and regenerated deterministically.
- CI/pytest-friendly test entrypoints exist where Python code exists.

### D0.2 — Paper-ready “master draft” (series bundle)
Preferred: a series of 2–3 papers, or one comprehensive paper.

Acceptance criteria:
- A master LaTeX build exists that can be compiled in one shot.
- Common notation is unified (spin conventions, parity rules, graph notation).
- One shared bibliography (BibTeX) with 5–10 core priors.

### D0.3 — Q2 2026 submission readiness
Acceptance criteria:
- All claims in the abstract/introduction have corresponding lemmas/propositions and at least one validation route.
- Limitations are explicit (numerical instability regimes, unsupported topologies, etc.).

---

## 1) Cross-repo technical tasks (highest leverage)

### T1 — Standardize spin domain/validation across code
Problem: half-integer spins and selection rules are common failure points.

Actions:
- Implement a shared “spin validation” policy in each repo that has Python:
  - Validate that each spin is integer or half-integer: $2j \in \mathbb{Z}$.
  - Enforce triangle inequalities and parity constraints where applicable.
  - Ensure summation bounds are computed **exactly** (avoid `int()` truncation).
- Add tests that explicitly include half-integer cases, e.g. $j=1/2, 3/2$.

Acceptance criteria:
- A half-integer dataset passes for 6j and 9j where supported.

### T2 — Deterministic “golden reference” datasets
Actions:
- Create/update canonical JSON datasets per repo:
  - 6j dataset (small spins + half-integers)
  - 9j dataset (small spins)
  - Optional: decompositions (9j→6j sums) where available
- Add scripts to regenerate references with pinned rules:
  - exact rational mode
  - numeric mode (float) with explicit tolerances

Acceptance criteria:
- Tests compare against golden datasets without network access.

### T3 — Cross-verification matrix (what checks what)
Build a table mapping:
- Formula → Implementation A → Implementation B → identity/invariant

Example checks:
- Closed form vs SymPy (`wigner_6j`, `wigner_9j`)
- Racah-summation implementation vs SymPy
- Recurrence reconstruction vs direct evaluation
- Generating functional coefficients vs direct Wigner values

Acceptance criteria:
- At least 2 independent routes validate each key claim.

### T4 — Numerical stability & UQ hooks
Actions:
- Add a simple, consistent UQ protocol:
  - sweep over spin ranges
  - track condition numbers / determinant stability (for generating functional)
  - compare rational vs numeric evaluation

Acceptance criteria:
- A “stability report” script produces a CSV/JSON summary.

---

## 2) Paper bundling / publication tasks

### P1 — Decide bundling (2–3 papers) vs single JMP draft
Suggested 3-paper arc:
1) Closed-form + uniform hypergeometric representation
2) Finite recurrences + algorithms/stability
3) Generating functionals + arbitrary-valence node matrix elements

Alternative single paper title:
- “Unified Closed-Form Representations and Generating Functionals for SU(2) 3n-j Recoupling Coefficients.”

Acceptance criteria:
- A single outline exists with section allocation and cross-references.

### P2 — Master LaTeX merge
Actions:
- Identify source LaTeX masters (per repo):
  - closed-form: `A Closed-Form Hypergeometric Product Formula for General SU(2) 3nj Recoupling Coefficients.tex`
  - uniform: `Universal Closed-Form Hypergeometric Representation of SU(2) 3nj Symbols.tex`
  - recurrences: `Closed-Form Finite Recurrences for SU(2) 3nj Symbols.tex`
  - generating functional: `A Universal Generating Functional for SU(2) 3nj Symbols.tex`
  - node matrix elements: `Closed-Form Matrix Elements for Arbitrary-Valence SU(2) Nodes via Generating Functionals.tex`
- Create a master tree (new repo recommended, e.g. `su2-3nj-series-paper/`) with:
  - shared macros
  - shared bibliography
  - appendices for proofs and code

Acceptance criteria:
- One `latexmk` command builds the full PDF.

### P3 — Literature integration (priors)
Actions:
- Add a “Related Work” section with BibTeX entries and explicit positioning.
- Integrate already-downloaded priors in `energy/papers/related/` into the bib.

Acceptance criteria:
- 5–10 relevant priors cited in intro + comparisons.

### P4 — Validation section + tables
Actions:
- Add a dedicated validation section:
  - known values (3j/6j)
  - random small-spin sampling (6j/9j)
  - identities (Biedenharn–Elliott, orthogonality)
  - recurrence cross-checks

Acceptance criteria:
- Tables/figures are reproducibly generated by scripts committed in repos.

---

## 3) Repo-specific TODOs

### 3.1 `su2-3nj-closedform`
Current assets:
- `scripts/coefficient_calculator.py`
- `scripts/symmetry_checker.py`
- LaTeX master: closed-form hypergeometric product paper

Tasks:
- C1: Add a minimal pytest suite that checks:
  - symmetry relations (via `symmetry_checker.py`)
  - agreement with SymPy `wigner_6j` / `wigner_9j` for supported cases
- C2: Add spin-domain validation utilities (triangle/parity/half-integers)
- C3: Make `coefficient_calculator.py` produce deterministic JSON tables for inclusion in the paper
- C4: Add performance notes (complexity and practical timings) for the product formula vs summation

### 3.2 `su2-3nj-uniform-closed-form`
Current assets:
- `project/su2_3nj_closed_form.py` (currently delegates to SymPy)
- Many scripts in `scripts/` and a reference dataset in `tests/reference_3nj_closed_form.json`

Tasks:
- U1: Replace “delegate to SymPy” with a real hypergeometric expression incrementally:
  - start with 6j as a 4F3 representation
  - then add a 9j special case if available
- U2: Convert ad-hoc scripts into pytest tests where appropriate
- U3: Add a single `python -m pytest` workflow that validates:
  - domain checks
  - symmetry checks
  - numeric spot checks

### 3.3 `su2-3nj-recurrences`
Current assets:
- LaTeX master: finite recurrences paper
- No Python entrypoint found yet

Tasks:
- R1: Implement a small reference recurrence engine (Python):
  - represent three-term recurrence coefficients $a_k,b_k,c_k$
  - compute sequences from boundary data
- R2: Provide stability analysis:
  - forward vs backward recursion
  - scaling/normalization strategies
- R3: Cross-check recurrence-generated values against SymPy (6j/9j) or against closed-form scripts

### 3.4 `su2-3nj-generating-functional`
Current assets:
- Python package in `src/su2_3nj_gen/`
- Tests in `tests/` including identity checks
- Scripts for UQ and series coefficients

Tasks:
- G1: Harden `recursion_3nj` implementation:
  - fix exact summation bounds (no truncation)
  - handle half-integers consistently
  - add explicit parity/triangle checks
- G2: Extend generating functional beyond the hard-coded 6j example graph
- G3: Determinant stability report:
  - produce CSV/JSON for condition numbers vs parameter sweeps
- G4: Make scripts deterministic and runnable as `python -m ...` modules

### 3.5 `su2-node-matrix-elements`
Current assets:
- LaTeX masters + docs
- No Python entrypoint found yet

Tasks:
- N1: Add a small Python module to compute node matrix elements using generating functional coefficients
- N2: Add unit tests that validate low-valence cases against known 6j/9j decompositions
- N3: Add a script to produce tables used in the node-matrix-element paper

---

## 4) Execution schedule (Q1–Q2 2026)

### Q1 (Jan–Mar 2026): validation + code hardening
- Week 1–2: spin-domain validation + golden datasets + pytest harness
- Week 3–4: recurrence prototype + cross-verification matrix
- Month 2–3: stability/UQ sweeps + figure/table generation scripts

### Q2 (Apr–Jun 2026): write + submit
- Merge LaTeX into master draft
- Integrate priors + comparisons
- Finalize validation section and appendices
- Submit preprint; then journal submission

---

## 5) “Start here” checklist (fastest path to momentum)

1) Run pytest in `su2-3nj-generating-functional` and fix any failures.
2) Add half-integer regression tests for 6j.
3) Convert the most important `su2-3nj-uniform-closed-form/scripts/test_*.py` into pytest tests.
4) Create/refresh reference datasets and pin them.
5) Start a master LaTeX bundle (new repo) once validations are stable.
