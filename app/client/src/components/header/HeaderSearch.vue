<template>
  <div class="header-search">
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
        placeholder="Search..."
        class="search-input"
        @input="$emit('update:modelValue', $event.target.value)"
        @keydown.enter="$emit('search', modelValue)"
      />
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: ''
  }
});

defineEmits(['update:modelValue', 'search']);
</script>

<style scoped>
.header-search {
  width: 300px;
}

.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 16px;
  width: 18px;
  height: 18px;
  color: var(--color-neutral-400);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 10px 16px 10px 44px;
  font-size: 14px;
  border: none;
  border-radius: 50px;
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

/* Responsive */
@media (max-width: 767px) {
  .header-search {
    display: none;
  }
}
</style>
