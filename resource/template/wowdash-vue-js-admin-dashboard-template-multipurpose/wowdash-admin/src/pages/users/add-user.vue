<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Add User" :breadcrumbs="[
            { name: 'Add User' }
        ]" />

        <AddUser />

        
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import AddUser from '@/components/Users/AddUser.vue'

export default {
  name: "AddUsers",
  components: {
    Breadcrumb,
    AddUser,
  },
}
</script>