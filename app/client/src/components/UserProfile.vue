<template>
  <div class="w-full">
    <div v-if="loading" class="text-center p-8 text-gray-500">Loading profile...</div>

    <BaseAlert v-else-if="error" variant="error">
      Failed to load profile: {{ error }}
    </BaseAlert>

    <div v-else-if="profile" class="bg-white rounded-lg shadow-card overflow-hidden">
      <div class="flex items-center gap-6 p-8 bg-gradient-to-br from-primary-500 to-brand-purple text-white">
        <BaseAvatar :first-name="profile.first_name" :last-name="profile.last_name" size="lg" />
        <div>
          <h2 class="m-0 text-2xl">{{ profile.first_name }} {{ profile.last_name }}</h2>
          <p class="my-2 opacity-90">{{ profile.email }}</p>
          <div class="flex gap-2 mt-3">
            <BaseBadge variant="role">{{ profile.role?.name || 'No Role' }}</BaseBadge>
            <BaseBadge variant="provider">{{ profile.auth_provider || 'local' }}</BaseBadge>
          </div>
        </div>
      </div>

      <div class="p-8 flex flex-col gap-8">
        <div>
          <h3 class="m-0 mb-4 text-gray-700 text-lg font-semibold">Account Information</h3>
          <div class="flex justify-between py-3 border-b border-gray-200">
            <span class="text-gray-500 font-medium">Email Verified:</span>
            <span :class="profile.is_email_verified ? 'text-green-600 font-medium' : 'text-yellow-600 font-medium'">
              {{ profile.is_email_verified ? 'Yes' : 'No' }}
            </span>
          </div>
          <div class="flex justify-between py-3 border-b border-gray-200">
            <span class="text-gray-500 font-medium">Authentication:</span>
            <span>{{ profile.auth_provider === 'google' ? 'Google OAuth' : 'Email & Password' }}</span>
          </div>
          <div class="flex justify-between py-3 border-b border-gray-200" v-if="profile.created_at">
            <span class="text-gray-500 font-medium">Member Since:</span>
            <span>{{ formatDate(profile.created_at) }}</span>
          </div>
          <div class="flex justify-between py-3" v-if="profile.last_login_at">
            <span class="text-gray-500 font-medium">Last Login:</span>
            <span>{{ formatDate(profile.last_login_at) }}</span>
          </div>
        </div>

        <div v-if="profile.tenant">
          <h3 class="m-0 mb-4 text-gray-700 text-lg font-semibold">Organization</h3>
          <div class="flex justify-between py-3 border-b border-gray-200">
            <span class="text-gray-500 font-medium">Company:</span>
            <span>{{ profile.tenant.company_name }}</span>
          </div>
          <div class="flex justify-between py-3">
            <span class="text-gray-500 font-medium">Plan:</span>
            <BaseBadge variant="plan">{{ profile.tenant.plan }}</BaseBadge>
          </div>
        </div>

        <div v-if="profile.permissions && profile.permissions.length > 0">
          <h3 class="m-0 mb-4 text-gray-700 text-lg font-semibold">Permissions</h3>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="permission in profile.permissions"
              :key="permission.id"
              class="px-4 py-2 bg-gray-100 rounded-md text-sm text-gray-700"
            >
              {{ permission.name }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useUserStore } from '../stores/user';
import { storeToRefs } from 'pinia';
import { BaseAlert, BaseAvatar, BaseBadge } from './ui';

const userStore = useUserStore();
const { profile, loading, error } = storeToRefs(userStore);

onMounted(async () => {
  if (!profile.value) {
    await userStore.fetchProfile();
  }
});

function formatDate(dateString) {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
}
</script>
