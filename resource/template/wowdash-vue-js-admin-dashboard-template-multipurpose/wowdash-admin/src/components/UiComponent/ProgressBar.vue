<template>
    <div class="row gy-4">
        <!-- Default Progress -->
        <div class="col-sm-6">
            <div class="card p-0 overflow-hidden position-relative radius-12">
                <div class="card-header py-16 px-24 bg-base border border-end-0 border-start-0 border-top-0">
                    <h6 class="text-lg mb-0">Default Progress</h6>
                </div>
                <div class="card-body p-24">
                    <div class="d-flex align-items-center flex-column gap-4">
                        <div class="progress h-8-px w-100 bg-primary-50" role="progressbar" aria-label="Basic example"
                            aria-valuenow="20" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar rounded-pill bg-primary-600" style="width: 20%"></div>
                        </div>
                        <div class="progress h-8-px w-100 bg-primary-50" role="progressbar" aria-label="Basic example"
                            aria-valuenow="35" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar rounded-pill bg-primary-600" style="width: 35%"></div>
                        </div>
                        <div class="progress h-8-px w-100 bg-primary-50" role="progressbar" aria-label="Basic example"
                            aria-valuenow="50" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar rounded-pill bg-primary-600" style="width: 50%"></div>
                        </div>
                        <div class="progress h-8-px w-100 bg-primary-50" role="progressbar" aria-label="Basic example"
                            aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar rounded-pill bg-primary-600" style="width: 75%"></div>
                        </div>
                        <div class="progress h-8-px w-100 bg-primary-50" role="progressbar" aria-label="Basic example"
                            aria-valuenow="90" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar rounded-pill bg-primary-600" style="width: 90%"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Progress with multiple color -->
        <div class="col-sm-6">
            <div class="card p-0 overflow-hidden position-relative radius-12">
                <div class="card-header py-16 px-24 bg-base border border-end-0 border-start-0 border-top-0">
                    <h6 class="text-lg mb-0">Progress with multiple color</h6>
                </div>
                <div class="card-body p-24">
                    <div class="d-flex align-items-center flex-column gap-4">
                        <div class="progress h-8-px w-100 bg-primary-50" role="progressbar" aria-label="Basic example"
                            aria-valuenow="20" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar rounded-pill bg-primary-600" style="width: 20%"></div>
                        </div>
                        <div class="progress h-8-px w-100 bg-success-100" role="progressbar" aria-label="Basic example"
                            aria-valuenow="35" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar rounded-pill bg-success-600" style="width: 35%"></div>
                        </div>
                        <div class="progress h-8-px w-100 bg-info-100" role="progressbar" aria-label="Basic example"
                            aria-valuenow="50" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar rounded-pill bg-info-600" style="width: 50%"></div>
                        </div>
                        <div class="progress h-8-px w-100 bg-warning-100" role="progressbar" aria-label="Basic example"
                            aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar rounded-pill bg-warning-600" style="width: 75%"></div>
                        </div>
                        <div class="progress h-8-px w-100 bg-danger-100" role="progressbar" aria-label="Basic example"
                            aria-valuenow="90" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar rounded-pill bg-danger-600" style="width: 90%"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Progress with right label -->
        <div class="col-sm-6">
            <div class="card p-0 overflow-hidden position-relative radius-12">
                <div class="card-header py-16 px-24 bg-base border border-end-0 border-start-0 border-top-0">
                    <h6 class="text-lg mb-0">Progress with right label</h6>
                </div>
                <div class="card-body p-24">
                    <div class="d-flex align-items-center flex-column gap-3">
                        <div class="d-flex align-items-center gap-2 w-100">
                            <div class="w-100 ms-auto">
                                <div class="progress progress-sm rounded-pill" role="progressbar"
                                    aria-label="Success example" aria-valuenow="10" aria-valuemin="0"
                                    aria-valuemax="100">
                                    <div class="progress-bar bg-primary-600 rounded-pill" style="width: 10%;"></div>
                                </div>
                            </div>
                            <span class="text-secondary-light font-xs fw-semibold line-height-1">10%</span>
                        </div>
                        <div class="d-flex align-items-center gap-2 w-100">
                            <div class="w-100 ms-auto">
                                <div class="progress progress-sm rounded-pill" role="progressbar"
                                    aria-label="Success example" aria-valuenow="30" aria-valuemin="0"
                                    aria-valuemax="100">
                                    <div class="progress-bar bg-primary-600 rounded-pill" style="width: 30%;"></div>
                                </div>
                            </div>
                            <span class="text-secondary-light font-xs fw-semibold line-height-1">30%</span>
                        </div>
                        <div class="d-flex align-items-center gap-2 w-100">
                            <div class="w-100 ms-auto">
                                <div class="progress progress-sm rounded-pill" role="progressbar"
                                    aria-label="Success example" aria-valuenow="50" aria-valuemin="0"
                                    aria-valuemax="100">
                                    <div class="progress-bar bg-primary-600 rounded-pill" style="width: 50%;"></div>
                                </div>
                            </div>
                            <span class="text-secondary-light font-xs fw-semibold line-height-1">50%</span>
                        </div>
                        <div class="d-flex align-items-center gap-2 w-100">
                            <div class="w-100 ms-auto">
                                <div class="progress progress-sm rounded-pill" role="progressbar"
                                    aria-label="Success example" aria-valuenow="70" aria-valuemin="0"
                                    aria-valuemax="100">
                                    <div class="progress-bar bg-primary-600 rounded-pill" style="width: 70%;"></div>
                                </div>
                            </div>
                            <span class="text-secondary-light font-xs fw-semibold line-height-1">70%</span>
                        </div>
                        <div class="d-flex align-items-center gap-2 w-100">
                            <div class="w-100 ms-auto">
                                <div class="progress progress-sm rounded-pill" role="progressbar"
                                    aria-label="Success example" aria-valuenow="90" aria-valuemin="0"
                                    aria-valuemax="100">
                                    <div class="progress-bar bg-primary-600 rounded-pill" style="width: 90%;"></div>
                                </div>
                            </div>
                            <span class="text-secondary-light font-xs fw-semibold line-height-1">90%</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Striped Progress -->
        <div class="col-sm-6">
            <div class="card p-0 overflow-hidden position-relative radius-12">
                <div class="card-header py-16 px-24 bg-base border border-end-0 border-start-0 border-top-0">
                    <h6 class="text-lg mb-0">Striped Progress</h6>
                </div>
                <div class="card-body p-24">
                    <div class="d-flex align-items-center flex-column gap-4">
                        <div class="progress h-8-px w-100 bg-primary-50" role="progressbar" aria-label="Basic example"
                            aria-valuenow="20" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar progress-bar-striped progress-bar-animated rounded-pill bg-primary-600"
                                style="width: 20%"></div>
                        </div>
                        <div class="progress h-8-px w-100 bg-primary-50" role="progressbar" aria-label="Basic example"
                            aria-valuenow="35" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar progress-bar-striped progress-bar-animated rounded-pill bg-primary-600"
                                style="width: 35%"></div>
                        </div>
                        <div class="progress h-8-px w-100 bg-primary-50" role="progressbar" aria-label="Basic example"
                            aria-valuenow="50" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar progress-bar-striped progress-bar-animated rounded-pill bg-primary-600"
                                style="width: 50%"></div>
                        </div>
                        <div class="progress h-8-px w-100 bg-primary-50" role="progressbar" aria-label="Basic example"
                            aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar progress-bar-striped progress-bar-animated rounded-pill bg-primary-600"
                                style="width: 75%"></div>
                        </div>
                        <div class="progress h-8-px w-100 bg-primary-50" role="progressbar" aria-label="Basic example"
                            aria-valuenow="90" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar progress-bar-striped progress-bar-animated rounded-pill bg-primary-600"
                                style="width: 90%"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Animated Progress -->
        <div class="col-sm-6">
            <div class="card p-0 overflow-hidden position-relative radius-12">
                <div class="card-header py-16 px-24 bg-base border border-end-0 border-start-0 border-top-0">
                    <h6 class="text-lg mb-0">Animated Progress</h6>
                </div>
                <div class="card-body p-24">
                    <div class="d-flex align-items-center flex-column gap-4">
                        <div class="progress h-8-px w-100 bg-primary-50" role="progressbar" aria-label="Basic example"
                            aria-valuenow="20" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar animated-bar rounded-pill bg-primary-600" style="width: 20%"></div>
                        </div>
                        <div class="progress h-8-px w-100 bg-success-100" role="progressbar" aria-label="Basic example"
                            aria-valuenow="35" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar animated-bar rounded-pill bg-success-600" style="width: 35%"></div>
                        </div>
                        <div class="progress h-8-px w-100 bg-info-100" role="progressbar" aria-label="Basic example"
                            aria-valuenow="50" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar animated-bar rounded-pill bg-info-600" style="width: 50%"></div>
                        </div>
                        <div class="progress h-8-px w-100 bg-warning-100" role="progressbar" aria-label="Basic example"
                            aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar animated-bar rounded-pill bg-warning-600" style="width: 75%"></div>
                        </div>
                        <div class="progress h-8-px w-100 bg-danger-100" role="progressbar" aria-label="Basic example"
                            aria-valuenow="90" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar animated-bar rounded-pill bg-danger-600" style="width: 90%"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Gradient Progress -->
        <div class="col-sm-6">
            <div class="card p-0 overflow-hidden position-relative radius-12">
                <div class="card-header py-16 px-24 bg-base border border-end-0 border-start-0 border-top-0">
                    <h6 class="text-lg mb-0"> Gradient Progress </h6>
                </div>
                <div class="card-body p-24">
                    <div class="d-flex align-items-center flex-column gap-4">
                        <div class="progress h-8-px w-100 bg-primary-50" role="progressbar" aria-label="Basic example"
                            aria-valuenow="20" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar animated-bar rounded-pill bg-primary-gradient" style="width: 20%">
                            </div>
                        </div>
                        <div class="progress h-8-px w-100 bg-success-100" role="progressbar" aria-label="Basic example"
                            aria-valuenow="35" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar animated-bar rounded-pill bg-success-gradient" style="width: 35%">
                            </div>
                        </div>
                        <div class="progress h-8-px w-100 bg-info-100" role="progressbar" aria-label="Basic example"
                            aria-valuenow="50" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar animated-bar rounded-pill bg-info-gradient" style="width: 50%">
                            </div>
                        </div>
                        <div class="progress h-8-px w-100 bg-warning-100" role="progressbar" aria-label="Basic example"
                            aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar animated-bar rounded-pill bg-warning-gradient" style="width: 75%">
                            </div>
                        </div>
                        <div class="progress h-8-px w-100 bg-danger-100" role="progressbar" aria-label="Basic example"
                            aria-valuenow="90" aria-valuemin="0" aria-valuemax="100">
                            <div class="progress-bar animated-bar rounded-pill bg-danger-gradient" style="width: 90%">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Left Column (Floating Label Top) -->
        <div class="col-sm-6">
            <div class="card p-0 overflow-hidden position-relative radius-12">
                <div class="card-header py-16 px-24 bg-base border border-end-0 border-start-0 border-top-0">
                    <h6 class="text-lg mb-0">Gradient Progress</h6>
                </div>
                <div class="card-body p-24">
                    <div class="progress-wrapper d-flex align-items-center flex-column gap-4"
                        v-for="(item, index) in progressItems" :key="'top-' + index" :data-perc="item"
                        ref="floatingTop">
                        <div class="h-50-px position-relative w-100 d-flex">
                            <span
                                class="floating-label position-absolute text-xs fw-semibold text-secondary-light bg-base border radius-8 w-50-px h-32-px z-1 shadow d-flex justify-content-center align-items-center">
                                {{ item }}
                            </span>
                            <div class="progress mt-auto h-8-px w-100 bg-primary-50" role="progressbar"
                                aria-label="Basic example" :aria-valuenow="parseInt(item)" aria-valuemin="0"
                                aria-valuemax="100">
                                <div class="progress-bar animated-bar rounded-pill bg-primary-gradien overflow-visible"
                                    :style="{ width: item }"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Right Column (Floating Label Bottom) -->
        <div class="col-sm-6">
            <div class="card p-0 overflow-hidden position-relative radius-12">
                <div class="card-header py-16 px-24 bg-base border border-end-0 border-start-0 border-top-0">
                    <h6 class="text-lg mb-0">Gradient Progress</h6>
                </div>
                <div class="card-body p-24">
                    <div class="progress-wrapper d-flex align-items-center flex-column gap-4"
                        v-for="(item, index) in progressItems" :key="'bottom-' + index" :data-perc="item"
                        ref="floatingBottom">
                        <div class="h-50-px position-relative w-100">
                            <span
                                class="floating-label bottom-0 top-auto mt-12 position-absolute text-xs fw-semibold text-secondary-light bg-base border radius-8 w-50-px h-32-px z-1 shadow d-flex justify-content-center align-items-center">
                                {{ item }}
                            </span>
                            <div class="progress mt-auto h-8-px w-100 bg-primary-50" role="progressbar"
                                aria-label="Basic example" :aria-valuenow="parseInt(item)" aria-valuemin="0"
                                aria-valuemax="100">
                                <div class="progress-bar animated-bar rounded-pill bg-primary-gradien overflow-visible"
                                    :style="{ width: item }"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Progress Circle -->
        <div class="col-xxl-12">
            <div class="card p-0 overflow-hidden position-relative radius-12">
                <div class="card-header py-16 px-24 bg-base border border-end-0 border-start-0 border-top-0">
                    <h6 class="text-lg mb-0">Progress Circle</h6>
                </div>
                <div class="card-body p-24">
                    <div class="progressBar w-90-px h-44-px position-relative text-primary-light fw-semibold">
                        <div class="barOverflow">
                            <div class="circleBar border-width-6-px" ref="circleBar"></div>
                        </div>
                        <div class="position-absolute start-50 translate-middle top-50 line-height-1 mt-8">
                            <div class="d-flex align-items-center justify-content-center line-height-1 text-sm">
                                <span class="barNumber line-height-1" ref="barNumber">{{ circlePercent }}</span>
                                <span>%</span>
                            </div>
                            <span class="line-height-1 text-xs text-secondary-light">Users</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import { ref, onMounted, nextTick } from 'vue'

