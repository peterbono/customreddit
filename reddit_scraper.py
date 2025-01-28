import requests

# Configurations Reddit API
ACCESS_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJsb2lkIiwiZXhwIjoxNzM4MTEyMDY1LjM1MjU2MiwiaWF0IjoxNzM4MDI1NjY1LjM1MjU2MiwianRpIjoia3dueGxSdXp0a1ZBaFZOd21zMjUxQnJ3SFRHQVVBIiwiY2lkIjoiWWVTY1kyd2R6cHUyMkxCb2djSHBlUSIsImxpZCI6InQyXzFpMjFrY25lZXgiLCJsY2EiOjE3MzgwMjU2NjUzNDAsInNjcCI6ImVKeUtWdEpTaWdVRUFBRF9fd056QVNjIiwiZmxvIjo2fQ.DWsmOrGIQAjHfLVGV-kfiq80EggaAqoSbja0rND5u-aUPwKHHvk1OmFgcDUBDLnZMqiStF8Zocjjj8hgVvVkckLRiSahgqe429aDCHI1rdEhWadnh4OCTElHX7wFYVUaJYW-lehQZYTQz99eOYJz3DxiWCB3BEwvNWYLmd8_q7z1WJqtrKoHKmcV8-54Ajq5A-lDytlv_zLkyFbikGQUAhYQkl7UtIXbDjgW1upHCEQJEmD0uXBABQFFTbSLJyujEhN02UsNWs75PItfOK-FNZI3ib3tsS4cjInOZELMVVvc8DlO6Zom-Hjgke-2bqStGpmmpDy6GzxAwjQu54jgFg"

USER_AGENT = "motousers/0.1 (by /u/YourRedditUsername)"


def search_reddit(query, subreddit="motorcycles"):
    url = f"https://oauth.reddit.com/r/{subreddit}/search"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "User-Agent": USER_AGENT,
    }
    params = {
        "q": query,        # Mot-clé de recherche
        "restrict_sr": "1", # Limiter au subreddit spécifié
        "sort": "relevance",
    }

    # Effectuer la recherche
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()["data"]["children"]
    else:
        print(f"Erreur lors de la recherche Reddit : {response.status_code}")
        print(f"Message retourné par Reddit : {response.text}")
        raise Exception(f"Failed to search Reddit: {response.status_code} - {response.text}")


if __name__ == "__main__":
    query = "Paris"
    try:
        results = search_reddit(query)
        print(f"Résultats trouvés : {len(results)}")
        for post in results:
            data = post["data"]
            print(f"- {data['title']} (Score : {data['score']}, Commentaires : {data['num_comments']})")
    except Exception as e:
        print(f"Erreur : {e}")