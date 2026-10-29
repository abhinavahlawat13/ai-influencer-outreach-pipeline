import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from config import GEMINI_API_KEY

class OutreachMessage(BaseModel):
    email_pitch: str = Field(description="Personalized collaboration email pitch between 60 and 90 words.")
    instagram_dm: str = Field(description="Short, natural Instagram DM between 15 and 30 words.")
    collaboration_angle: str = Field(description="Proposed angle such as Sponsored Integration, UGC, or Affiliate.")

class MessagePersonalizer:
    """
    Uses Gemini API to dynamically generate personalized outreach messages
    tailored to each gaming creator's specific niche and recent content.
    """
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

    def generate(self, influencer: dict) -> OutreachMessage:
        name = influencer.get("name", "Creator")
        themes = influencer.get("content_themes", "Gaming")
        recent_video = influencer.get("recent_video_title", "your recent videos")
        followers = influencer.get("followers", 0)

        # Fallback deterministic template if API key is not provided during local testing
        if not self.client:
            return OutreachMessage(
                email_pitch=(
                    f"Hi {name}, I've been following your gaming content and really enjoyed your video on {recent_video}. "
                    f"Given your active audience of {followers:,} gaming enthusiasts in the {themes} space, we would love to "
                    f"partner with you on a sponsored product integration. We offer competitive compensation and free gear. "
                    f"Would you be open to reviewing our campaign brief this week?"
                ),
                instagram_dm=f"Hey {name}, loved your recent setup on {recent_video}! Reaching out regarding a paid gaming sponsorship if you're open?",
                collaboration_angle="Sponsored Integration"
            )

        prompt = f"""
        You are an influencer marketing manager for a gaming brand. Generate two tailored outreach messages for this gaming creator:
        - Name: {name}
        - Platform: YouTube
        - Followers: {followers:,}
        - Content Themes: {themes}
        - Recent Video Context: {recent_video}

        Strict constraints:
        1. Email Pitch: Strictly between 60 and 90 words. Mention their recent content, niche, community fit, and a clear value proposition for a paid sponsorship or product collaboration.
        2. Instagram DM: Strictly between 15 and 30 words. Extremely natural, punchy, conversational, and non-spammy.
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=OutreachMessage,
                    temperature=0.4
                )
            )
            return OutreachMessage.model_validate_json(response.text)
        except Exception as e:
            print(f"[Warning] Gemini API generation failed for {name}: {e}. Falling back to template.")
            return OutreachMessage(
                email_pitch=(
                    f"Hi {name}, we loved your recent content around {recent_video}. With your engaged audience "
                    f"of {followers:,} gaming fans, we'd love to collaborate on a sponsored gaming gear campaign."
                ),
                instagram_dm=f"Hey {name}, great work on {recent_video}! Would love to discuss a quick gaming partnership.",
                collaboration_angle="Sponsorship"
            )