<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Terms & Conditions" :breadcrumbs="[
            { name: 'Terms & Conditions' }
        ]" />

        <TermsCondition />
    </div>

</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import TermsCondition from '@/components/TermsCondition/Terms.vue'
export default {
    name: "Terms&Conditions",
    components: {
        Breadcrumb,
        TermsCondition,
    },
}
</script>