<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="400" :breadcrumbs="[
            { name: '400' }
        ]" />

        <BadRequest />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import BadRequest from '@/components/Error/BadRequest.vue'
export default {
    name: "BadRequestError",
    components: {
        Breadcrumb,
        BadRequest
    },
}
</script>