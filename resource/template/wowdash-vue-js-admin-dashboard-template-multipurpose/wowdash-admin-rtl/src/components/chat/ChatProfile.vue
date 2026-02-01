<template>
    <div class="chat-sidebar profile-setting card">
      <div class="text-end">
        <router-link to="chat-message">
          <iconify-icon icon="akar-icons:cross"></iconify-icon>
        </router-link>
      </div>
  
      <!-- Profile Info -->
      <div class="chat-main-profile">
        <div class="img">
          <img :src="profile.avatar" alt="image" />
        </div>
        <div class="text-center">
          <h6 class="text-md mb-0">{{ profile.name }}</h6>
          <p class="mb-0 text-sm">{{ profile.role }}</p>
        </div>
      </div>
  
      <!-- About -->
      <div class="mt-24">
        <label class="form-label">About Me</label>
        <textarea
          name="about"
          class="form-control"
          placeholder="Write some description"
          v-model="profile.about"
        ></textarea>
      </div>
  
      <!-- Details -->
      <div class="mt-24">
        <ul class="d-flex flex-column gap-1">
          <li
            class="d-flex flex-wrap align-items-center justify-content-between"
            v-for="(item, index) in profile.details"
            :key="index"
          >
            <span class="d-inline-flex gap-2 align-items-center">
              <iconify-icon :icon="item.icon" class="text-lg"></iconify-icon>
              {{ item.label }}
            </span>
            <span class="text-primary-light">{{ item.value }}</span>
          </li>
        </ul>
      </div>
  
      <!-- Status -->
      <div class="mt-24">
        <h6 class="text-lg">Status</h6>
        <div class="d-flex flex-column gap-1">
          <div
            class="form-check d-flex align-items-center"
            v-for="(statusOption, index) in statusOptions"
            :key="index"
          >
            <input
              class="form-check-input"
              type="radio"
              :id="'status' + (index + 1)"
              name="status"
              :value="statusOption"
              v-model="selectedStatus"
            />
            <label class="form-check-label" :for="'status' + (index + 1)">
              {{ statusOption }}
            </label>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import userImg from "@/assets/images/chat/chat-main.png"
  export default {
    data() {
      return {
        profile: {
          name: "Kathryn Murphy",
          role: "Admin",
          avatar: userImg,
          about: "",
          details: [
            {
              label: "Location",
              value: "United State",
              icon: "mingcute:location-line"
            },
            {
              label: "Member since",
              value: "25 Jan 2025",
              icon: "fluent:person-24-regular"
            },
            {
              label: "Language",
              value: "English",
              icon: "cil:language"
            }
          ]
        },
        statusOptions: ["Active", "Do Not Disturb", "Away", "Offline"],
        selectedStatus: "Active"
      };
    }
  };
  </script>
  