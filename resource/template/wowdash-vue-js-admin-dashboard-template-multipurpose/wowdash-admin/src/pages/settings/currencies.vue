<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="Currencies" :breadcrumbs="[
            { name: 'Setting -  Currencies' }
        ]" />

        <Currencies />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import Currencies from '@/components/Settings/Currencies.vue'
export default {
    name: "CurrenciesData",
    components: {
        Breadcrumb,
        Currencies
    },
}
</script>