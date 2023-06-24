import csv
import pandas as pd
import re


def write_csv(data):
    # names of the columns in your csv
    fieldnames = [
        "filename",
        "avg_prob",
        "avg_fscore",
    ]  # 'filename' is now the first column

    # name of the csv file where the data will be written
    filename = "output.csv"

    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Check if the file is empty
        if file.tell() == 0:
            writer.writeheader()

        for row in data:
            writer.writerow(row)

    print(f"Data appended to {filename}")


def format_csv():
    filename = "output.csv"
    df = pd.read_csv(filename)

    df["topic"] = ""
    df["system"] = ""

    for idx, row in df.iterrows():
        matches = re.search("(\w+)-(\w+)\.txt", row["filename"])

        # Use at[] to modify the DataFrame directly
        df.at[idx, "topic"] = matches.group(1)
        df.at[idx, "system"] = matches.group(2)

    return df
