<template>
    <div class="dashboard-main-body">

        <Breadcrumb title="Finance & Banking" :breadcrumbs="[
            { name: 'Finance & Banking' }
        ]" />

        <!-- Widgets start -->
        <FinanceWidget />
        <!-- Widgets end -->

        <div class="mt-24">
            <div class="row gy-4">
                <div class="col-xl-8">
                    <div class="row gy-4">
                        <BalanceStatistic />
                        <EarningCategories />
                        <ExpenseStatistics />
                        <PaymentHistory />
                        <MonthlyExpenseBreakdown />
                    </div>
                </div>

                <!-- Sidebar start -->
                <div class="col-xl-4">
                    <QuickTransfer />
                    <!-- <div class="card radius-16">
                        <div class="card-header">
                            <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
                                <h6 class="mb-2 fw-bold text-lg mb-0">Quick Transfer</h6>
                            </div>
                        </div>
                        <div class="card-body p-0">
                            <div class="p-20">
                                <div class="position-relative z-1 py-32 text-center px-3">
                                    <img src="@/assets/images/home-eleven/bg/bg-orange-gradient.png" alt=""
                                        class="position-absolute top-0 start-0 w-100 h-100 z-n1">
                                    <h3 class="text-white">$500.00</h3>
                                    <span class="text-white">Your Balance</span>
                                </div>
                            </div>

                            <div class="px-24 bg-neutral-100 border-bottom-0 py-20 dark-bg-neutral-200">
                                <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between">
                                    <h6 class="mb-2 fw-bold text-lg mb-0">Contacts</h6>
                                    <a href="javascript:void(0)"
                                        class="text-primary-600 hover-text-primary d-flex align-items-center gap-1">
                                        View All
                                        <iconify-icon icon="solar:alt-arrow-right-linear" class="icon"></iconify-icon>
                                    </a>
                                </div>
                            </div>

                            <div class="py-16 px-24">
                                <div class="officer-slider">
                                    <div
                                        class="officer-slider__item d-flex flex-column text-center align-items-center justify-content-center">
                                        <div
                                            class="officer-slider__thumb w-56-px h-56-px rounded-circle overflow-hidden flex-shrink-0 mx-8">
                                            <img src="@/assets/images/home-eleven/officer-img1.png" alt=""
                                                class="w-100 h-100 object-fit-cover">
                                        </div>
                                        <div class="officer-slider__content mt-24 min-w-max-content">
                                            <h6 class="mb-0 text-xl">Mr. Bin</h6>
                                            <span class="text-sm text-secondary-light">Insurance officer</span>
                                        </div>
                                    </div>
                                    <div
                                        class="officer-slider__item d-flex flex-column text-center align-items-center justify-content-center">
                                        <div
                                            class="officer-slider__thumb w-56-px h-56-px rounded-circle overflow-hidden flex-shrink-0 mx-8">
                                            <img src="@/assets/images/home-eleven/officer-img2.png" alt=""
                                                class="w-100 h-100 object-fit-cover">
                                        </div>
                                        <div class="officer-slider__content mt-24 min-w-max-content">
                                            <h6 class="mb-0 text-xl">Mr. Robiul</h6>
                                            <span class="text-sm text-secondary-light">Insurance officer</span>
                                        </div>
                                    </div>
                                    <div
                                        class="officer-slider__item d-flex flex-column text-center align-items-center justify-content-center">
                                        <div
                                            class="officer-slider__thumb w-56-px h-56-px rounded-circle overflow-hidden flex-shrink-0 mx-8">
                                            <img src="@/assets/images/home-eleven/officer-img3.png" alt=""
                                                class="w-100 h-100 object-fit-cover">
                                        </div>
                                        <div class="officer-slider__content mt-24 min-w-max-content">
                                            <h6 class="mb-0 text-xl">Mr. Deo</h6>
                                            <span class="text-sm text-secondary-light">Insurance officer</span>
                                        </div>
                                    </div>
                                    <div
                                        class="officer-slider__item d-flex flex-column text-center align-items-center justify-content-center">
                                        <div
                                            class="officer-slider__thumb w-56-px h-56-px rounded-circle overflow-hidden flex-shrink-0 mx-8">
                                            <img src="@/assets/images/home-eleven/officer-img4.png" alt=""
                                                class="w-100 h-100 object-fit-cover">
                                        </div>
                                        <div class="officer-slider__content mt-24 min-w-max-content">
                                            <h6 class="mb-0 text-xl">Mr. Riad</h6>
                                            <span class="text-sm text-secondary-light">Insurance officer</span>
                                        </div>
                                    </div>
                                    <div
                                        class="officer-slider__item d-flex flex-column text-center align-items-center justify-content-center">
                                        <div
                                            class="officer-slider__thumb w-56-px h-56-px rounded-circle overflow-hidden flex-shrink-0 mx-8">
                                            <img src="@/assets/images/home-eleven/officer-img5.png" alt=""
                                                class="w-100 h-100 object-fit-cover">
                                        </div>
                                        <div class="officer-slider__content mt-24 min-w-max-content">
                                            <h6 class="mb-0 text-xl">Mr. Alex</h6>
                                            <span class="text-sm text-secondary-light">Insurance officer</span>
                                        </div>
                                    </div>
                                    <div
                                        class="officer-slider__item d-flex flex-column text-center align-items-center justify-content-center">
                                        <div
                                            class="officer-slider__thumb w-56-px h-56-px rounded-circle overflow-hidden flex-shrink-0 mx-8">
                                            <img src="@/assets/images/home-eleven/officer-img2.png" alt=""
                                                class="w-100 h-100 object-fit-cover">
                                        </div>
                                        <div class="officer-slider__content mt-24 min-w-max-content">
                                            <h6 class="mb-0 text-xl">Mr. John</h6>
                                            <span class="text-sm text-secondary-light">Insurance officer</span>
                                        </div>
                                    </div>
                                </div>

                                <form action="#">
                                    <div class="">
                                        <label for="message" class="d-block fw-semibold text-primary-light mb-8">Write
                                            Short
                                            Description </label>
                                        <textarea class="form-control" id="message" rows="4" cols="50"
                                            placeholder="Enter a description..."></textarea>
                                    </div>
                                    <div class="mt-16">
                                        <label for="Amount"
                                            class="d-block fw-semibold text-primary-light mb-8">Amount</label>
                                        <div class="d-flex gap-16">
                                            <input type="text" id="Amount" class="form-control form-control-lg"
                                                placeholder="Ex: $200">
                                            <button
                                                class="btn btn-primary-600 flex-shrink-0 d-flex align-items-center gap-2 px-32"
                                                type="submit">Send <i class="ri-send-plane-fill"></i> </button>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div> -->
                    <Investment />
                </div>
                <!-- Sidebar end -->

            </div>
        </div>

        <!-- Table Start -->
        <UserPaymentHistory />
        <!-- Table End -->

    </div>
