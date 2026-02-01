<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="Dropdown" :breadcrumbs="[
            { name: 'Components / Dropdown' }
        ]" />

        <DropdownButtons />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import DropdownButtons from '@/components/UiComponent/Dropdown.vue'

export default {
    name: "Dropdown",
    components: {
        Breadcrumb,
        DropdownButtons,
    },
}
</script>