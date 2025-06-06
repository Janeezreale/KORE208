from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_RECENT
import pandas as pd
import os

output_dir = "ai_content_expansion"
url_file_path = f'all_links/{output_dir}.txt'

os.makedirs(output_dir, exist_ok=True)

with open(url_file_path, 'r') as f:
    video_urls = [line.strip() for line in f if line.strip()]

downloader = YoutubeCommentDownloader()

def slugify_url(url):
    return url.split("/")[-1].split("?")[0].split("&")[0]

comments_in_total = 0

for url in video_urls:
    print(f"Downloading filtered comments for: {url}")
    video_id = slugify_url(url)
    csv_file = os.path.join(output_dir, f"{video_id}.csv")

    try:
        filtered_comments = []

        for comment in downloader.get_comments_from_url(url, sort_by=SORT_BY_RECENT):
            if "text" in comment and "time" in comment:
                if comment["time"] in ["2년 전", "1년 전"]:
                    filtered_comments.append({
                        "time": comment["time"], 
                        "text": comment["text"]
                    })

            if len(filtered_comments) >= 1100:
                break

        pd.DataFrame(filtered_comments).to_csv(csv_file, index=False, encoding='utf-8')

        print(f"Saved {len(filtered_comments)} comments to {csv_file}")
        comments_in_total += len(filtered_comments)
    except Exception as e:
        print(f"Failed to download comments for {url}: {e}")

# print(f"{comments_in_total} comments saved in total")



# ai_content_expansion - 120
# busan_expo_youtube - 9168
# fukushima_youtube - 10765
# israel_palestine_youtube - 19302

# itaewon_2023 TWITTER - 69
# itaewon_2023_youtube - 9277

# itaewon_case_2022 TWITTER - 485
# itaewon_case_youtube_2022 - 27601

# presidential_election_2022 TWITTER - 402
# presidential_election_youtube_2022 - 1247 

# shillim_station_case_youtube - 4502



