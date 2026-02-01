<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Users Grid" :breadcrumbs="[
            { name: 'Users Grid' }
        ]" />

        <UserGrid />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import UserGrid from '@/components/Users/UserGrid.vue'

export default {
    name: "UsersGrid",
    components: {
        Breadcrumb,
        UserGrid,
    },
}
</script>