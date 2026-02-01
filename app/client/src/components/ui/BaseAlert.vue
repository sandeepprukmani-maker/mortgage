<template>
  <div :class="alertClasses">
    <slot />
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  variant: {
    type: String,
    default: 'info',
    validator: (value) => ['error', 'success', 'warning', 'info'].includes(value)
  }
});

const baseClasses = 'px-3 py-3 rounded-md text-sm';

const variantClasses = {
  error: 'bg-red-100 border border-red-200 text-red-700',
  success: 'bg-green-100 border border-green-200 text-green-800',
  warning: 'bg-yellow-100 border border-yellow-200 text-yellow-800',
  info: 'bg-blue-100 border border-blue-200 text-blue-800'
};

const alertClasses = computed(() => {
  return [baseClasses, variantClasses[props.variant]].join(' ');
});
</script>
