<template>
    <div class="card h-100 p-0 radius-12 overflow-hidden">
        <div class="card-header border-bottom-0 pb-0 pt-0 px-0">
            <ul class="nav border-gradient-tab nav-pills mb-0 border-top-0" id="pills-tab" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link" :class="{ active: activeTab === 'all' }" @click="activeTab = 'all'"
                        type="button">All</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" :class="{ active: activeTab === 'ui-design' }"
                        @click="activeTab = 'ui-design'" type="button">UI Design</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" :class="{ active: activeTab === 'web-design' }"
                        @click="activeTab = 'web-design'" type="button">Web Design</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" :class="{ active: activeTab === 'development' }"
                        @click="activeTab = 'development'" type="button">Development</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" :class="{ active: activeTab === 'presentation' }"
                        @click="activeTab = 'presentation'" type="button">Presentations</button>
                </li>
            </ul>
        </div>
        <div class="card-body p-24">
            <div class="row gy-4">
                <div class="col-xxl-3 col-md-4 col-sm-6" v-for="(image, index) in getImagesByTab" :key="index">
                    <div class="hover-scale-img border radius-16 overflow-hidden">
                        <div class="max-h-266-px overflow-hidden">
                            <img :src="image.src" alt="" class="hover-scale-img__img w-100 h-100 object-fit-cover" />
                        </div>
                        <div class="py-16 px-24">
                            <h6 class="mb-4">{{ image.title }}</h6>
                            <p class="mb-0 text-sm text-secondary-light">{{ image.category }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import galleryImg1 from '@/assets/images/gallery/gallery-img1.png'
import galleryImg2 from '@/assets/images/gallery/gallery-img2.png'
import galleryImg3 from '@/assets/images/gallery/gallery-img3.png'
import galleryImg4 from '@/assets/images/gallery/gallery-img4.png'
import galleryImg5 from '@/assets/images/gallery/gallery-img5.png'
import galleryImg6 from '@/assets/images/gallery/gallery-img6.png'
import galleryImg7 from '@/assets/images/gallery/gallery-img7.png'
import galleryImg8 from '@/assets/images/gallery/gallery-img8.png'
import galleryImg9 from '@/assets/images/gallery/gallery-img9.png'
import galleryImg10 from '@/assets/images/gallery/gallery-img10.png'
import galleryImg11 from '@/assets/images/gallery/gallery-img11.png'
import galleryImg12 from '@/assets/images/gallery/gallery-img12.png'

export default {
    data() {
        return {
            activeTab: 'all',
            allImages: [
                { src: galleryImg1, title: 'This is Image title', category: 'UI Design' },
                { src: galleryImg2, title: 'This is Image title', category: 'Web Design' },
                { src: galleryImg3, title: 'This is Image title', category: 'Development' },
                { src: galleryImg4, title: 'This is Image title', category: 'UI Design' },
                { src: galleryImg5, title: 'This is Image title', category: 'Presentation' },
                { src: galleryImg6, title: 'This is Image title', category: 'Web Design' },
                { src: galleryImg7, title: 'This is Image title', category: 'Development' },
                { src: galleryImg8, title: 'This is Image title', category: 'Presentation' },
                { src: galleryImg9, title: 'This is Image title', category: 'UI Design' },
                { src: galleryImg10, title: 'This is Image title', category: 'Presentation' },
                { src: galleryImg11, title: 'This is Image title', category: 'Development' },
                { src: galleryImg12, title: 'This is Image title', category: 'Web Design' },
                { src: galleryImg1, title: 'This is Image title', category: 'UI Design' },
                { src: galleryImg2, title: 'This is Image title', category: 'Web Design' },
                { src: galleryImg3, title: 'This is Image title', category: 'Development' },
                { src: galleryImg4, title: 'This is Image title', category: 'UI Design' },
                { src: galleryImg5, title: 'This is Image title', category: 'Presentation' },
                { src: galleryImg6, title: 'This is Image title', category: 'Web Design' },
                { src: galleryImg7, title: 'This is Image title', category: 'Development' },
                { src: galleryImg8, title: 'This is Image title', category: 'Presentation' },
                { src: galleryImg9, title: 'This is Image title', category: 'Presentation' },
                { src: galleryImg10, title: 'This is Image title', category: 'Presentation' },
                { src: galleryImg11, title: 'This is Image title', category: 'Development' },
                { src: galleryImg12, title: 'This is Image title', category: 'UI Design' },
            ]
        }
    },
    computed: {
        getImagesByTab() {
            if (this.activeTab === 'all') return this.allImages
            if (this.activeTab === 'ui-design') return this.allImages.filter(img => img.category === 'UI Design')
            if (this.activeTab === 'web-design') return this.allImages.filter(img => img.category === 'Web Design')
            if (this.activeTab === 'development') return this.allImages.filter(img => img.category === 'Development')
            if (this.activeTab === 'presentation') return this.allImages.filter(img => img.category === 'Presentation')
            return []
        }
    }
}
</script>