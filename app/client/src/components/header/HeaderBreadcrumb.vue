<template>
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <ol class="breadcrumb-list">
      <li v-for="(item, index) in breadcrumbItems" :key="index" class="breadcrumb-item">
        <router-link
          v-if="item.to && index < breadcrumbItems.length - 1"
          :to="item.to"
          class="breadcrumb-link"
        >
          {{ item.label }}
        </router-link>
        <span v-else class="breadcrumb-current">{{ item.label }}</span>
        <span v-if="index < breadcrumbItems.length - 1" class="breadcrumb-separator">/</span>
      </li>
    </ol>
  </nav>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  }
});

const route = useRoute();

const breadcrumbItems = computed(() => {
  if (props.items.length > 0) {
    return props.items;
  }

  // Auto-generate breadcrumbs from route
  const items = [{ label: 'Dashboard', to: '/dashboard' }];

  if (route.path !== '/dashboard') {
    const routeName = route.name || route.path.split('/').pop();
    items.push({
      label: routeName.charAt(0).toUpperCase() + routeName.slice(1),
      to: route.path
    });
  }

  return items;
});
</script>

<style scoped>
.breadcrumb {
  display: flex;
  align-items: center;
}

.breadcrumb-list {
  display: flex;
  align-items: center;
  gap: 8px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.breadcrumb-link {
  color: var(--color-primary-600);
  text-decoration: none;
  transition: color 0.2s ease;
}

.breadcrumb-link:hover {
  color: var(--color-primary-700);
  text-decoration: underline;
}

.breadcrumb-current {
  color: var(--color-neutral-600);
}

.breadcrumb-separator {
  color: var(--color-neutral-400);
}
</style>
