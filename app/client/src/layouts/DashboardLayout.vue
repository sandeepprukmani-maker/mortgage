<template>
  <div class="layout-wrapper">
    <!-- Sidebar -->
    <AppSidebar />

    <!-- Main Content Area -->
    <div
      class="main-wrapper"
      :style="mainWrapperStyles"
    >
      <!-- Header -->
      <AppHeader :title="pageTitle" :breadcrumb-items="breadcrumbItems" />

      <!-- Content -->
      <main :class="contentClasses">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useSidebarStore } from '../stores/sidebar';
import AppSidebar from '../components/sidebar/AppSidebar.vue';
import AppHeader from '../components/header/AppHeader.vue';

const props = defineProps({
  pageTitle: {
    type: String,
    default: ''
  },
  breadcrumbItems: {
    type: Array,
    default: () => []
  },
  maxWidth: {
    type: String,
    default: 'full',
    validator: (value) => ['full', '7xl', '5xl', '3xl', 'lg'].includes(value)
  },
  noPadding: {
    type: Boolean,
    default: false
  }
});

const sidebarStore = useSidebarStore();
const { sidebarWidth, isCollapsed } = storeToRefs(sidebarStore);

const mainWrapperStyles = computed(() => ({
  marginLeft: window.innerWidth >= 768 ? sidebarWidth.value : '0',
  transition: 'margin-left 0.3s ease'
}));

const maxWidthClasses = {
  full: '',
  '7xl': 'max-w-7xl mx-auto',
  '5xl': 'max-w-5xl mx-auto',
  '3xl': 'max-w-3xl mx-auto',
  lg: 'max-w-lg mx-auto'
};

const contentClasses = computed(() => {
  const classes = ['content-wrapper'];
  if (!props.noPadding) {
    classes.push('p-6 md:p-8');
  }
  if (maxWidthClasses[props.maxWidth]) {
    classes.push(maxWidthClasses[props.maxWidth]);
  }
  return classes.join(' ');
});
</script>

<style scoped>
.layout-wrapper {
  min-height: 100vh;
  background-color: var(--color-neutral-100);
}

.main-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  transition: margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.content-wrapper {
  flex: 1;
  background-color: var(--color-neutral-100);
}

/* Mobile styles */
@media (max-width: 767px) {
  .main-wrapper {
    margin-left: 0 !important;
  }
}
</style>
