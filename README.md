# 📚 Analyse des Transitions en Langue Arabe avec Chaînes de Markov

> Projet de Master MLAIM (2024-2025)  
> Auteur : Ayat BOUHRIR  
> Encadrant : Pr. Hassan SATORI  
> Université Sidi Mohamed Ben Abdellah, Faculté des Sciences Dhar El Mehraz – Fès

---

## 🎯 Objectif du Projet

Ce projet a pour objectif de modéliser les relations entre les **lettres arabes** et leurs **diacritiques (Tachkils)** à l’aide des **chaînes de Markov**, en vue d'applications telles que :
- La génération automatique de texte vocalisé.
- La reconnaissance optique de caractères (OCR).
- L'analyse linguistique probabiliste.

---

## 🧪 Méthodologie

### 🗃️ 1. Constitution de la base de données
- **100 000 phrases en arabe vocalisé** (avec Tachkils).
- Collectées par un groupe de **13 contributeurs**.
- Fichier source : `Data_Arab_Taskeel.txt`.

### ✂️ 2. Prétraitement
- Découpage en mots.
- Extraction des **paires (lettre, tachkil)**.
- Stockage des transitions.

### 🔁 3. Modélisation par chaînes de Markov
- Création d’un **espace d’états** constitué des paires (lettre, tachkil).
- Calcul des **probabilités de transition** entre les états.
- Construction :
  - D'une **matrice de transition**.
  - D'une **matrice stochastique**.
  - D'une **matrice de stabilité d'ordre 2** (Markov d'ordre 2).

---

## 💡 Concepts Clés

- **Chaîne de Markov** : modèle où chaque état dépend uniquement de l’état précédent.
- **Matrice de transition** : matrice des probabilités de passer d’un état à un autre.
- **Stabilité d’ordre 2** : prend en compte deux états précédents pour prédire le suivant.

---

## 🛠️ Technologies & Librairies

- **Python 3**
- `matplotlib`, `numpy` — visualisation et calcul matriciel
- `openpyxl` — génération de fichiers Excel
- `collections.defaultdict`, `os` — gestion des données

---

## 📁 Structure du Code

| Fichier / Fonction                        | Description |
|------------------------------------------|-------------|
| `analyse_mot(mot)`                       | Analyse un mot en lettres + tachkils |
| `calculer_matrice_transition()`          | Crée la matrice de transition |
| `sauvegarder_matrice_excel()`            | Export Excel de la matrice |
| `sauvegarder_combi_txt()`                | Sauvegarde des paires lettres-diacritiques |
| `sauvegarder_proba_txt()`                | Export des probabilités de transition |

---

## 📊 Résultats Attendus

- **Visualisation Heatmap** des transitions (intensité selon la probabilité).
- **Matrice de transition** lisible et exportée en Excel.
- Analyse de la **densité de transitions fréquentes** (régions sombres/claires).
- **Probabilités faibles** (~10⁻¹⁰) indiquant la rareté de certaines transitions.

---

## ✅ Conclusion

Ce projet propose une solution robuste et adaptable pour :
- Modéliser les transitions linguistiques dans la langue arabe.
- Appliquer des techniques statistiques (Markov) au TAL.
- Poser les bases de futurs travaux sur la vocalisation, l’OCR ou la correction automatique.

---

## 📚 Références

1. Rabiner, L. R. (1989) — *A Tutorial on Hidden Markov Models*  
2. Jurafsky & Martin (2009) — *Speech and Language Processing*  
3. Habash, N. Y. (2010) — *Introduction to Arabic NLP*  
4. Manning & Schütze (1999) — *Foundations of Statistical NLP*  
5. [Kaggle: Tashkeela Dataset](https://www.kaggle.com/datasets/hamzaabbad/tashkeela-processed-fully-diacritized-arabic-text/data)

