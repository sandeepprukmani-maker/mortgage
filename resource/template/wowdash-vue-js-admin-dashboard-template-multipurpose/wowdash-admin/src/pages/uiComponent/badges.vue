<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Badges" :breadcrumbs="[
            { name: 'Components / Badges' }
        ]" />

        <BadgesData />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import BadgesData from '@/components/UiComponent/Badges.vue'

export default {
    name: "Badges",
    components: {
        Breadcrumb,
        BadgesData,
    },
}
</script>