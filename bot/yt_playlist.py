import difflib
import os

import requests
from dotenv import load_dotenv

load_dotenv()

# Replace with your API key
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Replace with your playlist ID
PLAYLIST_ID = "PLs5RvnKyJmy74KrJ0YdR_W3zFvKRfMwTE"  # Playlist de la loose
# PLAYLIST_ID = "PLs5RvnKyJmy55bJR-uYQHyZk4DMoqZGAg"  # Surplus

playlists_dict = {
    "loose": "PLs5RvnKyJmy74KrJ0YdR_W3zFvKRfMwTE",
    "surplus": "PLs5RvnKyJmy55bJR-uYQHyZk4DMoqZGAg",
}


def get_playlist_videos(playlist_id):
    videos = []
    base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        "part": "snippet",
        "playlistId": playlist_id,
        "maxResults": 50,
        "key": YOUTUBE_API_KEY,
    }

    while True:
        response = requests.get(base_url, params=params)
        data = response.json()

        if "items" not in data:
            raise Exception(f"Error fetching playlist: {data}")

        for item in data["items"]:
            title = item["snippet"]["title"]
            video_id = item["snippet"]["resourceId"]["videoId"]
            videos.append(
                {"title": title, "url": f"https://www.youtube.com/watch?v={video_id}"}
            )

        if "nextPageToken" in data:
            params["pageToken"] = data["nextPageToken"]
        else:
            break

    return videos


def get_playlist_diff(playlist_id: str):

    file1_path = f"bot/playlists_files/{playlist_id}.txt"

    # Read playlists
    with open(file1_path, "r", encoding="utf-8") as f1:
        old_playlist = f1.readlines()

    new_playlist = []
    for v in get_playlist_videos(playlist_id):
        new_playlist.append(f"{v['title']} — {v['url']}\n")

    # Create diff
    diff = difflib.unified_diff(
        old_playlist,
        new_playlist,
        fromfile="Old Playlist",
        tofile="New Playlist",
        lineterm="",
    )

    # Format for Discord code block
    discord_message = "```diff\n"
    for line in diff:
        if line.startswith("+") and not line.startswith("+++"):
            discord_message += f"{line}\n"  # green for additions
        elif line.startswith("-") and not line.startswith("---"):
            discord_message += f"{line}\n"  # red for removals
    discord_message += "```"

    return discord_message

    # print(discord_message)

    # pass


def save_playlist_txt(playlist_id: str):
    video_list = get_playlist_videos(playlist_id=playlist_id)
    txt_output = ""
    for v in video_list:
        txt_output += f"{v['title']} — {v['url']}\n"

    with open(f"bot/playlists_files/{playlist_id}.txt", "w", encoding="utf-8") as f:
        f.write(txt_output)

    return txt_output


if __name__ == "__main__":
    video_list = get_playlist_videos(YOUTUBE_API_KEY, PLAYLIST_ID)
    for i in range(len(video_list)):
        v = video_list[i]
        # print(f"{i+1} - {v['title']} — {v['url']}")
        print(f"{v['title']} — {v['url']}")
