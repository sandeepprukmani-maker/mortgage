<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Colors" :breadcrumbs="[
            { name: 'Components / Colors' }
        ]" />

        <ColorData />

    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ColorData from '@/components/UiComponent/Colors.vue'

export default {
    name: "Colors",
    components: {
        Breadcrumb,
        ColorData,
    },
}
</script>
