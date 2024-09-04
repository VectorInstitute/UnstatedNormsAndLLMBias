#!/bin/bash
#SBATCH --job-name=<job-name>
#SBATCH --nodes=1
#SBATCH --mem=0
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-gpu=6
#SBATCH --gres=gpu:1
#SBATCH --output=<output-path>/%j.out
#SBATCH --error=<error-path>/%j.err
#SBATCH --partition=<partition>
#SBATCH --qos=<qos>
#SBATCH --open-mode=append
#SBATCH --wait-all-nodes=1
#SBATCH --time=<time-limit>

export NCCL_IB_DISABLE=1
export NCCL_DEBUG=WARN
export NCCL_DEBUG_SUBSYS=WARN
export NCCL_P2P_DISABLE=1

export TORCH_DISTRIBUTED_DEBUG=DETAIL
export TORCH_CPP_LOG_LEVEL=INFO
export LOGLEVEL=INFO
export PYTHONFAULTHANDLER=1
export CUDA_LAUNCH_BLOCKING=0

torchrun --nnodes=1 --nproc-per-node=${SLURM_GPUS_ON_NODE} finetuning.py --yaml_path config.yaml
