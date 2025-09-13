#!/usr/bin/env python3
"""
Système de Gestion Commerciale - Version Simplifiée
Commercial Management System - Simplified Version

Cette version utilise seulement les packages Python standards disponibles.
This version uses only standard Python packages available.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import sqlite3
import os
from datetime import datetime
import hashlib

class GestionCommercialeHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.init_database()
        super().__init__(*args, **kwargs)
    
    def init_database(self):
        """Initialiser la base de données SQLite"""
        conn = sqlite3.connect('gestion_commerciale.db')
        cursor = conn.cursor()
        
        # Créer les tables
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                telephone TEXT,
                email TEXT,
                adresse TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS fournisseurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                telephone TEXT,
                email TEXT,
                adresse TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS produits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                description TEXT,
                prix_unitaire REAL NOT NULL,
                seuil_minimum INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS stocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produit_id INTEGER NOT NULL,
                quantite INTEGER DEFAULT 0,
                derniere_mise_a_jour TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (produit_id) REFERENCES produits (id)
            );
            
            CREATE TABLE IF NOT EXISTS ventes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                produit_id INTEGER NOT NULL,
                quantite INTEGER NOT NULL,
                prix_unitaire REAL NOT NULL,
                date_vente TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients (id),
                FOREIGN KEY (produit_id) REFERENCES produits (id)
            );
            
            CREATE TABLE IF NOT EXISTS achats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fournisseur_id INTEGER NOT NULL,
                produit_id INTEGER NOT NULL,
                quantite INTEGER NOT NULL,
                prix_unitaire REAL NOT NULL,
                date_achat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (fournisseur_id) REFERENCES fournisseurs (id),
                FOREIGN KEY (produit_id) REFERENCES produits (id)
            );
        ''')
        
        # Créer un utilisateur admin par défaut
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                         ('admin', password_hash))
        
        conn.commit()
        conn.close()
    
    def do_GET(self):
        """Gérer les requêtes GET"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/' or path == '/dashboard':
            self.serve_dashboard()
        elif path == '/login':
            self.serve_login()
        elif path == '/clients':
            self.serve_clients()
        elif path == '/fournisseurs':
            self.serve_fournisseurs()
        elif path == '/produits':
            self.serve_produits()
        elif path == '/stocks':
            self.serve_stocks()
        elif path == '/ventes':
            self.serve_ventes()
        elif path == '/achats':
            self.serve_achats()
        elif path.startswith('/static/'):
            self.serve_static(path)
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Gérer les requêtes POST"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        form_data = parse_qs(post_data)
        
        if path == '/login':
            self.handle_login(form_data)
        elif path == '/add_client':
            self.handle_add_client(form_data)
        elif path == '/add_fournisseur':
            self.handle_add_fournisseur(form_data)
        else:
            self.send_error(404)
    
    def serve_login(self):
        """Servir la page de connexion"""
        html = '''
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Connexion - Gestion Commerciale</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Segoe UI', sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center;
                }
                .container { 
                    background: white; 
                    padding: 2rem; 
                    border-radius: 15px; 
                    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                    width: 100%;
                    max-width: 400px;
                }
                .icon { 
                    width: 60px; 
                    height: 60px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 50%; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center;
                    margin: 0 auto 1rem;
                    color: white;
                    font-size: 1.5rem;
                }
                h1 { text-align: center; color: #2d3748; margin-bottom: 0.5rem; }
                p { text-align: center; color: #718096; margin-bottom: 2rem; }
                .form-group { margin-bottom: 1rem; }
                label { display: block; margin-bottom: 0.5rem; color: #2d3748; font-weight: 600; }
                input { 
                    width: 100%; 
                    padding: 0.75rem; 
                    border: 2px solid #e2e8f0; 
                    border-radius: 8px;
                    transition: border-color 0.3s;
                }
                input:focus { 
                    outline: none; 
                    border-color: #667eea; 
                    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
                }
                button { 
                    width: 100%; 
                    padding: 0.75rem; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white; 
                    border: none; 
                    border-radius: 8px; 
                    font-weight: 600;
                    cursor: pointer;
                    transition: transform 0.3s;
                }
                button:hover { transform: translateY(-2px); }
                .info { 
                    background: #e6fffa; 
                    color: #234e52; 
                    padding: 1rem; 
                    border-radius: 8px; 
                    margin-top: 1rem;
                    text-align: center;
                    font-size: 0.875rem;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="icon">🏪</div>
                <h1>Gestion Commerciale</h1>
                <p>Système de gestion des ventes et achats</p>
                
                <form method="POST" action="/login">
                    <div class="form-group">
                        <label for="username">Nom d'utilisateur</label>
                        <input type="text" id="username" name="username" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="password">Mot de passe</label>
                        <input type="password" id="password" name="password" required>
                    </div>
                    
                    <button type="submit">Se connecter</button>
                </form>
                
                <div class="info">
                    👤 Utilisateur par défaut: <strong>admin</strong> / <strong>admin123</strong>
                </div>
            </div>
        </body>
        </html>
        '''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_dashboard(self):
        """Servir le tableau de bord"""
        conn = sqlite3.connect('gestion_commerciale.db')
        cursor = conn.cursor()
        
        # Récupérer les statistiques
        cursor.execute('SELECT COUNT(*) FROM clients')
        total_clients = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM fournisseurs')
        total_fournisseurs = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM produits')
        total_produits = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM ventes')
        total_ventes = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM achats')
        total_achats = cursor.fetchone()[0]
        
        conn.close()
        
        html = f'''
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dashboard - Gestion Commerciale</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: 'Segoe UI', sans-serif; 
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    min-height: 100vh;
                }}
                .navbar {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 1rem 2rem;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .navbar h1 {{ display: inline-block; }}
                .nav-links {{ float: right; }}
                .nav-links a {{ 
                    color: white; 
                    text-decoration: none; 
                    margin-left: 1rem;
                    padding: 0.5rem 1rem;
                    border-radius: 5px;
                    transition: background 0.3s;
                }}
                .nav-links a:hover {{ background: rgba(255,255,255,0.1); }}
                .container {{ 
                    max-width: 1200px; 
                    margin: 2rem auto; 
                    padding: 0 2rem;
                }}
                .stats {{ 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
                    gap: 1rem; 
                    margin-bottom: 2rem;
                }}
                .stat-card {{ 
                    background: white; 
                    padding: 1.5rem; 
                    border-radius: 15px; 
                    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                    text-align: center;
                    transition: transform 0.3s;
                }}
                .stat-card:hover {{ transform: translateY(-5px); }}
                .stat-icon {{ 
                    width: 60px; 
                    height: 60px; 
                    border-radius: 50%; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center;
                    margin: 0 auto 1rem;
                    font-size: 1.5rem;
                    color: white;
                }}
                .primary {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
                .success {{ background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); }}
                .warning {{ background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%); }}
                .info {{ background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%); }}
                .stat-number {{ font-size: 2rem; font-weight: bold; color: #2d3748; }}
                .stat-label {{ color: #718096; }}
                .actions {{ 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                    gap: 1rem;
                }}
                .action-card {{ 
                    background: white; 
                    padding: 1.5rem; 
                    border-radius: 15px; 
                    text-align: center;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                    transition: transform 0.3s;
                }}
                .action-card:hover {{ transform: translateY(-3px); }}
                .action-card a {{ 
                    text-decoration: none; 
                    color: #2d3748;
                    display: block;
                }}
                .action-icon {{ 
                    font-size: 2rem; 
                    margin-bottom: 1rem;
                }}
            </style>
        </head>
        <body>
            <nav class="navbar">
                <h1>🏪 Gestion Commerciale</h1>
                <div class="nav-links">
                    <a href="/clients">👥 Clients</a>
                    <a href="/fournisseurs">🚛 Fournisseurs</a>
                    <a href="/produits">📦 Produits</a>
                    <a href="/stocks">📊 Stocks</a>
                    <a href="/ventes">💰 Ventes</a>
                    <a href="/achats">🛒 Achats</a>
                </div>
                <div style="clear: both;"></div>
            </nav>
            
            <div class="container">
                <h2 style="margin-bottom: 2rem; color: #2d3748;">📊 Tableau de Bord</h2>
                
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-icon primary">👥</div>
                        <div class="stat-number">{total_clients}</div>
                        <div class="stat-label">Clients</div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="stat-icon success">🚛</div>
                        <div class="stat-number">{total_fournisseurs}</div>
                        <div class="stat-label">Fournisseurs</div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="stat-icon warning">📦</div>
                        <div class="stat-number">{total_produits}</div>
                        <div class="stat-label">Produits</div>
                    </div>
                    
                    <div class="stat-card">
                        <div class="stat-icon info">💰</div>
                        <div class="stat-number">{total_ventes}</div>
                        <div class="stat-label">Ventes</div>
                    </div>
                </div>
                
                <h3 style="margin-bottom: 1rem; color: #2d3748;">⚡ Actions Rapides</h3>
                <div class="actions">
                    <div class="action-card">
                        <a href="/clients">
                            <div class="action-icon">👤</div>
                            <div>Gérer Clients</div>
                        </a>
                    </div>
                    
                    <div class="action-card">
                        <a href="/fournisseurs">
                            <div class="action-icon">🏭</div>
                            <div>Gérer Fournisseurs</div>
                        </a>
                    </div>
                    
                    <div class="action-card">
                        <a href="/produits">
                            <div class="action-icon">📦</div>
                            <div>Gérer Produits</div>
                        </a>
                    </div>
                    
                    <div class="action-card">
                        <a href="/stocks">
                            <div class="action-icon">📈</div>
                            <div>Voir Stocks</div>
                        </a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        '''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_clients(self):
        """Servir la liste des clients"""
        conn = sqlite3.connect('gestion_commerciale.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clients ORDER BY created_at DESC')
        clients = cursor.fetchall()
        conn.close()
        
        clients_rows = ''
        for client in clients:
            clients_rows += f'''
                <tr>
                    <td>#{client[0]}</td>
                    <td>{client[1]} {client[2]}</td>
                    <td>{client[3] or 'N/A'}</td>
                    <td>{client[4] or 'N/A'}</td>
                    <td>{client[5][:50] + '...' if client[5] and len(client[5]) > 50 else client[5] or 'N/A'}</td>
                    <td>{client[6][:10]}</td>
                </tr>
            '''
        
        html = f'''
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Clients - Gestion Commerciale</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: 'Segoe UI', sans-serif; 
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    min-height: 100vh;
                }}
                .navbar {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 1rem 2rem;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .navbar h1 {{ display: inline-block; }}
                .nav-links {{ float: right; }}
                .nav-links a {{ 
                    color: white; 
                    text-decoration: none; 
                    margin-left: 1rem;
                    padding: 0.5rem 1rem;
                    border-radius: 5px;
                    transition: background 0.3s;
                }}
                .nav-links a:hover {{ background: rgba(255,255,255,0.1); }}
                .container {{ 
                    max-width: 1200px; 
                    margin: 2rem auto; 
                    padding: 0 2rem;
                }}
                .card {{ 
                    background: white; 
                    border-radius: 15px; 
                    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                    overflow: hidden;
                }}
                .card-header {{ 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 1.5rem;
                    font-weight: bold;
                }}
                .btn {{ 
                    background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
                    color: white;
                    padding: 0.75rem 1.5rem;
                    border: none;
                    border-radius: 8px;
                    text-decoration: none;
                    display: inline-block;
                    margin-bottom: 1rem;
                    transition: transform 0.3s;
                }}
                .btn:hover {{ transform: translateY(-2px); }}
                table {{ 
                    width: 100%; 
                    border-collapse: collapse;
                }}
                th, td {{ 
                    padding: 1rem; 
                    text-align: left; 
                    border-bottom: 1px solid #e2e8f0;
                }}
                th {{ 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }}
                tr:hover {{ background: #f8f9fa; }}
                .empty {{ 
                    text-align: center; 
                    padding: 3rem; 
                    color: #718096;
                }}
                .empty-icon {{ 
                    font-size: 3rem; 
                    margin-bottom: 1rem;
                }}
            </style>
        </head>
        <body>
            <nav class="navbar">
                <h1><a href="/dashboard" style="color: white; text-decoration: none;">🏪 Gestion Commerciale</a></h1>
                <div class="nav-links">
                    <a href="/clients">👥 Clients</a>
                    <a href="/fournisseurs">🚛 Fournisseurs</a>
                    <a href="/produits">📦 Produits</a>
                    <a href="/stocks">📊 Stocks</a>
                    <a href="/ventes">💰 Ventes</a>
                    <a href="/achats">🛒 Achats</a>
                </div>
                <div style="clear: both;"></div>
            </nav>
            
            <div class="container">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
                    <h2 style="color: #2d3748;">👥 Gestion des Clients</h2>
                    <button class="btn" onclick="showAddForm()">➕ Nouveau Client</button>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        📋 Liste des Clients ({len(clients)})
                    </div>
                    {f'''
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Nom Complet</th>
                                <th>Téléphone</th>
                                <th>Email</th>
                                <th>Adresse</th>
                                <th>Date d'ajout</th>
                            </tr>
                        </thead>
                        <tbody>
                            {clients_rows}
                        </tbody>
                    </table>
                    ''' if clients else '''
                    <div class="empty">
                        <div class="empty-icon">👥</div>
                        <h3>Aucun client enregistré</h3>
                        <p>Commencez par ajouter votre premier client</p>
                        <button class="btn" onclick="showAddForm()" style="margin-top: 1rem;">➕ Ajouter un client</button>
                    </div>
                    '''}
                </div>
                
                <!-- Formulaire d'ajout (caché par défaut) -->
                <div id="addForm" style="display: none; margin-top: 2rem;">
                    <div class="card">
                        <div class="card-header">
                            ➕ Ajouter un Nouveau Client
                        </div>
                        <div style="padding: 2rem;">
                            <form method="POST" action="/add_client">
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                                    <div>
                                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Nom *</label>
                                        <input type="text" name="nom" required style="width: 100%; padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 8px;">
                                    </div>
                                    <div>
                                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Prénom *</label>
                                        <input type="text" name="prenom" required style="width: 100%; padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 8px;">
                                    </div>
                                </div>
                                
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                                    <div>
                                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Téléphone</label>
                                        <input type="tel" name="telephone" style="width: 100%; padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 8px;">
                                    </div>
                                    <div>
                                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Email</label>
                                        <input type="email" name="email" style="width: 100%; padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 8px;">
                                    </div>
                                </div>
                                
                                <div style="margin-bottom: 1rem;">
                                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Adresse</label>
                                    <textarea name="adresse" rows="3" style="width: 100%; padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 8px;"></textarea>
                                </div>
                                
                                <div style="display: flex; gap: 1rem;">
                                    <button type="button" onclick="hideAddForm()" style="background: #e53e3e; color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 8px; cursor: pointer;">Annuler</button>
                                    <button type="submit" style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 8px; cursor: pointer;">Enregistrer</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
                function showAddForm() {{
                    document.getElementById('addForm').style.display = 'block';
                }}
                
                function hideAddForm() {{
                    document.getElementById('addForm').style.display = 'none';
                }}
            </script>
        </body>
        </html>
        '''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_login(self, form_data):
        """Gérer la connexion"""
        username = form_data.get('username', [''])[0]
        password = form_data.get('password', [''])[0]
        
        conn = sqlite3.connect('gestion_commerciale.db')
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                      (username, password_hash))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # Rediriger vers le dashboard
            self.send_response(302)
            self.send_header('Location', '/dashboard')
            self.end_headers()
        else:
            # Rediriger vers login avec erreur
            self.send_response(302)
            self.send_header('Location', '/login')
            self.end_headers()
    
    def handle_add_client(self, form_data):
        """Ajouter un nouveau client"""
        nom = form_data.get('nom', [''])[0]
        prenom = form_data.get('prenom', [''])[0]
        telephone = form_data.get('telephone', [''])[0]
        email = form_data.get('email', [''])[0]
        adresse = form_data.get('adresse', [''])[0]
        
        conn = sqlite3.connect('gestion_commerciale.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clients (nom, prenom, telephone, email, adresse) 
            VALUES (?, ?, ?, ?, ?)
        ''', (nom, prenom, telephone, email, adresse))
        conn.commit()
        conn.close()
        
        # Rediriger vers la liste des clients
        self.send_response(302)
        self.send_header('Location', '/clients')
        self.end_headers()
    
    def serve_static(self, path):
        """Servir les fichiers statiques (pour plus tard)"""
        self.send_error(404)
    
    # Méthodes similaires pour les autres sections (fournisseurs, produits, etc.)
    def serve_fournisseurs(self):
        self.serve_clients()  # Pour l'instant, utilise la même logique
        
    def serve_produits(self):
        self.serve_clients()  # Pour l'instant, utilise la même logique
        
    def serve_stocks(self):
        self.serve_clients()  # Pour l'instant, utilise la même logique
        
    def serve_ventes(self):
        self.serve_clients()  # Pour l'instant, utilise la même logique
        
    def serve_achats(self):
        self.serve_clients()  # Pour l'instant, utilise la même logique

def run_server():
    """Démarrer le serveur"""
    port = 8080
    server = HTTPServer(('0.0.0.0', port), GestionCommercialeHandler)
    print(f"🏪 Système de Gestion Commerciale démarré!")
    print(f"🌐 Serveur web accessible sur: http://localhost:{port}")
    print(f"👤 Utilisateur par défaut: admin / admin123")
    print(f"🚀 Appuyez sur Ctrl+C pour arrêter le serveur")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur...")
        server.server_close()

if __name__ == '__main__':
    run_server()