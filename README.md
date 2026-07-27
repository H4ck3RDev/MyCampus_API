# MyCampus API

API REST pour la gestion d'un système universitaire (campus), implémentée en Python avec Flask.

## Fonctionnalités principales

- Authentification JWT
- Gestion des utilisateurs, rôles, étudiants, professeurs
- Gestion des années académiques, facultés, départements, promotions
- Gestion des cours, affectations de professeurs et inscriptions
- Gestion des notes, messages, notifications et présences
- Point d'entrée de vérification de connexion à la base de données

## Installation

1. Cloner le dépôt ou télécharger le projet.
2. Créer un environnement virtuel Python dans le dossier du projet :

```bash
python -m venv .venv
```

3. Activer l'environnement virtuel :

- Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

- Windows CMD :

```cmd
.venv\Scripts\activate.bat
```

4. Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Configuration

Le projet utilise un fichier `.env` pour charger les paramètres suivants :

```text
SECRET_KEY=une_cle_secrete
JWT_SECRET_KEY=une_cle_secrete_jwt
DB_USER=utilisateur_mysql
DB_PASSWORD=mot_de_passe_mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=nom_de_la_base
```

> Ne commitez jamais votre fichier `.env` dans le dépôt.

## Exécution

Lancer l'application Flask :

```bash
python app.py
```

L'API démarrera en local sur `http://127.0.0.1:5000`.

## Endpoints de base

- `GET /` : Accueil de l'API
- `GET /test-db` : Vérifie la connexion à la base MySQL

## Endpoints supplémentaires implémentés

- `GET /notes/` : Liste des notes
- `GET /notes/<id>` : Détail d'une note
- `POST /notes/` : Créer une note
- `PUT /notes/<id>` : Mettre à jour une note
- `DELETE /notes/<id>` : Supprimer une note

- `GET /messages/` : Liste des messages
- `GET /messages/<id>` : Détail d'un message
- `POST /messages/` : Envoyer un message
- `PUT /messages/<id>` : Mettre à jour un message
- `DELETE /messages/<id>` : Supprimer un message

- `GET /notifications/` : Liste des notifications
- `GET /notifications/<id>` : Détail d'une notification
- `POST /notifications/` : Créer une notification
- `PUT /notifications/<id>` : Mettre à jour une notification
- `DELETE /notifications/<id>` : Supprimer une notification

- `GET /presences/` : Liste des présences
- `GET /presences/<id>` : Détail d'une présence
- `POST /presences/` : Enregistrer une présence
- `PUT /presences/<id>` : Mettre à jour une présence
- `DELETE /presences/<id>` : Supprimer une présence

- `GET /documents/` : Liste des documents
- `GET /documents/<id>` : Détail d'un document
- `POST /documents/` : Créer un document
- `PUT /documents/<id>` : Mettre à jour un document
- `DELETE /documents/<id>` : Supprimer un document

## Notes

- Le projet est conçu pour une base de données MySQL via SQLAlchemy et PyMySQL.
- Les routes sont organisées dans le dossier `routes/`.
- Les modèles SQLAlchemy sont définis dans le dossier `models/`.

## GitHub

Le dépôt est déjà lié à :

`https://github.com/H4ck3RDev/MyCampus_API`
