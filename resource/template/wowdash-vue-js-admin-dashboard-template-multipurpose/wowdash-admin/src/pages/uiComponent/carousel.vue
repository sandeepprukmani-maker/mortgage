<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Carousel" :breadcrumbs="[
            { name: 'Components / Carousel' }
        ]" />

        <div class="row gy-4">
            <DefaultCarousel />
            <CarouselArrow />
            <CarouselPagination />
            <CarouselProgress />
            <MultipleSlides />
        </div>

    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import DefaultCarousel from '@/components/UiComponent/Carousel/DefaultCarousel.vue'
import CarouselArrow from '@/components/UiComponent/Carousel/CarouselArrow.vue'
import CarouselPagination from '@/components/UiComponent/Carousel/CarouselPagination.vue'
import CarouselProgress from '@/components/UiComponent/Carousel/CarouselProgress.vue'
import MultipleSlides from '@/components/UiComponent/Carousel/MultipleSlides.vue'

export default {
    name: "Carousel",
    components: {
        Breadcrumb,
        DefaultCarousel,
        CarouselArrow,
        CarouselPagination,
        CarouselProgress,
        MultipleSlides,
    },
}
</script>