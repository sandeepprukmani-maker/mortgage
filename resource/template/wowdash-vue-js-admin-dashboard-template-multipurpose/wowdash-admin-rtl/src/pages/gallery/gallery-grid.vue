<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="Gallery Grid" :breadcrumbs="[
            { name: 'Gallery Grid' }
        ]" />

        <Gallerygrid />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import Gallerygrid from '@/components/Gallery/GalleryGrid.vue'
export default {
    name: "GalleryGrid",
    components: {
        Breadcrumb,
        Gallerygrid,
    },
}
</script>