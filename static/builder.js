// Payload Builder functionality

document.addEventListener('DOMContentLoaded', () => {
  setupEventListeners();
  loadPayloadList();
  initializeFieldStates();
});

function initializeFieldStates() {
  // Disable all fields by default since toggles are unchecked
  document.querySelectorAll('.field-toggle').forEach(toggle => {
    const fieldId = toggle.getAttribute('data-field');
    const field = document.getElementById(fieldId);
    if (field) {
      field.disabled = !toggle.checked;
      field.style.opacity = toggle.checked ? '1' : '0.5';
    }
  });
}

function setupEventListeners() {
  // New template button
  document.getElementById('newPayloadBtn').addEventListener('click', () => {
    document.getElementById('builderForm').reset();
    document.getElementById('payloadName').focus();
  });

  // Load payload
  document.getElementById('loadPayloadBtn').addEventListener('click', loadSelectedPayload);

  // ✅ Auto-load template when selected in dropdown
  document.getElementById('payloadSelect').addEventListener('change', (e) => {
    if (e.target.value) {
      loadSelectedPayload();
    }
  });

  // Delete payload
  document.getElementById('deletePayloadBtn').addEventListener('click', deleteSelectedPayload);

  // Import JSON
  document.getElementById('importJsonBtn').addEventListener('click', importFromJSON);

  // Preview JSON
  document.getElementById('previewBtn').addEventListener('click', previewJSON);

  // Close preview
  document.getElementById('closePreviewBtn').addEventListener('click', () => {
    document.getElementById('previewModal').classList.add('hidden');
  });

  // Copy JSON
  document.getElementById('copyJsonBtn').addEventListener('click', copyJSON);

  // Form submit
  document.getElementById('builderForm').addEventListener('submit', handleSavePayload);

  // Field toggles - disable/enable fields
  document.querySelectorAll('.field-toggle').forEach(toggle => {
    toggle.addEventListener('change', (e) => {
      const fieldId = e.target.getAttribute('data-field');
      const field = document.getElementById(fieldId);
      if (field) {
        field.disabled = !e.target.checked;
        field.style.opacity = e.target.checked ? '1' : '0.5';
      }
    });
  });
}

function loadPayloadList() {
  const select = document.getElementById('payloadSelect');
  const payloads = getSavedPayloads();

  select.innerHTML = '<option value="">-- Select a Template --</option>' +
    Object.keys(payloads).map(name => `<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`).join('');
}

function loadSelectedPayload() {
  const select = document.getElementById('payloadSelect');
  const payloadName = select.value;

  if (!payloadName) {
    showToast('Please select a template to load', 'error');
    return;
  }

  const payloads = getSavedPayloads();
  const payload = payloads[payloadName];

  if (!payload) {
    showToast('Template not found', 'error');
    return;
  }

  // First, uncheck ALL field toggles and disable fields
  document.querySelectorAll('.field-toggle').forEach(toggle => {
    toggle.checked = false;
    const fieldId = toggle.getAttribute('data-field');
    const field = document.getElementById(fieldId);
    if (field) {
      field.disabled = true;
      field.style.opacity = '0.5';
    }
  });

  // Load payload into form
  document.getElementById('payloadName').value = payloadName;

  // Populate and enable only fields that exist in the payload
  Object.keys(payload).forEach(key => {
    const field = document.getElementById(key);
    const toggle = document.querySelector(`.field-toggle[data-field="${key}"]`);

    if (field && toggle) {
      // Enable the toggle
      toggle.checked = true;
      field.disabled = false;
      field.style.opacity = '1';

      // Set the value
      const value = payload[key];

      if (field.type === 'checkbox') {
        field.checked = !!value;
      } else if (field.tagName === 'SELECT' && field.multiple) {
        // Handle multi-select
        const values = Array.isArray(value) ? value : [value];
        Array.from(field.options).forEach(option => {
          option.selected = values.includes(parseInt(option.value)) || values.includes(option.value);
        });
      } else {
        field.value = value;
      }
    }
  });

  showToast(`Template "${payloadName}" loaded with ${Object.keys(payload).length} fields`, 'success');
}

function deleteSelectedPayload() {
  const select = document.getElementById('payloadSelect');
  const payloadName = select.value;

  if (!payloadName) {
    showToast('Please select a template to delete', 'error');
    return;
  }

  if (!confirm(`Are you sure you want to delete the template "${payloadName}"?`)) {
    return;
  }

  deletePayload(payloadName);
  loadPayloadList();
  document.getElementById('builderForm').reset();
  showToast('Template deleted successfully', 'success');
}

