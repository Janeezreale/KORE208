from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_RECENT
from itertools import islice
import pandas as pd
import os

#유튜브 url 리스트 내 열거
video_urls = [
    "https://www.youtube.com/watch?v=5qEbije55FE",
    "https://www.youtube.com/watch?v=0kQmWpnw450"
]

downloader = YoutubeCommentDownloader()

#슬러그 혹은 비디오id 추출
def slugify_url(url):
    return url.split("/")[-1] or "video"

#저장할 파일 경로 지정
output_dir = "./2018_gangseo"
os.makedirs(output_dir, exist_ok=True)

for url in video_urls:
    print(f"Downloading comments for: {url}")
    

    video_id = slugify_url(url)
    csv_file = os.path.join(output_dir, f"{video_id}.csv")

    #수집량 지정
    raw_comments = islice(downloader.get_comments_from_url(url, sort_by=SORT_BY_RECENT), 1000)

    #텍스트, 댓글 작성 시기 수집 / 6년 전 작성된 댓글만 수집
    filtered_comments = [{"text": c["text"], "time": c["time"]} for c in raw_comments if "text" in c and "time" in c and "6년 전" in c["time"]]

    #CSV파일로 저장
    df = pd.DataFrame(filtered_comments)
    df.to_csv(csv_file, index=False, encoding='utf-8')

    print(f"Saved {len(filtered_comments)} comments to {csv_file}")