import pandas as pd


def create_demonstrations(
    dataset: str, number_of_demonstrations_per_label: int, number_of_random_demonstrations: int
) -> str:
    if dataset == "SST5":
        path = "unstated_norms_llm_bias/prompt_based_classification/resources/processed_sst5.tsv"
    else:
        path = "unstated_norms_llm_bias/prompt_based_classification/resources/processed_semeval.tsv"
    if dataset != "ZeroShot":
        df = pd.read_csv(path, sep="\t", header=0)
        # Trying to balance the number of labels represented in the demonstrations
        sample_df_negative = df.Valence[df.Valence.eq("Negative")].sample(number_of_demonstrations_per_label).index
        sample_df_neutral = df.Valence[df.Valence.eq("Neutral")].sample(number_of_demonstrations_per_label).index
        sample_df_positive = df.Valence[df.Valence.eq("Positive")].sample(number_of_demonstrations_per_label).index
        random_sampled_df = df.sample(number_of_random_demonstrations).index
        sampled_df = df.loc[
            sample_df_negative.union(sample_df_neutral).union(sample_df_positive).union(random_sampled_df)
        ]
        texts = sampled_df["Text"].tolist()
        valences = sampled_df["Valence"].tolist()

        demonstrations = ""
        for text, valence in zip(texts, valences):
            demonstrations = (
                f"{demonstrations}Text: {text}\nQuestion: What is the sentiment of the text?\nAnswer: {valence}.\n\n"
            )
        print("Example of demonstrations")
        print("---------------------------------------------------------------------")
        print(demonstrations)
        print("---------------------------------------------------------------------")
        return demonstrations
    else:
        return ""
