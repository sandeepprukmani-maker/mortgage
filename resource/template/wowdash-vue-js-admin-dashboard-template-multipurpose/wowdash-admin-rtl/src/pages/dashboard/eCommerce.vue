<template>
  <div class="dashboard-main-body">


    <Breadcrumb title="Dashboard" :breadcrumbs="[
      { name: 'eCommerce' }
    ]" />

    <div class="row gy-4">
      <RevenueReport />
      <CustomersStatistics />
      <RecentOrders />
      <Transactions />
      <RecentOrdersChart />
      <DistributionMaps />
      <TopCustomers />
      <TopSellingProduct />
      <StockReport />
    </div>

  </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ApexCharts from "vue3-apexcharts";
import { Icon } from "@iconify/vue"; 
import RevenueReport from "@/components/dashboard/eCommerce/RevenueReport.vue"
import CustomersStatistics from "@/components/dashboard/eCommerce/CustomersStatistics.vue"
import RecentOrders from "@/components/dashboard/eCommerce/RecentOrders.vue"
import Transactions from "@/components/dashboard/eCommerce/Transactions.vue"
import RecentOrdersChart from "@/components/dashboard/eCommerce/RecentOrdersChart.vue"
import DistributionMaps from "@/components/dashboard/eCommerce/DistributionMaps.vue"
import TopCustomers from "@/components/dashboard/eCommerce/TopCustomers.vue"
import TopSellingProduct from "@/components/dashboard/eCommerce/TopSellingProduct.vue"
import StockReport from "@/components/dashboard/eCommerce/StockReport.vue"

export default {
  name: "eCommerce",
  components: {
    Breadcrumb,
    apexchart: ApexCharts,
    Icon,
    RevenueReport,
    CustomersStatistics,
    RecentOrders,
    Transactions,
    RecentOrdersChart,
    DistributionMaps,
    TopCustomers,
    TopSellingProduct,
    StockReport,
  },
};
</script>