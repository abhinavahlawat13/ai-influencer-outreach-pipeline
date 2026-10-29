import re
from typing import Dict

# Regex patterns for contact & social extraction
EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
INSTA_REGEX = r'(?:instagram\.com/|ig:\s*@?|insta:\s*@?)([a-zA-Z0-9_.]{3,30})'
WEBSITE_REGEX = r'https?://(?!(?:www\.)?(?:youtube\.com|youtu\.be|instagram\.com|twitter\.com|x\.com|discord\.gg|t\.me))[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?'

class ProfileEnricher:
    """
    Enriches influencer profiles with:
    - Contact Email (strictly labeled 'Not Found' if absent)
    - Content Themes (derived from bio + recent video context)
    - Optional links (Instagram handle, Website)
    """
    @staticmethod
    def enrich(profile: Dict) -> Dict:
        description = profile.get("description", "")
        recent_title = profile.get("recent_video_title", "")
        combined_text = f"{description} {recent_title}"

        # 1. Extract Contact Email (Strict 'Not Found' constraint)
        email_matches = re.findall(EMAIL_REGEX, description)
        # Filter out common false-positive image/asset extensions
        valid_emails = [
            e.lower().rstrip('.') for e in email_matches
            if not e.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
        ]
        contact_email = valid_emails[0] if valid_emails else "Not Found"

        # 2. Extract Optional Instagram Handle
        insta_match = re.search(INSTA_REGEX, description, re.IGNORECASE)
        instagram_handle = f"@{insta_match.group(1)}" if insta_match else "Not Found"

        # 3. Extract Optional Website URL
        web_match = re.search(WEBSITE_REGEX, description, re.IGNORECASE)
        website = web_match.group(0) if web_match else "Not Found"

        # 4. Classify Content Themes based on Gaming Sub-niches
        theme_map = {
            "Valorant / Tactical FPS": ["valorant", "csgo", "cs2", "tactical", "aim", "lineup"],
            "Battle Royale (BGMI/Apex)": ["bgmi", "pubg", "apex", "warzone", "battle royale"],
            "Minecraft & Sandbox": ["minecraft", "smp", "redstone", "roblox", "sandbox", "survival"],
            "GTA & Open World RP": ["gta", "roleplay", "rp", "cyberpunk", "open world"],
            "Game Reviews & Walkthroughs": ["review", "walkthrough", "playthrough", "indie", "lore"],
            "Esports & Competitive Highlights": ["montage", "highlights", "esports", "ranked", "tournament", "clips"]
        }

        detected_themes = []
        lower_text = combined_text.lower()
        for theme_label, keywords in theme_map.items():
            if any(kw in lower_text for kw in keywords):
                detected_themes.append(theme_label)

        content_themes = ", ".join(detected_themes) if detected_themes else "General Gaming & Gameplay"

        # Update and return enriched dictionary
        enriched_profile = profile.copy()
        enriched_profile.update({
            "contact_email": contact_email,
            "instagram": instagram_handle,
            "website": website,
            "content_themes": content_themes
        })

        return enriched_profile