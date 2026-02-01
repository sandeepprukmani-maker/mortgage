<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="Portfolios" :breadcrumbs="[
            { name: 'Portfolios' }
        ]" />

        <PortfoliosData />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import PortfoliosData from '@/components/CryptoCurrency/Portfolios/index.vue'

export default {
    name: "Portfolios",
    components: {
        Breadcrumb,
        PortfoliosData
    },
}
</script>