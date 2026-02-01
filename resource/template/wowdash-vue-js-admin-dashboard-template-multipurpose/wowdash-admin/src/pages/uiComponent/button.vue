<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Button" :breadcrumbs="[
            { name: 'Components / Button' }
        ]" />

        <ButtonData />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ButtonData from '@/components/UiComponent/Button.vue'

export default {
    name: "Button",
    components: {
        Breadcrumb,
        ButtonData,
    },
}
</script>