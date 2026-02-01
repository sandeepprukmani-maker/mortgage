<template>
    <!-- Loop through each blog item -->
    <div v-for="(blog, index) in blogs" :key="index" class="col-xxl-3 col-lg-4 col-sm-6">
        <div class="card h-100 p-0 radius-12 overflow-hidden">
            <div class="card-body p-24">
                <router-link to="/blog-details" class="w-100 max-h-194-px radius-8 overflow-hidden">
                    <img :src="blog.image" :alt="`Blog image ${index + 1}`" class="w-100 h-100 object-fit-cover" />
                </router-link>
                <div class="mt-20">
                    <div class="d-flex align-items-center gap-6 justify-content-between flex-wrap mb-16">
                        <a href="blog-details"
                            class="px-20 py-6 bg-neutral-100 rounded-pill bg-hover-neutral-300 text-neutral-600 fw-medium">{{
                            blog.category }}</a>
                        <div class="d-flex align-items-center gap-8 text-neutral-500 fw-medium">
                            <i class="ri-calendar-2-line"></i>
                            {{ blog.date }}
                        </div>
                    </div>
                    <h6 class="mb-16">
                        <router-link to="/blog-details" class="text-line-2 text-hover-primary-600 text-xl transition-2">
                            {{ blog.title }}
                        </router-link>
                    </h6>
                    <p class="text-line-3 text-neutral-500">{{ blog.description }}</p>
                    <router-link to="/blog-details"
                        class="d-flex align-items-center gap-8 fw-semibold text-neutral-900 text-hover-primary-600 transition-2">
                        Read More
                        <i class="ri-arrow-right-double-line text-xl d-flex line-height-1"></i>
                    </router-link>
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
export default {
    data() {
        return {
            blogs: [
                {
                    category: "Workshop",
                    date: "Jan 17, 2024",
                    title: "Discover Endless Possibilities in Real Estate Live Your Best Life in a",
                    description: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.",
                    image: blog1,
                },
                {
                    category: "Hiring",
                    date: "Jan 17, 2024",
                    title: "Turn Your Real Estate Dreams Into Reality Embrace the Real Estate",
                    description: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.",
                    image: blog2,
                },
                {
                    category: "Workshop",
                    date: "Jan 17, 2024",
                    title: "Your satisfaction is our top the best priority",
                    description: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.",
                    image: blog3,
                },
                {
                    category: "Workshop",
                    date: "Jan 17, 2024",
                    title: "Your journey to home ownership starts here",
                    description: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.",
                    image: blog4,
                }
            ]
        };
    }
};
</script>