const progressItems = ['10%', '30%', '50%', '70%', '90%']
const floatingTop = ref([])
const floatingBottom = ref([])

const circleBar = ref(null)
const barNumber = ref(null)
const circlePercent = ref(40)

onMounted(async () => {
    await nextTick()

    // Floating labels animation
    const animateFloating = (el, perc) => {
        el.style.setProperty('--left-percentage', perc)
        el.style.animationName = 'none'
        void el.offsetWidth // Trigger reflow
        el.style.left = perc
        el.style.animationName = 'animateFloatingLabel'
    }

    floatingTop.value.forEach((wrapper) => {
        const perc = wrapper.getAttribute('data-perc')
        const label = wrapper.querySelector('.floating-label')
        animateFloating(label, perc)
    })

    floatingBottom.value.forEach((wrapper) => {
        const perc = wrapper.getAttribute('data-perc')
        const label = wrapper.querySelector('.floating-label')
        animateFloating(label, perc)
    })

    // Circular progress animation
    const perc = circlePercent.value
    let current = 0
    const duration = 3000
    const start = performance.now()

    const animateCircle = (timestamp) => {
        const elapsed = timestamp - start
        const progress = Math.min(elapsed / duration, 1)
        const value = Math.floor(progress * perc)
        barNumber.value.textContent = value
        circleBar.value.style.transform = `rotate(${45 + value * 1.8}deg)`

        if (progress < 1) requestAnimationFrame(animateCircle)
    }

    requestAnimationFrame(animateCircle)
})
</script>