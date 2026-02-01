<template>
  <Transition name="modal">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="handleClose">
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-black bg-opacity-50"></div>

      <!-- Modal -->
      <div class="relative bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        <!-- Header -->
        <div class="px-6 py-4 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h2 class="text-2xl font-bold text-gray-900">Pricing Quote</h2>
            <button
              @click="handleClose"
              class="text-gray-400 hover:text-gray-600 transition-colors"
              aria-label="Close modal"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Best Price Display -->
          <div class="mt-4 p-4 bg-green-50 rounded-lg">
            <p class="text-sm text-gray-600 mb-1">Best Price</p>
            <p class="text-3xl font-bold text-green-600">{{ bestPrice }}</p>
          </div>
        </div>

        <!-- Body -->
        <div class="flex-1 overflow-y-auto px-6 py-4">
          <h3 class="text-lg font-semibold text-gray-900 mb-3">Complete Response</h3>
          <pre class="bg-gray-50 p-4 rounded-lg overflow-x-auto text-sm text-gray-800 border border-gray-200">{{ formattedResponse }}</pre>
        </div>

        <!-- Footer -->
        <div class="px-6 py-4 border-t border-gray-200 bg-gray-50">
          <BaseButton @click="handleClose" variant="secondary" class="w-full sm:w-auto">
            Close
          </BaseButton>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { computed, onMounted, onUnmounted } from 'vue';
import BaseButton from './ui/BaseButton.vue';

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  bestPrice: {
    type: String,
    default: 'N/A'
  },
  fullResponse: {
    type: Object,
    default: () => ({})
  }
});

const emit = defineEmits(['close']);

const formattedResponse = computed(() => {
  return JSON.stringify(props.fullResponse, null, 2);
});

const handleClose = () => {
  emit('close');
};

const handleEscape = (event) => {
  if (event.key === 'Escape' && props.show) {
    handleClose();
  }
};

onMounted(() => {
  document.addEventListener('keydown', handleEscape);
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape);
});
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .relative,
.modal-leave-active .relative {
  transition: transform 0.3s ease;
}

.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.95);
}
</style>
