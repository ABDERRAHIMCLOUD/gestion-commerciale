"""
Module d'intégration JasperReports pour la génération de rapports
JasperReports Integration Module for Report Generation
"""

import os
import sqlite3
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

class ReportGenerator:
    """Générateur de rapports avec support JasperReports et ReportLab"""
    
    def __init__(self, db_path='gestion_commerciale.db'):
        self.db_path = db_path
    
    def generate_vente_receipt(self, vente_id, output_path):
        """Générer un reçu de vente"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Récupérer les détails de la vente
        cursor.execute('''
            SELECT v.*, c.nom, c.prenom, c.telephone, c.email, c.adresse,
                   p.nom as produit_nom, p.description
            FROM ventes v
            JOIN clients c ON v.client_id = c.id
            JOIN produits p ON v.produit_id = p.id
            WHERE v.id = ?
        ''', (vente_id,))
        
        vente = cursor.fetchone()
        if not vente:
            return False
        
        # Créer le PDF
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # En-tête
        title = Paragraph("🏪 SYSTÈME DE GESTION COMMERCIALE", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 0.5*cm))
        
        subtitle = Paragraph("REÇU DE VENTE", styles['Heading2'])
        story.append(subtitle)
        story.append(Spacer(1, 0.3*cm))
        
        # Informations de la vente
        vente_info = f"""
        <b>Reçu N°:</b> {vente['id']}<br/>
        <b>Date:</b> {datetime.fromisoformat(vente['date_vente']).strftime('%d/%m/%Y à %H:%M')}<br/>
        <b>Client:</b> {vente['nom']} {vente['prenom']}<br/>
        <b>Téléphone:</b> {vente['telephone'] or 'N/A'}<br/>
        <b>Email:</b> {vente['email'] or 'N/A'}
        """
        
        info_para = Paragraph(vente_info, styles['Normal'])
        story.append(info_para)
        story.append(Spacer(1, 0.5*cm))
        
        # Tableau des articles
        data = [
            ['Article', 'Quantité', 'Prix Unit.', 'Total'],
            [
                vente['produit_nom'],
                str(vente['quantite']),
                f"{vente['prix_unitaire']:.2f} €",
                f"{vente['quantite'] * vente['prix_unitaire']:.2f} €"
            ]
        ]
        
        table = Table(data, colWidths=[6*cm, 3*cm, 3*cm, 3*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.5*cm))
        
        # Total
        total_text = f"<b>TOTAL À PAYER: {vente['quantite'] * vente['prix_unitaire']:.2f} €</b>"
        total_para = Paragraph(total_text, styles['Heading3'])
        story.append(total_para)
        story.append(Spacer(1, 1*cm))
        
        # Pied de page
        footer = Paragraph("Merci de votre confiance !", styles['Normal'])
        story.append(footer)
        
        # Générer le PDF
        doc.build(story)
        conn.close()
        return True
    
    def generate_stock_report(self, output_path):
        """Générer un rapport d'état des stocks"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Récupérer l'état des stocks
        cursor.execute('''
            SELECT p.nom, p.prix_unitaire, p.seuil_minimum, 
                   COALESCE(s.quantite, 0) as stock_actuel,
                   COALESCE(s.quantite * p.prix_unitaire, 0) as valeur_stock
            FROM produits p
            LEFT JOIN stocks s ON p.id = s.produit_id
            ORDER BY p.nom
        ''')
        
        stocks = cursor.fetchall()
        
        # Créer le PDF
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # En-tête
        title = Paragraph("🏪 RAPPORT D'ÉTAT DES STOCKS", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 0.5*cm))
        
        date_rapport = Paragraph(f"Date du rapport: {datetime.now().strftime('%d/%m/%Y à %H:%M')}", styles['Normal'])
        story.append(date_rapport)
        story.append(Spacer(1, 0.5*cm))
        
        # Statistiques générales
        total_articles = len(stocks)
        stock_critique = sum(1 for s in stocks if s['stock_actuel'] <= s['seuil_minimum'])
        valeur_totale = sum(s['valeur_stock'] for s in stocks)
        
        stats = f"""
        <b>Total d'articles:</b> {total_articles}<br/>
        <b>Articles en stock critique:</b> {stock_critique}<br/>
        <b>Valeur totale du stock:</b> {valeur_totale:.2f} €
        """
        
        stats_para = Paragraph(stats, styles['Normal'])
        story.append(stats_para)
        story.append(Spacer(1, 0.5*cm))
        
        # Tableau des stocks
        data = [['Article', 'Stock', 'Seuil Min.', 'État', 'Valeur']]
        
        for stock in stocks:
            etat = "🔴 Critique" if stock['stock_actuel'] <= stock['seuil_minimum'] else \
                   "🟡 Faible" if stock['stock_actuel'] <= stock['seuil_minimum'] * 2 else \
                   "🟢 Normal"
            
            data.append([
                stock['nom'],
                str(stock['stock_actuel']),
                str(stock['seuil_minimum']),
                etat,
                f"{stock['valeur_stock']:.2f} €"
            ])
        
        table = Table(data, colWidths=[5*cm, 2*cm, 2*cm, 3*cm, 3*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        
        # Générer le PDF
        doc.build(story)
        conn.close()
        return True
    
    def generate_sales_summary(self, start_date, end_date, output_path):
        """Générer un résumé des ventes sur une période"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Récupérer les ventes de la période
        cursor.execute('''
            SELECT v.*, c.nom, c.prenom, p.nom as produit_nom
            FROM ventes v
            JOIN clients c ON v.client_id = c.id
            JOIN produits p ON v.produit_id = p.id
            WHERE DATE(v.date_vente) BETWEEN ? AND ?
            ORDER BY v.date_vente DESC
        ''', (start_date, end_date))
        
        ventes = cursor.fetchall()
        
        # Créer le PDF
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # En-tête
        title = Paragraph("📊 RÉSUMÉ DES VENTES", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 0.5*cm))
        
        periode = Paragraph(f"Période: du {start_date} au {end_date}", styles['Heading3'])
        story.append(periode)
        story.append(Spacer(1, 0.3*cm))
        
        # Statistiques
        if ventes:
            total_ventes = len(ventes)
            ca_total = sum(v['quantite'] * v['prix_unitaire'] for v in ventes)
            
            stats = f"""
            <b>Nombre de ventes:</b> {total_ventes}<br/>
            <b>Chiffre d'affaires:</b> {ca_total:.2f} €<br/>
            <b>Vente moyenne:</b> {ca_total/total_ventes:.2f} €
            """
        else:
            stats = "<b>Aucune vente sur cette période</b>"
        
        stats_para = Paragraph(stats, styles['Normal'])
        story.append(stats_para)
        story.append(Spacer(1, 0.5*cm))
        
        if ventes:
            # Tableau des ventes
            data = [['Date', 'Client', 'Produit', 'Qté', 'Total']]
            
            for vente in ventes:
                data.append([
                    datetime.fromisoformat(vente['date_vente']).strftime('%d/%m'),
                    f"{vente['nom']} {vente['prenom']}",
                    vente['produit_nom'],
                    str(vente['quantite']),
                    f"{vente['quantite'] * vente['prix_unitaire']:.2f} €"
                ])
            
            table = Table(data, colWidths=[2*cm, 4*cm, 4*cm, 2*cm, 3*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
        
        # Générer le PDF
        doc.build(story)
        conn.close()
        return True

# Exemple d'utilisation
if __name__ == '__main__':
    generator = ReportGenerator()
    
    # Test de génération d'un rapport de stock
    if generator.generate_stock_report('rapport_stocks.pdf'):
        print("✅ Rapport de stocks généré: rapport_stocks.pdf")
    else:
        print("❌ Erreur lors de la génération du rapport")