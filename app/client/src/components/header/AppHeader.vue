<template>
  <header class="app-header">
    <div class="header-left">
      <!-- Mobile menu toggle -->
      <button
        type="button"
        class="menu-toggle mobile-only"
        @click="toggleMobile"
        aria-label="Toggle menu"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      <!-- Desktop sidebar toggle -->
      <button
        type="button"
        class="sidebar-toggle desktop-only"
        @click="toggle"
        :title="isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      <!-- Search -->
      <HeaderSearch v-model="searchQuery" @search="handleSearch" />
    </div>

    <div class="header-right">
      <!-- Theme toggle -->
      <button type="button" class="header-icon-btn" :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'" @click="toggleTheme">
        <!-- Sun icon (shown in dark mode) -->
        <svg v-if="isDark" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        <!-- Moon icon (shown in light mode) -->
        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
      </button>

      <!-- Notifications -->
      <HeaderNotifications />

      <!-- Breadcrumb -->
      <HeaderBreadcrumb :items="breadcrumbItems" class="desktop-only" />

      <!-- User menu -->
      <HeaderUserMenu />
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useSidebarStore } from '../../stores/sidebar';
import { useThemeStore } from '../../stores/theme';
import HeaderSearch from './HeaderSearch.vue';
import HeaderNotifications from './HeaderNotifications.vue';
import HeaderBreadcrumb from './HeaderBreadcrumb.vue';
import HeaderUserMenu from './HeaderUserMenu.vue';

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  breadcrumbItems: {
    type: Array,
    default: () => []
  }
});

const sidebarStore = useSidebarStore();
const themeStore = useThemeStore();
const { isCollapsed } = storeToRefs(sidebarStore);
const { isDark } = storeToRefs(themeStore);
const { toggle, toggleMobile } = sidebarStore;
const { toggleTheme } = themeStore;

const searchQuery = ref('');

function handleSearch(query) {
  // TODO: Implement search functionality
  console.log('Search:', query);
}
</script>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
  padding: 0 24px;
  background-color: var(--color-shade-white);
  border-bottom: 1px solid var(--color-neutral-200);
  position: sticky;
  top: 0;
  z-index: 30;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.menu-toggle,
.sidebar-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 8px;
  background: none;
  color: var(--color-neutral-600);
  cursor: pointer;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.menu-toggle:hover,
.sidebar-toggle:hover {
  background-color: var(--color-neutral-100);
  color: var(--color-neutral-900);
}

.menu-toggle svg,
.sidebar-toggle svg {
  width: 22px;
  height: 22px;
}

.header-icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background: none;
  color: var(--color-neutral-600);
  cursor: pointer;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.header-icon-btn:hover {
  background-color: var(--color-neutral-100);
  color: var(--color-neutral-900);
}

.header-icon-btn svg {
  width: 22px;
  height: 22px;
}

/* Responsive visibility */
.desktop-only {
  display: flex;
}

.mobile-only {
  display: none;
}

@media (max-width: 767px) {
  .app-header {
    padding: 0 16px;
  }

  .header-left {
    gap: 8px;
  }

  .header-right {
    gap: 4px;
  }

  .desktop-only {
    display: none;
  }

  .mobile-only {
    display: flex;
  }
}
</style>
