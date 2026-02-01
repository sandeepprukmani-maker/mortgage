<template>
    <div class="col-xxl-4">
      <div class="card">
        <div class="card-header border-bottom">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg mb-0">Doctors List</h6>
            <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
              View All
              <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
            </a>
          </div>
        </div>
        <div class="card-body">
          <div class="d-flex flex-column gap-24">
            <div v-for="(doctor, index) in doctors" :key="index" class="d-flex align-items-center justify-content-between gap-3">
              <div class="d-flex align-items-center">
                <img :src="doctor.image" alt="" class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12 overflow-hidden">
                <div class="flex-grow-1">
                  <h6 class="text-md mb-0">{{ doctor.name }}</h6>
                  <span class="text-sm text-secondary-light fw-medium">{{ doctor.specialty }}</span>
                </div>
              </div>
              <span :class="doctor.available ? 'bg-success-focus text-success-main' : 'bg-danger-focus text-danger-main'" class="px-10 py-4 radius-8 fw-medium text-sm">
                {{ doctor.available ? 'Available' : 'Not Available' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import doctor1 from '@/assets/images/home-eight/doctor-img1.png'
  import doctor2 from '@/assets/images/home-eight/doctor-img2.png'
  import doctor3 from '@/assets/images/home-eight/doctor-img3.png'
  import doctor4 from '@/assets/images/home-eight/doctor-img4.png'
  import doctor5 from '@/assets/images/home-eight/doctor-img5.png'
  import doctor6 from '@/assets/images/home-eight/doctor-img6.png'

  export default {
    name: 'DoctorsList',
    data() {
      return {
        doctors: [
          {
            name: 'Dr. Davis',
            specialty: 'Cardiology',
            image: doctor1,
            available: true
          },
          {
            name: 'Dr. Riead',
            specialty: 'Orthopedics',
            image: doctor2,
            available: true
          },
          {
            name: 'Albert Flores',
            specialty: 'Ophthalmology',
            image: doctor3,
            available: false
          },
          {
            name: 'Dr. Smith',
            specialty: 'Cardiology',
            image: doctor4,
            available: true
          },
          {
            name: 'Dr. Johnson',
            specialty: 'Cardiology',
            image: doctor6,
            available: false
          },
          {
            name: 'Dr. Martinez',
            specialty: 'Cardiology',
            image: doctor5,
            available: true
          }
        ]
      };
    }
  };
  </script>
  