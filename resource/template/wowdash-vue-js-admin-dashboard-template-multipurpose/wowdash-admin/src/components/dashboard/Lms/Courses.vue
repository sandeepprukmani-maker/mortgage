<template>
    <div class="col-xxl-8">
      <div class="card h-100">
        <div class="card-header">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
            <h6 class="mb-2 fw-bold text-lg mb-0">Courses</h6>
            <a
              href="javascript:void(0)"
              class="text-primary-600 hover-text-primary d-flex align-items-center gap-1"
            >
              View All
              <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
            </a>
          </div>
        </div>
        <div class="card-body p-24">
          <div class="table-responsive scroll-sm">
            <table class="table bordered-table mb-0">
              <thead>
                <tr>
                  <th scope="col">Registered On</th>
                  <th scope="col">Instructors</th>
                  <th scope="col">Users</th>
                  <th scope="col">Enrolled</th>
                  <th scope="col">Price</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(course, index) in courses" :key="index">
                  <td>
                    <span class="text-secondary-light">{{ course.registeredOn }}</span>
                  </td>
                  <td>
                    <span class="text-secondary-light">{{ course.instructor }}</span>
                  </td>
                  <td>
                    <div class="text-secondary-light">
                      <h6 class="text-md mb-0 fw-normal">{{ course.name }}</h6>
                      <span class="text-sm fw-normal">{{ course.lessons }} Lessons</span>
                    </div>
                  </td>
                  <td>
                    <span class="text-secondary-light">{{ course.enrolled }}</span>
                  </td>
                  <td>
                    <span class="text-secondary-light">{{ course.price }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "CoursesTable",
    data() {
      return {
        courses: [
          {
            registeredOn: "24 Jun 2024",
            instructor: "Ronald Richards",
            name: "3d Illustration & Art Design",
            lessons: 34,
            enrolled: 257,
            price: "$29.00",
          },
          {
            registeredOn: "24 Jun 2024",
            instructor: "Jerome Bell",
            name: "Advanced JavaScript Development",
            lessons: 20,
            enrolled: 375,
            price: "$29.00",
          },
          {
            registeredOn: "24 Jun 2024",
            instructor: "Cody Fisher",
            name: "Portrait Drawing Fundamentals",
            lessons: 16,
            enrolled: 220,
            price: "$29.00",
          },
          {
            registeredOn: "24 Jun 2024",
            instructor: "Floyd Miles",
            name: "Advanced App Development",
            lessons: 25,
            enrolled: 57,
            price: "$29.00",
          },
          {
            registeredOn: "24 Jun 2024",
            instructor: "Ralph Edwards",
            name: "HTML Fundamental Course",
            lessons: 17,
            enrolled: 27,
            price: "$29.00",
          },
        ],
      };
    },
  };
  </script>