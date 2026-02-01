<template>
    <div class="card p-0 radius-12 overflow-hidden">
      <div class="card-body p-0">
        <img :src="blogData.image" alt="" class="w-100 h-100 object-fit-cover" />
        <div class="p-32">
          <div class="d-flex align-items-center gap-16 justify-content-between flex-wrap mb-24">
            <div class="d-flex align-items-center gap-8">
              <img :src="blogData.author.avatar" alt="" class="w-48-px h-48-px rounded-circle object-fit-cover" />
              <div class="d-flex flex-column">
                <h6 class="text-lg mb-0">{{ blogData.author.name }}</h6>
                <span class="text-sm text-neutral-500">{{ blogData.author.postedAgo }}</span>
              </div>
            </div>
            <div class="d-flex align-items-center gap-md-3 gap-2 flex-wrap">
              <div class="d-flex align-items-center gap-8 text-neutral-500 text-lg fw-medium">
                <i class="ri-chat-3-line"></i>
                {{ blogData.meta.comments }} Comments
              </div>
              <div class="d-flex align-items-center gap-8 text-neutral-500 text-lg fw-medium">
                <i class="ri-calendar-2-line"></i>
                {{ blogData.meta.date }}
              </div>
            </div>
          </div>
          <h3 class="mb-16">{{ blogData.title }}</h3>
          <p
            v-for="(para, index) in blogData.content"
            :key="index"
            class="text-neutral-500 mb-16"
          >
            {{ para }}
          </p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import blogImg from "@/assets/images/blog/blog-details.png"
  import userImg from "@/assets/images/user-list/user-list1.png"
  export default {
    name: "BlogDetailsCard",
    data() {
      return {
        blogData: {
          image: blogImg,
          author: {
            name: "John Doe",
            avatar: userImg,
            postedAgo: "1 day ago"
          },
          meta: {
            comments: 10,
            date: "Jan 17, 2024"
          },
          title: "How to hire a right business executive for your company",
          content: [
            "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sequi voluptate quaerat possimus neque animi ex placeat ducimus reiciendis saepe mollitia tenetur aspernatur unde illum fugiat",
            "reprehenderit repellendus dicta accusantium laborum eum et inventore. Perferendis temporibus reiciendis ut magni numquam molestiae fugit, laboriosam adipisci modi, quisquam, rem aspernatur fugiat neque velit ratione? Ipsum maxime aperiam minus dolorem voluptatibus suscipit debitis delectus numquam.",
            "reprehenderit repellendus dicta accusantium laborum eum et inventore. Perferendis temporibus reiciendis ut magni numquam molestiae fugit, laboriosam adipisci modi, quisquam, rem aspernatur fugiat neque velit ratione? Ipsum maxime aperiam minus dolorem voluptatibus suscipit debitis delectus numquam. Illum delectus dicta sit soluta dolores odit facilis exercitationem animi quibusdam, autem nulla omnis harum magnam est ad aperiam quasi qui? Enim, natus porro debitis maiores ad soluta totam nesciunt deleniti tempora ipsum id consectetur? Alias dignissimos vel corrupti!"
          ]
        }
      };
    }
  };
  </script>
  