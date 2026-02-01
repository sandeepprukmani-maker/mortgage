<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Line Chart" :breadcrumbs="[
            { name: 'Components / Line Chart' }
        ]" />

        <div class="row gy-4">
            <DefaultChart />
            <ZoomableChart />
            <DataLabelChart />
            <AnimationChart />
            <SteplineChart />
            <GradientChart />
        </div>

    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import DefaultChart from '@/components/Chart/LineChart/DefaultChart.vue'
import ZoomableChart from '@/components/Chart/LineChart/ZoomableChart.vue'
import DataLabelChart from '@/components/Chart/LineChart/DataLabelChart.vue'
import AnimationChart from '@/components/Chart/LineChart/AnimationChart.vue'
import SteplineChart from '@/components/Chart/LineChart/SteplineChart.vue'
import GradientChart from '@/components/Chart/LineChart/GradientChart.vue'

export default {
    name: "LineChart",
    components: {
        Breadcrumb,
        DefaultChart,
        ZoomableChart,
        DataLabelChart,
        AnimationChart,
        SteplineChart,
        GradientChart
    },
}
</script>