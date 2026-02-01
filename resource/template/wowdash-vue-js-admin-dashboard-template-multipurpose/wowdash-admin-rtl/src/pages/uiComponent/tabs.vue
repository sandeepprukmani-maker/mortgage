<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Tab & Accordion" :breadcrumbs="[
            { name: 'Components / Tab & Accordion' }
        ]" />

        <Tab />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import Tab from '@/components/UiComponent/Tab.vue'

export default {
    name: "Tab&Accordion",
    components: {
        Breadcrumb,
        Tab,
    },
}
</script>