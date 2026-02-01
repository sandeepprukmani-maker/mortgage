<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Email" :breadcrumbs="[
            { name: 'Components / Email' }
        ]" />

        <div class="row gy-4">
        <EmailSidebar />
        <EmailData />
        </div>
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import { Icon } from "@iconify/vue"; 
import EmailSidebar from "@/components/email/EmailSidebar.vue"
import EmailData from "@/components/email/EmailData.vue"

export default {
  name: "Email",
  components: {
    Breadcrumb,
    Icon,
    EmailSidebar,
    EmailData,
  },
};
</script>