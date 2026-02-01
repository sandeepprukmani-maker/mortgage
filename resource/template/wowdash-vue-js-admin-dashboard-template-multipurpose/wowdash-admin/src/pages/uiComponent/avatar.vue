<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Avatars" :breadcrumbs="[
            { name: 'Components / Avatars' }
        ]" />

        <AvatarData />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import AvatarData from '@/components/UiComponent/Avatars.vue'

export default {
    name: "Avatars",
    components: {
        Breadcrumb,
        AvatarData,
    },
}
</script>