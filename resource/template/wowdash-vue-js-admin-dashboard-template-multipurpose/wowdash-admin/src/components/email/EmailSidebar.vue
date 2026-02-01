<template>
    <div class="col-xxl-3">
      <div class="card h-100 p-0">
        <div class="card-body p-24">
          <button
            type="button"
            class="btn btn-primary text-sm btn-sm px-12 py-12 w-100 radius-8 d-flex align-items-center gap-2 mb-16"
            data-bs-toggle="modal"
            data-bs-target="#exampleModal"
          >
            <iconify-icon
              icon="fa6-regular:square-plus"
              class="icon text-lg line-height-1"
            ></iconify-icon>
            Compose
          </button>
  
          <div class="mt-16">
            <ul>
              <li class="item-active mb-4">
                <router-link
                  to="/email"
                  class="bg-hover-primary-50 px-12 py-8 w-100 radius-8 text-secondary-light"
                >
                  <span class="d-flex align-items-center gap-10 justify-content-between w-100">
                    <span class="d-flex align-items-center gap-10">
                      <span class="icon text-xxl line-height-1 d-flex">
                        <iconify-icon
                          icon="uil:envelope"
                          class="icon line-height-1"
                        ></iconify-icon>
                      </span>
                      <span class="fw-semibold">Inbox</span>
                    </span>
                    <span class="fw-medium">800</span>
                  </span>
                </router-link>
              </li>
  
              <li class="mb-4">
                <router-link
                  to="/starred-email"
                  class="bg-hover-primary-50 px-12 py-8 w-100 radius-8 text-secondary-light"
                >
                  <span class="d-flex align-items-center gap-10 justify-content-between w-100">
                    <span class="d-flex align-items-center gap-10">
                      <span class="icon text-xxl line-height-1 d-flex">
                        <iconify-icon
                          icon="ph:star-bold"
                          class="icon line-height-1"
                        ></iconify-icon>
                      </span>
                      <span class="fw-semibold">Starred</span>
                    </span>
                    <span class="fw-medium">250</span>
                  </span>
                </router-link>
              </li>
  
              <li class="mb-4">
                <router-link
                  to="/email"
                  class="bg-hover-primary-50 px-12 py-8 w-100 radius-8 text-secondary-light"
                >
                  <span class="d-flex align-items-center gap-10 justify-content-between w-100">
                    <span class="d-flex align-items-center gap-10">
                      <span class="icon text-xxl line-height-1 d-flex">
                        <iconify-icon
                          icon="ion:paper-plane-outline"
                          class="icon line-height-1"
                        ></iconify-icon>
                      </span>
                      <span class="fw-semibold">Sent</span>
                    </span>
                    <span class="fw-medium">80</span>
                  </span>
                </router-link>
              </li>
  
              <li class="mb-4">
                <router-link
                  to="/email"
                  class="bg-hover-primary-50 px-12 py-8 w-100 radius-8 text-secondary-light"
                >
                  <span class="d-flex align-items-center gap-10 justify-content-between w-100">
                    <span class="d-flex align-items-center gap-10">
                      <span class="icon text-xxl line-height-1 d-flex">
                        <iconify-icon
                          icon="lucide:pencil"
                          class="icon line-height-1"
                        ></iconify-icon>
                      </span>
                      <span class="fw-semibold">Draft</span>
                    </span>
                    <span class="fw-medium">50</span>
                  </span>
                </router-link>
              </li>
  
              <li class="mb-4">
                <router-link
                  to="/email"
                  class="bg-hover-primary-50 px-12 py-8 w-100 radius-8 text-secondary-light"
                >
                  <span class="d-flex align-items-center gap-10 justify-content-between w-100">
                    <span class="d-flex align-items-center gap-10">
                      <span class="icon text-xxl line-height-1 d-flex">
                        <iconify-icon
                          icon="ph:warning-bold"
                          class="icon line-height-1"
                        ></iconify-icon>
                      </span>
                      <span class="fw-semibold">Spam</span>
                    </span>
                    <span class="fw-medium">30</span>
                  </span>
                </router-link>
              </li>
  
              <li>
                <router-link
                  to="/email"
                  class="bg-hover-primary-50 px-12 py-8 w-100 radius-8 text-secondary-light"
                >
                  <span class="d-flex align-items-center gap-10 justify-content-between w-100">
                    <span class="d-flex align-items-center gap-10">
                      <span class="icon text-xxl line-height-1 d-flex">
                        <iconify-icon
                          icon="material-symbols:delete-outline"
                          class="icon line-height-1"
                        ></iconify-icon>
                      </span>
                      <span class="fw-semibold">Bin</span>
                    </span>
                    <span class="fw-medium">20</span>
                  </span>
                </router-link>
              </li>
            </ul>
  
            <div class="mt-24">
              <h6 class="text-lg fw-semibold text-primary-light mb-16">TAGS</h6>
              <ul>
                <li class="mb-20">
                  <span
                    class="line-height-1 fw-medium text-secondary-light text-sm d-flex align-items-center gap-10"
                  >
                    <span class="w-8-px h-8-px bg-primary-600 rounded-circle"></span>
                    Personal
                  </span>
                </li>
                <li class="mb-20">
                  <span
                    class="line-height-1 fw-medium text-secondary-light text-sm d-flex align-items-center gap-10"
                  >
                    <span class="w-8-px h-8-px bg-lilac-600 rounded-circle"></span>
                    Social
                  </span>
                </li>
                <li class="mb-20">
                  <span
                    class="line-height-1 fw-medium text-secondary-light text-sm d-flex align-items-center gap-10"
                  >
                    <span class="w-8-px h-8-px bg-success-600 rounded-circle"></span>
                    Promotions
                  </span>
                </li>
                <li class="mb-20">
                  <span
                    class="line-height-1 fw-medium text-secondary-light text-sm d-flex align-items-center gap-10"
                  >
                    <span class="w-8-px h-8-px bg-warning-600 rounded-circle"></span>
                    Business
                  </span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "EmailSidebar",
  };
  </script>
  