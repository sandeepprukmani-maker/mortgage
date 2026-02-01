<template>
    <div class="card h-100 p-0 radius-12 overflow-hidden">
      <div class="card-body p-40">
        <form @submit.prevent="handleSubmit">
          <div class="row">
            <div class="col-sm-6">
              <div class="mb-20">
                <label for="firebaseSecretKey" class="form-label fw-semibold text-primary-light text-sm mb-8">
                  Firebase secret key
                </label>
                <input
                  v-model="firebaseData.firebaseSecretKey"
                  type="text"
                  class="form-control radius-8"
                  id="firebaseSecretKey"
                  placeholder="Firebase secret key"
                />
              </div>
            </div>
            <div class="col-sm-6">
              <div class="mb-20">
                <label for="firebasePublicVapidKey" class="form-label fw-semibold text-primary-light text-sm mb-8">
                  Firebase public vapid key (key pair)
                </label>
                <input
                  v-model="firebaseData.firebasePublicVapidKey"
                  type="text"
                  class="form-control radius-8"
                  id="firebasePublicVapidKey"
                  placeholder="Firebase public vapid key (key pair)"
                />
              </div>
            </div>
            <div class="col-sm-6">
              <div class="mb-20">
                <label for="firebaseAPIKey" class="form-label fw-semibold text-primary-light text-sm mb-8">
                  Firebase API Key
                </label>
                <input
                  v-model="firebaseData.firebaseAPIKey"
                  type="text"
                  class="form-control radius-8"
                  id="firebaseAPIKey"
                  placeholder="Firebase API Key"
                />
              </div>
            </div>
            <div class="col-sm-6">
              <div class="mb-20">
                <label for="firebaseAuthDomain" class="form-label fw-semibold text-primary-light text-sm mb-8">
                  Firebase AUTH Domain
                </label>
                <input
                  v-model="firebaseData.firebaseAuthDomain"
                  type="text"
                  class="form-control radius-8"
                  id="firebaseAuthDomain"
                  placeholder="Firebase AUTH Domain"
                />
              </div>
            </div>
            <div class="col-sm-6">
              <div class="mb-20">
                <label for="firebaseProjectID" class="form-label fw-semibold text-primary-light text-sm mb-8">
                  Firebase Project ID
                </label>
                <input
                  v-model="firebaseData.firebaseProjectID"
                  type="text"
                  class="form-control radius-8"
                  id="firebaseProjectID"
                  placeholder="Firebase Project ID"
                />
              </div>
            </div>
            <div class="col-sm-6">
              <div class="mb-20">
                <label for="firebaseStorageBucket" class="form-label fw-semibold text-primary-light text-sm mb-8">
                  Firebase Storage Bucket
                </label>
                <input
                  v-model="firebaseData.firebaseStorageBucket"
                  type="text"
                  class="form-control radius-8"
                  id="firebaseStorageBucket"
                  placeholder="Firebase Storage Bucket"
                />
              </div>
            </div>
            <div class="col-sm-6">
              <div class="mb-20">
                <label for="firebaseMessageSenderID" class="form-label fw-semibold text-primary-light text-sm mb-8">
                  Firebase Message Sender ID
                </label>
                <input
                  v-model="firebaseData.firebaseMessageSenderID"
                  type="text"
                  class="form-control radius-8"
                  id="firebaseMessageSenderID"
                  placeholder="Firebase Message Sender ID"
                />
              </div>
            </div>
            <div class="col-sm-6">
              <div class="mb-20">
                <label for="firebaseAppID" class="form-label fw-semibold text-primary-light text-sm mb-8">
                  Firebase App ID
                </label>
                <input
                  v-model="firebaseData.firebaseAppID"
                  type="text"
                  class="form-control radius-8"
                  id="firebaseAppID"
                  placeholder="Firebase App ID"
                />
              </div>
            </div>
            <div class="col-sm-12">
              <div class="mb-20">
                <label for="firebaseMeasurmentID" class="form-label fw-semibold text-primary-light text-sm mb-8">
                  Firebase Measurement ID
                </label>
                <input
                  v-model="firebaseData.firebaseMeasurmentID"
                  type="text"
                  class="form-control radius-8"
                  id="firebaseMeasurmentID"
                  placeholder="Firebase Measurement ID"
                />
              </div>
            </div>
  
            <div class="d-flex align-items-center justify-content-center gap-3 mt-24">
              <button type="reset" class="border border-danger-600 bg-hover-danger-200 text-danger-600 text-md px-40 py-11 radius-8">
                Reset
              </button>
              <button type="submit" class="btn btn-primary border border-primary-600 text-md px-24 py-12 radius-8">
                Save Change
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        firebaseData: {
          firebaseSecretKey: "AAAAxGHw9lE:APA91bHKj6OsrD6EhnG5p26oTiQkXvOxTZwZEfVuuuipyUSNM-a8NB_CugVwfvvaosOvWgFAhQJOLMvxtv7e3Sw8DYpaWKwJIN3kjyIPoNRAe541sBz3x7E6sXZkA-ebueqnQiqNtbdP",
          firebasePublicVapidKey: "BKAvKJbnB3QATdp8n1aUo_uhoNK3exVKLVzy7MP8VKydjjzthdlAWdlku6LQISxm4zA7dWoRACI9AHymf4V64kA",
          firebaseAPIKey: "AIzaSyDg1xBSwmHKV0usIKxTFL5a6fFTb4s3XVM",
          firebaseAuthDomain: "wowdash.firebaseapp.com",
          firebaseProjectID: "wowdash.com",
          firebaseStorageBucket: "wowdash.appsport.com",
          firebaseMessageSenderID: "52362145",
          firebaseAppID: "1:843456771665:web:ac1e3115e9e17ee1582a70",
          firebaseMeasurmentID: "G-GSJPS921XW",
        }
      };
    },
    methods: {
      handleSubmit() {
        // Handle form submission logic here, e.g., API call
        console.log("Firebase Data Submitted", this.firebaseData);
      },
    },
  };
  </script>