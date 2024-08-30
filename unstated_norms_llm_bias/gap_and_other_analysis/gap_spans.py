import os
import statistics
from typing import Dict, List, Tuple

import numpy as np

PATH_STUB = "unstated_norms_llm_bias/gap_and_other_analysis/stats_files"

GAP_FILE_NAME_AMAZON = "amazon_gaps.csv"
GAP_FILE_NAME_NS_PROMPTS = "ns_prompts_gaps.csv"
GAP_FILE_NAME_REGARD = "regard_gaps.csv"

all_neg_fpr_spans: Dict[str, List[float]] = {}
all_pos_fpr_spans: Dict[str, List[float]] = {}

how_often_is_white_a_span_extreme_neg_fpr = 0
how_often_is_white_a_span_extreme_pos_fpr = 0

for GAP_FILE_NAME in [GAP_FILE_NAME_AMAZON, GAP_FILE_NAME_NS_PROMPTS, GAP_FILE_NAME_REGARD]:

    gap_file_path = os.path.join(PATH_STUB, GAP_FILE_NAME)

    # Return order is model name, subgroup, negative fpr gap mean, positive fpr gap mean
    def parse_gap_line(gap_line: str) -> Tuple[str, str, float, float]:
        line_pieces = gap_line.split(",")
        return (line_pieces[0], line_pieces[1], float(line_pieces[2]), float(line_pieces[4]))

    with open(gap_file_path, "r") as gap_file:
        gap_lines = gap_file.readlines()
        all_neg_fpr_info: Dict[str, List[float]] = {}
        all_pos_fpr_info: Dict[str, List[float]] = {}
        # skip the first two lines
        for gap_line in gap_lines[2:]:
            model_name, subgroup, neg_fpr_gap_mean, pos_fpr_gap_mean = parse_gap_line(gap_line)

            if model_name in all_neg_fpr_info:
                all_neg_fpr_info[model_name].append(neg_fpr_gap_mean)
            else:
                all_neg_fpr_info[model_name] = [neg_fpr_gap_mean]

            if model_name in all_pos_fpr_info:
                all_pos_fpr_info[model_name].append(pos_fpr_gap_mean)
            else:
                all_pos_fpr_info[model_name] = [pos_fpr_gap_mean]

        neg_fpr_gap_model_spans: List[Tuple[str, float]] = []
        pos_fpr_gap_model_spans: List[Tuple[str, float]] = []

        for model_name, neg_fpr_info in all_neg_fpr_info.items():
            print(f"Negative FPR Gap Analysis for Model {model_name}")
            print("----------------------------------------------------")
            max_gap = max(neg_fpr_info)
            min_gap = min(neg_fpr_info)
            if np.argmax(neg_fpr_info) == 5 or np.argmin(neg_fpr_info) == 5:
                how_often_is_white_a_span_extreme_neg_fpr += 1
            span = max_gap - min_gap
            print(f"Gap Span is: {span}")
            print()
            neg_fpr_gap_model_spans.append((model_name, span))
            if model_name in all_neg_fpr_spans:
                all_neg_fpr_spans[model_name].append(span)
            else:
                all_neg_fpr_spans[model_name] = [span]

        for model_name, pos_fpr_info in all_pos_fpr_info.items():
            print(f"Positive FPR Gap Analysis for Model {model_name}")
            print("----------------------------------------------------")
            max_gap = max(pos_fpr_info)
            min_gap = min(pos_fpr_info)
            span = max_gap - min_gap
            if np.argmax(neg_fpr_info) == 5 or np.argmin(neg_fpr_info) == 5:
                how_often_is_white_a_span_extreme_pos_fpr += 1
            print(f"Gap Span is: {span}")
            print()
            pos_fpr_gap_model_spans.append((model_name, span))
            if model_name in all_pos_fpr_spans:
                all_pos_fpr_spans[model_name].append(span)
            else:
                all_pos_fpr_spans[model_name] = [span]

        print("Negative FPR Gap Span Summary")
        print("----------------------------------------------------")
        sorted_list = sorted(neg_fpr_gap_model_spans, key=lambda x: x[1], reverse=True)
        for model_name, span in sorted_list:
            print(f"Model: {model_name}, Span: {span}")
        print("----------------------------------------------------")
        print()

        print("Positive FPR Gap Span Summary")
        print("----------------------------------------------------")
        sorted_list = sorted(pos_fpr_gap_model_spans, key=lambda x: x[1], reverse=True)
        for model_name, span in sorted_list:
            print(f"Model: {model_name}, Span: {span}")
        print("----------------------------------------------------")
        print()

neg_fpr_span_avgs: List[Tuple[str, float]] = []
pos_fpr_span_avgs: List[Tuple[str, float]] = []

for model_name, spans in all_neg_fpr_spans.items():
    neg_fpr_span_avgs.append((model_name, statistics.mean(spans)))

for model_name, spans in all_pos_fpr_spans.items():
    pos_fpr_span_avgs.append((model_name, statistics.mean(spans)))

print("Average Negative FPR Gap Spans")
print("----------------------------------------------------")
sorted_list = sorted(neg_fpr_span_avgs, key=lambda x: x[1], reverse=True)
for model_name, span in sorted_list:
    print(f"Model: {model_name}, Span: {span}")
print("----------------------------------------------------")

print("Average Positive FPR Gap Spans")
print("----------------------------------------------------")
sorted_list = sorted(pos_fpr_span_avgs, key=lambda x: x[1], reverse=True)
for model_name, span in sorted_list:
    print(f"Model: {model_name}, Span: {span}")
print("----------------------------------------------------")

print("Number of times White group constitutes one of the Gap Extremes")
print(f"Negative FPR: {how_often_is_white_a_span_extreme_neg_fpr/33.0}")
print(f"Positive FPR: {how_often_is_white_a_span_extreme_pos_fpr/33.0}")
