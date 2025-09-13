"""
Models de base de données pour le système de gestion commerciale
SQLite Database Models with Relationships
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Modèle utilisateur pour l'authentification"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Client(db.Model):
    """Modèle pour les clients"""
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    adresse = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    ventes = db.relationship('Vente', backref='client', lazy=True)
    versements = db.relationship('VersementClient', backref='client', lazy=True)
    
    def __repr__(self):
        return f'<Client {self.nom} {self.prenom}>'
    
    @property
    def nom_complet(self):
        return f'{self.nom} {self.prenom}'
    
    @property
    def total_achats(self):
        """Calcul du total des achats du client"""
        return sum(vente.total for vente in self.ventes)
    
    @property
    def total_verse(self):
        """Calcul du total versé par le client"""
        return sum(versement.montant for versement in self.versements)
    
    @property
    def solde(self):
        """Calcul du solde client (dû - versé)"""
        return self.total_achats - self.total_verse

class Fournisseur(db.Model):
    """Modèle pour les fournisseurs"""
    __tablename__ = 'fournisseurs'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    adresse = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    achats = db.relationship('Achat', backref='fournisseur', lazy=True)
    versements = db.relationship('VersementFournisseur', backref='fournisseur', lazy=True)
    
    def __repr__(self):
        return f'<Fournisseur {self.nom}>'
    
    @property
    def total_achats(self):
        """Calcul du total des achats auprès du fournisseur"""
        return sum(achat.total for achat in self.achats)
    
    @property
    def total_verse(self):
        """Calcul du total versé au fournisseur"""
        return sum(versement.montant for versement in self.versements)
    
    @property
    def solde(self):
        """Calcul du solde fournisseur (dû - versé)"""
        return self.total_achats - self.total_verse

class Produit(db.Model):
    """Modèle pour les produits"""
    __tablename__ = 'produits'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    prix_unitaire = db.Column(db.Float, nullable=False)
    seuil_minimum = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    ventes = db.relationship('Vente', backref='produit', lazy=True)
    achats = db.relationship('Achat', backref='produit', lazy=True)
    stock = db.relationship('Stock', backref='produit', uselist=False, lazy=True)
    
    def __repr__(self):
        return f'<Produit {self.nom}>'
    
    @property
    def quantite_en_stock(self):
        """Quantité actuelle en stock"""
        return self.stock.quantite if self.stock else 0
    
    @property
    def alerte_stock(self):
        """Vérifie si le stock est en dessous du seuil minimum"""
        return self.quantite_en_stock <= self.seuil_minimum

class Stock(db.Model):
    """Modèle pour la gestion des stocks"""
    __tablename__ = 'stocks'
    
    id = db.Column(db.Integer, primary_key=True)
    produit_id = db.Column(db.Integer, db.ForeignKey('produits.id'), nullable=False, unique=True)
    quantite = db.Column(db.Integer, default=0, nullable=False)
    derniere_mise_a_jour = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Stock Produit:{self.produit_id} Quantité:{self.quantite}>'

class Vente(db.Model):
    """Modèle pour les ventes"""
    __tablename__ = 'ventes'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produits.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_unitaire = db.Column(db.Float, nullable=False)
    date_vente = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Vente {self.id} - Client:{self.client_id} Produit:{self.produit_id}>'
    
    @property
    def total(self):
        """Calcul du total de la vente"""
        return self.quantite * self.prix_unitaire

class Achat(db.Model):
    """Modèle pour les achats"""
    __tablename__ = 'achats'
    
    id = db.Column(db.Integer, primary_key=True)
    fournisseur_id = db.Column(db.Integer, db.ForeignKey('fournisseurs.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produits.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_unitaire = db.Column(db.Float, nullable=False)
    date_achat = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Achat {self.id} - Fournisseur:{self.fournisseur_id} Produit:{self.produit_id}>'
    
    @property
    def total(self):
        """Calcul du total de l'achat"""
        return self.quantite * self.prix_unitaire

class VersementClient(db.Model):
    """Modèle pour les versements des clients"""
    __tablename__ = 'versements_clients'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    mode_paiement = db.Column(db.String(50), default='Espèces')  # Espèces, Chèque, Virement, etc.
    date_versement = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<VersementClient {self.id} - Client:{self.client_id} Montant:{self.montant}>'

class VersementFournisseur(db.Model):
    """Modèle pour les versements aux fournisseurs"""
    __tablename__ = 'versements_fournisseurs'
    
    id = db.Column(db.Integer, primary_key=True)
    fournisseur_id = db.Column(db.Integer, db.ForeignKey('fournisseurs.id'), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    mode_paiement = db.Column(db.String(50), default='Espèces')  # Espèces, Chèque, Virement, etc.
    date_versement = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<VersementFournisseur {self.id} - Fournisseur:{self.fournisseur_id} Montant:{self.montant}>'