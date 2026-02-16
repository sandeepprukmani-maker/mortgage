// Customer Analysis Page with cached results

let cacheKey = null;
let customerKey = null;
let customerData = null;

document.addEventListener('DOMContentLoaded', () => {
  setupEventListeners();
  getParametersFromURL();
});

function setupEventListeners() {
  // Back button
  document.getElementById('backBtn').addEventListener('click', () => {
    window.location.href = '/leads.html';
  });

  // Analysis form submit (single-customer analysis)
  const analysisForm = document.getElementById('analysisForm');
  if (analysisForm) {
    analysisForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      // If we're in cached mode, the form shouldn't run here (cached view uses separate flow)
      if (cacheKey && customerKey) {
        showToast('Viewing cached analysis', 'info');
        return;
      }

      // Single-customer analysis flow
      if (!customerKey) {
        showToast('No customer specified', 'error');
        return;
      }

      const payloadSelect = document.getElementById('payloadSelect');
      const payloadName = payloadSelect ? payloadSelect.value : '';
      if (!payloadName) {
        showToast('Please select a payload template', 'error');
        return;
      }

      const payloads = getSavedPayloads();
      const basePayload = payloads[payloadName];
      if (!basePayload) {
        showToast('Selected payload not found', 'error');
        return;
      }

      const minSavings = parseFloat(document.getElementById('minSavings').value || '200');
      const targetAmount = parseFloat(document.getElementById('targetAmount').value || '-2000');

      // Show loading state
      document.getElementById('loadingState').classList.remove('hidden');
      document.getElementById('configPanel').classList.add('hidden');
      document.getElementById('resultsSection').classList.add('hidden');
      document.getElementById('noResultsState').classList.add('hidden');

      try {
        const resp = await apiCall(`/api/customers/${customerKey}/analyze`, {
          method: 'POST',
          body: JSON.stringify({
            payload: basePayload,
            min_savings: minSavings,
            target_amount: targetAmount
          })
        });

        // The detailed analyze endpoint returns an object with scenarios, customer, best_option, etc.
        // Reuse the displayAnalysisResults call which expects { customer, scenarios }
        // If the API returns a slightly different shape, adapt minimally here.
        if (!resp) {
          throw new Error('Empty response from analysis API');
        }

        // If the response includes 'error' field, throw
        if (resp.error) {
          throw new Error(resp.error);
        }

        // Ensure customer is present
        if (!resp.customer) {
          // If API returned top-level customer info under a different key, try to map it.
          if (resp.customer_data) resp.customer = resp.customer_data;
        }

        // Show results section
        document.getElementById('loadingState').classList.add('hidden');
        document.getElementById('resultsSection').classList.remove('hidden');

        displayAnalysisResults(resp);

      } catch (err) {
        document.getElementById('loadingState').classList.add('hidden');
        document.getElementById('configPanel').classList.remove('hidden');
        showToast(`Analysis failed: ${err.message}`, 'error');
      }
    });
  }
}

function getParametersFromURL() {
  const urlParams = new URLSearchParams(window.location.search);
  cacheKey = urlParams.get('cache');
  customerKey = urlParams.get('customer');

  // If both cache and customer are provided, show cached result
  if (cacheKey && customerKey) {
    loadCachedAnalysis();
    return;
  }

  // If only customer is provided, load single-customer analysis UI
  if (customerKey && !cacheKey) {
    // Populate payload dropdown from localStorage
    loadPayloadOptions();
    loadCustomerForSingleAnalysis(customerKey);
    return;
  }

  // No valid params
  showToast('Invalid parameters', 'error');
  return;
}

