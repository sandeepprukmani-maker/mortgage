<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Video" :breadcrumbs="[
            { name: 'Components / Videos' }
        ]" />

        <Videos />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import Videos from '@/components/UiComponent/Videos.vue'

export default {
    name: "Video",
    components: {
        Breadcrumb,
        Videos,
    },
}
</script>