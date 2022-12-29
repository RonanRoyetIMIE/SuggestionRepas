from django.shortcuts import render

import requests

url = "https://world.openfoodfacts.org/?json=true"

reponse = requests.get(url)
print("Récupération des données de l'API:")
print(reponse)
contenu = reponse.json()
print(contenu)

def index(request):
    return render(request, "repas/index.html")