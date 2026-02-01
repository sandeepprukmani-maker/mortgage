<template>
  <router-link
    v-if="to"
    :to="to"
    :class="menuItemClasses"
  >
    <span class="menu-icon">
      <Icon v-if="icon" :icon="icon" class="w-5 h-5" />
      <slot v-else name="icon" />
    </span>
    <span v-if="!collapsed" class="menu-label">{{ label }}</span>
    <span v-if="!collapsed && badge" class="menu-badge">{{ badge }}</span>
  </router-link>
  <a
    v-else
    href="#"
    :class="menuItemClasses"
    @click.prevent="$emit('click')"
  >
    <span class="menu-icon">
      <Icon v-if="icon" :icon="icon" class="w-5 h-5" />
      <slot v-else name="icon" />
    </span>
    <span v-if="!collapsed" class="menu-label">{{ label }}</span>
    <span v-if="!collapsed && badge" class="menu-badge">{{ badge }}</span>
  </a>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { useSidebarStore } from '../../stores/sidebar';

const props = defineProps({
  to: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    required: true
  },
  icon: {
    type: String,
    default: ''
  },
  badge: {
    type: [String, Number],
    default: ''
  },
  exactMatch: {
    type: Boolean,
    default: false
  }
});

defineEmits(['click']);

const route = useRoute();
const sidebarStore = useSidebarStore();

const collapsed = computed(() => sidebarStore.isCollapsed);

const isActive = computed(() => {
  if (!props.to) return false;
  if (props.exactMatch) {
    return route.path === props.to;
  }
  return route.path.startsWith(props.to);
});

const menuItemClasses = computed(() => {
  const base = [
    'flex items-center gap-3 px-5 py-3 text-[15px] font-medium',
    'transition-all duration-200 no-underline cursor-pointer',
    'border-l-[3px] border-transparent'
  ];

  if (collapsed.value) {
    base.push('justify-center px-0');
  }

  if (isActive.value) {
    base.push('bg-primary-50 text-primary-600 border-l-primary-600');
  } else {
    base.push('text-neutral-600 hover:bg-neutral-100 hover:text-neutral-900');
  }

  return base.join(' ');
});
</script>

<style scoped>
.menu-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.menu-icon :deep(svg) {
  width: 20px;
  height: 20px;
}

.menu-label {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.menu-badge {
  padding: 2px 8px;
  font-size: 11px;
  font-weight: 600;
  background-color: var(--color-primary-600);
  color: white;
  border-radius: 10px;
}
</style>