function importFromJSON() {
  const jsonText = document.getElementById('jsonImport').value.trim();

  if (!jsonText) {
    showToast('Please paste JSON to import', 'error');
    return;
  }

  try {
    const payload = JSON.parse(jsonText);

    // First, uncheck ALL field toggles and disable all fields
    document.querySelectorAll('.field-toggle').forEach(toggle => {
      toggle.checked = false;
      const fieldId = toggle.getAttribute('data-field');
      const field = document.getElementById(fieldId);
      if (field) {
        field.disabled = true;
        field.style.opacity = '0.5';
      }
    });

    // Now, only populate and enable fields that exist in the JSON
    Object.keys(payload).forEach(key => {
      const field = document.getElementById(key);
      const toggle = document.querySelector(`.field-toggle[data-field="${key}"]`);

      if (field && toggle) {
        // Enable the toggle
        toggle.checked = true;
        field.disabled = false;
        field.style.opacity = '1';

        // Set the value
        const value = payload[key];

        if (field.type === 'checkbox') {
          field.checked = !!value;
        } else if (field.tagName === 'SELECT' && field.multiple) {
          // Handle multi-select
          const values = Array.isArray(value) ? value : [value];
          Array.from(field.options).forEach(option => {
            option.selected = values.includes(parseInt(option.value)) || values.includes(option.value);
          });
        } else {
          field.value = value;
        }
      }
    });

    document.getElementById('jsonImport').value = '';
    showToast(`JSON imported successfully - ${Object.keys(payload).length} fields enabled`, 'success');
  } catch (error) {
    showToast('Invalid JSON format: ' + error.message, 'error');
  }
}

function populateFormFromPayload(payload) {
  // Iterate through all form fields
  Object.keys(payload).forEach(key => {
    const field = document.getElementById(key);
    if (field) {
      const value = payload[key];

      if (field.type === 'checkbox') {
        // Boolean checkbox
        field.checked = !!value;
      } else if (field.tagName === 'SELECT' && field.multiple) {
        // Multi-select
        const values = Array.isArray(value) ? value : [value];
        Array.from(field.options).forEach(option => {
          // Compare as strings and numbers
          const optVal = option.value;
          option.selected = values.some(v =>
            String(v) === String(optVal) ||
            Number(v) === Number(optVal)
          );
        });
      } else if (field.tagName === 'SELECT') {
        // Single select - set value as string
        field.value = String(value);
      } else {
        // Text, number, email, etc.
        field.value = value;
      }
    }
  });
}

function previewJSON() {
  const payload = buildPayloadFromForm();
  const modal = document.getElementById('previewModal');
  const preview = document.getElementById('jsonPreview');

  preview.textContent = JSON.stringify(payload, null, 2);
  modal.classList.remove('hidden');
}

function copyJSON() {
  const preview = document.getElementById('jsonPreview');
  const text = preview.textContent;

  navigator.clipboard.writeText(text).then(() => {
    showToast('JSON copied to clipboard', 'success');
  }).catch(() => {
    showToast('Failed to copy JSON', 'error');
  });
}

function handleSavePayload(e) {
  e.preventDefault();

  const payloadName = document.getElementById('payloadName').value.trim();

  if (!payloadName) {
    showToast('Please enter a template name', 'error');
    return;
  }

  const payload = buildPayloadFromForm();

  // Check if overwriting
  const payloads = getSavedPayloads();
  if (payloads[payloadName]) {
    if (!confirm(`Template "${payloadName}" already exists. Overwrite it?`)) {
      return;
    }
  }

  savePayload(payloadName, payload);
  loadPayloadList();

  // Select the newly saved payload
  document.getElementById('payloadSelect').value = payloadName;

  showToast('Template saved successfully', 'success');
}

function buildPayloadFromForm() {
  const payload = {};

  // Get all field toggles
  const toggles = document.querySelectorAll('.field-toggle');

  toggles.forEach(toggle => {
    if (!toggle.checked) return; // Skip disabled fields

    const fieldId = toggle.getAttribute('data-field');
    const field = document.getElementById(fieldId);

    if (!field) return;

    let value;

    if (field.type === 'checkbox') {
      // Boolean checkbox field
      value = field.checked;
    } else if (field.tagName === 'SELECT' && field.multiple) {
      // Multi-select: return array, preserve string/number type from options
      value = Array.from(field.selectedOptions).map(option => {
        const val = option.value;
        // Check if the original value in the option is numeric
        return /^\d+$/.test(val) ? parseInt(val) : val;
      });
    } else if (field.tagName === 'SELECT') {
      // Single select: preserve as string or number based on value
      const val = field.value;
      if (val === '') {
        value = '';
      } else if (/^\d+$/.test(val)) {
        value = parseInt(val);
      } else {
        value = val;
      }
    } else if (field.type === 'number') {
      // Number input
      const val = field.value;
      value = val === '' ? null : parseFloat(val);
    } else {
      // Text, email, etc - keep as string
      value = field.value;
    }

    payload[fieldId] = value;
  });

  return payload;
}

function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
