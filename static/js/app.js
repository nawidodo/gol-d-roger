// API Base URL
const API_BASE = window.location.origin;

// State
let currentPrices = null;
let purchases = [];
let editingId = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadPrices();
    loadPurchases();
    loadPortfolio();
    setupFormHandlers();

    // Refresh prices every 5 minutes
    setInterval(loadPrices, 5 * 60 * 1000);
});

// Setup form handlers
function setupFormHandlers() {
    const form = document.getElementById('purchaseForm');
    form.addEventListener('submit', handleFormSubmit);

    // Auto-calculate total when weight or price changes
    const weightInput = document.getElementById('weight');
    const priceInput = document.getElementById('purchasePrice');

    weightInput.addEventListener('input', calculateTotal);
    priceInput.addEventListener('input', calculateTotal);
}

// Calculate total paid
function calculateTotal() {
    const weight = parseFloat(document.getElementById('weight').value) || 0;
    const price = parseFloat(document.getElementById('purchasePrice').value) || 0;
    const total = weight * price;
    document.getElementById('totalPaid').value = total.toFixed(2);
}

// Load current gold prices
async function loadPrices() {
    try {
        const response = await fetch(`${API_BASE}/api/prices`);
        const data = await response.json();

        if (data.error) {
            console.error('Error loading prices:', data.error);
            return;
        }

        currentPrices = data;
        displayPriceTicker(data);
    } catch (error) {
        console.error('Error loading prices:', error);
    }
}

// Display price ticker
function displayPriceTicker(priceData) {
    const ticker = document.getElementById('priceTicker');

    if (!priceData.data) {
        ticker.innerHTML = '<div class="ticker-item">Loading prices...</div>';
        return;
    }

    const items = Object.entries(priceData.data)
        .map(([weight, prices]) => {
            const buyPrice = formatCurrency(prices.buy);
            return `<div class="ticker-item">${weight}g: ${buyPrice}</div>`;
        })
        .join('');

    ticker.innerHTML = items;
}

// Load purchases
async function loadPurchases() {
    try {
        const response = await fetch(`${API_BASE}/api/purchases`);
        purchases = await response.json();
        displayPurchases();
    } catch (error) {
        console.error('Error loading purchases:', error);
        document.getElementById('purchaseList').innerHTML =
            '<div class="error">Failed to load purchases</div>';
    }
}

// Display purchases
function displayPurchases() {
    const container = document.getElementById('purchaseList');

    if (purchases.length === 0) {
        container.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">📊</div>
        <p>No purchases yet. Add your first gold purchase above!</p>
      </div>
    `;
        return;
    }

    const html = purchases.map(purchase => {
        const date = new Date(purchase.purchase_date).toLocaleDateString('id-ID', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });

        return `
      <div class="purchase-item fade-in">
        <div class="purchase-header">
          <div class="purchase-weight">${purchase.weight}g</div>
          <div class="purchase-actions">
            <button class="btn btn-small" onclick="editPurchase(${purchase.id})">Edit</button>
            <button class="btn btn-danger btn-small" onclick="deletePurchase(${purchase.id})">Delete</button>
          </div>
        </div>
        <div class="purchase-details">
          <div class="detail-item">
            <span class="detail-label">Purchase Price</span>
            <span class="detail-value">${formatCurrency(purchase.purchase_price)}/g</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Total Paid</span>
            <span class="detail-value">${formatCurrency(purchase.total_paid)}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Date</span>
            <span class="detail-value">${date}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Added</span>
            <span class="detail-value">${formatRelativeTime(purchase.created_at)}</span>
          </div>
        </div>
        ${purchase.notes ? `<div class="purchase-notes">${purchase.notes}</div>` : ''}
      </div>
    `;
    }).join('');

    container.innerHTML = html;
}

// Load portfolio summary
async function loadPortfolio() {
    try {
        const response = await fetch(`${API_BASE}/api/portfolio`);
        const data = await response.json();

        if (data.error) {
            console.error('Error loading portfolio:', data.error);
            return;
        }

        displayPortfolio(data);
    } catch (error) {
        console.error('Error loading portfolio:', error);
    }
}

// Display portfolio summary
function displayPortfolio(data) {
    document.getElementById('totalWeight').textContent = `${data.total_weight.toFixed(2)}g`;
    document.getElementById('totalInvested').textContent = formatCurrency(data.total_invested);
    document.getElementById('currentValue').textContent = formatCurrency(data.current_value);

    const profitLoss = data.profit_loss;
    const percentage = data.profit_loss_percentage;
    const profitElement = document.getElementById('profitLoss');

    const sign = profitLoss >= 0 ? '+' : '';
    const className = profitLoss >= 0 ? 'profit-positive' : 'profit-negative';

    profitElement.textContent = `${sign}${formatCurrency(profitLoss)}`;
    profitElement.className = `card-value ${className}`;

    document.getElementById('profitPercentage').textContent =
        `${sign}${percentage.toFixed(2)}%`;
    document.getElementById('profitPercentage').className =
        `card-subtitle ${className}`;
}

// Handle form submit
async function handleFormSubmit(e) {
    e.preventDefault();

    const formData = {
        weight: parseFloat(document.getElementById('weight').value),
        purchase_price: parseFloat(document.getElementById('purchasePrice').value),
        total_paid: parseFloat(document.getElementById('totalPaid').value),
        purchase_date: document.getElementById('purchaseDate').value,
        notes: document.getElementById('notes').value
    };

    try {
        let response;
        if (editingId) {
            response = await fetch(`${API_BASE}/api/purchases/${editingId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
        } else {
            response = await fetch(`${API_BASE}/api/purchases`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
        }

        if (response.ok) {
            document.getElementById('purchaseForm').reset();
            editingId = null;
            document.querySelector('.section-title').textContent = '➕ Add Purchase';
            await loadPurchases();
            await loadPortfolio();
        } else {
            const error = await response.json();
            alert(`Error: ${error.error}`);
        }
    } catch (error) {
        console.error('Error saving purchase:', error);
        alert('Failed to save purchase');
    }
}

// Edit purchase
function editPurchase(id) {
    const purchase = purchases.find(p => p.id === id);
    if (!purchase) return;

    editingId = id;
    document.querySelector('.section-title').textContent = '✏️ Edit Purchase';

    document.getElementById('weight').value = purchase.weight;
    document.getElementById('purchasePrice').value = purchase.purchase_price;
    document.getElementById('totalPaid').value = purchase.total_paid;
    document.getElementById('purchaseDate').value = purchase.purchase_date.split('T')[0];
    document.getElementById('notes').value = purchase.notes || '';

    // Scroll to form
    document.querySelector('.form-section').scrollIntoView({ behavior: 'smooth' });
}

// Delete purchase
async function deletePurchase(id) {
    if (!confirm('Are you sure you want to delete this purchase?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/purchases/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            await loadPurchases();
            await loadPortfolio();
        } else {
            const error = await response.json();
            alert(`Error: ${error.error}`);
        }
    } catch (error) {
        console.error('Error deleting purchase:', error);
        alert('Failed to delete purchase');
    }
}

// Format currency (Indonesian Rupiah)
function formatCurrency(amount) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

// Format relative time
function formatRelativeTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;

    return date.toLocaleDateString('id-ID', { month: 'short', day: 'numeric' });
}
