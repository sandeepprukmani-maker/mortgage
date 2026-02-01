<template>
  <div v-if="!collapsed" class="sidebar-search">
    <div class="search-wrapper">
      <svg
        class="search-icon"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
      <input
        type="text"
        :value="modelValue"
        placeholder="Search"
        class="search-input"
        @input="$emit('update:modelValue', $event.target.value)"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useSidebarStore } from '../../stores/sidebar';

defineProps({
  modelValue: {
    type: String,
    default: ''
  }
});

defineEmits(['update:modelValue']);

const sidebarStore = useSidebarStore();
const collapsed = computed(() => sidebarStore.isCollapsed);
</script>

<style scoped>
.sidebar-search {
  padding: 0 16px;
  margin-bottom: 16px;
}

.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  width: 18px;
  height: 18px;
  color: var(--color-neutral-400);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 10px 12px 10px 40px;
  font-size: 14px;
  border: none;
  border-radius: 8px;
  background-color: var(--color-neutral-100);
  color: var(--color-neutral-900);
  outline: none;
  transition: background-color 0.2s ease, box-shadow 0.2s ease;
}

.search-input::placeholder {
  color: var(--color-neutral-400);
}

.search-input:focus {
  background-color: var(--color-shade-white);
  box-shadow: 0 0 0 2px var(--color-primary-200);
}
</style>
