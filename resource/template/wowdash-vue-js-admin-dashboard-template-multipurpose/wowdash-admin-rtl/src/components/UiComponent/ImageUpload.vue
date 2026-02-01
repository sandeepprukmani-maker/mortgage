<template>
    <div class="row gy-4">
      <!-- Single Upload -->
      <div class="col-md-6">
        <div class="card h-100 p-0">
          <div class="card-header border-bottom bg-base py-16 px-24">
            <h6 class="text-lg fw-semibold mb-0">Basic Upload</h6>
          </div>
          <div class="card-body p-24">
            <label for="basic-upload" class="border border-primary-600 fw-medium text-primary-600 px-16 py-12 radius-12 d-inline-flex align-items-center gap-2 bg-hover-primary-50">
              <iconify-icon icon="solar:upload-linear" class="text-xl"></iconify-icon>
              Click to upload
            </label>
            <input type="file" class="form-control w-auto mt-24 form-control-lg" id="basic-upload" @change="handleSingleUpload" ref="singleFileInput">
          </div>
        </div>
      </div>
  
      <!-- Image Upload -->
      <div class="col-md-6">
        <div class="card h-100 p-0">
          <div class="card-header border-bottom bg-base py-16 px-24">
            <h6 class="text-lg fw-semibold mb-0">Image Upload</h6>
          </div>
          <div class="card-body p-24">
            <div class="upload-image-wrapper d-flex align-items-center gap-3">
              <div v-if="imageSrc" class="uploaded-img position-relative h-120-px w-120-px border input-form-light radius-8 overflow-hidden border-dashed bg-neutral-50">
                <button type="button" class="uploaded-img__remove position-absolute top-0 end-0 z-1 text-2xxl line-height-1 me-8 mt-8 d-flex" @click="removeImage">
                  <iconify-icon icon="radix-icons:cross-2" class="text-xl text-danger-600"></iconify-icon>
                </button>
                <img :src="imageSrc" class="w-100 h-100 object-fit-cover" alt="image">
              </div>
  
              <label class="upload-file h-120-px w-120-px border input-form-light radius-8 overflow-hidden border-dashed bg-neutral-50 bg-hover-neutral-200 d-flex align-items-center flex-column justify-content-center gap-1" for="upload-file">
                <iconify-icon icon="solar:camera-outline" class="text-xl text-secondary-light"></iconify-icon>
                <span class="fw-semibold text-secondary-light">Upload</span>
                <input id="upload-file" type="file" hidden @change="handleImageUpload" ref="imageFileInput">
              </label>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Multiple Image Upload -->
      <div class="col-md-6">
        <div class="card h-100 p-0">
          <div class="card-header border-bottom bg-base py-16 px-24">
            <h6 class="text-lg fw-semibold mb-0">Upload With image preview</h6>
          </div>
          <div class="card-body p-24">
            <div class="upload-image-wrapper d-flex align-items-center gap-3 flex-wrap">
              <div class="uploaded-imgs-container d-flex gap-3 flex-wrap">
                <div v-for="(image, index) in uploadedImages" :key="index" class="position-relative h-120-px w-120-px border input-form-light radius-8 overflow-hidden border-dashed bg-neutral-50">
                  <button type="button" class="uploaded-img__remove position-absolute top-0 end-0 z-1 text-2xxl line-height-1 me-8 mt-8 d-flex" @click="removeUploadedImage(index)">
                    <iconify-icon icon="radix-icons:cross-2" class="text-xl text-danger-600"></iconify-icon>
                  </button>
                  <img :src="image" class="w-100 h-100 object-fit-cover" alt="image">
                </div>
              </div>
  
              <label class="upload-file-multiple h-120-px w-120-px border input-form-light radius-8 overflow-hidden border-dashed bg-neutral-50 bg-hover-neutral-200 d-flex align-items-center flex-column justify-content-center gap-1" for="upload-file-multiple">
                <iconify-icon icon="solar:camera-outline" class="text-xl text-secondary-light"></iconify-icon>
                <span class="fw-semibold text-secondary-light">Upload</span>
                <input id="upload-file-multiple" type="file" hidden multiple @change="handleMultipleImageUpload" ref="multipleFileInput">
              </label>
            </div>
          </div>
        </div>
      </div>
  
      <!-- File Name Upload -->
      <div class="col-md-6">
        <div class="card h-100 p-0">
          <div class="card-header border-bottom bg-base py-16 px-24">
            <h6 class="text-lg fw-semibold mb-0">Upload With image preview</h6>
          </div>
          <div class="card-body p-24">
            <label for="file-upload-name" class="mb-16 border border-neutral-600 fw-medium text-secondary-light px-16 py-12 radius-12 d-inline-flex align-items-center gap-2 bg-hover-neutral-200">
              <iconify-icon icon="solar:upload-linear" class="text-xl"></iconify-icon>
              Click to upload
              <input type="file" class="form-control w-auto mt-24 form-control-lg" id="file-upload-name" multiple hidden @change="handleFileNameUpload" ref="fileNameInput">
            </label>
            <ul id="uploaded-img-names" class="">
              <li v-for="(file, index) in uploadedFileNames" :key="index" class="uploaded-image-name-list text-primary-600 fw-semibold d-flex align-items-center gap-2">
                <iconify-icon icon="ph:link-break-light" class="text-xl text-secondary-light"></iconify-icon>
                {{ file.name }}
                <iconify-icon icon="radix-icons:cross-2" class="remove-image text-xl text-secondary-light text-hover-danger-600" @click="removeFileName(index)"></iconify-icon>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        imageSrc: '', // To store single uploaded image src
        uploadedImages: [], // Array to store multiple images
        uploadedFileNames: [] // Array to store uploaded file names
      };
    },
    methods: {
      handleSingleUpload(event) {
        const file = event.target.files[0];
        if (file) {
          const src = URL.createObjectURL(file);
          this.imageSrc = src;
        }
      },
      removeImage() {
        this.imageSrc = '';
        this.$refs.singleFileInput.value = '';
      },
      handleImageUpload(event) {
        const file = event.target.files[0];
        if (file) {
          const src = URL.createObjectURL(file);
          this.imageSrc = src;
        }
      },
      handleMultipleImageUpload(event) {
        const files = event.target.files;
        for (let i = 0; i < files.length; i++) {
          const file = files[i];
          const src = URL.createObjectURL(file);
          this.uploadedImages.push(src);
        }
        this.$refs.multipleFileInput.value = '';
      },
      removeUploadedImage(index) {
        this.uploadedImages.splice(index, 1);
      },
      handleFileNameUpload(event) {
        const files = event.target.files;
        this.uploadedFileNames = Array.from(files);
      },
      removeFileName(index) {
        this.uploadedFileNames.splice(index, 1);
      }
    }
  };
  </script>
  