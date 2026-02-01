<template>
  <div class="user-overview-card">
    <div class="card-header">
      <h3 class="card-title">{{ title }}</h3>
      <button class="more-btn">
        <Icon icon="solar:menu-dots-bold" class="w-5 h-5" />
      </button>
    </div>
    <div class="chart-container">
      <apexchart
        type="donut"
        height="280"
        :options="chartOptions"
        :series="seriesData"
      />
    </div>
    <div class="legend-list">
      <div v-for="(item, index) in legendItems" :key="index" class="legend-item">
        <span class="legend-dot" :style="{ backgroundColor: colors[index] }"></span>
        <span class="legend-label">{{ item.label }}</span>
        <span class="legend-value">{{ item.value }}</span>
        <span class="legend-percent" :class="item.change >= 0 ? 'positive' : 'negative'">
          {{ item.change >= 0 ? '+' : '' }}{{ item.change }}%
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import VueApexCharts from 'vue3-apexcharts';

const apexchart = VueApexCharts;

const props = defineProps({
  title: {
    type: String,
    default: 'User Overview'
  },
  data: {
    type: Array,
    default: () => []
  },
  labels: {
    type: Array,
    default: () => ['Active Users', 'New Users', 'Inactive Users']
  }
});

const colors = ['#487FFF', '#22C55E', '#FF9F43', '#EA5455'];

const seriesData = computed(() => {
  if (props.data.length > 0) {
    return props.data.map(item => item.value || item);
  }
  return [4500, 2300, 1200];
});

const legendItems = computed(() => {
  if (props.data.length > 0 && typeof props.data[0] === 'object') {
    return props.data;
  }
  return [
    { label: 'Active Users', value: '4,500', change: 12.5 },
    { label: 'New Users', value: '2,300', change: 8.2 },
    { label: 'Inactive Users', value: '1,200', change: -3.4 }
  ];
});

const chartOptions = computed(() => ({
  chart: {
    type: 'donut',
    fontFamily: 'Inter, sans-serif'
  },
  colors: colors,
  labels: props.labels,
  legend: {
    show: false
  },
  dataLabels: {
    enabled: false
  },
  plotOptions: {
    pie: {
      donut: {
        size: '70%',
        labels: {
          show: true,
          name: {
            show: true,
            fontSize: '14px',
            fontWeight: 500,
            color: '#737373'
          },
          value: {
            show: true,
            fontSize: '24px',
            fontWeight: 700,
            color: '#171717',
            formatter: (val) => val.toLocaleString()
          },
          total: {
            show: true,
            label: 'Total Users',
            fontSize: '14px',
            fontWeight: 500,
            color: '#737373',
            formatter: (w) => {
              const total = w.globals.seriesTotals.reduce((a, b) => a + b, 0);
              return total.toLocaleString();
            }
          }
        }
      }
    }
  },
  stroke: {
    show: false
  },
  tooltip: {
    y: {
      formatter: (val) => val.toLocaleString()
    }
  }
}));
</script>

<style scoped>
.user-overview-card {
  background-color: var(--color-shade-white);
  border-radius: 0.75rem;
  box-shadow: var(--shadow-card);
  padding: 1.5rem;
  height: 100%;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-neutral-900);
  margin: 0;
}

.more-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  background: transparent;
  border: none;
  border-radius: 0.375rem;
  color: var(--color-neutral-500);
  cursor: pointer;
  transition: all 0.2s ease;
}

.more-btn:hover {
  background-color: var(--color-neutral-100);
  color: var(--color-neutral-900);
}

.chart-container {
  display: flex;
  justify-content: center;
}

.legend-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-neutral-200);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.legend-dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  flex-shrink: 0;
}

.legend-label {
  flex: 1;
  font-size: 0.875rem;
  color: var(--color-neutral-600);
}

.legend-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-neutral-900);
}

.legend-percent {
  font-size: 0.75rem;
  font-weight: 500;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
}

.legend-percent.positive {
  background-color: var(--color-success-50);
  color: var(--color-success-main);
}

.legend-percent.negative {
  background-color: var(--color-danger-50);
  color: var(--color-danger-main);
}
</style>
