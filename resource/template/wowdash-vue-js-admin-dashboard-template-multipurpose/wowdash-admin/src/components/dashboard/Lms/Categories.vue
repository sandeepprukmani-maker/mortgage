<template>
  <div class="col-xxl-4 col-md-6">
    <div class="card">
      <div class="card-header">
        <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
          <h6 class="mb-2 fw-bold text-lg mb-0">Top Categories</h6>
          <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
            View All
            <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
          </a>
        </div>
      </div>
      <div class="card-body">
        <div
          v-for="(category, index) in categories"
          :key="index"
          class="d-flex align-items-center justify-content-between gap-3"
          :class="{ 'mb-24': index !== categories.length - 1, 'mb-0': index === categories.length - 1 }"
        >
          <div class="d-flex align-items-center gap-12">
            <div :class="['w-40-px h-40-px radius-8 flex-shrink-0 d-flex justify-content-center align-items-center', category.bgColor]">
              <img :src="category.image" alt="" />
            </div>
            <div class="flex-grow-1">
              <h6 class="text-md mb-0 fw-normal">{{ category.title }}</h6>
              <span class="text-sm text-secondary-light fw-normal">{{ category.courses }}</span>
            </div>
          </div>
          <a href="#" class="w-24-px h-24-px bg-primary-50 text-primary-600 d-flex justify-content-center align-items-center text-lg bg-hover-primary-100 radius-4">
            <i class="ri-arrow-right-s-line"></i>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import icon1 from "@/assets/images/home-six/category-icon1.png"
import icon2 from "@/assets/images/home-six/category-icon2.png"
import icon3 from "@/assets/images/home-six/category-icon3.png"
import icon4 from "@/assets/images/home-six/category-icon4.png"
import icon5 from "@/assets/images/home-six/category-icon5.png"
import icon6 from "@/assets/images/home-six/category-icon6.png"

export default {
  name: "TopCategoriesCard",
  data() {
    return {
      categories: [
        {
          title: "Web Development",
          courses: "40+ Courses",
          image: icon1,
          bgColor: "bg-info-50",
        },
        {
          title: "Graphic Design",
          courses: "40+ Courses",
          image: icon2,
          bgColor: "bg-success-50",
        },
        {
          title: "UI/UX Design",
          courses: "40+ Courses",
          image: icon3,
          bgColor: "bg-lilac-50",
        },
        {
          title: "Digital Marketing",
          courses: "40+ Courses",
          image: icon4,
          bgColor: "bg-warning-50",
        },
        {
          title: "3d Illustration & Art Design",
          courses: "40+ Courses",
          image: icon5,
          bgColor: "bg-danger-50",
        },
        {
          title: "Logo Design",
          courses: "40+ Courses",
          image: icon6,
          bgColor: "bg-primary-50",
        }
      ]
    };
  }
};
</script>