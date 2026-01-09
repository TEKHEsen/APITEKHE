

# 🩺 TEKHE - Santé Maternelle & Néonatale (Sénégal)

**TEKHE** est une plateforme numérique d'intelligence clinique conçue pour réduire la mortalité maternelle et néonatale au Sénégal. Elle permet le suivi prénatal/postnatal, le calcul du risque obstétrical (Moteur de règles GHIF), l'enrôlement à la Couverture Sanitaire Universelle (CSU) et la gestion des références SONU.

---

## 🚀 Fonctionnalités Clés

* **Offline-First & Sync :** Identification communautaire via UUID pour un fonctionnement sans réseau.
* **Moteur de Risque GHIF :** Analyse en temps réel des facteurs morbides (Antécédents, biométrie, signes de danger) avec sémaphore de couleur (Vert, Orange, Rouge).
* **Module CSU :** Enrôlement au point de service, capture d'attestations et génération de preuves via QR Code.
* **Suivi Nutritionnel :** Monitoring de l'IMC, du périmètre brachial (MUAC) et de la prise de poids.
* **Contrôle Géo-Hiérarchique :** Accès aux données strictement limité selon le niveau (National, Régional, District, Poste).
* **Alerte SONU :** Timeline de référence en temps réel pour les urgences obstétricales.

---

## 🛠 Architecture Technique

* **Backend :** Python 3.13 + FastAPI (Asynchrone).
* **Base de données :** PostgreSQL (SQLAlchemy ORM).
* **Validation :** Pydantic v2 (Validation stricte des données de santé).
* **Sécurité :** JWT (JSON Web Tokens) & Hachage de mots de passe (Passlib/Bcrypt).
* **Interopérabilité :** Export JSON/CSV conforme aux formats DHIS2 Sénégal.

---

## 📂 Structure du Projet

```text
TEKHE/
├── app/
│   ├── api/            # Endpoints FastAPI (v1)
│   ├── core/           # Configuration, Sécurité, Constantes
│   ├── crud/           # Logique d'accès à la base de données (DAO)
│   ├── db/             # Modèles SQLAlchemy & Sessions
│   ├── models/         # Définition des tables SQL
│   ├── schemas/        # Modèles Pydantic (DTO)
│   └── services/       # Moteur de risque, Calcul CSU, Sync
├── main.py             # Point d'entrée de l'application
├── .env                # Variables d'environnement (non versionné)
└── requirements.txt    # Dépendances Python

```

---

## ⚙️ Installation et Configuration

### 1. Clonage et Environnement

```powershell
git clone https://github.com/votre-repo/tekhe.git
cd tekhe
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

```

### 2. Configuration (`.env`)

Créez un fichier `.env` à la racine :

```env
PROJECT_NAME="TEKHE API"
SECRET_KEY="votre_cle_secrete"
POSTGRES_USER=postgres
POSTGRES_PASSWORD=votre_pass
POSTGRES_SERVER=localhost
POSTGRES_DB=tekhe_db

# Identifiants Admin par défaut
FIRST_SUPERUSER=admin@tekhe.sn
FIRST_SUPERUSER_PASSWORD=TekheSenegal2026!

```

### 3. Initialisation de la Base de Données

Cette commande crée les tables, les zones géographiques de base et l'administrateur national :

```powershell
python -m app.db.init_db

```

---

## 🖥️ Utilisation

### Lancer le serveur

```powershell
python main.py

```

### Accéder à la Documentation

L'API est auto-documentée. Une fois le serveur lancé, visitez :

* **Swagger UI (Interactif) :** `http://127.0.0.1:8000/docs`
* **ReDoc :** `http://127.0.0.1:8000/redoc`

---

## 🩺 Moteur de Risque (Exemple de calcul)

Le système évalue le risque selon les paramètres suivants :

1. **Facteurs Gynéco :** Âge (<18 ou >35), Taille (<152cm), Drépanocytose SS.
2. **Facteurs Obstétricaux :** Bassin rétréci, Saignements, Absence de MAF.
3. **Nutrition :** IMC critique ou MUAC < 23cm.

---

## 🤝 Contribution

1. Créez une branche (`feature/ma-fonctionnalite`).
2. Commitez vos changements.
3. Ouvrez une Pull Request pour revue clinique et technique.

---

## 📝 Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.

---

**Contact Technique :** 7MAKSACOD (Admin TEKHE Project)
