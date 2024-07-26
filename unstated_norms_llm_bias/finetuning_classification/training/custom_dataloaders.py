import math
from typing import Tuple, Union

import datasets
from datasets import load_dataset
from torch.utils.data import DataLoader, Subset, random_split
from transformers import PreTrainedTokenizer, PreTrainedTokenizerFast


def make_train_val_datasets(dataset: datasets.Dataset, split_ratio: float) -> Tuple[Subset, Subset]:
    assert 0.0 < split_ratio < 1.0

    original_length = len(dataset)
    train_length = math.floor(original_length * split_ratio)
    lengths = [train_length, original_length - train_length]
    train_dataset, val_dataset = random_split(dataset, lengths)
    return train_dataset, val_dataset


def construct_dataloaders(
    batch_size: int,
    train_split_ratio: float,
    tokenizer: Union[PreTrainedTokenizer, PreTrainedTokenizerFast],
    dataset_name: str,
) -> Tuple[DataLoader, DataLoader, DataLoader]:

    dataset_dict = load_dataset(dataset_name)
    tokenized_dataset_dict = dataset_dict.map(
        lambda row: tokenizer(row["text"], truncation=True, padding="max_length"), batched=True
    )
    train_dataset = tokenized_dataset_dict["train"]
    test_dataset = tokenized_dataset_dict["test"]

    if "validation" in tokenized_dataset_dict.keys():
        val_dataset = tokenized_dataset_dict["validation"]
    else:
        # Some datasets (e.g., AG news) just has train and test sets (no validation set)
        # split the original training dataset into a training and validation set.
        train_dataset, val_dataset = make_train_val_datasets(train_dataset, train_split_ratio)

    train_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])
    val_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])
    test_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

    # Create pytorch dataloaders from the dataset objects.
    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_dataloader = DataLoader(val_dataset, batch_size=batch_size, shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    example_train_batch = next(iter(train_dataloader))
    example_encode_batch = example_train_batch["input_ids"]
    example_decode = tokenizer.batch_decode(example_encode_batch, skip_special_tokens=True)[0]
    print(f"Training data example encoding: {example_encode_batch[0]}")
    print(f"Training data example decoding: {example_decode}")

    return train_dataloader, val_dataloader, test_dataloader
