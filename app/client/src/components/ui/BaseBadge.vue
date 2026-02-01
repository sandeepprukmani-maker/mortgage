<template>
  <span :class="badgeClasses">
    <slot />
  </span>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'primary', 'success', 'warning', 'danger', 'role', 'provider', 'plan'].includes(value)
  }
});

const baseClasses = 'inline-flex items-center px-3 py-1 rounded-full text-xs font-medium';

const variantClasses = {
  default: 'bg-gray-100 text-gray-700',
  primary: 'bg-primary-100 text-primary-800',
  success: 'bg-green-100 text-green-800',
  warning: 'bg-yellow-100 text-yellow-800',
  danger: 'bg-red-100 text-red-800',
  role: 'bg-white/20 text-white',
  provider: 'bg-white/15 text-white',
  plan: 'bg-blue-100 text-blue-800 capitalize'
};

const badgeClasses = computed(() => {
  return [baseClasses, variantClasses[props.variant]].join(' ');
});
</script>
