import os
from collections import defaultdict
from openpyxl import Workbook
import matplotlib.pyplot as plt
import numpy as np


def analyse_mot(mot):
    TACHKIL = ['َ', 'ً', 'ُ', 'ٌ', 'ِ', 'ٍ', 'ْ', 'ّ', 'ٰ']
    LETTERS = u'ابتةثجحخدذرزسشصضطظعغفقكلمنهويءآأؤإئ'

    lettres = []
    tachkils = []
    paires = []

    i = 0
    while i < len(mot):
        if mot[i] in LETTERS:
            lettres.append(mot[i])

            if i + 1 < len(mot) and mot[i + 1] == 'ّ':
                if i + 2 < len(mot) and mot[i + 2] in TACHKIL:
                    paires.append(mot[i] + 'ْ')
                    tachkils.append('ْ')
                    paires.append(mot[i] + mot[i + 2])
                    tachkils.append(mot[i + 2])
                    i += 3
                else:
                    paires.append(mot[i] + 'ْ')
                    tachkils.append('ْ')
                    paires.append(mot[i] + 'َ')
                    tachkils.append('َ')
                    i += 2
            elif i + 1 < len(mot) and mot[i + 1] in TACHKIL:
                paires.append(mot[i] + mot[i + 1])
                tachkils.append(mot[i + 1])
                i += 2
            else:
                paires.append(mot[i])
                tachkils.append('')
                i += 1
        else:
            i += 1

    paires = ['DEBUT'] + paires + ['FIN']
    tachkils = ['DEBUT'] + tachkils + ['FIN']

    return {
        "lettres": lettres,
        "tachkil": tachkils,
        "paires": paires
    }


def calculer_matrice_transition(mots_analyses):
    transitions = defaultdict(lambda: defaultdict(int))
    etats_counts = defaultdict(int)

    # Collecter tous les états possibles
    tous_etats = set()
    for mot_info in mots_analyses:
        paires = mot_info["paires"]
        for paire in paires:
            tous_etats.add(paire)

    # Initialiser la matrice avec tous les états
    proba = {etat: defaultdict(float) for etat in tous_etats}

    for mot_info in mots_analyses:
        paires = mot_info["paires"]
        for i in range(len(paires) - 1):
            etat_actuel = paires[i]
            etat_suivant = paires[i + 1]
            transitions[etat_actuel][etat_suivant] += 1
            etats_counts[etat_actuel] += 1

    # Calculer les probabilités
    for etat_actuel in transitions:
        total = etats_counts[etat_actuel]
        for etat_suivant, count in transitions[etat_actuel].items():
            proba[etat_actuel][etat_suivant] = count / total

    nombre_de_cas = sum(etats_counts.values())
    return proba, list(tous_etats), nombre_de_cas


def calculer_matrice_stabilite(matrice_transition, etats, tolerance=1e-10, max_iterations=1000):
    taille = len(etats)

    # Convertir en matrice numpy
    matrice = np.zeros((taille, taille))
    etat_index = {etat: idx for idx, etat in enumerate(etats)}

    for etat_actuel in matrice_transition:
        for etat_suivant, proba in matrice_transition[etat_actuel].items():
            i = etat_index[etat_actuel]
            j = etat_index[etat_suivant]
            matrice[i, j] = proba

    # Itérer jusqu'à convergence
    matrice_precedente = matrice.copy()
    for iteration in range(max_iterations):
        matrice_nouvelle = np.dot(matrice_precedente, matrice)

        difference = np.abs(matrice_nouvelle - matrice_precedente).max()
        if difference < tolerance:
            print(f"Convergence atteinte après {iteration + 1} itérations")
            break

        matrice_precedente = matrice_nouvelle.copy()
    else:
        print(f"Attention: La convergence n'a pas été atteinte après {max_iterations} itérations")

    # Convertir le résultat en dictionnaire
    matrice_stabilite = defaultdict(lambda: defaultdict(float))
    for i, etat in enumerate(etats):
        for j, etat_suivant in enumerate(etats):
            matrice_stabilite[etat][etat_suivant] = matrice_nouvelle[i, j]

    return matrice_stabilite


def sauvegarder_combi_txt(mots_analyses, chemin_combin):
    with open(chemin_combin, mode='w', encoding='utf-8') as file:
        for mot_info in mots_analyses:
            lettres = mot_info["lettres"]
            tachkils = mot_info["tachkil"][::-1]
            paires = mot_info["paires"]

            file.write(f"Mot: {''.join(lettres)}\n")
            file.write(f"  Lettres: {lettres}\n")
            file.write(f"  Tachkil: {tachkils}\n")
            file.write("  Paires successives:\n")

            for i in range(len(paires) - 1):
                if i == 0:
                    file.write(f"    Debut de mot -> {paires[i + 1]}\n")
                elif i == len(paires) - 2:
                    file.write(f"    {paires[i]} -> Fin de mot\n")
                else:
                    file.write(f"    {paires[i]} -> {paires[i + 1]}\n")

            file.write("\n")


