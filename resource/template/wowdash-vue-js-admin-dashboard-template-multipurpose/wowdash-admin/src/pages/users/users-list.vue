<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Users List" :breadcrumbs="[
            { name: 'Users List' }
        ]" />

        <UserList />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import UserList from '@/components/Users/UserList.vue'

export default {
    name: "UsersList",
    components: {
        Breadcrumb,
        UserList,
    },
}
</script>