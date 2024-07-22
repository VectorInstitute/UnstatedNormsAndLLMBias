import random

import numpy as np
import torch

from unstated_norms_llm_bias.prompt_based_classification.prompt_experiments.utils import create_demonstrations

np.random.seed(2024)
random.seed(2024)
torch.manual_seed(2024)


def test_stable_sst5_prompt_shots() -> None:
    prompt_demonstrations = create_demonstrations(
        "SST5", number_of_demonstrations_per_label=3, number_of_random_demonstrations=1
    )

    with open("tests/prompt_templates/assets/sst5_demo_reference.txt", "r") as f:
        prompt_demonstration_target = f.read()

    assert prompt_demonstrations.strip() == prompt_demonstration_target.strip()


def test_stable_semeval_prompt_shots() -> None:
    prompt_demonstrations = create_demonstrations(
        "SemEval", number_of_demonstrations_per_label=3, number_of_random_demonstrations=1
    )

    with open("tests/prompt_templates/assets/semeval_demo_reference.txt", "r") as f:
        prompt_demonstration_target = f.read()

    assert prompt_demonstrations.strip() == prompt_demonstration_target.strip()


def test_zero_shot_prompts() -> None:
    prompt_demonstrations = create_demonstrations(
        "ZeroShot", number_of_demonstrations_per_label=3, number_of_random_demonstrations=1
    )
    # Demonstrations should be empty
    assert prompt_demonstrations == ""
