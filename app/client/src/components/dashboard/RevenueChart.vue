<template>
  <div class="revenue-chart-card">
    <div class="chart-header">
      <div>
        <h3 class="chart-title">{{ title }}</h3>
        <p v-if="subtitle" class="chart-subtitle">{{ subtitle }}</p>
      </div>
      <div v-if="showPeriodSelector" class="period-selector">
        <button
          v-for="period in periods"
          :key="period.value"
          :class="['period-btn', { active: selectedPeriod === period.value }]"
          @click="selectedPeriod = period.value"
        >
          {{ period.label }}
        </button>
      </div>
    </div>
    <div class="chart-container">
      <apexchart
        type="area"
        height="320"
        :options="chartOptions"
        :series="series"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import VueApexCharts from 'vue3-apexcharts';

const apexchart = VueApexCharts;

const props = defineProps({
  title: {
    type: String,
    default: 'Revenue Overview'
  },
  subtitle: {
    type: String,
    default: ''
  },
  data: {
    type: Array,
    default: () => []
  },
  categories: {
    type: Array,
    default: () => ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  },
  showPeriodSelector: {
    type: Boolean,
    default: true
  }
});

const selectedPeriod = ref('year');

const periods = [
  { label: 'Week', value: 'week' },
  { label: 'Month', value: 'month' },
  { label: 'Year', value: 'year' }
];

const series = computed(() => {
  if (props.data.length > 0) {
    return props.data;
  }
  // Default demo data
  return [
    {
      name: 'Revenue',
      data: [4500, 5200, 4800, 6100, 5800, 7200, 6800, 8100, 7600, 8900, 8400, 9200]
    },
    {
      name: 'Expenses',
      data: [2800, 3100, 2900, 3400, 3200, 3800, 3600, 4100, 3900, 4500, 4200, 4800]
    }
  ];
});

const chartOptions = computed(() => ({
  chart: {
    type: 'area',
    height: 320,
    toolbar: {
      show: false
    },
    zoom: {
      enabled: false
    },
    fontFamily: 'Inter, sans-serif'
  },
  colors: ['#487FFF', '#22C55E'],
  dataLabels: {
    enabled: false
  },
  stroke: {
    curve: 'smooth',
    width: 2
  },
  fill: {
    type: 'gradient',
    gradient: {
      shadeIntensity: 1,
      opacityFrom: 0.4,
      opacityTo: 0.1,
      stops: [0, 90, 100]
    }
  },
  grid: {
    borderColor: '#e5e5e5',
    strokeDashArray: 4,
    padding: {
      left: 10,
      right: 10
    }
  },
  xaxis: {
    categories: props.categories,
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false
    },
    labels: {
      style: {
        colors: '#737373',
        fontSize: '12px'
      }
    }
  },
  yaxis: {
    labels: {
      style: {
        colors: '#737373',
        fontSize: '12px'
      },
      formatter: (value) => `$${(value / 1000).toFixed(0)}k`
    }
  },
  legend: {
    position: 'top',
    horizontalAlign: 'right',
    floating: true,
    offsetY: -25,
    offsetX: -5,
    markers: {
      width: 8,
      height: 8,
      radius: 8
    },
    itemMargin: {
      horizontal: 10
    }
  },
  tooltip: {
    y: {
      formatter: (value) => `$${value.toLocaleString()}`
    }
  }
}));
</script>

<style scoped>
.revenue-chart-card {
  background-color: var(--color-shade-white);
  border-radius: 0.75rem;
  box-shadow: var(--shadow-card);
  padding: 1.5rem;
}

.chart-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.chart-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-neutral-900);
  margin: 0;
}

.chart-subtitle {
  font-size: 0.875rem;
  color: var(--color-neutral-500);
  margin: 0.25rem 0 0;
}

.period-selector {
  display: flex;
  gap: 0.25rem;
  background-color: var(--color-neutral-100);
  padding: 0.25rem;
  border-radius: 0.5rem;
}

.period-btn {
  padding: 0.375rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--color-neutral-600);
  background: transparent;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.period-btn:hover {
  color: var(--color-neutral-900);
}

.period-btn.active {
  background-color: var(--color-shade-white);
  color: var(--color-primary-600);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.chart-container {
  margin-top: 0.5rem;
}
</style>
