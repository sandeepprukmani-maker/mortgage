<template>
    <div class="col-xxl-3 col-lg-4">
      <div class="card h-100 p-0">
        <div class="card-body p-24">
          <div class="mb-20">
            <label for="resulation" class="text-sm fw-semibold text-primary-light mb-8">Image Resolution</label>
            <input
              type="text"
              class="form-control px-16 py-14 h-48-px"
              id="resulation"
              v-model="formData.resolution"
            />
          </div>
          <div class="mb-20">
            <label for="style" class="text-sm fw-semibold text-primary-light mb-8">Image Resolution</label>
            <select
              class="form-select form-control px-16 py-14 h-48-px"
              id="style"
              v-model="formData.style"
            >
              <option value="">Carton</option>
              <option value="">Oil painting</option>
              <option value="">Pencil sketch</option>
              <option value="">Paper collage</option>
              <option value="">Street art</option>
            </select>
          </div>
          <div class="mb-20">
            <label for="LightingStyle" class="text-sm fw-semibold text-primary-light mb-8">Lighting Style</label>
            <select
              class="form-select form-control px-16 py-14 h-48-px"
              id="LightingStyle"
              v-model="formData.lightingStyle"
            >
              <option value="">Back lighting</option>
              <option value="">None</option>
              <option value="">Chiaroscuro</option>
              <option value="">God rays</option>
              <option value="">Studio lighting</option>
              <option value="">Candlelight</option>
              <option value="">Street lighting</option>
            </select>
          </div>
          <div class="mb-20">
            <label for="Mood" class="text-sm fw-semibold text-primary-light mb-8">Mood</label>
            <select
              class="form-select form-control px-16 py-14 h-48-px"
              id="Mood"
              v-model="formData.mood"
            >
              <option value="">None</option>
              <option value="">Chiaroscuro</option>
              <option value="">God rays</option>
              <option value="">Studio lighting</option>
              <option value="">Candlelight</option>
              <option value="">Street lighting</option>
            </select>
          </div>
          <div class="mb-20">
            <label for="imageNumber" class="text-sm fw-semibold text-primary-light mb-8">Number Of Image</label>
            <input
              type="number"
              class="form-control px-16 py-14 h-48-px"
              id="imageNumber"
              v-model.number="formData.imageNumber"
            />
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        formData: {
          resolution: '1024 x 1024px',
          style: '',
          lightingStyle: '',
          mood: '',
          imageNumber: 4
        }
      };
    }
  };
  </script>
  