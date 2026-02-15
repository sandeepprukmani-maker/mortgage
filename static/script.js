document.addEventListener('DOMContentLoaded', () => {
  // ============================================================
  // ✅ NEW: Full-page analysis mode (no more rendering in modal)
  // ============================================================
  const ANALYSIS_STORAGE_KEY = 'analysisResultV1';
  const LEADGEN_STATE_KEY = 'leadGenStateV1';

  function saveLeadGenStateToSession() {
    try {
      const payload = {
        allCustomersData: allCustomersData || [],
        qualifiedCustomersData: qualifiedCustomersData || [],
        customerAnalysisCache: window.customerAnalysisCache || {},
        currentLeadGenFilters: currentLeadGenFilters || {}
      };
      sessionStorage.setItem(LEADGEN_STATE_KEY, JSON.stringify(payload));
      console.debug('[leadgen] saved state to sessionStorage', { count: (qualifiedCustomersData || []).length });
    } catch (e) {
      console.warn('Could not save leadgen state to sessionStorage', e);
    }
  }

  function restoreLeadGenStateFromSession() {
    try {
      const raw = sessionStorage.getItem(LEADGEN_STATE_KEY);
      console.debug('[leadgen] attempting restore from sessionStorage', { present: !!raw });
      if (!raw) return false;
      const st = JSON.parse(raw);
      if (!st) return false;

      // Restore globals used by lead-gen
      allCustomersData = Array.isArray(st.allCustomersData) ? st.allCustomersData : [];
      qualifiedCustomersData = Array.isArray(st.qualifiedCustomersData) ? st.qualifiedCustomersData : [];
      window.customerAnalysisCache = (st.customerAnalysisCache && typeof st.customerAnalysisCache === 'object') ? st.customerAnalysisCache : {};
      currentLeadGenFilters = st.currentLeadGenFilters || {};

      // Render UI if we have qualified results
      const leadCount = document.getElementById('leadCount');
      const results = document.getElementById('leadGenResults');
      const tbody = document.getElementById('leadGenTableBody');
      if (results && tbody) {
        // Build rows for qualified customers — skip invalid entries
        const validQualified = (Array.isArray(qualifiedCustomersData) ? qualifiedCustomersData : []).filter(c => c && (c.customer_key || c.name || c.email || c.phone));

        tbody.innerHTML = validQualified.map(customer => `
          <tr class="customer-row" data-customer-key="${customer.customer_key}" style="transition: background-color 0.3s ease; opacity: 1;">
            <td>${customer.name}</td>
            <td>${customer.phone || 'N/A'}</td>
            <td>${customer.email || 'N/A'}</td>
            <td>$${(customer.current_monthly_payment || 0).toLocaleString()}</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td>
              <button class="btn-sm" onclick="viewQualifiedCustomerDetails('${customer.customer_key}')" style="background: #10b981; color: white; font-weight: bold;">✓ View Details</button>
            </td>
          </tr>
        `).join('');

        if (leadCount) leadCount.textContent = `${qualifiedCustomersData.length} Qualified`;
        results.classList.remove('hidden');
        console.debug('[leadgen] restored UI for qualified results', { qualified: qualifiedCustomersData.length });

        // Ensure lead-gen tab/section is active so the user sees results after returning
        try {
          const leadBtn = document.querySelector('.tab-btn[data-tab="leadGen"]');
          if (leadBtn) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            leadBtn.classList.add('active');
            const leadSection = document.getElementById('leadGenSection');
            if (leadSection) leadSection.classList.add('active');
          }
        } catch (e) {
          // ignore
        }
      }

      // Clean up the saved state now that it's restored (avoid stale data on future navigations)
      sessionStorage.removeItem(LEADGEN_STATE_KEY);
      console.debug('[leadgen] removed saved leadgen state from sessionStorage after restore');
      return true;
    } catch (e) {
      console.warn('Could not restore leadgen state from sessionStorage', e);
      return false;
    }
  }

  function openAnalysisPage({ title, data }) {
    // Before navigating to analysis page, persist lead-gen state (so results survive back navigation)
    try {
      // Only save lead-gen state if the leadGenResults container exists (we're on the lead-gen screen)
      const leadGenEl = document.getElementById('leadGenResults');
      if (leadGenEl) saveLeadGenStateToSession();
    } catch (e) {
      // ignore
    }

    // store payload for analysis page
    sessionStorage.setItem(ANALYSIS_STORAGE_KEY, JSON.stringify({
      title,
      data,
      fromUrl: window.location.pathname + window.location.search + window.location.hash
    }));
    console.debug('[leadgen] navigating to analysis page; analysis payload saved');

    // go to analysis page
    window.location.href = '/analysis.html';
  }

  // If we are on analysis.html, render the stored analysis and stop
  const analysisBodyEl = document.getElementById('analysisBody');
  if (analysisBodyEl) {
    const backBtn = document.getElementById('backBtn');
    if (backBtn) {
      backBtn.addEventListener('click', () => {
        const stored = sessionStorage.getItem(ANALYSIS_STORAGE_KEY);
        if (stored) {
          try {
            const parsed = JSON.parse(stored);
            if (parsed && parsed.fromUrl) {
              window.location.href = parsed.fromUrl;
              return;
            }
          } catch (_) {}
        }
        window.history.back();
      });
    }

    const stored = sessionStorage.getItem(ANALYSIS_STORAGE_KEY);
    if (!stored) {
      analysisBodyEl.innerHTML = `<div class="error">No analysis data found. Please go back and run analysis again.</div>`;
      return;
    }

    let payload;
    try {
      payload = JSON.parse(stored);
    } catch (e) {
      analysisBodyEl.innerHTML = `<div class="error">Corrupted analysis data. Please go back and run analysis again.</div>`;
      return;
    }

    // Set title if the page has these elements
    const titleEl = document.getElementById('analysisCustomerName');
    if (titleEl && payload?.title) titleEl.textContent = payload.title;

    // Render analysis into analysisBody
    displayDetailedAnalysis(payload.data, analysisBodyEl);

    return; // ✅ important: do not run rest of app JS on analysis page
  }

  // ============================================================
  // Existing app page logic starts here
  // ============================================================

  // Tab switching
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(`${btn.dataset.tab}Section`).classList.add('active');

      if (btn.dataset.tab === 'leadGen') {
        loadSavedPayloads();
      } else if (btn.dataset.tab === 'builder') {
        loadSavedPayloads();
      } else if (btn.dataset.tab === 'customers') {
        loadCustomers();
      }
    });
  });

  // ===== PAYLOAD MANAGEMENT =====
  function loadSavedPayloads() {
    const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
    const options = '<option value="">-- Select a Payload --</option>' +
      Object.keys(saved).map(name => `<option value="${name}">${name}</option>`).join('');

    const lgSel = document.getElementById('lgPayloadSelect');
    const bSel = document.getElementById('payloadSelect');
    if (lgSel) lgSel.innerHTML = options;
    if (bSel) bSel.innerHTML = options;
  }

  // ===== SCREEN 1: LEAD GENERATION =====
  const leadGenForm = document.getElementById('leadGenForm');
  let currentLeadGenFilters = {};
  let allCustomersData = [];
  let viewedCustomers = new Set(); // ✅ Track which customers have been VIEWED
  let qualifiedCustomersData = []; // ✅ Only store qualified customers
  let analysisInProgress = new Map(); // ✅ Track which customers are being analyzed

  if (leadGenForm) {
    leadGenForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const payloadName = document.getElementById('lgPayloadSelect').value;
      if (!payloadName) {
        alert('Please select a payload template');
        return;
      }

      const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
      const payload = saved[payloadName];
      if (!payload) {
        alert('Payload not found');
        return;
      }

      const minSavings = parseFloat(document.getElementById('lgMinSavings').value);
      const targetAmount = parseFloat(document.getElementById('lgTargetAmount').value);

      // Store filters
      currentLeadGenFilters = {
        payload: payload,
        min_savings: minSavings,
        target_amount: targetAmount,
        payloadName: payloadName
      };

      // Reset tracking
      viewedCustomers.clear();
      qualifiedCustomersData = [];
      analysisInProgress.clear();

      showLoader();

      try {
        // Load all customers
        const response = await fetch('/api/customers');
        allCustomersData = await response.json();

        // ✅ Show initial table with "Analyzing..." status and START background analysis
        displayInitialLeadsTable(allCustomersData);
        hideLoader();

        // ✅ Start analyzing in background WITHOUT waiting
        startBackgroundAnalysisWithLiveUpdates(allCustomersData);

      } catch (error) {
        alert('Error: ' + error.message);
        hideLoader();
      }
    });
  }

  // ✅ NEW: Display initial table immediately
  function displayInitialLeadsTable(customers) {
    const leadCount = document.getElementById('leadCount');
    const results = document.getElementById('leadGenResults');
    const tbody = document.getElementById('leadGenTableBody');
    if (!tbody) return;

    if (leadCount) leadCount.textContent = `Analyzing (${qualifiedCustomersData.length})`;
    if (results) results.classList.remove('hidden');

    // Filter out any invalid/empty customer objects that may appear during fetch/restore
    const validCustomers = (Array.isArray(customers) ? customers : []).filter(c => {
      if (!c) return false;
      // Accept if it has an id/key or at least one meaningful contact field
      return Boolean(c.customer_key || c.customerId || c.name || c.email || c.phone);
    });

    tbody.innerHTML = validCustomers.map(customer => `
      <tr class="customer-row" data-customer-key="${customer.customer_key}" style="transition: background-color 0.3s ease; opacity: 0.6;">
        <td>${customer.name}</td>
        <td>${customer.phone || 'N/A'}</td>
        <td>${customer.email || 'N/A'}</td>
        <td>$${(customer.current_monthly_payment || 0).toLocaleString()}</td>
        <td colspan="6" style="text-align: center; color: #6b7280; font-style: italic;">Analyzing...</td>
      </tr>
    `).join('');
  }

  // ✅ NEW: Background analysis with live updates
  async function startBackgroundAnalysisWithLiveUpdates(customers) {
    if (!window.customerAnalysisCache) {
      window.customerAnalysisCache = {};
    }

    // Ensure we only analyze valid customers to avoid phantom placeholder rows
    const validCustomers = (Array.isArray(customers) ? customers : []).filter(isValidCustomer);
    if (!validCustomers.length) {
      console.debug('[leadgen] no valid customers to analyze');
      return;
    }

    for (const customer of validCustomers) {
      // Mark as analyzing
      analysisInProgress.set(customer.customer_key, true);
      updateCustomerRowUI(customer.customer_key, 'analyzing', customer);

      try {
        const response = await fetch(`/api/customers/${customer.customer_key}/analyze`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            payload: currentLeadGenFilters.payload,
            min_savings: currentLeadGenFilters.min_savings,
            target_amount: currentLeadGenFilters.target_amount
          })
        });

        if (!response.ok) {
          console.warn(`Analysis failed for ${customer.name}`);
          analysisInProgress.delete(customer.customer_key);
          updateCustomerRowUI(customer.customer_key, 'failed', customer);
          continue;
        }

        const data = await response.json();
        window.customerAnalysisCache[customer.customer_key] = data;

        // ✅ Check if customer qualifies
        const hasQualifyingProduct = data.has_qualifying_product ||
          (data.results && data.results.some(buydownGroup => {
            return buydownGroup.products && buydownGroup.products.some(product => {
              return product.rates && product.rates.some(rate => rate.qualifying === true);
            });
          }));

        if (hasQualifyingProduct) {
          qualifiedCustomersData.push({
            ...customer,
            analysisData: data
          });
        }

        // ✅ Mark as complete and update UI
        analysisInProgress.delete(customer.customer_key);

        if (hasQualifyingProduct) {
          updateCustomerRowUI(customer.customer_key, 'qualified', customer);
        } else {
          updateCustomerRowUI(customer.customer_key, 'not-qualified', customer);
        }

        // Update count
        const leadCount = document.getElementById('leadCount');
        if (leadCount) {
          const pending = allCustomersData.length - qualifiedCustomersData.length -
                         (allCustomersData.length - analysisInProgress.size - qualifiedCustomersData.length);
          leadCount.textContent = `${qualifiedCustomersData.length} Qualified`;
        }

      } catch (error) {
        console.error(`Error analyzing ${customer.name}:`, error);
        analysisInProgress.delete(customer.customer_key);
        updateCustomerRowUI(customer.customer_key, 'error', customer);
      }

      // Small delay to avoid overwhelming server
      await new Promise(resolve => setTimeout(resolve, 200));
    }

    // ✅ Final display when all done
    setTimeout(() => {
      displayFinalQualifiedLeads();
    }, 500);
  }

  // Helper: validate customer object
  function isValidCustomer(c) {
    if (!c || typeof c !== 'object') return false;
    // Must have a business key and at least one identifier (name / email / phone)
    if (!c.customer_key) return false;
    if (c.name || c.email || c.phone) return true;
    return false;
  }

  // ✅ NEW: Update row UI based on analysis status
  function updateCustomerRowUI(customerKey, status, customer = null) {
    let row = document.querySelector(`tr[data-customer-key="${customerKey}"]`);
    // If row doesn't exist, only create it when we have a valid customer object
    if (!row) {
      if (!customer || !isValidCustomer(customer)) {
        // Nothing to render — avoid creating a placeholder row
        console.debug('[leadgen] skip updating row; missing DOM row and no valid customer data', { customerKey });
        return;
      }

      const tbody = document.getElementById('leadGenTableBody');
      if (!tbody) return;
      const tr = document.createElement('tr');
      tr.className = 'customer-row';
      tr.dataset.customerKey = customerKey;
      tbody.appendChild(tr);
      // assign the created row back to the variable so subsequent updates use it
      row = tr;
      // Use the created row for further updates
      // Note: continue so the switch below will run and populate content
    }

    const tbody = document.getElementById('leadGenTableBody');
    const btn = row ? row.querySelector('button') : document.createElement('button');

    switch (status) {
      case 'analyzing':
        row.style.opacity = '0.6';
        row.style.backgroundColor = 'white';
        row.innerHTML = `
          <td>${customer?.name || ''}</td>
          <td>${customer?.phone || 'N/A'}</td>
          <td>${customer?.email || 'N/A'}</td>
          <td>$${(customer?.current_monthly_payment || 0).toLocaleString()}</td>
          <td colspan="6" style="text-align: center; color: #6b7280; font-style: italic;">
            <span style="display: inline-block; animation: spin 1s linear infinite; margin-right: 5px;">⌛</span>
            Analyzing...
          </td>
        `;
        break;

      case 'qualified':
        row.style.opacity = '1';
        row.style.backgroundColor = 'white';
        row.innerHTML = `
          <td>${customer?.name || ''}</td>
          <td>${customer?.phone || 'N/A'}</td>
          <td>${customer?.email || 'N/A'}</td>
          <td>$${(customer?.current_monthly_payment || 0).toLocaleString()}</td>
          <td>-</td>
          <td>-</td>
          <td>-</td>
          <td>-</td>
          <td>-</td>
          <td>-</td>
          <td>
            <button class="btn-sm" onclick="viewQualifiedCustomerDetails('${customerKey}')" style="background: #10b981; color: white; font-weight: bold;">✓ View Details</button>
          </td>
        `;
        break;

      case 'not-qualified':
        row.style.opacity = '0.5';
        row.style.backgroundColor = '#f3f4f6';
        row.innerHTML = `
          <td>${customer?.name || ''}</td>
          <td>${customer?.phone || 'N/A'}</td>
          <td>${customer?.email || 'N/A'}</td>
          <td>$${(customer?.current_monthly_payment || 0).toLocaleString()}</td>
          <td colspan="6" style="text-align: center; color: #9ca3af; font-size: 0.9rem;">Does not qualify</td>
        `;
        break;

      case 'failed':
        row.style.opacity = '0.5';
        row.style.backgroundColor = '#fee2e2';
        row.innerHTML = `
          <td>${customer?.name || ''}</td>
          <td>${customer?.phone || 'N/A'}</td>
          <td>${customer?.email || 'N/A'}</td>
          <td>$${(customer?.current_monthly_payment || 0).toLocaleString()}</td>
          <td colspan="6" style="text-align: center; color: #991b1b; font-size: 0.9rem;">❌ Analysis failed</td>
        `;
        break;

      case 'error':
        row.style.backgroundColor = '#fee2e2';
        break;
    }
  }

  // ✅ NEW: Display final qualified leads when all done
  function displayFinalQualifiedLeads() {
    const leadCount = document.getElementById('leadCount');
    if (leadCount) leadCount.textContent = qualifiedCustomersData.length;

    // Keep only qualified customers visible, hide others
    const rows = document.querySelectorAll('tr.customer-row');
    rows.forEach(row => {
      const btn = row.querySelector('button');
      if (!btn || !btn.textContent.includes('View Details')) {
        row.style.display = 'none';
      }
    });
  }

  // ✅ NEW: View qualified customer details and mark as viewed
  window.viewQualifiedCustomerDetails = async (customerKey) => {
    if (!window.customerAnalysisCache || !window.customerAnalysisCache[customerKey]) {
      alert('Analysis data not found');
      return;
    }

    const data = window.customerAnalysisCache[customerKey];
    const customer = qualifiedCustomersData.find(c => c.customer_key === customerKey);

    // ✅ Mark as viewed
    viewedCustomers.add(customerKey);

    // ✅ Highlight row in yellow
    const row = document.querySelector(`tr[data-customer-key="${customerKey}"]`);
    if (row) {
      row.style.backgroundColor = '#fef3c7';
    }

    // Open analysis page
    const title = `${customer ? customer.name : 'Customer'} - Analysis with ${currentLeadGenFilters.payloadName}`;
    openAnalysisPage({ title, data });
  };

  // ===== SCREEN 2: PAYLOAD BUILDER =====
  const loadJsonBtn = document.getElementById('loadJsonBtn');
  if (loadJsonBtn) {
    loadJsonBtn.addEventListener('click', () => {
      const jsonText = document.getElementById('jsonImportText').value.trim();
      if (!jsonText) {
        alert('Please paste JSON first');
        return;
      }

      try {
        const payload = JSON.parse(jsonText);

        // First, uncheck ALL field toggles
        document.querySelectorAll('.field-toggle').forEach(toggle => {
          toggle.checked = false;
        });

        // Load each field from JSON and check its toggle
        Object.entries(payload).forEach(([key, value]) => {
          const field = document.querySelector(`[name="${key}"]`);
          const toggle = document.querySelector(`.field-toggle[data-field="${key}"]`);
          if (!field) return;

          if (toggle) toggle.checked = true;

          if (field.type === 'checkbox') {
            field.checked = !!value;
          } else if (Array.isArray(value) && field.tagName === 'SELECT' && field.multiple) {
            Array.from(field.options).forEach(opt => {
              opt.selected = value.includes(opt.value);
            });
          } else {
            field.value = value;
          }
        });

        alert('JSON loaded successfully! Fields not in JSON are unchecked.');
        document.getElementById('jsonImportText').value = '';
      } catch (error) {
        alert('Invalid JSON: ' + error.message);
      }
    });
  }

  function buildPayload() {
    const form = document.getElementById('builderForm');
    const payload = {};
    if (!form) return payload;

    const fields = form.querySelectorAll('[name]');
    fields.forEach(el => {
      const key = el.name;
      if (!key) return;

      const toggle = document.querySelector(`.field-toggle[data-field="${key}"]`);
      if (toggle && !toggle.checked) return;

      if (el.tagName === 'SELECT' && el.multiple) {
        payload[key] = Array.from(el.selectedOptions).map(o => o.value);
      } else if (el.type === 'checkbox') {
        payload[key] = el.checked;
      } else if (el.type === 'number' && key !== 'propertyZipCode') {
        payload[key] = el.value === '' ? null : Number(el.value);
      } else {
        payload[key] = el.value;
      }
    });

    return payload;
  }

  const builderForm = document.getElementById('builderForm');
  if (builderForm) {
    builderForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const name = document.getElementById('payloadName').value.trim();
      if (!name) {
        alert('Please enter a payload name');
        return;
      }

      const payload = buildPayload();
      const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
      saved[name] = payload;
      localStorage.setItem('savedPayloads', JSON.stringify(saved));

      loadSavedPayloads();
      alert('Payload saved successfully!');
    });
  }

  const previewBtn = document.getElementById('previewBtn');
  if (previewBtn) {
    previewBtn.addEventListener('click', () => {
      const payload = buildPayload();
      const jsonContent = document.getElementById('jsonContent');
      const jsonPreview = document.getElementById('jsonPreview');
      if (jsonContent) jsonContent.textContent = JSON.stringify(payload, null, 2);
      if (jsonPreview) jsonPreview.classList.remove('hidden');
    });
  }

  const payloadSelect = document.getElementById('payloadSelect');
  if (payloadSelect) {
    payloadSelect.addEventListener('change', (e) => {
      const name = e.target.value;
      if (!name) return;

      const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
      const payload = saved[name];
      if (!payload) return;

      document.getElementById('payloadName').value = name;

      document.querySelectorAll('.field-toggle').forEach(toggle => {
        toggle.checked = false;
      });

      Object.entries(payload).forEach(([key, value]) => {
        const field = document.querySelector(`[name="${key}"]`);
        const toggle = document.querySelector(`.field-toggle[data-field="${key}"]`);
        if (!field) return;

        if (toggle) toggle.checked = true;

        if (field.type === 'checkbox') {
          field.checked = !!value;
        } else if (Array.isArray(value) && field.tagName === 'SELECT' && field.multiple) {
          Array.from(field.options).forEach(opt => {
            opt.selected = value.includes(opt.value);
          });
        } else {
          field.value = value;
        }
      });
    });
  }

  const deletePayloadBtn = document.getElementById('deletePayloadBtn');
  if (deletePayloadBtn) {
    deletePayloadBtn.addEventListener('click', () => {
      const name = document.getElementById('payloadSelect').value;
      if (!name) return;

      if (!confirm(`Delete payload "${name}"?`)) return;

      const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
      delete saved[name];
      localStorage.setItem('savedPayloads', JSON.stringify(saved));

      loadSavedPayloads();
      document.getElementById('payloadName').value = '';
    });
  }

  // ===== SCREEN 3: CUSTOMER MANAGEMENT =====
  let allCustomers = [];

  // Zipcode lookup with debouncing
  let zipcodeLookupTimeout;
  const cZip = document.getElementById('cZip');
  if (cZip) {
    cZip.addEventListener('input', async (e) => {
      const zipcode = e.target.value.trim();
      const zipStatus = document.getElementById('zipStatus');

      clearTimeout(zipcodeLookupTimeout);

      // Reset fields
      const cState = document.getElementById('cState');
      const cCounty = document.getElementById('cCounty');
      const cCity = document.getElementById('cCity');
      if (cState) cState.value = '';
      if (cCounty) cCounty.value = '';
      if (cCity) cCity.value = '';
      if (zipStatus) {
        zipStatus.textContent = '';
        zipStatus.className = '';
      }

      if (!/^\d{5}$/.test(zipcode)) {
        if (zipcode.length > 0 && zipStatus) {
          zipStatus.textContent = 'Enter 5-digit zipcode';
          zipStatus.className = 'zip-error';
        }
        return;
      }

      if (zipStatus) {
        zipStatus.textContent = 'Looking up...';
        zipStatus.className = 'zip-loading';
      }

      zipcodeLookupTimeout = setTimeout(async () => {
        try {
          const response = await fetch(`/api/zipcode/${zipcode}`);
          const data = await response.json();

          if (data.success) {
            if (cState) cState.value = data.state;
            if (cCounty) cCounty.value = data.county;
            if (cCity) cCity.value = data.city || '';
            if (zipStatus) {
              zipStatus.textContent = `✓ ${data.city}, ${data.state}`;
              zipStatus.className = 'zip-success';
            }
          } else {
            if (zipStatus) {
              zipStatus.textContent = '✗ Zipcode not found';
              zipStatus.className = 'zip-error';
            }
          }
        } catch (error) {
          if (zipStatus) {
            zipStatus.textContent = '✗ Lookup failed';
            zipStatus.className = 'zip-error';
          }
        }
      }, 500);
    });
  }

  async function loadCustomers() {
    try {
      const response = await fetch('/api/customers');
      allCustomers = await response.json();
      renderCustomers(allCustomers);
    } catch (error) {
      console.error('Error loading customers:', error);
    }
  }

  function renderCustomers(customers) {
    const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
    const tbody = document.getElementById('customerTableBody');
    if (!tbody) return;

    tbody.innerHTML = customers.map(c => {
      const payloadOptions = Object.keys(saved).map(name =>
        `<option value="${name}">${name}</option>`
      ).join('');

      return `
      <tr>
        <td>${c.name}</td>
        <td>${c.phone || 'N/A'}</td>
        <td>${c.email || 'N/A'}</td>
        <td>$${(c.current_monthly_payment || 0).toLocaleString()}</td>
        <td>${c.credit_score}</td>
        <td>v${c.version}</td>
        <td>
          <div style="display: flex; gap: 0.5rem; align-items: center;">
            <select class="customer-payload-select" data-customer-key="${c.customer_key}" style="font-size: 0.85rem; padding: 0.25rem;">
              <option value="">Select Template</option>
              ${payloadOptions}
            </select>
            <button class="btn-sm" onclick="analyzeCustomerWithTemplate('${c.customer_key}')">Analyze</button>
            <button class="btn-sm" onclick="editCustomer('${c.customer_key}')">Edit</button>
            <button class="btn-sm" onclick="viewHistory('${c.customer_key}')">History</button>
            <button class="btn-sm btn-danger" onclick="deleteCustomer('${c.customer_key}')">Delete</button>
          </div>
        </td>
      </tr>
    `}).join('');
  }

  // ✅ UPDATED: Analyze customer with template -> open NEW PAGE (no modal)
  window.analyzeCustomerWithTemplate = async (customerKey) => {
    const selectElement = document.querySelector(`.customer-payload-select[data-customer-key="${customerKey}"]`);
    const templateName = selectElement ? selectElement.value : '';

    if (!templateName) {
      alert('Please select a payload template first');
      return;
    }

    const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
    const payload = saved[templateName];

    if (!payload) {
      alert('Template not found');
      return;
    }

    const customer = allCustomers.find(c => c.customer_key === customerKey);
    const title = `${customer ? customer.name : 'Customer'} - Analysis with ${templateName}`;

    showLoader();
    try {
      const response = await fetch(`/api/customers/${customerKey}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          payload: payload,
          min_savings: 200,
          target_amount: -2000
        })
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || `HTTP ${response.status}`);
      }

      const data = await response.json();
      openAnalysisPage({ title, data });
    } catch (error) {
      alert('Analysis error: ' + error.message);
    } finally {
      hideLoader();
    }
  };

  const customerSearch = document.getElementById('customerSearch');
  if (customerSearch) {
    customerSearch.addEventListener('input', (e) => {
      const term = e.target.value.toLowerCase();
      const filtered = allCustomers.filter(c =>
        c.name.toLowerCase().includes(term) ||
        (c.email && c.email.toLowerCase().includes(term)) ||
        (c.phone && c.phone.includes(term))
      );
      renderCustomers(filtered);
    });
  }

  const addCustomerBtn = document.getElementById('addCustomerBtn');
  if (addCustomerBtn) {
    addCustomerBtn.addEventListener('click', () => {
      document.getElementById('formTitle').textContent = 'Add Customer';
      document.getElementById('customerKey').value = '';
      document.getElementById('customerFormElement').reset();
      document.getElementById('customerForm').classList.remove('hidden');
    });
  }

  const cancelCustomerBtn = document.getElementById('cancelCustomerBtn');
  if (cancelCustomerBtn) {
    cancelCustomerBtn.addEventListener('click', () => {
      document.getElementById('customerForm').classList.add('hidden');
    });
  }

  const customerFormElement = document.getElementById('customerFormElement');
  if (customerFormElement) {
    customerFormElement.addEventListener('submit', async (e) => {
      e.preventDefault();

      const customerKey = document.getElementById('customerKey').value;
      const data = {
        name: document.getElementById('cName').value,
        phone: document.getElementById('cPhone').value,
        email: document.getElementById('cEmail').value,
        current_monthly_payment: document.getElementById('cPayment').value,
        remaining_balance: document.getElementById('cBalance').value,
        property_value: document.getElementById('cValue').value,
        credit_score: document.getElementById('cScore').value,
        monthly_income: document.getElementById('cIncome').value,
        property_zip: document.getElementById('cZip').value,
        property_state: document.getElementById('cState').value,
        property_county: document.getElementById('cCounty').value,
      };

      try {
        const url = customerKey ? `/api/customers/${customerKey}` : '/api/customers';
        const method = customerKey ? 'PUT' : 'POST';

        const response = await fetch(url, {
          method,
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });

        if (response.ok) {
          document.getElementById('customerForm').classList.add('hidden');
          loadCustomers();
        }
      } catch (error) {
        alert('Error: ' + error.message);
      }
    });
  }

  window.editCustomer = async (customerKey) => {
    const customer = allCustomers.find(c => c.customer_key === customerKey);
    if (!customer) return;

    document.getElementById('formTitle').textContent = 'Edit Customer';
    document.getElementById('customerKey').value = customerKey;
    document.getElementById('cName').value = customer.name;
    document.getElementById('cPhone').value = customer.phone || '';
    document.getElementById('cEmail').value = customer.email || '';
    document.getElementById('cPayment').value = customer.current_monthly_payment;
    document.getElementById('cBalance').value = customer.remaining_balance;
    document.getElementById('cValue').value = customer.property_value;
    document.getElementById('cScore').value = customer.credit_score;
    document.getElementById('cIncome').value = customer.monthly_income;
    document.getElementById('cZip').value = customer.property_zip;
    document.getElementById('cState').value = customer.property_state || '';
    document.getElementById('cCounty').value = customer.property_county || '';
    const cCity = document.getElementById('cCity');
    if (cCity) cCity.value = '';

    const zipStatus = document.getElementById('zipStatus');
    if (customer.property_state && zipStatus) {
      zipStatus.textContent = `✓ ${customer.property_state}`;
      zipStatus.className = 'zip-success';
    }

    document.getElementById('customerForm').classList.remove('hidden');
  };

  window.deleteCustomer = async (customerKey) => {
    if (!confirm('Are you sure you want to deactivate this customer?')) return;
    try {
      await fetch(`/api/customers/${customerKey}`, { method: 'DELETE' });
      loadCustomers();
    } catch (error) {
      alert('Error: ' + error.message);
    }
  };

  window.viewHistory = async (customerKey) => {
    try {
      const response = await fetch(`/api/customers/${customerKey}/history`);
      const history = await response.json();

      const historyHtml = history.map(h => `
        <div class="history-item">
          <strong>Version ${h.version}</strong>
          <span>${new Date(h.effective_date).toLocaleString()}</span>
          ${h.end_date ? `<span>to ${new Date(h.end_date).toLocaleString()}</span>` : '<span class="badge-current">CURRENT</span>'}
          <div>Payment: $${h.current_monthly_payment}, Balance: $${h.remaining_balance}, Score: ${h.credit_score}</div>
        </div>
      `).join('');

      showModal('Customer History', historyHtml);
    } catch (error) {
      alert('Error: ' + error.message);
    }
  };

  // ✅ UPDATED: Lead-gen "Details" -> open NEW PAGE (no modal)
  window.analyzeCustomerDetail = async (customerKey) => {
    // Try to find customer in cache, or fetch if needed
    let customer = allCustomers.find(c => c.customer_key === customerKey);

    if (!customer) {
      try {
        const resp = await fetch('/api/customers');
        const customers = await resp.json();
        allCustomers = customers;
        customer = customers.find(c => c.customer_key === customerKey);
      } catch (e) {
        alert('Error loading customer: ' + e.message);
        return;
      }
    }

    if (!customer) {
      alert('Customer not found');
      return;
    }

    // Get payload - try lead gen select first, then builder select
    let payloadName = document.getElementById('lgPayloadSelect')?.value;
    if (!payloadName) payloadName = document.getElementById('payloadSelect')?.value;

    const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
    const payload = saved[payloadName];

    if (!payload) {
      alert('No payload template selected. Select/create one in Payload Builder.');
      return;
    }

    const title = `${customer.name} - Detailed Analysis`;

    showLoader();
    try {
      const response = await fetch(`/api/customers/${customerKey}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          payload: payload,
          min_savings: 200,
          target_amount: -2000
        })
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || `HTTP ${response.status}`);
      }

      const data = await response.json();
      openAnalysisPage({ title, data });
    } catch (error) {
      alert('Analysis error: ' + error.message);
    } finally {
      hideLoader();
    }
  };

  // ============================================================
  // ✅ Analysis renderer (works for BOTH modalBody or analysisBody)
  // ============================================================
  function displayDetailedAnalysis(data, targetEl) {
    const container = targetEl || document.getElementById('modalBody') || document.body;

    if (!data || !data.customer || !data.scenarios) {
      container.innerHTML = `<div class="error">Invalid analysis data received</div>`;
      return;
    }

    const customer = data.customer;
    const scenariosRaw = Array.isArray(data.scenarios) ? data.scenarios : [];

    // Fixed buydown order (positions never change)
    const BUydownOrder = ["None", "1-0 LLPA", "2-1 LLPA"];
    const normBuydown = (v) => (v ?? "").toString().trim().replace(/\s+/g, " ");
    const DISPLAY_BUYDOWN = {
      "None": "None",
      "1-0 LLPA": "1-0 LLPA",
      "2-1 LLPA": "2-1 LLPA",
    };

    const scenarios = [...scenariosRaw].sort((a, b) => {
      const ai = BUydownOrder.indexOf(normBuydown(a.buydown_type));
      const bi = BUydownOrder.indexOf(normBuydown(b.buydown_type));
      return (ai === -1 ? 999 : ai) - (bi === -1 ? 999 : bi);
    });

    // Build term index: term_years -> { buydown_type -> [products...] }
    const termIndex = {};
    scenarios.forEach(sc => {
      const bt = normBuydown(sc.buydown_type) || "Unknown";
      const products = Array.isArray(sc.products) ? sc.products : [];
      products.forEach(p => {
        const term = (p.term_years ?? "Unknown").toString();
        if (!termIndex[term]) termIndex[term] = {};
        if (!termIndex[term][bt]) termIndex[term][bt] = [];
        termIndex[term][bt].push(p);
      });
    });

    const terms = Object.keys(termIndex).sort((a, b) => {
      const na = Number(a); const nb = Number(b);
      if (!Number.isFinite(na) && !Number.isFinite(nb)) return a.localeCompare(b);
      if (!Number.isFinite(na)) return 1;
      if (!Number.isFinite(nb)) return -1;
      return na - nb;
    });

    const fmtMoney = (v) => `$${(Number(v) || 0).toLocaleString()}`;
    const fmtRate = (v) =>
      (v === null || v === undefined || Number.isNaN(Number(v))) ? 'N/A' : `${Number(v).toFixed(3)}%`;

    // Target credit/cost (finalPriceAfterOriginationFee.amount) used to pick the "best" row
    const TARGET_AMOUNT = Number(data.target_amount ?? data.targetAmount ?? -2000);

    // Pick 1 closest-to-target + 3 lower-rate + 2 higher-rate (all in ascending rate order)
    function pickRatesAroundTarget(allRates, targetAmount) {
      const rates = (Array.isArray(allRates) ? allRates : [])
        .filter(r => r && r.interest_rate !== null && r.interest_rate !== undefined)
        .map(r => ({
          ...r,
          _rateNum: Number(r.interest_rate),
          _creditNum: Number(r.credit_cost)
        }))
        .filter(r => Number.isFinite(r._rateNum));

      if (!rates.length) return { selected: [], targetKey: null };

      // Find closest to targetAmount by credit_cost (fallback to 0 if missing)
      let best = null;
      let bestDiff = Infinity;

      for (const r of rates) {
        const credit = Number.isFinite(r._creditNum) ? r._creditNum : 0;
        const diff = Math.abs(credit - targetAmount);
        if (diff < bestDiff) {
          bestDiff = diff;
          best = r;
        }
      }

      // Sort by rate ascending, then by credit_cost closeness
      const sorted = [...rates].sort((a, b) => {
        if (a._rateNum !== b._rateNum) return a._rateNum - b._rateNum;
        const aCredit = Number.isFinite(a._creditNum) ? a._creditNum : 0;
        const bCredit = Number.isFinite(b._creditNum) ? b._creditNum : 0;
        return Math.abs(aCredit - targetAmount) - Math.abs(bCredit - targetAmount);
      });

      // Find index of best in sorted list
      const bestIdx = sorted.findIndex(r =>
        r._rateNum === best._rateNum &&
        ((Number.isFinite(r._creditNum) ? r._creditNum : 0) === (Number.isFinite(best._creditNum) ? best._creditNum : 0)) &&
        ((r.monthly_payment ?? null) === (best.monthly_payment ?? null))
      );

      const idx = bestIdx >= 0 ? bestIdx : sorted.findIndex(r => r._rateNum === best._rateNum);

      const lower = sorted.slice(Math.max(0, idx - 3), idx);
      const higher = sorted.slice(idx + 1, idx + 3);
      const selected = [...lower, sorted[idx], ...higher].filter(Boolean);

      // Mark the best row for highlighting (use a stable-ish key)
      const targetKey = `${sorted[idx]._rateNum}::${Number.isFinite(sorted[idx]._creditNum) ? sorted[idx]._creditNum : 0}::${sorted[idx].monthly_payment ?? 0}`;

      const dedup = [];
      const seen = new Set();
      for (const r of selected) {
        const key = `${r._rateNum}::${Number.isFinite(r._creditNum) ? r._creditNum : 0}::${r.monthly_payment ?? 0}`;
        if (!seen.has(key)) {
          seen.add(key);
          dedup.push(r);
        }
      }

      // Return in ascending rate order
      dedup.sort((a, b) => a._rateNum - b._rateNum);
      return { selected: dedup, targetKey };
    }



    let html = `
      <div class="customer-summary">
        <h4>${customer.name}</h4>
        <div class="summary-grid">
          <div><strong>Current Payment:</strong> ${fmtMoney(customer.current_monthly_payment)}</div>
          <div><strong>Balance:</strong> ${fmtMoney(customer.remaining_balance)}</div>
          <div><strong>Credit Score:</strong> ${customer.credit_score || 'N/A'}</div>
        </div>
      </div>
    `;

    if (!scenarios.length || !terms.length) {
      html += `<div class="error">No qualifying products found</div>`;
      container.innerHTML = html;
      return;
    }

    html += `<div class="term-accordion">`;

    terms.forEach((term, idx) => {
      const termLabel = Number.isFinite(Number(term)) ? `${term} Year Term` : `Term: ${term}`;
      const isCollapsed = idx !== 0;

      html += `
        <div class="term-accordion-item ${isCollapsed ? 'collapsed' : ''}" data-term="${term}">
          <button class="term-accordion-header term-toggle" type="button" aria-expanded="${!isCollapsed}">
            <span class="term-title">${termLabel}</span>
            <span class="term-meta">Click to ${isCollapsed ? 'expand' : 'collapse'}</span>
          </button>

          <div class="term-accordion-body">
            <div class="buydown-comparison">
      `;

      BUydownOrder.forEach(bt => {
        const scenarioObj =
          scenarios.find(s => normBuydown(s.buydown_type || "Unknown") === bt) || { buydown_type: bt };
        const prods = (termIndex[term] && termIndex[term][bt]) ? termIndex[term][bt] : [];

        html += `
          <div class="buydown-scenario">
            <div class="scenario-header">
              <h4>${DISPLAY_BUYDOWN[bt] || bt}</h4>
            </div>
            <div class="scenario-body">
        `;

        if (prods.length === 0) {
          html += `<div class="error">No products found</div>`;
        } else {
          // Pick rates around target for this product set
          const { selected, targetKey } = pickRatesAroundTarget(prods, TARGET_AMOUNT);

          prods.forEach(p => {
            const isSelected = selected.includes(p);
            const rateClass = isSelected ? 'rate-highlight' : '';
            const monthlyPayment = (p.monthly_payment || 0).toLocaleString();
            const fmtPoints = (p.points ?? 0).toFixed(3);
            const fmtFee = fmtMoney(p.origination_fee);

            html += `
              <div class="product-row ${rateClass}" data-product-id="${p.product_id}">
                <div class="row-inner">
                  <div class="col col-rate">${fmtRate(p.interest_rate)}</div>
                  <div class="col col-monthly-payment">$${monthlyPayment}</div>
                  <div class="col col-points">${fmtPoints}</div>
                  <div class="col col-fee">${fmtFee}</div>
                  <div class="col col-total-cost">${fmtMoney(p.total_cost)}</div>
                  <div class="col col-qualifying">${p.qualifying ? '✓' : '✗'}</div>
                </div>
              </div>
            `;
          });
        }

        html += `
            </div>
          </div>
        `;
      });

      html += `
            </div>
          </div>
        `;
    });

    html += `</div>`;

    container.innerHTML = html;
  }

  // ============================================================
  // Global error handler
  // ============================================================
  window.addEventListener('error', (e) => {
    console.error('Global error caught:', e);
    alert('An unexpected error occurred. Please try again later.');
  });

  // Optional: catch unhandled promise rejections
  window.addEventListener('unhandledrejection', (e) => {
    console.error('Unhandled promise rejection:', e);
    alert('An unexpected error occurred. Please try again later.');
  });
});

