<template>

    <div class="dashboard-main-body">
      
      <Breadcrumb title="Dashboard" :breadcrumbs="[
            { name: 'CRM' }
        ]" />

      <div class="row gy-4">
        <CrmTopbar/>
        <!-- Revenue Growth start -->
        <RevenueGrowth/>
        <!-- Revenue Growth End -->

        <!-- Earning Static start -->
        <EarningStatistic/>
        <!-- Earning Static End -->

        <!-- Campaign Static start -->
        <div class="col-xxl-4">
          <div class="row gy-4">
           <Campaigns/>
           <CustomOverview/>
          </div>
        </div>
        <!-- Campaign Static End -->

        <!-- Client Payment Status Start -->
        <ClientPaymentStatus/>
        <!-- Client Payment Status End -->

        <!-- Country Status Start -->
        <CountriesStatus/>
        <!-- Country Status End -->

        <!-- Top performance Start -->
        <TopPerformer />
        <!-- Top performance End -->

        <!-- Latest Performance Start -->
        <Allitem />
        <LastTransaction />
        <!-- Latest Performance End -->
      </div>
    </div>

</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ApexCharts from "vue3-apexcharts";
import { Icon } from "@iconify/vue"; 
import CrmTopbar from "@/components/dashboard/Crm/CrmTopbar.vue"
import RevenueGrowth from "@/components/dashboard/Crm/RevenueGrowth.vue"
import EarningStatistic from "@/components/dashboard/Crm/EarningStatistic.vue"
import ClientPaymentStatus from "@/components/dashboard/Crm/ClientPaymentStatus.vue"
import CustomOverview from "@/components/dashboard/Crm/CustomOverview.vue"
import Campaigns from "@/components/dashboard/Crm/Campaigns.vue"
import CountriesStatus from "@/components/dashboard/Crm/CountriesStatus.vue"
import TopPerformer from "@/components/dashboard/Crm/TopPerformer.vue"
import Allitem from "@/components/dashboard/Crm/Allitem.vue"
import LastTransaction from "@/components/dashboard/Crm/LastTransaction.vue"

export default {
  name: "Crm",
  components: {
    Breadcrumb,
    apexchart: ApexCharts,
    Icon,
    CrmTopbar,
    RevenueGrowth,
    EarningStatistic,
    ClientPaymentStatus,
    Campaigns,
    CustomOverview,
    CountriesStatus,
    TopPerformer,
    Allitem,
    LastTransaction,
  },
};
</script>
