<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="Wallet" :breadcrumbs="[
            { name: 'Wallet' }
        ]" />

        <div class="row gy-4">
            <WalletData />
            <WalletList />
        </div>
    </div>

</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import WalletData from '@/components/CryptoCurrency/Wallet/WalletData.vue'
import WalletList from '@/components/CryptoCurrency/Wallet/WalletList.vue'

export default {
    name: "Wallet",
    components: {
        Breadcrumb,
        WalletData,
        WalletList
    },
}
</script>