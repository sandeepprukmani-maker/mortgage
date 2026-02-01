import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useSidebarStore = defineStore('sidebar', () => {
  // State
  const isCollapsed = ref(localStorage.getItem('sidebar-collapsed') === 'true');
  const isMobileOpen = ref(false);

  // Getters
  const sidebarWidth = computed(() => isCollapsed.value ? '80px' : '250px');
  const sidebarWidthValue = computed(() => isCollapsed.value ? 80 : 250);

  // Actions
  function toggle() {
    isCollapsed.value = !isCollapsed.value;
    localStorage.setItem('sidebar-collapsed', isCollapsed.value.toString());
  }

  function collapse() {
    isCollapsed.value = true;
    localStorage.setItem('sidebar-collapsed', 'true');
  }

  function expand() {
    isCollapsed.value = false;
    localStorage.setItem('sidebar-collapsed', 'false');
  }

  function toggleMobile() {
    isMobileOpen.value = !isMobileOpen.value;
  }

  function closeMobile() {
    isMobileOpen.value = false;
  }

  function openMobile() {
    isMobileOpen.value = true;
  }

  return {
    // State
    isCollapsed,
    isMobileOpen,
    // Getters
    sidebarWidth,
    sidebarWidthValue,
    // Actions
    toggle,
    collapse,
    expand,
    toggleMobile,
    closeMobile,
    openMobile
  };
});
