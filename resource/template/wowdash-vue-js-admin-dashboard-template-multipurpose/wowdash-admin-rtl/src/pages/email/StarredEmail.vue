<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="Email" :breadcrumbs="[
            { name: 'Components / Email' }
        ]" />

        <div class="row gy-4">
            <EmailSidebar />
            <StarredEmailData />
        </div>
    </div>

</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import { Icon } from "@iconify/vue";
import EmailSidebar from "@/components/email/EmailSidebar.vue"
import StarredEmailData from "@/components/email/StarredEmail.vue"

export default {
    name: "StarredEmail",
    components: {
        Breadcrumb,
        Icon,
        EmailSidebar,
        StarredEmailData,
    },
};
</script>