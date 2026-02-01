<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Form Validation" :breadcrumbs="[
            { name: 'Form Validation' }
        ]" />

        <FormValidationData />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import FormValidationData from '@/components/Forms/FormValidation.vue'

export default {
    name: "FormValidation",
    components: {
        Breadcrumb,
        FormValidationData,
    },
}
</script>