# Train and Evaluate Classifier Models

This folder contains scripts for training and evaluating classifier models, organized into two sets of experiments:

1. **Single GPU Training**: This set is for smaller models that can be trained on a single GPU. All scripts and resources needed are in the `single_gpu_training/` folder. Detailed instructions for running these experiments are provided in the [Single GPU Training](#single-gpu-training) section.

2. **Multi-GPU Training**: This set is for fine-tuning models that require multiple GPUs. We use the [vectorlm](https://github.com/VectorInstitute/vectorlm) repository from the Vector Institute for this purpose. Scripts for this setup are located in the `multi_gpu_training/` folder. The [Multi-GPU Training](#multi-gpu-training) section explains how to run these experiments.

## Single-GPU Training
This section provides instructions for training and evaluating smaller models using a single GPU.

### Files

- `train_and_evaluate_classifier.py`: Main script for training and evaluating the classifier.
- `training_utils.py`: Contains utility functions for training and evaluation.
- `data_loader.py`: Contains functions to construct data loaders from datasets.

### Usage
First, navigate to the `single_gpu_training/` folder:
```bash
cd single_gpu_training
```
Then, run the training script with the required arguments:
```bash
python train_and_evaluate_classifier.py <learning_rate> <weight_decay> <early_stopping> <seed> <hf_model_name>
```

### Arguments

- `<learning_rate>`: Learning rate (e.g., 0.00001)
- `<weight_decay>`: Weight decay (e.g., 0.001)
- `<early_stopping>`: Early stopping threshold (e.g., 5)
- `<seed>`: Seed for reproducibility (e.g., 8)
- `<hf_model_name>`: Hugging Face model name (e.g., `facebook/opt-125m`)

## Multi-GPU Training

This section provides instructions for training and evaluating larger models using multiple GPUs. We use the [vectorlm] (https://github.com/VectorInstitute/vectorlm) repository from the Vector Institute for this purpose. All necessary files for our specific experiments, modified from an example in the `vectorlm` repository (found at `vectorlm/example`), are located in the `multi_gpu_training/` folder. For general information on running experiments using the `vectorlm` setup, refer to its [README](https://github.com/VectorInstitute/vectorlm/blob/master/README.md).

### Files

Under the `multi_gpu_training/` folder, you will find the following files:

- `finetuning.py`: Adapted from `llama_example.py` in `vectorlm/example/llama_example.py`, this script is used for finetuning models with our specific parameters.
- `launch.sh`: A shell script to initiate the training process using SLURM job scheduling. This script includes several template fields which are enclosed in angle brackets (e.g., `<job-name>`) that need to be filled out with specific values based on your system's configuration before running the job.
- `config.yaml`: A configuration file that defines parameters of the experiments. Any fields within the `config.yaml` file that are enclosed in angle brackets (e.g., `<path-to-model-weights>`) are templates and need to be filled in with the appropriate values specific to each experiment.
For more detailed information about the `config.yaml` file and its options, please refer to the `vectorlm` configuration documentation available [here](https://github.com/VectorInstitute/vectorlm/blob/master/docs/config.md).
