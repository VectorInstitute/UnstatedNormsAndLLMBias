from unstated_norms_llm_bias.prompt_based_classification.prompt_experiments.prompting_czarnowska_llama2_7b import (
    create_demonstrations as llama2_demos,
)
from unstated_norms_llm_bias.prompt_based_classification.prompt_experiments.prompting_czarnowska_llama_7b import (
    create_demonstrations as llama_demos,
)
from unstated_norms_llm_bias.prompt_based_classification.prompt_experiments.prompting_czarnowska_opt6_7b import (
    create_demonstrations as opt_demos,
)


def test_stable_sst5_prompt_shots() -> None:
    # llama_sst5
    llama_demos("SST5")

    assert False

    # llama2_sst5
    llama2_demos("SST5")

    # opt_sst5
    opt_demos("SST5")
