import os
import pandas as pd
from src.discovery import YouTubeGamingDiscovery
from src.filter import InfluencerFilter
from src.enricher import ProfileEnricher
from src.personalizer import MessagePersonalizer
from src.sender import OutreachSender

def main():
    os.makedirs("data", exist_ok=True)
    print("\n" + "=" * 70)
    print("EDXSO AI ENGINEER INTERN - AUTOMATED GAMING INFLUENCER OUTREACH SYSTEM")
    print("=" * 70)

    # Phase 1: Discovery
    print("\n[Phase 1] Discovering 50+ Gaming Micro-Influencers from YouTube (yt-dlp)...")
    discovery = YouTubeGamingDiscovery()
    raw_creators = discovery.discover_influencers(target_count=52)
    print(f"-> Total unique channels discovered: {len(raw_creators)}")

    # Phase 2 & 3: Filtering & Enrichment
    print("\n[Phase 2 & 3] Evaluating Filtering Criteria & Enriching Profiles...")
    dataset_records = []
    qualified_influencers = []

    for c in raw_creators:
        passed, reason = InfluencerFilter.evaluate(c)
        enriched = ProfileEnricher.enrich(c)

        # Build Master Dataset Record (Deliverable B requirement)
        dataset_records.append({
            "Name": enriched["name"],
            "Platform": enriched["platform"],
            "Followers": enriched["followers"],
            "Engagement": f"{enriched['engagement_rate']}%",
            "Niche": enriched["niche"],
            "Email": enriched["contact_email"],
            "Profile URL": enriched["profile_url"],
            "Content Theme": enriched["content_themes"],
            "Status": "PASSED" if passed else reason
        })

        if passed:
            qualified_influencers.append(enriched)

    # Save Master Influencer Dataset CSV
    df_dataset = pd.DataFrame(dataset_records)
    dataset_path = "data/influencers_dataset.csv"
    df_dataset.to_csv(dataset_path, index=False)
    print(f"-> Saved master dataset ({len(df_dataset)} records) to {dataset_path}")
    print(f"-> Qualified micro-influencers passing all gates: {len(qualified_influencers)}")

    # Phase 4 & 5: Personalization & Sending Layer
    print("\n[Phase 4 & 5] Generating AI Messages & Executing Sending Layer...")
    personalizer = MessagePersonalizer()
    sender = OutreachSender()

    for idx, inf in enumerate(qualified_influencers, 1):
        print(f"\n--------------------------------------------------")
        print(f"[{idx}/{len(qualified_influencers)}] Processing Creator: {inf['name']} ({inf['followers']:,} subs)")
        
        # Generate AI Messages
        messages = personalizer.generate(inf)
        print(f"  • IG DM ({len(messages.instagram_dm.split())} words): {messages.instagram_dm}")
        
        # Dispatch & Track
        status = sender.dispatch(inf, messages)
        print(f"  • Dispatch Status: {status}")

    # Export Outreach Tracker CSV (Deliverable D requirement)
    sender.export_tracker_csv()

    print("\n" + "=" * 70)
    print("[SUCCESS] Assignment pipeline execution completed successfully!")
    print("Check your 'data/' folder for:")
    print(" - influencers_dataset.csv (Deliverable B)")
    print(" - outreach_tracker.csv    (Deliverable D)")
    print("=" * 70)

if __name__ == "__main__":
    main()