import requests
import os
from dotenv import load_dotenv

load_dotenv()

def parse_views(view_str):
    if not view_str:
        return 0
    view_str = str(view_str).lower().replace(' views', '').replace(',', '')
    if 'k' in view_str:
        return int(float(view_str.replace('k', '')) * 1_000)
    if 'm' in view_str:
        return int(float(view_str.replace('m', '')) * 1_000_000)
    if 'b' in view_str:
        return int(float(view_str.replace('b', '')) * 1_000_000_000)
    try:
        return int(view_str)
    except ValueError:
        return 0

def get_top3_youtube_links(topic):
    api_key = os.environ.get("serp_api")
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "q": f"site:youtube.com {topic}"
    }
    url = "https://google.serper.dev/search"

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        results = response.json()
        organic = results.get("organic", [])

        top3 = []
        for item in organic:
            link = item.get("link")
            title = item.get("title")
            if "youtube.com/watch" in link:
                top3.append({"title": title, "link": link})
            if len(top3) == 3:
                break

        return top3

    except requests.Timeout:
        print("Request timed out.")
        return []
    except Exception as e:
        print(f"Error searching for '{topic}': {e}")
        return []
