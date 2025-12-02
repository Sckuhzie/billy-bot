import difflib
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

# Replace with your API key
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
DISCORD_LIMIT = 2000


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


def diff_with_context(old_playlist, new_playlist):
    diff = list(
        difflib.unified_diff(
            old_playlist,
            new_playlist,
            fromfile="Old Playlist",
            tofile="New Playlist",
            lineterm="",
        )
    )

    result = "```\n"
    i = 0

    while i < len(diff):
        line = diff[i]

        if not (line.startswith("+++") or line.startswith("---")):
            if line.startswith("@@"):
                result += f"\n{line}\n"
            elif line.startswith(" "):
                result += "=" + line[1:]
            else:
                result += line

        i += 1

    result += "```"
    return result


def split_discord_message(message: str):
    """
    Splits a long diff message into multiple Discord-safe parts (< 2000 chars),
    ensuring no chunk is split in the middle of a line.
    Each chunk is wrapped in its own ```diff code block.
    """
    parts = []

    # Strip outer code block if present
    if message.startswith("```") and message.endswith("```"):
        inner = message[3:-3].strip("\n")
    else:
        inner = message

    lines = inner.split("\n")

    current_chunk = ""
    for line in lines:
        if len(current_chunk) + len(line) + 1 > (DISCORD_LIMIT - 10):
            parts.append(f"```diff\n{current_chunk.rstrip()}\n```")
            current_chunk = ""

        current_chunk += line + "\n"

    # Add last chunk
    if current_chunk.strip():
        parts.append(f"```diff\n{current_chunk.rstrip()}\n```")

    return parts


def get_playlist_diff(playlist_id: str):

    file1_path = f"bot/playlists_files/{playlist_id}.txt"

    # Read playlists
    with open(file1_path, "r", encoding="utf-8") as f1:
        old_playlist_lines = f1.readlines()
    version_date = old_playlist_lines[0].rstrip("\n")
    old_playlist = old_playlist_lines[1:]

    # new_playlist = [f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"]
    new_playlist = []
    for v in get_playlist_videos(playlist_id):
        new_playlist.append(f"{v['title']} — {v['url']}\n")

    full_message = diff_with_context(old_playlist, new_playlist)
    list_message = split_discord_message(full_message)

    return version_date, list_message


def save_playlist_txt(playlist_id: str):
    video_list = get_playlist_videos(playlist_id=playlist_id)
    txt_output = f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
    for v in video_list:
        txt_output += f"{v['title']} — {v['url']}\n"

    with open(f"bot/playlists_files/{playlist_id}.txt", "w", encoding="utf-8") as f:
        f.write(txt_output)

    return txt_output
