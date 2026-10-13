"""Generate a Seedance 2.5 text-to-video clip with the Higgsfield API.

Reads HF_KEY (key-id:key-secret) from .env.local next to this file, or from the
environment. Prints the video URL on success and exits non-zero otherwise.
"""

import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

import higgsfield_client

MODEL = "bytedance/seedance-2.5/text-to-video"
ARGUMENTS = {
    "prompt": "A cinematic scene at sunset",
    "duration": 5,
    "resolution": "720p",
    "aspect_ratio": "16:9",
}


def find_video_url(result):
    video = result.get("video")
    if isinstance(video, dict) and video.get("url"):
        return video["url"]
    videos = result.get("videos")
    if isinstance(videos, list) and videos and isinstance(videos[0], dict):
        return videos[0].get("url")
    return None


def main():
    load_dotenv(Path(__file__).with_name(".env.local"))

    try:
        result = higgsfield_client.subscribe(
            MODEL,
            arguments=ARGUMENTS,
            on_enqueue=lambda request_id: print(f"Request {request_id} queued", file=sys.stderr),
        )
    except higgsfield_client.CredentialsMissedError:
        print("HF_KEY is not set. Add HF_KEY=key-id:key-secret to .env.local.", file=sys.stderr)
        return 1
    except higgsfield_client.HiggsfieldClientError as error:
        print(f"Higgsfield API error: {error}", file=sys.stderr)
        return 1
    except httpx.TransportError as error:
        print(f"Could not reach the Higgsfield API: {error}", file=sys.stderr)
        return 1

    # subscribe() returns the final request state whatever it is, so check it.
    status = result.get("status")
    request_id = result.get("request_id", "unknown")
    if status == "completed":
        url = find_video_url(result)
        if url:
            print(url)
            return 0
        print(
            f"Request {request_id} completed but no video URL was found "
            f"(response keys: {sorted(result)}).",
            file=sys.stderr,
        )
        return 1
    if status == "nsfw":
        print(f"Request {request_id} was blocked by content moderation.", file=sys.stderr)
    elif status == "failed":
        print(f"Request {request_id} failed.", file=sys.stderr)
    elif status == "canceled":
        print(f"Request {request_id} was canceled.", file=sys.stderr)
    else:
        print(f"Request {request_id} ended with unexpected status {status!r}.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
