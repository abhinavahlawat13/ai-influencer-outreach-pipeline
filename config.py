import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

# Email settings
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
SIMULATION_MODE = os.getenv("SIMULATION_MODE", "true").lower() == "true"

# Micro-influencer thresholds (5k to 10k followers)
MIN_FOLLOWERS = 5000
MAX_FOLLOWERS = 10000
MIN_ENGAGEMENT_RATE = 2.0
TARGET_NICHE = "Gaming"

GAMING_KEYWORDS = [
    "gaming", "gameplay", "walkthrough", "streamer", "esports",
    "bgmi", "valorant", "minecraft", "gta", "fps", "roblox"
]