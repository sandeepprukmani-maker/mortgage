<template>
  <div :class="avatarClasses">
    <img v-if="src" :src="src" :alt="initials" class="w-full h-full object-cover" />
    <span v-else>{{ initials }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  firstName: {
    type: String,
    default: ''
  },
  lastName: {
    type: String,
    default: ''
  },
  src: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
  }
});

const initials = computed(() => {
  return `${props.firstName?.[0] || ''}${props.lastName?.[0] || ''}`.toUpperCase();
});

const baseClasses = 'rounded-full bg-white/20 flex items-center justify-center font-bold border-[3px] border-white/30 overflow-hidden';

const sizeClasses = {
  sm: 'w-10 h-10 text-sm',
  md: 'w-16 h-16 text-xl',
  lg: 'w-20 h-20 text-2xl',
  xl: 'w-24 h-24 text-3xl'
};

const avatarClasses = computed(() => {
  return [baseClasses, sizeClasses[props.size]].join(' ');
});
</script>