</template>

<script>
import Breadcrumb from '@/components/breadcrumb/Breadcrumb.vue';
import ApexCharts from "vue3-apexcharts";
import { Icon } from "@iconify/vue"; 
import FinanceWidget from "@/components/dashboard/FinanceBanking/FinanceWidget.vue"
import BalanceStatistic from "@/components/dashboard/FinanceBanking/BalanceStatistic.vue"
import EarningCategories from "@/components/dashboard/FinanceBanking/EarningCategories.vue"
import ExpenseStatistics from "@/components/dashboard/FinanceBanking/ExpenseStatistics.vue"
import PaymentHistory from "@/components/dashboard/FinanceBanking/PaymentHistory.vue"
import MonthlyExpenseBreakdown from "@/components/dashboard/FinanceBanking/MonthlyExpense.vue"
import QuickTransfer from "@/components/dashboard/FinanceBanking/QuickTransfer.vue"
import Investment from "@/components/dashboard/FinanceBanking/Investment.vue"
import UserPaymentHistory from "@/components/dashboard/FinanceBanking/UserPaymentHistory.vue"

export default {
  name: "Lms",
  components: {
    Breadcrumb,
    apexchart: ApexCharts,
    Icon,
    FinanceWidget,
    BalanceStatistic,
    EarningCategories,
    ExpenseStatistics,
    PaymentHistory,
    MonthlyExpenseBreakdown,
    QuickTransfer,
    Investment,
    UserPaymentHistory
  },
};
</script>