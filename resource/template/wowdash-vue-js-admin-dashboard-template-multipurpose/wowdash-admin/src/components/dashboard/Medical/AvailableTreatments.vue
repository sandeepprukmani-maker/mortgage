<template>
    <div class="col-xxl-12 col-xl-6">
      <div class="card">
        <div class="card-header">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg mb-0">Available Treatments</h6>
            <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
              View All
              <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
            </a>
          </div>
        </div>
        <div class="card-body">
          <div
            v-for="(treatment, index) in treatments"
            :key="index"
            class="d-flex align-items-center justify-content-between gap-3"
            :class="{ 'mb-24': index !== treatments.length - 1 }"
          >
            <div class="d-flex align-items-center gap-12">
              <div :class="['w-40-px', 'h-40-px', 'rounded-circle', 'flex-shrink-0', treatment.bgClass, 'd-flex', 'justify-content-center', 'align-items-center']">
                <img :src="treatment.icon" alt="" />
              </div>
              <div class="flex-grow-1">
                <h6 class="text-md mb-0 fw-normal">{{ treatment.name }}</h6>
                <span class="text-sm text-secondary-light fw-normal">{{ treatment.doctors }} Doctors</span>
              </div>
            </div>
            <span class="text-secondary-light">08:45 AM</span>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import treatment1 from '@/assets/images/home-eight/treatment-icon1.png'
  import treatment2 from '@/assets/images/home-eight/treatment-icon2.png'
  import treatment3 from '@/assets/images/home-eight/treatment-icon3.png'
  import treatment4 from '@/assets/images/home-eight/treatment-icon4.png'
  import treatment5 from '@/assets/images/home-eight/treatment-icon5.png'
  import treatment6 from '@/assets/images/home-eight/treatment-icon6.png'

  export default {
    name: 'AvailableTreatmentsCard',
    data() {
      return {
        treatments: [
          {
            name: 'Psychiatry',
            doctors: 57,
            icon: treatment1,
            bgClass: 'bg-info-50'
          },
          {
            name: 'Orthopedic',
            doctors: 85,
            icon: treatment2,
            bgClass: 'bg-success-50'
          },
          {
            name: 'Cardiology',
            doctors: 60,
            icon: treatment3,
            bgClass: 'bg-lilac-50'
          },
          {
            name: 'Pediatrics',
            doctors: 120,
            icon: treatment4,
            bgClass: 'bg-warning-50'
          },
          {
            name: 'Neurology',
            doctors: 25,
            icon: treatment5,
            bgClass: 'bg-danger-50'
          },
          {
            name: 'Gastroenterology',
            doctors: 95,
            icon: treatment6,
            bgClass: 'bg-primary-50'
          }
        ]
      };
    }
  };
  </script>
  