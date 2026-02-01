<template>
      <!-- Loop through each blog item -->
      <div v-for="(blog, index) in blogs" :key="index" class="col-xxl-3 col-lg-4 col-sm-6">
        <div class="card h-100 p-0 radius-12 overflow-hidden">
          <div class="card-body p-0">
            <router-link to="/blog-details" class="w-100 max-h-266-px radius-0 overflow-hidden">
              <img :src="blog.image" :alt="`Blog image ${index + 1}`" class="w-100 h-100 object-fit-cover">
            </router-link>
            <div class="p-20">
              <h6 class="mb-16">
                <router-link to="/blog-details" class="text-line-2 text-hover-primary-600 text-xl transition-2">
                  {{ blog.title }}
                </router-link>
              </h6>
              <p class="text-line-3 text-neutral-500 mb-0">{{ blog.description }}</p>
              <span class="d-block border-bottom border-neutral-300 border-dashed my-20"></span>
              <div class="d-flex align-items-center justify-content-between flex-wrap gap-6">
                <div class="d-flex align-items-center gap-8">
                  <img :src="blog.user.image" alt="" class="w-40-px h-40-px rounded-circle object-fit-cover">
                  <div class="d-flex flex-column">
                    <h6 class="text-sm mb-0">{{ blog.user.name }}</h6>
                    <span class="text-xs text-neutral-500">{{ blog.user.timeAgo }}</span>
                  </div>
                </div>
                <router-link to="/blog-details" class="btn btn-sm btn-primary-600 d-flex align-items-center gap-1 text-xs px-8 py-6">
                  Read More
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
  </template>
  
  <script>
  import blog5 from "@/assets/images/blog/blog5.png"
  import blog6 from "@/assets/images/blog/blog6.png"
  import blog7 from "@/assets/images/blog/blog7.png"

  import userList1 from "@/assets/images/user-list/user-list1.png"
  import userList2 from "@/assets/images/user-list/user-list2.png"
  import userList3 from "@/assets/images/user-list/user-list3.png"
  import userList5 from "@/assets/images/user-list/user-list5.png"


  export default {
    data() {
      return {
        // Array of blog objects to loop over
        blogs: [
          {
            title: "How to hire a right business executive for your company",
            description: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.",
            image: blog5,
            user: {
              image: userList1,
              name: "John Doe",
              timeAgo: "1 day ago"
            }
          },
          {
            title: "The Gig Economy: Adapting to a Flexible Workforce",
            description: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.",
            image: blog6,
            user: {
              image: userList2,
              name: "Robiul Hasan",
              timeAgo: "1 day ago"
            }
          },
          {
            title: "The Future of Remote Work: Strategies for Success",
            description: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.",
            image: blog7,
            user: {
              image: userList3,
              name: "John Doe",
              timeAgo: "1 day ago"
            }
          },
          {
            title: "Lorem ipsum dolor sit amet consectetur adipisicing.",
            description: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.",
            image: blog6,
            user: {
              image: userList5,
              name: "John Doe",
              timeAgo: "1 day ago"
            }
          }
        ]
      };
    }
  };
  </script>