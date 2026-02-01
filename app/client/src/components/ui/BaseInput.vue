<template>
  <div class="flex flex-col gap-2">
    <label v-if="label" :for="id" class="font-medium text-gray-700">
      {{ label }}
    </label>
    <input
      :id="id"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :required="required"
      class="px-3 py-3 border border-gray-300 rounded-md text-base transition-colors duration-200 focus:outline-none focus:border-blue-500 focus:ring-[3px] focus:ring-blue-500/10 disabled:bg-gray-100 disabled:cursor-not-allowed"
      :class="{ 'border-red-500 focus:border-red-500 focus:ring-red-500/10': error }"
      @input="$emit('update:modelValue', $event.target.value)"
    />
    <span v-if="error" class="text-red-500 text-sm">{{ error }}</span>
    <small v-if="helpText && !error" class="text-gray-500 text-xs">{{ helpText }}</small>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  placeholder: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  },
  helpText: {
    type: String,
    default: ''
  },
  id: {
    type: String,
    default: () => `input-${Math.random().toString(36).substr(2, 9)}`
  }
});

defineEmits(['update:modelValue']);
</script>
