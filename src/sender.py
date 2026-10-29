import sqlite3
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import pandas as pd
from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SIMULATION_MODE

class OutreachSender:
 
    def __init__(self, db_path: str = "data/outreach.db", tracker_csv: str = "data/outreach_tracker.csv"):
        self.db_path = db_path
        self.tracker_csv = tracker_csv
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS outreach_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    influencer_name TEXT,
                    email TEXT UNIQUE,
                    instagram_handle TEXT,
                    email_pitch TEXT,
                    instagram_dm TEXT,
                    sent_status TEXT,
                    sent_date TEXT
                )
            """)

    def is_duplicate(self, email: str) -> bool:
        if not email or email == "Not Found":
            return False
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM outreach_log WHERE email = ?", (email,))
            return cursor.fetchone() is not None

    def dispatch(self, influencer: dict, messages) -> str:
        name = influencer.get("name", "Unknown")
        email = influencer.get("contact_email", "Not Found")
        insta = influencer.get("instagram", "Not Found")

        # 1. Check if email is missing
        if email == "Not Found":
            status = "SKIPPED: No valid contact email found"
            self._log_to_db(name, email, insta, messages, status)
            return status

        # 2. Check for duplicate outreach
        if self.is_duplicate(email):
            status = "SKIPPED: Duplicate outreach prevented"
            return status

        # 3. Sending Layer (SMTP or Simulation)
        status = "SENT_SIMULATED"
        if not SIMULATION_MODE and SMTP_USER and SMTP_PASS:
            try:
                msg = MIMEText(messages.email_pitch)
                msg["Subject"] = f"Collaboration Opportunity // {name}"
                msg["From"] = SMTP_USER
                msg["To"] = email

                with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                    server.starttls()
                    server.login(SMTP_USER, SMTP_PASS)
                    server.send_message(msg)
                status = "SENT_SMTP_SUCCESS"
            except Exception as e:
                status = f"FAILED: SMTP Error ({str(e)[:40]})"

        # 4. Record to SQLite Database
        self._log_to_db(name, email, insta, messages, status)
        return status

    def _log_to_db(self, name, email, insta, messages, status):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        email_pitch = messages.email_pitch if messages else "N/A"
        insta_dm = messages.instagram_dm if messages else "N/A"

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO outreach_log 
                (influencer_name, email, instagram_handle, email_pitch, instagram_dm, sent_status, sent_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, email, insta, email_pitch, insta_dm, status, timestamp))

    def export_tracker_csv(self):
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query("""
                SELECT 
                    influencer_name AS Influencer,
                    email AS Email,
                    email_pitch AS [Message Generated],
                    CASE WHEN sent_status LIKE 'SENT%' THEN 'Yes' ELSE 'No' END AS Sent,
                    sent_date AS Date,
                    sent_status AS Status
                FROM outreach_log
            """, conn)
            df.to_csv(self.tracker_csv, index=False)
            print(f"[Sender] Outreach Tracker successfully exported to: {self.tracker_csv}")