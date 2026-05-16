import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

_API_KEY = os.getenv("YOUTUBE_API_KEY")
_SERVICE = "youtube"
_VERSION = "v3"


@dataclass
class VideoSignal:
    video_id: str
    title: str
    tags: list[str]
    view_count: int
    like_count: int
    published_at: str
    category_id: str
    description: str
    source: str  # "trending" or "rising"


def fetch_trending(region_code: str = "US", max_results: int = 50) -> list[VideoSignal]:
    """Returns the current most-popular videos for a region."""
    client = build(_SERVICE, _VERSION, developerKey=_API_KEY)
    try:
        response = client.videos().list(
            part="snippet,statistics",
            chart="mostPopular",
            regionCode=region_code,
            maxResults=max_results,
        ).execute()
    except HttpError as e:
        raise RuntimeError(f"YouTube API error (trending): {e}") from e

    return [_parse(item, "trending") for item in response.get("items", [])]


def fetch_rising(topic: str, region_code: str = "US", max_results: int = 50) -> list[VideoSignal]:
    """Returns videos for a topic published in the last 72 hours, sorted by view count."""
    client = build(_SERVICE, _VERSION, developerKey=_API_KEY)
    published_after = (
        datetime.now(timezone.utc) - timedelta(hours=72)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")

    try:
        search_resp = client.search().list(
            part="id",
            q=topic,
            type="video",
            order="viewCount",
            publishedAfter=published_after,
            regionCode=region_code,
            maxResults=max_results,
        ).execute()
    except HttpError as e:
        raise RuntimeError(f"YouTube API error (rising search): {e}") from e

    video_ids = [item["id"]["videoId"] for item in search_resp.get("items", [])]
    if not video_ids:
        return []

    try:
        videos_resp = client.videos().list(
            part="snippet,statistics",
            id=",".join(video_ids),
        ).execute()
    except HttpError as e:
        raise RuntimeError(f"YouTube API error (rising details): {e}") from e

    return [_parse(item, "rising") for item in videos_resp.get("items", [])]


def _parse(item: dict, source: str) -> VideoSignal:
    snippet = item.get("snippet", {})
    stats = item.get("statistics", {})
    return VideoSignal(
        video_id=item["id"],
        title=snippet.get("title", ""),
        tags=snippet.get("tags", []),
        view_count=int(stats.get("viewCount", 0)),
        like_count=int(stats.get("likeCount", 0)),
        published_at=snippet.get("publishedAt", ""),
        category_id=snippet.get("categoryId", ""),
        description=snippet.get("description", ""),
        source=source,
    )
