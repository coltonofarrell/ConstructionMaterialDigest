from digest import fetch_and_summarize_articles
from emailer import send_email
from datetime import date

def main():
    print("🔧 Generating construction materials digest...")
    today = date.today().isoformat()
    subject = f"📬 Construction Materials Digest – {today}"

    summaries = fetch_and_summarize_articles()
    if not summaries:
        print("❌ No articles found.")
        return

    body = f"Here’s the latest news on construction materials suppliers for {today}:\n\n"
    for entry in summaries:
        body += f"📰 Title: {entry['title']}\n"
        body += f"📝 Summary: {entry['summary']}\n"
        body += f"🔗 Link: {entry['url']}\n\n"

    send_email(subject, body)
    print("✅ Digest sent successfully!")

if __name__ == "__main__":
    main()
