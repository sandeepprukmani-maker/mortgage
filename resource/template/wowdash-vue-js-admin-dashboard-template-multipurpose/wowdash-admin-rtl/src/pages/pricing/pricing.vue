<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="Pricing" :breadcrumbs="[
            { name: 'Pricing' }
        ]" />

        <PricingPlanMultipleColor />
        <SimplePricingPlan />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import PricingPlanMultipleColor from '@/components/Pricing/PricingMultipleColor.vue'
import SimplePricingPlan from '@/components/Pricing/SimplePricingPlan.vue'
export default {
    name: "Pricing",
    components: {
        Breadcrumb,
        PricingPlanMultipleColor,
        SimplePricingPlan,
    },
}
</script>