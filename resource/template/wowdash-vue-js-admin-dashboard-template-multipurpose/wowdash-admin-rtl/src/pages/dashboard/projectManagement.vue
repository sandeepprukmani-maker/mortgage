<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Project Management" :breadcrumbs="[
            { name: 'Project Management' }
        ]" />

        <div class="row gy-4">
            <AverageEarnings />
            <WorkingSchedule />

            <!-- Widgets start -->
            <ProjectWidget />
            <!-- Widgets End -->

            <MyTasks />
            <ProjectAnalysis />
            <TeamMembers />
            <TasksOverview />
            <ProjectsStatus />
        </div>
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ApexCharts from "vue3-apexcharts";
import { Icon } from "@iconify/vue"; 
import AverageEarnings from "@/components/dashboard/ProjectManagement/AverageEarnings.vue"
import WorkingSchedule from "@/components/dashboard/ProjectManagement/WorkingSchedule.vue"
import ProjectWidget from "@/components/dashboard/ProjectManagement/ProjectWidget.vue"
import MyTasks from "@/components/dashboard/ProjectManagement/MyTasks.vue"
import ProjectAnalysis from "@/components/dashboard/ProjectManagement/ProjectAnalysis.vue"
import TeamMembers from "@/components/dashboard/ProjectManagement/TeamMembers.vue"
import TasksOverview from "@/components/dashboard/ProjectManagement/TasksOverview.vue"
import ProjectsStatus from "@/components/dashboard/ProjectManagement/ProjectsStatus.vue"

export default {
  name: "ProjectManagement",
  components: {
    Breadcrumb,
    apexchart: ApexCharts,
    Icon,
    AverageEarnings,
    WorkingSchedule,
    ProjectWidget,
    MyTasks,
    ProjectAnalysis,
    TeamMembers,
    TasksOverview,
    ProjectsStatus
  },
};
</script>