async function loadCustomerForSingleAnalysis(cKey) {
  try {
    // Fetch all customers and find the one we need
    const customers = await apiCall('/api/customers');
    const customer = (customers || []).find(c => c.customer_key === cKey);

    if (!customer) {
      showToast('Customer not found', 'error');
      return;
    }

    customerData = customer;

    // Update page title and info card
    document.getElementById('customerName').textContent = `Analysis: ${customer.name}`;
    document.getElementById('currentPayment').textContent = formatCurrency(customer.current_monthly_payment);
    document.getElementById('remainingBalance').textContent = formatCurrency(customer.remaining_balance);
    document.getElementById('propertyValue').textContent = formatCurrency(customer.property_value);
    document.getElementById('creditScore').innerHTML = `<span class="badge ${getCreditScoreBadgeClass(customer.credit_score)}">${customer.credit_score}</span>`;
    document.getElementById('monthlyIncome').textContent = formatCurrency(customer.monthly_income);
    document.getElementById('location').textContent = customer.property_zip ? `${customer.property_zip}, ${customer.property_state || ''}` : 'N/A';

    // Ensure config panel visible and results hidden until run
    document.getElementById('configPanel').classList.remove('hidden');
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('resultsSection').classList.add('hidden');
    document.getElementById('noResultsState').classList.add('hidden');

  } catch (err) {
    showToast(`Failed to load customer: ${err.message}`, 'error');
  }
}

function loadPayloadOptions() {
  const select = document.getElementById('payloadSelect');
  const payloads = getSavedPayloads();

  if (!select) return;

  select.innerHTML = '<option value="">-- Select a Payload Template --</option>' +
    Object.keys(payloads).map(name => `<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`).join('');

  if (Object.keys(payloads).length === 0) {
    select.innerHTML = '<option value="">No payloads available - create one first</option>';
    select.disabled = true;
  } else {
    select.disabled = false;
  }
}

async function loadCachedAnalysis() {
  try {
    const result = await apiCall(`/api/analysis/${cacheKey}/result/${customerKey}`);

    // Update page title
    document.getElementById('customerName').textContent = `Analysis: ${result.customer.name}`;

    // Hide config panel and loading
    document.getElementById('configPanel').classList.add('hidden');
    document.getElementById('loadingState').classList.add('hidden');

    // Display results
    displayAnalysisResults(result);

  } catch (error) {
    showToast(`Error loading analysis: ${error.message}`, 'error');
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('configPanel').classList.remove('hidden');
  }
}

function displayAnalysisResults(data) {
  // Update customer info
  const customer = data.customer;
  document.getElementById('currentPayment').textContent = formatCurrency(customer.current_monthly_payment);
  document.getElementById('remainingBalance').textContent = formatCurrency(customer.remaining_balance);
  document.getElementById('propertyValue').textContent = formatCurrency(customer.property_value);
  document.getElementById('creditScore').innerHTML = `<span class="badge ${getCreditScoreBadgeClass(customer.credit_score)}">${customer.credit_score}</span>`;
  document.getElementById('monthlyIncome').textContent = formatCurrency(customer.monthly_income);
  document.getElementById('location').textContent = customer.property_zip ?
    `${customer.property_zip}, ${customer.property_state || ''}` : 'N/A';

  // Collect all options
  const allOptions = [];

  for (const scenario of data.scenarios || []) {
    for (const product of scenario.products || []) {
      for (const rate of product.rates || []) {
        allOptions.push({
          buydown: scenario.buydown_type,
          product: product.product_name,
          term: product.term_years,
          rate: rate.interest_rate,
          monthlyPayment: rate.monthly_payment,
          monthlySavings: rate.monthly_savings,
          annualSavings: rate.monthly_savings * 12,
          creditCost: rate.credit_cost || 0,
          buydownBreakdown: rate.buydown_breakdown
        });
      }
    }
  }

  if (allOptions.length === 0) {
    document.getElementById('noResultsState').classList.remove('hidden');
    return;
  }

  // Sort by monthly savings (best first)
  allOptions.sort((a, b) => b.monthlySavings - a.monthlySavings);

  // Show results
  document.getElementById('resultsSection').classList.remove('hidden');

  // Display top 3 best options
  const bestOptions = allOptions.slice(0, 3);
  displayBestOptions(bestOptions);

  // Display all scenarios grouped by buydown type
  displayAllScenarios(data.scenarios, customer.current_monthly_payment);
}

