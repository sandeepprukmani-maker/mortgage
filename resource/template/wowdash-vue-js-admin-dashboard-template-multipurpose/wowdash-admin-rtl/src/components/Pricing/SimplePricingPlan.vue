<template>
    <div class="card h-100 p-0 radius-12 overflow-hidden mt-24">
      <div class="card-header border-bottom bg-base py-16 px-24">
        <h6 class="mb-0 text-lg">Simple Pricing Plan</h6>
      </div>
      <div class="card-body p-40">
        <div class="row justify-content-center">
          <div class="col-xxl-10">
            <div class="text-center">
              <h4 class="mb-16">Simple, Transparent Pricing</h4>
              <p class="mb-0 text-lg text-secondary-light">
                Lorem ipsum dolor sit amet consectetur adipiscing elit dolor posuere vel venenatis eu sit massa volutpat.
              </p>
            </div>
  
            <div class="pricing-tab">
              <div class="form-switch switch-primary d-flex align-items-center gap-3 mt-40 justify-content-center">
                <label class="form-check-label line-height-1 fw-medium text-secondary-light" for="toggle">Monthly</label>
                <input class="form-check-input" type="checkbox" role="switch" id="toggle" v-model="isAnnually" />
                <label class="form-check-label line-height-1 fw-medium text-secondary-light" for="toggle">Annually</label>
              </div>
            </div>
  
            <div class="row gy-4">
              <!-- Basic Plan -->
              <div class="col-xxl-4 col-sm-6">
                <div class="pricing-plan position-relative radius-24 overflow-hidden border bg-base">
                  <div class="d-flex align-items-center gap-16">
                    <span class="w-72-px h-72-px d-flex justify-content-center align-items-center radius-16 bg-primary-50">
                      <img src="@/assets/images/pricing/price-icon4.png" alt="" />
                    </span>
                    <div>
                      <span class="fw-medium text-md text-secondary-light">For individuals</span>
                      <h6 class="mb-0">Basic</h6>
                    </div>
                  </div>
                  <p class="mt-16 mb-0 text-secondary-light mb-28">Lorem ipsum dolor sit amet doloroli sitiol conse ctetur adipiscing elit.</p>
                  <h3 class="mb-24">
                    ${{ isAnnually ? 99 * 12 : 99 }}
                    <span class="fw-medium text-md text-secondary-light">/{{ isAnnually ? 'annually' : 'monthly' }}</span>
                  </h3>
                  <span class="mb-20 fw-medium">What’s included</span>
                  <ul>
                    <li class="d-flex align-items-center gap-16 mb-16" v-for="(item, index) in features" :key="'basic-' + index">
                      <span class="w-24-px h-24-px d-flex justify-content-center align-items-center bg-primary-600 rounded-circle">
                        <iconify-icon icon="iconamoon:check-light" class="text-white text-lg"></iconify-icon>
                      </span>
                      <span class="text-secondary-light text-lg">{{ item }}</span>
                    </li>
                  </ul>
                  <button type="button" class="bg-primary-600 bg-hover-primary-700 text-white text-center border border-primary-600 text-sm btn-sm px-12 py-10 w-100 radius-8 mt-28" data-bs-toggle="modal" data-bs-target="#exampleModal">Get started</button>
                </div>
              </div>
  
              <!-- Pro Plan -->
              <div class="col-xxl-4 col-sm-6">
                <div class="pricing-plan featured-item position-relative radius-24 overflow-hidden border bg-primary-600 text-white z-1">
                  <img src="@/assets/images/pricing/pricing-shape.png" alt="" class="position-absolute end-0 top-10 z-n1" />
                  <span class="bg-white bg-opacity-25 text-white radius-24 py-8 px-24 text-sm position-absolute end-0 top-0 z-1 rounded-start-top-0 rounded-end-bottom-0">Popular</span>
                  <div class="d-flex align-items-center gap-16">
                    <span class="w-72-px h-72-px d-flex justify-content-center align-items-center radius-16 bg-base">
                      <img src="@/assets/images/pricing/price-icon2.png" alt="" />
                    </span>
                    <div>
                      <span class="fw-medium text-md text-white">For startups</span>
                      <h6 class="mb-0 text-white">Pro</h6>
                    </div>
                  </div>
                  <p class="mt-16 mb-0 text-white mb-28">Lorem ipsum dolor sit amet doloroli sitiol conse ctetur adipiscing elit.</p>
                  <h3 class="mb-24 text-white">
                    ${{ isAnnually ? 199 * 12 : 199 }}
                    <span class="fw-medium text-md text-white">/{{ isAnnually ? 'annually' : 'monthly' }}</span>
                  </h3>
                  <span class="mb-20 fw-medium">What’s included</span>
                  <ul>
                    <li class="d-flex align-items-center gap-16 mb-16" v-for="(item, index) in features" :key="'pro-' + index">
                      <span class="w-24-px h-24-px d-flex justify-content-center align-items-center bg-white rounded-circle text-primary-600">
                        <iconify-icon icon="iconamoon:check-light" class="text-lg"></iconify-icon>
                      </span>
                      <span class="text-white text-lg">{{ item }}</span>
                    </li>
                  </ul>
                  <button type="button" class="bg-white text-primary-600 text-white text-center border border-white text-sm btn-sm px-12 py-10 w-100 radius-8 mt-28" data-bs-toggle="modal" data-bs-target="#exampleModal">Get started</button>
                </div>
              </div>
  
              <!-- Enterprise Plan -->
              <div class="col-xxl-4 col-sm-6">
                <div class="pricing-plan position-relative radius-24 overflow-hidden border bg-base">
                  <div class="d-flex align-items-center gap-16">
                    <span class="w-72-px h-72-px d-flex justify-content-center align-items-center radius-16 bg-primary-50">
                      <img src="@/assets/images/pricing/price-icon5.png" alt="" />
                    </span>
                    <div>
                      <span class="fw-medium text-md text-secondary-light">For big companies</span>
                      <h6 class="mb-0">Enterprise</h6>
                    </div>
                  </div>
                  <p class="mt-16 mb-0 text-secondary-light mb-28">Lorem ipsum dolor sit amet doloroli sitiol conse ctetur adipiscing elit.</p>
                  <h3 class="mb-24">
                    ${{ isAnnually ? 399 * 12 : 399 }}
                    <span class="fw-medium text-md text-secondary-light">/{{ isAnnually ? 'annually' : 'monthly' }}</span>
                  </h3>
                  <span class="mb-20 fw-medium">What’s included</span>
                  <ul>
                    <li class="d-flex align-items-center gap-16 mb-16" v-for="(item, index) in features" :key="'enterprise-' + index">
                      <span class="w-24-px h-24-px d-flex justify-content-center align-items-center bg-primary-600 rounded-circle">
                        <iconify-icon icon="iconamoon:check-light" class="text-white text-lg"></iconify-icon>
                      </span>
                      <span class="text-secondary-light text-lg">{{ item }}</span>
                    </li>
                  </ul>
                  <button type="button" class="bg-primary-600 bg-hover-primary-700 text-white text-center border border-primary-600 text-sm btn-sm px-12 py-10 w-100 radius-8 mt-28" data-bs-toggle="modal" data-bs-target="#exampleModal">Get started</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'PricingSection',
    data() {
      return {
        isAnnually: false,
        features: [
          "All analytics features",
          "Up to 250,000 tracked visits",
          "Normal support",
          "Up to 3 team members"
        ]
      };
    }
  };
  </script>
  