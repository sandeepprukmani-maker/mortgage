<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Tooltip & Popover" :breadcrumbs="[
            { name: 'Components / Tooltip & Popover' }
        ]" />
        <TooltipData />

    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import TooltipData from '@/components/UiComponent/Tooltip.vue'

export default {
    name: "Badges",
    components: {
        Breadcrumb,
        TooltipData,
    },
}
</script>