#!/bin/bash
# setup-env.sh - Environment setup script

echo "Setting up physics-suite conda environment with Python 3.12..."

# Create/update conda environment from environment.yml
conda env create -f environment.yml --name physics-suite || conda env update -f environment.yml --name physics-suite

echo "Environment setup complete!"
echo "Activate with: conda activate physics-suite"