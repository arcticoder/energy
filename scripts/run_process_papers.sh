#!/bin/bash
# Script to run the paper processing script

# Activate the virtual environment
source /home/echo_/Code/asciimath/energy/.venv/bin/activate

# Log output so crashes can be inspected later
LOG_DIR="/home/echo_/Code/asciimath/energy/scripts/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/process_papers_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG_FILE") 2>&1

# Upgrade MinerU and related packages to reduce warnings
python -m pip install --upgrade mineru --quiet

# FlashInfer is not always available on WSL/older GPUs; avoid noisy errors
if python - <<'PY'
import platform
print('microsoft' not in platform.release().lower())
PY
then
	python -m pip install --upgrade flashinfer --quiet || echo "FlashInfer not available for this platform"
else
	echo "Skipping FlashInfer install on WSL"
fi

# Reduce MinerU/vLLM warnings on older GPUs
export VLLM_WORKER_MULTIPROC_METHOD=spawn
export VLLM_ATTENTION_BACKEND=TORCH_SDPA
export VLLM_GPU_MEMORY_UTILIZATION=0.6
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128,garbage_collection_threshold:0.8
export PYTHONUNBUFFERED=1

# Run the script
python -u /home/echo_/Code/asciimath/energy/scripts/process_papers.py