import random

import numpy as np
import torch
from transformers import pipeline

generator = pipeline("text-generation", model="gpt2", device="cpu")

np.random.seed(2024)
random.seed(2024)
torch.manual_seed(2024)


def test_stable_predictions_through_hf_generator() -> None:
    prompts = ["Hello, is it me you're", "Where should I look?", "The quick brown fox"]
    targets = [" talking about?", " I'm going", " is actually slightly"]
    batched_sequences = generator(prompts, do_sample=True, max_new_tokens=3, temperature=0.8, return_full_text=False)
    for prompt_sequence, target in zip(batched_sequences, targets):
        generated_text = prompt_sequence[0]["generated_text"]
        assert generated_text == target
