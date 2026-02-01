<template>
    <div class="col-12">
      <div class="nft-promo-card card radius-12 overflow-hidden position-relative z-1">
        <img
          src="@/assets/images/nft/nft-gradient-bg.png"
          class="position-absolute start-0 top-0 w-100 h-100 z-n1"
          alt=""
        />
        <div class="nft-promo-card__inner d-flex align-items-center">
          <div class="nft-promo-card__thumb w-100">
            <img
              src="@/assets/images/nft/nf-card-img.png"
              alt=""
              class="w-100 h-100 object-fit-cover"
            />
          </div>
          <div class="flex-grow-1">
            <h4 class="mb-16 text-white">Discover The Largest NFTs Marketplace</h4>
            <p class="text-white text-md">
              The largest NFT (Non-Fungible Token) marketplace is OpenSea. Established in 2017, OpenSea has grown to become the leading platform for buying, selling, and trading digital assets.
            </p>
            <div class="d-flex align-items-center flex-wrap mt-24 gap-16">
              <a
                href="#"
                class="btn rounded-pill border br-white text-white radius-8 px-32 py-11 hover-bg-white text-hover-neutral-900"
                >Explore</a
              >
              <a
                href="#"
                class="btn rounded-pill btn-primary-600 radius-8 px-28 py-11"
                >Create Now</a
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "NftPromoCard",
  };
  </script>