<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Podcast" :breadcrumbs="[
            { name: 'Podcast' }
        ]" />

        <div class="row gy-4">
            <PodcastWidget />
            <AudienceStats />
            <EarningsOverview />
            <RecentlyPlayed />
            <RecentPurchasePlan />
            <CountriesStatus />
            <TrendingEpisodes />
            <Top5Categories />
            <TopPodcaster />
        </div>
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ApexCharts from "vue3-apexcharts";
import { Icon } from "@iconify/vue"; 
import PodcastWidget from "@/components/dashboard/Podcast/PodcastWidget.vue"
import AudienceStats from "@/components/dashboard/Podcast/AudienceStats.vue"
import EarningsOverview from "@/components/dashboard/Podcast/EarningsOverview.vue"
import RecentlyPlayed from "@/components/dashboard/Podcast/RecentlyPlayed.vue"
import RecentPurchasePlan from "@/components/dashboard/Podcast/RecentPurchasePlan.vue"
import CountriesStatus from "@/components/dashboard/Podcast/CountriesStatus.vue"
import TrendingEpisodes from "@/components/dashboard/Podcast/TrendingEpisodes.vue"
import Top5Categories from "@/components/dashboard/Podcast/Top5Categories.vue"
import TopPodcaster from "@/components/dashboard/Podcast/TopPodcaster.vue"

export default {
  name: "Podcast",
  components: {
    Breadcrumb,
    apexchart: ApexCharts,
    Icon,
    PodcastWidget,
    AudienceStats,
    EarningsOverview,
    RecentlyPlayed,
    RecentPurchasePlan,
    CountriesStatus,
    TrendingEpisodes,
    Top5Categories,
    TopPodcaster,
  },
};
</script>