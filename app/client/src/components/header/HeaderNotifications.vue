<template>
  <div class="notifications" ref="notificationsRef">
    <button
      type="button"
      class="notifications-trigger"
      @click="toggleDropdown"
      aria-haspopup="true"
      :aria-expanded="isOpen"
    >
      <Icon icon="solar:bell-outline" class="w-[22px] h-[22px]" />
      <span v-if="unreadCount > 0" class="notifications-badge">{{ unreadCount > 9 ? '9+' : unreadCount }}</span>
    </button>

    <Transition name="dropdown">
      <div v-if="isOpen" class="notifications-dropdown">
        <div class="dropdown-header">
          <div>
            <span class="dropdown-title">Notifications</span>
            <span v-if="unreadCount > 0" class="unread-count">{{ unreadCount }} new</span>
          </div>
          <button v-if="notifications.length > 0" type="button" class="mark-read-btn" @click="markAllRead">
            Mark all read
          </button>
        </div>

        <div class="dropdown-content">
          <div v-if="notifications.length === 0" class="empty-state">
            <Icon icon="solar:bell-off-outline" class="w-10 h-10" />
            <p>No notifications yet</p>
          </div>

          <div v-else class="notifications-list">
            <div
              v-for="notification in notifications"
              :key="notification.id"
              class="notification-item"
              :class="{ 'notification-item--unread': !notification.read }"
              @click="markAsRead(notification)"
            >
              <div class="notification-icon" :class="`notification-icon--${notification.type}`">
                <Icon :icon="getNotificationIcon(notification.type)" class="w-[18px] h-[18px]" />
              </div>
              <div class="notification-content">
                <p class="notification-message">{{ notification.message }}</p>
                <span class="notification-time">{{ notification.time }}</span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="notifications.length > 0" class="dropdown-footer">
          <a href="#" class="view-all-link">View all notifications</a>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';

const notificationsRef = ref(null);
const isOpen = ref(false);

// Demo notifications - in production this would come from a store/API
const notifications = ref([
  {
    id: 1,
    type: 'success',
    message: 'Your loan application has been approved',
    time: '2 min ago',
    read: false
  },
  {
    id: 2,
    type: 'info',
    message: 'New document uploaded for review',
    time: '15 min ago',
    read: false
  },
  {
    id: 3,
    type: 'warning',
    message: 'Income verification pending for 3 applications',
    time: '1 hour ago',
    read: true
  }
]);

function getNotificationIcon(type) {
  const icons = {
    success: 'solar:check-circle-bold',
    warning: 'solar:danger-triangle-bold',
    info: 'solar:info-circle-bold',
    error: 'solar:close-circle-bold'
  };
  return icons[type] || icons.info;
}

function markAsRead(notification) {
  notification.read = true;
}

const unreadCount = computed(() => {
  return notifications.value.filter(n => !n.read).length;
});

function toggleDropdown() {
  isOpen.value = !isOpen.value;
}

function closeDropdown() {
  isOpen.value = false;
}

function markAllRead() {
  notifications.value.forEach(n => {
    n.read = true;
  });
}

function handleClickOutside(event) {
  if (notificationsRef.value && !notificationsRef.value.contains(event.target)) {
    closeDropdown();
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
.notifications {
  position: relative;
}

.notifications-trigger {
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
  position: relative;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.notifications-trigger:hover {
  background-color: var(--color-neutral-100);
  color: var(--color-neutral-900);
}

.notifications-trigger svg {
  width: 22px;
  height: 22px;
}

.notifications-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  font-size: 11px;
  font-weight: 600;
  color: white;
  background-color: #ef4444;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notifications-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 320px;
  background-color: var(--color-shade-white);
  border: 1px solid var(--color-neutral-200);
  border-radius: 12px;
  box-shadow: var(--shadow-dropdown);
  overflow: hidden;
  z-index: 50;
}

.dropdown-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  border-bottom: 1px solid var(--color-neutral-200);
}

.dropdown-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-neutral-900);
}

.mark-read-btn {
  font-size: 12px;
  color: var(--color-primary-600);
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.2s ease;
}

.mark-read-btn:hover {
  color: var(--color-primary-700);
}

.dropdown-content {
  max-height: 320px;
  overflow-y: auto;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px 16px;
  color: var(--color-neutral-500);
}

.empty-state svg {
  width: 40px;
  height: 40px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.empty-state p {
  font-size: 14px;
  margin: 0;
}

.notifications-list {
  padding: 8px 0;
}

.notification-item {
  display: flex;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.notification-item:hover {
  background-color: var(--color-neutral-50);
}

.notification-item--unread {
  background-color: var(--color-primary-50);
}

.notification-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notification-icon svg {
  width: 18px;
  height: 18px;
}

.notification-icon--success {
  background-color: #dcfce7;
  color: #16a34a;
}

.notification-icon--warning {
  background-color: #fef3c7;
  color: #d97706;
}

.notification-icon--info {
  background-color: var(--color-primary-100);
  color: var(--color-primary-600);
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-message {
  font-size: 13px;
  color: var(--color-neutral-800);
  margin: 0 0 4px 0;
  line-height: 1.4;
}

.notification-time {
  font-size: 11px;
  color: var(--color-neutral-500);
}

.unread-count {
  margin-left: 8px;
  padding: 2px 8px;
  font-size: 11px;
  font-weight: 600;
  background-color: var(--color-primary-100);
  color: var(--color-primary-600);
  border-radius: 10px;
}

.dropdown-footer {
  padding: 12px 16px;
  border-top: 1px solid var(--color-neutral-200);
  text-align: center;
}

.view-all-link {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-primary-600);
  text-decoration: none;
  transition: color 0.2s ease;
}

.view-all-link:hover {
  color: var(--color-primary-700);
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
