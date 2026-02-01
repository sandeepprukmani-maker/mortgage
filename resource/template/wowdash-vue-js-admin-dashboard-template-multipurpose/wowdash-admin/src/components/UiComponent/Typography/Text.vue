<template>
    <div class="col-md-6">
      <div class="card h-100 p-0">
        <div class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center justify-content-between">
          <h6 class="text-lg fw-semibold mb-0">Text</h6>
          <h6 class="text-lg fw-semibold mb-0">Font Size</h6>
        </div>
        <div class="card-body py-16 px-24">
          <div class="d-flex align-items-center justify-content-between mb-16">
            <p class="text-lg text-secondary-light">This is text</p>
            <span class="text-sm text-secondary-light fw-normal">18px</span>
          </div>
          <div class="d-flex align-items-center justify-content-between mb-16">
            <p class="text-md text-secondary-light">This is text</p>
            <span class="text-sm text-secondary-light fw-normal">16px</span>
          </div>
          <div class="d-flex align-items-center justify-content-between mb-16">
            <p class="text-sm text-secondary-light">This is text</p>
            <span class="text-sm text-secondary-light fw-normal">14px</span>
          </div>
          <div class="d-flex align-items-center justify-content-between">
            <p class="text-xs text-secondary-light">This is text</p>
            <span class="text-sm text-secondary-light fw-normal">12px</span>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'TextFontSizeCard'
  }
  </script>
  