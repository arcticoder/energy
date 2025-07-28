#!/usr/bin/env python3
"""
extract_kb.py

Utility for extracting Verification & Validation knowledge-base snippets
from the asciimath repositories.  It emits a single Markdown file containing
full-module dumps for key files and targeted code/LaTeX/Markdown snippets
wrapped in fenced code blocks for easy review and task creation.
"""
import re, os, argparse

# ——— Full list of files to pull in (relative to asciimath/) ———
TARGET_FILES = [
    # —— Energy & Warp code (unchanged) ——
    "energy/analysis/analyze_subspace_range.py",
    "energy/analysis/realistic_subspace_analysis.py",
    "energy/analysis/stress_energy_tensor_coupling.py",
    "energy/demos/dynamic_backreaction_demo.py",
    "energy/src/dynamic_backreaction_factor.py",
    "energy/src/enhanced_artificial_gravity_implementation.py",
    "energy/tools/count_warp_field_coils.py",

    # —— SU(2) 3nj generating-functional & tests ——
    "su2-3nj-generating-functional/src/su2_3nj_gen/su2_3nj.py",
    "su2-3nj-generating-functional/src/su2_3nj_gen/generating_functional.py",
    "su2-3nj-generating-functional/scripts/compute_G_xy_series.py",
    "su2-3nj-generating-functional/scripts/compute_hilbert_series.py",
    "su2-3nj-generating-functional/scripts/generate_reference_coeffs.py",
    "su2-3nj-generating-functional/tests/test_generate_3nj.py",
    "su2-3nj-generating-functional/tests/test_biedenharn_elliott_identity.py",
    # closed-form hypergeometric
    "su2-3nj-closedform/scripts/coefficient_calculator.py",
    "su2-3nj-closedform/scripts/symmetry_checker.py",

    # —— Recurrences & uniform closed form ——
    "su2-3nj-recurrences/scripts/closed_form_recurrences.py",
    "su2-3nj-uniform-closed-form/project/su2_3nj_closed_form.py",
    "su2-3nj-uniform-closed-form/scripts/validate_closed_form.py",

    # —— Negative-energy & LQG core ——
    "negative-energy-generator/src/theoretical/generating_functional.py",
    "negative-energy-generator/src/theoretical/su2_recoupling.py",
    "lqg-volume-quantization-controller/src/core/su2_mathematical_core.py",

    # —— Warp solver equations ——
    "warp-solver-equations/scripts/generate_solver_equations.py",
    "warp-solver-equations/scripts/solver.py",
    "warp-solver-equations/docs/technical-documentation.md",

    # —— (Keep your previous warp-field-coils etc) ——
    "warp-field-coils/examples/lqg_subspace_demo.py",
    "warp-field-coils/lqg_enhanced_field_coils.py",
    "warp-field-coils/src/control/dynamic_trajectory_controller.py",
    "warp-field-coils/src/subspace_transceiver/transceiver.py",
    "warp-field-coils/src/tomographic_scanner.py",
    "polymerized-lqg-matter-transporter/src/utils/multi_field_superposition.py",
    "unified-lqg/fusion/lqg_fusion_reactor_system.py",

    # —— LaTeX cores ——
    "warp-bubble-assemble-expressions/final_expressions.tex",
    "warp-bubble-coordinate-spec/metrics/alcubierre_ansatz.tex",
    "warp-bubble-coordinate-spec/metrics/natario_example.tex",
    "warp-bubble-connection-curvature/connection_curvature.tex",
    "su2-3nj-closedform/A Closed-Form Hypergeometric Product for 12j.tex",
    "su2-3nj-generating-functional/A Universal Generating Functional for SU(2) 3nj.tex",
    "su2-3nj-recurrences/Closed-Form Finite Recurrences for SU(2) 6j and 9j Symbols.tex",
    "unified-lqg-qft/docs/A Universal Generating Functional for Unified LQG QFT.tex",

    # —— Markdown docs ——
    "su2-3nj-closedform/docs/technical-documentation.md",
    "su2-3nj-generating-functional/README.md",
    "su2-node-matrix-elements/docs/technical-documentation.md",
    "su2-node-matrix-elements/docs/Closed-Form Matrix Elements for SU(2) Nodes.md",
    "unified-lqg-qft/docs/Closed-Form Finite Recurrences for Unified LQG QFT.md",
]

