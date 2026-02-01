<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="Blog Details" :breadcrumbs="[
            { name: 'Blog Details' }
        ]" />

        <div class="row gy-4">
            <div class="col-lg-8">
                <BlogOne />
                <Comments />
                <AddComment />
            </div>
            <!-- Sidebar Start -->
            <BlogSidebar />
        </div>
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import BlogOne from '@/components/Blog/BlogDetails/BlogOne.vue'
import Comments from '@/components/Blog/BlogDetails/Comments.vue'
import AddComment from '@/components/Blog/BlogDetails/AddComment.vue'
import BlogSidebar from '@/components/Blog/BlogDetails/BlogSidebar.vue'
export default {
    name: "BlogDetails",
    components: {
        Breadcrumb,
        BlogOne,
        Comments,
        AddComment,
        BlogSidebar
    },
}
</script>