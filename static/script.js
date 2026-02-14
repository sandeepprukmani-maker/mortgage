document.addEventListener('DOMContentLoaded', () => {
  const analyzeForm = document.getElementById('analyzeForm');
  const builderForm = document.getElementById('builderForm');
  const submitBtn = document.getElementById('submitBtn');
  const resultsSection = document.getElementById('resultsSection');
  const resultsContainer = document.getElementById('resultsContainer');
  const errorSection = document.getElementById('errorSection');
  const errorMessage = document.getElementById('errorMessage');

  // Tab switching
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');
  const payloadSelect = document.getElementById('payloadSelect');
  const analyzePayloadSelect = document.getElementById('analyzePayloadSelect');

  // Array fields in the UWM request payload
  const ARRAY_FIELDS = new Set([
    'loanTypeIds',
    'loanTermIds',
    'waivableFeeTypeIds',
    'useMortgageInsuranceTypeIds',
  ]);

  // Helper: multi-select read
  function getSelectedValues(selectEl) {
    return Array.from(selectEl.selectedOptions).map(o => o.value);
  }

  // Helper: multi-select write
  function setSelectedValues(selectEl, values) {
    const set = new Set((values || []).map(String));
    Array.from(selectEl.options).forEach(opt => {
      opt.selected = set.has(String(opt.value));
    });
  }

  // --- localStorage payloads ---
  function loadSavedPayloads() {
    const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
    const options =
      '<option value="">-- Select a Payload --</option>' +
      Object.keys(saved).map(name => `<option value="${name}">${name}</option>`).join('');

    payloadSelect.innerHTML = options;
    if (analyzePayloadSelect) analyzePayloadSelect.innerHTML = options;
  }

  loadSavedPayloads();

  // Tab events
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(`${btn.dataset.tab}Section`).classList.add('active');

      // Clear errors when switching tabs
      if (errorSection) errorSection.classList.add('hidden');

      if (btn.dataset.tab === 'customers') {
        loadCustomers();
      }
    });
  });

  // --- Customer Management ---
  const customerForm = document.getElementById('customerForm');
  const customerTableBody = document.getElementById('customerTableBody');
  const cancelCustomerBtn = document.getElementById('cancelCustomerBtn');
  const customerSearch = document.getElementById('customerSearch');
  let allCustomers = [];

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
    const payloadOptions =
      '<option value="">-- Template --</option>' +
      Object.keys(saved).map(name => `<option value="${name}">${name}</option>`).join('');

    customerTableBody.innerHTML = customers
      .map(
        c => `
        <tr>
          <td>${c.name}</td>
          <td>$${(c.monthly_income || 0).toLocaleString()}</td>
          <td>$${(c.current_monthly_payment || 0).toLocaleString()}</td>
          <td>${c.credit_score}</td>
          <td>
            <div style="display:flex; gap:.5rem; align-items:center;">
              <select class="payload-select-sm" id="payload-${c.id}">
                ${payloadOptions}
              </select>
              <button class="primary-btn btn-sm" onclick="analyzeCustomer(${c.id})">Analyze</button>
            </div>
          </td>
          <td>
            <button class="secondary-btn btn-sm" onclick="editCustomer(${JSON.stringify(c).replace(/"/g, '&quot;')})">Edit</button>
            <button class="secondary-btn btn-sm delete-btn" onclick="deleteCustomer(${c.id})">Delete</button>
          </td>
        </tr>
      `
      )
      .join('');
  }

  if (customerSearch) {
    customerSearch.addEventListener('input', e => {
      const term = e.target.value.toLowerCase();
      const filtered = allCustomers.filter(c => c.name.toLowerCase().includes(term));
      renderCustomers(filtered);
    });
  }

  window.analyzeCustomer = async customerId => {
    const select = document.getElementById(`payload-${customerId}`);
    const payloadName = select ? select.value : '';
    const customer = allCustomers.find(c => c.id === customerId);
    if (!customer) return;

    const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
    const payloadTemplate = saved[payloadName];

    let body;
    if (payloadTemplate) {
      // Merge customer data into payload template
      const templatePayload = payloadTemplate.payload || payloadTemplate;
      const mergedPayload = {
        ...templatePayload,
        borrowerName: customer.name,
        monthlyIncome: customer.monthly_income,
        currentMonthlyPayment: customer.current_monthly_payment, // used only for savings calc (backend)
        creditScore: customer.credit_score,
        propertyZipCode: customer.property_zip,
      };
      body = JSON.stringify([mergedPayload]);
    } else {
      // Direct analysis with just customer data
      body = JSON.stringify([customer]);
    }

    handleAnalysis(body, '/api/analyze/direct?min_savings=200&target_amount=-2000', true);

    // Switch to analyze tab to show results
    const analyzeTab = Array.from(tabBtns).find(b => b.dataset.tab === 'analyze');
    if (analyzeTab) analyzeTab.click();
  };

  window.editCustomer = customer => {
    document.getElementById('customerId').value = customer.id;
    document.getElementById('cName').value = customer.name;
    document.getElementById('cIncome').value = customer.monthly_income;
    document.getElementById('cPayment').value = customer.current_monthly_payment;
    document.getElementById('cBalance').value = customer.remaining_balance;
    document.getElementById('cValue').value = customer.property_value;
    document.getElementById('cZip').value = customer.property_zip;
    document.getElementById('cState').value = customer.property_state;
    document.getElementById('cScore').value = customer.credit_score;
    document.getElementById('saveCustomerBtn').textContent = 'Update Customer';
  };

  window.deleteCustomer = async id => {
    if (!confirm('Are you sure you want to delete this customer?')) return;
    try {
      const response = await fetch(`/api/customers/${id}`, { method: 'DELETE' });
      if (response.ok) loadCustomers();
    } catch (error) {
      console.error('Error deleting customer:', error);
    }
  };

  cancelCustomerBtn.addEventListener('click', () => {
    customerForm.reset();
    document.getElementById('customerId').value = '';
    document.getElementById('saveCustomerBtn').textContent = 'Save Customer';
  });

  customerForm.addEventListener('submit', async e => {
    e.preventDefault();
    const id = document.getElementById('customerId').value;
    const data = {
      name: document.getElementById('cName').value,
      monthly_income: document.getElementById('cIncome').value,
      current_monthly_payment: document.getElementById('cPayment').value,
      remaining_balance: document.getElementById('cBalance').value,
      property_value: document.getElementById('cValue').value,
      property_zip: document.getElementById('cZip').value,
      property_state: document.getElementById('cState').value,
      credit_score: document.getElementById('cScore').value,
      property_county: '', // optional for now
    };

    try {
      const url = id ? `/api/customers/${id}` : '/api/customers';
      const method = id ? 'PUT' : 'POST';
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        customerForm.reset();
        document.getElementById('customerId').value = '';
        document.getElementById('saveCustomerBtn').textContent = 'Save Customer';
        loadCustomers();
      }
    } catch (error) {
      console.error('Error saving customer:', error);
    }
  });

  // --- Load Payload into builder ---
  payloadSelect.addEventListener('change', () => {
    const name = payloadSelect.value;
    if (!name) return;

    const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
    const payloadData = saved[name];
    if (!payloadData) return;

    const payload = payloadData.payload || payloadData;
    const excludedFields = payloadData.excludedFields || [];

    document.getElementById('payloadName').value = name;

    // Fill form fields
    Object.entries(payload).forEach(([key, value]) => {
      const field = builderForm.querySelector(`[name="${key}"]`);
      if (!field) return;

      if (field.type === 'checkbox') {
        field.checked = !!value;
        return;
      }

      if (Array.isArray(value)) {
        if (field.tagName === 'SELECT' && field.multiple) {
          setSelectedValues(field, value);
        } else {
          field.value = value[0] ?? '';
        }
        return;
      }

      field.value = value;
    });

    // Set toggles based on excludedFields
    const toggles = builderForm.querySelectorAll('.field-toggle');
    toggles.forEach(toggle => {
      const fieldName = toggle.dataset.field;
      toggle.checked = !excludedFields.includes(fieldName);
    });
  });

  // --- Save / Delete Payload ---
  document.getElementById('savePayloadBtn').addEventListener('click', () => {
    const name = document.getElementById('payloadName').value.trim();
    if (!name) {
      alert('Please enter a payload name');
      return;
    }
    const { payload, excludedFields } = buildPayloadWithExclusions();
    const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
    saved[name] = { payload, excludedFields };
    localStorage.setItem('savedPayloads', JSON.stringify(saved));
    loadSavedPayloads();
    payloadSelect.value = name;
    alert('Payload saved successfully!');
  });

  document.getElementById('deletePayloadBtn').addEventListener('click', () => {
    const name = payloadSelect.value;
    if (!name) return;

    const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
    if (!saved[name]) return;

    if (!confirm(`Delete payload "${name}"?`)) return;

    delete saved[name];
    localStorage.setItem('savedPayloads', JSON.stringify(saved));
    loadSavedPayloads();

    document.getElementById('payloadName').value = '';
    payloadSelect.value = '';
    alert('Payload deleted.');
  });

  function buildPayloadWithExclusions() {
    const payload = buildPayload();
    const excludedFields = [];
    const toggles = builderForm.querySelectorAll('.field-toggle');

    toggles.forEach(toggle => {
      if (!toggle.checked) {
        const fieldName = toggle.dataset.field;
        excludedFields.push(fieldName);
        delete payload[fieldName];
      }
    });

    return { payload, excludedFields };
  }

  // --- Builder submit: Analyze Scenario ---
  builderForm.addEventListener('submit', async e => {
    e.preventDefault();
    const { payload } = buildPayloadWithExclusions();
    // backend expects list
    handleAnalysis(JSON.stringify([payload]), '/api/analyze/direct', true);
  });

  // --- Database Analysis Form ---
  if (analyzeForm) {
    analyzeForm.addEventListener('submit', async e => {
      e.preventDefault();

      const formData = new FormData(analyzeForm);
      const payloadName = formData.get('analyzePayloadSelect');
      const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
      const payloadTemplate = saved[payloadName] ? JSON.stringify(saved[payloadName]) : '';

      const body = new FormData();
      body.append('min_savings', formData.get('min_savings'));
      body.append('target_amount', formData.get('target_amount'));
      body.append('tolerance', formData.get('tolerance'));
      if (payloadTemplate) body.append('base_payload', payloadTemplate);

      handleAnalysis(body, '/api/analyze');
    });
  }

  // --- Preview / Download JSON ---
  document.getElementById('previewBtn').addEventListener('click', () => {
    const { payload } = buildPayloadWithExclusions();
    const preview = document.getElementById('jsonPreview');
    const content = document.getElementById('jsonContent');
    content.textContent = JSON.stringify(payload, null, 4);
    preview.classList.remove('hidden');
  });

  document.getElementById('downloadBtn').addEventListener('click', () => {
    const { payload } = buildPayloadWithExclusions();
    const blob = new Blob([JSON.stringify(payload, null, 4)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${payload.borrowerName || 'payload'}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  });

  // ✅ Fixed payload builder: correctly reads ALL selected values for array/multi-select fields
  function buildPayload() {
    const payload = {};

    const fields = builderForm.querySelectorAll('input[name], select[name], textarea[name]');
    fields.forEach(el => {
      const key = el.name;
      if (!key) return;

      // Multi-select: array
      if (el.tagName === 'SELECT' && el.multiple) {
        payload[key] = getSelectedValues(el);
        return;
      }

      // Checkbox: boolean
      if (el.type === 'checkbox') {
        payload[key] = el.checked;
        return;
      }

      // Number input: number (except zip)
      if (el.type === 'number' && key !== 'propertyZipCode') {
        payload[key] = el.value === '' ? null : Number(el.value);
        return;
      }

      // Other: string
      payload[key] = el.value;
    });

    // Ensure array fields are arrays of strings even if something submits single value
    ARRAY_FIELDS.forEach(k => {
      if (payload[k] == null) return;
      if (!Array.isArray(payload[k])) payload[k] = [String(payload[k])];
      payload[k] = payload[k].map(String);
    });

    return payload;
  }

  async function handleAnalysis(body, url, isJson = false) {
    // Reset UI
    resultsSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    resultsContainer.innerHTML = '';

    const currentBtn = isJson ? document.getElementById('buildAnalyzeBtn') : submitBtn;
    const originalText = currentBtn.textContent;
    currentBtn.disabled = true;
    currentBtn.textContent = 'Analyzing...';

    try {
      const options = { method: 'POST', body };
      if (isJson) {
        options.headers = { 'Content-Type': 'application/json' };
      }

      const response = await fetch(url, options);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Analysis failed');
      }

      displayResults(data);
    } catch (error) {
      console.error('Error:', error);
      errorMessage.textContent = error.message;
      errorSection.classList.remove('hidden');
    } finally {
      currentBtn.disabled = false;
      currentBtn.textContent = originalText;
    }
  }

  function displayResults(data) {
    if (!data || data.length === 0) {
      resultsContainer.innerHTML = '<p>No qualifying products found matching criteria.</p>';
      resultsSection.classList.remove('hidden');
      window.scrollTo({ top: resultsSection.offsetTop, behavior: 'smooth' });
      return;
    }

    data.forEach(customerResult => {
      const card = document.createElement('div');
      card.className = 'result-card';

      const productsHtml = customerResult.products
        .map(
          prod => `
          <tr>
            <td>${prod.mortgageProductName}<br><small>${prod.mortgageProductAlias || ''}</small></td>
            <td>${(prod.interestRate * 100).toFixed(3)}%</td>
            <td>$${prod.closestAmount.toLocaleString()}</td>
            <td>$${prod.matchedMonthlyPayment.toLocaleString()}</td>
            <td class="positive">$${prod.monthlySavings.toLocaleString()}</td>
          </tr>
        `
        )
        .join('');

      card.innerHTML = `
        <h3 class="customer-name">${customerResult.name}</h3>
        <div class="summary-grid">
          <div class="summary-item">
            <label>Current Monthly Payment</label>
            <span>$${customerResult.currentMonthlyPayment.toLocaleString()}</span>
          </div>
          <div class="summary-item">
            <label>Qualifying Options</label>
            <span>${customerResult.products.length}</span>
          </div>
        </div>

        <h4>Recommended Products</h4>
        <div class="table-responsive">
          <table class="products-table">
            <thead>
              <tr>
                <th>Product</th>
                <th>Rate</th>
                <th>Credit/Cost</th>
                <th>New Payment</th>
                <th>Monthly Savings</th>
              </tr>
            </thead>
            <tbody>
              ${productsHtml}
            </tbody>
          </table>
        </div>
      `;

      resultsContainer.appendChild(card);
    });

    resultsSection.classList.remove('hidden');
    window.scrollTo({ top: resultsSection.offsetTop, behavior: 'smooth' });
  }
});
