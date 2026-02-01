<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="Marketplace" :breadcrumbs="[
            { name: 'Marketplace' }
        ]" />
        <MarketplaceData />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import MarketplaceData from '@/components/CryptoCurrency/Marketplace/MarketplaceData.vue'

export default {
    name: "Marketplace",
    components: {
        Breadcrumb,
        MarketplaceData,
    },
}
</script>