# ——— Files whose *full* contents we want — not just snippets ———
FULL_CONTENT_FILES = [
    # energy core routines
    "energy/src/compute_einstein_tensor.py",
    "energy/src/compute_stress_energy_tensor.py",
    # dynamic trajectory & shape timing
    "energy/src/dynamic_backreaction_factor.py",
    "warp-field-coils/src/control/dynamic_trajectory_controller.py",
    "polymerized-lqg-matter-transporter/src/utils/multi_field_superposition.py",

    # solver-generation & warp validation
    "warp-solver-validation/scripts/generate_solver_equations.py",
    "warp-solver-validation/scripts/solver.py",

    # final expressions
    "warp-bubble-assemble-expressions/final_expressions.tex",

    # zero-exotic-energy theory
    "negative-energy-generator/src/theoretical/generating_functional.py",
    "negative-energy-generator/src/theoretical/su2_recoupling.py",

    # sensor-to-field conversion
    "warp-field-coils/src/subspace_transceiver/transceiver.py",

    # --- Added full content files ---
    "lqg-positive-matter-assembler/src/core/bobrick_martire_geometry.py",
    "lqg-ftl-metric-engineering/navigation/trajectory_optimizer.py",
]

# ——— Expanded regex patterns ———
PY_FUNC_RE     = re.compile(r'^\s*def\s+[\w_]+\(.*\):')  # catch all defs
LATEX_ENV_RE   = re.compile(r'\\begin\{(?:equation|align)\}|\$\$|\\\[|\\\(')
INLINE_MATH_RE = re.compile(r'\$(?:[^$]|\\\$)+\$')
KEYWORD_RE     = re.compile(
    r'\b(?:warp|bubble|field|metric|einstein|stress_energy|'
    r'diff|gradient|profile|su2|3nj|nj|recurrence|hypergeometric|'
    r'biedenharn|elliott|pentagon|closed_form|generating_functional)\b',
    re.I
)

def extract_from_py(lines):
    out = []
    for i, L in enumerate(lines):
        if PY_FUNC_RE.search(L) or KEYWORD_RE.search(L):
            s, e = max(0, i-2), min(len(lines), i+3)
            out.append(''.join(lines[s:e]))
    return out

def extract_from_tex(lines):
    out, buf, in_env = [], [], False
    for L in lines:
        if LATEX_ENV_RE.search(L):
            in_env = True
        if in_env:
            buf.append(L)
            if r'\end' in L or '$$' in L:
                out.append(''.join(buf)); buf, in_env = [], False
        elif INLINE_MATH_RE.search(L) or KEYWORD_RE.search(L):
            out.append(L.rstrip())
    return out

def extract_from_md(lines):
    out, buf, in_code = [], [], False
    for L in lines:
        if L.strip().startswith('```'):
            if in_code:
                out.append(''.join(buf)); buf, in_code = [], False
            else:
                in_code = True; buf = [L]
        elif in_code:
            buf.append(L)
        else:
            if INLINE_MATH_RE.search(L) or KEYWORD_RE.search(L):
                out.append(L.rstrip())
    return out

def extract_snippets(path):
    ext = os.path.splitext(path)[1].lower()
    lines = open(path, encoding='utf-8').read().splitlines(keepends=True)
    if ext == '.py':  return extract_from_py(lines)
    if ext == '.tex': return extract_from_tex(lines)
    if ext == '.md':  return extract_from_md(lines)
    return []

def main(root, out_md):
    snippets = 0
    with open(out_md, 'w', encoding='utf-8') as out:
        for rel in TARGET_FILES:
            src = os.path.join(root, *rel.split('/'))
            if not os.path.isfile(src):
                continue

            # If configured for full content, dump entire file:
            if rel in FULL_CONTENT_FILES:
                content = open(src, encoding='utf-8').read()
                out.write(f"```{os.path.abspath(src)}\n")
                out.write(content)
                if not content.endswith('\n'):
                    out.write('\n')
                out.write("```\n\n")
                snippets += 1
                continue

            # Otherwise, extract and dump snippets as before
            for sn in extract_snippets(src):
                out.write(f"```{os.path.abspath(src)}\n")
                out.write(sn)
                if not sn.endswith('\n'):
                    out.write('\n')
                out.write("```\n\n")
                snippets += 1
    print(f"✅ Extracted {snippets} KB snippets to {out_md}")

if __name__=='__main__':
    p = argparse.ArgumentParser()
    p.add_argument('-r','--asciimath-root', default=os.getcwd(),
                   help="Path to asciimath/ root")
    p.add_argument('-o','--output', default="kb_snippets.md",
                   help="Output Markdown file")
    args = p.parse_args()
    main(args.asciimath_root, args.output)