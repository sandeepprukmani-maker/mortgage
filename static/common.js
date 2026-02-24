// Common utilities and API functions

const API_BASE = '';

// ====================================
// API Helper Functions
// ====================================

async function apiCall(endpoint, options = {}) {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Request failed' }));
      throw new Error(error.error || `HTTP ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

// ====================================
// Payload Storage Functions (Server-side, persistent)
// ====================================

async function getSavedPayloads() {
  try {
    const list = await apiCall('/api/payloads');
    // Return as { name: payload_data } map for backwards compatibility
    const map = {};
    for (const item of list) {
      map[item.name] = item.payload_data;
    }
    return map;
  } catch (e) {
    console.error('Failed to load payloads:', e);
    return {};
  }
}

async function savePayload(name, payload) {
  await apiCall('/api/payloads', {
    method: 'POST',
    body: JSON.stringify({ name, payload_data: payload }),
  });
}

async function deletePayload(name) {
  await apiCall(`/api/payloads/by-name/${encodeURIComponent(name)}`, {
    method: 'DELETE',
  });
}

// ====================================
// Formatting Functions
// ====================================

function formatCurrency(value) {
  if (value === null || value === undefined) return '$0';
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value);
}

function formatNumber(value) {
  if (value === null || value === undefined) return '0';
  return new Intl.NumberFormat('en-US').format(value);
}

function formatPercent(value) {
  if (value === null || value === undefined) return '0%';
  return `${value.toFixed(2)}%`;
}

function formatPhone(phone) {
  if (!phone) return '';
  const cleaned = phone.replace(/\D/g, '');
  if (cleaned.length === 10) {
    return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
  }
  return phone;
}

// ====================================
// Toast Notifications
// ====================================

function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;

  const style = document.createElement('style');
  style.textContent = `
    .toast {
      position: fixed;
      bottom: 2rem;
      right: 2rem;
      padding: 1rem 1.5rem;
      background: white;
      border-radius: 8px;
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
      z-index: 9999;
      animation: slideIn 0.3s ease-out;
      max-width: 400px;
    }

    .toast-success {
      border-left: 4px solid #10b981;
    }

    .toast-error {
      border-left: 4px solid #ef4444;
    }

    .toast-info {
      border-left: 4px solid #3b82f6;
    }

    @keyframes slideIn {
      from {
        transform: translateX(100%);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
  `;

  if (!document.querySelector('style[data-toast]')) {
    style.setAttribute('data-toast', 'true');
    document.head.appendChild(style);
  }

  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'slideIn 0.3s ease-out reverse';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// ====================================
// Navigation Active State
// ====================================

function updateNavigation() {
  const currentPath = window.location.pathname;
  const navItems = document.querySelectorAll('.nav-item');

  navItems.forEach(item => {
    const href = item.getAttribute('href');
    if (currentPath === href || (currentPath === '/index.html' && href === '/')) {
      item.classList.add('active');
    } else {
      item.classList.remove('active');
    }
  });
}

// Initialize navigation on page load
document.addEventListener('DOMContentLoaded', updateNavigation);

// ====================================
// Debounce Utility
// ====================================

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// ====================================
// CSV Export
// ====================================

function exportToCSV(data, filename) {
  if (!data || data.length === 0) {
    showToast('No data to export', 'error');
    return;
  }

  const headers = Object.keys(data[0]);
  const csv = [
    headers.join(','),
    ...data.map(row =>
      headers.map(header => {
        const value = row[header];
        // Escape quotes and wrap in quotes if contains comma
        if (value === null || value === undefined) return '';
        const stringValue = String(value);
        if (stringValue.includes(',') || stringValue.includes('"')) {
          return `"${stringValue.replace(/"/g, '""')}"`;
        }
        return stringValue;
      }).join(',')
    )
  ].join('\n');

  const blob = new Blob([csv], { type: 'text/csv' });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);

  showToast('Export successful', 'success');
}