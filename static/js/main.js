// JavaScript pour l'interface moderne et interactive
// Modern and interactive JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Animation pour les cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in-up');
    });

    // Confirmation de suppression
    const deleteButtons = document.querySelectorAll('.btn-danger[data-confirm]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Êtes-vous sûr de vouloir supprimer cet élément ?')) {
                e.preventDefault();
            }
        });
    });

    // Auto-hide des alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.querySelector('.btn-close')) {
                alert.querySelector('.btn-close').click();
            }
        }, 5000);
    });

    // Recherche en temps réel
    const searchInputs = document.querySelectorAll('[data-search]');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const targetTable = document.querySelector(this.dataset.search);
            
            if (targetTable) {
                const rows = targetTable.querySelectorAll('tbody tr');
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(searchTerm) ? '' : 'none';
                });
            }
        });
    });

    // Mise à jour automatique du stock
    function updateStockDisplay() {
        const stockCells = document.querySelectorAll('[data-stock-id]');
        stockCells.forEach(cell => {
            const produitId = cell.dataset.stockId;
            fetch(`/api/stock/${produitId}`)
                .then(response => response.json())
                .then(data => {
                    cell.textContent = data.quantite;
                    
                    // Couleur selon le niveau de stock
                    cell.classList.remove('stock-low', 'stock-medium', 'stock-high');
                    if (data.quantite <= 5) {
                        cell.classList.add('stock-low');
                    } else if (data.quantite <= 20) {
                        cell.classList.add('stock-medium');
                    } else {
                        cell.classList.add('stock-high');
                    }
                })
                .catch(error => console.error('Erreur mise à jour stock:', error));
        });
    }

    // Mettre à jour le stock toutes les 30 secondes
    if (document.querySelectorAll('[data-stock-id]').length > 0) {
        setInterval(updateStockDisplay, 30000);
    }

    // Calculateur automatique pour les formulaires de vente/achat
    const quantityInputs = document.querySelectorAll('input[name="quantite"]');
    const priceInputs = document.querySelectorAll('input[name="prix_unitaire"]');
    const totalDisplays = document.querySelectorAll('[data-total]');

    function calculateTotal() {
        const quantity = parseFloat(document.querySelector('input[name="quantite"]')?.value) || 0;
        const price = parseFloat(document.querySelector('input[name="prix_unitaire"]')?.value) || 0;
        const total = quantity * price;
        
        totalDisplays.forEach(display => {
            display.textContent = total.toFixed(2) + ' €';
        });
    }

    quantityInputs.forEach(input => {
        input.addEventListener('input', calculateTotal);
    });

    priceInputs.forEach(input => {
        input.addEventListener('input', calculateTotal);
    });

    // Validation des formulaires
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredInputs = form.querySelectorAll('input[required], select[required]');
            let valid = true;

            requiredInputs.forEach(input => {
                if (!input.value.trim()) {
                    input.classList.add('is-invalid');
                    valid = false;
                } else {
                    input.classList.remove('is-invalid');
                }
            });

            if (!valid) {
                e.preventDefault();
                alert('Veuillez remplir tous les champs obligatoires.');
            }
        });
    });

    // Smooth scrolling pour les ancres
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Tooltip Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Animation du loading
    function showLoader() {
        const loader = document.createElement('div');
        loader.id = 'page-loader';
        loader.innerHTML = `
            <div class="d-flex justify-content-center align-items-center" style="height: 100vh; position: fixed; top: 0; left: 0; width: 100%; background: rgba(255,255,255,0.9); z-index: 9999;">
                <div class="spinner-border spinner-border-custom" role="status">
                    <span class="visually-hidden">Chargement...</span>
                </div>
            </div>
        `;
        document.body.appendChild(loader);
    }

    function hideLoader() {
        const loader = document.getElementById('page-loader');
        if (loader) {
            loader.remove();
        }
    }

    // Intercepter les liens pour afficher le loader
    const internalLinks = document.querySelectorAll('a[href^="/"]');
    internalLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (!this.getAttribute('href').includes('#')) {
                showLoader();
            }
        });
    });

    // Masquer le loader au chargement de la page
    window.addEventListener('load', hideLoader);

    console.log('Système de Gestion Commerciale - Interface chargée avec succès!');
});

// Fonctions utilitaires
function formatCurrency(amount) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

// Export des fonctions pour usage global
window.GestionCommerciale = {
    formatCurrency,
    formatDate
};