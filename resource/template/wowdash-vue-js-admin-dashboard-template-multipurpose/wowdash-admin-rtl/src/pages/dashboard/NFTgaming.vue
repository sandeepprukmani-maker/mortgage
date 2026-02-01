<template>
    <div class="dashboard-main-body nft-page">

        <Breadcrumb title="Dashboard" :breadcrumbs="[
            { name: 'NFT & Gaming' }
        ]" />

        <div class="row gy-4">
            <div class="col-xxl-8">
                <div class="row gy-4">
                    <TopNFT />
                    <TrendingBids />
                    <TrendingNFTs />
                    <RecentBid />
                </div>
            </div>

            <div class="col-xxl-4">
                <div class="row gy-4">
                    <ETHprice />
                    <Statistics />
                    <FeaturedCreators />
                    <FeaturedCreators2 />
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ApexCharts from "vue3-apexcharts";
import { Icon } from "@iconify/vue"; 
import TopNFT from "@/components/dashboard/NFTgaming/TopNFT.vue";
import TrendingBids from "@/components/dashboard/NFTgaming/TrendingBids.vue";
import TrendingNFTs from "@/components/dashboard/NFTgaming/TrendingNFTs.vue";
import RecentBid from "@/components/dashboard/NFTgaming/RecentBid.vue";
import ETHprice from "@/components/dashboard/NFTgaming/ETHprice.vue";
import Statistics from "@/components/dashboard/NFTgaming/Statistics.vue";
import FeaturedCreators from "@/components/dashboard/NFTgaming/FeaturedCreators.vue";
import FeaturedCreators2 from "@/components/dashboard/NFTgaming/FeaturedCreators2.vue";

export default {
  name: "Lms",
  components: {
    Breadcrumb,
    apexchart: ApexCharts,
    Icon,
    TopNFT,
    TrendingBids,
    TrendingNFTs,
    RecentBid,
    ETHprice,
    Statistics,
    FeaturedCreators,
    FeaturedCreators2
  },
};
</script>