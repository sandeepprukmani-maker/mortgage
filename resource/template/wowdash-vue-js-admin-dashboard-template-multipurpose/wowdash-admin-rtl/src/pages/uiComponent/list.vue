<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="List" :breadcrumbs="[
            { name: 'Components / List' }
        ]" />

        <List />

    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import List from '@/components/UiComponent/List.vue'

export default {
    name: "Lists",
    components: {
        Breadcrumb,
        List,
    },
}
</script>