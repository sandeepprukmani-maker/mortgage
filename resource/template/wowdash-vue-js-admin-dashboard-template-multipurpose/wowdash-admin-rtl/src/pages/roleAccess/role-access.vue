<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Role & Access" :breadcrumbs="[
            { name: 'Role & Access' }
        ]" />

        <Role />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import Role from '@/components/RoleAccess/Role.vue'

export default {
    name: "RoleAcces",
    components: {
        Breadcrumb,
        Role,
    },
}
</script>