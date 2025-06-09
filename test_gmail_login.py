import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

email = os.getenv("GMAIL_USER")
password = os.getenv("GMAIL_PASSWORD")

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email, password)
        print("✅ Login successful!")
except Exception as e:
        print(f"❌ Login failed: {e}")

