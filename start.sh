#!/bin/bash

# 🏪 Script de démarrage du Système de Gestion Commerciale
# Commercial Management System Startup Script

echo "🏪 Démarrage du Système de Gestion Commerciale..."
echo "📅 $(date)"
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

echo "✅ Python 3 détecté: $(python3 --version)"

# Vérifier si le fichier de base de données existe
if [ ! -f "gestion_commerciale.db" ]; then
    echo "📄 Création de la base de données..."
fi

# Essayer d'installer les dépendances si requirements.txt existe
if [ -f "requirements.txt" ]; then
    echo "📦 Tentative d'installation des dépendances..."
    python3 -m pip install -r requirements.txt --user --quiet 2>/dev/null || echo "⚠️  Installation des dépendances échouée, utilisation de la version simple"
fi

# Démarrer le serveur
echo ""
echo "🚀 Démarrage du serveur web..."
echo "🌐 URL: http://localhost:8080"
echo "👤 Connexion: admin / admin123"
echo ""
echo "📱 Compatible mobile, tablette et PC"
echo "🎨 Interface moderne avec couleurs impressionnantes"
echo "🔄 Appuyez sur Ctrl+C pour arrêter"
echo ""

# Essayer Flask d'abord, sinon version simple
if python3 -c "import flask" 2>/dev/null; then
    echo "🌶️  Démarrage avec Flask..."
    python3 app.py
else
    echo "🐍 Démarrage avec serveur HTTP natif..."
    python3 app_simple.py
fi