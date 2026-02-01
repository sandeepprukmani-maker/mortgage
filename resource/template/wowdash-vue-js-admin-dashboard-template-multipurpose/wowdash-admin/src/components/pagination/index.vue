<template>
  <div class="d-flex align-items-center justify-content-between flex-wrap gap-2 mt-24">
    <span>Showing {{ startIndex + 1 }} to {{ endIndex }} of {{ totalItems }} entries</span>
    <ul class="pagination d-flex flex-wrap align-items-center gap-2 justify-content-center">
      <!-- Previous Button -->
      <li class="page-item" :class="{ disabled: currentPage === 1 }">
        <a class="page-link bg-neutral-200 text-secondary-light fw-semibold radius-8 border-0 
          d-flex align-items-center justify-content-center h-32-px w-32-px p-0"
          @click.prevent="changePage(currentPage - 1)">
          <iconify-icon icon="ep:d-arrow-left"></iconify-icon>
        </a>
      </li>

      <!-- Page Numbers -->
      <li class="page-item" v-for="n in 5" :key="n">
        <a :class="[
          'page-link text-secondary-light fw-semibold radius-8 border-0 d-flex align-items-center justify-content-center h-32-px w-32-px',
          currentPage === n ? 'bg-primary-600 text-white' : 'bg-neutral-200'
        ]" href="javascript:void(0)" @click="changePage(n)">
          {{ n }}
        </a>
      </li>

      <!-- Next Button -->
      <li class="page-item" :class="{ disabled: currentPage === totalPages }">
        <a class="page-link bg-neutral-200 text-secondary-light fw-semibold radius-8 border-0 
          d-flex align-items-center justify-content-center h-32-px w-32-px p-0"
          @click.prevent="changePage(currentPage + 1)">
          <iconify-icon icon="ep:d-arrow-right"></iconify-icon>
        </a>

      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    currentPage: Number,
    totalPages: Number,
    startIndex: Number,
    endIndex: Number,
    totalItems: Number
  },
  emits: ['page-changed'],
  methods: {
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.$emit('page-changed', page);
      }
    }
  }
};
</script>