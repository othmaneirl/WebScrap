# Ce script permet de récupérer les liens des annonces Airbnb à partir d'une liste de liens de recherche
import pandas as pd
def generate_airbnb_urls(cities_neighborhoods):
    base_url = "https://www.airbnb.com/s/{neighborhood}-{city}-Morocco/homes"
    urls = []

    for city, neighborhoods in cities_neighborhoods.items():
        for neighborhood in neighborhoods:
            url = base_url.format(neighborhood=neighborhood, city=city)
            urls.append([url,neighborhood,city])

    return urls

# Dictionnaire prérempli avec les villes et quartiers
# cities_neighborhoods = {
#     "Casablanca": ["Ain-Diab", "Maarif", "Anfa", "Sidi-Belyout", "Bourgogne", "Gauthier", "Derb-Ghallef", "Oasis"],
#     "Marrakech": ["Gueliz", "Medina", "Hivernage", "Agdal", "Palmeraie", "Kasbah", "Targa", "Sidi-Mimoun"],
#     "Fes": ["Fes-El-Bali", "Fes-Jdid", "Nouvelle-Ville", "Ziat", "Bab-Bou-Jeloud", "Mellah", "Sidi-Boujida", "Ain-Kadous"],
#     "Rabat": ["Agdal", "Hay-Riad", "Medina", "Hassan", "Souissi", "Yacoub-El-Mansour", "Ocean", "Akkari"],
#     "Tangier": ["Malabata", "Iberia", "Marshan", "Medina", "Boukhalef", "Charf", "California", "Tangier-Port"],
#     "Agadir": ["Talborjt", "Founty", "Dakhla", "Agadir-Oufella", "Ben-Sergao", "El-Houda", "Anza", "Hay-Mohammadi"],
#     "Essaouira": ["Medina", "Diabat", "Essaouira-Ouest", "El-Ghazoua", "Azlef", "Boukhris", "Dunes", "Lotissement"],
#     "Chefchaouen": ["Medina", "El-Kharrazine", "Souika", "Hassan-1", "Sebbanine", "Rif-Al-Andalous", "Moulay-Ali-Ben-Rachid", "Bab-El-Mahruk"],
#     "Meknes": ["Hamria", "Ville-Nouvelle", "Medina", "El-Bassatine", "Al-Ismailia", "Marjane", "Sidi-Bouzekri", "Zitoune"],
#     "Oujda": ["Quartier-Industriel", "Medina", "Quartier-Sud", "Ville-Nouvelle", "Al-Qods", "El-Ouafa", "Hay-Riyad", "Hay-El-Baraka"],
#     "Tetouan": ["Medina", "Mellah", "Centre-Ville", "Oued-Laou", "Martil", "Jbel-Dersa", "Mhannech", "Ain-Mskour"],
#     "El Jadida": ["Sidi-Bouzid", "Medina", "Haouzia", "Zerzate", "Mellah", "Bir-Anzarane", "Lalla-Meria", "Hay-El-Matar"],
#     "Kenitra": ["Mehdia", "Bir-Rami", "Ville-Haute", "Oulad-Oujih", "Quartier-Industriel", "Maamora", "Haddada", "Ain-Sebaa"],
#     "Nador": ["Al-Matar", "Hayon-Fath", "Quartier-Dyar-Beni-Yer", "El-Aroui", "Medina", "Kariat-Arkmane", "Segangan", "Bouarg"],
#     "Laayoune": ["Maatallah", "El-Marsa", "Quartier-Laayoune", "Colline", "El-Wahda", "Moulay-Rachid", "Ras-El-Khaimah", "Hay-El-Massira"]
# }

cities_neighborhoods = {
    "Casablanca": ["Ain-Diab", "Maarif", "Anfa"],
    "Marrakech": ["Gueliz", "Medina", "Hivernage"],
    "Fes": ["Fes-El-Bali", "Fes-Jdid", "Nouvelle-Ville"],
    "Rabat": ["Agdal", "Hay-Riad", "Medina"],
    "Tangier": ["Malabata", "Iberia", "Marshan"],
    "Agadir": ["Talborjt", "Founty", "Dakhla"],
    "Essaouira": ["Medina", "Diabat", "Essaouira-Ouest"],
    "Chefchaouen": ["Medina", "El-Kharrazine", "Souika"],
    "Meknes": ["Hamria", "Ville-Nouvelle", "Medina"],
    "Oujda": ["Quartier-Industriel", "Medina", "Quartier-Sud"],
    "Tetouan": ["Medina", "Mellah", "Centre-Ville"],
    "El Jadida": ["Sidi-Bouzid", "Medina", "Haouzia"],
    "Kenitra": ["Mehdia", "Bir-Rami", "Ville-Haute"],
    "Nador": ["Al-Matar", "Hayon-Fath", "Quartier-Dyar-Beni-Yer"],
    "Laayoune": ["Maatallah", "El-Marsa", "Quartier-Laayoune"]
}


urls = generate_airbnb_urls(cities_neighborhoods)
urls = pd.DataFrame(urls, columns=['URL','Quartier','Ville'])
urls.to_csv('Liens/test.csv', index=False)
