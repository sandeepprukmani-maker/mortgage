document.addEventListener('DOMContentLoaded', () => {
  const analyzeForm = document.getElementById('analyzeForm');
  const builderForm = document.getElementById('builderForm');
  const submitBtn = document.getElementById('submitBtn');
  const resultsSection = document.getElementById('resultsSection');
  const resultsContainer = document.getElementById('resultsContainer');
  const customerResultsSection = document.getElementById('customerAnalysisResults');
  const customerResultsContainer = document.getElementById('customerResultsContainer');
  const errorSection = document.getElementById('errorSection');
  const errorMessage = document.getElementById('errorMessage');

  // Sidebar navigation logic
  const navItems = document.querySelectorAll('.nav-item');
  const tabContents = document.querySelectorAll('.tab-content');

  navItems.forEach(item => {
    item.addEventListener('click', () => {
      const targetTab = item.dataset.tab;

      navItems.forEach(nav => nav.classList.remove('active'));
      tabContents.forEach(tab => tab.classList.remove('active'));

      item.classList.add('active');
      document.getElementById(`${targetTab}Section`).classList.add('active');

      if (targetTab === 'customers') {
        loadCustomers();
      }

      // Clear generic error section when switching
      errorSection.classList.add('hidden');
    });
  });

  const payloadSelect = document.getElementById('payloadSelect');
  const analyzePayloadSelect = document.getElementById('analyzePayloadSelect');

  const ARRAY_FIELDS = new Set([
    'loanTypeIds',
    'loanTermIds',
    'waivableFeeTypeIds',
    'useMortgageInsuranceTypeIds',
  ]);

  function getSelectedValues(selectEl) {
    return Array.from(selectEl.selectedOptions).map(o => o.value);
  }

  function setSelectedValues(selectEl, values) {
    const set = new Set((values || []).map(String));
    Array.from(selectEl.options).forEach(opt => {
      opt.selected = set.has(String(opt.value));
    });
  }

  function loadSavedPayloads() {
    const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
    const options =
      '<option value="">-- Select a Template --</option>' +
      Object.keys(saved).map(name => `<option value="${name}">${name}</option>`).join('');

    if (payloadSelect) payloadSelect.innerHTML = options;
    if (analyzePayloadSelect) analyzePayloadSelect.innerHTML = options;
  }

  loadSavedPayloads();

  // --- Customer Management ---
  const customerForm = document.getElementById('customerForm');
  const customerTableBody = document.getElementById('customerTableBody');
  const cancelCustomerBtn = document.getElementById('cancelCustomerBtn');
  const customerSearch = document.getElementById('customerSearch');
  const customerCountBadge = document.getElementById('customerCountBadge');
  let allCustomers = [];

  async function loadCustomers() {
    try {
      const response = await fetch('/api/customers');
      allCustomers = await response.json();
      if (customerCountBadge) customerCountBadge.textContent = `${allCustomers.length} Customers`;
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
          <td style="font-weight: 500;">${c.name}</td>
          <td>$${(c.monthly_income || 0).toLocaleString()}</td>
          <td>$${(c.current_monthly_payment || 0).toLocaleString()}</td>
          <td><span class="badge badge-blue">${c.credit_score}</span></td>
          <td>
            <div style="display:flex; gap:.5rem; align-items:center;">
              <select class="payload-select-sm" id="payload-${c.id}" style="max-width: 140px; padding: 0.4rem;">
                ${payloadOptions}
              </select>
              <button class="btn-primary" style="padding: 0.4rem 0.8rem; width: auto;" onclick="analyzeCustomer(${c.id})">Analyze</button>
            </div>
          </td>
          <td>
            <div style="display:flex; gap:.25rem;">
              <button class="btn-secondary" style="padding: 0.4rem 0.8rem; width: auto;" onclick="editCustomer(${JSON.stringify(c).replace(/"/g, '&quot;')})">Edit</button>
              <button class="btn-danger" style="padding: 0.4rem 0.8rem; width: auto;" onclick="deleteCustomer(${c.id})">Del</button>
            </div>
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
      const templatePayload = payloadTemplate.payload || payloadTemplate;
      const excludedFields = payloadTemplate.excludedFields || [];
      const mergedPayload = JSON.parse(JSON.stringify(templatePayload));

      if ('borrowerName' in mergedPayload) mergedPayload.borrowerName = customer.name;
      if ('monthlyIncome' in mergedPayload) mergedPayload.monthlyIncome = customer.monthly_income;
      if ('creditScore' in mergedPayload) mergedPayload.creditScore = customer.credit_score;
      if ('loanAmount' in mergedPayload) mergedPayload.loanAmount = customer.remaining_balance;
      if ('appraisedValue' in mergedPayload) mergedPayload.appraisedValue = customer.property_value;
      if ('propertyZipCode' in mergedPayload) mergedPayload.propertyZipCode = customer.property_zip;
      if ('propertyState' in mergedPayload) mergedPayload.propertyState = customer.property_state;
      if ('propertyCounty' in mergedPayload) mergedPayload.propertyCounty = customer.property_county || '';

      mergedPayload.currentMonthlyPayment = customer.current_monthly_payment;

      if ('monthsOfReservesId' in mergedPayload && typeof mergedPayload.monthsOfReservesId === 'number') {
        mergedPayload.monthsOfReservesId = String(mergedPayload.monthsOfReservesId);
      }

      excludedFields.forEach(field => { delete mergedPayload[field]; });
      body = JSON.stringify([mergedPayload]);
    } else {
      body = JSON.stringify([customer]);
    }

    // Pass target container for in-page display
    handleAnalysis(body, '/api/analyze/direct?min_savings=200&target_amount=-2000', true, customerResultsSection, customerResultsContainer);
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
    window.scrollTo({ top: 0, behavior: 'smooth' });
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
    document.getElementById('saveCustomerBtn').textContent = 'Add Customer';
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
      property_county: '',
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
        document.getElementById('saveCustomerBtn').textContent = 'Add Customer';
        loadCustomers();
      }
    } catch (error) {
      console.error('Error saving customer:', error);
    }
  });

  // --- Payload Builder Logic ---
  const jsonImportText = document.getElementById('jsonImportText');
  const loadJsonBtn = document.getElementById('loadJsonBtn');

  if (loadJsonBtn) {
    loadJsonBtn.addEventListener('click', () => {
      const text = jsonImportText.value.trim();
      if (!text) return;
      try {
        const imported = JSON.parse(text);
        const payload = imported.payload || imported;
        const excludedFields = imported.excludedFields || [];

        // Get all field toggles
        const toggles = builderForm.querySelectorAll('.field-toggle');

        // First, uncheck ALL toggles (start fresh)
        toggles.forEach(toggle => {
          toggle.checked = false;
        });

        // Then, only check toggles for fields that exist in the payload
        Object.keys(payload).forEach(key => {
          const toggle = builderForm.querySelector(`.field-toggle[data-field="${key}"]`);
          if (toggle) {
            toggle.checked = true;
          }
        });

        // Additionally, handle excludedFields if provided
        if (excludedFields.length > 0) {
          excludedFields.forEach(field => {
            const toggle = builderForm.querySelector(`.field-toggle[data-field="${field}"]`);
            if (toggle) {
              toggle.checked = false;
            }
          });
        }

        // Now populate the form fields with the payload values
        Object.entries(payload).forEach(([key, value]) => {
          const field = builderForm.querySelector(`[name="${key}"]`);
          if (!field) return;

          if (field.type === 'checkbox') {
            field.checked = !!value;
          } else if (Array.isArray(value)) {
            if (field.tagName === 'SELECT' && field.multiple) {
              setSelectedValues(field, value);
            } else {
              field.value = value[0] ?? '';
            }
          } else {
            field.value = value;
          }
        });

        alert('JSON loaded successfully! Only fields present in the JSON are included.');
      } catch (e) {
        alert('Error parsing JSON: ' + e.message);
      }
    });
  }

  const savePayloadBtn = document.getElementById('savePayloadBtn');
  if (savePayloadBtn) {
    savePayloadBtn.addEventListener('click', () => {
      const name = document.getElementById('payloadName').value.trim();
      if (!name) { alert('Please enter a payload name'); return; }
      const { payload, excludedFields } = buildPayloadWithExclusions();
      const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
      saved[name] = { payload, excludedFields };
      localStorage.setItem('savedPayloads', JSON.stringify(saved));
      loadSavedPayloads();
      alert('Template saved!');
    });
  }

  const deletePayloadBtn = document.getElementById('deletePayloadBtn');
  if (deletePayloadBtn) {
    deletePayloadBtn.addEventListener('click', () => {
      const selectedName = payloadSelect.value;
      if (!selectedName) {
        alert('Please select a template to delete');
        return;
      }
      if (!confirm(`Are you sure you want to delete "${selectedName}"?`)) return;

      const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
      delete saved[selectedName];
      localStorage.setItem('savedPayloads', JSON.stringify(saved));
      loadSavedPayloads();
      alert('Template deleted!');
    });
  }

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

  function buildPayload() {
    const payload = {};
    const fields = builderForm.querySelectorAll('input[name], select[name], textarea[name]');
    fields.forEach(el => {
      const key = el.name;
      if (!key) return;
      if (el.tagName === 'SELECT' && el.multiple) payload[key] = getSelectedValues(el);
      else if (el.type === 'checkbox') payload[key] = el.checked;
      else if (el.type === 'number') payload[key] = el.value === '' ? null : Number(el.value);
      else payload[key] = el.value;
    });
    ARRAY_FIELDS.forEach(k => {
      if (payload[k] == null) return;
      if (!Array.isArray(payload[k])) payload[k] = [String(payload[k])];
      payload[k] = payload[k].map(String);
    });
    return payload;
  }

  if (builderForm) {
    builderForm.addEventListener('submit', async e => {
      e.preventDefault();
      const { payload } = buildPayloadWithExclusions();
      handleAnalysis(JSON.stringify([payload]), '/api/analyze/direct', true, resultsSection, resultsContainer);
    });
  }

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

      handleAnalysis(body, '/api/analyze', false, resultsSection, resultsContainer);
    });
  }

  const previewBtn = document.getElementById('previewBtn');
  if (previewBtn) {
    previewBtn.addEventListener('click', () => {
      const { payload } = buildPayloadWithExclusions();
      const preview = document.getElementById('jsonPreview');
      const content = document.getElementById('jsonContent');
      content.textContent = JSON.stringify(payload, null, 4);
      preview.classList.remove('hidden');
    });
  }

  const downloadBtn = document.getElementById('downloadBtn');
  if (downloadBtn) {
    downloadBtn.addEventListener('click', () => {
      const content = document.getElementById('jsonContent');
      if (!content.textContent) return;

      const blob = new Blob([content.textContent], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'payload.json';
      a.click();
      URL.revokeObjectURL(url);
    });
  }

  async function handleAnalysis(body, url, isJson, section, container) {
    section.classList.add('hidden');
    errorSection.classList.add('hidden');
    container.innerHTML = '';

    const activeTab = document.querySelector('.nav-item.active').dataset.tab;
    const currentBtn = (activeTab === 'analyze') ? submitBtn :
                       (activeTab === 'builder') ? document.getElementById('buildAnalyzeBtn') :
                       null; // Individual analysis handled by inline buttons

    if (currentBtn) {
      currentBtn.disabled = true;
      currentBtn.dataset.originalText = currentBtn.textContent;
      currentBtn.textContent = 'Analyzing...';
    }

    try {
      const options = { method: 'POST', body };
      if (isJson) options.headers = { 'Content-Type': 'application/json' };

      const response = await fetch(url, options);
      const data = await response.json();

      if (!response.ok) throw new Error(data.message || 'Analysis failed');

      displayResults(data, section, container);
    } catch (error) {
      errorMessage.textContent = error.message;
      errorSection.classList.remove('hidden');
      window.scrollTo({ top: errorSection.offsetTop, behavior: 'smooth' });
    } finally {
      if (currentBtn) {
        currentBtn.disabled = false;
        currentBtn.textContent = currentBtn.dataset.originalText;
      }
    }
  }

  function displayResults(data, section, container) {
    if (!data || data.length === 0) {
      container.innerHTML = '<p style="padding: 1rem; color: var(--text-secondary);">No qualifying products found matching your criteria.</p>';
    } else {
      data.forEach(customerResult => {
        const card = document.createElement('div');
        card.className = 'result-card';

        const scenariosHtml = (customerResult.scenarios || []).map(scenario => {
          const termGroupsHtml = (scenario.termGroups || []).map(termGroup => {
            const productsHtml = termGroup.products.map(prod => `
              <tr>
                <td>${Number.isFinite(prod.interestRate?.value) ? prod.interestRate.value.toFixed(3) : '0.000'}%</td>
                <td>$${prod.closestAmount.toLocaleString()}</td>
                <td>$${prod.matchedMonthlyPayment.toLocaleString()}</td>
                <td class="positive">$${prod.monthlySavings.toLocaleString()}</td>
              </tr>
            `).join('');

            return `
              <div style="margin-bottom: 1.5rem;">
                <h5 style="margin: 0 0 0.5rem 0; color: var(--primary-color);">${termGroup.mortgageProductName}</h5>
                <div class="table-container">
                  <table>
                    <thead>
                      <tr>
                        <th>Rate</th>
                        <th>Credit/Cost</th>
                        <th>New Pay</th>
                        <th>Savings</th>
                      </tr>
                    </thead>
                    <tbody>${productsHtml}</tbody>
                  </table>
                </div>
              </div>
            `;
          }).join('');

          return `
            <div style="flex: 1; min-width: 300px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h4 style="margin: 0; font-size: 1rem;">${scenario.scenario}</h4>
                <span class="badge badge-green">${(scenario.termGroups || []).reduce((sum, g) => sum + g.products.length, 0)} options</span>
              </div>
              ${scenario.error ? `<div class="error-msg">${scenario.error}</div>` : termGroupsHtml}
            </div>
          `;
        }).join('');

        card.innerHTML = `
          <h3 style="margin: 0 0 1rem 0; font-size: 1.25rem;">${customerResult.name}</h3>
          <div style="display: flex; gap: 2rem; margin-bottom: 1.5rem; padding: 1rem; background: var(--bg-color); border-radius: 0.5rem;">
            <div>
              <label style="color: var(--text-secondary); font-size: 0.75rem;">Current Payment</label>
              <div style="font-weight: 600;">$${customerResult.currentMonthlyPayment.toLocaleString()}</div>
            </div>
          </div>
          <div style="display: flex; flex-wrap: wrap; gap: 2rem;">
            ${scenariosHtml}
          </div>
        `;
        container.appendChild(card);
      });
    }

    section.classList.remove('hidden');
    window.scrollTo({ top: section.offsetTop - 20, behavior: 'smooth' });
  }

  // Load payload when selected from dropdown
  if (payloadSelect) {
    payloadSelect.addEventListener('change', () => {
      const selectedName = payloadSelect.value;
      if (!selectedName) return;

      const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
      const template = saved[selectedName];
      if (!template) return;

      const payload = template.payload || template;
      const excludedFields = template.excludedFields || [];

      // Get all field toggles
      const toggles = builderForm.querySelectorAll('.field-toggle');

      // First, uncheck ALL toggles
      toggles.forEach(toggle => {
        toggle.checked = false;
      });

      // Then, only check toggles for fields that exist in the payload
      Object.keys(payload).forEach(key => {
        const toggle = builderForm.querySelector(`.field-toggle[data-field="${key}"]`);
        if (toggle) {
          toggle.checked = true;
        }
      });

      // Handle excludedFields if provided
      if (excludedFields.length > 0) {
        excludedFields.forEach(field => {
          const toggle = builderForm.querySelector(`.field-toggle[data-field="${field}"]`);
          if (toggle) {
            toggle.checked = false;
          }
        });
      }

      // Populate form fields
      Object.entries(payload).forEach(([key, value]) => {
        const field = builderForm.querySelector(`[name="${key}"]`);
        if (!field) return;

        if (field.type === 'checkbox') {
          field.checked = !!value;
        } else if (Array.isArray(value)) {
          if (field.tagName === 'SELECT' && field.multiple) {
            setSelectedValues(field, value);
          } else {
            field.value = value[0] ?? '';
          }
        } else {
          field.value = value;
        }
      });

      document.getElementById('payloadName').value = selectedName;
    });
  }

  // Initial load
  loadCustomers();
});