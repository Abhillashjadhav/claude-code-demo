// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// State Management
let allStocks = [];
let filteredStocks = [];
let watchlist = JSON.parse(localStorage.getItem('watchlist')) || [];
let isDarkMode = localStorage.getItem('darkMode') === 'true';

// DOM Elements
const stocksTableBody = document.getElementById('stocksTableBody');
const resultCount = document.getElementById('resultCount');
const watchlistCount = document.getElementById('watchlistCount');
const themeToggle = document.getElementById('themeToggle');
const watchlistBtn = document.getElementById('watchlistBtn');
const applyFiltersBtn = document.getElementById('applyFilters');
const resetFiltersBtn = document.getElementById('resetFilters');
const exportCSVBtn = document.getElementById('exportCSV');
const stockModal = document.getElementById('stockModal');
const watchlistModal = document.getElementById('watchlistModal');
const closeModalBtn = document.getElementById('closeModal');
const closeWatchlistBtn = document.getElementById('closeWatchlist');

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

async function initializeApp() {
    // Apply saved theme
    if (isDarkMode) {
        document.documentElement.setAttribute('data-theme', 'dark');
        themeToggle.querySelector('.theme-icon').textContent = '☀️';
    }

    // Load initial data
    await loadStats();
    await loadStocks();
    await loadSectors();

    // Update watchlist count
    updateWatchlistCount();

    // Setup event listeners
    setupEventListeners();
}

function setupEventListeners() {
    themeToggle.addEventListener('click', toggleTheme);
    watchlistBtn.addEventListener('click', openWatchlist);
    applyFiltersBtn.addEventListener('click', applyFilters);
    resetFiltersBtn.addEventListener('click', resetFilters);
    exportCSVBtn.addEventListener('click', exportToCSV);
    closeModalBtn.addEventListener('click', () => closeModal(stockModal));
    closeWatchlistBtn.addEventListener('click', () => closeModal(watchlistModal));

    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === stockModal) closeModal(stockModal);
        if (e.target === watchlistModal) closeModal(watchlistModal);
    });
}

// Theme Toggle
function toggleTheme() {
    isDarkMode = !isDarkMode;
    localStorage.setItem('darkMode', isDarkMode);

    if (isDarkMode) {
        document.documentElement.setAttribute('data-theme', 'dark');
        themeToggle.querySelector('.theme-icon').textContent = '☀️';
    } else {
        document.documentElement.removeAttribute('data-theme');
        themeToggle.querySelector('.theme-icon').textContent = '🌙';
    }
}

// API Calls
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        const data = await response.json();

        document.getElementById('totalStocks').textContent = data.total_stocks;
        document.getElementById('avgPE').textContent = data.average_pe;
        document.getElementById('avgSentiment').textContent = data.average_sentiment;
        document.getElementById('positiveGuidance').textContent = data.guidance_breakdown.positive;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function loadStocks() {
    try {
        const response = await fetch(`${API_BASE_URL}/stocks`);
        allStocks = await response.json();
        filteredStocks = allStocks;
        renderStocksTable();
    } catch (error) {
        console.error('Error loading stocks:', error);
        stocksTableBody.innerHTML = '<tr><td colspan="11" class="loading">Error loading stocks. Please ensure the backend is running.</td></tr>';
    }
}

async function loadSectors() {
    try {
        const response = await fetch(`${API_BASE_URL}/sectors`);
        const sectors = await response.json();
        renderSectorFilters(sectors);
    } catch (error) {
        console.error('Error loading sectors:', error);
    }
}

function renderSectorFilters(sectors) {
    const sectorFilters = document.getElementById('sectorFilters');
    sectorFilters.innerHTML = sectors.map(sector => `
        <label class="checkbox-label">
            <input type="checkbox" value="${sector}" class="sector-checkbox">
            ${sector}
        </label>
    `).join('');
}

// Filtering
async function applyFilters() {
    const filters = {
        min_market_cap: parseFloat(document.getElementById('minMarketCap').value) || null,
        max_market_cap: parseFloat(document.getElementById('maxMarketCap').value) || null,
        min_pe_ratio: parseFloat(document.getElementById('minPE').value) || null,
        max_pe_ratio: parseFloat(document.getElementById('maxPE').value) || null,
        min_ps_ratio: parseFloat(document.getElementById('minPS').value) || null,
        max_ps_ratio: parseFloat(document.getElementById('maxPS').value) || null,
        min_revenue_growth: parseFloat(document.getElementById('minRevGrowth').value) || null,
        min_sentiment_score: parseFloat(document.getElementById('minSentiment').value) || null,
        management_guidance: document.getElementById('guidanceFilter').value || null,
        sectors: Array.from(document.querySelectorAll('.sector-checkbox:checked')).map(cb => cb.value)
    };

    // Remove null values
    Object.keys(filters).forEach(key => {
        if (filters[key] === null || filters[key] === '' || (Array.isArray(filters[key]) && filters[key].length === 0)) {
            delete filters[key];
        }
    });

    try {
        const response = await fetch(`${API_BASE_URL}/screen`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(filters)
        });

        filteredStocks = await response.json();
        renderStocksTable();
    } catch (error) {
        console.error('Error filtering stocks:', error);
    }
}

