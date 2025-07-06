# Analysis Directory

This directory contains analysis scripts and their associated output files.

## Contents

### Analysis Scripts
- `cross_repository_computational_load_resolution.py` - Cross-repository computational load analysis
- `materials_engineering_solution.py` - Materials engineering solution analysis
- `replicator_energy_framework_integration.py` - Replicator energy framework integration analysis
- `scale_up_feasibility_analysis.py` - Scale-up feasibility analysis
- `stress_energy_tensor_coupling.py` - Stress-energy tensor coupling analysis
- `volume_quantization_controller.py` - Volume quantization controller analysis

### Output Files
- `correlation_matrices_heatmap.png` - Correlation matrices visualization
- `correlation_matrix_validation_report.txt` - Correlation matrix validation results
- `cross_repository_computational_load_analysis.png` - Computational load analysis visualization
- `cross_repository_computational_load_report.json` - Computational load analysis results
- `master_uq_resolution_report_20250704_135158.json` - Master UQ resolution results
- `replicator_energy_integration_analysis.png` - Replicator energy integration visualization
- `replicator_energy_integration_report.json` - Replicator energy integration results
- `uq_implementation_validation.json` - UQ implementation validation results
- `uq_resolution_validation_report.json` - UQ resolution validation results

### Analysis Result Directories
- `comprehensive_uq_assessment/` - Comprehensive UQ assessment results
- `final_uq_resolution/` - Final UQ resolution analysis results
- `lqg_uq_resolution_results/` - LQG UQ resolution analysis results
- `supplementary_uq_resolution/` - Supplementary UQ resolution results

## Usage

Analysis scripts can be run from the energy repository root:

```bash
cd /path/to/energy
python analysis/cross_repository_computational_load_resolution.py
python analysis/scale_up_feasibility_analysis.py
```

Output files and visualizations are generated in this directory to keep results organized and accessible.
