import os
import feedparser
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")

RSS_FEEDS = [
    "https://www.reuters.com/rss/technologyNews",
    "https://www.technologyreview.com/feed/",
    "https://feeds.arstechnica.com/arstechnica/index",
    "https://www.wired.com/feed/rss",
    "https://www.theregister.com/headlines.atom"
]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def process_rss():
    for feed_url in RSS_FEEDS:
        print(f"Fetching: {feed_url}")
        feed = feedparser.parse(feed_url)

        if not feed.entries:
            print(f"No entries found: {feed_url}")
            continue

        for entry in feed.entries:
            existing = supabase.table("articles").select("id").eq("url", entry.link).execute()
            
            if not existing.data:
                data = {
                    "title": entry.title,
                    "url": entry.link,
                    "content": entry.get("summary", entry.get("description", "")),
                    "published_at": entry.get("published", entry.get("updated", "")),
                    "source": feed.feed.get("title", "Unknown")
                }
                try:
                    supabase.table("articles").insert(data).execute()
                    print(f"Inserted: {entry.title}")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print(f"Skipped: {entry.title}")

if __name__ == "__main__":
    process_rss()
