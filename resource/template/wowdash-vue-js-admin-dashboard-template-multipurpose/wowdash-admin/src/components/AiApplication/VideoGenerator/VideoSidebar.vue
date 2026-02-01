<template>
    <div class="col-xxl-3 col-lg-4">
      <div class="card h-100 p-0">
        <div class="card-body p-24">
          <div class="mb-20">
            <label for="Title" class="text-sm fw-semibold text-primary-light mb-8">Title</label>
            <input type="text" class="form-control px-16 py-14 h-48-px" id="Title" placeholder="Enter Title" v-model="title" />
          </div>
  
          <div class="mb-20">
            <label for="Voice" class="text-sm fw-semibold text-primary-light mb-8">Voice</label>
            <select class="form-select form-control px-16 py-14 h-48-px" id="Voice" v-model="voice">
              <option value="">Male</option>
              <option value="">Female</option>
            </select>
          </div>
  
          <div class="mb-20">
            <label for="desc" class="text-sm fw-semibold text-primary-light mb-8">Title</label>
            <textarea class="form-control px-16 py-14" id="desc" placeholder="Write something..." v-model="description"></textarea>
          </div>
  
          <div class="mb-20">
            <label for="fileUpload" class="text-sm fw-semibold text-primary-light mb-8">Upload Avatar</label>
            <input type="file" id="fileUpload" @change="handleImageUpload" class="fileUpload image-upload" />
  
            <div v-if="imageUrl" id="imagePreview" class="mt-3 w-100 radius-8" :style="{
              backgroundImage: `url(${imageUrl})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              backgroundRepeat: 'no-repeat',
              width: '100%',
              height: '200px',
              transition: 'opacity 0.5s',
              opacity: imageLoaded ? 1 : 0
            }"></div>
          </div>
  
          <button type="button" class="btn btn-primary d-flex align-items-center gap-8 px-20 flex-shrink-0">
            Generate
            <i class="ri-ai-generate"></i>
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        title: '',
        voice: '',
        description: '',
        imageUrl: '',
        imageLoaded: false,
      };
    },
    methods: {
      handleImageUpload(event) {
        const file = event.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (e) => {
            this.imageUrl = e.target.result;
            this.imageLoaded = false;
            this.$nextTick(() => {
              this.imageLoaded = true;
            });
          };
          reader.readAsDataURL(file);
        }
      },
    },
  };
  </script>