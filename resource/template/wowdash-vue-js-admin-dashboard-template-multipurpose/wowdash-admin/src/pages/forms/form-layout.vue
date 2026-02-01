<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Input Layout" :breadcrumbs="[
            { name: 'Input Layout' }
        ]" />

        <InputLayout />
    </div>

</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import InputLayout from '@/components/Forms/InputLayout.vue'

export default {
    name: "FormsLayout",
    components: {
        Breadcrumb,
        InputLayout,
    },
}
</script>