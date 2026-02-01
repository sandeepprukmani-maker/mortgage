<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Star Ratings" :breadcrumbs="[
            { name: 'Components / Star Ratings' }
        ]" />

        <StarRatings />
    </div>

</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import StarRatings from '@/components/UiComponent/StarRatings.vue'

export default {
    name: "StarRating",
    components: {
        Breadcrumb,
        StarRatings,
    },
}
</script>