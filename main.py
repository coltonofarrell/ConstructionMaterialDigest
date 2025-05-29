import requests
import openai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import datetime

# Retrieve your API keys and Gmail credentials from environment variables
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')

# Initialize the OpenAI client with the provided API key
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Function to fetch the top 5 headlines related to construction materials
def fetch_headlines():
    url = f'https://newsapi.org/v2/everything?q=construction materials supplier&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data.get('articles', [])
    return articles[:5]  # Limit to top 5 articles

# Function to summarize an article using OpenAI's ChatCompletion API
def summarize_article(article):
    prompt = f"Summarize this article for a construction industry newsletter: {article['title']} - {article['description']} - {article['url']}"

    # Use the gpt-3.5-turbo model
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use gpt-3.5-turbo instead of gpt-4
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    # Extract and return the summary
    summary = response['choices'][0]['message']['content'].strip()
    return summary

# Function to send the digest email
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = GMAIL_USER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASSWORD)
    server.sendmail(GMAIL_USER, GMAIL_USER, msg.as_string())
    server.quit()

# Main function to generate the daily digest
def create_digest():
    print("Starting script...")
    today = datetime.date.today()
    subject = f"Construction Materials Digest - {today}"
    body = f"Here's the latest news on construction materials suppliers:\n\n"

    # Fetch the top 5 news articles
    articles = fetch_headlines()
    print(f"Fetched {len(articles)} articles.")

    # Summarize each article and add to the email body
    for article in articles:
        summary = summarize_article(article)
        body += f"Title: {article['title']}\nSummary: {summary}\nLink: {article['url']}\n\n"

    # Send the email
    send_email(subject, body)
    print("Email sent successfully!")  # Confirmation of email being sent

if __name__ == "__main__":
    create_digest()
