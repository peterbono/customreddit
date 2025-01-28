import requests

# Configuration API Reddit
ACCESS_TOKEN = "VOTRE_ACCESS_TOKEN"
USER_AGENT = "motousers/0.1 (by /u/YourRedditUsername)"

# Liste des régions françaises
regions = [
    "Île-de-France", "Provence-Alpes-Côte d'Azur", "Auvergne-Rhône-Alpes", 
    "Hauts-de-France", "Grand Est", "Occitanie", "Nouvelle-Aquitaine", 
    "Bretagne", "Normandie", "Bourgogne-Franche-Comté", "Centre-Val de Loire", 
    "Pays de la Loire", "Corse"
]

def search_reddit(query, subreddit="motorcycles"):
    url = f"https://oauth.reddit.com/r/{subreddit}/search"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "User-Agent": USER_AGENT,
    }
    params = {
        "q": query,         # Mot-clé de recherche
        "restrict_sr": "1", # Limiter au subreddit spécifié
        "sort": "relevance"
    }

    # Effectuer la requête
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()["data"]["children"]
    else:
        print(f"Erreur lors de la recherche Reddit : {response.status_code}")
        print(f"Message retourné par Reddit : {response.text}")
        raise Exception(f"Failed to search Reddit: {response.status_code} - {response.text}")

def collect_motard_data():
    region_data = {}
    for region in regions:
        print(f"Recherche pour la région : {region}")
        results = search_reddit(region)
        region_data[region] = len(results)
        print(f"Résultats pour {region} : {len(results)} posts trouvés")
    return region_data

if __name__ == "__main__":
    data = collect_motard_data()
    print("\nRésumé des données :")
    for region, count in data.items():
        print(f"{region} : {count} posts trouvés")