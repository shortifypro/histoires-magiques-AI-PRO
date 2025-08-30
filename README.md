# Histoires Magiques - Générateur d'histoires audio pour enfants

## 🎯 Description

Histoires Magiques est une application web complète qui génère des histoires audio personnalisées pour enfants. L'application combine intelligence artificielle, génération audio et système de paiement pour offrir une expérience magique aux familles.

## ✨ Fonctionnalités

### 🎨 Frontend
- **Design enfantin** avec couleurs magiques et illustrations personnalisées
- **Interface responsive** (mobile, tablette, desktop)
- **Navigation intuitive** avec sections dédiées
- **Système de tarification** avec 3 plans (Gratuit, Starter, Family)

### 🤖 Backend & IA
- **Génération d'histoires** avec OpenAI GPT-3.5-turbo
- **6 thèmes disponibles** : Aventure, Amitié, Nature, Courage, Famille, Magie
- **3 types de personnages** : Animaux, Humains, Fantastiques
- **Personnalisation complète** : nom, thème, morale, âge

### 🎵 Audio
- **Génération audio** avec ElevenLabs
- **2 voix disponibles** : féminine et masculine
- **Narration optimisée** avec introduction et conclusion
- **Système de fallback** en cas d'erreur

### 📄 Documents
- **Génération PDF automatique** du livret d'histoire
- **Fichiers MP3** téléchargeables
- **Bibliothèque personnelle** pour chaque utilisateur

### 💳 Paiements
- **Intégration PayPal** complète
- **Système de crédits gratuits** (3 par utilisateur)
- **Abonnements mensuels** avec gestion automatique
- **Webhooks PayPal** pour les notifications

## 🚀 Installation

### Prérequis
- Python 3.11+
- Node.js 20+
- Comptes API : OpenAI, ElevenLabs, PayPal

### Backend (Flask)
```bash
cd histoires-magiques-api
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Frontend (React)
```bash
cd histoires-magiques
npm install
npm run build
cp -r dist/* ../histoires-magiques-api/src/static/
```

### Configuration
1. Copiez `.env.example` vers `.env`
2. Remplissez vos clés API :
   - `OPENAI_API_KEY` : Votre clé OpenAI
   - `ELEVENLABS_API_KEY` : Votre clé ElevenLabs
   - `PAYPAL_CLIENT_ID` et `PAYPAL_CLIENT_SECRET` : Vos identifiants PayPal

### Lancement
```bash
cd histoires-magiques-api
source venv/bin/activate
python src/main.py
```

L'application sera accessible sur `http://localhost:5001`

## 📊 Structure du projet

```
histoires-magiques-api/
├── src/
│   ├── models/           # Modèles de base de données
│   │   ├── user.py       # Utilisateurs et crédits
│   │   └── subscription.py # Abonnements et histoires
│   ├── routes/           # Routes API
│   │   ├── user.py       # Gestion utilisateurs
│   │   ├── paypal.py     # Paiements PayPal
│   │   ├── stories.py    # Génération d'histoires
│   │   └── audio.py      # Génération audio
│   ├── static/           # Frontend compilé
│   └── main.py           # Point d'entrée Flask
├── requirements.txt      # Dépendances Python
└── README.md

histoires-magiques/       # Code source React
├── src/
│   ├── components/       # Composants React
│   └── assets/          # Images et ressources
└── dist/                # Build de production
```

## 🔧 API Endpoints

### Histoires
- `POST /api/stories/generate` - Générer une nouvelle histoire
- `GET /api/stories/themes` - Liste des thèmes disponibles
- `GET /api/stories/user-stories/<email>` - Histoires d'un utilisateur
- `GET /api/stories/user-credits/<email>` - Crédits restants

### Audio
- `POST /api/audio/generate` - Générer l'audio d'une histoire
- `GET /api/audio/voices` - Liste des voix disponibles
- `POST /api/audio/regenerate-audio` - Changer la voix

### PayPal
- `POST /api/paypal/create-subscription` - Créer un abonnement
- `POST /api/paypal/execute-subscription` - Activer un abonnement
- `POST /api/paypal/cancel-subscription` - Annuler un abonnement
- `GET /api/paypal/subscription-status/<email>` - Statut utilisateur

## 💰 Modèle économique

### Plan Gratuit (0€)
- 3 histoires gratuites à l'inscription
- Fichiers MP3 et PDF inclus
- Voix française de qualité

### Plan Starter (12€/mois)
- Histoires illimitées
- Toutes les voix disponibles
- Personnalisation avancée
- Bibliothèque personnelle

### Plan Family (24€/mois)
- Tout du plan Starter
- Jusqu'à 5 profils enfants
- Histoires plus longues (10 min)
- Accès anticipé aux nouveautés

## 🛠️ Technologies utilisées

### Frontend
- **React** + **Vite** - Framework et build tool
- **Tailwind CSS** - Styling
- **Lucide Icons** - Icônes

### Backend
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM base de données
- **SQLite** - Base de données

### IA & Audio
- **OpenAI GPT-3.5-turbo** - Génération de texte
- **ElevenLabs** - Synthèse vocale
- **FPDF2** - Génération PDF

### Paiements
- **PayPal REST SDK** - Gestion des abonnements

## 📝 Licence

Ce projet est propriétaire. Tous droits réservés.

## 📞 Support

Pour toute question : contact@histoires-magiques.com

---

**Créé avec ❤️ pour les familles qui aiment les belles histoires**

