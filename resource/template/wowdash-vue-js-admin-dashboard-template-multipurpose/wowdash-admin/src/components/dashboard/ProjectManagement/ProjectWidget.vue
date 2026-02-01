<template>
    <!-- Widgets start -->
    <div class="col-xxl-3 col-sm-6" v-for="(widget, index) in widgets" :key="index">
      <div class="bg-base p-16 radius-8 position-relative overflow-hidden">
        <span :class="['blur-gradient', widget.blurClass, 'position-absolute', 'end-0', 'top-50']"></span>
  
        <div class="d-flex align-items-center justify-content-between gap-1">
          <div class="">
            <span class="text-secondary-light text-sm fw-medium">{{ widget.title }}</span>
            <h6 class="text-2xl mb-0">{{ widget.value }}</h6>
          </div>
          <span :class="['w-40-px', 'h-40-px', 'radius-8', widget.iconBgClass, 'text-white', 'd-flex', 'justify-content-center', 'align-items-center', 'text-xxl']">
            <i :class="widget.iconClass"></i>
          </span>
        </div>
        <a href="javascript:void(0)" class="btn btn-success-100 text-success-600 text-sm py-1 px-16 mt-10">View More</a>
      </div>
    </div>
    <!-- Widgets End -->
  </template>
  
  <script>
  export default {
    data() {
      return {
        widgets: [
          {
            title: "Total Projects",
            value: 320,
            blurClass: "blur-gradient-1",
            iconBgClass: "bg-danger-600",
            iconClass: "ri-file-text-fill",
          },
          {
            title: "Total Clients",
            value: 547,
            blurClass: "blur-gradient-2",
            iconBgClass: "bg-success-600",
            iconClass: "ri-user-2-fill",
          },
          {
            title: "Team Members",
            value: 356,
            blurClass: "blur-gradient-3",
            iconBgClass: "bg-warning-600",
            iconClass: "ri-group-fill",
          },
          {
            title: "Finished Projects",
            value: 435,
            blurClass: "blur-gradient-4",
            iconBgClass: "bg-info-600",
            iconClass: "ri-file-list-3-fill",
          }
        ]
      };
    }
  };
  </script>