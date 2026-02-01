<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Booking System" :breadcrumbs="[
            { name: 'Booking System' }
        ]" />

        <div class="mb-24">
            <div class="row gy-4">

                <!-- Card Start -->
                <BookingWidget />
                <!-- Card End -->

                <!-- Semi Circle Gauge start -->
                <AvailableRoom />
                <!-- Semi Circle Gauge End -->

                <!-- Booking Statistics progress start -->
                <BookingStatistic />
                <!-- Booking Statistics progress End -->

            </div>
        </div>
        <div class="row g-4">
            <div class="col-xl-8">
                <div class="d-flex flex-column gap-24">

                    <!-- Travel Slider Start -->
                    <ExclusiveTravelPackages />
                    <!-- Travel SLider end -->

                    <!-- Earning Statistics start -->
                    <EarningStatistic />
                    <!-- Earning Statistics end -->

                    <!-- Transaction History Table Start -->
                    <TransactionHistory />
                    <!-- Transaction History Table end -->

                </div>
            </div>


            <div class="col-xl-4">
                <div class="d-flex flex-column gap-24">

                    <!-- Country Status Start -->
                    <CountriesStatus />
                    <!-- Country Status End -->

                    <!-- Check in checkout Start -->
                    <CheckInCheckout />
                    <!-- Check in checkout End -->

                    <!-- Spend Overview Progress Start -->
                    <SpendOverview />
                    <!-- Spend Overview Progress End -->

                </div>
            </div>
        </div>
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ApexCharts from "vue3-apexcharts";
import { Icon } from "@iconify/vue"; 
import BookingWidget from "@/components/dashboard/BookingSystem/BookingWidget.vue"
import AvailableRoom from "@/components/dashboard/BookingSystem/AvailableRoom.vue"
import BookingStatistic from "@/components/dashboard/BookingSystem/BookingStatistic.vue"
import ExclusiveTravelPackages from "@/components/dashboard/BookingSystem/ExclusiveTravel.vue"
import EarningStatistic from "@/components/dashboard/BookingSystem/EarningStatistic.vue"
import TransactionHistory from "@/components/dashboard/BookingSystem/TransactionHistory.vue"
import CountriesStatus from "@/components/dashboard/BookingSystem/CountriesStatus.vue"
import CheckInCheckout from "@/components/dashboard/BookingSystem/CheckInCheckout.vue"
import SpendOverview from "@/components/dashboard/BookingSystem/SpendOverview.vue"

export default {
  name: "BookingSystem",
  components: {
    Breadcrumb,
    apexchart: ApexCharts,
    Icon,
    BookingWidget,
    AvailableRoom,
    BookingStatistic,
    ExclusiveTravelPackages,
    EarningStatistic,
    TransactionHistory,
    CountriesStatus,
    CheckInCheckout,
    SpendOverview
  },
};
</script>