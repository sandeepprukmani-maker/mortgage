// Customers page functionality

let allCustomers = [];
let currentEditingKey = null;

document.addEventListener('DOMContentLoaded', () => {
  setupEventListeners();
  loadCustomers();
});

function setupEventListeners() {
  // Add customer button
  document.getElementById('addCustomerBtn').addEventListener('click', () => {
    openCustomerForm();
  });

  // Close form buttons
  document.getElementById('closeFormBtn').addEventListener('click', closeCustomerForm);
  document.getElementById('cancelFormBtn').addEventListener('click', closeCustomerForm);

  // Customer form submit
  document.getElementById('customerForm').addEventListener('submit', handleCustomerSubmit);

  // Search functionality
  const searchInput = document.getElementById('customerSearch');
  searchInput.addEventListener('input', debounce((e) => {
    filterCustomers(e.target.value);
  }, 300));

  // Zip code lookup
  const zipInput = document.getElementById('cZip');
  zipInput.addEventListener('blur', handleZipLookup);

  // Check for action in URL
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('action') === 'add') {
    openCustomerForm();
  }
}

function openCustomerForm(customer = null) {
  const modal = document.getElementById('customerFormModal');
  const title = document.getElementById('formTitle');
  const form = document.getElementById('customerForm');

  if (customer) {
    // Edit mode
    title.textContent = 'Edit Customer';
    currentEditingKey = customer.customer_key;

    document.getElementById('customerKey').value = customer.customer_key;
    document.getElementById('cName').value = customer.name || '';
    document.getElementById('cPhone').value = customer.phone || '';
    document.getElementById('cEmail').value = customer.email || '';
    document.getElementById('cPayment').value = customer.current_monthly_payment || '';
    document.getElementById('cBalance').value = customer.remaining_balance || '';
    document.getElementById('cValue').value = customer.property_value || '';
    document.getElementById('cScore').value = customer.credit_score || '';
    document.getElementById('cIncome').value = customer.monthly_income || '';
    document.getElementById('cZip').value = customer.property_zip || '';
    document.getElementById('cState').value = customer.property_state || '';
    document.getElementById('cCounty').value = customer.property_county || '';
  } else {
    // Add mode
    title.textContent = 'Add New Customer';
    currentEditingKey = null;
    form.reset();
    document.getElementById('zipStatus').textContent = '';
  }

  modal.classList.remove('hidden');
}

function closeCustomerForm() {
  const modal = document.getElementById('customerFormModal');
  modal.classList.add('hidden');
  currentEditingKey = null;
  document.getElementById('customerForm').reset();
}

async function handleCustomerSubmit(e) {
  e.preventDefault();

  const customerData = {
    name: document.getElementById('cName').value,
    phone: document.getElementById('cPhone').value,
    email: document.getElementById('cEmail').value,
    current_monthly_payment: parseFloat(document.getElementById('cPayment').value),
    remaining_balance: parseFloat(document.getElementById('cBalance').value),
    property_value: parseFloat(document.getElementById('cValue').value),
    credit_score: parseInt(document.getElementById('cScore').value),
    monthly_income: parseFloat(document.getElementById('cIncome').value),
    property_zip: document.getElementById('cZip').value,
    property_state: document.getElementById('cState').value,
    property_county: document.getElementById('cCounty').value
  };

  try {
    if (currentEditingKey) {
      // Update existing customer
      await apiCall(`/api/customers/${currentEditingKey}`, {
        method: 'PUT',
        body: JSON.stringify(customerData)
      });
      showToast('Customer updated successfully', 'success');
    } else {
      // Add new customer
      await apiCall('/api/customers', {
        method: 'POST',
        body: JSON.stringify(customerData)
      });
      showToast('Customer added successfully', 'success');
    }

    closeCustomerForm();
    loadCustomers();
  } catch (error) {
    showToast(`Error: ${error.message}`, 'error');
  }
}

