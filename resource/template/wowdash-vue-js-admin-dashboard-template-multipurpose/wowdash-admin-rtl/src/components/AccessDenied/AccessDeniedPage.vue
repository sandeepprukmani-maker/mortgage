<template>
    <div class="custom-bg">
      <div class="container container--xl">
        <div class="d-flex align-items-center justify-content-between py-24">
          <router-link to="/">
            <img src="@/assets/images/logo.png" alt="" />
          </router-link>
          <router-link to="/" class="btn btn-outline-primary-600 text-sm">Go To Home</router-link>
        </div>
  
        <div class="pt-48 pb-40 text-center">
          <div class="max-w-500-px mx-auto">
            <img src="@/assets/images/forbidden/forbidden-img.png" alt="" />
          </div>
          <div class="max-w-700-px mx-auto mt-40">
            <h3 class="mb-24 max-w-1000-px">Access Denied</h3>
            <p class="text-neutral-500 max-w-700-px text-lg">
              You don't have authorization to get to this page. If it's not too much trouble,
              contact your site executive to demand access.
            </p>
            <router-link to="/" class="btn btn-primary-600 px-32 py-16 flex-shrink-0 d-inline-flex align-items-center justify-content-center gap-8 mt-28">
              <i class="ri-home-4-line"></i> Go Back To Home
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "AccessDenied",
  };
  </script>
  