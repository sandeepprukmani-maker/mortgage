// Leads page with cached analysis results

let isSearching = false;
let searchAbortController = null;
let currentCacheKey = null;
let qualifiedLeads = [];
let viewedCustomers = new Set();

document.addEventListener('DOMContentLoaded', () => {
  setupEventListeners();
  loadPayloadOptions();
  restoreSessionIfExists();
});

function setupEventListeners() {
  document.getElementById('leadSearchForm').addEventListener('submit', handleSearch);
  document.getElementById('stopBtn').addEventListener('click', stopSearch);
  document.getElementById('exportBtn').addEventListener('click', exportLeads);
}

function loadPayloadOptions() {
  const select = document.getElementById('payloadSelect');
  const payloads = getSavedPayloads();

  select.innerHTML = '<option value="">-- Select a Payload Template --</option>' +
    Object.keys(payloads).map(name => `<option value="${name}">${escapeHtml(name)}</option>`).join('');

  if (Object.keys(payloads).length === 0) {
    select.innerHTML = '<option value="">No payloads available - create one first</option>';
    select.disabled = true;
  }
}

function restoreSessionIfExists() {
  // Check if there's an active session in sessionStorage
  const storedSession = sessionStorage.getItem('analysisSession');
  if (storedSession) {
    try {
      const session = JSON.parse(storedSession);
      currentCacheKey = session.cacheKey;

      // Restore viewed customers
      if (session.viewedCustomers) {
        viewedCustomers = new Set(session.viewedCustomers);
      }

      // Load cached results
      loadCachedResults();
    } catch (error) {
      console.error('Error restoring session:', error);
      sessionStorage.removeItem('analysisSession');
    }
  }
}

async function loadCachedResults() {
  if (!currentCacheKey) return;

  try {
    const data = await apiCall(`/api/analysis/${currentCacheKey}/results`);

    // Update UI with cached results
    document.getElementById('emptyState').classList.add('hidden');
    document.getElementById('resultsSection').classList.remove('hidden');

    // Clear existing grid
    document.getElementById('leadsGrid').innerHTML = '';
    qualifiedLeads = [];

    // Display all cached results
    Object.entries(data.results).forEach(([customerKey, result]) => {
      if (result.best_option) {
        const lead = {
          customer: result.customer,
          ...result.best_option,
          analyzed_at: result.analyzed_at
        };
        qualifiedLeads.push(lead);
        addLeadCard(lead, customerKey);
      }
    });

    updateResultsCount();
    updateProgressDisplay(data.analyzed_count, data.qualified_count, 0);

  } catch (error) {
    // Cache expired or not found
    console.error('Failed to load cached results:', error);
    sessionStorage.removeItem('analysisSession');
    currentCacheKey = null;
  }
}

