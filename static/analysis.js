// Customer Analysis Page with cached results

let cacheKey = null;
let customerKey = null;
let customerData = null;
let analysisData = null; // Store the full analysis data
let isFilteredView = true; // Default to filtered view

document.addEventListener('DOMContentLoaded', async () => {
  setupEventListeners();
  await getParametersFromURL();
});

function setupEventListeners() {
  // Back button
  document.getElementById('backBtn').addEventListener('click', () => {
    window.location.href = '/leads.html';
  });

  // Filter toggle button
  const filterToggle = document.getElementById('filterToggle');
  if (filterToggle) {
    filterToggle.addEventListener('click', () => {
      isFilteredView = !isFilteredView;
      updateToggleButton();
      if (analysisData) {
        displayAllScenarios(analysisData.scenarios, analysisData.customer.current_monthly_payment, analysisData.target_amount, isFilteredView);
      }
    });
  }

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

      const payloads = await getSavedPayloads();
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

        if (!resp) {
          throw new Error('Empty response from analysis API');
        }

        if (resp.error) {
          throw new Error(resp.error);
        }

        // Ensure customer is present
        if (!resp.customer) {
          if (resp.customer_data) resp.customer = resp.customer_data;
        }

        analysisData = resp; // Store the full analysis data for filtering
        analysisData.payload = basePayload; // Keep payload for accurate buydown lookups

        // Show results section
        document.getElementById('loadingState').classList.add('hidden');
        document.getElementById('resultsSection').classList.remove('hidden');

        await displayAnalysisResults(resp);

      } catch (err) {
        document.getElementById('loadingState').classList.add('hidden');
        document.getElementById('configPanel').classList.remove('hidden');
        showToast(`Analysis failed: ${err.message}`, 'error');
      }
    });
  }
}

async function getParametersFromURL() {
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
    await loadPayloadOptions();
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

async function loadPayloadOptions() {
  const select = document.getElementById('payloadSelect');
  const payloads = await getSavedPayloads();

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

    analysisData = result; // Store for filtering

    // Display results
    await displayAnalysisResults(result);

  } catch (error) {
    showToast(`Error loading analysis: ${error.message}`, 'error');
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('configPanel').classList.remove('hidden');
  }
}

async function displayAnalysisResults(data) {
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

  // Display summary table with highlighted rows grouped by term
  await displaySummaryTable(data);

  // Update toggle button to show correct state
  updateToggleButton();

  // Display all scenarios grouped by term with filtered view by default
  displayAllScenarios(data.scenarios, customer.current_monthly_payment, data.target_amount, isFilteredView);
}

