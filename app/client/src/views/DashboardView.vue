<template>
  <DashboardLayout page-title="Dashboard">
    <div class="dashboard-content">
      <!-- Welcome Header -->
      <header class="welcome-header">
        <div>
          <h1 class="welcome-title">Welcome back, {{ userProfile?.first_name || 'User' }}!</h1>
          <p class="welcome-subtitle">Here's what's happening with your mortgage automation today.</p>
        </div>
      </header>

      <!-- Stats Cards Row -->
      <div class="stats-grid">
        <StatsCard
          title="Total Applications"
          :value="1247"
          :change="12.5"
          change-type="positive"
          icon="solar:document-add-bold-duotone"
          icon-color="primary"
        />
        <StatsCard
          title="Approved Loans"
          :value="856"
          :change="8.2"
          change-type="positive"
          icon="solar:check-circle-bold-duotone"
          icon-color="success"
        />
        <StatsCard
          title="Pending Review"
          :value="124"
          :change="-3.4"
          change-type="negative"
          icon="solar:clock-circle-bold-duotone"
          icon-color="warning"
        />
        <StatsCard
          title="Total Volume"
          value="$24.8M"
          :change="15.3"
          change-type="positive"
          icon="solar:wallet-bold-duotone"
          icon-color="info"
        />
      </div>

      <!-- Charts Row -->
      <div class="charts-grid">
        <div class="chart-main">
          <RevenueChart
            title="Loan Volume Overview"
            subtitle="Monthly loan processing volume"
          />
        </div>
        <div class="chart-side">
          <UserOverview
            title="Application Status"
            :labels="['Approved', 'In Review', 'Pending']"
          />
        </div>
      </div>

      <!-- Activity Row -->
      <div class="activity-grid">
        <div class="activity-main">
          <RecentActivity
            title="Recent Activity"
            :max-items="5"
          />
        </div>
        <div class="activity-side">
          <TopPerformers
            title="Top Performers"
            :max-items="5"
          />
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { onMounted } from 'vue';
import { useUserStore } from '../stores/user';
import { storeToRefs } from 'pinia';
import DashboardLayout from '../layouts/DashboardLayout.vue';
import StatsCard from '../components/dashboard/StatsCard.vue';
import RevenueChart from '../components/dashboard/RevenueChart.vue';
import UserOverview from '../components/dashboard/UserOverview.vue';
import RecentActivity from '../components/dashboard/RecentActivity.vue';
import TopPerformers from '../components/dashboard/TopPerformers.vue';

const userStore = useUserStore();
const { profile: userProfile } = storeToRefs(userStore);

onMounted(async () => {
  if (!userProfile.value) {
    await userStore.fetchProfile();
  }
});
</script>

<style scoped>
.dashboard-content {
  padding: 1.5rem;
}

.welcome-header {
  margin-bottom: 1.5rem;
}

.welcome-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-neutral-900);
  margin: 0 0 0.25rem;
}

.welcome-subtitle {
  font-size: 0.875rem;
  color: var(--color-neutral-500);
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.chart-main,
.chart-side {
  min-height: 400px;
}

.activity-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

/* Responsive adjustments */
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-grid {
    grid-template-columns: 1fr;
  }

  .activity-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .dashboard-content {
    padding: 1rem;
  }
}
</style>
