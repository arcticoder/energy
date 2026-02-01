# Scripts Directory

This directory contains Python scripts organized by category:

## Directory Structure

### `uq/` - Uncertainty Quantification Scripts
- `comprehensive_uq_assessment.py` - Comprehensive UQ framework assessment
- `critical_lqg_uq_resolution.py` - Critical LQG UQ issue resolution
- `final_production_uq_resolution.py` - Final production-ready UQ resolution
- `master_uq_resolution.py` - Master UQ resolution orchestrator
- `simplified_uq_resolver.py` - Simplified UQ resolution methods
- `supplementary_uq_resolution.py` - Supplementary UQ resolution tools
- `uq_extensions_implementation.py` - UQ extensions implementation
- `uq_implementation_validator.py` - UQ implementation validation
- `uq_todo_consolidation.py` - UQ TODO item consolidation

### `validation/` - Validation and Verification Scripts
- `component_precision_verification.py` - Component precision validation
- `correlation_matrix_validation.py` - Correlation matrix validation
- `medical_protection_verification.py` - Medical safety protocol verification
- `quantum_coherence_preservation.py` - Quantum coherence validation

### `tools/` - Utility Tools
- `regenerate_index.py` - Documentation index regeneration
- `uq_file_cleanup.py` - UQ file cleanup utility

### `process_papers.py` - Paper Processing Script
- Processes PDFs using MinerU to extract markdown from academic papers
- Matches papers from BibTeX citations with PDF locations from TSV file
- Skips already processed papers

Run with:
```bash
./run_process_papers.sh
```

## Usage

All scripts are designed to be run from the energy repository root directory:

```bash
cd /path/to/energy
python scripts/uq/master_uq_resolution.py
python scripts/validation/component_precision_verification.py
python scripts/tools/regenerate_index.py
python scripts/process_papers.py
```

## Related Directories

- `../analysis/` - Contains analysis scripts and their output files
- `../docs/` - Contains documentation files
