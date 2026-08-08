Exercice Django — API REST Patients & Médicaments (+ Prescription à implémenter)

Présentation
------------
Base de projet Django + Django REST Framework pour lister des Patients et des Médicaments.

But de l'exercice candidat: ajouter une nouvelle ressource « Prescription » avec une API REST (lecture + création + mise
à jour) et des possibilités de filtrage.


Installation des Prérequis
---------
Le projet utilise Python 3.10 et Django 4.0.
Avant tout, vous devez vous placer dans le répertoire `Exercice_Django`.

### Python et pip

- **Vérifier l'installation:**

```bash
python3 --version
pip3 --version
```

### Installation de Python et pip

**Sur Ubuntu/Debian:**

```bash
sudo apt update 
sudo apt install python3 python3-pip python3-venv
```

Installation
------------

1) Créer un environnement virtuel et installer les dépendances

```bash
python3 -m venv .venv
````

```bash
source .venv/bin/activate  #(Windows: .venv\\Scripts\\activate)
```

```bash
pip install -r requirements.txt
```

2) Initialiser la base de données

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

3) Générer des données fictives
   (cela peut prendre plusieurs secondes)
```bash
python manage.py seed_demo --patients 2500 --medications 150 
```

5) Lancer le serveur de développement

```bash
python manage.py runserver
```

Ouvrir http://127.0.0.1:8000/Patient et http://127.0.0.1:8000/Medication

Endpoints
---------

- GET /Patient
    - Filtres: nom | last_name, prenom | first_name, date_naissance | birth_date (YYYY-MM-DD)
- GET /Medication
    - Filtres: code, label, status (actif | suppr)

- Prescriptions (Nouvelle ressource)
    - GET /Prescription
    - GET /Prescription/{id}
    - POST /Prescription
    - PUT /Prescription/{id}
    - PATCH /Prescription/{id}
    - DELETE /Prescription/{id}

- Champs:
    - patient (id)
    - medication (id)
    - dosage
    - start_date
    - end_date (optionnel)
    - status (active | completed | cancelled)

- Filtres disponibles
    - patient
    - medication
    - status
    - start_date_gte
    - start_date_lte
    - end_date_gte
    - end_date_lte

Exemples 
---------------
- /Prescription?patient=1
- /Prescription?status=active
- /Prescription?start_date_gte=2024-01-01

Exemples (curl)
---------------

- curl -s "http://127.0.0.1:8000/Patient"
- curl -s "http://127.0.0.1:8000/Patient?nom=Martin"
- curl -s "http://127.0.0.1:8000/Medication?status=actif"

Django Admin
---------------
Interface d’administration disponible via :

    http://127.0.0.1:8000/admin

Créer un super utilisateur :
```bash
python manage.py createsuperuser
```

L’admin permet :
- Gestion des patients
- Gestion des médicaments
- Gestion des prescriptions
- Recherche et filtrage

Documentation API (Swagger / OpenAPI)
-------------------------------------
Documentation interactive disponible via :

    http://127.0.0.1:8000/api/docs/

Schéma OpenAPI brut :

    http://127.0.0.1:8000/api/schema/

Tests
-----

Lancer les tests avec :
```bash
    python manage.py test
```
Les tests couvrent :
- Listes patients et médicaments
- Filtres
- Création de prescription
- Validation métier (end_date > start_date)