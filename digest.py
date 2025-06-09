import requests
import openai
from config import NEWS_API_KEY, OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def fetch_headlines():
    url = f"https://newsapi.org/v2/everything?q=construction materials supplier&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('articles', [])[:5]
    except Exception as e:
        print(f"❌ Failed to fetch articles: {e}")
        return []

def summarize_article(article):
    prompt = f"Summarize this article for a construction industry newsletter:\nTitle: {article['title']}\nDescription: {article['description']}\nURL: {article['url']}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Failed to summarize article: {e}")
        return "Summary unavailable."

def fetch_and_summarize_articles():
    articles = fetch_headlines()
    summaries = []
    for article in articles:
        summary = summarize_article(article)
        summaries.append({
            "title": article["title"],
            "summary": summary,
            "url": article["url"]
        })
    return summaries
