import os
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from io import StringIO

url = "https://fr.wikipedia.org/w/index.php?title=Championnat_de_France_de_football_2016-2017&oldid=219399721"

# Récupération du HTML
response = requests.get(url)
response.encoding = response.apparent_encoding

if response.status_code == 200: #all good
    soup = BeautifulSoup(response.text, "html.parser")

    # Création du dossier de sauvegarde (Data) s'il n'existe pas
    output_dir = "C:/Users/pc/Desktop/Projet1/TD1/Data"
    os.makedirs(output_dir, exist_ok=True)

    # 1.Trouver le tableau "Participants" qui a la classe "DebutCarte"
    tableequipe = soup.find('table', {'class': 'DebutCarte'})
    participants = []
    if tableequipe:
         # On parcourt toutes les lignes du tableau
        rows = tableequipe.find_all('tr')
        for row in rows:
            colonnes = row.find_all('td')
            if colonnes:
                #nom de l'équipe se trouve dans la première colonne
                team_name = colonnes[0].get_text(strip=True)
                if team_name:
                    participants.append(team_name)
    else:
        print("Tableau 'Participants' non trouvé.")

        # # Afficher les résultats
        # print("Liste des équipes (Participants) :")
        # print(participants)
    if participants:
        df1 = pd.DataFrame(participants, columns=['Equipe'])
        print(df1.head(10))
        df1.to_csv(os.path.join(output_dir, 'participants.csv'), index=False, encoding="utf-8")
    else:
        print("Aucune équipe trouvée.")

    # Question 5
sections = {
        "Changements_d'entraîneur": "changements_entraineur.csv",
        "Compétition": "competition.csv",
        "Matchs": "matchs.csv",
        "Domicile_et_extérieur": "domicile_exterieur.csv",
        "Évolution_du_classement": "evolution_classement.csv",
        "Classement_des_buteurs": "classement_buteurs.csv",
        "Classement_des_passeurs": "classement_passeurs.csv",
        "Plus_grosses_affluences_de_la_saison": "affluences.csv"
    }

for section_id, csv_filename in sections.items():
        # Recherche de la balise <h3> ayant l'attribut id égal à la valeur fournie
        headline = soup.find("h3", id=section_id)
        if headline:
            header_tag = headline.parent
            # On cherche le premier tableau qui suit immédiatement ce h3
            table = header_tag.find_next("table", class_="wikitable")
            if table:
                try:
                    df_section = pd.read_html(StringIO(str(table)))[0]
                    print(f"\nSection : {section_id}")
                    print(df_section.head())
                    df_section.to_csv(os.path.join(output_dir, csv_filename), index=False, encoding="utf-8-sig")
                except Exception as e:
                    print(f"Erreur lors du parsing du tableau pour la section '{section_id}' : {e}")
            else:
                print(f"Aucun tableau trouvé pour la section '{section_id}'.")
        else:
            print(f"La section '{section_id}' n'a pas été trouvée dans la page.")
else:
    print("Erreur lors de la requête HTTP. Code :", response.status_code)