from typing import Tuple, Dict
from config import MIN_FOLLOWERS, MAX_FOLLOWERS, MIN_ENGAGEMENT_RATE, GAMING_KEYWORDS

class InfluencerFilter:
    """
    Filters and classifies discovered profiles based on micro-influencer criteria:
    - Follower range: 5,000 to 10,000
    - Engagement rate: >= 2.0%
    - Content/Niche relevance: Gaming keywords check
    """
    @staticmethod
    def evaluate(influencer: Dict) -> Tuple[bool, str]:
        followers = influencer.get("followers", 0)
        engagement = influencer.get("engagement_rate", 0.0)
        description = influencer.get("description", "").lower()
        recent_title = influencer.get("recent_video_title", "").lower()
        niche = influencer.get("niche", "").lower()

        # 1. Follower Count Check (5k - 10k)
        if followers < MIN_FOLLOWERS:
            return False, f"FAILED: Followers ({followers:,}) below minimum {MIN_FOLLOWERS:,} threshold"
        if followers > MAX_FOLLOWERS:
            return False, f"FAILED: Followers ({followers:,}) exceed maximum {MAX_FOLLOWERS:,} target cap"

        # 2. Engagement Rate Check
        if engagement < MIN_ENGAGEMENT_RATE:
            return False, f"FAILED: Engagement rate ({engagement}%) below minimum {MIN_ENGAGEMENT_RATE}% requirement"

        # 3. Brand-Fit & Content Relevance Check
        combined_text = f"{description} {recent_title} {niche}"
        matched_keywords = [kw for kw in GAMING_KEYWORDS if kw in combined_text]
        if not matched_keywords:
            return False, "FAILED: No relevant gaming niche keywords found in profile/content"

        return True, "PASSED: Meets 5k-10k follower, engagement, and gaming niche criteria"