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
        });
    });

    // Save Payload
    document.getElementById('savePayloadBtn').addEventListener('click', () => {
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
        payloadSelect.value = name;
        alert('Payload saved successfully!');
    });

    // Load Payload
    payloadSelect.addEventListener('change', () => {
        const name = payloadSelect.value;
        if (!name) return;
        const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
        const payload = saved[name];
        if (!payload) return;

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
    });

    // Delete Payload
    document.getElementById('deletePayloadBtn').addEventListener('click', () => {
        const name = payloadSelect.value;
        if (!name) return;
        if (!confirm(`Are you sure you want to delete "${name}"?`)) return;

        const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
        delete saved[name];
        localStorage.setItem('savedPayloads', JSON.stringify(saved));
        loadSavedPayloads();
        builderForm.reset();
    });

    // File Analysis
    analyzeForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const fileInput = document.getElementById('file');
        const selectedPayloadName = analyzePayloadSelect.value;
        const saved = JSON.parse(localStorage.getItem('savedPayloads') || '{}');
        const basePayload = selectedPayloadName ? saved[selectedPayloadName] : {};
        
        if (fileInput.files.length > 0) {
            const formData = new FormData(analyzeForm);
            // Append base payload if selected
            formData.append('base_payload', JSON.stringify(basePayload));
            handleAnalysis(formData, '/api/analyze');
        } else if (selectedPayloadName) {
            const payload = basePayload;
            
            const minSavings = document.getElementById('min_savings').value;
            const targetAmount = document.getElementById('target_amount').value;
            const tolerance = document.getElementById('tolerance').value;
            
            const url = `/api/analyze/direct?min_savings=${minSavings}&target_amount=${targetAmount}&tolerance=${tolerance}`;
            handleAnalysis(JSON.stringify([payload]), url, true);
        } else {
            alert('Please select a file or a saved payload');
        }
    });

    // Builder Analysis
    builderForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = buildPayload();
        // Wrap in list since backend expects a list of customers
        handleAnalysis(JSON.stringify([payload]), '/api/analyze/direct', true);
    });

    // Preview JSON
    document.getElementById('previewBtn').addEventListener('click', () => {
        const payload = buildPayload();
        const preview = document.getElementById('jsonPreview');
        const content = document.getElementById('jsonContent');
        content.textContent = JSON.stringify(payload, null, 4);
        preview.classList.remove('hidden');
    });

    // Download JSON
    document.getElementById('downloadBtn').addEventListener('click', () => {
        const payload = buildPayload();
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
