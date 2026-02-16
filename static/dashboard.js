// Dashboard page functionality

document.addEventListener('DOMContentLoaded', async () => {
  await loadDashboardStats();
  loadRecentActivity();
});

async function loadDashboardStats() {
  try {
    // Load customers count
    const customers = await apiCall('/api/customers');
    document.getElementById('totalCustomers').textContent = customers.length;

    // Load saved payloads count
    const payloads = getSavedPayloads();
    document.getElementById('savedPayloads').textContent = Object.keys(payloads).length;

    // Calculate qualified leads (mock for now - would need to store this)
    document.getElementById('qualifiedLeads').textContent = '0';

    // Calculate average savings (mock)
    document.getElementById('avgSavings').textContent = '$0';

  } catch (error) {
    console.error('Error loading dashboard stats:', error);
  }
}

function loadRecentActivity() {
  const activityList = document.getElementById('recentActivity');

  // For now, show empty state
  // In a real app, you'd fetch activity from the backend
  activityList.innerHTML = `
    <div class="activity-empty">
      <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
        <circle cx="24" cy="24" r="20" stroke="currentColor" stroke-width="2" opacity="0.2"/>
        <path d="M24 16v8l5 3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
      <p>No recent activity</p>
    </div>
  `;
}