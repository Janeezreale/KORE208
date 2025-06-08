import pandas as pd
import re


def processing(text):
    text = str(text)
    text = re.sub(r"\(.*?\)", "", text)                    
    text = re.sub(r"https?://[^\s]+", "", text)            
    text = re.sub(r"@\S+", "", text)                       
    text = text.replace("\n", " ").replace("\r", " ")   
    text = re.sub(r"[^ㄱ-ㅎ가-힣0-9a-zA-Z ]", "", text)     
    text = re.sub(r"\s+", " ", text).strip()               
    return text


csv_files = ["topics/itaewon_case_youtube_2022.csv", "topics/presidential_election_youtube_2022.csv"]
             
# csv_files = ["topics/ai_content_expansion.csv",
#              "topics/busan_expo_youtube.csv",
#              "topics/fukushima_youtube.csv",
#              "topics/israel_palestine_youtube.csv",
#              "topics/itaewon_2023_youtube.csv",
#              "topics/shillim_station_case_youtube.csv"]

max_comments = 4000
short_comments = 5
long_comments = 300

comments_per_file = max_comments // len(csv_files)
remaining_comments_needed = max_comments % len(csv_files)


all_comments = []
for file in csv_files:
    df = pd.read_csv(file)
    if "time" in df.columns:
        df = df.drop(columns=["time"])

    df = df.dropna(subset=["text"])
    df["text"] = df["text"].apply(processing)
    df = df.drop_duplicates(subset=["text"])

    df = df[df["text"].str.len() >= short_comments]
    df = df[df["text"].str.len() <= long_comments]

    # Store cleaned comments as list
    comments = df["text"].tolist()
    all_comments.append(comments)


final_comments = []

# collect up to comments_per_file from each file
for i, comment_list in enumerate(all_comments):
    take = min(comments_per_file, len(comment_list))
    final_comments.extend(comment_list[:take])
    all_comments[i] = comment_list[take:]  # Save leftovers for later

# fill remaining slots from any file that has leftover comments
while len(final_comments) < max_comments and remaining_comments_needed > 0:
    for comment_list in all_comments:
        if comment_list and len(final_comments) < max_comments:
            final_comments.append(comment_list.pop(0))
            remaining_comments_needed -= 1


pd.DataFrame({"text": final_comments}).to_csv("2022_cleaned.txt", index=False, encoding="utf-8", line_terminator="\n")

# print(f"Saved {len(final_comments)} cleaned comments to 2022_cleaned.txt")