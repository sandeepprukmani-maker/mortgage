<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Card" :breadcrumbs="[
            { name: 'Components / Card' }
        ]" />

        <CardData />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import CardData from '@/components/UiComponent/Card.vue'

export default {
    name: "Card",
    components: {
        Breadcrumb,
        CardData,
    },
}
</script>