# Train and Evaluate Classifier

This directory contains scripts to train and evaluate a classifier model using the Hugging Face transformers library. It is designed for training smaller models on a single GPU. For multi-GPU training, please refer to the [vectorlm](https://github.com/VectorInstitute/vectorlm) repository by the Vector Institute.

## Files

- `train_and_evaluate_classifier.py`: Main script for training and evaluating the classifier.
- `training_utils.py`: Contains utility functions for training and evaluation.
- `data_loader.py`: Contains functions to construct data loaders from datasets.

## Usage

```bash
python train_and_evaluate_classifier.py <learning_rate> <weight_decay> <early_stopping> <seed> <hf_model_name>
```

### Arguments

- `<learning_rate>`: Learning rate (e.g., 0.00001)
- `<weight_decay>`: Weight decay (e.g., 0.001)
- `<early_stopping>`: Early stopping threshold (e.g., 5)
- `<seed>`: Seed for reproducibility (e.g., 8)
- `<hf_model_name>`: Hugging Face model name (e.g., `facebook/opt-125m`)