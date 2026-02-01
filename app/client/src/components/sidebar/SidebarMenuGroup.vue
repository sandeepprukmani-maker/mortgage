<template>
  <div class="menu-group">
    <!-- Group Header (clickable to expand/collapse) -->
    <button
      v-if="!collapsed"
      type="button"
      class="group-header"
      @click="toggleOpen"
    >
      <Icon v-if="icon" :icon="icon" class="group-icon-iconify" />
      <span v-else-if="$slots.icon" class="group-icon">
        <slot name="icon" />
      </span>
      <span class="group-title">{{ title }}</span>
      <Icon
        icon="solar:alt-arrow-down-linear"
        class="chevron-icon"
        :class="{ 'rotate-180': isOpen }"
      />
    </button>

    <!-- Group Items -->
    <Transition
      @before-enter="beforeEnter"
      @enter="enter"
      @after-enter="afterEnter"
      @before-leave="beforeLeave"
      @leave="leave"
      @after-leave="afterLeave"
    >
      <div v-show="isOpen || collapsed" class="group-items">
        <slot />
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useSidebarStore } from '../../stores/sidebar';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  icon: {
    type: String,
    default: ''
  },
  defaultOpen: {
    type: Boolean,
    default: false
  },
  persistKey: {
    type: String,
    default: ''
  }
});

const sidebarStore = useSidebarStore();
const collapsed = computed(() => sidebarStore.isCollapsed);

const storageKey = computed(() => props.persistKey || `sidebar-group-${props.title.toLowerCase().replace(/\s+/g, '-')}`);

const isOpen = ref(props.defaultOpen);

function toggleOpen() {
  isOpen.value = !isOpen.value;
  // Persist to localStorage
  localStorage.setItem(storageKey.value, JSON.stringify(isOpen.value));
}

// Restore state from localStorage on mount
onMounted(() => {
  const savedState = localStorage.getItem(storageKey.value);
  if (savedState !== null) {
    isOpen.value = JSON.parse(savedState);
  }
});

// When sidebar expands, restore the group state
watch(collapsed, (newVal) => {
  if (!newVal && props.defaultOpen) {
    const savedState = localStorage.getItem(storageKey.value);
    if (savedState === null) {
      isOpen.value = true;
    }
  }
});

// Smooth height animation functions
function beforeEnter(el) {
  el.style.height = '0px';
  el.style.opacity = '0';
  el.style.overflow = 'hidden';
}

function enter(el) {
  el.style.transition = 'height 0.3s ease, opacity 0.3s ease';
  el.style.height = el.scrollHeight + 'px';
  el.style.opacity = '1';
}

function afterEnter(el) {
  el.style.height = 'auto';
  el.style.overflow = '';
  el.style.transition = '';
}

function beforeLeave(el) {
  el.style.height = el.scrollHeight + 'px';
  el.style.opacity = '1';
  el.style.overflow = 'hidden';
}

function leave(el) {
  el.style.transition = 'height 0.3s ease, opacity 0.3s ease';
  requestAnimationFrame(() => {
    el.style.height = '0px';
    el.style.opacity = '0';
  });
}

function afterLeave(el) {
  el.style.height = '';
  el.style.opacity = '';
  el.style.transition = '';
  el.style.overflow = '';
}
</script>

<style scoped>
.menu-group {
  margin-bottom: 4px;
}

.group-header {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 10px 20px;
  border: none;
  background: none;
  cursor: pointer;
  text-align: left;
  color: var(--color-neutral-500);
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: color 0.2s ease, background-color 0.2s ease;
}

.group-header:hover {
  color: var(--color-neutral-700);
  background-color: var(--color-neutral-100);
}

.group-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
}

.group-icon :deep(svg) {
  width: 16px;
  height: 16px;
}

.group-icon-iconify {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.group-title {
  flex: 1;
}

.chevron-icon {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
  flex-shrink: 0;
}

.chevron-icon.rotate-180 {
  transform: rotate(180deg);
}

.group-items {
  overflow: hidden;
}
</style>
