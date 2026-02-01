<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Pie Chart" :breadcrumbs="[
            { name: 'Components / Pie Chart' }
        ]" />

        <div class="row gy-4">
        <BasicChart />
        <DonutChart />
        <RadarChart />
        <MultipleseriesChart />
        </div>

    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import BasicChart from '@/components/Chart/PieChart/BasicChart.vue'
import DonutChart from '@/components/Chart/PieChart/DonutChart.vue'
import RadarChart from '@/components/Chart/PieChart/RadarChart.vue'
import MultipleseriesChart from '@/components/Chart/PieChart/MultipleseriesChart.vue'

export default {
  name: "PieChart",
  components: {
    Breadcrumb,
    BasicChart,
    DonutChart,
    RadarChart,
    MultipleseriesChart
  },
}
</script>