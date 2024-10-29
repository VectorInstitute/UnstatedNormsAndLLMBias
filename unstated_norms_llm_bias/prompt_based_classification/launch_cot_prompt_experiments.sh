#!/bin/bash

###############################################
# Usage:
#
#  ./unstated_norms_llm_bias/prompt_based_classification/launch_cot_prompt_experiments.sh \
#   run_id \
#   dataset
# Example
#  ./unstated_norms_llm_bias/prompt_based_classification/launch_cot_prompt_experiments.sh \
#   "run_1" \
#   "SST5"
###############################################

RUN_ID=$1
DATASET=$2

# Run the ID and DATASET for each of the llama, llama2, llama3, and Mistral models

# LLaMA
SBATCH_COMMAND="unstated_norms_llm_bias/prompt_based_classification/slrm_scripts/run_llama_experiment_cot.slrm \
    ${RUN_ID} \
    ${DATASET}"
echo "Running sbatch command ${SBATCH_COMMAND}"
sbatch ${SBATCH_COMMAND}

# Llama 2
SBATCH_COMMAND="unstated_norms_llm_bias/prompt_based_classification/slrm_scripts/run_llama2_experiment_cot.slrm \
    ${RUN_ID} \
    ${DATASET}"
echo "Running sbatch command ${SBATCH_COMMAND}"
sbatch ${SBATCH_COMMAND}

# Llama 3
SBATCH_COMMAND="unstated_norms_llm_bias/prompt_based_classification/slrm_scripts/run_llama3_experiment_cot.slrm \
    ${RUN_ID} \
    ${DATASET}"
echo "Running sbatch command ${SBATCH_COMMAND}"
sbatch ${SBATCH_COMMAND}

# Mistral
SBATCH_COMMAND="unstated_norms_llm_bias/prompt_based_classification/slrm_scripts/run_mistral_experiment_cot.slrm \
    ${RUN_ID} \
    ${DATASET}"
echo "Running sbatch command ${SBATCH_COMMAND}"
sbatch ${SBATCH_COMMAND}

echo Experiments Launched