def sauvegarder_matrice_excel(matrice, etats, chemin_excel):
    wb = Workbook()
    ws = wb.active
    ws.title = "Matrice de Transition"

    # En-tête
    ws.append([''] + etats)

    # Données
    for etat_actuel in etats:
        row = [etat_actuel]
        for etat_suivant in etats:
            valeur = matrice[etat_actuel][etat_suivant]
            row.append(valeur)
        ws.append(row)

    wb.save(chemin_excel)


def generer_matrice_image(matrice, etats, chemin_image, titre="Matrice de Transition"):
    taille = len(etats)
    matrice_numpy = np.zeros((taille, taille))

    for i, etat_actuel in enumerate(etats):
        for j, etat_suivant in enumerate(etats):
            matrice_numpy[i, j] = matrice[etat_actuel][etat_suivant]

    plt.figure(figsize=(12, 10))
    plt.imshow(matrice_numpy, interpolation='nearest', cmap='Blues', aspect='auto')
    plt.colorbar(label="Probabilités de transition")

    for i in range(taille):
        for j in range(taille):
            value = matrice_numpy[i, j]
            if value > 0:
                plt.text(j, i, f"{value:.4f}", ha='center', va='center',
                         color='black' if value < 0.5 else 'white', fontsize=8)

    plt.xticks(ticks=range(taille), labels=etats, rotation=45, ha='right', fontsize=10)
    plt.yticks(ticks=range(taille), labels=etats, fontsize=10)

    plt.title(titre, fontsize=14)
    plt.xlabel("État Suivant", fontsize=12)
    plt.ylabel("État Actuel", fontsize=12)

    plt.tight_layout()
    plt.savefig(chemin_image, dpi=300)
    plt.close()


def sauvegarder_proba_txt(proba, nombre_de_cas, chemin_proba):
    with open(chemin_proba, mode='w', encoding='utf-8') as file:
        file.write("Probabilités de transition des paires successives:\n")

        somme_probabilites = 0
        for etat_actuel, transitions_suivantes in proba.items():
            for etat_suivant, proba_value in transitions_suivantes.items():
                file.write(f"  {etat_actuel} -> {etat_suivant}: {proba_value:.4f}\n")
                somme_probabilites += proba_value
        nombre_de_cas=272
        proba_totale = somme_probabilites / nombre_de_cas
        file.write(f"\nSomme totale des probabilités de transition: {somme_probabilites:.4f}\n")
        file.write(f"Proba totale = {somme_probabilites} / {nombre_de_cas} = {proba_totale:.4f}\n")


def main():
    chemin_donnees = r"C:\Users\Dr.Ayat\Desktop\mlaim\proba\projet_arabe\Data_Arab_Tashkeel"
    print("Lecture des fichiers en cours...")

    texte = ""
    for fichier in os.listdir(chemin_donnees):
        if fichier.endswith('.txt'):
            with open(os.path.join(chemin_donnees, fichier), 'r', encoding='utf-8') as f:
                texte += f.read() + " "

    mots = texte.split()
    mots_analyses = [analyse_mot(mot) for mot in mots if mot.strip()]

    # Calculer la matrice de transition initiale (P)
    matrice_transition, etats, nombre_de_cas = calculer_matrice_transition(mots_analyses)

    # Calculer la matrice de stabilité
    matrice_stabilite = calculer_matrice_stabilite(matrice_transition, etats)

    # Créer le dossier de sortie
    dossier_sortie = os.path.join(chemin_donnees, "resultats")
    os.makedirs(dossier_sortie, exist_ok=True)

    # Définir les chemins des fichiers de sortie
    chemin_combin = os.path.join(dossier_sortie, 'combinee2025.txt')
    chemin_matrice = os.path.join(dossier_sortie, 'matrice_transition2025.xlsx')
    chemin_proba = os.path.join(dossier_sortie, 'proba2025.txt')
    chemin_image_transition = os.path.join(dossier_sortie, 'matrice_transition2025.png')
    chemin_image_stabilite = os.path.join(dossier_sortie, 'matrice_stabilite2025.png')
    chemin_matrice_stabilite = os.path.join(dossier_sortie, 'matrice_stabilite2025.xlsx')

    # Sauvegarder tous les résultats
    print("Sauvegarde des résultats...")
    sauvegarder_combi_txt(mots_analyses, chemin_combin)
    sauvegarder_matrice_excel(matrice_transition, etats, chemin_matrice)
    sauvegarder_matrice_excel(matrice_stabilite, etats, chemin_matrice_stabilite)
    generer_matrice_image(matrice_transition, etats, chemin_image_transition, "Matrice de Transition (P)")
    generer_matrice_image(matrice_stabilite, etats, chemin_image_stabilite, "Matrice de Stabilité")
    sauvegarder_proba_txt(matrice_transition, nombre_de_cas, chemin_proba)

    print(f"\nNombre total de mots traités : {len(mots_analyses)}")
    print(f"Résultats détaillés sauvegardés dans : {chemin_combin}")
    print(f"Matrice de transition sauvegardée dans : {chemin_matrice}")
    print(f"Matrice de stabilité sauvegardée dans : {chemin_matrice_stabilite}")
    print(f"Images des matrices sauvegardées dans : {chemin_image_transition} et {chemin_image_stabilite}")
    print(f"Fichier des probabilités sauvegardé dans : {chemin_proba}")


if __name__ == "__main__":
    main()


