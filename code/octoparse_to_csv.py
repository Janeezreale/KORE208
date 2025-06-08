import json
import csv
from datetime import datetime, timezone
import dateutil.parser

links_2023 = {
    "https://x.com/news_NA/status/1611266511448207360",
    "https://x.com/WiseManU/status/1614162553529331712",
    "https://x.com/WiseManU/status/1649711410031788032",
    "https://x.com/WiseManU/status/1624318685845549056",
    "https://x.com/newsvop/status/1736582321992835418",
    "https://x.com/0926kgj/status/1737800742835200464",
    "https://x.com/yong_hyein/status/1727181126916256249",
    "https://x.com/newsvop/status/1736943329395519728",
    "https://x.com/LaborWithDream/status/1718498524550312205"
}

# Convert UTC time to relative format
def get_relative_time(utc_time_str):
    try:
        post_time = dateutil.parser.parse(utc_time_str)
        now = datetime.now(timezone.utc)
        delta = now - post_time

        years = delta.days // 365
        months = (delta.days % 365) // 30
        days = delta.days

        if years >= 1:
            return f"{years}년 전"
        elif months >= 1:
            return f"{months}개월 전"
        elif days >= 1:
            return f"{days}일 전"
        else:
            return "오늘"
    except:
        return ""


with open('presidential_election_twitter_2022_octoparse.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

rows_2023 = []
rows_2022 = []

for item in data:
    tweet_url = item.get("Tweet_Website", "")
    utc_time = item.get("Comment_Timestamp", "")
    comment = item.get("Comment_Content", "").replace('\r', '').replace('\n', '\\n')

    if utc_time and comment:
        relative_time = get_relative_time(utc_time)
        row = {"time": relative_time, "text": comment}

        if tweet_url in links_2023:
            rows_2023.append(row)
        else:
            rows_2022.append(row)

# Writing 2023 file
with open('presidential_election_twitter_2022_octoparse.csv', 'w', encoding='utf-8-sig', newline='') as f2023:
    writer = csv.DictWriter(f2023, fieldnames=["time", "text"])
    writer.writeheader()
    writer.writerows(rows_2023)

# Writing 2022 file
with open('presidential_election_twitter_2022_octoparse.csv', 'w', encoding='utf-8-sig', newline='') as f2022:
    writer = csv.DictWriter(f2022, fieldnames=["time", "text"])
    writer.writeheader()
    writer.writerows(rows_2022)
