<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Widgets" :breadcrumbs="[
            { name: 'Widgets' }
        ]" />
        <div class="card h-100 p-0 radius-12">
            <div class="card-header border-bottom bg-base py-16 px-24">
                <h6 class="text-lg fw-semibold mb-0">Metrics</h6>
            </div>
            <div class="card-body p-24">
                <MetricsOne />
                <MetricsTwo />
                <MetricsThree />
                <MetricsFour />
            </div>
        </div>

        <div class="row gy-4 mt-1">
            <SalesStatisticChart />
            <TopCountries />
            <ClientPaymentStatusChart />
            <EarningStatisticChart />
            <UsersOverviewChart />
            <TotalTransactionsChart />
            <Statisticchart />
        </div>

    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import MetricsOne from '@/components/Widgets/Metrics/MetricsOne.vue'
import MetricsTwo from '@/components/Widgets/Metrics/MetricsTwo.vue'
import MetricsThree from '@/components/Widgets/Metrics/MetricsThree.vue'
import MetricsFour from '@/components/Widgets/Metrics/MetricsFour.vue'
import SalesStatisticChart from '@/components/Widgets/SalesStatisticChart.vue'
import TopCountries from '@/components/Widgets/TopCountries.vue'
import ClientPaymentStatusChart from '@/components/Widgets/ClientPaymentStatusChart.vue'
import EarningStatisticChart from '@/components/Widgets/EarningStatisticChart.vue'
import UsersOverviewChart from '@/components/Widgets/UsersOverviewChart.vue'
import TotalTransactionsChart from '@/components/Widgets/TotalTransactionsChart.vue'
import Statisticchart from '@/components/Widgets/Statisticchart.vue'

export default {
  name: "Widgets",
  components: {
    Breadcrumb,
    MetricsOne,
    MetricsTwo,
    MetricsThree,
    MetricsFour,
    SalesStatisticChart,
    TopCountries,
    ClientPaymentStatusChart,
    EarningStatisticChart,
    UsersOverviewChart,
    TotalTransactionsChart,
    Statisticchart
  },
}
</script>