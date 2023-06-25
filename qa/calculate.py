from deal_with_csv import format_csv
import pandas as pd


def count_overall_systems_with_highest_avg_fscore(df):
    overall_result_dict = {}
    grouped_df = df.groupby("topic")
    system_count = len(pd.unique(df["system"]))

    groups = []

    for _, group in grouped_df:
        if len(group.index) == system_count:
            groups.append(group)

    for group in groups:
        max_fscore = group["avg_fscore"].max()
        systems_with_max_fscore = group[group["avg_fscore"] == max_fscore]["system"]
        systems_count = systems_with_max_fscore.value_counts().to_dict()

        if len(group.index) != system_count:
            continue

        # accumulate the counts for each system
        for system, count in systems_count.items():
            if system in overall_result_dict:
                overall_result_dict[system]["hit"] += count
            else:
                overall_result_dict[system] = {}
                overall_result_dict[system]["count"] = len(groups)
                overall_result_dict[system]["hit"] = count

    # NOTE: Calc Averages
    for system, var in overall_result_dict.items():
        overall_result_dict[system]["avg"] = (
            var["hit"] / overall_result_dict[system]["count"]
        )

    return overall_result_dict


df = format_csv()

overall_result_dict = count_overall_systems_with_highest_avg_fscore(df)

for system, var in overall_result_dict.items():
    print(
        f"System: {system}, Count: {var['count']}, Hit: {var['hit']}, Avg: {var['avg']}"
    )
