<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="Testimonials" :breadcrumbs="[
            { name: 'Testimonials' }
        ]" />

        <TestimonialData />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import TestimonialData from '@/components/Testimonial/TestimonialData.vue'
export default {
    name: "Testimonial",
    components: {
        Breadcrumb,
        TestimonialData,
    },
}
</script>