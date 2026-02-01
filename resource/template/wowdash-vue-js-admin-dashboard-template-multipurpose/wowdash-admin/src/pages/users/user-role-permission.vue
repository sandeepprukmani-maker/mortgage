<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="User Roles & Permissions" :breadcrumbs="[
            { name: 'User Roles & Permissions' }
        ]" />
        <RolesPermission />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import RolesPermission from '@/components/Users/RolesPermission.vue'

export default {
    name: "Roles&Permission",
    components: {
        Breadcrumb,
        RolesPermission,
    },
}
</script>