function displayBestOptions(options) {
  const grid = document.getElementById('bestOptionsGrid');

  grid.innerHTML = options.map((option, index) => `
    <div class="lead-card" style="border: 2px solid ${index === 0 ? 'var(--success-color)' : 'var(--border-color)'};">
      ${index === 0 ? '<div style="background: var(--success-color); color: white; padding: 0.5rem; text-align: center; font-weight: 600; margin: -1.5rem -1.5rem 1rem; border-radius: var(--border-radius-lg) var(--border-radius-lg) 0 0;">🏆 Best Option</div>' : ''}

      <div class="lead-header">
        <div class="lead-info">
          <h4>${escapeHtml(option.product)}</h4>
          <div class="lead-contact">${option.term} Year ${option.buydown}</div>
        </div>
        <div class="savings-badge">
          ${formatCurrency(option.monthlySavings)}/mo
        </div>
      </div>

      <div class="lead-details">
        <div class="detail-item">
          <div class="detail-label">New Payment</div>
          <div class="detail-value">${formatCurrency(option.monthlyPayment)}</div>
        </div>
        <div class="detail-item">
          <div class="detail-label">Annual Savings</div>
          <div class="detail-value text-success">${formatCurrency(option.annualSavings)}</div>
        </div>
        <div class="detail-item">
          <div class="detail-label">Interest Rate</div>
          <div class="detail-value">${formatPercent(option.rate)}</div>
        </div>
        <div class="detail-item">
          <div class="detail-label">Credit/Cost</div>
          <div class="detail-value ${option.creditCost < 0 ? 'text-success' : ''}">${formatCurrency(option.creditCost)}</div>
        </div>
      </div>

      ${option.buydownBreakdown ? `
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border-color);">
          <div style="font-weight: 600; margin-bottom: 0.5rem; font-size: 0.875rem;">Buydown Details:</div>
          <div style="font-size: 0.75rem; color: var(--text-secondary);">
            ${formatBuydownBreakdown(option.buydownBreakdown)}
          </div>
        </div>
      ` : ''}
    </div>
  `).join('');
}

function displayAllScenarios(scenarios, currentPayment) {
  const container = document.getElementById('scenariosContainer');

  container.innerHTML = scenarios.map(scenario => `
    <div class="form-section" style="margin-bottom: 2rem;">
      <h4>${escapeHtml(scenario.buydown_type)}</h4>

      ${scenario.products && scenario.products.length > 0 ? `
        ${scenario.products.map(product => `
          <div style="margin-bottom: 2rem;">
            <h5 style="color: var(--text-secondary); font-size: 1rem; margin-bottom: 1rem;">
              ${escapeHtml(product.product_name)} - ${product.term_years} Years
            </h5>

            ${product.rates && product.rates.length > 0 ? `
              <div class="data-table-wrapper">
                <div class="data-table-container">
                  <table class="data-table">
                    <thead>
                      <tr>
                        <th>Rate</th>
                        <th>Monthly Payment</th>
                        <th>Monthly Savings</th>
                        <th>Annual Savings</th>
                        <th>Credit/Cost</th>
                      </tr>
                    </thead>
                    <tbody>
                      ${product.rates.map(rate => `
                        <tr>
                          <td><strong>${formatPercent(rate.interest_rate)}</strong></td>
                          <td>${formatCurrency(rate.monthly_payment)}</td>
                          <td class="text-success"><strong>${formatCurrency(rate.monthly_savings)}</strong></td>
                          <td class="text-success">${formatCurrency(rate.monthly_savings * 12)}</td>
                          <td class="${rate.credit_cost < 0 ? 'text-success' : ''}">${formatCurrency(rate.credit_cost || 0)}</td>
                        </tr>
                      `).join('')}
                    </tbody>
                  </table>
                </div>
              </div>
            ` : '<p style="color: var(--text-secondary); padding: 1rem;">No qualifying rates found for this product.</p>'}
          </div>
        `).join('')}
      ` : '<p style="color: var(--text-secondary); padding: 1rem;">No products available for this buydown type.</p>'}
    </div>
  `).join('');
}

function formatBuydownBreakdown(breakdown) {
  if (!breakdown || !breakdown.years) return 'N/A';

  return breakdown.years.map(year =>
    `Year ${year.year}: ${formatPercent(year.rate)} - ${formatCurrency(year.payment)}/mo`
  ).join('<br>');
}

function getCreditScoreBadgeClass(score) {
  if (!score) return 'info';
  if (score >= 750) return 'success';
  if (score >= 670) return 'info';
  if (score >= 580) return 'warning';
  return 'danger';
}

function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}