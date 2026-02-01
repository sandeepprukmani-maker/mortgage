<template>
        <div class="dashboard-main-body">

            <Breadcrumb title="Dashboard" :breadcrumbs="[
            { name: 'Medical' }
        ]" />

            <div class="row gy-4">
                <div class="col-xxxl-9">
                    <div class="row gy-4">
                        <MedicalWidget />

                        <!-- Earning Statistic -->
                        <EarningStatistic />
                        <!-- Earning Statistic -->

                        <!-- Patient Visited by Depertment & gender -->
                        <PatientVisited />
                        <!-- Patient Visited by Depertment & gender -->

                        <!-- Doctors List Start -->
                        <DoctorsList />
                        <!-- Doctors List End -->

                        <!-- Latest Performance Start -->
                        <LatestAppointments />
                        <!-- Latest Performance End -->
                    </div>
                </div>

                <div class="col-xxxl-3">
                    <div class="row gy-4">
                        <Totalincome />
                        <AvailableTreatments />
                        <HealthReportsDocument />
                    </div>
                </div>
            </div>
        </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ApexCharts from "vue3-apexcharts";
import { Icon } from "@iconify/vue"; 
import MedicalWidget from "@/components/dashboard/Medical/MedicalWidget.vue"
import EarningStatistic from "@/components/dashboard/Medical/EarningStatistic.vue"
import PatientVisited from "@/components/dashboard/Medical/PatientVisited.vue"
import DoctorsList from "@/components/dashboard/Medical/DoctorsList.vue"
import LatestAppointments from "@/components/dashboard/Medical/LatestAppointments.vue"
import Totalincome from "@/components/dashboard/Medical/Totalincome.vue"
import AvailableTreatments from "@/components/dashboard/Medical/AvailableTreatments.vue"
import HealthReportsDocument from "@/components/dashboard/Medical/HealthReports.vue"

export default {
  name: "Lms",
  components: {
    Breadcrumb,
    apexchart: ApexCharts,
    Icon,
    MedicalWidget,
    EarningStatistic,
    PatientVisited,
    DoctorsList,
    LatestAppointments,
    Totalincome,
    AvailableTreatments,
    HealthReportsDocument
  },
};
</script>