<template>
    <div class="col-xxl-4 col-md-6">
      <div class="card">
        <div class="card-header">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg mb-0">Student's Progress</h6>
            <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
              View All
              <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
            </a>
          </div>
        </div>
        <div class="card-body">
          <div
            v-for="(student, index) in students"
            :key="index"
            class="d-flex align-items-center justify-content-between gap-3"
            :class="{'mb-24': index !== students.length - 1, 'mb-0': index === students.length -1 }"
          >
            <div class="d-flex align-items-center">
              <img
                :src="student.img"
                alt=""
                class="w-40-px h-40-px radius-8 flex-shrink-0 me-12 overflow-hidden"
              />
              <div class="flex-grow-1">
                <h6 class="text-md mb-0 fw-medium">{{ student.name }}</h6>
                <span class="text-sm text-secondary-light fw-medium">{{ student.course }}</span>
              </div>
            </div>
            <div>
              <span class="text-primary-light text-sm d-block text-end">
                <svg class="radial-progress" viewBox="0 0 80 80">
                  <circle class="incomplete" cx="40" cy="40" r="35"></circle>
                  <circle
                    class="complete"
                    cx="40"
                    cy="40"
                    r="35"
                    :style="{ strokeDashoffset: student.offset, transition: 'stroke-dashoffset 1.5s ease' }"
                  ></circle>
                  <text class="percentage" x="50%" y="57%" transform="matrix(0, 1, -1, 0, 80, 0)">
                    {{ student.percentage }}
                  </text>
                </svg>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import student1 from "@/assets/images/home-six/student-img1.png"
  import student2 from "@/assets/images/home-six/student-img2.png"
  import student3 from "@/assets/images/home-six/student-img3.png"
  import student4 from "@/assets/images/home-six/student-img4.png"
  import student5 from "@/assets/images/home-six/student-img5.png"
  import student6 from "@/assets/images/home-six/student-img6.png"

  export default {
    name: "StudentsProgress",
    data() {
      return {
        radius: 35,
        students: [
          {
            name: "Theresa Webb",
            course: "UI/UX Design Course",
            img: student1,
            percentage: 33,
            offset: 2 * Math.PI * 35,
          },
          {
            name: "Robert Fox",
            course: "Graphic Design Course",
            img: student2,
            percentage: 70,
            offset: 2 * Math.PI * 35,
          },
          {
            name: "Guy Hawkins",
            course: "Web developer Course",
            img: student3,
            percentage: 80,
            offset: 2 * Math.PI * 35,
          },
          {
            name: "Cody Fisher",
            course: "UI/UX Design Course",
            img: student4,
            percentage: 20,
            offset: 2 * Math.PI * 35,
          },
          {
            name: "Jacob Jones",
            course: "UI/UX Design Course",
            img: student5,
            percentage: 40,
            offset: 2 * Math.PI * 35,
          },
          {
            name: "Darlene Robertson",
            course: "UI/UX Design Course",
            img: student6,
            percentage: 24,
            offset: 2 * Math.PI * 35,
          },
        ],
      };
    },
    mounted() {
      this.animateProgress();
    },
    methods: {
      calculateOffset(percentage) {
        const circumference = 2 * Math.PI * this.radius;
        return ((100 - percentage) / 100) * circumference;
      },
      animateProgress() {
        this.students.forEach((student, index) => {
          setTimeout(() => {
            student.offset = this.calculateOffset(student.percentage);
          }, 100); // small delay for smooth transition
        });
      },
    },
  };
  </script>
  