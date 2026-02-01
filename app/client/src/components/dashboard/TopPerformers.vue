<template>
  <div class="top-performers-card">
    <div class="card-header">
      <h3 class="card-title">{{ title }}</h3>
      <button class="more-btn">
        <Icon icon="solar:menu-dots-bold" class="w-5 h-5" />
      </button>
    </div>
    <div class="performers-list">
      <div v-for="(performer, index) in displayedPerformers" :key="index" class="performer-item">
        <div class="rank-badge" :class="getRankClass(index)">
          {{ index + 1 }}
        </div>
        <div class="performer-avatar">
          <img v-if="performer.avatar" :src="performer.avatar" :alt="performer.name" />
          <span v-else class="avatar-initials">{{ getInitials(performer.name) }}</span>
        </div>
        <div class="performer-info">
          <h4 class="performer-name">{{ performer.name }}</h4>
          <p class="performer-role">{{ performer.role }}</p>
        </div>
        <div class="performer-stats">
          <span class="stats-value">{{ performer.value }}</span>
          <span class="stats-label">{{ performer.metric }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  title: {
    type: String,
    default: 'Top Performers'
  },
  performers: {
    type: Array,
    default: () => []
  },
  maxItems: {
    type: Number,
    default: 5
  }
});

const defaultPerformers = [
  { name: 'Sarah Johnson', role: 'Loan Officer', value: '$2.4M', metric: 'Closed' },
  { name: 'Michael Chen', role: 'Processor', value: '156', metric: 'Applications' },
  { name: 'Emily Davis', role: 'Underwriter', value: '98%', metric: 'Approval Rate' },
  { name: 'James Wilson', role: 'Loan Officer', value: '$1.8M', metric: 'Closed' },
  { name: 'Amanda Lee', role: 'Processor', value: '142', metric: 'Applications' }
];

const displayedPerformers = computed(() => {
  const items = props.performers.length > 0 ? props.performers : defaultPerformers;
  return items.slice(0, props.maxItems);
});

function getInitials(name) {
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
}

function getRankClass(index) {
  if (index === 0) return 'rank-gold';
  if (index === 1) return 'rank-silver';
  if (index === 2) return 'rank-bronze';
  return '';
}
</script>

<style scoped>
.top-performers-card {
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
  margin-bottom: 1.25rem;
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

.performers-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.performer-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.rank-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.5rem;
  height: 1.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--color-neutral-600);
  background-color: var(--color-neutral-100);
  border-radius: 0.375rem;
  flex-shrink: 0;
}

.rank-gold {
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  color: white;
}

.rank-silver {
  background: linear-gradient(135deg, #C0C0C0 0%, #A0A0A0 100%);
  color: white;
}

.rank-bronze {
  background: linear-gradient(135deg, #CD7F32 0%, #8B4513 100%);
  color: white;
}

.performer-avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  background-color: var(--color-primary-100);
  display: flex;
  align-items: center;
  justify-content: center;
}

.performer-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-initials {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-primary-600);
}

.performer-info {
  flex: 1;
  min-width: 0;
}

.performer-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-neutral-900);
  margin: 0 0 0.125rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.performer-role {
  font-size: 0.75rem;
  color: var(--color-neutral-500);
  margin: 0;
}

.performer-stats {
  text-align: right;
  flex-shrink: 0;
}

.stats-value {
  display: block;
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--color-neutral-900);
}

.stats-label {
  font-size: 0.75rem;
  color: var(--color-neutral-500);
}
</style>
