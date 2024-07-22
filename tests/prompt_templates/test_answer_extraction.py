import random

import numpy as np
import torch

from unstated_norms_llm_bias.prompt_based_classification.prompt_experiments.utils import extract_predicted_label

np.random.seed(2024)
random.seed(2024)
torch.manual_seed(2024)


def test_extraction_when_present_case_insensitive() -> None:
    answer = extract_predicted_label("Hello Negative")
    assert answer == "negative"

    answer = extract_predicted_label("Hello it is NEGATIVE yes?")
    assert answer == "negative"

    answer = extract_predicted_label("Hello it is positive NEGATIVE yes?")
    assert answer == "positive"

    answer = extract_predicted_label("NEGATIVE yes?")
    assert answer == "negative"

    answer = extract_predicted_label("Hello it is Neutral yes?")
    assert answer == "neutral"


def test_random_choice_stable_from_string() -> None:
    answer = extract_predicted_label("It is bad")
    assert answer == "negative"

    answer = extract_predicted_label("energetic")
    assert answer == "positive"

    answer = extract_predicted_label("I think it makes sense")
    assert answer == "neutral"
