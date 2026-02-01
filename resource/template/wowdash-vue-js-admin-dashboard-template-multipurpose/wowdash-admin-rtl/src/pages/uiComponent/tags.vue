<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Tags" :breadcrumbs="[
            { name: 'Components / Tags' }
        ]" />
        <Tags />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import Tags from '@/components/UiComponent/Tags.vue'

export default {
    name: "Tag",
    components: {
        Breadcrumb,
        Tags,
    },
}
</script>