<template>
    <div class="card h-100 p-0 radius-12 overflow-hidden">
        <div class="card-header border-bottom bg-base py-16 px-24">
            <h6 class="mb-0 text-lg">Pricing Plan Multiple Color</h6>
        </div>
        <div class="card-body p-40">
            <div class="row justify-content-center">
                <div class="col-xxl-10">
                    <div class="text-center">
                        <h4 class="mb-16">Pricing Plan</h4>
                        <p class="mb-0 text-lg text-secondary-light">No contracts. No surprise fees.</p>
                    </div>

                    <!-- Tabs -->
                    <ul class="nav nav-pills button-tab mt-32 pricing-tab justify-content-center" role="tablist">
                        <li class="nav-item" role="presentation">
                            <button class="nav-link px-24 py-10 text-md rounded-pill text-secondary-light fw-medium"
                                :class="{ active: activeTab === 'monthly' }" type="button" role="tab"
                                @click="activeTab = 'monthly'">
                                Monthly
                            </button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link px-24 py-10 text-md rounded-pill text-secondary-light fw-medium"
                                :class="{ active: activeTab === 'yearly' }" type="button" role="tab"
                                @click="activeTab = 'yearly'">
                                Yearly
                            </button>
                        </li>
                    </ul>

                    <!-- Tab content -->
                    <div class="tab-content mt-4">
                        <!-- Monthly Tab -->
                        <div class="tab-pane fade" :class="{ 'show active': activeTab === 'monthly' }" role="tabpanel">
                            <div class="row gy-4">
                                <div class="col-xxl-4 col-sm-6 pricing-plan-wrapper" v-for="(plan, i) in monthlyPlans"
                                    :key="'m' + i">
                                    <div class="pricing-plan position-relative radius-24 overflow-hidden border"
                                        :class="plan.bgClass">
                                        <span v-if="plan.popular"
                                            class="bg-white bg-opacity-25 text-white radius-24 py-8 px-24 text-sm position-absolute end-0 top-0 z-1 rounded-start-top-0 rounded-end-bottom-0">
                                            Popular
                                        </span>
                                        <div class="d-flex align-items-center gap-16">
                                            <span
                                                class="w-72-px h-72-px d-flex justify-content-center align-items-center radius-16 bg-base">
                                                <img :src="plan.icon" alt="">
                                            </span>
                                            <div>
                                                <span class="fw-medium text-md"
                                                    :class="plan.title === 'Pro' ? 'text-white' : 'text-black dark:text-white'">{{
                                                    plan.target }}</span>
                                                <h6 class="mb-0"
                                                    :class="plan.title === 'Pro' ? 'text-white' : 'text-black dark:text-white'">
                                                    {{ plan.title }}</h6>
                                            </div>
                                        </div>
                                        <p class="mt-16 mb-0 mb-28"
                                            :class="plan.title === 'Pro' ? 'text-white' : 'text-black dark:text-white'">
                                            {{ plan.description }}</p>
                                        <h3 class="mb-24"
                                            :class="plan.title === 'Pro' ? 'text-white' : 'text-black dark:text-white'">
                                            {{ plan.price }}
                                            <span class="fw-medium text-md"
                                                :class="plan.title === 'Pro' ? 'text-white' : 'text-black dark:text-white'">/monthly</span>
                                        </h3>
                                        <span class="mb-20 fw-medium"
                                            :class="plan.title === 'Pro' ? 'text-white' : 'text-black dark:text-white'">What’s
                                            included</span>
                                        <ul>
                                            <li class="d-flex align-items-center gap-16 mb-16"
                                                v-for="(feature, j) in plan.features" :key="j">
                                                <span
                                                    class="w-24-px h-24-px d-flex justify-content-center align-items-center rounded-circle"
                                                    :class="plan.iconBgClass">
                                                    <iconify-icon icon="iconamoon:check-light" class="text-lg"
                                                        :class="plan.checkIconClass"></iconify-icon>
                                                </span>
                                                <span class="text-lg"
                                                    :class="plan.title === 'Pro' ? 'text-white' : 'text-black dark:text-white'">{{
                                                    feature }}</span>
                                            </li>
                                        </ul>
                                        <button type="button"
                                            class="text-center text-sm btn-sm px-12 py-10 w-100 radius-8 mt-28"
                                            :class="plan.buttonClass" data-bs-toggle="modal"
                                            data-bs-target="#exampleModal">
                                            Get started
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Yearly Tab -->
                        <div class="tab-pane fade" :class="{ 'show active': activeTab === 'yearly' }" role="tabpanel">
                            <div class="row gy-4">
                                <div class="col-xxl-4 col-sm-6 pricing-plan-wrapper" v-for="(plan, i) in yearlyPlans"
                                    :key="'y' + i">
                                    <div class="pricing-plan position-relative radius-24 overflow-hidden border"
                                        :class="plan.bgClass">
                                        <span v-if="plan.popular"
                                            class="bg-white bg-opacity-25 text-white radius-24 py-8 px-24 text-sm position-absolute end-0 top-0 z-1 rounded-start-top-0 rounded-end-bottom-0">
                                            Popular
                                        </span>
                                        <div class="d-flex align-items-center gap-16">
                                            <span
                                                class="w-72-px h-72-px d-flex justify-content-center align-items-center radius-16 bg-base">
                                                <img :src="plan.icon" alt="">
                                            </span>
                                            <div>
                                                <span class="fw-medium text-md"
                                                    :class="plan.title === 'Pro' ? 'text-white' : 'text-black dark:text-white'">{{
                                                    plan.target }}</span>
                                                <h6 class="mb-0"
                                                    :class="plan.title === 'Pro' ? 'text-white' : 'text-black dark:text-white'">
                                                    {{ plan.title }}</h6>
                                            </div>
                                        </div>
                                        <p class="mt-16 mb-0 mb-28"
                                            :class="plan.title === 'Pro' ? 'text-white' : 'text-black dark:text-white'">
                                            {{ plan.description }}</p>
                                        <h3 class="mb-24"
                                            :class="plan.title === 'Pro' ? 'text-white' : 'text-black dark:text-white'">
                                            {{ plan.price }}
                                            <span class="fw-medium text-md"
                                                :class="plan.title === 'Pro' ? 'text-white' : 'text-black dark:text-white'">/monthly</span>
                                        </h3>
                                        <span class="mb-20 fw-medium"
                                            :class="plan.title === 'Pro' ? 'text-white' : 'text-black dark:text-white'">What’s
                                            included</span>
                                        <ul>
                                            <li class="d-flex align-items-center gap-16 mb-16"
                                                v-for="(feature, j) in plan.features" :key="j">
                                                <span
                                                    class="w-24-px h-24-px d-flex justify-content-center align-items-center rounded-circle"
                                                    :class="plan.iconBgClass">
                                                    <iconify-icon icon="iconamoon:check-light" class="text-lg"
                                                        :class="plan.checkIconClass"></iconify-icon>
                                                </span>
                                                <span class="text-lg"
                                                    :class="plan.title === 'Pro' ? 'text-white' : 'text-black dark:text-white'">{{
                                                    feature }}</span>
                                            </li>
                                        </ul>
                                        <button type="button"
                                            class="text-center text-sm btn-sm px-12 py-10 w-100 radius-8 mt-28"
                                            :class="plan.buttonClass" data-bs-toggle="modal"
                                            data-bs-target="#exampleModal">
                                            Get started
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div> <!-- tab-content end -->
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import priceIcon1 from '@/assets/images/pricing/price-icon1.png'
import priceIcon2 from '@/assets/images/pricing/price-icon2.png'
import priceIcon3 from '@/assets/images/pricing/price-icon3.png'
export default {
    name: 'PricingPlans',
    data() {
        return {
            activeTab: 'monthly',
            monthlyPlans: [
                {
                    title: 'Basic',
                    target: 'For individuals',
                    price: '$99',
                    icon: priceIcon1,
                    description: 'Lorem ipsum dolor sit amet doloroli sitiol conse ctetur adipiscing elit.',
                    bgClass: 'bg-lilac-100',
                    iconBgClass: 'bg-lilac-600',
                    textClass: 'text-secondary-light',
                    buttonClass: 'bg-lilac-600 bg-hover-lilac-700 text-white border border-lilac-600',
                    checkIconClass: 'text-white',
                    features: ['All analytics features', 'Up to 250,000 tracked visits', 'Normal support', 'Up to 3 team members']
                },
                {
                    title: 'Pro',
                    target: 'For startups',
                    price: '$199',
                    icon: priceIcon2,
                    description: 'Lorem ipsum dolor sit amet doloroli sitiol conse ctetur adipiscing elit.',
                    popular: true,
                    bgClass: 'bg-primary-600 text-white scale-item',
                    iconBgClass: 'bg-white',
                    textClass: 'text-white',
                    buttonClass: 'bg-white text-primary-600 border border-white',
                    checkIconClass: 'text-primary-600',
                    features: ['All analytics features', 'Up to 250,000 tracked visits', 'Normal support', 'Up to 3 team members']
                },
                {
                    title: 'Enterprise',
                    target: 'For big companies',
                    price: '$399',
                    icon: priceIcon3,
                    description: 'Lorem ipsum dolor sit amet doloroli sitiol conse ctetur adipiscing elit.',
                    bgClass: 'bg-success-100',
                    iconBgClass: 'bg-success-600',
                    textClass: 'text-secondary-light',
                    buttonClass: 'bg-success-600 bg-hover-success-700 text-white border border-success-600',
                    checkIconClass: 'text-white',
                    features: ['All analytics features', 'Up to 250,000 tracked visits', 'Normal support', 'Up to 3 team members']
                }
            ],
            yearlyPlans: [
                {
                    title: 'Basic',
                    target: 'For individuals',
                    price: '$399',
                    icon: priceIcon1,
                    description: 'Lorem ipsum dolor sit amet doloroli sitiol conse ctetur adipiscing elit.',
                    bgClass: 'bg-lilac-100',
                    iconBgClass: 'bg-lilac-600',
                    textClass: 'text-secondary-light',
                    buttonClass: 'bg-lilac-600 bg-hover-lilac-700 text-white border border-lilac-600',
                    checkIconClass: 'text-white',
                    features: ['All analytics features', 'Up to 250,000 tracked visits', 'Normal support', 'Up to 3 team members']
                },
                {
                    title: 'Pro',
                    target: 'For startups',
                    price: '$699',
                    icon: priceIcon2,
                    description: 'Lorem ipsum dolor sit amet doloroli sitiol conse ctetur adipiscing elit.',
                    popular: true,
                    bgClass: 'bg-primary-600 text-white scale-item',
                    iconBgClass: 'bg-white',
                    textClass: 'text-white',
                    buttonClass: 'bg-white text-primary-600 border border-white',
                    checkIconClass: 'text-primary-600',
                    features: ['All analytics features', 'Up to 250,000 tracked visits', 'Normal support', 'Up to 3 team members']
                },
                {
                    title: 'Enterprise',
                    target: 'For big companies',
                    price: '$999',
                    icon: priceIcon3,
                    description: 'Lorem ipsum dolor sit amet doloroli sitiol conse ctetur adipiscing elit.',
                    bgClass: 'bg-success-100',
                    iconBgClass: 'bg-success-600',
                    textClass: 'text-secondary-light',
                    buttonClass: 'bg-success-600 bg-hover-success-700 text-white border border-success-600',
                    checkIconClass: 'text-white',
                    features: ['All analytics features', 'Up to 250,000 tracked visits', 'Normal support', 'Up to 3 team members']
                }
            ]
        };
    }
};
</script>