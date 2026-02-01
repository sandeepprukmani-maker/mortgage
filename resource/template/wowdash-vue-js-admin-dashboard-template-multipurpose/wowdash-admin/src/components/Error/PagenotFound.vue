<template>
    <div class="card basic-data-table">
      <div class="card-body py-80 px-32 text-center">
        <div class="max-w-454-px mx-auto">
          <img src="@/assets/images/error/404-img.png" alt="Thumbnail" class="mb-24" />
        </div>
        <h6 class="mb-16">403 Page not Found</h6>
        <p class="text-secondary-light max-w-650-px mx-auto">
          400 Bad Request response status code indicates that the server cannot or will not process the request due to something that is perceived to be a client error
        </p>
        <router-link to="/" class="btn btn-danger-600 radius-8 px-40 py-16">Back to Home</router-link>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'PageNotFound',
  };
  </script>
  