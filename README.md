# Template-Based Probes and LLM Bias

This repository houses the code used to produce the experiments in the paper "Template-Based Probes Are Imperfect Lenses for Counterfactual Bias Evaluation in LLMs"

For information about setting up the environment to run the experiments, see the documentation in [CONTRIBUTING.MD](CONTRIBUTING.MD).

## Prompt-Based Classification Experiments

All of the code used for the experiments based purely on prompting are housed in the `prompt_based_classification` folder. Below are details around the folder contents and how experiments are run.

### Resources

The `resources` folder holds tsv files corresponding to important artifacts:
* The Amazon templates (`sentiment_fairness_tests.tsv`) for all sensitive attributes (not just ethnicity)
* The SemEval dataset (`2018-Valence-oc-En-train.txt`) used to created the processed examples from which the prompt demonstration are drawn.
* The subset of the SST5 (`processed_sst5.tsv`) and SemEval (`processed_semeval.tsv`) datasets that were used in sampling the prompt demonstrations in the experiments.

### Shot Dataset Processing

In `shot_dataset_processing/` there are two notebooks used to create the subsampled versions of the SST5 and SemEval datasets used in few-shot prompt construction.

### Prediction Scripts

The python scripts for the prompt setup, LLM generation, and answer extraction is housed in `prompt_experiments`. These scripts cover the construction of zero-shot, 9-shot, and CoT prompts for the OPT-6.7B, LLaMA-7B, and Llama-2-7B models. They use the HuggingFace generation pipeline and all of the code necessary for predictions on the Amazon dataset. The code relies on model artifacts hosted on Vector's cluster. However, these models were taken directly from Hugging Face's hosting of these models. So the paths can be substituted for these model artifacts if you have access and the space to store them.

These scripts have seeds indexed by the run IDs (run_1, run_2, ..., run_5) to facilitate reproducibility.

### Slurm Scripts and Experiment Launch Scripts

The folder `slrm_scripts` contains the scripts necessary to run a single experiment for each of the models (with CoT treated differently from the other prompting approaches). Each script takes the arguments `RUN_ID`, which is chosen from ("run_1", "run_2", ..., "run_5") to vary the random seeds across 5 runs and `DATASET`, chosen from ("SST5", "SemEval", "Zero-Shot") to vary the kind of prompting that is being done:
* SST5 corresponds to 9-shot prompts with demonstrations drawn from SST5.
* SemEval corresponds to 9-shot prompts with demonstrations drawn from SemEval
* Zero-shot corresponds to Zero-shot prompts

Note that, by convention, when doing experiments with CoT, we pass in SST5 to have a placeholder for the dataset, but no demonstrations are actually used for those experiments.

These SLURM scripts are meant specifically for the Vector HPC cluster and the size of the LLMs require a high-quality GPU. In our case, we use A40s.

The experiment launch scripts (`launch_cot_prompt_experiments.sh` and `launch_prompt_experiments.sh`) are meant to automate launching a full set of experiments across models. Each script takes in the arguments `RUN_ID` and `DATASET`, just like the slrm scripts with the same effect.
* `launch_prompt_experiments.sh`: Launches a single run of standard prompting experiments across OPT-6.7B, LLaMA-7B, and Llama-2-7B.
    * To run a single prompted classification run on the Amazon dataset for all of the models using 9-shot prompts with demonstrations drawn from SST5 one would run
    ```bash
    ./unstated_norms_llm_bias/prompt_based_classification/launch_prompt_experiments.sh "run_1" "SST5"`
    ```
* `launch_cot_prompt_experiments.sh`: Launches a single run of Zero-shot CoT prompting experiments across LLaMA-7B, and Llama-2-7B.
    * To run a single zero-shot prompted classification run on the Amazon dataset for all of the models.
    ```bash
    ./unstated_norms_llm_bias/prompt_based_classification/launch_cot_prompt_experiments.sh "run_1" "SST5"`
    ```

### Visualizations

Two notebooks for visualizing the results of these predictions over the 5 runs are provided in `visualization` under the name `pure_prompt_fairness_plots_old.ipynb` and `prompting_group_fairness_plots.ipynb`. These notebooks visualize the mean FPR gaps (among others) for the prompting experiments along with the associated confidence intervals. The notebook `pure_prompt_fairness_plots_old.ipynb` uses an older color scheme but is still useful in that it produces slightly simpler figures. The notebook `prompting_group_fairness_plots.ipynb` can be used to reproduce the plots from the paper using the prediction files in the `prompt_based_classification/predictions` folder.

### Predictions and Artifacts

All of the predictions produced by the prompting experiments across the five runs for the paper are housed in the `predictions/` folder. They are broken out by model name, then named for the type of prompting used to produce the predictions.

In addition to the predictions produced by the prompting runs, we have also stored the logs associated with the scripts produced during all experiments. Some logs have been overwritten due to SLURM preemption and other failures, but they contain good visualizations of the prompts used and time that predictions took for individuals interested in reviewing such low-level details

### Accuracy Results

To compute the accuracy and standard deviations of the prompt-based classification approaches, the notebook `measure_prompt_results_accuracy.ipynb` can be used. It acts on the predictions tsv files and computes the accuracy of the predictions against the true values from the Amazon dataset.

## Fine-Tuning Classification Experiments
All of the code used for classification experiments through fine-tuning is housed in the `finetuning_classification/` folder. Below are details around the folder contents and how experiments are run.

### Training
The `training/` folder contains scripts used for fine-tuning models. For more details, refer to its [README](unstated_norms_llm_bias/finetuning_classification/training/README.md) file.

### Resources
The `resources/` folder contains essential materials for the experiments, organized as follows:
- `samples/`: Contains `.tsv` files with samples generated from the templates.
- `templates/`: Includes the `NS-Prompts` and `Regard` templates used in the experiments.

### Predictions and Artifacts
All of the predictions produced by the fine-tuning experiments across five runs for the paper are housed in the `predictions/` folder. Within this folder, there are two folders:
- `fully-fine-tuned/`: Contains prediction files for the smaller models that have been fully fine-tuned. Each file is named following the format `TEMPLATE-NAME_MODEL-NAME.tsv`, where `TEMPLATE-NAME` is the name of the template dataset and `MODEL-NAME` is the name of the model.
- `lora-fine-tuned/`: Contains prediction files for the larger models that have been fine-tuned using LoRA. These files follow the same naming structure as those in the `fully-fine-tuned/` folder.

### Visualizations
The notebook for visualizing the results of predictions over the five runs is provided in the `visualization/` folder under the name `finetuning_group_fairness_plots.ipynb`. This notebook visualizes the mean FPR gaps (both positive and negative sentiment) for the fine-tuning experiments, along with the associated confidence intervals.

### Accuracy Results
To compute the accuracy and standard deviations of fine-tuning classification approaches, the notebook `measure_prompt_results_accuracy.ipynb` can be used. This notebook is the same as the one found in the [`prompt_based_classification`](unstated_norms_llm_bias/prompt_based_classification) folder.

## Citation

We hope that the repository will be useful to both NLP practitioners and researchers working on bias quantification and mitigation research. If you find this code or the paper useful please cite
```
@misc{kohankhaki2024impactunstatednormsbias,
      title={The Impact of Unstated Norms in Bias Analysis of Language Models},
      author={Farnaz Kohankhaki and Jacob-Junqi Tian and David Emerson and Laleh Seyyed-Kalantari and Faiza Khan Khattak},
      year={2024},
      eprint={2404.03471},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2404.03471},
}
```
