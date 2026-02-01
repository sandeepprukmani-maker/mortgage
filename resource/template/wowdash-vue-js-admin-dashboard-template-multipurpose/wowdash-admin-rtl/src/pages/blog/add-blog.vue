<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="Add Blog" :breadcrumbs="[
            { name: 'Add Blog' }
        ]" />

        <div class="row gy-4">
            <AddNewPost />
            <!-- Sidebar Start -->
            <LatestPost />
        </div>
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import AddNewPost from '@/components/Blog/AddBlog/AddNewPost.vue'
import LatestPost from '@/components/Blog/AddBlog/LatestPost.vue'
export default {
    name: "AddBlog",
    components: {
        Breadcrumb,
        AddNewPost,
        LatestPost
    },
}
</script>