# modules/yt_api.py
from googleapiclient.discovery import build
from langdetect import detect
from datetime import datetime


def search_videos(api_key, query, max_results=5):
    """
    Cari video berdasarkan keyword.
    Return list videoId.
    """
    youtube = build("youtube", "v3", developerKey=api_key)
    try:
        res = youtube.search().list(
            part="id",
            q=query,
            type="video",
            maxResults=max_results
        ).execute()
        return [item["id"]["videoId"] for item in res.get("items", [])]
    except Exception as e:
        print(f"⚠️ Gagal search video: {e}")
        return []


def get_youtube_comments(api_key, video_id, max_comments=500, allowed_langs=None, include_replies=True):
    """
    Ambil komentar dari sebuah video dengan API.
    Bisa ambil top-level + replies.
    """
    youtube = build("youtube", "v3", developerKey=api_key)
    comments = []
    collected = 0

    try:
        request = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText"
        )

        while request and collected < max_comments:
            resp = request.execute()

            for item in resp.get("items", []):
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                text = snippet.get("textDisplay", "").strip()
                date = snippet.get("publishedAt", datetime.utcnow().isoformat())
                author = snippet.get("authorDisplayName", "unknown")
                likes = snippet.get("likeCount", 0)

                try:
                    lang = detect(text)
                except Exception:
                    lang = "und"

                if allowed_langs and lang not in allowed_langs:
                    continue

                comments.append({
                    "text": text,
                    "lang": lang,
                    "date": date,
                    "author": author,
                    "likes": likes,
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "source": "youtube_api"
                })
                collected += 1
                if collected >= max_comments:
                    break

                # === Ambil replies kalau ada ===
                if include_replies and "replies" in item:
                    for reply in item["replies"].get("comments", []):
                        r_snip = reply["snippet"]
                        r_text = r_snip.get("textDisplay", "").strip()
                        r_date = r_snip.get("publishedAt", datetime.utcnow().isoformat())
                        r_author = r_snip.get("authorDisplayName", "unknown")
                        r_likes = r_snip.get("likeCount", 0)

                        try:
                            r_lang = detect(r_text)
                        except Exception:
                            r_lang = "und"

                        if allowed_langs and r_lang not in allowed_langs:
                            continue

                        comments.append({
                            "text": r_text,
                            "lang": r_lang,
                            "date": r_date,
                            "author": r_author,
                            "likes": r_likes,
                            "url": f"https://www.youtube.com/watch?v={video_id}",
                            "source": "youtube_api_reply"
                        })
                        collected += 1
                        if collected >= max_comments:
                            break

            if collected >= max_comments:
                break

            request = youtube.commentThreads().list_next(request, resp)

    except Exception as e:
        print(f"⚠️ Error ambil komentar video {video_id}: {e}")

    return comments
