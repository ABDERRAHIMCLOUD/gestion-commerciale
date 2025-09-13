# 🏪 Système de Gestion Commerciale

Un système complet de gestion commerciale avec interface moderne, support multi-plateformes et fonctionnalités métier complètes.

## ✨ Fonctionnalités

### 📊 Modules Principaux
- **👥 Gestion des Clients** - Ajout, modification et suivi des clients
- **🚛 Gestion des Fournisseurs** - Base de données des partenaires
- **📦 Gestion des Produits** - Catalogue avec prix et descriptions
- **📈 Suivi des Stocks** - Surveillance en temps réel avec alertes
- **💰 Gestion des Ventes** - Enregistrement et suivi des transactions
- **🛒 Gestion des Achats** - Réapprovisionnement et commandes
- **💳 Versements** - Suivi des paiements clients et fournisseurs

### 🎨 Interface Moderne
- **Design Responsive** - Compatible téléphone, tablette et PC
- **Icônes Arrondies** - Interface moderne avec émojis
- **Couleurs Impressionnantes** - Gradients et animations CSS
- **Navigation Intuitive** - Menu moderne et ergonomique

### 💾 Base de Données
- **SQLite Intégrée** - Base de données relationnelle
- **Relations Correctes** - Clés étrangères et intégrité
- **Performance Optimisée** - Requêtes efficaces

### 📄 Rapports et Impression
- **JasperReports** - Intégration pour rapports professionnels
- **ReportLab** - Génération PDF native Python
- **Reçus de Vente** - Impression automatique
- **Rapports de Stock** - États périodiques
- **Analyses de Vente** - Statistiques détaillées

## 🚀 Installation et Démarrage

### Prérequis
```bash
Python 3.8+
```

### Installation
```bash
# Cloner le repository
git clone https://github.com/ABDERRAHIMCLOUD/gestion-commerciale.git
cd gestion-commerciale

# Installer les dépendances (optionnel pour la version simple)
pip install -r requirements.txt
```

### Démarrage Rapide
```bash
# Version simple (sans dépendances externes)
python3 app_simple.py

# Version complète Flask (si dépendances installées)
python3 app.py
```

L'application sera accessible sur : **http://localhost:8080**

### Connexion Par Défaut
- **Utilisateur** : `admin`
- **Mot de passe** : `admin123`

## 📱 Multi-Plateformes

### 📱 Mobile (Téléphone)
- Interface responsive optimisée
- Navigation tactile fluide
- Formulaires adaptés écran tactile

### 📱 Tablette
- Affichage en grille optimisé
- Zone de travail étendue
- Navigation hybride

### 💻 PC/Desktop
- Interface complète
- Raccourcis clavier
- Multi-fenêtres

## 🗄️ Structure de la Base de Données

### Tables Principales
```sql
users               # Utilisateurs du système
├── clients         # Base clients avec relations
├── fournisseurs    # Base fournisseurs
├── produits        # Catalogue produits
├── stocks          # État des stocks (FK produits)
├── ventes          # Transactions vente (FK clients, produits)
├── achats          # Transactions achat (FK fournisseurs, produits)
├── versements_clients    # Paiements clients (FK clients)
└── versements_fournisseurs # Paiements fournisseurs (FK fournisseurs)
```

### Relations Clés
- `stocks.produit_id → produits.id`
- `ventes.client_id → clients.id`
- `ventes.produit_id → produits.id`
- `achats.fournisseur_id → fournisseurs.id`
- `achats.produit_id → produits.id`

## 🎯 Utilisation

### 1. Gestion des Clients
- Ajouter nouveaux clients avec informations complètes
- Suivre historique des achats et versements
- Calculer soldes clients automatiquement

### 2. Gestion des Produits
- Créer catalogue avec prix et descriptions
- Définir seuils minimum pour alertes stock
- Suivi valeur stock en temps réel

### 3. Transactions Vente
- Interface simple de saisie vente
- Vérification stock automatique
- Calcul total en temps réel
- Mise à jour stock automatique

### 4. Réapprovisionnement
- Commandes fournisseurs simplifiées
- Alertes stock faible
- Mise à jour stock automatique

### 5. Rapports
```python
from reports import ReportGenerator

# Générer rapport de stock
generator = ReportGenerator()
generator.generate_stock_report('stocks.pdf')

# Reçu de vente
generator.generate_vente_receipt(vente_id, 'recu.pdf')

# Résumé période
generator.generate_sales_summary('2024-01-01', '2024-01-31', 'ventes.pdf')
```

## 🛠️ Développement

### Architecture
```
gestion-commerciale/
├── app.py                 # Application Flask complète
├── app_simple.py          # Version autonome HTTP server
├── models.py             # Modèles de données SQLAlchemy
├── reports.py            # Générateur de rapports
├── requirements.txt      # Dépendances Python
├── static/
│   ├── css/style.css    # Styles modernes
│   └── js/main.js       # JavaScript interactif
├── templates/           # Templates HTML Jinja2
│   ├── base.html       # Template principal
│   ├── dashboard.html  # Tableau de bord
│   ├── login.html      # Page connexion
│   ├── clients/        # Templates clients
│   ├── fournisseurs/   # Templates fournisseurs
│   ├── produits/       # Templates produits
│   ├── stocks/         # Templates stocks
│   ├── ventes/         # Templates ventes
│   └── achats/         # Templates achats
└── gestion_commerciale.db # Base SQLite
```

### Technologies
- **Backend** : Python 3, SQLite, HTTP Server natif
- **Frontend** : HTML5, CSS3, JavaScript vanilla
- **Styles** : CSS Grid, Flexbox, Gradients, Animations
- **Base de données** : SQLite avec relations
- **Rapports** : ReportLab PDF, JasperReports

## 📊 Captures d'Écran

### Dashboard Principal
![Dashboard](https://github.com/user-attachments/assets/206bef38-87b3-416b-b640-cbf65ba07ebf)

### Gestion Clients
![Clients](https://github.com/user-attachments/assets/2c2ebead-e04e-45c7-9d86-cda778b99e01)

### Page de Connexion
![Login](https://github.com/user-attachments/assets/77b9f7e3-21f2-4f7b-a9c3-6afddeb37dd6)

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/amelioration`)
3. Commit les changements (`git commit -m 'Ajout fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

**ABDERRAHIMCLOUD** - *Développement initial*

---

⭐ **N'hésitez pas à donner une étoile si ce projet vous aide !**