async function handleSearch(e) {
  e.preventDefault();

  if (isSearching) return;

  const payloadName = document.getElementById('payloadSelect').value;
  if (!payloadName) {
    showToast('Please select a payload template', 'error');
    return;
  }

  const payloads = getSavedPayloads();
  const payload = payloads[payloadName];
  if (!payload) {
    showToast('Payload not found', 'error');
    return;
  }

  const minSavings = parseFloat(document.getElementById('minSavings').value);
  const targetAmount = parseFloat(document.getElementById('targetAmount').value);
  const ttlHours = parseFloat(document.getElementById('ttlHours').value);

  // Start new analysis session
  try {
    const startResponse = await apiCall('/api/analysis/start', {
      method: 'POST',
      body: JSON.stringify({
        payload: payload,
        min_savings: minSavings,
        target_amount: targetAmount,
        ttl_hours: ttlHours
      })
    });

    currentCacheKey = startResponse.cache_key;

    // Save session to sessionStorage
    saveSession();

    // Reset state
    qualifiedLeads = [];
    viewedCustomers = new Set();
    isSearching = true;
    searchAbortController = new AbortController();

    // Update UI
    document.getElementById('searchBtn').classList.add('hidden');
    document.getElementById('stopBtn').classList.remove('hidden');
    document.getElementById('emptyState').classList.add('hidden');
    document.getElementById('progressSection').classList.remove('hidden');
    document.getElementById('resultsSection').classList.remove('hidden');
    document.getElementById('leadsGrid').innerHTML = '';

    // Get all customers
    const customers = await apiCall('/api/customers', {
      signal: searchAbortController.signal
    });

    const total = customers.length;
    let analyzed = 0;

    updateProgressDisplay(analyzed, 0, total);

    // Process customers one by one
    for (const customer of customers) {
      if (!isSearching) break;

      try {
        const result = await apiCall(`/api/analysis/${currentCacheKey}/analyze-next`, {
          method: 'POST',
          body: JSON.stringify({
            customer_key: customer.customer_key
          }),
          signal: searchAbortController.signal
        });

        analyzed++;
        updateProgressDisplay(analyzed, qualifiedLeads.length, total);

        if (result.qualified && result.analysis) {
          const lead = {
            customer: result.analysis.customer,
            ...result.analysis.best_option,
            analyzed_at: result.analysis.analyzed_at
          };
          qualifiedLeads.push(lead);
          addLeadCard(lead, customer.customer_key);
          updateResultsCount();
        }

      } catch (error) {
        if (error.name !== 'AbortError') {
          console.error(`Error analyzing customer ${customer.customer_key}:`, error);
        }
        analyzed++;
        updateProgressDisplay(analyzed, qualifiedLeads.length, total);
      }
    }

    // Search complete
    if (isSearching) {
      showToast(`Analysis complete! Found ${qualifiedLeads.length} qualified leads`, 'success');
    }

  } catch (error) {
    if (error.name !== 'AbortError') {
      showToast(`Error: ${error.message}`, 'error');
    }
  } finally {
    searchComplete();
  }
}

function updateProgressDisplay(analyzed, qualified, total) {
  if (total > 0) {
    const percentage = (analyzed / total) * 100;
    document.getElementById('progressBar').style.width = `${percentage}%`;
    document.getElementById('progressText').textContent =
      analyzed === total ? 'Analysis complete!' : `Analyzing customer ${analyzed} of ${total}...`;
  }

  document.getElementById('analyzedCount').textContent = analyzed;
  document.getElementById('qualifiedCount').textContent = qualified;
}

function addLeadCard(lead, customerKey) {
  const grid = document.getElementById('leadsGrid');
  const card = document.createElement('div');
  const isViewed = viewedCustomers.has(customerKey);

  card.className = `lead-card ${isViewed ? 'lead-viewed' : 'lead-unviewed'}`;
  card.setAttribute('data-customer-key', customerKey);
  card.innerHTML = `
    <div class="lead-header">
      <div class="lead-info">
        <h4>${escapeHtml(lead.customer.name)} ${isViewed ? '<span class="viewed-badge">✓ Viewed</span>' : ''}</h4>
        <div class="lead-contact">
          ${lead.customer.phone ? formatPhone(lead.customer.phone) : ''}
          ${lead.customer.email ? `<br>${escapeHtml(lead.customer.email)}` : ''}
        </div>
      </div>
      <div class="savings-badge">
        ${formatCurrency(lead.monthly_savings)}/mo
      </div>
    </div>

    <div class="lead-details">
      <div class="detail-item">
        <div class="detail-label">Current Payment</div>
        <div class="detail-value">${formatCurrency(lead.customer.current_monthly_payment)}</div>
      </div>
      <div class="detail-item">
        <div class="detail-label">New Payment</div>
        <div class="detail-value">${formatCurrency(lead.monthly_payment)}</div>
      </div>
      <div class="detail-item">
        <div class="detail-label">Annual Savings</div>
        <div class="detail-value text-success">${formatCurrency(lead.monthly_savings * 12)}</div>
      </div>
      <div class="detail-item">
        <div class="detail-label">Interest Rate</div>
        <div class="detail-value">${formatPercent(lead.rate)}</div>
      </div>
      <div class="detail-item">
        <div class="detail-label">Product</div>
        <div class="detail-value">${escapeHtml(lead.product)}</div>
      </div>
      <div class="detail-item">
        <div class="detail-label">Buydown</div>
        <div class="detail-value">${escapeHtml(lead.buydown)}</div>
      </div>
    </div>

    <div class="lead-actions">
      <button class="btn-primary" onclick="viewFullAnalysis('${customerKey}')">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M1 8s3-5 7-5 7 5 7 5-3 5-7 5-7-5-7-5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <circle cx="8" cy="8" r="2" stroke="currentColor" stroke-width="2"/>
        </svg>
        View Full Analysis
      </button>
      <button class="btn-secondary" onclick="contactCustomer('${customerKey}')">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M14 11v1a2 2 0 01-2 2 12 12 0 01-10-10 2 2 0 012-2h1l2 4-1 1a8 8 0 004 4l1-1 4 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Contact
      </button>
    </div>
  `;

  grid.appendChild(card);
}

