<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="Gallery Grid" :breadcrumbs="[
            { name: 'Gallery Grid' }
        ]" />

        <Gallerymasonry />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import Gallerymasonry from '@/components/Gallery/GalleryMasonry.vue'
export default {
    name: "GalleryMasonry",
    components: {
        Breadcrumb,
        Gallerymasonry,
    },
}
</script>