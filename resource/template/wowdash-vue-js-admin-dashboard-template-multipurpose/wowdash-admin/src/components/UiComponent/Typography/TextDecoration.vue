<template>
    <div class="col-md-6">
      <div class="card h-100 p-0">
        <div class="card-header border-bottom bg-base py-16 px-24">
          <h6 class="text-lg fw-semibold mb-0">Text Decoration</h6>
        </div>
        <div class="card-body py-16 px-24">
          <p class="mb-16 text-secondary-light fw-normal">
            Use text-decoration-underline, text-decoration-line-through, or text-decoration-none class to decorate text in components respectively.
          </p>
          <p class="mb-16 text-primary-light fw-normal text-decoration-underline">
            This text has a line underneath it.
          </p>
          <p class="mb-16 text-primary-light fw-normal text-decoration-line-through">
            This text has a line going through it.
          </p>
          <p class="text-secondary-light fw-normal">
            This link has its text decoration removed
          </p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'TextDecorationCard'
  }
  </script>
  