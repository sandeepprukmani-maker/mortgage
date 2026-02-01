<template>
    <div class="card mt-24" id="comment-form">
      <div class="card-header border-bottom">
        <h6 class="text-xl mb-0">Add A Comment</h6>
      </div>
      <div class="card-body p-24">
        <form @submit.prevent="submitComment" class="d-flex flex-column gap-16">
          <div>
            <label class="form-label fw-semibold" for="username">Username</label>
            <input
              type="text"
              class="form-control border border-neutral-200 radius-8"
              id="username"
              placeholder="Enter your username"
              v-model="form.username"
            />
          </div>
          <div>
            <label class="form-label fw-semibold" for="email">Email</label>
            <input
              type="email"
              class="form-control border border-neutral-200 radius-8"
              id="email"
              placeholder="Enter your email"
              v-model="form.email"
            />
          </div>
          <div>
            <label class="form-label fw-semibold" for="desc">Email</label>
            <textarea
              class="form-control border border-neutral-200 radius-8"
              rows="4"
              cols="50"
              id="desc"
              placeholder="Enter a description..."
              v-model="form.desc"
            ></textarea>
          </div>
          <button type="submit" class="btn btn-primary-600 radius-8">Submit</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "AddCommentForm",
    data() {
      return {
        form: {
          username: "",
          email: "",
          desc: ""
        }
      };
    },
    methods: {
      submitComment() {
        // Handle form submission logic here
        console.log("Form submitted:", this.form);
  
        // Clear the form (optional)
        this.form.username = "";
        this.form.email = "";
        this.form.desc = "";
      }
    }
  };
  </script>
  