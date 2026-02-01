<template>
    <div class="card h-100 p-0 radius-12 overflow-hidden">
      <div class="card-body p-40">
        <form @submit.prevent="handleSubmit">
          <!-- Mail Notification Messages -->
          <div class="mb-24">
            <h6 class="mb-16">Mail Notification Messages</h6>
            <div class="d-flex flex-wrap justify-content-between gap-1">
              <label class="form-label fw-medium text-secondary-light text-md mb-8">Admin New Order Message</label>
              <div class="form-switch switch-primary d-flex align-items-center gap-3">
                <input
                  class="form-check-input"
                  type="checkbox"
                  role="switch"
                  id="On"
                  v-model="notificationSettings.mail.newOrderMessageStatus"
                />
                <label class="form-check-label line-height-1 fw-medium text-secondary-light" for="On">On</label>
              </div>
            </div>
            <textarea
              class="form-control radius-8 h-80-px"
              placeholder="You have a new order."
              v-model="notificationSettings.mail.newOrderMessage"
            ></textarea>
          </div>
  
          <!-- SMS Notification Messages -->
          <div class="mb-24">
            <h6 class="mb-16">Sms Notification Messages</h6>
            <div class="d-flex flex-wrap justify-content-between gap-1">
              <label class="form-label fw-medium text-secondary-light text-md mb-8">Admin New Order Message</label>
              <div class="form-switch switch-primary d-flex align-items-center gap-3">
                <input
                  class="form-check-input"
                  type="checkbox"
                  role="switch"
                  id="Off"
                  v-model="notificationSettings.sms.newOrderMessageStatus"
                />
                <label class="form-check-label line-height-1 fw-medium text-secondary-light" for="Off">OFF</label>
              </div>
            </div>
            <textarea
              class="form-control radius-8 h-80-px"
              placeholder="You have a new order."
              v-model="notificationSettings.sms.newOrderMessage"
            ></textarea>
          </div>
  
          <!-- Push Notification Messages -->
          <div class="mb-24">
            <h6 class="mb-16">Push Notification Messages</h6>
            <div class="d-flex flex-wrap justify-content-between gap-1">
              <label class="form-label fw-medium text-secondary-light text-md mb-8">Admin New Order Message</label>
              <div class="form-switch switch-primary d-flex align-items-center gap-3">
                <input
                  class="form-check-input"
                  type="checkbox"
                  role="switch"
                  id="Offf"
                  v-model="notificationSettings.push.newOrderMessageStatus"
                />
                <label class="form-check-label line-height-1 fw-medium text-secondary-light" for="Offf">OFF</label>
              </div>
            </div>
            <textarea
              class="form-control radius-8 h-80-px"
              placeholder="You have a new order."
              v-model="notificationSettings.push.newOrderMessage"
            ></textarea>
          </div>
  
          <!-- Buttons -->
          <div class="d-flex align-items-center justify-content-center gap-3 mt-24">
            <button type="reset" class="border border-danger-600 bg-hover-danger-200 text-danger-600 text-md px-40 py-11 radius-8">
              Reset
            </button>
            <button type="submit" class="btn btn-primary border border-primary-600 text-md px-24 py-12 radius-8">
              Save Change
            </button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        notificationSettings: {
          mail: {
            newOrderMessageStatus: true,
            newOrderMessage: "You have a new order."
          },
          sms: {
            newOrderMessageStatus: false,
            newOrderMessage: "You have a new order."
          },
          push: {
            newOrderMessageStatus: false,
            newOrderMessage: "You have a new order."
          }
        }
      };
    },
    methods: {
      handleSubmit() {
        // Handle form submission logic here, e.g., API call
        console.log("Notification Settings Submitted", this.notificationSettings);
      }
    }
  };
  </script>