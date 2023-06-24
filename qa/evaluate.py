from summaqa import QG_masked, QA_Metric
from os import listdir
from os.path import isfile, join
from deal_with_csv import write_csv, format_csv
from tqdm import tqdm
import re

question_generator = QG_masked()
qa_metric = QA_Metric()

sources_path = "./qa/sources"
summaries_path = "./qa/summaries"

sources_files = [f for f in listdir(sources_path) if isfile(join(sources_path, f))]
summaries_files = [
    f for f in listdir(summaries_path) if isfile(join(summaries_path, f))
]

formated_csv = format_csv()

results = []

for file_name in tqdm(sources_files):
    with open(sources_path + "/" + file_name, "r", encoding="utf-8") as file:
        text = file.read()

    masked_questions, answer_spans = question_generator.get_questions(text)
    file_name_without_ext = file_name.replace(".txt", "")

    summaries_current_files = list(
        filter(
            lambda item: re.search(r"(^.+)(?=-)", item).group(1)
            == file_name_without_ext,
            summaries_files,
        )
    )

    for summary_file in summaries_current_files:
        print(summary_file)
        with open(
            summaries_path + "/" + summary_file, "r", encoding="utf-8"
        ) as file_name:
            text = file_name.read()

        if summary_file in formated_csv["filename"].values:
            continue

        score = qa_metric.compute(masked_questions, answer_spans, text)
        score["filename"] = summary_file

        results.append(score)

write_csv(results)
