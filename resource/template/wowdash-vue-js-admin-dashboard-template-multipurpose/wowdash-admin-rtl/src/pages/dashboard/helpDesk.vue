<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Help Desk" :breadcrumbs="[
            { name: 'Help Desk' }
        ]" />

        <div class="row gy-4">
            <TaskSummary />
            <TicketPriority />
            <TicketStatus />
            <PendingSolvedTicket />
            <ToDoList />    
            <TopPodcaster />
            <PerformanceofAgents />
            <ResponseTime />
        </div>

    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ApexCharts from "vue3-apexcharts";
import { Icon } from "@iconify/vue"; 
import TaskSummary from "@/components/dashboard/HelpDesk/TaskSummary.vue"
import TicketPriority from "@/components/dashboard/HelpDesk/TicketPriority.vue"
import TicketStatus from "@/components/dashboard/HelpDesk/TicketStatus.vue"
import PendingSolvedTicket from "@/components/dashboard/HelpDesk/PendingSolvedTicket.vue"
import ToDoList from "@/components/dashboard/HelpDesk/ToDoList.vue"
import TopPodcaster from "@/components/dashboard/HelpDesk/TopPodcaster.vue"
import PerformanceofAgents from "@/components/dashboard/HelpDesk/PerformanceofAgents.vue"
import ResponseTime from "@/components/dashboard/HelpDesk/ResponseTime.vue"

export default {
  name: "HelpDesk",
  components: {
    Breadcrumb,
    apexchart: ApexCharts,
    Icon,
    TaskSummary,
    TicketPriority,
    TicketStatus,
    PendingSolvedTicket,
    ToDoList,
    TopPodcaster,
    PerformanceofAgents,
    ResponseTime
  },
};
</script>