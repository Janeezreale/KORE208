from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_RECENT
from itertools import islice
import pandas as pd
import os

# List of YouTube URLs
video_urls = [
    'https://www.youtube.com/watch?v=skMJbOLdo5E',
    'https://www.youtube.com/watch?v=goFnDYYbHkA&t=7s',
    'https://www.youtube.com/watch?v=c8SD7UCUjjk',
    'https://www.youtube.com/watch?v=drhjaXX5ij8',
    'https://www.youtube.com/watch?v=qq-Pr7iFSkE',
    'https://www.youtube.com/watch?v=sIaLQwhyWbc',
    'https://www.youtube.com/watch?v=6N7yMX4kmN8'
]

# Initialize the downloader
downloader = YoutubeCommentDownloader()

# Helper to extract a slug/video ID from URL
def slugify_url(url):
    return url.split("/")[-1] or "video"

# Output directory
output_dir = "metoo_comment"
os.makedirs(output_dir, exist_ok=True)

for url in video_urls:
    print(f"Downloading comments for: {url}")
    
    video_id = slugify_url(url)
    csv_file = os.path.join(output_dir, f"{video_id}.txt")

    # Download comments and keep only needed fields
    raw_comments = islice(downloader.get_comments_from_url(url, sort_by=SORT_BY_RECENT), 1000)

    filtered_comments = [{"text": c["text"]} for c in raw_comments if "text" in c]

    # Save to CSV

    df = pd.DataFrame(filtered_comments)
    df.to_csv(csv_file, index=False, encoding='utf-8')

    print(f"Saved {len(filtered_comments)} comments to {csv_file}")


