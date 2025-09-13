#!/usr/bin/env python3
"""
Système de Gestion Commerciale
Commercial Management System

Features:
- Achats et Ventes (Purchases and Sales)
- Versements Clients et Fournisseurs (Customer and Supplier Payments)
- Suivi des Stocks (Stock Tracking)
- Interface Moderne Multi-plateformes (Modern Multi-platform Interface)
- Base de données SQLite (SQLite Database)
- Rapports JasperReports (JasperReports Integration)
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os
from models import db, User, Client, Fournisseur, Produit, Vente, Achat, VersementClient, VersementFournisseur, Stock

# Configuration de l'application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'gestion-commerciale-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gestion_commerciale.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation des extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes principales
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Connexion réussie!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Statistiques pour le dashboard
    total_clients = Client.query.count()
    total_fournisseurs = Fournisseur.query.count()
    total_produits = Produit.query.count()
    total_ventes = Vente.query.count()
    total_achats = Achat.query.count()
    
    return render_template('dashboard.html',
                         total_clients=total_clients,
                         total_fournisseurs=total_fournisseurs,
                         total_produits=total_produits,
                         total_ventes=total_ventes,
                         total_achats=total_achats)

# Routes pour les clients
@app.route('/clients')
@login_required
def clients():
    clients = Client.query.all()
    return render_template('clients/list.html', clients=clients)

@app.route('/clients/add', methods=['GET', 'POST'])
@login_required
def add_client():
    if request.method == 'POST':
        client = Client(
            nom=request.form['nom'],
            prenom=request.form['prenom'],
            telephone=request.form['telephone'],
            email=request.form['email'],
            adresse=request.form['adresse']
        )
        db.session.add(client)
        db.session.commit()
        flash('Client ajouté avec succès!', 'success')
        return redirect(url_for('clients'))
    
    return render_template('clients/add.html')

# Routes pour les fournisseurs
@app.route('/fournisseurs')
@login_required
def fournisseurs():
    fournisseurs = Fournisseur.query.all()
    return render_template('fournisseurs/list.html', fournisseurs=fournisseurs)

@app.route('/fournisseurs/add', methods=['GET', 'POST'])
@login_required
def add_fournisseur():
    if request.method == 'POST':
        fournisseur = Fournisseur(
            nom=request.form['nom'],
            telephone=request.form['telephone'],
            email=request.form['email'],
            adresse=request.form['adresse']
        )
        db.session.add(fournisseur)
        db.session.commit()
        flash('Fournisseur ajouté avec succès!', 'success')
        return redirect(url_for('fournisseurs'))
    
    return render_template('fournisseurs/add.html')

# Routes pour les produits
@app.route('/produits')
@login_required
def produits():
    produits = Produit.query.all()
    return render_template('produits/list.html', produits=produits)

@app.route('/produits/add', methods=['GET', 'POST'])
@login_required
def add_produit():
    if request.method == 'POST':
        produit = Produit(
            nom=request.form['nom'],
            description=request.form['description'],
            prix_unitaire=float(request.form['prix_unitaire']),
            seuil_minimum=int(request.form['seuil_minimum'])
        )
        db.session.add(produit)
        db.session.commit()
        
        # Initialiser le stock à zéro
        stock = Stock(produit_id=produit.id, quantite=0)
        db.session.add(stock)
        db.session.commit()
        
        flash('Produit ajouté avec succès!', 'success')
        return redirect(url_for('produits'))
    
    return render_template('produits/add.html')

# Routes pour les stocks
@app.route('/stocks')
@login_required
def stocks():
    stocks = db.session.query(Stock, Produit).join(Produit).all()
    return render_template('stocks/list.html', stocks=stocks)

# Routes pour les ventes
@app.route('/ventes')
@login_required
def ventes():
    ventes = Vente.query.all()
    return render_template('ventes/list.html', ventes=ventes)

@app.route('/ventes/add', methods=['GET', 'POST'])
@login_required
def add_vente():
    if request.method == 'POST':
        vente = Vente(
            client_id=int(request.form['client_id']),
            produit_id=int(request.form['produit_id']),
            quantite=int(request.form['quantite']),
            prix_unitaire=float(request.form['prix_unitaire']),
            date_vente=datetime.now()
        )
        
        # Mettre à jour le stock
        stock = Stock.query.filter_by(produit_id=vente.produit_id).first()
        if stock and stock.quantite >= vente.quantite:
            stock.quantite -= vente.quantite
            db.session.add(vente)
            db.session.commit()
            flash('Vente enregistrée avec succès!', 'success')
            return redirect(url_for('ventes'))
        else:
            flash('Stock insuffisant!', 'error')
    
    clients = Client.query.all()
    produits = Produit.query.all()
    return render_template('ventes/add.html', clients=clients, produits=produits)

# Routes pour les achats
@app.route('/achats')
@login_required
def achats():
    achats = Achat.query.all()
    return render_template('achats/list.html', achats=achats)

@app.route('/achats/add', methods=['GET', 'POST'])
@login_required
def add_achat():
    if request.method == 'POST':
        achat = Achat(
            fournisseur_id=int(request.form['fournisseur_id']),
            produit_id=int(request.form['produit_id']),
            quantite=int(request.form['quantite']),
            prix_unitaire=float(request.form['prix_unitaire']),
            date_achat=datetime.now()
        )
        
        # Mettre à jour le stock
        stock = Stock.query.filter_by(produit_id=achat.produit_id).first()
        if stock:
            stock.quantite += achat.quantite
        else:
            stock = Stock(produit_id=achat.produit_id, quantite=achat.quantite)
        
        db.session.add(achat)
        db.session.add(stock)
        db.session.commit()
        flash('Achat enregistré avec succès!', 'success')
        return redirect(url_for('achats'))
    
    fournisseurs = Fournisseur.query.all()
    produits = Produit.query.all()
    return render_template('achats/add.html', fournisseurs=fournisseurs, produits=produits)

# API pour les données en temps réel
@app.route('/api/stock/<int:produit_id>')
@login_required
def api_stock(produit_id):
    stock = Stock.query.filter_by(produit_id=produit_id).first()
    return jsonify({'quantite': stock.quantite if stock else 0})

def create_default_user():
    """Créer un utilisateur par défaut si aucun n'existe"""
    if User.query.count() == 0:
        admin = User(
            username='admin',
            email='admin@gestion-commerciale.com',
            password=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()
        print("Utilisateur admin créé (admin/admin123)")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_user()
    
    print("Système de Gestion Commerciale démarré!")
    print("Accédez à l'application: http://localhost:5000")
    print("Utilisateur par défaut: admin / admin123")
    
    app.run(debug=True, host='0.0.0.0', port=5000)