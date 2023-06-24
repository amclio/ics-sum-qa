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
                overall_result_dict[system]["hit"] += count
            else:
                overall_result_dict[system] = {}
                overall_result_dict[system]["hit"] = count

    # NOTE: Calc Averages
    for system, var in overall_result_dict.items():
        count = len(df[df["system"] == system].index)
        overall_result_dict[system]["count"] = count
        overall_result_dict[system]["avg"] = var["hit"] / count

    return overall_result_dict


df = format_csv()

overall_result_dict = count_overall_systems_with_highest_avg_fscore(df)

for system, var in overall_result_dict.items():
    print(
        f"System: {system}, Count: {var['count']}, Hit: {var['hit']}, Avg: {var['avg']}"
    )
