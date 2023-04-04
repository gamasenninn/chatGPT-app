import pandas as pd
import re

def parse_vtt(file_name):
    with open(file_name, "r", encoding="utf-16", errors="ignore") as file:
        content = file.read()

    cues = content.strip().split("\n\n")[1:]
    time_ranges = []
    texts = []

    for cue in cues:
        lines = cue.strip().split("\n")
        print(f"lines:{lines}")

        if len(lines) == 3:
            _, time_range, text = lines
        else:
            time_range, text = lines
        start_time, end_time = time_range.split(" --> ")

        time_ranges.append((start_time, end_time))
        texts.append(text)

    return time_ranges, texts

def create_dataframe_from_vtt(file_name):
    time_ranges, texts = parse_vtt(file_name)
    data = {
        "Start_Time": [start_time for start_time, _ in time_ranges],
        "End_Time": [end_time for _, end_time in time_ranges],
        "Text": texts
    }
    df = pd.DataFrame(data)
    return df

vtt_file = "L_file.vtt"
df = create_dataframe_from_vtt(vtt_file)
print(df)
