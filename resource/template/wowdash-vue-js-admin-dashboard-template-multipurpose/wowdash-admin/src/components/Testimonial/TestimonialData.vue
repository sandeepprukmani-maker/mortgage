<template>
    <div class="row gy-4">
      <div
        v-for="(user, index) in users"
        :key="index"
        class="col-xxl-4 col-md-6"
      >
        <div class="card rounded-3 overflow-hidden h-100">
          <div class="card-body p-24">
            <div class="d-flex align-items-start justify-content-between gap-2">
              <div class="d-flex align-items-center gap-12 flex-wrap">
                <div class="w-56-px h-56-px overflow-hidden flex-shrink-0">
                  <img :src="user.image" alt="" class="w-100 h-100 object-fit-cover rounded-circle" />
                </div>
                <div class="d-flex flex-column flex-grow-1">
                  <h6 class="text-xl mb-0">{{ user.name }}</h6>
                  <span class="text-neutral-500">{{ user.title }}</span>
                </div>
              </div>
              <ul class="d-flex align-items-center justify-content-end gap-1">
                <li
                  v-for="i in 5"
                  :key="i"
                  :class="[
                    'text-xl d-flex line-height-1',
                    i <= user.rating ? 'text-warning-600' : 'text-neutral-300'
                  ]"
                >
                  <i class="ri-star-fill"></i>
                </li>
              </ul>
            </div>
            <p class="mt-24 text-neutral-500 text-lg mb-0">{{ user.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import userImg1 from "@/assets/images/user-list/user-list1.png"
  import userImg2 from "@/assets/images/user-list/user-list2.png"
  import userImg3 from "@/assets/images/user-list/user-list3.png"
  import userImg4 from "@/assets/images/user-list/user-list4.png"
  import userImg5 from "@/assets/images/user-list/user-list5.png"
  import userImg7 from "@/assets/images/user-list/user-list7.png"
  import userImg8 from "@/assets/images/user-list/user-list8.png"
  import userImg9 from "@/assets/images/user-list/user-list9.png"
  import userImg10 from "@/assets/images/user-list/user-list10.png"
  export default {
    name: 'UserList',
    data() {
      return {
        users: [
          {
            name: 'Robert Fox',
            title: 'Prime Investments',
            rating: 5,
            image: userImg1,
            description:
              'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Magni ea, voluptatem adipisci dignissimos pariatur, nulla, amet quas laborum sit sint laudantium fuga. Vitae hic, facilis asperiores reiciendis quis qui reprehenderit.',
          },
          {
            name: 'Robiul Hasan',
            title: 'Front End Developer',
            rating: 4,
            image: userImg2,
            description:
              'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Magni ea, voluptatem adipisci dignissimos pariatur, nulla, amet quas laborum sit sint laudantium fuga. Vitae hic, facilis asperiores reiciendis quis qui reprehenderit.',
          },
          {
            name: 'John Doe',
            title: 'Designer',
            rating: 3,
            image: userImg3,
            description:
              'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Magni ea, voluptatem adipisci dignissimos pariatur, nulla, amet quas laborum sit sint laudantium fuga. Vitae hic, facilis asperiores reiciendis quis qui reprehenderit.',
          },
          {
            name: 'Annette Black',
            title: 'UX/UI Designer',
            rating: 3,
            image: userImg4,
            description:
              'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Magni ea, voluptatem adipisci dignissimos pariatur, nulla, amet quas laborum sit sint laudantium fuga. Vitae hic, facilis asperiores reiciendis quis qui reprehenderit.',
          },
          {
            name: 'Kathryn Murphy',
            title: 'Business Man',
            rating: 5,
            image: userImg5,
            description:
              'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Magni ea, voluptatem adipisci dignissimos pariatur, nulla, amet quas laborum sit sint laudantium fuga. Vitae hic, facilis asperiores reiciendis quis qui reprehenderit.',
          },
          {
            name: 'Ronald Richards',
            title: 'Back End Developer',
            rating: 4,
            image: userImg7,
            description:
              'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Magni ea, voluptatem adipisci dignissimos pariatur, nulla, amet quas laborum sit sint laudantium fuga. Vitae hic, facilis asperiores reiciendis quis qui reprehenderit.',
          },
          {
            name: 'Eleanor Pena',
            title: 'Business Consultant',
            rating: 5,
            image: userImg8,
            description:
              'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Magni ea, voluptatem adipisci dignissimos pariatur, nulla, amet quas laborum sit sint laudantium fuga. Vitae hic, facilis asperiores reiciendis quis qui reprehenderit.',
          },
          {
            name: 'Leslie Alexander',
            title: 'Doctor',
            rating: 2,
            image: userImg9,
            description:
              'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Magni ea, voluptatem adipisci dignissimos pariatur, nulla, amet quas laborum sit sint laudantium fuga. Vitae hic, facilis asperiores reiciendis quis qui reprehenderit.',
          },
          {
            name: 'Eleanor Pena',
            title: 'Back End Developer',
            rating: 3,
            image: userImg10,
            description:
              'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Magni ea, voluptatem adipisci dignissimos pariatur, nulla, amet quas laborum sit sint laudantium fuga. Vitae hic, facilis asperiores reiciendis quis qui reprehenderit.',
          },
        ],
      };
    },
  };
  </script>
  