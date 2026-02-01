<template>
  <div class="dashboard-main-body">
    <Breadcrumb title="Dashboard" :breadcrumbs="[{ name: 'Ai' }]" />
     
    <AiWidgets />

    <div class="row gy-4 mt-1">
      <SalesStatistic />
      <TotalSubscriber />
      <UserOverview />
      <LatestUser /> <!-- Latest Register & Latest Subscribe -->
      <TopPerformer />
      <CountriesMap />
      <GeneratedContent />
    </div>
  </div>
</template>
<script>
import Breadcrumb from "@/components/breadcrumb/Breadcrumb.vue";
import { ref } from "vue";
import ApexCharts from "vue3-apexcharts";
import { Icon } from "@iconify/vue"; 
import AiWidgets from "@/components/dashboard/Ai/AiWidgets.vue";
import SalesStatistic from "@/components/dashboard/Ai/SalesStatistic.vue";
import TotalSubscriber from "@/components/dashboard/Ai/TotalSubscriber.vue"
import UserOverview from "@/components/dashboard/Ai/UserOverview.vue"; 
import LatestUser from "@/components/dashboard/Ai/LatestUser.vue"; 
import TopPerformer from "@/components/dashboard/Ai/TopPerformer.vue"; 
import CountriesMap from "@/components/dashboard/Ai/CountriesMap.vue"
import GeneratedContent from "@/components/dashboard/Ai/GeneratedContent.vue"

export default {
  name: "Ai",
  components: {
    Breadcrumb,
    apexchart: ApexCharts,
    Icon,
    AiWidgets,
    LatestUser,
    SalesStatistic,
    TotalSubscriber,
    UserOverview,
    TopPerformer,
    CountriesMap,
    GeneratedContent,
  },
};
</script>
