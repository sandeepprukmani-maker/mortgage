<template>
    <div class="col-xxl-12 col-xl-6">
        <div class="card">
            <div class="card-header">
                <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
                    <h6 class="mb-2 fw-bold text-lg mb-0">Health Reports Document</h6>
                    <a href="javascript:void(0)"
                        class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
                        View All
                        <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
                    </a>
                </div>
            </div>
            <div class="card-body">
                <div class="d-flex flex-column gap-24">
                    <div v-for="(report, index) in reports" :key="index"
                        class="d-flex align-items-center justify-content-between gap-3">
                        <div class="d-flex align-items-center gap-12">
                            <div class="flex-shrink-0">
                                <img :src="report.icon" alt="" class="" />
                            </div>
                            <div class="flex-grow-1">
                                <h6 class="text-md mb-0 fw-normal">{{ report.name }}</h6>
                                <span class="text-xs text-secondary-light fw-normal">{{ report.size }}</span>
                            </div>
                        </div>
                        <div class="flex-align d-flex gap-1">
                            <button type="button"
                                class="w-32-px h-32-px d-inline-flex justify-content-center align-items-center bg-danger-100 text-danger-600 bg-hover-danger-600 text-hover-white text-md rounded-circle">
                                <i class="ri-delete-bin-5-line"></i>
                            </button>
                            <button type="button"
                                class="w-32-px h-32-px d-inline-flex justify-content-center align-items-center bg-success-100 text-success-600 bg-hover-success-600 text-hover-white text-md rounded-circle">
                                <i class="ri-download-2-fill"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
  
  <script>
  import iconPdf from '@/assets/images/home-eight/icon-pdf.png'
  import iconText from '@/assets/images/home-eight/icon-text.png'

  export default {
    name: 'HealthReportsCard',
    data() {
      return {
        reports: [
          {
            name: 'Checkup Result.pdf',
            size: '2.5mb',
            icon: iconPdf
          },
          {
            name: 'Checkup Result.doc',
            size: '2mb',
            icon: iconText
          },
          {
            name: 'Prescription.pdf',
            size: '3mb',
            icon: iconPdf
          },
          {
            name: 'Xray Result.doc',
            size: '3mb',
            icon: iconText
          },
          {
            name: 'Glucose Level Report.pdf',
            size: '3mb',
            icon: iconPdf
          },
          {
            name: 'Checkup Result.doc',
            size: '2mb',
            icon: iconText
          }
        ]
      };
    }
  };
  </script>
  