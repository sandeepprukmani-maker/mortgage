<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="Email" :breadcrumbs="[
            { name: 'Components / Email' }
        ]" />

        <div class="row gy-4">
            <EmailSidebar />
            <VeiwDetails />
        </div>
    </div>

</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import { Icon } from "@iconify/vue"; 
import EmailSidebar from "@/components/email/EmailSidebar.vue"
import VeiwDetails from "@/components/email/VeiwDetails.vue"

export default {
  name: "EmailViewDetails",
  components: {
    Breadcrumb,
    Icon,
    EmailSidebar,
    VeiwDetails,
  },
};
</script>