<template>
  <div class="recent-activity-card">
    <div class="card-header">
      <h3 class="card-title">{{ title }}</h3>
      <a href="#" class="view-all-link">View All</a>
    </div>
    <div class="activity-list">
      <div v-for="(activity, index) in displayedActivities" :key="index" class="activity-item">
        <div class="activity-avatar" :class="getAvatarClass(activity.type)">
          <Icon :icon="getActivityIcon(activity.type)" class="w-5 h-5" />
        </div>
        <div class="activity-content">
          <p class="activity-text">
            <strong>{{ activity.user }}</strong>
            {{ activity.action }}
          </p>
          <span class="activity-time">{{ activity.time }}</span>
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
    default: 'Recent Activity'
  },
  activities: {
    type: Array,
    default: () => []
  },
  maxItems: {
    type: Number,
    default: 5
  }
});

const defaultActivities = [
  {
    user: 'John Doe',
    action: 'submitted a new loan application',
    time: '2 minutes ago',
    type: 'application'
  },
  {
    user: 'Sarah Wilson',
    action: 'uploaded income verification documents',
    time: '15 minutes ago',
    type: 'document'
  },
  {
    user: 'Mike Johnson',
    action: 'completed pre-qualification questionnaire',
    time: '1 hour ago',
    type: 'form'
  },
  {
    user: 'Emily Brown',
    action: 'scheduled a closing appointment',
    time: '2 hours ago',
    type: 'calendar'
  },
  {
    user: 'David Lee',
    action: 'approved for loan processing',
    time: '3 hours ago',
    type: 'success'
  }
];

const displayedActivities = computed(() => {
  const items = props.activities.length > 0 ? props.activities : defaultActivities;
  return items.slice(0, props.maxItems);
});

function getActivityIcon(type) {
  const iconMap = {
    application: 'solar:document-add-bold-duotone',
    document: 'solar:file-check-bold-duotone',
    form: 'solar:clipboard-check-bold-duotone',
    calendar: 'solar:calendar-bold-duotone',
    success: 'solar:check-circle-bold-duotone',
    user: 'solar:user-bold-duotone',
    default: 'solar:bell-bold-duotone'
  };
  return iconMap[type] || iconMap.default;
}

function getAvatarClass(type) {
  const classMap = {
    application: 'bg-primary-100 text-primary-600',
    document: 'bg-info-100 text-info-600',
    form: 'bg-warning-100 text-warning-600',
    calendar: 'bg-purple/10 text-purple',
    success: 'bg-success-100 text-success-600',
    user: 'bg-neutral-200 text-neutral-600',
    default: 'bg-neutral-200 text-neutral-600'
  };
  return classMap[type] || classMap.default;
}
</script>

<style scoped>
.recent-activity-card {
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

.view-all-link {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-primary-600);
  text-decoration: none;
  transition: color 0.2s ease;
}

.view-all-link:hover {
  color: var(--color-primary-700);
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.activity-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
  min-width: 0;
}

.activity-text {
  font-size: 0.875rem;
  color: var(--color-neutral-700);
  margin: 0 0 0.25rem;
  line-height: 1.4;
}

.activity-text strong {
  font-weight: 600;
  color: var(--color-neutral-900);
}

.activity-time {
  font-size: 0.75rem;
  color: var(--color-neutral-500);
}
</style>
