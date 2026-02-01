<template>
    <div class="col-xxl-12 col-md-6">
      <div class="card h-100">
        <div class="card-header border-bottom d-flex align-items-center flex-wrap gap-2 justify-content-between">
          <h6 class="fw-bold text-lg mb-0">Featured Creators</h6>
          <a href="javascript:void(0)" class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
            View All
            <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
          </a>
        </div>
        <div class="card-body">
          <div class="d-flex align-items-center justify-content-between gap-8 flex-wrap">
            <div class="d-flex align-items-center">
              <img src="@/assets/images/nft/nft-items-img1.png" alt="" class="flex-shrink-0 me-12 w-40-px h-40-px rounded-circle me-12">
              <div class="flex-grow-1">
                <h6 class="text-md mb-0 fw-semibold">Theresa Webb</h6>
                <span class="text-sm text-secondary-light fw-normal">Owned by ABC</span>
              </div>
            </div>
            <button type="button" class="btn btn-outline-primary-600 px-24 rounded-pill">Follow</button>
          </div>
          <div class="mt-24">
            <div class="row gy-3">
              <div class="col-sm-6 col-xs-6">
                <div class="nft-card bg-base radius-16 overflow-hidden shadow-4">
                  <div class="radius-16 overflow-hidden">
                    <img src="@/assets/images/nft/featured-creator1.png" alt="" class="w-100 h-100 object-fit-cover">
                  </div>
                  <div class="p-12">
                    <h6 class="text-md fw-bold text-primary-light mb-12">New Figures</h6>
                    <div class="d-flex align-items-center gap-8">
                      <img src="@/assets/images/nft/bitcoin.png" class="w-28-px h-28-px rounded-circle object-fit-cover" alt="">
                      <span class="text-sm text-secondary-light fw-medium">0.10 BTC</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-sm-6 col-xs-6">
                <div class="nft-card bg-base radius-16 overflow-hidden shadow-4">
                  <div class="radius-16 overflow-hidden">
                    <img src="@/assets/images/nft/featured-creator2.png" alt="" class="w-100 h-100 object-fit-cover">
                  </div>
                  <div class="p-12">
                    <h6 class="text-md fw-bold text-primary-light mb-12">Abstrac Girl</h6>
                    <div class="d-flex align-items-center gap-8">
                      <img src="@/assets/images/nft/bitcoin.png" class="w-28-px h-28-px rounded-circle object-fit-cover" alt="">
                      <span class="text-sm text-secondary-light fw-medium">0.10 BTC</span>
                    </div>
                  </div>
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
    name: 'FeaturedCreators'
  };
  </script>
  