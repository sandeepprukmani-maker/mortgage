<template>
    <div class="col-xxl-6 col-xl-6">
        <div class="card h-100 border shadow-none">
            <div class="card-body">
                <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between mb-20">
                    <h6 class="mb-2 fw-bold text-lg mb-0">Top Countries</h6>
                    <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
                        <option>Today</option>
                        <option>Weekly</option>
                        <option>Monthly</option>
                        <option>Yearly</option>
                    </select>
                </div>

                <div class="row gy-4">
                    <div class="col-sm-6">
                        <div id="world-map" class="h-100 border radius-8"></div>
                    </div>

                    <div class="col-sm-6">
                        <div class="h-100 border p-16 pe-0 radius-8">
                            <div class="max-h-266-px overflow-y-auto scroll-sm pe-16">
                                <div class="d-flex align-items-center justify-content-between gap-3 mb-12 pb-2">
                                    <div class="d-flex align-items-center w-100">
                                        <img src="@/assets/images/flags/flag1.png" alt=""
                                            class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12">
                                        <div class="flex-grow-1">
                                            <h6 class="text-sm mb-0">USA</h6>
                                            <span class="text-xs text-secondary-light fw-medium">1,240 Users</span>
                                        </div>
                                    </div>
                                    <div class="d-flex align-items-center gap-2 w-100">
                                        <div class="w-100 max-w-66 ms-auto">
                                            <div class="progress progress-sm rounded-pill" role="progressbar"
                                                aria-label="Success example" aria-valuenow="25" aria-valuemin="0"
                                                aria-valuemax="100">
                                                <div class="progress-bar bg-primary-600 rounded-pill"
                                                    style="width: 80%;"></div>
                                            </div>
                                        </div>
                                        <span class="text-secondary-light font-xs fw-semibold">80%</span>
                                    </div>
                                </div>

                                <div class="d-flex align-items-center justify-content-between gap-3 mb-12 pb-2">
                                    <div class="d-flex align-items-center w-100">
                                        <img src="@/assets/images/flags/flag2.png" alt=""
                                            class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12">
                                        <div class="flex-grow-1">
                                            <h6 class="text-sm mb-0">Japan</h6>
                                            <span class="text-xs text-secondary-light fw-medium">1,240 Users</span>
                                        </div>
                                    </div>
                                    <div class="d-flex align-items-center gap-2 w-100">
                                        <div class="w-100 max-w-66 ms-auto">
                                            <div class="progress progress-sm rounded-pill" role="progressbar"
                                                aria-label="Success example" aria-valuenow="25" aria-valuemin="0"
                                                aria-valuemax="100">
                                                <div class="progress-bar bg-orange rounded-pill" style="width: 60%;">
                                                </div>
                                            </div>
                                        </div>
                                        <span class="text-secondary-light font-xs fw-semibold">60%</span>
                                    </div>
                                </div>

                                <div class="d-flex align-items-center justify-content-between gap-3 mb-12 pb-2">
                                    <div class="d-flex align-items-center w-100">
                                        <img src="@/assets/images/flags/flag3.png" alt=""
                                            class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12">
                                        <div class="flex-grow-1">
                                            <h6 class="text-sm mb-0">France</h6>
                                            <span class="text-xs text-secondary-light fw-medium">1,240 Users</span>
                                        </div>
                                    </div>
                                    <div class="d-flex align-items-center gap-2 w-100">
                                        <div class="w-100 max-w-66 ms-auto">
                                            <div class="progress progress-sm rounded-pill" role="progressbar"
                                                aria-label="Success example" aria-valuenow="25" aria-valuemin="0"
                                                aria-valuemax="100">
                                                <div class="progress-bar bg-yellow rounded-pill" style="width: 49%;">
                                                </div>
                                            </div>
                                        </div>
                                        <span class="text-secondary-light font-xs fw-semibold">49%</span>
                                    </div>
                                </div>

                                <div class="d-flex align-items-center justify-content-between gap-3 mb-12 pb-2">
                                    <div class="d-flex align-items-center w-100">
                                        <img src="@/assets/images/flags/flag4.png" alt=""
                                            class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12">
                                        <div class="flex-grow-1">
                                            <h6 class="text-sm mb-0">Germany</h6>
                                            <span class="text-xs text-secondary-light fw-medium">1,240 Users</span>
                                        </div>
                                    </div>
                                    <div class="d-flex align-items-center gap-2 w-100">
                                        <div class="w-100 max-w-66 ms-auto">
                                            <div class="progress progress-sm rounded-pill" role="progressbar"
                                                aria-label="Success example" aria-valuenow="25" aria-valuemin="0"
                                                aria-valuemax="100">
                                                <div class="progress-bar bg-success-main rounded-pill"
                                                    style="width: 100%;"></div>
                                            </div>
                                        </div>
                                        <span class="text-secondary-light font-xs fw-semibold">100%</span>
                                    </div>
                                </div>

                                <div class="d-flex align-items-center justify-content-between gap-3 mb-12 pb-2">
                                    <div class="d-flex align-items-center w-100">
                                        <img src="@/assets/images/flags/flag5.png" alt=""
                                            class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12">
                                        <div class="flex-grow-1">
                                            <h6 class="text-sm mb-0">South Korea</h6>
                                            <span class="text-xs text-secondary-light fw-medium">1,240 Users</span>
                                        </div>
                                    </div>
                                    <div class="d-flex align-items-center gap-2 w-100">
                                        <div class="w-100 max-w-66 ms-auto">
                                            <div class="progress progress-sm rounded-pill" role="progressbar"
                                                aria-label="Success example" aria-valuenow="25" aria-valuemin="0"
                                                aria-valuemax="100">
                                                <div class="progress-bar bg-info-main rounded-pill" style="width: 30%;">
                                                </div>
                                            </div>
                                        </div>
                                        <span class="text-secondary-light font-xs fw-semibold">30%</span>
                                    </div>
                                </div>
                                <div class="d-flex align-items-center justify-content-between gap-3">
                                    <div class="d-flex align-items-center w-100">
                                        <img src="@/assets/images/flags/flag1.png" alt=""
                                            class="w-40-px h-40-px rounded-circle flex-shrink-0 me-12">
                                        <div class="flex-grow-1">
                                            <h6 class="text-sm mb-0">USA</h6>
                                            <span class="text-xs text-secondary-light fw-medium">1,240 Users</span>
                                        </div>
                                    </div>
                                    <div class="d-flex align-items-center gap-2 w-100">
                                        <div class="w-100 max-w-66 ms-auto">
                                            <div class="progress progress-sm rounded-pill" role="progressbar"
                                                aria-label="Success example" aria-valuenow="25" aria-valuemin="0"
                                                aria-valuemax="100">
                                                <div class="progress-bar bg-primary-600 rounded-pill"
                                                    style="width: 80%;"></div>
                                            </div>
                                        </div>
                                        <span class="text-secondary-light font-xs fw-semibold">80%</span>
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