<template>
    <div class="col-12">
      <div class="mb-16 mt-8 d-flex flex-wrap justify-content-between gap-16">
        <h6 class="mb-0">Trending NFTs</h6>
        <ul class="nav button-tab nav-pills mb-16 gap-12" id="pills-tab-three" role="tablist">
          <li class="nav-item" role="presentation" v-for="tab in tabs" :key="tab.id">
            <button
              class="nav-link fw-semibold text-secondary-light rounded-pill px-20 py-6 border border-neutral-300"
              :class="{ active: activeTab === tab.target }"
              :id="tab.id"
              data-bs-toggle="pill"
              :data-bs-target="`#${tab.target}`"
              type="button"
              role="tab"
              :aria-controls="tab.target"
              :aria-selected="activeTab === tab.target"
              @click="activeTab = tab.target"
            >
              {{ tab.name }}
            </button>
          </li>
        </ul>
      </div>
  
      <div class="tab-content" id="pills-tab-threeContent">
        <div
          v-for="tab in tabs"
          :key="tab.target"
          class="tab-pane fade"
          :class="{ 'show active': activeTab === tab.target }"
          :id="tab.target"
          role="tabpanel"
          :aria-labelledby="tab.id"
        >
          <div class="row g-3">
            <div
              v-for="(nft, index) in getNfts(tab.target)"
              :key="index"
              class="col-xxl-3 col-sm-6 col-xs-6"
            >
              <div class="nft-card bg-base radius-16 overflow-hidden">
                <div class="radius-16 overflow-hidden">
                  <img :src="nft.image" alt="" class="w-100 h-100 object-fit-cover" />
                </div>
                <div class="p-10">
                  <h6 class="text-md fw-bold text-primary-light">{{ nft.title }}</h6>
                  <div class="d-flex align-items-center gap-8">
                    <img
                      :src="nft.userImage"
                      class="w-28-px h-28-px rounded-circle object-fit-cover"
                      alt=""
                    />
                    <span class="text-sm text-secondary-light fw-medium">{{ nft.userName }}</span>
                  </div>
                  <div class="mt-10 d-flex align-items-center justify-content-between gap-8 flex-wrap">
                    <span class="text-sm text-secondary-light fw-medium">
                      Price:
                      <span class="text-sm text-primary-light fw-semibold">{{ nft.price }} ETH</span>
                    </span>
                    <span class="text-sm fw-semibold text-primary-600">{{ nft.usd }}</span>
                  </div>
                  <div class="d-flex align-items-center flex-wrap mt-12 gap-8">
                    <a
                      href="#"
                      class="btn rounded-pill border text-neutral-500 border-neutral-500 radius-8 px-12 py-6 bg-hover-neutral-500 text-hover-white flex-grow-1"
                    >History</a>
                    <a
                      href="#"
                      class="btn rounded-pill btn-primary-600 radius-8 px-12 py-6 flex-grow-1"
                    >Buy Now</a>
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
  import nft_img1 from '@/assets/images/nft/nft-img1.png'
  import nft_img2 from '@/assets/images/nft/nft-img2.png'
  import nft_img3 from '@/assets/images/nft/nft-img3.png'
  import nft_img4 from '@/assets/images/nft/nft-img4.png'

  import nft_user1 from '@/assets/images/nft/nft-user-img1.png'
  import nft_user2 from '@/assets/images/nft/nft-user-img2.png'
  import nft_user3 from '@/assets/images/nft/nft-user-img3.png'
  import nft_user4 from '@/assets/images/nft/nft-user-img4.png'

  export default {
    data() {
      return {
        activeTab: 'pills-button-all',
        tabs: [
          { id: 'pills-button-all-tab', name: 'All', target: 'pills-button-all' },
          { id: 'pills-button-art-tab', name: 'Art', target: 'pills-button-art' },
          { id: 'pills-button-music-tab', name: 'Music', target: 'pills-button-music' },
          { id: 'pills-button-utility-tab', name: 'Utility', target: 'pills-button-utility' },
          { id: 'pills-button-fashion-tab', name: 'Fashion', target: 'pills-button-fashion' }
        ],
        nftData: {
          'pills-button-all': [
            { title: 'Fantastic Alien',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img1,
              userImage: nft_user1
            },
            {
              title: 'New Figures',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img2,
              userImage: nft_user2
            },
            {
              title: 'New Figures',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img3,
              userImage: nft_user3
            },
            {
              title: 'New Figures',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img4,
              userImage: nft_user4
            }
          ],
          'pills-button-art': [
            { title: 'Fantastic Alien',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img1,
              userImage: nft_user1
            },
            {
              title: 'New Figures',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img2,
              userImage: nft_user2
            },
            {
              title: 'New Figures',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img3,
              userImage: nft_user3
            },
            {
              title: 'New Figures',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img4,
              userImage: nft_user4
            }
          ],
          'pills-button-music': [
            { title: 'Fantastic Alien',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img1,
              userImage: nft_user1
            },
            {
              title: 'New Figures',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img2,
              userImage: nft_user2
            },
            {
              title: 'New Figures',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img3,
              userImage: nft_user3
            },
            {
              title: 'New Figures',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img4,
              userImage: nft_user4
            }
          ],
          'pills-button-utility': [
            { title: 'Fantastic Alien',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img1,
              userImage: nft_user1
            },
            {
              title: 'New Figures',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img2,
              userImage: nft_user2
            },
            {
              title: 'New Figures',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img3,
              userImage: nft_user3
            },
            {
              title: 'New Figures',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img4,
              userImage: nft_user4
            }
          ],
          'pills-button-fashion': [
            { title: 'Fantastic Alien',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img1,
              userImage: nft_user1
            },
            {
              title: 'New Figures',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img2,
              userImage: nft_user2
            },
            {
              title: 'New Figures',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img3,
              userImage: nft_user3
            },
            {
              title: 'New Figures',
              userName: 'Watson Kristin',
              price: '1.44',
              usd: '$4,224.96',
              image: nft_img4,
              userImage: nft_user4
            }
          ]
        }
      };
    },
    methods: {
      getNfts(tabId) {
        return this.nftData[tabId] || [];
      }
    }
  };
  </script>
  