<template>
  <DashboardLayout page-title="Settings">
    <div class="settings-content">
      <!-- UWM Integration Card -->
      <div class="uwm-card">
        <!-- Header -->
        <div class="uwm-card-header">
          <h2 class="uwm-title">UWM</h2>
          <BaseButton
            @click="testConnection"
            :loading="loading"
            :disabled="loading"
            size="sm"
          >
            Test Connection
          </BaseButton>
        </div>

        <!-- Body - Log Display -->
        <div class="uwm-card-body">
          <div v-if="!hasRun" class="placeholder-text">
            Click 'Test Connection' to verify UWM API connectivity
          </div>
          <pre v-else class="log-display">{{ formattedLogs }}</pre>
        </div>

        <!-- Footer - Summary Table -->
        <div v-if="hasRun && connectionResult" class="uwm-card-footer">
          <h3 class="summary-title">Summary</h3>
          <table class="summary-table">
            <tbody>
              <tr>
                <td class="summary-label">Outgoing IP</td>
                <td class="summary-value">{{ connectionResult.outgoing_ip || 'Unknown' }}</td>
              </tr>
              <tr>
                <td class="summary-label">Client ID</td>
                <td class="summary-value">{{ connectionResult.client_id || 'Not configured' }}</td>
              </tr>
              <tr>
                <td class="summary-label">Scope</td>
                <td class="summary-value">{{ connectionResult.scope || 'Not configured' }}</td>
              </tr>
              <tr>
                <td class="summary-label">Grant Type</td>
                <td class="summary-value">{{ connectionResult.grant_type || 'N/A' }}</td>
              </tr>
              <tr>
                <td class="summary-label">Status</td>
                <td class="summary-value">
                  <span v-if="connectionResult.success" class="status-success">
                    <span class="status-icon success">&#x2705;</span> Connection successful
                  </span>
                  <span v-else class="status-error">
                    <span class="status-icon error">&#x274C;</span> {{ connectionResult.error || 'Connection failed' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed } from 'vue';
import DashboardLayout from '../layouts/DashboardLayout.vue';
import BaseButton from '../components/ui/BaseButton.vue';
import { uwmService } from '../services/uwmService';

const loading = ref(false);
const logs = ref([]);
const connectionResult = ref(null);
const hasRun = ref(false);

const formattedLogs = computed(() => {
  return logs.value.join('\n');
});

const testConnection = async () => {
  loading.value = true;
  logs.value = [];
  connectionResult.value = null;

  try {
    const result = await uwmService.testConnection();
    connectionResult.value = result;
    logs.value = result.logs || [];
    hasRun.value = true;
  } catch (error) {
    connectionResult.value = {
      success: false,
      error: typeof error === 'string' ? error : 'Failed to test connection',
      logs: [],
      outgoing_ip: null,
      client_id: '',
      scope: '',
      grant_type: ''
    };
    logs.value = [`ERROR: ${typeof error === 'string' ? error : 'Failed to test connection'}`];
    hasRun.value = true;
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.settings-content {
  max-width: 800px;
  margin: 0 auto;
}

.uwm-card {
  background-color: var(--color-shade-white);
  border-radius: 12px;
  box-shadow: var(--shadow-card);
  overflow: hidden;
}

.uwm-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-neutral-200);
}

.uwm-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-neutral-900);
  margin: 0;
}

.uwm-card-body {
  padding: 24px;
  background-color: var(--color-neutral-50);
  min-height: 200px;
  max-height: 400px;
  overflow-y: auto;
}

.placeholder-text {
  color: var(--color-neutral-500);
  font-size: 14px;
  text-align: center;
  padding: 60px 20px;
}

.log-display {
  font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
  font-size: 12px;
  line-height: 1.6;
  color: var(--color-neutral-800);
  background-color: var(--color-neutral-100);
  padding: 16px;
  border-radius: 8px;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
}

.uwm-card-footer {
  padding: 20px 24px;
  border-top: 1px solid var(--color-neutral-200);
}

.summary-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-neutral-700);
  margin: 0 0 12px 0;
}

.summary-table {
  width: 100%;
  border-collapse: collapse;
}

.summary-table tr {
  border-bottom: 1px solid var(--color-neutral-100);
}

.summary-table tr:last-child {
  border-bottom: none;
}

.summary-label {
  padding: 8px 12px 8px 0;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-neutral-600);
  width: 120px;
  vertical-align: top;
}

.summary-value {
  padding: 8px 0;
  font-size: 13px;
  color: var(--color-neutral-800);
  word-break: break-all;
}

.status-icon {
  margin-left: 8px;
}

.status-icon.success {
  color: var(--color-success-600, #16a34a);
}

.status-icon.error {
  color: var(--color-error-600, #dc2626);
}

.status-success {
  color: var(--color-success-600, #16a34a);
  font-weight: 500;
}

.status-error {
  color: var(--color-error-600, #dc2626);
  font-weight: 500;
}
</style>
