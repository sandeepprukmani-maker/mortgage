<template>
    <div class="row gy-4">
      <!-- Default Tags -->
      <div class="col-sm-6">
        <div class="card h-100 p-0">
          <div class="card-header border-bottom bg-base py-16 px-24">
            <h6 class="text-lg fw-semibold mb-0">Default Tags</h6>
          </div>
          <div class="card-body p-24">
            <ul class="d-flex flex-wrap align-items-center gap-32">
              <li class="text-secondary-light border radius-4 px-8 py-4 text-sm line-height-1 fw-medium">Label</li>
              <li class="text-secondary-light border radius-4 px-8 py-4 text-sm line-height-1 fw-medium">Label</li>
              <li class="text-secondary-light border radius-4 px-8 py-4 text-sm line-height-1 fw-medium">Label</li>
            </ul>
            <ul class="tag-list d-flex flex-wrap align-items-center gap-20 mt-20">
              <li v-if="showDefault1" class="text-secondary-light border radius-4 px-8 py-2 text-sm line-height-1 fw-medium d-flex align-items-center gap-1">
                Label
                <button @click="showDefault1 = false" class="remove-tag text-lg d-flex justify-content-center align-items-center" type="button">
                  <iconify-icon icon="iconamoon:sign-times-light" class="icon line-height-1"></iconify-icon>
                </button>
              </li>
              <li v-if="showDefault2" class="text-secondary-light border radius-4 px-8 py-2 text-sm line-height-1 fw-medium d-flex align-items-center gap-1">
                Label
                <button @click="showDefault2 = false" class="remove-tag text-lg d-flex justify-content-center align-items-center" type="button">
                  <iconify-icon icon="iconamoon:sign-times-light" class="icon line-height-1"></iconify-icon>
                </button>
              </li>
              <li v-if="showDefault3" class="text-secondary-light border radius-4 px-8 py-2 text-sm line-height-1 fw-medium d-flex align-items-center gap-1">
                Label
                <button @click="showDefault3 = false" class="remove-tag text-lg d-flex justify-content-center align-items-center" type="button">
                  <iconify-icon icon="iconamoon:sign-times-light" class="icon line-height-1"></iconify-icon>
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
  
      <!-- Color Tags -->
      <div class="col-sm-6">
        <div class="card h-100 p-0">
          <div class="card-header border-bottom bg-base py-16 px-24">
            <h6 class="text-lg fw-semibold mb-0">Colors tags</h6>
          </div>
          <div class="card-body p-24">
            <ul class="d-flex flex-wrap align-items-center gap-32">
              <li class="text-white bg-primary-600 border border-primary-600 radius-4 px-8 py-4 text-sm line-height-1 fw-medium">Label</li>
              <li class="text-white bg-lilac-600 border border-lilac-600 radius-4 px-8 py-4 text-sm line-height-1 fw-medium">Label</li>
              <li class="text-white bg-warning-600 border border-warning-600 radius-4 px-8 py-4 text-sm line-height-1 fw-medium">Label</li>
            </ul>
            <ul class="tag-list d-flex flex-wrap align-items-center gap-20 mt-20">
              <li v-if="showColor1" class="text-primary-600 border border-primary-600 radius-4 px-8 py-2 text-sm line-height-1 fw-medium d-flex align-items-center gap-1">
                Label
                <button @click="showColor1 = false" class="remove-tag text-lg d-flex justify-content-center align-items-center" type="button">
                  <iconify-icon icon="iconamoon:sign-times-light" class="icon line-height-1"></iconify-icon>
                </button>
              </li>
              <li v-if="showColor2" class="text-lilac-600 border border-lilac-600 radius-4 px-8 py-2 text-sm line-height-1 fw-medium d-flex align-items-center gap-1">
                Label
                <button @click="showColor2 = false" class="remove-tag text-lg d-flex justify-content-center align-items-center" type="button">
                  <iconify-icon icon="iconamoon:sign-times-light" class="icon line-height-1"></iconify-icon>
                </button>
              </li>
              <li v-if="showColor3" class="text-warning-600 border border-warning-600 radius-4 px-8 py-2 text-sm line-height-1 fw-medium d-flex align-items-center gap-1">
                Label
                <button @click="showColor3 = false" class="remove-tag text-lg d-flex justify-content-center align-items-center" type="button">
                  <iconify-icon icon="iconamoon:sign-times-light" class="icon line-height-1"></iconify-icon>
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
  
      <!-- Tags With Image -->
      <div class="col-sm-6">
        <div class="card h-100 p-0">
          <div class="card-header border-bottom bg-base py-16 px-24">
            <h6 class="text-lg fw-semibold mb-0">Tags With Image</h6>
          </div>
          <div class="card-body p-24">
            <ul class="d-flex flex-wrap align-items-center gap-20 mt-20">
              <li class="text-secondary-light border radius-4 px-8 py-4 text-sm line-height-1 fw-medium d-flex align-items-center gap-1">
                <img src="@/assets/images/flags/flag-tag.png" class="w-16-px h-16-px rounded-circle" alt="">
                Label
              </li>
              <li class="text-secondary-light border radius-4 px-8 py-4 text-sm line-height-1 fw-medium d-flex align-items-center gap-1">
                <img src="@/assets/images/flags/flag-tag.png" class="w-16-px h-16-px rounded-circle" alt="">
                Label
              </li>
              <li class="text-secondary-light border radius-4 px-8 py-4 text-sm line-height-1 fw-medium d-flex align-items-center gap-1">
                <img src="@/assets/images/flags/flag-tag.png" class="w-16-px h-16-px rounded-circle" alt="">
                Label
              </li>
            </ul>
            <ul class="tag-list d-flex flex-wrap align-items-center gap-20 mt-20">
              <li v-if="showImage1" class="text-secondary-light border radius-4 px-8 py-4 text-sm line-height-1 fw-medium d-flex align-items-center gap-1">
                <img src="@/assets/images/flags/flag-tag.png" class="w-16-px h-16-px rounded-circle" alt="">
                Label
                <button @click="showImage1 = false" class="remove-tag text-lg d-flex justify-content-center align-items-center" type="button">
                  <iconify-icon icon="iconamoon:sign-times-light" class="icon line-height-1"></iconify-icon>
                </button>
              </li>
              <li v-if="showImage2" class="text-secondary-light border radius-4 px-8 py-4 text-sm line-height-1 fw-medium d-flex align-items-center gap-1">
                <img src="@/assets/images/flags/flag-tag.png" class="w-16-px h-16-px rounded-circle" alt="">
                Label
                <button @click="showImage2 = false" class="remove-tag text-lg d-flex justify-content-center align-items-center" type="button">
                  <iconify-icon icon="iconamoon:sign-times-light" class="icon line-height-1"></iconify-icon>
                </button>
              </li>
              <li v-if="showImage3" class="text-secondary-light border radius-4 px-8 py-4 text-sm line-height-1 fw-medium d-flex align-items-center gap-1">
                <img src="@/assets/images/flags/flag-tag.png" class="w-16-px h-16-px rounded-circle" alt="">
                Label
                <button @click="showImage3 = false" class="remove-tag text-lg d-flex justify-content-center align-items-center" type="button">
                  <iconify-icon icon="iconamoon:sign-times-light" class="icon line-height-1"></iconify-icon>
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
  
      <!-- Tags Indicator -->
      <div class="col-sm-6">
        <div class="card h-100 p-0">
          <div class="card-header border-bottom bg-base py-16 px-24">
            <h6 class="text-lg fw-semibold mb-0">Tags Indicator</h6>
          </div>
          <div class="card-body p-24">
            <ul class="d-flex flex-wrap align-items-center gap-32">
              <li class="text-secondary-light border radius-4 px-8 py-4 text-sm line-height-1 fw-medium d-flex align-items-center gap-1">
                <span class="w-8-px h-8-px bg-success-main rounded-circle"></span>
                Label
              </li>
              <li class="text-secondary-light border radius-4 px-8 py-4 text-sm line-height-1 fw-medium d-flex align-items-center gap-1">
                <span class="w-8-px h-8-px bg-success-main rounded-circle"></span>
                Label
              </li>
              <li class="text-secondary-light border radius-4 px-8 py-4 text-sm line-height-1 fw-medium d-flex align-items-center gap-1">
                <span class="w-8-px h-8-px bg-success-main rounded-circle"></span>
                Label
              </li>
            </ul>
            <ul class="tag-list d-flex flex-wrap align-items-center gap-20 mt-20">
              <li v-if="showIndicator1" class="text-secondary-light border radius-4 px-8 py-2 text-sm line-height-1 fw-medium d-flex align-items-center gap-1">
                <span class="w-8-px h-8-px bg-success-main rounded-circle"></span>
                Label
                <button @click="showIndicator1 = false" class="remove-tag text-lg d-flex justify-content-center align-items-center" type="button">
                  <iconify-icon icon="iconamoon:sign-times-light" class="icon line-height-1"></iconify-icon>
                </button>
              </li>
              <li v-if="showIndicator2" class="text-secondary-light border radius-4 px-8 py-2 text-sm line-height-1 fw-medium d-flex align-items-center gap-1">
                <span class="w-8-px h-8-px bg-success-main rounded-circle"></span>
                Label
                <button @click="showIndicator2 = false" class="remove-tag text-lg d-flex justify-content-center align-items-center" type="button">
                  <iconify-icon icon="iconamoon:sign-times-light" class="icon line-height-1"></iconify-icon>
                </button>
              </li>
              <li v-if="showIndicator3" class="text-secondary-light border radius-4 px-8 py-2 text-sm line-height-1 fw-medium d-flex align-items-center gap-1">
                <span class="w-8-px h-8-px bg-success-main rounded-circle"></span>
                Label
                <button @click="showIndicator3 = false" class="remove-tag text-lg d-flex justify-content-center align-items-center" type="button">
                  <iconify-icon icon="iconamoon:sign-times-light" class="icon line-height-1"></iconify-icon>
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const showDefault1 = ref(true)
  const showDefault2 = ref(true)
  const showDefault3 = ref(true)
  
  const showColor1 = ref(true)
  const showColor2 = ref(true)
  const showColor3 = ref(true)
  
  const showImage1 = ref(true)
  const showImage2 = ref(true)
  const showImage3 = ref(true)
  
  const showIndicator1 = ref(true)
  const showIndicator2 = ref(true)
  const showIndicator3 = ref(true)
  </script>
  