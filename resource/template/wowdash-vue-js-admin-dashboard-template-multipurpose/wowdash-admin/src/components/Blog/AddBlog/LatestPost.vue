<template>
    <div class="col-lg-4">
        <div class="d-flex flex-column gap-24">
            <!-- Latest Blog -->
            <div class="card">
                <div class="card-header border-bottom">
                    <h6 class="text-xl mb-0">Latest Posts</h6>
                </div>
                <div class="card-body d-flex flex-column gap-24 p-24">
                    <div v-for="(post, index) in posts" :key="index" class="d-flex flex-wrap">
                        <router-link to="/blog-details" class="blog__thumb w-100 radius-12 overflow-hidden">
                            <img :src="post.image" :alt="post.title" class="w-100 h-100 object-fit-cover">
                        </router-link>
                        <div class="blog__content">
                            <h6 class="mb-8">
                                <router-link to="/blog-details" class="text-line-2 text-hover-primary-600 text-md transition-2">{{
                                    post.title }}</router-link>
                            </h6>
                            <p class="text-line-2 text-sm text-neutral-500 mb-0">{{ post.description }}</p>
                        </div>
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
import blog5 from "@/assets/images/blog/blog5.png"
import blog6 from "@/assets/images/blog/blog6.png"
import blog7 from "@/assets/images/blog/blog7.png"
export default {
    data() {
        return {
            posts: [
                {
                    title: 'How to hire a right business executive for your company',
                    description: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.',
                    image: blog1,
                },
                {
                    title: 'The Gig Economy: Adapting to a Flexible Workforce',
                    description: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.',
                    image: blog2,
                },
                {
                    title: 'The Future of Remote Work: Strategies for Success',
                    description: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.',
                    image: blog3,
                },
                {
                    title: 'Lorem ipsum dolor sit amet consectetur adipisicing.',
                    description: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.',
                    image: blog4,
                },
                {
                    title: 'How to hire a right business executive for your company',
                    description: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.',
                    image: blog5,
                },
                {
                    title: 'The Gig Economy: Adapting to a Flexible Workforce',
                    description: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.',
                    image: blog6,
                },
                {
                    title: 'The Future of Remote Work: Strategies for Success',
                    description: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.',
                    image: blog7,
                }
            ]
        };
    }
};
</script>

<style scoped>
/* You can add custom styles here */
</style>