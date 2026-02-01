<template>
  <div class="col-lg-8">
    <div class="shadow-7 radius-12 bg-base h-100 overflow-hidden">
      <div class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center justify-content-between">
        <h6 class="text-lg fw-semibold mb-0">To Do List</h6>
        <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
          View All
          <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
        </a>
      </div>
      <div class="card-body p-0">
        <div class="table-responsive scroll-sm">
          <table class="table bordered-table table-py-8 mb-0 rounded-0 border-0">
            <thead>
              <tr>
                <th scope="col" class="rounded-0">
                  <div class="d-flex align-items-center gap-10">
                    <div class="form-check style-check d-flex align-items-center">
                      <input class="form-check-input radius-4 border border-neutral-300 input-form-dark" type="checkbox" v-model="selectAll" @change="toggleAll">
                    </div>
                    ID
                  </div>
                </th>
                <th scope="col" class="rounded-0">Task Name</th>
                <th scope="col" class="rounded-0">Assigned To</th>
                <th scope="col" class="rounded-0">Due Date</th>
                <th scope="col" class="rounded-0">Priority</th>
                <th scope="col" class="rounded-0">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(task, index) in tasks" :key="index">
                <td class="text-secondary-light">
                  <div class="d-flex align-items-center gap-10">
                    <div class="form-check style-check d-flex align-items-center">
                      <input class="form-check-input radius-4 border border-neutral-300 input-form-dark" type="checkbox" v-model="task.checked">
                    </div>
                    {{ task.id }}
                  </div>
                </td>
                <td class="text-secondary-light">{{ task.name }}</td>
                <td class="text-secondary-light">
                  <div class="d-flex align-items-center">
                    <span v-for="(img, i) in task.assignees" :key="i" class="w-36-px h-36-px border border-white rounded-circle shadow-8" :class="{ 'ms--10px': i !== 0 }">
                      <img :src="img" alt="Image" class="w-100 h-100 object-fit-cover">
                    </span>
                    <label v-if="task.allowUpload" class="w-36-px h-36-px border border-white rounded-circle shadow-8 ms--10px d-inline-flex justify-content-center align-items-center bg-primary-600 text-white" for="uploadImage">
                      <i class="ri-add-fill"></i>
                      <input type="file" id="uploadImage" hidden>
                    </label>
                  </div>
                </td>
                <td class="text-secondary-light">{{ task.dueDate }}</td>
                <td class="text-secondary-light">{{ task.priority }}</td>
                <td class="text-center">
                  <span :class="task.statusClass + ' px-16 py-2 radius-4 fw-medium text-sm'">{{ task.status }}</span>
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
import todoImg1 from "@/assets/images/homeThirteen/todo-list-img1.png"
import todoImg2 from "@/assets/images/homeThirteen/todo-list-img2.png"
import todoImg3 from "@/assets/images/homeThirteen/todo-list-img3.png"
import todoImg4 from "@/assets/images/homeThirteen/todo-list-img4.png"

export default {
  name: "ToDoList",
  data() {
    return {
      selectAll: false,
      tasks: [
        {
          id: 26531,
          name: "Mobile app Development",
          assignees: [ todoImg1, todoImg2, todoImg3, todoImg4 ],
          dueDate: "Feb 10, 2025",
          priority: "High",
          status: "Basic",
          statusClass: "bg-success-focus text-success-main",
          checked: false,
          allowUpload: true
        },
        {
          id: 26531,
          name: "Product design",
          assignees: [ todoImg1, todoImg2, todoImg3 ],
          dueDate: "Feb 10, 2025",
          priority: "Low",
          status: "Standard",
          statusClass: "bg-warning-focus text-warning-main",
          checked: false,
          allowUpload: false
        },
        {
          id: 26531,
          name: "UI/UX Design",
          assignees: [ todoImg1, todoImg2 ],
          dueDate: "Feb 10, 2025",
          priority: "Medium",
          status: "Premium",
          statusClass: "bg-info-focus text-info-main",
          checked: false,
          allowUpload: false
        },
        {
          id: 26531,
          name: "Website ui design",
          assignees: [ todoImg1, todoImg2, todoImg3 ],
          dueDate: "Feb 10, 2025",
          priority: "High",
          status: "Basic",
          statusClass: "bg-success-focus text-success-main",
          checked: false,
          allowUpload: false
        },
        {
          id: 26531,
          name: "PHP Project",
          assignees: [ todoImg1 ],
          dueDate: "Feb 10, 2025",
          priority: "Low",
          status: "Standard",
          statusClass: "bg-warning-focus text-warning-main",
          checked: false,
          allowUpload: false
        }
      ]
    };
  },
  methods: {
    toggleAll() {
      this.tasks.forEach(task => {
        task.checked = this.selectAll;
      });
    }
  }
};
</script>
