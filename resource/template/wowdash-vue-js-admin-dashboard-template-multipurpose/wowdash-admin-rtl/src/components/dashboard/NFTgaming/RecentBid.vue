<template>
    <div class="col-12">
      <div class="card h-100">
        <div class="card-body p-24">
          <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between mb-20">
            <h6 class="mb-2 fw-bold text-lg mb-0">Recent Bid</h6>
            <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8 rounded-pill">
              <option>All Items</option>
              <option>New Item</option>
              <option>Trending Item</option>
              <option>Old Item</option>
            </select>
          </div>
          <div class="table-responsive scroll-sm">
            <table class="table bordered-table sm-table mb-0">
              <thead>
                <tr>
                  <th scope="col">Items</th>
                  <th scope="col">Price</th>
                  <th scope="col">Your Offer</th>
                  <th scope="col">Recent Offer</th>
                  <th scope="col">Time Left</th>
                  <th scope="col" class="text-center">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in bids" :key="index">
                  <td>
                    <div class="d-flex align-items-center">
                      <img :src="item.image" alt="" class="flex-shrink-0 me-12 w-40-px h-40-px rounded-circle me-12">
                      <div class="flex-grow-1">
                        <h6 class="text-md mb-0 fw-semibold">{{ item.title }}</h6>
                        <span class="text-sm text-secondary-light fw-normal">Owned by {{ item.owner }}</span>
                      </div>
                    </div>
                  </td>
                  <td>{{ item.price }}</td>
                  <td>{{ item.yourOffer }}</td>
                  <td>
                    <div class="d-flex align-items-center">
                      <img :src="item.offerImage" alt="" class="flex-shrink-0 me-12 w-40-px h-40-px rounded-circle me-12">
                      <div class="flex-grow-1">
                        <h6 class="text-md mb-0 fw-semibold text-primary-light">{{ item.recentOffer }}</h6>
                      </div>
                    </div>
                  </td>
                  <td>{{ item.timeLeft }}</td>
                  <td>
                    <div class="d-inline-flex align-items-center gap-12">
                      <button type="button" class="text-xl text-success-600"><i class="ri-edit-line"></i></button>
                      <button
                        type="button"
                        class="text-xl text-danger-600 remove-btn"
                        @click="deleteBid(index)"
                      >
                        <i class="ri-delete-bin-6-line"></i>
                      </button>
                    </div>
                  </td>
                </tr>
                <tr v-if="bids.length === 0">
                  <td colspan="6" class="text-center">No items found.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import item1 from '@/assets/images/nft/nft-items-img1.png'
  import item2 from '@/assets/images/nft/nft-items-img2.png'
  import item3 from '@/assets/images/nft/nft-items-img3.png'
  import item4 from '@/assets/images/nft/nft-items-img4.png'
  import item5 from '@/assets/images/nft/nft-items-img5.png'
  import item6 from '@/assets/images/nft/nft-items-img6.png'

  import offer1 from '@/assets/images/nft/nft-offer-img1.png'
  import offer2 from '@/assets/images/nft/nft-offer-img2.png'
  import offer3 from '@/assets/images/nft/nft-offer-img3.png'
  import offer4 from '@/assets/images/nft/nft-offer-img4.png'
  import offer5 from '@/assets/images/nft/nft-offer-img5.png'
  import offer6 from '@/assets/images/nft/nft-offer-img6.png'
  import offer7 from '@/assets/images/nft/nft-offer-img7.png'


  export default {
    name: 'RecentBidTable',
    data() {
      return {
        bids: [
        {
          title: 'Spanky & Friends',
          owner: 'ABC',
          image: item1,
          offerImage: offer1,
          price: '1.44 ETH',
          yourOffer: '3.053 ETH',
          recentOffer: '1.44.00 ETH',
          timeLeft: '2h 5m 40s'
        },
        {
          title: 'Nike Air Shoe',
          owner: 'ABC',
          image: item2,
          offerImage: offer2,
          price: '1.44 ETH',
          yourOffer: '3.053 ETH',
          recentOffer: '1.44.00 ETH',
          timeLeft: '2h 5m 40s'
        },
        {
          title: 'Woman Dresses',
          owner: 'ABC',
          image: item3,
          offerImage: offer3,
          price: '1.44 ETH',
          yourOffer: '3.053 ETH',
          recentOffer: '1.44.00 ETH',
          timeLeft: '2h 5m 40s'
        },
        {
          title: 'Smart Watch',
          owner: 'ABC',
          image: item4,
          offerImage: offer4,
          price: '1.44 ETH',
          yourOffer: '3.053 ETH',
          recentOffer: '1.44.00 ETH',
          timeLeft: '2h 5m 40s'
        },
        {
          title: 'Hoodie Rose',
          owner: 'ABC',
          image: item5,
          offerImage: offer5,
          price: '1.44 ETH',
          yourOffer: '3.053 ETH',
          recentOffer: '1.44.00 ETH',
          timeLeft: '2h 5m 40s'
        },
        {
          title: 'Hoodie Rose',
          owner: 'ABC',
          image: item6,
          offerImage: offer6,
          price: '1.44 ETH',
          yourOffer: '3.053 ETH',
          recentOffer: '1.44.00 ETH',
          timeLeft: '2h 5m 40s'
        },
        {
          title: 'Hoodie Rose',
          owner: 'ABC',
          image: item2,
          offerImage: offer7,
          price: '1.44 ETH',
          yourOffer: '3.053 ETH',
          recentOffer: '1.44.00 ETH',
          timeLeft: '2h 5m 40s'
        }
        ]
      };
    },
    methods: {
      deleteBid(index) {
        this.bids.splice(index, 1);
      }
    }
  };
  </script>
  