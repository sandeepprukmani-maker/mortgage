<template>
    <div class="card basic-data-table">
      <div class="card-body py-80 px-32 text-center">
        <div class="max-w-454-px mx-auto">
          <img src="@/assets/images/error/403-img.png" alt="Thumbnail" class="mb-24" />
        </div>
        <h6 class="mb-16">403 Forbidden</h6>
        <p class="text-secondary-light max-w-650-px mx-auto">
          403 Forbidden response status code indicates that the server understands the request but refuses to authorize it.
        </p>
        <router-link to="/" class="btn btn-primary-600 radius-8 px-40 py-16">Back to Home</router-link>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ForbiddenPage',
  };
  </script>
  