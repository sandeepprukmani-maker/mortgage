<template>
  <div class="auth-layout">
    <div class="auth-container">
      <slot />
    </div>
  </div>
</template>

<script setup>
// Simple layout for authentication pages
// No sidebar, just centered content with gradient background
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-primary-500), var(--color-brand-purple));
  padding: 16px;
}

.auth-container {
  width: 100%;
  max-width: 448px;
}
</style>
