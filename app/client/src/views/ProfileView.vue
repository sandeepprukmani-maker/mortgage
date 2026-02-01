<template>
  <DashboardLayout page-title="Profile" max-width="3xl">
    <div class="mb-8">
      <h2 class="m-0 text-3xl text-neutral-800 font-semibold">User Profile</h2>
      <p class="mt-2 text-neutral-500 text-lg">View and manage your account information</p>
    </div>

    <UserProfile />
  </DashboardLayout>
</template>

<script setup>
import UserProfile from '../components/UserProfile.vue';
import DashboardLayout from '../layouts/DashboardLayout.vue';
</script>
