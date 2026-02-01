<template>
    <div class="col-xxl-9">
      <div class="card h-100 p-0 email-card overflow-x-auto d-block">
        <div class="min-w-450-px d-flex flex-column justify-content-between h-100">
          <div class="card-header border-bottom bg-base py-16 px-24 d-flex align-items-center gap-3 justify-content-between flex-wrap">
            <div class="d-flex align-items-center gap-2">
              <button class="text-secondary-light d-flex me-8">
                <iconify-icon icon="mingcute:arrow-left-line" class="icon fs-3 line-height-1"></iconify-icon>
              </button>
              <h6 class="mb-0 text-lg">Kathryn Murphy</h6>
              <span class="bg-primary-50 text-primary-600 text-sm radius-4 px-8">Personal</span>
            </div>
            <div class="d-flex align-items-center gap-3">
              <button class="text-secondary-light d-flex">
                <iconify-icon icon="mi:print" class="icon text-xxl line-height-1"></iconify-icon>
              </button>
              <button class="text-secondary-light d-flex">
                <iconify-icon icon="mdi:star-outline" class="icon text-xxl line-height-1"></iconify-icon>
              </button>
              <button class="text-secondary-light d-flex">
                <iconify-icon icon="material-symbols:delete-outline" class="icon text-xxl line-height-1"></iconify-icon>
              </button>
            </div>
          </div>
  
          <div class="card-body p-0">
            <div class="py-16 px-24 border-bottom">
              <div class="d-flex align-items-start gap-3">
                <img src="@/assets/images/user-list/user-list1.png" alt="" class="w-40-px h-40-px rounded-pill" />
                <div>
                  <div class="d-flex align-items-center flex-wrap gap-2">
                    <h6 class="mb-0 text-lg">Kathryn Murphy</h6>
                    <span class="text-secondary-light text-md">kathrynmurphy@gmail.com</span>
                  </div>
                  <div class="mt-20">
                    <p class="mb-16 text-primary-light">Hi William</p>
                    <p class="mb-16 text-primary-light">
                      Just confirming that we transferred $63.86 to you via PayPal
                      <a href="javascript:void(0)" class="text-primary-600 text-decoration-underline">(info367@gmail.com)</a>
                      which you earned on the themewow Market since your last payout.
                    </p>
                    <p class="mb-0 text-primary-light">Thank you for selling with us!</p>
                  </div>
                </div>
              </div>
            </div>
  
            <div class="py-16 px-24 border-bottom">
              <div class="d-flex align-items-start gap-3">
                <img src="@/assets/images/user-list/user-list2.png" alt="" class="w-40-px h-40-px rounded-pill" />
                <div>
                  <div class="d-flex align-items-center flex-wrap gap-2">
                    <h6 class="mb-0 text-lg">Subrata Sen</h6>
                    <span class="text-secondary-light text-md">subratasen@gmail.com</span>
                  </div>
                  <div class="mt-20">
                    <p class="mb-0 text-primary-light">Awesome, thank you so much!</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
          <div class="card-footer py-16 px-24 bg-base shadow-top">
            <form action="#">
              <div class="d-flex align-items-center justify-content-between">
                <textarea
                  ref="messageInput"
                  class="textarea-max-height form-control p-0 border-0 py-8 pe-16 resize-none scroll-sm"
                  placeholder="Write massage"
                  @input="adjustHeight"
                ></textarea>
                <div class="d-flex align-items-center gap-4 ms-16">
                  <div>
                    <label for="attatchment" class="text-secondary-light text-xl">
                      <iconify-icon icon="octicon:link-16" class="icon line-height-1"></iconify-icon>
                    </label>
                    <input type="file" id="attatchment" hidden />
                  </div>
                  <div>
                    <label for="gallery" class="text-secondary-light text-xl">
                      <iconify-icon icon="solar:gallery-bold" class="icon line-height-1"></iconify-icon>
                    </label>
                    <input type="file" id="gallery" hidden />
                  </div>
                  <button
                    type="submit"
                    class="btn btn-primary text-sm btn-sm px-12 py-12 w-100 radius-8 d-flex align-items-center justify-content-center gap-1 h-44-px"
                  >
                    <iconify-icon icon="ion:paper-plane-outline" class="icon text-lg line-height-1"></iconify-icon>
                    Send
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      adjustHeight(event) {
        const textarea = event.target;
        textarea.style.height = 'auto';
        const scrollHeight = textarea.scrollHeight;
  
        if (scrollHeight > 44 && scrollHeight <= 60) {
          textarea.style.height = `${scrollHeight}px`;
        } else if (scrollHeight > 60) {
          textarea.style.height = `60px`;
        }
      },
    },
  };
  </script>
  