# Ticketing-App

Application web de gestion de tickets IT développée en Python avec Flask.

## Contexte
Projet réalisé dans le cadre de ma formation Bachelor DSNS (Cybersécurité) à l'ESIEE-IT.  
Objectif : simuler un outil de ticketing type GLPI pour le support N1/N2.

## Stack technique
- Python 3.14
- Flask 3.1
- HTML/CSS (interface dark mode)

## Fonctionnalités
- Création de tickets (titre, demandeur, catégorie, priorité, description)
- Dashboard avec compteurs en temps réel (total, ouverts, en cours, fermés)
- Gestion du cycle de vie : Ouvert → En cours → Fermé
- Badges de priorité colorés (Haute / Moyenne / Basse)
- Interface responsive dark mode

## Lancer l'application
```bash
pip install flask
python app.py
```
Puis ouvrir `http://localhost:5000`

## Aperçu
![Dashboard ticketing](screenshot.png)

## Auteur
Lucas Bigot — [ESIEE-IT](https://www.esiee-it.fr) | Bachelor DSNS Cybersécurité
