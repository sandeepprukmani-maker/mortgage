<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Switch" :breadcrumbs="[
            { name: 'Components / Switch' }
        ]" />

        <SwitchData />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import SwitchData from '@/components/UiComponent/Switch.vue'

export default {
    name: "Radio",
    components: {
        Breadcrumb,
        SwitchData,
    },
}
</script>