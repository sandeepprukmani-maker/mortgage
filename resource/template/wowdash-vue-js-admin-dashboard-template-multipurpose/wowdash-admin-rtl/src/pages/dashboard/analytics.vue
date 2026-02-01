<template>
  <div class="dashboard-main-body">

    <Breadcrumb title="Analytics" :breadcrumbs="[
      { name: 'Analytics' }
    ]" />
    <div class="row gy-4">
      <AnalyticsWidget />
      <RevenueStatistic />
      <SupportTracker />
      <AverageDailySales />
      <Transactions />
      <SalesbyCountries />
      <SourceVisitors />
      <MonthlyCampaignState />
      <RecentActivity />
    </div>
  </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ApexCharts from "vue3-apexcharts";
import { Icon } from "@iconify/vue"; 
import AnalyticsWidget from "@/components/dashboard/Analytics/AnalyticsWidget.vue"
import RevenueStatistic from "@/components/dashboard/Analytics/RevenueStatistic.vue"
import SupportTracker from "@/components/dashboard/Analytics/SupportTracker.vue"
import AverageDailySales from "@/components/dashboard/Analytics/AverageDailySales.vue"
import Transactions from "@/components/dashboard/Analytics/Transactions.vue"
import SalesbyCountries from "@/components/dashboard/Analytics/SalesbyCountries.vue"
import SourceVisitors from "@/components/dashboard/Analytics/SourceVisitors.vue"
import MonthlyCampaignState from "@/components/dashboard/Analytics/MonthlyCampaign.vue"
import RecentActivity from "@/components/dashboard/Analytics/RecentActivity.vue"

export default {
  name: "Lms",
  components: {
    Breadcrumb,
    apexchart: ApexCharts,
    Icon,
    AnalyticsWidget,
    RevenueStatistic,
    SupportTracker,
    AverageDailySales,
    Transactions,
    SalesbyCountries,
    SourceVisitors,
    MonthlyCampaignState,
    RecentActivity
  },
};
</script>