# youtube_api.py
# ShrutiBots API integration for Telegram Music Userbot

import os
import aiohttp
from py_yt import VideosSearch

FALLBACK_API_URL = "https://shrutibots.site"
YOUR_API_URL = FALLBACK_API_URL


async def search_youtube(query: str):
    """
    Search YouTube and return first result details.
    """
    try:
        results = VideosSearch(query, limit=1)
        data = await results.next()

        if not data["result"]:
            return None

        result = data["result"][0]

        return {
            "title": result["title"],
            "duration": result.get("duration", "0:00"),
            "thumbnail": result["thumbnails"][0]["url"].split("?")[0],
            "video_id": result["id"],
            "url": result["link"],
        }
    except Exception as e:
        print(f"[ERROR] Search failed: {e}")
        return None


async def download_song(video_id: str):
    """
    Download song using ShrutiBots API
    """
    download_dir = "downloads"
    os.makedirs(download_dir, exist_ok=True)

    file_path = os.path.join(download_dir, f"{video_id}.mp3")

    if os.path.exists(file_path):
        return file_path

    try:
        async with aiohttp.ClientSession() as session:
            params = {"url": video_id, "type": "audio"}

            async with session.get(
                f"{YOUR_API_URL}/download",
                params=params,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:

                if response.status != 200:
                    return None

                data = await response.json()
                token = data.get("download_token")

                if not token:
                    return None

                stream_url = f"{YOUR_API_URL}/stream/{video_id}?type=audio"

                async with session.get(
                    stream_url,
                    headers={"X-Download-Token": token},
                    timeout=aiohttp.ClientTimeout(total=300)
                ) as file_response:

                    if file_response.status != 200:
                        return None

                    with open(file_path, "wb") as f:
                        async for chunk in file_response.content.iter_chunked(16384):
                            f.write(chunk)

        return file_path

    except Exception as e:
        print(f"[ERROR] Download failed: {e}")
        return None


async def get_song(query: str):
    """
    Search and download in one step
    """
    result = await search_youtube(query)

    if not result:
        return None

    file_path = await download_song(result["video_id"])

    if not file_path:
        return None

    result["file_path"] = file_path
    return result
