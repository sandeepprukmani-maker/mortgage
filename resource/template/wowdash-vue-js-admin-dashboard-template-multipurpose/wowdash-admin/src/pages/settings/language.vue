<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="Languages" :breadcrumbs="[
            { name: 'Settings - Languages' }
        ]" />

        <Languages />
    </div>

</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import Languages from '@/components/Settings/Languages.vue'
export default {
    name: "LanguagesData",
    components: {
        Breadcrumb,
        Languages
    },
}
</script>