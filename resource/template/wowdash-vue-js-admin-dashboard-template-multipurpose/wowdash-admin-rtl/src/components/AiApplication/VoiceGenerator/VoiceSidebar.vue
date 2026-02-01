<template>
    <div class="col-xxl-3 col-lg-4">
      <div class="card h-100 p-0">
        <div class="card-body p-24">
          <div class="mb-20">
            <label for="language" class="text-sm fw-semibold text-primary-light mb-8">Language</label>
            <select class="form-select form-control px-16 py-14 h-48-px" id="language" v-model="form.language">
              <option value="">English</option>
              <option value="">Bangla</option>
              <option value="">Hindi</option>
              <option value="">Urdhu</option>
            </select>
          </div>
          <div class="mb-20">
            <label for="audioEffect" class="text-sm fw-semibold text-primary-light mb-8">Audio Effect</label>
            <select class="form-select form-control px-16 py-14 h-48-px" id="audioEffect" v-model="form.audioEffect">
              <option value="">Smart Voice</option>
              <option value="">Old Voice</option>
              <option value="">Similar Voice</option>
            </select>
          </div>
          <div class="mb-20">
            <label for="voice" class="text-sm fw-semibold text-primary-light mb-8">Voice</label>
            <select class="form-select form-control px-16 py-14 h-48-px" id="voice" v-model="form.voice">
              <option value="">Amber Heath</option>
              <option value="">Amber Heath</option>
              <option value="">Amber Heath</option>
              <option value="">Amber Heath</option>
            </select>
          </div>
          <div class="mb-20">
            <label for="format" class="text-sm fw-semibold text-primary-light mb-8">Format</label>
            <select class="form-select form-control px-16 py-14 h-48-px" id="format" v-model="form.format">
              <option value="">Mp3</option>
              <option value="">Mp4</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        form: {
          language: '',
          audioEffect: '',
          voice: '',
          format: ''
        }
      };
    }
  };
  </script>
  