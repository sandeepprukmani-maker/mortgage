<template>
    <div class="col-lg-4">
        <div class="d-flex flex-column gap-24">
            <!-- Search -->
            <div class="card">
                <div class="card-header border-bottom">
                    <h6 class="text-xl mb-0">Search Here</h6>
                </div>
                <div class="card-body p-24">
                    <form class="position-relative" @submit.prevent>
                        <input type="text" class="form-control border border-neutral-200 radius-8 ps-40" name="search"
                            placeholder="Search" v-model="search" />
                        <iconify-icon icon="ion:search-outline"
                            class="icon position-absolute positioned-icon top-50 translate-middle-y"></iconify-icon>
                    </form>
                </div>
            </div>

            <!-- Latest Blog -->
            <div class="card">
                <div class="card-header border-bottom">
                    <h6 class="text-xl mb-0">Latest Posts</h6>
                </div>
                <div class="card-body d-flex flex-column gap-24 p-24">
                    <div v-for="(post, index) in latestPosts" :key="index" class="d-flex flex-wrap">
                        <router-link :to="post.link" class="blog__thumb w-100 radius-12 overflow-hidden">
                            <img :src="post.image" alt="" class="w-100 h-100 object-fit-cover" />
                        </router-link>
                        <div class="blog__content">
                            <h6 class="mb-8">
                                <router-link :to="post.link"
                                    class="text-line-2 text-hover-primary-600 text-md transition-2">
                                    {{ post.title }}
                                </router-link>
                            </h6>
                            <p class="text-line-2 text-sm text-neutral-500 mb-0">
                                {{ post.description }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Category -->
            <div class="card">
                <div class="card-header border-bottom">
                    <h6 class="text-xl mb-0">Tags</h6>
                </div>
                <div class="card-body p-24">
                    <ul>
                        <li v-for="(cat, index) in categories" :key="index"
                            class="w-100 d-flex align-items-center justify-content-between flex-wrap gap-8 border-bottom border-dashed pb-12 mb-12"
                            :class="{ 'mb-0 pb-0 border-bottom-0': index === categories.length - 1 }">
                            <a :href="cat.link" class="text-hover-primary-600 transition-2">
                                {{ cat.name }}
                            </a>
                            <span
                                class="text-neutral-500 w-28-px h-28-px rounded-circle bg-neutral-100 d-flex justify-content-center align-items-center transition-2 text-xs fw-semibold">
                                {{ cat.count }}
                            </span>
                        </li>
                    </ul>
                </div>
            </div>

            <!-- Tags -->
            <div class="card">
                <div class="card-header border-bottom">
                    <h6 class="text-xl mb-0">Tags</h6>
                </div>
                <div class="card-body p-24">
                    <div class="d-flex align-items-center flex-wrap gap-8">
                        <a v-for="(tag, index) in tags" :key="index" :href="tag.link"
                            class="btn btn-sm btn-primary-600 bg-primary-50 bg-hover-primary-600 text-primary-600 border-0 d-inline-flex align-items-center gap-1 text-sm px-16 py-6">
                            {{ tag.name }}
                        </a>
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
export default {
    name: "SidebarWidgets",
    data() {
        return {
            search: "",
            latestPosts: [
                {
                    title: "How to hire a right business executive for your company",
                    description:
                        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.",
                    image: blog5,
                    link: "blog-details",
                },
                {
                    title: "The Gig Economy: Adapting to a Flexible Workforce",
                    description:
                        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.",
                    image: blog6,
                    link: "blog-details",
                },
                {
                    title: "The Future of Remote Work: Strategies for Success",
                    description:
                        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.",
                    image: blog7,
                    link: "blog-details",
                },
                {
                    title: "Lorem ipsum dolor sit amet consectetur adipisicing.",
                    description:
                        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Omnis dolores explicabo corrupti, fuga necessitatibus fugiat adipisci quidem eveniet enim minus.",
                    image: blog6,
                    link: "blog-details",
                },
            ],
            categories: [
                { name: "Techbology", count: "01", link: "/blog" },
                { name: "Business", count: "01", link: "/blog" },
                { name: "Consulting", count: "01", link: "/blog" },
                { name: "Course", count: "01", link: "/blog" },
                { name: "Real Estate", count: "01", link: "/blog" },
            ],
            tags: [
                { name: "Development", link: "/blog" },
                { name: "Design", link: "/blog" },
                { name: "Technology", link: "/blog" },
                { name: "Popular", link: "/blog" },
                { name: "Codignator", link: "/blog" },
                { name: "Javascript", link: "/blog" },
                { name: "Bootstrap", link: "/blog" },
                { name: "PHP", link: "/blog" },
            ],
        };
    },
};
</script>