<template>
  <nav class="bg-white shadow-card px-4 md:px-8 py-4 flex justify-between items-center">
    <div class="flex gap-6 items-center">
      <router-link to="/dashboard" class="flex items-center cursor-pointer transition-opacity duration-200 hover:opacity-80">
        <img src="/logo.svg" alt="ValerGen" class="h-7 md:h-9 w-auto" />
      </router-link>
      <router-link
        to="/dashboard"
        :class="[
          'no-underline font-medium transition-colors duration-200 flex items-center gap-2 text-sm md:text-base hover:text-primary-500',
          $route.path === '/dashboard' ? 'text-primary-600 font-semibold border-b-2 border-primary-500' : 'text-gray-600'
        ]"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-[18px] h-[18px] md:w-5 md:h-5">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
        Dashboard
      </router-link>
    </div>
    <div class="flex gap-3 md:gap-4 items-center">
      <router-link
        to="/customers"
        class="text-gray-600 no-underline font-medium transition-colors duration-200 flex items-center gap-2 text-sm md:text-base hover:text-primary-500"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-[18px] h-[18px] md:w-5 md:h-5">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        Customers
      </router-link>
      <router-link
        to="/profile"
        :class="[
          'no-underline font-medium transition-colors duration-200 flex items-center gap-2 text-sm md:text-base hover:text-primary-500',
          $route.path === '/profile' ? 'text-primary-600 font-semibold border-b-2 border-primary-500' : 'text-gray-600'
        ]"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-[18px] h-[18px] md:w-5 md:h-5">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
        Profile
      </router-link>
      <button
        @click="handleLogout"
        class="px-3 py-1.5 md:px-4 md:py-2 bg-red-500 text-white border-none rounded-md font-medium cursor-pointer transition-colors duration-200 flex items-center gap-2 text-sm md:text-base hover:bg-red-600"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-[18px] h-[18px] md:w-5 md:h-5">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
        Logout
      </button>
    </div>
  </nav>
</template>

<script setup>
import { useAuth } from '../composables/useAuth';

defineProps({
  showProfileLink: {
    type: Boolean,
    default: false
  },
  showDashboardLink: {
    type: Boolean,
    default: false
  }
});

const { logout } = useAuth();

async function handleLogout() {
  await logout();
}
</script>