function resetFilters() {
    document.getElementById('minMarketCap').value = '';
    document.getElementById('maxMarketCap').value = '';
    document.getElementById('minPE').value = '';
    document.getElementById('maxPE').value = '';
    document.getElementById('minPS').value = '';
    document.getElementById('maxPS').value = '';
    document.getElementById('minRevGrowth').value = '';
    document.getElementById('minSentiment').value = '';
    document.getElementById('guidanceFilter').value = '';
    document.querySelectorAll('.sector-checkbox').forEach(cb => cb.checked = false);

    filteredStocks = allStocks;
    renderStocksTable();
}

// Table Rendering
function renderStocksTable() {
    resultCount.textContent = filteredStocks.length;

    if (filteredStocks.length === 0) {
        stocksTableBody.innerHTML = '<tr><td colspan="11" class="loading">No stocks match your filters.</td></tr>';
        return;
    }

    stocksTableBody.innerHTML = filteredStocks.map(stock => `
        <tr>
            <td class="ticker-cell" onclick="viewStockDetails('${stock.ticker}')">${stock.ticker}</td>
            <td>${stock.name}</td>
            <td>${stock.sector}</td>
            <td>$${stock.price.toFixed(2)}</td>
            <td>$${stock.market_cap.toFixed(1)}B</td>
            <td>${stock.pe_ratio ? stock.pe_ratio.toFixed(1) : 'N/A'}</td>
            <td>${stock.ps_ratio ? stock.ps_ratio.toFixed(1) : 'N/A'}</td>
            <td class="${stock.revenue_growth >= 0 ? 'text-success' : 'text-danger'}">
                ${stock.revenue_growth.toFixed(1)}%
            </td>
            <td>
                <span class="sentiment-badge sentiment-${getSentimentClass(stock.sentiment_score)}">
                    ${stock.sentiment_score.toFixed(2)}
                    <span class="trend-${stock.sentiment_trend === 'up' ? 'up' : stock.sentiment_trend === 'down' ? 'down' : ''}"></span>
                </span>
            </td>
            <td>
                <span class="guidance-badge guidance-${stock.management_guidance}">
                    ${stock.management_guidance}
                </span>
            </td>
            <td>
                <div class="action-buttons">
                    <button class="btn-small btn-view" onclick="viewStockDetails('${stock.ticker}')">View</button>
                    <button class="btn-small btn-watchlist ${isInWatchlist(stock.ticker) ? 'active' : ''}"
                            onclick="toggleWatchlist('${stock.ticker}', event)">
                        ${isInWatchlist(stock.ticker) ? '★' : '☆'}
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

function getSentimentClass(score) {
    if (score >= 0.6) return 'positive';
    if (score >= 0.3) return 'neutral';
    return 'negative';
}

// Stock Details Modal
function viewStockDetails(ticker) {
    const stock = allStocks.find(s => s.ticker === ticker);
    if (!stock) return;

    const modalBody = document.getElementById('modalBody');
    document.getElementById('modalTitle').textContent = `${stock.name} (${stock.ticker})`;

    modalBody.innerHTML = `
        <div class="stock-detail-grid">
            <div class="detail-item">
                <div class="detail-label">Current Price</div>
                <div class="detail-value">$${stock.price.toFixed(2)}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Market Cap</div>
                <div class="detail-value">$${stock.market_cap.toFixed(1)}B</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">P/E Ratio</div>
                <div class="detail-value">${stock.pe_ratio ? stock.pe_ratio.toFixed(2) : 'N/A'}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">P/S Ratio</div>
                <div class="detail-value">${stock.ps_ratio ? stock.ps_ratio.toFixed(2) : 'N/A'}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">P/B Ratio</div>
                <div class="detail-value">${stock.pb_ratio ? stock.pb_ratio.toFixed(2) : 'N/A'}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">EV/EBITDA</div>
                <div class="detail-value">${stock.ev_ebitda ? stock.ev_ebitda.toFixed(2) : 'N/A'}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Revenue Growth</div>
                <div class="detail-value ${stock.revenue_growth >= 0 ? 'text-success' : 'text-danger'}">
                    ${stock.revenue_growth.toFixed(1)}%
                </div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Earnings Growth</div>
                <div class="detail-value ${stock.earnings_growth >= 0 ? 'text-success' : 'text-danger'}">
                    ${stock.earnings_growth.toFixed(1)}%
                </div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Volume</div>
                <div class="detail-value">${stock.volume.toLocaleString()}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Sector</div>
                <div class="detail-value">${stock.sector}</div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Sentiment Score</div>
                <div class="detail-value">
                    <span class="sentiment-badge sentiment-${getSentimentClass(stock.sentiment_score)}">
                        ${stock.sentiment_score.toFixed(2)} (${stock.sentiment_trend})
                    </span>
                </div>
            </div>
            <div class="detail-item">
                <div class="detail-label">Management Guidance</div>
                <div class="detail-value">
                    <span class="guidance-badge guidance-${stock.management_guidance}">
                        ${stock.management_guidance}
                    </span>
                </div>
            </div>
        </div>
        <div style="margin-top: 1rem;">
            <button class="btn-primary btn-full" onclick="toggleWatchlist('${stock.ticker}')">
                ${isInWatchlist(stock.ticker) ? 'Remove from Watchlist' : 'Add to Watchlist'}
            </button>
        </div>
    `;

    openModal(stockModal);
}

// Watchlist Management
function toggleWatchlist(ticker, event) {
    if (event) {
        event.stopPropagation();
    }

    const index = watchlist.indexOf(ticker);
    if (index > -1) {
        watchlist.splice(index, 1);
    } else {
        watchlist.push(ticker);
    }

    localStorage.setItem('watchlist', JSON.stringify(watchlist));
    updateWatchlistCount();
    renderStocksTable();

    // If stock modal is open, update it
    if (stockModal.classList.contains('active')) {
        const modalTitle = document.getElementById('modalTitle').textContent;
        if (modalTitle.includes(ticker)) {
            viewStockDetails(ticker);
        }
    }
}

function isInWatchlist(ticker) {
    return watchlist.includes(ticker);
}

function updateWatchlistCount() {
    watchlistCount.textContent = watchlist.length;
}

function openWatchlist() {
    const watchlistContent = document.getElementById('watchlistContent');

    if (watchlist.length === 0) {
        watchlistContent.innerHTML = '<div class="watchlist-empty">Your watchlist is empty. Add stocks by clicking the star icon.</div>';
    } else {
        const watchlistStocks = allStocks.filter(s => watchlist.includes(s.ticker));
        watchlistContent.innerHTML = watchlistStocks.map(stock => `
            <div class="watchlist-item">
                <div>
                    <div style="font-weight: 600; margin-bottom: 0.25rem;">${stock.ticker} - ${stock.name}</div>
                    <div style="font-size: 0.85rem; color: var(--text-secondary);">
                        $${stock.price.toFixed(2)} |
                        <span class="${stock.revenue_growth >= 0 ? 'text-success' : 'text-danger'}">
                            ${stock.revenue_growth.toFixed(1)}% growth
                        </span>
                    </div>
                </div>
                <div style="display: flex; gap: 0.5rem;">
                    <button class="btn-small btn-view" onclick="viewStockDetails('${stock.ticker}'); closeModal(watchlistModal);">
                        View
                    </button>
                    <button class="btn-small btn-watchlist active" onclick="toggleWatchlist('${stock.ticker}'); openWatchlist();">
                        Remove
                    </button>
                </div>
            </div>
        `).join('');
    }

    openModal(watchlistModal);
}

// Modal Controls
function openModal(modal) {
    modal.classList.add('active');
}

function closeModal(modal) {
    modal.classList.remove('active');
}

// Export to CSV
function exportToCSV() {
    const headers = ['Ticker', 'Company', 'Sector', 'Price', 'Market Cap (B)', 'P/E', 'P/S', 'Revenue Growth %', 'Sentiment', 'Guidance'];

    const rows = filteredStocks.map(stock => [
        stock.ticker,
        stock.name,
        stock.sector,
        stock.price,
        stock.market_cap,
        stock.pe_ratio || 'N/A',
        stock.ps_ratio || 'N/A',
        stock.revenue_growth,
        stock.sentiment_score,
        stock.management_guidance
    ]);

    const csvContent = [
        headers.join(','),
        ...rows.map(row => row.join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `nasdaq-tech-screener-${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
