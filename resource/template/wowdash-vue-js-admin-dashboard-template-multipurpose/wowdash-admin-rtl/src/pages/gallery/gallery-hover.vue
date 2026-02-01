<template>
    <div class="dashboard-main-body">
        <Breadcrumb title="Gallery Grid" :breadcrumbs="[
            { name: 'Gallery Grid' }
        ]" />

        <HoverEffectOne />
        <HoverEffectTwo />
        <HoverEffectThree />
        <HoverEffectFour />
        <HoverEffectFive />
        <HoverEffectSix />
        <HoverEffectSeven />
        <HoverEffectEight />
        <HoverEffectNine />
    </div>
</template>
<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import HoverEffectOne from '@/components/Gallery/GalleryHoverEffect/HoverEffectOne.vue'
import HoverEffectTwo from '@/components/Gallery/GalleryHoverEffect/HoverEffectTwo.vue'
import HoverEffectThree from '@/components/Gallery/GalleryHoverEffect/HoverEffectThree.vue'
import HoverEffectFour from '@/components/Gallery/GalleryHoverEffect/HoverEffectFour.vue'
import HoverEffectFive from '@/components/Gallery/GalleryHoverEffect/HoverEffectFive.vue'
import HoverEffectSix from '@/components/Gallery/GalleryHoverEffect/HoverEffectSix.vue'
import HoverEffectSeven from '@/components/Gallery/GalleryHoverEffect/HoverEffectSeven.vue'
import HoverEffectEight from '@/components/Gallery/GalleryHoverEffect/HoverEffectEight.vue'
import HoverEffectNine from '@/components/Gallery/GalleryHoverEffect/HoverEffectNine.vue'
export default {
    name: "HoverEffect",
    components: {
        Breadcrumb,
        HoverEffectOne,
        HoverEffectTwo,
        HoverEffectThree,
        HoverEffectFour,
        HoverEffectFive,
        HoverEffectSix,
        HoverEffectSeven,
        HoverEffectEight,
        HoverEffectNine
    },
}
</script>