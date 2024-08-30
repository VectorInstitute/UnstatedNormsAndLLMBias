import os
from typing import Dict, List, Tuple

PATH_STUB = "unstated_norms_llm_bias/gap_and_other_analysis/stats_files"

# GAP_FILE_NAME = "amazon_gaps.csv"
# GAP_FILE_NAME = "ns_prompts_gaps.csv"
GAP_FILE_NAME = "regard_gaps.csv"

percent_threshold = 0.1

gap_file_path = os.path.join(PATH_STUB, GAP_FILE_NAME)


# Return order is model name, subgroup, negative fpr gap mean, positive fpr gap mean
def parse_gap_line(gap_line: str) -> Tuple[str, str, float, float]:
    line_pieces = gap_line.split(",")
    return (line_pieces[0], line_pieces[1], float(line_pieces[2]), float(line_pieces[4]))


with open(gap_file_path, "r") as gap_file:
    gap_lines = gap_file.readlines()
    all_neg_fpr_gap_means: List[float] = []
    all_pos_fpr_gap_means: List[float] = []
    all_neg_fpr_info: Dict[str, List[Tuple[str, float]]] = {}
    all_pos_fpr_info: Dict[str, List[Tuple[str, float]]] = {}
    # skip the first two lines
    for gap_line in gap_lines[2:]:
        model_name, subgroup, neg_fpr_gap_mean, pos_fpr_gap_mean = parse_gap_line(gap_line)
        all_neg_fpr_gap_means.append(abs(neg_fpr_gap_mean))
        all_pos_fpr_gap_means.append(abs(pos_fpr_gap_mean))

        if subgroup in all_neg_fpr_info:
            all_neg_fpr_info[subgroup].append((model_name, neg_fpr_gap_mean))
        else:
            all_neg_fpr_info[subgroup] = [(model_name, neg_fpr_gap_mean)]

        if subgroup in all_pos_fpr_info:
            all_pos_fpr_info[subgroup].append((model_name, pos_fpr_gap_mean))
        else:
            all_pos_fpr_info[subgroup] = [(model_name, pos_fpr_gap_mean)]

    neg_fpr_max_abs_gap = max(all_neg_fpr_gap_means)
    pos_fpr_max_abs_gap = max(all_pos_fpr_gap_means)

    print(f"Neg FPR Max Absolute Gap: {neg_fpr_max_abs_gap}")
    print(f"Pos FPR Max Absolute Gap: {pos_fpr_max_abs_gap}")

    neg_models: Dict[str, List[str]] = {}
    pos_models: Dict[str, List[str]] = {}

    for subgroup, neg_fpr_info in all_neg_fpr_info.items():
        neg_models[subgroup] = []
        print(f"Negative FPR Gap Analysis for Subgroup {subgroup}")
        print("----------------------------------------------------")
        print(f"Identifying small gaps (below {percent_threshold} of max absolute gap)")
        print(f"Gap Threshold is {percent_threshold*neg_fpr_max_abs_gap}")
        print("----------------------------------------------------")
        any_small_gaps = False
        threshold = percent_threshold * neg_fpr_max_abs_gap
        for model_name, neg_fpr_gap_mean in neg_fpr_info:
            if abs(neg_fpr_gap_mean) <= threshold:
                any_small_gaps = True
                neg_models[subgroup].append(model_name)
                print(f"Gap for {model_name} is below threshold with gap of {neg_fpr_gap_mean}")
        if not any_small_gaps:
            print("NONE")
        print("----------------------------------------------------")
        print()

    for subgroup, pos_fpr_info in all_pos_fpr_info.items():
        pos_models[subgroup] = []
        print(f"Positive FPR Gap Analysis for Subgroup {subgroup}")
        print("----------------------------------------------------")
        print(f"Identifying small gaps (below {percent_threshold} of max absolute gap)")
        print(f"Gap Threshold is {percent_threshold*pos_fpr_max_abs_gap}")
        print("----------------------------------------------------")
        threshold = percent_threshold * pos_fpr_max_abs_gap
        any_small_gaps = False
        for model_name, pos_fpr_gap_mean in pos_fpr_info:
            if abs(pos_fpr_gap_mean) <= threshold:
                any_small_gaps = True
                pos_models[subgroup].append(model_name)
                print(f"Gap for {model_name} is below threshold with gap of {pos_fpr_gap_mean}")
        if not any_small_gaps:
            print("NONE")
        print("----------------------------------------------------")
        print()

    # Summarize
    print()
    print()
    print("Negative FPR Gap Summary")
    print("---------------------------")
    for subgroup, models in neg_models.items():
        print(f"Subgroup: {subgroup}, Low Absolute Gap Models: {models}")

    print()
    print("Positive FPR Gap Summary")
    print("---------------------------")
    for subgroup, models in pos_models.items():
        print(f"Subgroup: {subgroup}, Low Absolute Gap Models: {models}")
