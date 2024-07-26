import random
import sys

import numpy as np
import torch
import wandb
from custom_dataloaders import construct_dataloaders
from torch import cuda, nn
from training_utils import infer, train
from transformers import AutoModelForSequenceClassification, AutoTokenizer

DATASET = "jacobthebanana/sst5_mapped_grouped"


def set_seeds(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)

    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def train_classifier(lr: float, wd: float, es: int, seed: int, hf_model_name: str) -> None:
    set_seeds(seed)

    tokenizer = AutoTokenizer.from_pretrained(hf_model_name)

    tokenizer.model_max_length = 512
    train_dataloader, val_dataloader, test_dataloader = construct_dataloaders(
        batch_size=8,
        train_split_ratio=0.8,
        tokenizer=tokenizer,
        dataset_name=DATASET,
    )

    device = "cuda" if cuda.is_available() else "cpu"
    print(f"Detected device: {device}")

    classifier_model = AutoModelForSequenceClassification.from_pretrained(hf_model_name, num_labels=3)
    loss_function = nn.CrossEntropyLoss()

    models_path = "/ssd005/projects/llm/fair-llm/"
    hf_model_name_formatted = hf_model_name.split("/")[-1]
    dataset_name_formatted = DATASET.split("/")[-1]
    output_model_file = f"{models_path}{hf_model_name_formatted}_{dataset_name_formatted}_{seed!s}/"

    wandb_run_name = f"{hf_model_name_formatted}_lr={lr}_wd={wd}_es={es}_idx={seed}"
    wandb.init(
        project="fine-tuning classifier",
        name=wandb_run_name,
        tags=["final-model"],
        config={
            "model": hf_model_name,
            "dataset": dataset_name_formatted,
            "output model address": output_model_file,
            "lr": lr,
            "wd": wd,
            "es": es,
            "seed": seed,
        },
    )

    print("Begin model training ...")
    train(
        classifier_model,
        train_dataloader,
        val_dataloader,
        loss_function,
        device,
        n_epochs=1000,
        n_training_steps=30000,
        lr=lr,
        weight_decay=wd,
        early_stop_threshold=es,
    )
    print("Training completed.")

    print("Saving model ...")
    classifier_model.save_pretrained(output_model_file)
    tokenizer.save_pretrained(output_model_file)
    print(f"Model saved to {output_model_file}.")

    print("Evaluating model on the test set ...")
    test_accuracy, test_loss = infer(classifier_model, loss_function, test_dataloader, device)
    print(f"Test loss: {test_loss}")
    print(f"Test accuracy: {test_accuracy}%")
    print("Model evaluated.")

    wandb.log({"test_acc": test_accuracy, "test_loss": test_loss})


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python script.py <learning_rate> <weight_decay> <early_stopping> <index> <hf_model_name>")
        sys.exit(1)

    lr = float(sys.argv[1])
    wd = float(sys.argv[2])
    es = int(sys.argv[3])
    seed = int(sys.argv[4])
    hf_model_name = sys.argv[5]

    train_classifier(lr, wd, es, seed, hf_model_name)
