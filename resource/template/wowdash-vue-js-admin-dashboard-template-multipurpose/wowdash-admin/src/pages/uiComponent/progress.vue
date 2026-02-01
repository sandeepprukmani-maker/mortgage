<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Progress Bar" :breadcrumbs="[
            { name: 'Components / Progress Bar' }
        ]" />

        <ProgressBarData />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ProgressBarData from '@/components/UiComponent/ProgressBar.vue'

export default {
    name: "ProgressBar",
    components: {
        Breadcrumb,
        ProgressBarData,
    },
}
</script>