async function loadCustomers() {
  const tbody = document.getElementById('customerTableBody');

  try {
    const customers = await apiCall('/api/customers');
    allCustomers = customers;

    if (customers.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="7" style="text-align: center; padding: 3rem; color: var(--text-secondary);">
            <div style="display: flex; flex-direction: column; align-items: center; gap: 1rem;">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <path d="M38 40v-4a8 8 0 00-8-8H18a8 8 0 00-8 8v4M24 16a8 8 0 100-16 8 8 0 000 16z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <div>
                <div style="font-weight: 600; margin-bottom: 0.25rem;">No customers yet</div>
                <div style="font-size: 0.875rem;">Click "Add Customer" to get started</div>
              </div>
            </div>
          </td>
        </tr>
      `;
      return;
    }

    renderCustomers(customers);
  } catch (error) {
    tbody.innerHTML = `
      <tr>
        <td colspan="7" style="text-align: center; padding: 2rem; color: var(--danger-color);">
          Error loading customers: ${error.message}
        </td>
      </tr>
    `;
  }
}

function renderCustomers(customers) {
  const tbody = document.getElementById('customerTableBody');

  tbody.innerHTML = customers.map(customer => `
    <tr>
      <td>
        <div style="font-weight: 600;">${escapeHtml(customer.name)}</div>
        <div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.125rem;">
          ID: ${escapeHtml(customer.customer_key.substring(0, 8))}...
        </div>
      </td>
      <td>
        ${customer.phone ? `<div>${formatPhone(customer.phone)}</div>` : ''}
        ${customer.email ? `<div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.125rem;">${escapeHtml(customer.email)}</div>` : ''}
      </td>
      <td><strong>${formatCurrency(customer.current_monthly_payment)}</strong></td>
      <td>
        <span class="badge ${getCreditScoreBadgeClass(customer.credit_score)}">
          ${customer.credit_score || 'N/A'}
        </span>
      </td>
      <td>${formatCurrency(customer.property_value)}</td>
      <td>
        <span class="badge info">v${customer.version}</span>
      </td>
      <td>
        <div class="action-buttons">
          <button class="table-btn primary" onclick="viewCustomerHistory('${customer.customer_key}')">
            History
          </button>
          <button class="table-btn primary" onclick="editCustomer('${customer.customer_key}')">
            Edit
          </button>
          <button class="table-btn secondary" onclick="analyzeCustomer('${customer.customer_key}')">
            Analyze
          </button>
          <button class="table-btn danger" onclick="deleteCustomer('${customer.customer_key}', '${escapeHtml(customer.name)}')">
            Delete
          </button>
        </div>
      </td>
    </tr>
  `).join('');
}

function filterCustomers(searchTerm) {
  if (!searchTerm) {
    renderCustomers(allCustomers);
    return;
  }

  const term = searchTerm.toLowerCase();
  const filtered = allCustomers.filter(customer =>
    customer.name?.toLowerCase().includes(term) ||
    customer.email?.toLowerCase().includes(term) ||
    customer.phone?.includes(term) ||
    customer.customer_key?.toLowerCase().includes(term)
  );

  renderCustomers(filtered);
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

window.editCustomer = function(customerKey) {
  const customer = allCustomers.find(c => c.customer_key === customerKey);
  if (customer) {
    openCustomerForm(customer);
  }
};

window.deleteCustomer = async function(customerKey, customerName) {
  if (!confirm(`Are you sure you want to delete customer "${customerName}"? This will mark them as inactive.`)) {
    return;
  }

  try {
    await apiCall(`/api/customers/${customerKey}`, {
      method: 'DELETE'
    });
    showToast('Customer deleted successfully', 'success');
    loadCustomers();
  } catch (error) {
    showToast(`Error: ${error.message}`, 'error');
  }
};

window.viewCustomerHistory = async function(customerKey) {
  const modal = document.getElementById('historyModal');
  const title = document.getElementById('historyTitle');
  const content = document.getElementById('historyContent');

  const customer = allCustomers.find(c => c.customer_key === customerKey);
  title.textContent = `History: ${customer?.name || 'Customer'}`;

  content.innerHTML = '<div class="table-loading"><div class="spinner-small"></div><span>Loading history...</span></div>';
  modal.classList.remove('hidden');

  try {
    const history = await apiCall(`/api/customers/${customerKey}/history`);

    content.innerHTML = `
      <div class="data-table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Version</th>
              <th>Effective Date</th>
              <th>End Date</th>
              <th>Payment</th>
              <th>Balance</th>
              <th>Credit Score</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            ${history.map(h => `
              <tr>
                <td><span class="badge info">v${h.version}</span></td>
                <td>${new Date(h.effective_date).toLocaleDateString()}</td>
                <td>${h.end_date ? new Date(h.end_date).toLocaleDateString() : '-'}</td>
                <td>${formatCurrency(h.current_monthly_payment)}</td>
                <td>${formatCurrency(h.remaining_balance)}</td>
                <td>${h.credit_score || 'N/A'}</td>
                <td>
                  <span class="badge ${h.is_current ? 'success' : 'info'}">
                    ${h.is_current ? 'Current' : 'Historical'}
                  </span>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `;
  } catch (error) {
    content.innerHTML = `<div style="color: var(--danger-color); text-align: center; padding: 2rem;">Error loading history: ${error.message}</div>`;
  }

  document.getElementById('closeHistoryBtn').onclick = () => {
    modal.classList.add('hidden');
  };
};

window.analyzeCustomer = function(customerKey) {
  // Redirect to analysis page with customer key
  window.location.href = `/analysis.html?customer=${customerKey}`;
};

async function handleZipLookup() {
  const zipInput = document.getElementById('cZip');
  const zipStatus = document.getElementById('zipStatus');
  const zip = zipInput.value.trim();

  if (!zip || zip.length !== 5) {
    zipStatus.textContent = '';
    return;
  }

  zipStatus.textContent = 'Looking up...';
  zipStatus.style.color = 'var(--text-secondary)';

  try {
    const data = await apiCall(`/api/zipcode/${zip}`);

    if (data.success) {
      document.getElementById('cState').value = data.state || '';
      document.getElementById('cCounty').value = data.county || '';
      document.getElementById('cCity').value = data.city || '';
      zipStatus.textContent = `✓ ${data.city}, ${data.state}`;
      zipStatus.style.color = 'var(--success-color)';
    } else {
      zipStatus.textContent = '✗ Zip code not found';
      zipStatus.style.color = 'var(--danger-color)';
    }
  } catch (error) {
    zipStatus.textContent = '✗ Lookup failed';
    zipStatus.style.color = 'var(--danger-color)';
  }
}