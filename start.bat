@echo off
rem 🏪 Script de démarrage Windows pour le Système de Gestion Commerciale
rem Windows Startup Script for Commercial Management System

echo 🏪 Démarrage du Système de Gestion Commerciale...
echo 📅 %date% %time%
echo.

rem Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou accessible
    pause
    exit /b 1
)

echo ✅ Python détecté
python --version

rem Vérifier si le fichier de base de données existe
if not exist "gestion_commerciale.db" (
    echo 📄 Création de la base de données...
)

rem Essayer d'installer les dépendances
if exist "requirements.txt" (
    echo 📦 Tentative d'installation des dépendances...
    python -m pip install -r requirements.txt --user --quiet >nul 2>&1 || echo ⚠️ Installation des dépendances échouée, utilisation de la version simple
)

echo.
echo 🚀 Démarrage du serveur web...
echo 🌐 URL: http://localhost:8080
echo 👤 Connexion: admin / admin123
echo.
echo 📱 Compatible mobile, tablette et PC
echo 🎨 Interface moderne avec couleurs impressionnantes
echo 🔄 Appuyez sur Ctrl+C pour arrêter
echo.

rem Essayer Flask d'abord, sinon version simple
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo 🐍 Démarrage avec serveur HTTP natif...
    python app_simple.py
) else (
    echo 🌶️ Démarrage avec Flask...
    python app.py
)

pause