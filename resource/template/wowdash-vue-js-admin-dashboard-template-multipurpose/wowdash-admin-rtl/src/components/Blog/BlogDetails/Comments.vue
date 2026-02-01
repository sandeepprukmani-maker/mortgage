<template>
    <div class="card mt-24">
      <div class="card-header border-bottom">
        <h6 class="text-xl mb-0">Comments</h6>
      </div>
      <div class="card-body p-24">
        <div class="comment-list d-flex flex-column">
          <div
            class="comment-list__item"
            v-for="(comment, index) in comments"
            :key="index"
            :class="comment.isReply ? 'ms--48' : ''"
          >
            <div class="d-flex align-items-start gap-16">
              <div class="flex-shrink-0">
                <img
                  :src="comment.avatar"
                  alt=""
                  class="w-60-px h-60-px rounded-circle object-fit-cover"
                />
              </div>
              <div
                class="flex-grow-1"
                :class="{
                  'border-bottom pb-40 mb-40 border-dashed': comment.hasBorder
                }"
              >
                <h6 class="text-lg mb-4">{{ comment.name }}</h6>
                <span class="text-neutral-500 text-sm">{{ comment.date }}</span>
                <p class="text-neutral-600 text-md my-16">
                  {{ comment.text }}
                </p>
                <div class="d-flex align-items-center gap-8">
                  <a
                    href="javascript:void(0)"
                    class="btn btn-sm btn-danger-600 d-flex align-items-center gap-1 text-xxs px-8 py-6"
                  >
                    <i class="ri-heart-3-line text-xs line-height-1"></i>
                    Like
                  </a>
                  <a
                    href="#comment-form"
                    class="btn btn-sm btn-primary-600 d-flex align-items-center gap-1 text-xxs px-8 py-6"
                  >
                    <i class="ri-reply-line text-xs line-height-1"></i>
                    Reply
                  </a>
                </div>
              </div>
            </div>
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
  import userImg6 from "@/assets/images/user-list/user-list6.png"
  export default {
    name: "CommentSection",
    data() {
      return {
        comments: [
          {
            name: "Jenny Wilson",
            avatar: userImg1,
            date: "Jan 21, 2024 at 11:25 pm",
            text:
              "Lorem ipsum dolor sit amet consectetur. Nec nunc pellentesque massa pretium. Quam sapien nec venenatis vivamus sed cras faucibus mi viverra. Quam faucibus morbi cras vitae neque. Necnunc pellentesque massa pretium.",
            isReply: false,
            hasBorder: true
          },
          {
            name: "Robiul Hasan",
            avatar: userImg2,
            date: "Jan 21, 2024 at 11:25 pm",
            text:
              "Lorem ipsum dolor sit amet consectetur. Nec nunc pellentesque massa pretium. Quam sapien nec venenatis vivamus sed cras faucibus mi viverra. Quam faucibus morbi cras vitae neque. Necnunc pellentesque massa pretium.",
            isReply: true,
            hasBorder: true
          },
          {
            name: "John Doe",
            avatar: userImg3,
            date: "Jan 21, 2024 at 11:25 pm",
            text:
              "Lorem ipsum dolor sit amet consectetur. Nec nunc pellentesque massa pretium. Quam sapien nec venenatis vivamus sed cras faucibus mi viverra. Quam faucibus morbi cras vitae neque. Necnunc pellentesque massa pretium.",
            isReply: true,
            hasBorder: true
          },
          {
            name: "Mariam Akter",
            avatar: userImg4,
            date: "Jan 21, 2024 at 11:25 pm",
            text:
              "Lorem ipsum dolor sit amet consectetur. Nec nunc pellentesque massa pretium. Quam sapien nec venenatis vivamus sed cras faucibus mi viverra. Quam faucibus morbi cras vitae neque. Necnunc pellentesque massa pretium.",
            isReply: false,
            hasBorder: true
          },
          {
            name: "Dainel Defoe",
            avatar: userImg6,
            date: "Jan 21, 2024 at 11:25 pm",
            text:
              "Lorem ipsum dolor sit amet consectetur. Nec nunc pellentesque massa pretium. Quam sapien nec venenatis vivamus sed cras faucibus mi viverra. Quam faucibus morbi cras vitae neque. Necnunc pellentesque massa pretium.",
            isReply: true,
            hasBorder: false
          }
        ]
      };
    }
  };
  </script>
  