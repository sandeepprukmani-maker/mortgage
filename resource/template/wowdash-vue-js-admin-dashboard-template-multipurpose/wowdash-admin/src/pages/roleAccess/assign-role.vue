<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Role & Access" :breadcrumbs="[
            { name: 'Role & Access' }
        ]" />

        <AssignRole />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import AssignRole from '@/components/RoleAccess/AssignRole.vue'

export default {
    name: "RolesAssign",
    components: {
        Breadcrumb,
        AssignRole
    },
}
</script>