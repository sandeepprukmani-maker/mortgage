<template>
  <DashboardLayout page-title="Coming Soon">
    <div class="coming-soon-content">
      <div class="coming-soon-card">
        <div class="icon-wrapper">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
          </svg>
        </div>
        <h1 class="coming-soon-title">Coming Soon</h1>
        <p class="coming-soon-text">
          We're working hard to bring you this feature. Stay tuned for updates!
        </p>
        <router-link to="/dashboard" class="back-link">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back to Dashboard
        </router-link>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from '../layouts/DashboardLayout.vue';
</script>

<style scoped>
.coming-soon-content {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 200px);
}

.coming-soon-card {
  text-align: center;
  padding: 48px;
  background-color: var(--color-shade-white);
  border-radius: 16px;
  box-shadow: var(--shadow-card);
  max-width: 480px;
}

.icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  background: linear-gradient(135deg, var(--color-primary-100), var(--color-primary-200));
  border-radius: 50%;
}

.icon-wrapper svg {
  width: 40px;
  height: 40px;
  color: var(--color-primary-600);
}

.coming-soon-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-neutral-900);
  margin: 0 0 12px;
}

.coming-soon-text {
  font-size: 16px;
  color: var(--color-neutral-500);
  margin: 0 0 32px;
  line-height: 1.6;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-shade-white);
  background-color: var(--color-primary-600);
  border-radius: 8px;
  text-decoration: none;
  transition: background-color 0.2s ease;
}

.back-link:hover {
  background-color: var(--color-primary-700);
}

.back-link svg {
  width: 18px;
  height: 18px;
}
</style>
