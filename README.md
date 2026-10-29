A production-ready, modular Python system that automates the end-to-end workflow of discovering micro-influencers on YouTube, filtering them against strict qualification thresholds, enriching their profile metadata, generating AI-powered personalized outreach messages, and managing a deduplicated sending/tracking layer.

---

## 🛠️ Tech Stack & Architecture

- **Language:** Python 3.13
- **Data Discovery:** `yt-dlp` (Zero-cost, API-key-free YouTube scraping)
- **Data Processing & Validation:** Pandas, Pydantic, Regex
- **AI Personalization:** Gemini API (`google-genai`) with structured JSON outputs
- **Storage & State Management:** SQLite (`data/outreach.db`) & CSV logs

---

## 📂 Project Structure

```text
assignment 1/
├── data/
│   ├── influencers_dataset.csv  # Discovered 52+ profiles with pass/fail audit status (Deliverable B)
│   ├── outreach_tracker.csv     # Final execution & outreach log (Deliverable D)
│   └── outreach.db              # SQLite database for deduplication & state
├── src/
│   ├── __init__.py
│   ├── discovery.py             # YouTube channel scraper
│   ├── filter.py                # Niche, follower (5k-10k), & engagement filters
│   ├── enricher.py              # Regex email parser & sub-niche classifier
│   ├── personalizer.py          # Gemini API prompt generator (Email + IG DM)
│   └── sender.py                # SMTP / Simulation dispatcher & deduplicator
├── config.py                    # Threshold configuration & environment variables
├── requirements.txt             # Project dependencies
├── main.py                      # Master pipeline orchestrator
└── README.md                    # Documentation