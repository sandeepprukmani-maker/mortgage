<template>
  <div class="flex items-center text-center my-6">
    <div class="flex-1 border-b border-gray-200"></div>
    <span v-if="text || $slots.default" class="px-4 text-gray-400 text-sm font-medium">
      <slot>{{ text }}</slot>
    </span>
    <div class="flex-1 border-b border-gray-200"></div>
  </div>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    default: ''
  }
});
</script>
