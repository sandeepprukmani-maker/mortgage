<template>
        <div class="dashboard-main-body">


            <Breadcrumb title="Dashboard" :breadcrumbs="[
                { name: 'Crypto Currency' }
            ]" />

            <!-- Crypto Home Widgets Start -->
            <CryptoWidgets />
            <!-- Crypto Home Widgets End -->

            <div class="row gy-4 mt-4">

                <!-- Crypto Home Widgets Start -->
                <div class="col-xxl-8">
                    <div class="row gy-4">
                        <CoinAnalyticsChart />
                        <CoinAnalytics />
                        <MyOrders />
                        <RecentTransaction />
                    </div>
                </div>
                <!-- Crypto Home Widgets End -->

                <div class="col-xxl-4">
                    <div class="row gy-4">
                        <MyCards />
                        <TotalBalance/>
                        <UserActivates/>
                    </div>
                </div>
            </div>
        </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ApexCharts from "vue3-apexcharts";
import { Icon } from "@iconify/vue"; 
import CryptoWidgets from "@/components/dashboard/CryptoCurrency/CryptoWidgets.vue"
import CoinAnalyticsChart from "@/components/dashboard/CryptoCurrency/CoinAnalyticsChart.vue"
import CoinAnalytics from "@/components/dashboard/CryptoCurrency/CoinAnalytics.vue"
import MyOrders from "@/components/dashboard/CryptoCurrency/MyOrders.vue"
import RecentTransaction from "@/components/dashboard/CryptoCurrency/RecentTransaction.vue"

import MyCards from "@/components/dashboard/CryptoCurrency/MyCards.vue"
import TotalBalance from "@/components/dashboard/CryptoCurrency/TotalBalance.vue"
import UserActivates from "@/components/dashboard/CryptoCurrency/UserActivates.vue"

export default {
  name: "CryptoCurrency",
  components: {
    Breadcrumb,
    apexchart: ApexCharts,
    Icon,
    CryptoWidgets,
    CoinAnalyticsChart,
    CoinAnalytics,
    MyOrders,
    RecentTransaction,
    MyCards,
    TotalBalance,
    UserActivates,
  },
};
</script>