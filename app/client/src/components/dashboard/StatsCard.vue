<template>
  <div class="stats-card">
    <div class="stats-icon" :class="iconBgClass">
      <Icon :icon="icon" class="w-6 h-6" />
    </div>
    <div class="stats-content">
      <p class="stats-label">{{ title }}</p>
      <h3 class="stats-value">{{ formattedValue }}</h3>
      <div v-if="change !== undefined" class="stats-change" :class="changeClass">
        <Icon :icon="changeIcon" class="w-4 h-4" />
        <span>{{ Math.abs(change) }}%</span>
        <span class="text-neutral-500">vs last month</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [Number, String],
    required: true
  },
  change: {
    type: Number,
    default: undefined
  },
  changeType: {
    type: String,
    default: 'positive',
    validator: (value) => ['positive', 'negative', 'neutral'].includes(value)
  },
  icon: {
    type: String,
    default: 'solar:chart-2-bold-duotone'
  },
  iconColor: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'success', 'warning', 'danger', 'info', 'purple'].includes(value)
  },
  prefix: {
    type: String,
    default: ''
  },
  suffix: {
    type: String,
    default: ''
  }
});

const formattedValue = computed(() => {
  if (typeof props.value === 'number') {
    const formatted = props.value.toLocaleString();
    return `${props.prefix}${formatted}${props.suffix}`;
  }
  return `${props.prefix}${props.value}${props.suffix}`;
});

const iconBgClass = computed(() => {
  const colorMap = {
    primary: 'bg-primary-100 text-primary-600',
    success: 'bg-success-100 text-success-600',
    warning: 'bg-warning-100 text-warning-600',
    danger: 'bg-danger-100 text-danger-600',
    info: 'bg-info-100 text-info-600',
    purple: 'bg-purple/10 text-purple'
  };
  return colorMap[props.iconColor] || colorMap.primary;
});

const changeClass = computed(() => {
  if (props.changeType === 'positive' || props.change > 0) {
    return 'text-success-main';
  } else if (props.changeType === 'negative' || props.change < 0) {
    return 'text-danger-main';
  }
  return 'text-neutral-500';
});

const changeIcon = computed(() => {
  if (props.changeType === 'positive' || props.change > 0) {
    return 'solar:arrow-up-bold';
  } else if (props.changeType === 'negative' || props.change < 0) {
    return 'solar:arrow-down-bold';
  }
  return 'solar:minus-bold';
});
</script>

<style scoped>
.stats-card {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.5rem;
  background-color: var(--color-shade-white);
  border-radius: 0.75rem;
  box-shadow: var(--shadow-card);
  transition: box-shadow 0.2s ease;
}

.stats-card:hover {
  box-shadow: var(--shadow-card-hover);
}

.stats-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3rem;
  height: 3rem;
  border-radius: 0.75rem;
  flex-shrink: 0;
}

.stats-content {
  flex: 1;
  min-width: 0;
}

.stats-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-neutral-500);
  margin: 0 0 0.25rem;
}

.stats-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-neutral-900);
  margin: 0 0 0.5rem;
  line-height: 1.2;
}

.stats-change {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.stats-change span:last-child {
  margin-left: 0.25rem;
}
</style>
