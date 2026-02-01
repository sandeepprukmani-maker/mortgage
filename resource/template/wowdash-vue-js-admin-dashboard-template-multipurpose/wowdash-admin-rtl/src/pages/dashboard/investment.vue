<template>
    <div class="dashboard-main-body">

      <Breadcrumb title="Dashboard" :breadcrumbs="[
            { name: 'Investment' }
        ]" />

      <div class="row gy-4">

        <!-- Dashboard Widget Start -->
        <InvestmentWidget />
        <!-- Dashboard Widget End -->

        <!-- Revenue Statistics Start -->
        <RevenueStatistics />
        <!-- Revenue Statistics End -->

        <!-- Statistics Start -->
        <Statistic />
        <!-- Statistics End -->

        <!-- Most Location Start -->
        <MostLocation />
        <!-- Most Location End -->

        <!-- My portfolio Start -->
        <MyPortfolio />
        <!-- My portfolio End -->

        <!-- Latest Investments Start -->
        <LatestInvestments />
        <!-- Latest Investments End -->

        <!-- Notice board Start -->
        <NoticeBoard />
        <!-- Notice board End -->

        <!-- Total Transactions Start -->
        <TotalTransactions />
        <!-- Total Transactions End -->

        <!-- Project Status Start -->
        <ProjectStatus />
        <!-- Project Status End -->

      </div>

    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ApexCharts from "vue3-apexcharts";
import { Icon } from "@iconify/vue"; 
import InvestmentWidget from "@/components/dashboard/Investment/InvestmentWidget.vue"
import RevenueStatistics from "@/components/dashboard/Investment/RevenueStatistics.vue"
import Statistic from "@/components/dashboard/Investment/Statistic.vue"
import MostLocation from "@/components/dashboard/Investment/MostLocation.vue"
import MyPortfolio from "@/components/dashboard/Investment/MyPortfolio.vue"
import LatestInvestments from "@/components/dashboard/Investment/LatestInvestments.vue"
import NoticeBoard from "@/components/dashboard/Investment/NoticeBoard.vue"
import TotalTransactions from "@/components/dashboard/Investment/TotalTransactions.vue"
import ProjectStatus from "@/components/dashboard/Investment/ProjectStatus.vue"

export default {
  name: "Investment",
  components: {
    Breadcrumb,
    apexchart: ApexCharts,
    Icon,
    InvestmentWidget,
    RevenueStatistics,
    Statistic,
    MostLocation,
    MyPortfolio,
    LatestInvestments,
    NoticeBoard,
    TotalTransactions,
    ProjectStatus,
  },
};
</script>