<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="Kanban" :breadcrumbs="[
            { name: 'Kanban' }
        ]" />
        
        <KanbanData />
    </div>

</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import { Icon } from "@iconify/vue"; 
import KanbanData from "@/components/kanban/Kanban.vue"

export default {
  name: "Kanban",
  components: {
    Breadcrumb,
    Icon,
    KanbanData,
  },
};
</script>