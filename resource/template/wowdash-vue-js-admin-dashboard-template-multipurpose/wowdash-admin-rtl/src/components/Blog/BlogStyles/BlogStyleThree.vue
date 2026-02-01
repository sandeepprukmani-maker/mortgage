<template>
    <!-- Loop through each blog item -->
    <div v-for="(blog, index) in blogs" :key="index" class="col-xxl-3 col-lg-4 col-sm-6">
        <div class="card h-100 p-0 radius-12 overflow-hidden">
            <div class="card-body p-24">
                <h6 class="mb-16">
                    <router-link to="/blog-details" class="text-line-2 text-hover-primary-600 text-xl transition-2">
                        {{ blog.title }}
                    </router-link>
                </h6>
                <div class="d-flex align-items-center gap-6 justify-content-between flex-wrap mb-16">
                    <div class="d-flex align-items-center gap-8 text-neutral-500 fw-medium">
                        <i class="ri-chat-3-line"></i>
                        {{ blog.comments }} Comments
                    </div>
                    <div class="d-flex align-items-center gap-8 text-neutral-500 fw-medium">
                        <i class="ri-calendar-2-line"></i>
                        {{ blog.date }}
                    </div>
                </div>
                <router-link to="/blog-details" class="w-100 max-h-194-px radius-8 overflow-hidden">
                    <img :src="blog.image" :alt="`Blog image ${index + 1}`" class="w-100 h-100 object-fit-cover">
                </router-link>
                <div class="mt-20">
                    <p class="text-line-3 text-neutral-500">{{ blog.description }}</p>
                    <span class="d-block border-bottom border-neutral-300 border-dashed my-20"></span>
                    <div class="d-flex align-items-center justify-content-between flex-wrap gap-6">
                        <div class="d-flex align-items-center gap-8">
                            <img :src="blog.user.image" alt="" class="w-40-px h-40-px rounded-circle object-fit-cover">
                            <div class="d-flex flex-column">
                                <h6 class="text-sm mb-0">{{ blog.user.name }}</h6>
                                <span class="text-xs text-neutral-500">{{ blog.user.timeAgo }}</span>
                            </div>
                        </div>
                        <router-link to="/blog-details"
                            class="btn btn-sm btn-primary-600 d-flex align-items-center gap-1 text-xs px-8 py-6">
                            Read More
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import blog1 from "@/assets/images/blog/blog1.png"
import blog2 from "@/assets/images/blog/blog2.png"
import blog3 from "@/assets/images/blog/blog3.png"
import blog4 from "@/assets/images/blog/blog4.png"

import userList1 from "@/assets/images/user-list/user-list1.png"
export default {
    data() {
        return {
            // Array of blog objects to loop over
            blogs: [
                {
                    title: "Discover Endless Possibilities in Real Estate Live Your Best Life in a",
                    comments: 10,
                    date: "Jan 17, 2024",
                    image: blog1,
                    description: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.",
                    user: {
                        image: userList1,
                        name: "John Doe",
                        timeAgo: "1 day ago"
                    }
                },
                {
                    title: "Turn Your Real Estate Dreams Into Reality Embrace the Real Estate",
                    comments: 10,
                    date: "Jan 17, 2024",
                    image: blog2,
                    description: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.",
                    user: {
                        image: userList1,
                        name: "John Doe",
                        timeAgo: "1 day ago"
                    }
                },
                {
                    title: "Your satisfaction is our top the best priority",
                    comments: 10,
                    date: "Jan 17, 2024",
                    image: blog3,
                    description: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.",
                    user: {
                        image: userList1,
                        name: "John Doe",
                        timeAgo: "1 day ago"
                    }
                },
                {
                    title: "Your journey to home ownership starts here",
                    comments: 10,
                    date: "Jan 17, 2024",
                    image: blog4,
                    description: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.",
                    user: {
                        image: userList1,
                        name: "John Doe",
                        timeAgo: "1 day ago"
                    }
                }
            ]
        };
    }
};
</script>