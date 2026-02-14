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

    function loadSavedPayloads() {
        const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
        const options = '<option value="">-- Select a Payload --</option>' + 
            Object.keys(saved).map(name => `<option value="${name}">${name}</option>`).join('');
        
        payloadSelect.innerHTML = options;
        if (analyzePayloadSelect) analyzePayloadSelect.innerHTML = options;
    }

    loadSavedPayloads();

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(`${btn.dataset.tab}Section`).classList.add('active');
            if (btn.dataset.tab === 'customers') {
                loadCustomers();
            }
        });
    });

    // Customer Management
    const customerForm = document.getElementById('customerForm');
    const customerTableBody = document.getElementById('customerTableBody');
    const cancelCustomerBtn = document.getElementById('cancelCustomerBtn');

    async function loadCustomers() {
        try {
            const response = await fetch('/api/customers');
            const customers = await response.json();
            customerTableBody.innerHTML = customers.map(c => `
                <tr>
                    <td>${c.name}</td>
                    <td>$${c.monthly_income.toLocaleString()}</td>
                    <td>$${c.current_monthly_payment.toLocaleString()}</td>
                    <td>${c.credit_score}</td>
                    <td>
                        <button class="secondary-btn btn-sm" onclick="editCustomer(${JSON.stringify(c).replace(/"/g, '&quot;')})">Edit</button>
                        <button class="secondary-btn btn-sm delete-btn" onclick="deleteCustomer(${c.id})">Delete</button>
                    </td>
                </tr>
            `).join('');
        } catch (error) {
            console.error('Error loading customers:', error);
        }
    }

    window.editCustomer = (customer) => {
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

    window.deleteCustomer = async (id) => {
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

    customerForm.addEventListener('submit', async (e) => {
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
            property_county: '' // Optional for now
        };

        try {
            const url = id ? `/api/customers/${id}` : '/api/customers';
            const method = id ? 'PUT' : 'POST';
            const response = await fetch(url, {
                method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
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

    // Load Payload
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
            } else if (Array.isArray(value)) {
                field.value = value[0];
            } else {
                field.value = value;
            }
        });

        // Set toggles
        const toggles = builderForm.querySelectorAll('.field-toggle');
        toggles.forEach(toggle => {
            const fieldName = toggle.dataset.field;
            toggle.checked = !excludedFields.includes(fieldName);
        });
    });

    // Save Payload
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

    // Builder Analysis
    builderForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const { payload } = buildPayloadWithExclusions();
        // Wrap in list since backend expects a list of customers
        handleAnalysis(JSON.stringify([payload]), '/api/analyze/direct', true);
    });

    // Database Analysis Form
    if (analyzeForm) {
        analyzeForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(analyzeForm);
            const payloadName = formData.get('analyzePayloadSelect');
            const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
            const payloadTemplate = saved[payloadName] ? JSON.stringify(saved[payloadName]) : '';

            const body = new FormData();
            body.append('min_savings', formData.get('min_savings'));
            body.append('target_amount', formData.get('target_amount'));
            body.append('tolerance', formData.get('tolerance'));
            if (payloadTemplate) {
                body.append('base_payload', payloadTemplate);
            }

            handleAnalysis(body, '/api/analyze');
        });
    }

    // Preview JSON
    document.getElementById('previewBtn').addEventListener('click', () => {
        const { payload } = buildPayloadWithExclusions();
        const preview = document.getElementById('jsonPreview');
        const content = document.getElementById('jsonContent');
        content.textContent = JSON.stringify(payload, null, 4);
        preview.classList.remove('hidden');
    });

    // Download JSON
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

    function buildPayload() {
        const formData = new FormData(builderForm);
        const payload = {};
        formData.forEach((value, key) => {
            if (key === 'loanTypeIds' || key === 'loanTermIds' || key === 'waivableFeeTypeIds') {
                payload[key] = [value];
            } else if (value === 'true' || value === 'on') {
                payload[key] = true;
            } else if (value === 'false') {
                payload[key] = false;
            } else if (!isNaN(value) && value.trim() !== '' && key !== 'propertyZipCode') {
                payload[key] = Number(value);
            } else {
                payload[key] = value;
            }
        });
        
        // Handle checkboxes explicitly if not checked
        const checkboxes = builderForm.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(cb => {
            if (!cb.checked) payload[cb.name] = false;
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

            const productsHtml = customerResult.products.map(prod => `
                <tr>
                    <td>${prod.mortgageProductName}<br><small>${prod.mortgageProductAlias || ''}</small></td>
                    <td>${(prod.interestRate * 100).toFixed(3)}%</td>
                    <td>$${prod.closestAmount.toLocaleString()}</td>
                    <td>$${prod.matchedMonthlyPayment.toLocaleString()}</td>
                    <td class="positive">$${prod.monthlySavings.toLocaleString()}</td>
                </tr>
            `).join('');

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
