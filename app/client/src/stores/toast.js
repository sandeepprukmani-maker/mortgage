import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useToastStore = defineStore('toast', () => {
  const toasts = ref([])
  let nextId = 0

  const activeToasts = computed(() => toasts.value)

  function addToast({ message, type = 'info', duration = 5000 }) {
    const id = nextId++
    const toast = {
      id,
      message,
      type, // 'success', 'error', 'warning', 'info'
      createdAt: Date.now()
    }

    toasts.value.push(toast)

    // Auto-remove after duration
    if (duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, duration)
    }

    return id
  }

  function removeToast(id) {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  function success(message, duration = 4000) {
    return addToast({ message, type: 'success', duration })
  }

  function error(message, duration = 6000) {
    return addToast({ message, type: 'error', duration })
  }

  function warning(message, duration = 5000) {
    return addToast({ message, type: 'warning', duration })
  }

  function info(message, duration = 5000) {
    return addToast({ message, type: 'info', duration })
  }

  function clear() {
    toasts.value = []
  }

  return {
    toasts: activeToasts,
    addToast,
    removeToast,
    success,
    error,
    warning,
    info,
    clear
  }
})
