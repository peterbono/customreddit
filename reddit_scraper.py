import requests
import csv

# Configurations Reddit API
CLIENT_ID = "YeScY2wdzpu22LBogcHpeQ"
CLIENT_SECRET = "X74jO9XTcxnbqWzWXCRJn2dYXtEX_Q"
USER_AGENT = "motousers/0.1 (by /u/YourRedditUsername)"
ACCESS_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJsb2lkIiwiZXhwIjoxNzM4MTEyMDY1LjM1MjU2MiwiaWF0IjoxNzM4MDI1NjY1LjM1MjU2MiwianRpIjoia3dueGxSdXp0a1ZBaFZOd21zMjUxQnJ3SFRHQVVBIiwiY2lkIjoiWWVTY1kyd2R6cHUyMkxCb2djSHBlUSIsImxpZCI6InQyXzFpMjFrY25lZXgiLCJsY2EiOjE3MzgwMjU2NjUzNDAsInNjcCI6ImVKeUtWdEpTaWdVRUFBRF9fd056QVNjIiwiZmxvIjo2fQ.DWsmOrGIQAjHfLVGV-kfiq80EggaAqoSbja0rND5u-aUPwKHHvk1OmFgcDUBDLnZMqiStF8Zocjjj8hgVvVkckLRiSahgqe429aDCHI1rdEhWadnh4OCTElHX7wFYVUaJYW-lehQZYTQz99eOYJz3DxiWCB3BEwvNWYLmd8_q7z1WJqtrKoHKmcV8-54Ajq5A-lDytlv_zLkyFbikGQUAhYQkl7UtIXbDjgW1upHCEQJEmD0uXBABQFFTbSLJyujEhN02UsNWs75PItfOK-FNZI3ib3tsS4cjInOZELMVVvc8DlO6Zom-Hjgke-2bqStGpmmpDy6GzxAwjQu54jgFg"

# Configurations des régions et subreddits
regions = [
    "\u00cele-de-France", "Provence-Alpes-Côte d'Azur", "Auvergne-Rhône-Alpes",
    "Hauts-de-France", "Grand Est", "Occitanie", "Nouvelle-Aquitaine",
    "Bretagne", "Normandie", "Bourgogne-Franche-Comté", "Centre-Val de Loire",
    "Pays de la Loire", "Corse"
]
keywords = ["moto", "motard", "balade", "rassemblement", "tourisme"]
subreddits = ["motorcycles", "moto", "france", "AdventureMotorcycles", "AutoMoto"]

# Headers pour l'API Reddit
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "User-Agent": USER_AGENT,
}

# Fonction pour rechercher sur Reddit via l'API officielle
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

# Collecte des données par région
def collect_data():
    data = {}
    for region in regions:
        print(f"Recherche pour la région : {region}")
        total_results = 0

        # Recherche dans les subreddits
        for subreddit in subreddits:
            for keyword in keywords:
                query = f"{keyword} {region}"
                results = search_reddit(query, subreddit=subreddit)
                total_results += len(results)

        data[region] = total_results
        print(f"{region} : {total_results} résultats trouvés")
    return data

# Exporter les données vers un fichier CSV
def export_to_csv(data):
    with open("motards_par_region.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Région", "Nombre de posts"])
        for region, count in data.items():
            writer.writerow([region, count])
    print("Données exportées vers motards_par_region.csv")

if __name__ == "__main__":
    # Collecte des données
    data = collect_data()

    # Exportation des données
    export_to_csv(data)

    # Affichage des résultats
    print("\nRésumé des données :")
    for region, count in data.items():
        print(f"{region} : {count} posts trouvés")
