import yt_dlp
from typing import List, Dict

class YouTubeGamingDiscovery:
    """
    Zero-API-key YouTube discovery engine using yt-dlp.
    Extracts 50+ real gaming micro-influencer profiles, metrics, and descriptions.
    """
    def __init__(self):
        # Targeted search queries where gaming creators include business emails in descriptions
        self.search_queries = [
            "ytsearch20:valorant montage gameplay business email",
            "ytsearch20:minecraft smp lets play business inquiry",
            "ytsearch20:bgmi highlights streamer contact email",
            "ytsearch20:indie game review walkthrough contact",
            "ytsearch20:apex legends ranked guide business"
        ]

    def discover_influencers(self, target_count: int = 52) -> List[Dict]:
        """Scrapes YouTube search results to discover 50+ unique real gaming channels."""
        discovered_channels = {}
        
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "ignoreerrors": True,
            "extract_flat": False,  # Extract full video & channel metadata
            "skip_download": True,
        }

        print(f"[Discovery] Scraping YouTube for {target_count}+ real gaming creators (No API Key required)...")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for query in self.search_queries:
                if len(discovered_channels) >= target_count:
                    break

                print(f"  -> Running query: {query.replace('ytsearch20:', '')}")
                try:
                    info = ydl.extract_info(query, download=False)
                    if not info or "entries" not in info:
                        continue

                    for entry in info["entries"]:
                        if not entry:
                            continue

                        channel_id = entry.get("channel_id") or entry.get("uploader_id")
                        if not channel_id or channel_id in discovered_channels:
                            continue

                        subs = entry.get("channel_follower_count") or 0
                        views = entry.get("view_count") or 0
                        likes = entry.get("like_count") or 0
                        comments = entry.get("comment_count") or 0

                        # Skip channels where subscriber count isn't publicly visible
                        if subs == 0:
                            continue

                        # Calculate engagement rate from video interactions vs channel subscribers
                        if likes > 0:
                            engagement_rate = round(((likes + comments) / max(subs, 1)) * 100, 2)
                        else:
                            # Fallback proxy using view-to-subscriber ratio if likes are hidden
                            engagement_rate = round((views / max(subs, 1)) * 5.0, 2)

                        engagement_rate = min(max(engagement_rate, 0.5), 25.0)

                        channel_url = entry.get("channel_url") or entry.get("uploader_url") or f"https://www.youtube.com/channel/{channel_id}"
                        description = entry.get("description") or ""

                        discovered_channels[channel_id] = {
                            "name": entry.get("channel") or entry.get("uploader") or "Unknown Creator",
                            "platform": "YouTube",
                            "profile_url": channel_url,
                            "followers": int(subs),
                            "engagement_rate": engagement_rate,
                            "description": description,
                            "recent_video_title": entry.get("title", ""),
                            "niche": "Gaming"
                        }

                        print(f"     [+] Found: {discovered_channels[channel_id]['name']} ({subs:,} subs)")

                        if len(discovered_channels) >= target_count:
                            break
                except Exception as e:
                    print(f"  [!] Query error: {e}")
                    continue

        results = list(discovered_channels.values())
        print(f"[Discovery] Completed! Collected {len(results)} unique real gaming channels.")
        return results