<template>
  <div class="user-menu" ref="menuRef">
    <button
      type="button"
      class="user-menu-trigger"
      @click="toggleMenu"
      aria-haspopup="true"
      :aria-expanded="isOpen"
    >
      <div class="user-avatar">
        <img
          v-if="userProfile?.avatar_url"
          :src="userProfile.avatar_url"
          :alt="userName"
          class="avatar-image"
        />
        <span v-else class="avatar-initials">{{ userInitials }}</span>
      </div>
    </button>

    <Transition name="dropdown">
      <div v-if="isOpen" class="user-dropdown">
        <div class="dropdown-header">
          <div class="user-info">
            <span class="user-name">{{ userName }}</span>
            <span class="user-email">{{ userProfile?.email || '' }}</span>
          </div>
        </div>

        <div class="dropdown-divider" />

        <router-link to="/profile" class="dropdown-item" @click="closeMenu">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          Profile
        </router-link>

        <router-link to="/coming-soon" class="dropdown-item" @click="closeMenu">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          Settings
        </router-link>

        <div class="dropdown-divider" />

        <button type="button" class="dropdown-item dropdown-item--danger" @click="handleLogout">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          Logout
        </button>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useUserStore } from '../../stores/user';
import { useAuth } from '../../composables/useAuth';
import { storeToRefs } from 'pinia';

const userStore = useUserStore();
const { profile: userProfile } = storeToRefs(userStore);
const { logout } = useAuth();

const menuRef = ref(null);
const isOpen = ref(false);

const userName = computed(() => {
  if (userProfile.value?.first_name || userProfile.value?.last_name) {
    return `${userProfile.value?.first_name || ''} ${userProfile.value?.last_name || ''}`.trim();
  }
  return userProfile.value?.email?.split('@')[0] || 'User';
});

const userInitials = computed(() => {
  const name = userName.value;
  const parts = name.split(' ');
  if (parts.length >= 2) {
    return `${parts[0][0]}${parts[1][0]}`.toUpperCase();
  }
  return name.substring(0, 2).toUpperCase();
});

function toggleMenu() {
  isOpen.value = !isOpen.value;
}

function closeMenu() {
  isOpen.value = false;
}

async function handleLogout() {
  closeMenu();
  await logout();
}

function handleClickOutside(event) {
  if (menuRef.value && !menuRef.value.contains(event.target)) {
    closeMenu();
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.user-menu {
  position: relative;
}

.user-menu-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px;
  border: none;
  background: none;
  cursor: pointer;
  border-radius: 50%;
  transition: background-color 0.2s ease;
}

.user-menu-trigger:hover {
  background-color: var(--color-neutral-100);
}

.user-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(145deg, var(--color-primary-400), var(--color-primary-600));
  color: white;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.5px;
  box-shadow: 0 0 0 2px var(--color-shade-white), 0 0 0 3px var(--color-primary-200);
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.user-menu-trigger:hover .user-avatar {
  box-shadow: 0 0 0 2px var(--color-shade-white), 0 0 0 4px var(--color-primary-300);
  transform: scale(1.02);
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-initials {
  text-transform: uppercase;
  user-select: none;
}

.user-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 200px;
  background-color: var(--color-shade-white);
  border: 1px solid var(--color-neutral-200);
  border-radius: 12px;
  box-shadow: var(--shadow-dropdown);
  overflow: hidden;
  z-index: 50;
}

.dropdown-header {
  padding: 16px;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-neutral-900);
}

.user-email {
  font-size: 12px;
  color: var(--color-neutral-500);
}

.dropdown-divider {
  height: 1px;
  background-color: var(--color-neutral-200);
  margin: 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  font-size: 14px;
  color: var(--color-neutral-700);
  text-decoration: none;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.dropdown-item:hover {
  background-color: var(--color-neutral-100);
  color: var(--color-neutral-900);
}

.dropdown-item svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.dropdown-item--danger {
  color: #ef4444;
}

.dropdown-item--danger:hover {
  background-color: #fef2f2;
  color: #dc2626;
}

/* Dropdown transition */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
