<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Input Form" :breadcrumbs="[
            { name: 'Input Form' }
        ]" />

        <InputFrom />
    </div>

</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import InputFrom from '@/components/Forms/Form.vue'

export default {
    name: "Forms",
    components: {
        Breadcrumb,
        InputFrom,
    },
}
</script>