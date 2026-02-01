<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="Marketplace Details" :breadcrumbs="[
            { name: 'Marketplace Details' }
        ]" />

        <div class="row gy-4">
            <MarketData />
            <MarketSidebar />
        </div>
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import MarketData from '@/components/CryptoCurrency/MarketplaceDetails/MarketData.vue'
import MarketSidebar from '@/components/CryptoCurrency/MarketplaceDetails/MarketSidebar.vue'

export default {
    name: "MarketplaceDetails",
    components: {
        Breadcrumb,
        MarketData,
        MarketSidebar
    },
}
</script>