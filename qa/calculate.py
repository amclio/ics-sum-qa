from deal_with_csv import format_csv


def count_overall_systems_with_highest_avg_fscore(df):
    overall_result_dict = {}
    grouped_df = df.groupby("topic")

    for _, group in grouped_df:
        max_fscore = group["avg_fscore"].max()
        systems_with_max_fscore = group[group["avg_fscore"] == max_fscore]["system"]
        systems_count = systems_with_max_fscore.value_counts().to_dict()

        # accumulate the counts for each system
        for system, count in systems_count.items():
            if system in overall_result_dict:
                overall_result_dict[system] += count
            else:
                overall_result_dict[system] = count

    # NOTE: Calc Averages
    for system, count in overall_result_dict.items():
        overall_result_dict[system] = count / len(df[df["system"] == system].index)

    return overall_result_dict


df = format_csv()

overall_result_dict = count_overall_systems_with_highest_avg_fscore(df)

print(overall_result_dict)
for system, count in overall_result_dict.items():
    print(f"System: {system}, Count: {count}")