async function displaySummaryTable(data) {
  const container = document.getElementById('bestOptionsGrid');

  // Helper: compute Year 1 target rate from base rate + buydown type
  function year1TargetRate(baseRate, buydownType) {
    if (buydownType.includes('2-1')) return Math.round((baseRate - 2.0) * 1000) / 1000;
    if (buydownType.includes('1-0')) return Math.round((baseRate - 1.0) * 1000) / 1000;
    return null;
  }

  // Helper: find exact rate match in a product's rate list (within 0.001%)
  function findExactRate(rates, targetRate) {
    if (targetRate === null) return null;
    return rates.find(r => r.interest_rate !== null && Math.abs(r.interest_rate - targetRate) < 0.01) || null;
  }

  // Helper: call /api/buydown/accurate with targetRateValue
  async function fetchAccurateYear1(customerKey, productName, termYears, buydownType, targetRate, payload) {
    try {

      const resp = await fetch('/api/buydown/accurate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          customer_key: customerKey,
          product_name: productName,
          term_years: termYears,
          buydown_type: buydownType,
          target_rate: targetRate,
          payload: payload
        })
      });
      const result = await resp.json();
      if (result && !result.error) return result;
    } catch (e) {
      console.warn('fetchAccurateYear1 failed:', e);
    }
    return null;
  }

  // Show a loading placeholder while we resolve Year 1 data
  container.innerHTML = '<div style="padding: 2rem; text-align: center; color: var(--text-secondary);">Loading Year 1 data...</div>';

  // Build summaryData with Year 1 values resolved
  const summaryData = {};
  const customerKey = data.customer.customer_key;
  const payload = (analysisData && analysisData.payload) ? analysisData.payload : {};

  for (const scenario of data.scenarios || []) {
    const buydownType = scenario.buydown_type;

    for (const product of scenario.products || []) {
      const term = product.term_years;
      const productName = product.product_name;

      const highlightedRate = product.rates?.find(r => r.is_closest_to_target);
      if (!highlightedRate) continue;

      if (!summaryData[term]) summaryData[term] = [];

      // Non-buydown: show as-is
      if (buydownType === 'None') {
        summaryData[term].push({
          buydownType,
          productName,
          rate: highlightedRate.interest_rate,
          payment: highlightedRate.monthly_payment,
          savings: highlightedRate.monthly_savings,
          hasBuydown: false,
          yearLabel: '',
          year1Source: null
        });
        continue;
      }

      // Buydown: resolve Year 1 values
      const baseRate = highlightedRate.interest_rate;
      const targetY1Rate = year1TargetRate(baseRate, buydownType);

      let year1Rate = null, year1Payment = null, year1Savings = null, year1Source = null;

      // Step 1: look for exact match in "All Rates" of this product
      const exactMatch = findExactRate(product.rates, targetY1Rate);
      if (exactMatch) {
        year1Rate = exactMatch.interest_rate;
        year1Payment = exactMatch.monthly_payment;
        year1Savings = exactMatch.monthly_savings;
        year1Source = 'rates';
      }

      // Step 2: if not found, call /api/buydown/accurate with targetRateValue
      if (!year1Rate && targetY1Rate !== null) {
        const accurate = await fetchAccurateYear1(customerKey, productName, term, buydownType, targetY1Rate, payload);
        if (accurate) {
          year1Rate = accurate.rate;
          year1Payment = accurate.payment;
          year1Savings = accurate.savings;
          year1Source = 'api';
        }
      }

      summaryData[term].push({
        buydownType,
        productName,
        rate: year1Rate !== null ? year1Rate : (targetY1Rate || baseRate),
        payment: year1Payment,
        savings: year1Savings,
        hasBuydown: true,
        yearLabel: 'Year 1',
        year1Source,
        baseRate
      });
    }
  }

  // Sort terms ascending
  const sortedTerms = Object.keys(summaryData).sort((a, b) => parseInt(a) - parseInt(b));

  // Render tables
  container.innerHTML = sortedTerms.map(term => `
    <div class="form-section" style="margin-bottom: 2rem;">
      <h4 style="margin-bottom: 0.5rem; color: var(--text-primary);">${term} Year Term - Summary</h4>
      <p style="margin-bottom: 1rem; color: var(--text-secondary); font-size: 0.875rem;">
        ${summaryData[term].some(item => item.hasBuydown) ? '<span style="color: #10b981;">✓ Buydowns show Year 1 values</span>' : ''}
      </p>

      <div class="data-table-wrapper">
        <div class="data-table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Buydown Type</th>
                <th>Product Name</th>
                <th>Rate</th>
                <th>Payment</th>
                <th>Savings</th>
              </tr>
            </thead>
            <tbody>
              ${summaryData[term].map((item, idx) => `
                <tr style="${idx % 2 === 0 ? 'background-color: #f9fafb;' : ''}">
                  <td><strong>${escapeHtml(item.buydownType)}</strong></td>
                  <td>${escapeHtml(item.productName)}</td>
                  <td>
                    <strong>${item.rate !== null ? formatPercent(item.rate) : 'N/A'}</strong>
                    ${item.yearLabel ? `<div style="font-size: 0.75rem; color: #10b981; margin-top: 0.25rem;">${item.yearLabel}</div>` : ''}
                  </td>
                  <td>
                    ${item.payment !== null && item.payment !== undefined ? formatCurrency(item.payment) : 'N/A'}
                    ${item.yearLabel ? `<div style="font-size: 0.75rem; color: #10b981; margin-top: 0.25rem;">${item.yearLabel}</div>` : ''}
                  </td>
                  <td class="text-success">
                    <strong>${item.savings !== null && item.savings !== undefined ? formatCurrency(item.savings) : 'N/A'}</strong>
                    ${item.yearLabel ? `<div style="font-size: 0.75rem; color: #10b981; margin-top: 0.25rem;">${item.yearLabel}</div>` : ''}
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>

      ${summaryData[term].some(item => item.hasBuydown && item.year1Source) ? `
        <div style="margin-top: 1rem; padding: 0.75rem; background: #dcfce7; border-left: 3px solid #10b981; font-size: 0.85rem; color: var(--text-secondary);">
          <strong>✓ Note:</strong> For buydown products, rates, payments and savings shown are <strong>Year 1 values</strong>.
          Expand "All Available Options" below to see the full year-by-year breakdown.
        </div>
      ` : ''}
    </div>
  `).join('');
}

function displayBestOptions(options) {
  // Legacy function - kept for backward compatibility
  // Now redirects to displaySummaryTable
  console.warn('displayBestOptions is deprecated, use displaySummaryTable instead');
}

function displayAllScenarios(scenarios, currentPayment, targetAmount, applyFilter) {
  const container = document.getElementById('scenariosContainer');

  // First, collect all unique buydown types dynamically
  const allBuydownTypes = [...new Set(scenarios.map(s => s.buydown_type))];

  // Sort buydown types for consistent ordering (None first, then alphabetically)
  allBuydownTypes.sort((a, b) => {
    if (a === 'None') return -1;
    if (b === 'None') return 1;
    return a.localeCompare(b);
  });

  // Collect all unique term/product combinations across all buydown types
  const termGroups = {};

  scenarios.forEach(scenario => {
    const buydownType = scenario.buydown_type;

    if (scenario.products && scenario.products.length > 0) {
      scenario.products.forEach(product => {
        const term = product.term_years;

        if (!termGroups[term]) {
          termGroups[term] = {
            term: term,
            buydownTypes: {}
          };
          // Initialize all buydown types with empty arrays
          allBuydownTypes.forEach(bt => {
            termGroups[term].buydownTypes[bt] = [];
          });
        }

        // Apply filtering if enabled
        let ratesToDisplay = product.rates || [];

        if (applyFilter && ratesToDisplay.length > 0 && targetAmount !== undefined) {
          const validRates = ratesToDisplay.filter(r =>
            r.credit_cost !== null && r.credit_cost !== undefined && r.interest_rate !== null && r.interest_rate !== undefined
          );

          if (validRates.length > 0) {
            const closestRate = validRates.reduce((closest, rate) => {
              const closestDiff = Math.abs(closest.credit_cost - targetAmount);
              const rateDiff = Math.abs(rate.credit_cost - targetAmount);
              return rateDiff < closestDiff ? rate : closest;
            });

            const sortedRates = [...validRates].sort((a, b) => a.interest_rate - b.interest_rate);
            const closestIndex = sortedRates.findIndex(r =>
              r.interest_rate === closestRate.interest_rate &&
              r.credit_cost === closestRate.credit_cost
            );

            if (closestIndex !== -1) {
              const startIndex = Math.max(0, closestIndex - 3);
              const endIndex = Math.min(sortedRates.length, closestIndex + 3);
              ratesToDisplay = sortedRates.slice(startIndex, endIndex);
            }
          }
        }

        termGroups[term].buydownTypes[buydownType].push({
          productName: product.product_name,
          productAlias: product.product_alias,
          rates: ratesToDisplay
        });
      });
    }
  });

  // Sort terms ascending
  const sortedTerms = Object.keys(termGroups).sort((a, b) => parseInt(a) - parseInt(b));

  container.innerHTML = sortedTerms.map(term => {
    const group = termGroups[term];

    // Find the maximum number of products in any buydown type
    const maxProducts = Math.max(
      ...allBuydownTypes.map(bt => group.buydownTypes[bt].length),
      1 // Ensure at least 1 row
    );

    // Create rows - each row will have N columns (one per buydown type)
    const rows = [];
    for (let i = 0; i < maxProducts; i++) {
      rows.push(i);
    }

    return `
      <div class="form-section" style="margin-bottom: 3rem;">
        <h4 style="margin-bottom: 1.5rem;">
          ${term} Year Term
          ${applyFilter ? ' <span style="color: var(--primary-color); font-size: 0.875rem; font-weight: 400;">(Filtered View)</span>' : ''}
          <span style="color: var(--text-secondary); font-size: 0.875rem; font-weight: 400; margin-left: 1rem;">
            (${allBuydownTypes.length} buydown type${allBuydownTypes.length !== 1 ? 's' : ''})
          </span>
        </h4>

        ${rows.map(rowIndex => {
          return `
            <div style="display: grid; grid-template-columns: repeat(${allBuydownTypes.length}, 1fr); gap: 1.5rem; align-items: start; margin-bottom: 1.5rem;">
              ${allBuydownTypes.map(buydownType => {
                const products = group.buydownTypes[buydownType];

                // Get the product for this row - if the buydown type has fewer products than maxProducts,
                // repeat the last available product
                let product = null;
                let isRepeated = false;

                if (products.length === 0) {
                  // No products at all for this buydown type
                  product = null;
                } else if (rowIndex < products.length) {
                  // Normal case: we have a product at this index
                  product = products[rowIndex];

                  // Check if this same product appeared earlier in this buydown type
                  if (rowIndex > 0) {
                    for (let j = 0; j < rowIndex; j++) {
                      if (products[j] && products[j].productName === product.productName) {
                        isRepeated = true;
                        break;
                      }
                    }
                  }
                } else {
                  // This buydown type has fewer products than maxProducts
                  // Repeat the last available product for comparison
                  product = products[products.length - 1];
                  isRepeated = true; // It's definitely a repeat since we're beyond the original array
                }

                if (!product || !product.rates || product.rates.length === 0) {
                  return `
                    <div style="
                      border: 1px dashed var(--border-color);
                      border-radius: var(--border-radius-lg);
                      padding: 2rem 1.5rem;
                      background: var(--background-secondary);
                      text-align: center;
                      min-height: 200px;
                      display: flex;
                      flex-direction: column;
                      justify-content: center;
                      min-width: 0;
                    ">
                      <h5 style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 0.5rem; word-wrap: break-word;">
                        ${escapeHtml(buydownType)}
                      </h5>
                      <p style="color: var(--text-secondary); font-size: 0.875rem; margin: 0;">
                        ${product ? 'No qualifying rates' : 'No product'}
                      </p>
                    </div>
                  `;
                }

                return `
                  <div style="
                    border: 2px solid ${isRepeated ? '#f59e0b' : 'var(--border-color)'};
                    border-radius: var(--border-radius-lg);
                    padding: 0;
                    background: white;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    display: flex;
                    flex-direction: column;
                    height: 100%;
                    ${isRepeated ? 'opacity: 0.85;' : ''}
                    min-width: 0;
                  ">
                    ${isRepeated ? `
                      <div style="
                        background: #f59e0b;
                        color: white;
                        padding: 0.25rem 0.75rem;
                        font-size: 0.75rem;
                        font-weight: 600;
                        text-align: center;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                      ">
                        🔄 Repeated for Comparison
                      </div>
                    ` : ''}

                    <div style="
                      background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
                      color: white;
                      padding: 1rem 1.5rem;
                      border-radius: ${isRepeated ? '0' : 'var(--border-radius-lg) var(--border-radius-lg)'} 0 0;
                      font-weight: 600;
                      font-size: 0.95rem;
                      word-wrap: break-word;
                      overflow-wrap: break-word;
                    ">
                      ${escapeHtml(buydownType)}
                    </div>

                    <div style="
                      background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
                      padding: 0.75rem 1.5rem;
                      border-bottom: 2px solid var(--border-color);
                      font-weight: 600;
                      font-size: 0.9rem;
                      color: var(--text-primary);
                      word-wrap: break-word;
                      overflow-wrap: break-word;
                    ">
                      ${escapeHtml(product.productName)}
                    </div>

                    <div style="padding: 1.5rem; flex: 1;">
                      <div style="overflow-x: auto;">
                        <table style="width: 100%; font-size: 0.85rem; border-collapse: collapse;">
                          <thead>
                            <tr style="border-bottom: 2px solid var(--border-color);">
                              <th style="text-align: left; padding: 0.5rem 0.25rem; font-weight: 600; color: var(--text-secondary); font-size: 0.8rem;">Rate</th>
                              <th style="text-align: right; padding: 0.5rem 0.25rem; font-weight: 600; color: var(--text-secondary); font-size: 0.8rem;">Payment</th>
                              <th style="text-align: right; padding: 0.5rem 0.25rem; font-weight: 600; color: var(--text-secondary); font-size: 0.8rem;">Savings</th>
                              <th style="text-align: right; padding: 0.5rem 0.25rem; font-weight: 600; color: var(--text-secondary); font-size: 0.8rem;">Cost</th>
                              ${buydownType !== 'None' ? '<th style="text-align: center; padding: 0.5rem 0.25rem; font-weight: 600; color: var(--text-secondary); font-size: 0.8rem;"></th>' : ''}
                            </tr>
                          </thead>
                          <tbody>
                            ${product.rates.map((rate, idx) => {
                              const hasBreakdown = rate.buydown_breakdown && rate.buydown_breakdown.year1;
                              const rowId = `rate-${term}-${buydownType.replace(/\s+/g, '-')}-${idx}`;

                              return `
                              <tr style="
                                border-bottom: 1px solid var(--border-color);
                                ${rate.is_closest_to_target ? 'background-color: #fff3cd;' : ''}
                                ${!rate.is_closest_to_target && idx % 2 === 0 ? 'background-color: #f9fafb;' : ''}
                              ">
                                <td style="padding: 0.75rem 0.25rem; font-weight: 600; font-size: 0.85rem;">
                                  ${formatPercent(rate.interest_rate)}
                                  ${rate.is_closest_to_target ? ' ⭐' : ''}
                                </td>
                                <td style="padding: 0.75rem 0.25rem; text-align: right; font-size: 0.85rem;">
                                  ${formatCurrency(rate.monthly_payment)}
                                </td>
                                <td style="padding: 0.75rem 0.25rem; text-align: right; color: var(--success-color); font-weight: 600; font-size: 0.85rem;">
                                  ${formatCurrency(rate.monthly_savings)}
                                </td>
                                <td style="padding: 0.75rem 0.25rem; text-align: right; font-size: 0.85rem; ${rate.credit_cost < 0 ? 'color: var(--success-color); font-weight: 600;' : ''}">
                                  ${formatCurrency(rate.credit_cost || 0)}
                                </td>
                                ${buydownType !== 'None' && hasBreakdown ? `
                                  <td style="padding: 0.75rem 0.25rem; text-align: center;">
                                    <button
                                      onclick="toggleBuydownDetails('${rowId}')"
                                      style="
                                        background: none;
                                        border: 1px solid var(--primary-color);
                                        color: var(--primary-color);
                                        border-radius: 4px;
                                        padding: 0.25rem 0.5rem;
                                        cursor: pointer;
                                        font-size: 0.75rem;
                                        font-weight: 600;
                                      "
                                    >
                                      Years ▼
                                    </button>
                                  </td>
                                ` : buydownType !== 'None' ? '<td></td>' : ''}
                              </tr>
                              ${hasBreakdown ? `
                                <tr id="${rowId}" style="display: none;">
                                  <td colspan="${buydownType !== 'None' ? '5' : '4'}" style="padding: 0; border-bottom: 2px solid var(--border-color);">
                                    <div style="background: linear-gradient(to bottom, #f9fafb, #ffffff); padding: 1rem 1.5rem;">
                                      <div style="font-weight: 600; margin-bottom: 0.75rem; color: var(--text-primary); font-size: 0.9rem;">
                                        📊 Buydown Schedule - Actual Rates from API
                                      </div>
                                      <table style="width: 100%; font-size: 0.85rem; border-collapse: collapse; background: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                                        <thead>
                                          <tr style="background: linear-gradient(135deg, #667eea, #764ba2); color: white;">
                                            <th style="text-align: left; padding: 0.75rem; font-weight: 600;">Period</th>
                                            <th style="text-align: right; padding: 0.75rem; font-weight: 600;">Rate</th>
                                            <th style="text-align: right; padding: 0.75rem; font-weight: 600;">Payment</th>
                                            <th style="text-align: right; padding: 0.75rem; font-weight: 600;">Savings</th>
                                            <th style="text-align: right; padding: 0.75rem; font-weight: 600;">Cost</th>
                                          </tr>
                                        </thead>
                                        <tbody>
                                          <tr style="background: #fef3c7; border-bottom: 2px solid var(--border-color);">
                                            <td style="padding: 0.75rem; font-weight: 600;">
                                              Actual (Year 3+)
                                              <div style="font-size: 0.75rem; font-weight: 400; color: var(--text-secondary); margin-top: 0.25rem;">
                                                ${rate.buydown_breakdown.actual?.note || ''}
                                              </div>
                                            </td>
                                            <td style="padding: 0.75rem; text-align: right; font-weight: 600;">${formatPercent(rate.interest_rate)}</td>
                                            <td style="padding: 0.75rem; text-align: right; font-weight: 600;">${formatCurrency(rate.monthly_payment)}</td>
                                            <td style="padding: 0.75rem; text-align: right; color: var(--success-color); font-weight: 600;">${formatCurrency(rate.monthly_savings)}</td>
                                            <td style="padding: 0.75rem; text-align: right; font-weight: 600;">${formatCurrency(rate.credit_cost || 0)}</td>
                                          </tr>
                                          ${rate.buydown_breakdown.year1 ? `
                                            <tr style="background: ${!rate.buydown_breakdown.year1.is_exact ? '#fef3c7' : '#dcfce7'}; border-top: 2px solid var(--border-color);">
                                              <td style="padding: 0.75rem;">
                                                <div style="font-weight: 600;">Year 1</div>
                                                <div style="font-size: 0.75rem; color: ${!rate.buydown_breakdown.year1.is_exact ? '#f59e0b' : 'var(--text-secondary)'}; margin-top: 0.25rem;">
                                                  ${!rate.buydown_breakdown.year1.is_exact ? '⚠️ ' : ''}${rate.buydown_breakdown.year1.note}
                                                </div>
                                              </td>
                                              <td style="padding: 0.75rem; text-align: right; font-weight: 600;">${formatPercent(rate.buydown_breakdown.year1.rate)}</td>
                                              <td style="padding: 0.75rem; text-align: right; font-weight: 600;">${formatCurrency(rate.buydown_breakdown.year1.payment)}</td>
                                              <td style="padding: 0.75rem; text-align: right; color: var(--success-color); font-weight: 600;">${formatCurrency(rate.buydown_breakdown.year1.savings)}</td>
                                              <td style="padding: 0.75rem; text-align: right; font-weight: 600;">${formatCurrency(rate.buydown_breakdown.year1.credit_cost || 0)}</td>
                                            </tr>
                                          ` : ''}
                                          ${rate.buydown_breakdown.year2 && rate.buydown_breakdown.year2.rate !== rate.interest_rate ? `
                                            <tr style="background: ${!rate.buydown_breakdown.year2.is_exact ? '#fef3c7' : '#dbeafe'};">
                                              <td style="padding: 0.75rem;">
                                                <div style="font-weight: 600;">Year 2</div>
                                                <div style="font-size: 0.75rem; color: ${!rate.buydown_breakdown.year2.is_exact ? '#f59e0b' : 'var(--text-secondary)'}; margin-top: 0.25rem;">
                                                  ${!rate.buydown_breakdown.year2.is_exact ? '⚠️ ' : ''}${rate.buydown_breakdown.year2.note}
                                                </div>
                                              </td>
                                              <td style="padding: 0.75rem; text-align: right; font-weight: 600;">${formatPercent(rate.buydown_breakdown.year2.rate)}</td>
                                              <td style="padding: 0.75rem; text-align: right; font-weight: 600;">${formatCurrency(rate.buydown_breakdown.year2.payment)}</td>
                                              <td style="padding: 0.75rem; text-align: right; color: var(--success-color); font-weight: 600;">${formatCurrency(rate.buydown_breakdown.year2.savings)}</td>
                                              <td style="padding: 0.75rem; text-align: right; font-weight: 600;">${formatCurrency(rate.buydown_breakdown.year2.credit_cost || 0)}</td>
                                            </tr>
                                          ` : ''}
                                        </tbody>
                                      </table>
                                      <div style="margin-top: 0.75rem; padding: 0.5rem; background: #eff6ff; border-left: 3px solid #3b82f6; font-size: 0.8rem; color: var(--text-secondary);">
                                        <strong>Note:</strong> Rates and payments are pulled from actual API responses for each buydown scenario.
                                      </div>
                                    </div>
                                  </td>
                                </tr>
                              ` : ''}
                            `;
                            }).join('')}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          `;
        }).join('')}
      </div>
    `;
  }).join('');
}

function formatBuydownBreakdown(breakdown) {
  if (!breakdown) return 'N/A';

  // Handle new structure with year1, year2, actual
  if (breakdown.year1) {
    let result = `Year 1: ${formatPercent(breakdown.year1.rate)} - ${formatCurrency(breakdown.year1.payment)}/mo`;
    if (breakdown.year2 && breakdown.year2.rate !== breakdown.actual?.rate) {
      result += `<br>Year 2: ${formatPercent(breakdown.year2.rate)} - ${formatCurrency(breakdown.year2.payment)}/mo`;
    }
    return result;
  }

  // Handle old structure with years array (fallback)
  if (breakdown.years) {
    return breakdown.years.map(year =>
      `Year ${year.year}: ${formatPercent(year.rate)} - ${formatCurrency(year.payment)}/mo`
    ).join('<br>');
  }

  return 'N/A';
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

function updateToggleButton() {
  const filterToggle = document.getElementById('filterToggle');
  if (!filterToggle) return;

  // Update the button text and style based on the current state
  if (isFilteredView) {
    filterToggle.textContent = 'Switch to All Rates View';
    filterToggle.classList.remove('btn-outline-primary');
    filterToggle.classList.add('btn-primary');
  } else {
    filterToggle.textContent = 'Switch to Filtered View';
    filterToggle.classList.remove('btn-primary');
    filterToggle.classList.add('btn-outline-primary');
  }
}

function toggleBuydownDetails(rowId) {
  const detailRow = document.getElementById(rowId);
  if (detailRow) {
    const isHidden = detailRow.style.display === 'none';
    detailRow.style.display = isHidden ? 'table-row' : 'none';

    // Update button text
    const button = event.target;
    if (button) {
      button.innerHTML = isHidden ? 'Years ▲' : 'Years ▼';
    }
  }
}

window.getAccurateBuydown = async function(button, customerKey, productName, termYears, buydownType, rate, payment, savings, cost) {
  button.disabled = true;
  button.textContent = 'Loading...';
  try {
    // Estimate buydown percent from buydownType (e.g., '2-1 LLPA' => 2)
    // Use the current payload from analysisData
    const payload = analysisData ? analysisData.payload : {};
    const resp = await fetch('/api/buydown/accurate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        customer_key: customerKey,
        product_name: productName,
        term_years: termYears,
        buydown_type: buydownType,
        target_rate: parseFloat(rate),
        payload: payload
      })
    });
    const result = await resp.json();
    if (result && result.is_exact) {
      // Update the row with accurate values
      button.parentElement.querySelector('strong').textContent = formatPercent(result.rate);
      button.parentElement.parentElement.querySelectorAll('td')[3].innerHTML = formatCurrency(result.payment) + `<div style="font-size: 0.75rem; color: #10b981; margin-top: 0.25rem;">Year 1</div>`;
      button.parentElement.parentElement.querySelectorAll('td')[4].innerHTML = `<strong>${formatCurrency(result.savings)}</strong><div style="font-size: 0.75rem; color: #10b981; margin-top: 0.25rem;">Year 1</div>`;
      button.remove();
    } else {
      button.textContent = 'No Accurate Data';
    }
  } catch (err) {
    button.textContent = 'Error';
  }
};