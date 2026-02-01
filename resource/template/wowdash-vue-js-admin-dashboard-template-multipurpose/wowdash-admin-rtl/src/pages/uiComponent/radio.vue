<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Radio" :breadcrumbs="[
            { name: 'Components / Radio' }
        ]" />

        <RadioData />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import RadioData from '@/components/UiComponent/Radio.vue'

export default {
    name: "Radio",
    components: {
        Breadcrumb,
        RadioData,
    },
}
</script>