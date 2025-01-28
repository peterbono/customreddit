import requests
import csv

# Configurations Reddit API
CLIENT_ID = "YeScY2wdzpu22LBogcHpeQ"
CLIENT_SECRET = "X74jO9XTcxnbqWzWXCRJn2dYXtEX_Q"
USER_AGENT = "motousers/0.1 (by /u/YourRedditUsername)"
ACCESS_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJsb2lkIiwiZXhwIjoxNzM4MTEyMDY1LjM1MjU2MiwiaWF0IjoxNzM4MDI1NjY1LjM1MjU2MiwianRpIjoia3dueGxSdXp0a1ZBaFZOd21zMjUxQnJ3SFRHQVVBIiwiY2lkIjoiWWVTY1kyd2R6cHUyMkxCb2djSHBlUSIsImxpZCI6InQyXzFpMjFrY25lZXgiLCJsY2EiOjE3MzgwMjU2NjUzNDAsInNjcCI6ImVKeUtWdEpTaWdVRUFBRF9fd056QVNjIiwiZmxvIjo2fQ.DWsmOrGIQAjHfLVGV-kfiq80EggaAqoSbja0rND5u-aUPwKHHvk1OmFgcDUBDLnZMqiStF8Zocjjj8hgVvVkckLRiSahgqe429aDCHI1rdEhWadnh4OCTElHX7wFYVUaJYW-lehQZYTQz99eOYJz3DxiWCB3BEwvNWYLmd8_q7z1WJqtrKoHKmcV8-54Ajq5A-lDytlv_zLkyFbikGQUAhYQkl7UtIXbDjgW1upHCEQJEmD0uXBABQFFTbSLJyujEhN02UsNWs75PItfOK-FNZI3ib3tsS4cjInOZELMVVvc8DlO6Zom-Hjgke-2bqStGpmmpDy6GzxAwjQu54jgFg"

# Configurations des subreddits et mots-clés
subreddits = ["motorcycles", "moto", "france", "AdventureMotorcycles", "AutoMoto"]
keywords = ["location moto", "louer ma moto", "risques location moto", "peur location moto", "freins location moto"]

# Headers pour l'API Reddit
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "User-Agent": USER_AGENT,
}

# Fonction pour rechercher les questions sur Reddit
def search_reddit(query, subreddit):
    url = f"https://oauth.reddit.com/r/{subreddit}/search"
    params = {
        "q": query,
        "restrict_sr": "1",
        "sort": "relevance",
        "limit": 100
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()["data"]["children"]
    else:
        print(f"Erreur pour {query} dans {subreddit} : {response.status_code}")
        return []

# Collecte des questions par mot-clé et subreddit
def collect_questions():
    questions = []
    for subreddit in subreddits:
        for keyword in keywords:
            print(f"Recherche pour : {keyword} dans {subreddit}")
            results = search_reddit(keyword, subreddit=subreddit)
            for post in results:
                data = post["data"]
                title = data.get("title", "")
                score = data.get("score", 0)
                num_comments = data.get("num_comments", 0)
                link = f"https://www.reddit.com{data.get('permalink', '')}"
                questions.append({
                    "title": title,
                    "score": score,
                    "num_comments": num_comments,
                    "link": link
                })
    return questions

# Exporter les questions vers un fichier CSV
def export_questions_to_csv(questions):
    with open("questions_location_moto.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Titre", "Score", "Nombre de commentaires", "Lien"])
        for question in questions:
            writer.writerow([question["title"], question["score"], question["num_comments"], question["link"]])
    print("Questions exportées vers questions_location_moto.csv")

# Afficher les questions les plus populaires
def display_top_questions(questions, top_n=10):
    sorted_questions = sorted(questions, key=lambda x: x["score"], reverse=True)[:top_n]
    print("\nQuestions les plus populaires :")
    for i, question in enumerate(sorted_questions, start=1):
        print(f"{i}. {question['title']} (Score: {question['score']}, Commentaires: {question['num_comments']})")
        print(f"Lien : {question['link']}\n")

if __name__ == "__main__":
    # Collecte des questions
    questions = collect_questions()

    # Exportation des questions
    export_questions_to_csv(questions)

    # Affichage des questions les plus populaires
    display_top_questions(questions)