function updateResultsCount() {
  document.getElementById('resultsCount').textContent =
    `${qualifiedLeads.length} ${qualifiedLeads.length === 1 ? 'customer' : 'customers'} found`;
}

function stopSearch() {
  if (searchAbortController) {
    searchAbortController.abort();
  }
  isSearching = false;
  searchComplete();
  showToast('Search stopped', 'info');
}

function searchComplete() {
  isSearching = false;
  searchAbortController = null;
  document.getElementById('searchBtn').classList.remove('hidden');
  document.getElementById('stopBtn').classList.add('hidden');

  if (qualifiedLeads.length === 0 && !currentCacheKey) {
    document.getElementById('resultsSection').classList.add('hidden');
    document.getElementById('progressSection').classList.add('hidden');
    document.getElementById('emptyState').classList.remove('hidden');
    document.getElementById('emptyState').innerHTML = `
      <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
        <circle cx="32" cy="32" r="28" stroke="currentColor" stroke-width="2" opacity="0.2"/>
        <path d="M32 20v16M32 44h.01" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
      </svg>
      <h3>No Qualified Leads Found</h3>
      <p>Try adjusting your search criteria or adding more customers to the database.</p>
    `;
  }
}

function exportLeads() {
  if (qualifiedLeads.length === 0) {
    showToast('No leads to export', 'error');
    return;
  }

  const csvData = qualifiedLeads.map(lead => ({
    'Customer Name': lead.customer.name,
    'Phone': lead.customer.phone || '',
    'Email': lead.customer.email || '',
    'Current Payment': lead.customer.current_monthly_payment,
    'New Payment': lead.monthly_payment,
    'Monthly Savings': lead.monthly_savings,
    'Annual Savings': lead.monthly_savings * 12,
    'Interest Rate': lead.rate,
    'Product': lead.product,
    'Buydown': lead.buydown,
    'Credit Cost': lead.credit_cost || 0,
    'Analyzed At': lead.analyzed_at
  }));

  const timestamp = new Date().toISOString().split('T')[0];
  exportToCSV(csvData, `qualified-leads-${timestamp}.csv`);
}

function saveSession() {
  if (currentCacheKey) {
    sessionStorage.setItem('analysisSession', JSON.stringify({
      cacheKey: currentCacheKey,
      viewedCustomers: Array.from(viewedCustomers)
    }));
  }
}

window.viewFullAnalysis = async function(customerKey) {
  if (!currentCacheKey) {
    showToast('No active analysis session', 'error');
    return;
  }

  // Mark as viewed
  viewedCustomers.add(customerKey);
  saveSession();

  // Update UI
  const card = document.querySelector(`[data-customer-key="${customerKey}"]`);
  if (card) {
    card.classList.remove('lead-unviewed');
    card.classList.add('lead-viewed');

    const header = card.querySelector('.lead-info h4');
    if (header && !header.querySelector('.viewed-badge')) {
      header.innerHTML += ' <span class="viewed-badge">✓ Viewed</span>';
    }
  }

  // Mark on backend
  try {
    await apiCall(`/api/analysis/${currentCacheKey}/mark-viewed/${customerKey}`, {
      method: 'POST'
    });
  } catch (error) {
    console.error('Failed to mark as viewed:', error);
  }

  // Navigate to analysis page
  window.location.href = `/analysis.html?cache=${currentCacheKey}&customer=${customerKey}`;
};

window.contactCustomer = function(customerKey) {
  const lead = qualifiedLeads.find(l => l.customer.customer_key === customerKey);
  if (!lead) return;

  if (lead.customer.email) {
    window.location.href = `mailto:${lead.customer.email}`;
  } else if (lead.customer.phone) {
    window.location.href = `tel:${lead.customer.phone}`;
  } else {
    showToast('No contact information available', 'error');
  }
};

function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}