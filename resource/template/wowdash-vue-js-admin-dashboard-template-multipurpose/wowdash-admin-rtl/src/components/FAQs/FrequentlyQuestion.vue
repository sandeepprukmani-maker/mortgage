<template>
    <div class="card basic-data-table">
        <div class="card-header p-0 border-0">
            <div class="responsive-padding-40-150 bg-light-pink">
                <div class="row gy-4 align-items-center">
                    <div class="col-xl-7">
                        <h4 class="mb-20">Frequently asked questions.</h4>
                        <p class="mb-0 text-secondary-light max-w-634-px text-xl">Lorem Ipsum is simply dummy text of
                            the printing and typesetting industry. Lorem Ipsum has been the industry's standard du text
                            ever since the 1500s, when an unkn</p>
                    </div>
                    <div class="col-xl-5 d-xl-block d-none">
                        <img src="@/assets/images/faq-img.png" alt="">
                    </div>
                </div>
            </div>
        </div>
        <div class="card-body bg-base responsive-padding-40-150">
            <div class="row gy-4">
                <div class="col-lg-4">
                    <div class="active-text-tab nav flex-column nav-pills bg-base shadow py-0 px-24 radius-12 border"
                        id="v-pills-tab" role="tablist" aria-orientation="vertical">
                        <button
                            class="nav-link text-secondary-light fw-semibold text-xl px-0 py-16 border-bottom active"
                            id="v-pills-about-us-tab" data-bs-toggle="pill" data-bs-target="#v-pills-about-us"
                            type="button" role="tab" aria-controls="v-pills-about-us" aria-selected="true">About
                            Us</button>
                        <button class="nav-link text-secondary-light fw-semibold text-xl px-0 py-16 border-bottom"
                            id="v-pills-ux-ui-tab" data-bs-toggle="pill" data-bs-target="#v-pills-ux-ui" type="button"
                            role="tab" aria-controls="v-pills-ux-ui" aria-selected="false">UX UI Design</button>
                        <button class="nav-link text-secondary-light fw-semibold text-xl px-0 py-16 border-bottom"
                            id="v-pills-development-tab" data-bs-toggle="pill" data-bs-target="#v-pills-development"
                            type="button" role="tab" aria-controls="v-pills-development"
                            aria-selected="false">Development</button>
                        <button class="nav-link text-secondary-light fw-semibold text-xl px-0 py-16 border-bottom"
                            id="v-pills-use-case-tab" data-bs-toggle="pill" data-bs-target="#v-pills-use-case"
                            type="button" role="tab" aria-controls="v-pills-use-case" aria-selected="false">How to can i
                            use WowDash?
                        </button>
                        <button class="nav-link text-secondary-light fw-semibold text-xl px-0 py-16"
                            id="v-pills-use-agency-tab" data-bs-toggle="pill" data-bs-target="#v-pills-use-agency"
                            type="button" role="tab" aria-controls="v-pills-use-agency" aria-selected="false">Can I use
                            my
                            agency?</button>
                    </div>
                </div>
                <div class="col-lg-8">
                    <div class="tab-content" id="v-pills-tabContent">
                        <div class="tab-pane fade show active" id="v-pills-about-us" role="tabpanel"
                            aria-labelledby="v-pills-about-us-tab" tabindex="0">
                            <div class="accordion" id="accordionExample">
                                <div class="accordion-item" v-for="(item, index) in AbotUs" :key="index">
                                    <h2 class="accordion-header">
                                        <button class="accordion-button text-primary-light text-xl" type="button"
                                            :data-bs-toggle="'collapse'" :data-bs-target="'#collapse' + (index + 1)"
                                            :aria-expanded="index === 0 ? 'true' : 'false'"
                                            :aria-controls="'collapse' + (index + 1)">
                                            {{ item.question }}
                                        </button>
                                    </h2>
                                    <div :id="'collapse' + (index + 1)" class="accordion-collapse collapse"
                                        :class="{ show: index === 0 }" :data-bs-parent="'#accordionExample'">
                                        <div class="accordion-body">
                                            {{ item.answer }}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="tab-pane fade" id="v-pills-ux-ui" role="tabpanel"
                            aria-labelledby="v-pills-ux-ui-tab" tabindex="0">
                            <div class="accordion" id="accordionExampleTwo">
                                <div class="accordion-item" v-for="(item, index) in UiUxDesign" :key="index">
                                    <h2 class="accordion-header">
                                        <button class="accordion-button text-primary-light text-xl" type="button"
                                            :data-bs-toggle="'collapse'" :data-bs-target="'#c-' + (index + 1)"
                                            :aria-expanded="index === 0 ? 'true' : 'false'"
                                            :aria-controls="'c-' + (index + 1)">
                                            {{ item.question }}
                                        </button>
                                    </h2>
                                    <div :id="'c-' + (index + 1)" class="accordion-collapse collapse"
                                        :class="{ show: index === 0 }" :data-bs-parent="'#accordionExampleTwo'">
                                        <div class="accordion-body">
                                            {{ item.answer }}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="tab-pane fade" id="v-pills-development" role="tabpanel"
                            aria-labelledby="v-pills-development-tab" tabindex="0">
                            <div class="accordion" id="accordionExampleThree">
                                <div class="accordion-item" v-for="(item, index) in Development" :key="index">
                                    <h2 class="accordion-header">
                                        <button class="accordion-button text-primary-light text-xl" type="button"
                                            :data-bs-toggle="'collapse'" :data-bs-target="'#c-' + (index + 7)"
                                            :aria-expanded="index === 0 ? 'true' : 'false'"
                                            :aria-controls="'c-' + (index + 7)">
                                            {{ item.question }}
                                        </button>
                                    </h2>
                                    <div :id="'c-' + (index + 7)" class="accordion-collapse collapse"
                                        :class="{ show: index === 0 }" :data-bs-parent="'#accordionExampleThree'">
                                        <div class="accordion-body">
                                            {{ item.answer }}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="tab-pane fade" id="v-pills-use-case" role="tabpanel"
                            aria-labelledby="v-pills-use-case-tab" tabindex="0">
                            <div class="accordion" id="accordionExampleFour">
                                <div class="accordion-item" v-for="(item, index) in WowDash" :key="index">
                                    <h2 class="accordion-header">
                                        <button class="accordion-button text-primary-light text-xl" type="button"
                                            :data-bs-toggle="'collapse'" :data-bs-target="'#c-' + (index + 13)"
                                            :aria-expanded="index === 0 ? 'true' : 'false'"
                                            :aria-controls="'c-' + (index + 13)">
                                            {{ item.question }}
                                        </button>
                                    </h2>
                                    <div :id="'c-' + (index + 13)" class="accordion-collapse collapse"
                                        :class="{ show: index === 0 }" :data-bs-parent="'#accordionExampleFour'">
                                        <div class="accordion-body">
                                            {{ item.answer }}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="tab-pane fade" id="v-pills-use-agency" role="tabpanel"
                            aria-labelledby="v-pills-use-agency-tab" tabindex="0">
                            <div class="accordion" id="accordionExampleFIve">
                                <div class="accordion-item" v-for="(item, index) in agency" :key="index">
                                    <h2 class="accordion-header">
                                        <button class="accordion-button text-primary-light text-xl" type="button"
                                            :data-bs-toggle="'collapse'" :data-bs-target="'#c-' + (index + 19)"
                                            :aria-expanded="index === 0 ? 'true' : 'false'"
                                            :aria-controls="'c-' + (index + 19)">
                                            {{ item.question }}
                                        </button>
                                    </h2>
                                    <div :id="'c-' + (index + 19)" class="accordion-collapse collapse"
                                        :class="{ show: index === 0 }" :data-bs-parent="'#accordionExampleFIve'">
                                        <div class="accordion-body">
                                            {{ item.answer }}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            AbotUs: [
                {
                    question: "Is there a free trial available?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "Can I change my plan later?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "What is your cancellation policy?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "Can other info be added to an invoice?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "How does billing work?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "How do I change my account email?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
            ],
            UiUxDesign: [
                {
                    question: "Is there a free trial available?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "Can I change my plan later?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "What is your cancellation policy?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "Can other info be added to an invoice?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "How does billing work?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "How do I change my account email?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
            ],
            Development: [
                {
                    question: "Is there a free trial available?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "Can I change my plan later?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "What is your cancellation policy?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "Can other info be added to an invoice?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "How does billing work?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "How do I change my account email?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
            ],
            WowDash: [
                {
                    question: "Is there a free trial available?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "Can I change my plan later?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "What is your cancellation policy?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "Can other info be added to an invoice?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "How does billing work?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "How do I change my account email?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
            ],
            agency: [
                {
                    question: "Is there a free trial available?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "Can I change my plan later?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "What is your cancellation policy?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "Can other info be added to an invoice?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "How does billing work?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
                {
                    question: "How do I change my account email?",
                    answer:
                        "Yes, you can try us for free for 30 days. If you want, we’ll provide you with a free, personalized 30-minute onboarding call to get you up and running as soon as possible.",
                },
            ],
        };
    },
};
</script>
