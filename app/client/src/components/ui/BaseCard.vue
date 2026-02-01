<template>
  <div
    class="bg-white rounded-lg overflow-hidden"
    :class="{
      'shadow-card': shadow,
      'p-6': padding && !$slots.header && !$slots.footer
    }"
  >
    <div v-if="$slots.header" class="p-6 border-b border-gray-200">
      <slot name="header" />
    </div>
    <div :class="{ 'p-6': padding }">
      <slot />
    </div>
    <div v-if="$slots.footer" class="p-6 border-t border-gray-200">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  padding: {
    type: Boolean,
    default: true
  },
  shadow: {
    type: Boolean,
    default: true
  }
});
</script>
