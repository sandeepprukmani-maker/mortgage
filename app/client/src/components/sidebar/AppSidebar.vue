<template>
  <!-- Mobile Overlay Backdrop -->
  <Transition name="fade">
    <div
      v-if="isMobileOpen"
      class="sidebar-backdrop"
      @click="closeMobile"
    />
  </Transition>

  <!-- Sidebar -->
  <aside
    :class="sidebarClasses"
    :style="sidebarStyles"
  >
    <!-- Logo Section -->
    <div :class="['sidebar-header', { 'sidebar-header--collapsed': isCollapsed }]">
      <router-link to="/dashboard" class="logo-link">
        <img src="/logo.svg" alt="Valargen" :class="['logo-icon', { 'logo-icon--collapsed': isCollapsed }]" />
      </router-link>
      <button
        v-if="!isCollapsed"
        type="button"
        class="toggle-btn desktop-only"
        @click="toggle"
        title="Collapse sidebar"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
        </svg>
      </button>
    </div>

    <!-- Search -->
    <!-- <SidebarSearch v-model="searchQuery" /> -->

    <!-- Navigation Menu -->
    <nav class="sidebar-nav">
      <!-- Main Menu -->
      <SidebarMenuItem to="/dashboard" label="Dashboard" :exact-match="true" icon="solar:home-smile-angle-outline" />

      <!-- Application Group -->
      <SidebarMenuGroup title="Application" :default-open="true">
        <SidebarMenuItem to="/customers" label="Customers" icon="solar:users-group-rounded-outline" />
        <SidebarMenuItem to="/coming-soon" label="Users" icon="solar:user-outline" />
        <SidebarMenuItem to="/coming-soon" label="Role & Access" icon="solar:shield-user-outline" />
      </SidebarMenuGroup>

      <!-- Analytics Group -->
      <SidebarMenuGroup title="Analytics" :default-open="false">
        <SidebarMenuItem to="/coming-soon" label="Overview" icon="solar:chart-2-outline" />
        <SidebarMenuItem to="/coming-soon" label="Reports" icon="solar:document-text-outline" />
        <SidebarMenuItem to="/coming-soon" label="Statistics" icon="solar:graph-up-outline" />
      </SidebarMenuGroup>

      <!-- Settings Group -->
      <SidebarMenuGroup title="Settings" :default-open="false">
        <SidebarMenuItem to="/profile" label="Profile" icon="solar:user-circle-outline" />
        <SidebarMenuItem to="/coming-soon" label="Company" icon="solar:buildings-2-outline" />
        <SidebarMenuItem to="/coming-soon" label="Notifications" icon="solar:bell-outline" />
        <SidebarMenuItem to="/coming-soon" label="Preferences" icon="solar:settings-outline" />
      </SidebarMenuGroup>
    </nav>
  </aside>
</template>

<script setup>
import { ref, computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useSidebarStore } from '../../stores/sidebar';
import SidebarSearch from './SidebarSearch.vue';
import SidebarMenuItem from './SidebarMenuItem.vue';
import SidebarMenuGroup from './SidebarMenuGroup.vue';

const sidebarStore = useSidebarStore();
const { isCollapsed, isMobileOpen, sidebarWidth } = storeToRefs(sidebarStore);
const { toggle, closeMobile } = sidebarStore;

const searchQuery = ref('');

const sidebarClasses = computed(() => {
  const classes = ['sidebar'];
  if (isCollapsed.value) {
    classes.push('sidebar--collapsed');
  }
  if (isMobileOpen.value) {
    classes.push('sidebar--mobile-open');
  }
  return classes.join(' ');
});

const sidebarStyles = computed(() => ({
  '--sidebar-width': sidebarWidth.value
}));
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: var(--sidebar-width, 250px);
  height: 100vh;
  background-color: var(--color-shade-white);
  border-right: 1px solid var(--color-neutral-200);
  z-index: 40;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease, transform 0.3s ease;
  overflow: hidden;
}

.sidebar--collapsed {
  width: 80px;
}

.sidebar-backdrop {
  position: fixed;
  inset: 0;
  background-color: rgba(100, 100, 100, 0.2);
  backdrop-filter: blur(2px);
  z-index: 35;
}

.sidebar-header {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  border-bottom: 1px solid var(--color-neutral-200);
  height: 70px;
  transition: padding 0.3s ease, justify-content 0.3s ease;
}

.sidebar-header--collapsed {
  justify-content: center;
  padding: 0;
}

.logo-link {
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.logo-link:hover {
  opacity: 0.85;
  transform: scale(1.02);
}

.logo-icon {
  height: 28px;
  width: auto;
  flex-shrink: 0;
  transition: height 0.3s ease, transform 0.3s ease;
}

.logo-icon--collapsed {
  height: 24px;
}

.toggle-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 6px;
  background-color: transparent;
  color: var(--color-neutral-500);
  cursor: pointer;
  flex-shrink: 0;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.toggle-btn:hover {
  background-color: var(--color-neutral-100);
  color: var(--color-neutral-900);
}

.toggle-btn svg {
  width: 16px;
  height: 16px;
}

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 8px 0;
}

/* Scrollbar styling */
.sidebar-nav::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background-color: var(--color-neutral-300);
  border-radius: 4px;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Mobile styles */
@media (max-width: 767px) {
  .sidebar {
    transform: translateX(-100%);
  }

  .sidebar--mobile-open {
    transform: translateX(0);
  }

  .desktop-only {
    display: none;
  }
}
</style>
