<template>
    <div class="row gy-4">
        <!-- Default Alerts -->
        <div class="col-lg-6">
            <div class="card h-100 p-0">
                <div class="card-header border-bottom bg-base py-16 px-24">
                    <h6 class="text-lg fw-semibold mb-0">Default Alerts</h6>
                </div>
                <div class="card-body p-24 d-flex flex-column gap-4">
                    <!-- Primary Alert -->
                    <div v-if="primaryVisible"
                        class="alert alert-primary bg-primary-50 text-primary-600 border-primary-50 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                        role="alert">
                        This is a Primary alert
                        <button @click="removeAlert('primary')"
                            class="remove-button text-primary-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>

                    <!-- Secondary Alert -->
                    <div v-if="secondaryVisible"
                        class="alert alert-lilac bg-lilac-50 text-lilac-600 border-lilac-50 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                        role="alert">
                        This is a Secondary alert
                        <button @click="removeAlert('secondary')"
                            class="remove-button text-lilac-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>

                    <!-- Warning Alert -->
                    <div v-if="warningVisible"
                        class="alert alert-warning bg-warning-100 text-warning-600 border-warning-100 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                        role="alert">
                        This is a Warning alert
                        <button @click="removeAlert('warning')"
                            class="remove-button text-warning-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>

                    <!-- Info Alert -->
                    <div v-if="infoVisible"
                        class="alert alert-info bg-info-100 text-info-600 border-info-100 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                        role="alert">
                        This is a Info alert
                        <button @click="removeAlert('info')" class="remove-button text-info-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>

                    <!-- Danger Alert -->
                    <div v-if="dangerVisible"
                        class="alert alert-danger bg-danger-100 text-danger-600 border-danger-100 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                        role="alert">
                        This is a Danger alert
                        <button @click="removeAlert('danger')"
                            class="remove-button text-danger-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Outline Alerts -->
        <div class="col-lg-6">
            <div class="card h-100 p-0">
                <div class="card-header border-bottom bg-base py-16 px-24">
                    <h6 class="text-lg fw-semibold mb-0">Outline Alerts</h6>
                </div>
                <div class="card-body p-24 d-flex flex-column gap-4">
                    <div v-if="outlinePrimaryVisible"
                        class="alert alert-primary bg-transparent text-primary-600 border-primary-600 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                        role="alert">
                        This is a Primary alert
                        <button @click="removeOutlineAlert('outlinePrimary')"
                            class="remove-button text-primary-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>

                    <div v-if="outlineSecondaryVisible"
                        class="alert alert-lilac bg-transparent text-lilac-600 border-lilac-600 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                        role="alert">
                        This is a Secondary alert
                        <button @click="removeOutlineAlert('outlineSecondary')"
                            class="remove-button text-lilac-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>

                    <div v-if="outlineWarningVisible"
                        class="alert alert-warning bg-transparent text-warning-600 border-warning-600 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                        role="alert">
                        This is a Warning alert
                        <button @click="removeOutlineAlert('outlineWarning')"
                            class="remove-button text-warning-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>

                    <div v-if="outlineInfoVisible"
                        class="alert alert-info bg-transparent text-info-600 border-info-600 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                        role="alert">
                        This is a Info alert
                        <button @click="removeOutlineAlert('outlineInfo')"
                            class="remove-button text-info-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>

                    <div v-if="outlineDangerVisible"
                        class="alert alert-danger bg-transparent text-danger-600 border-danger-600 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                        role="alert">
                        This is a Danger alert
                        <button @click="removeOutlineAlert('outlineDanger')"
                            class="remove-button text-danger-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Solid Alerts -->
        <div class="col-xl-12">
            <div class="card h-100 p-0">
                <div class="card-header border-bottom bg-base py-16 px-24">
                    <h6 class="text-lg fw-semibold mb-0">Solid Alerts</h6>
                </div>
                <div class="card-body p-24">
                    <div class="row gy-4">
                        <div class="col-sm-6">
                            <div class="d-flex flex-column gap-4">
                                <!-- Solid Primary Alert -->
                                <div v-if="solidPrimaryVisible"
                                    class="alert alert-primary bg-primary-600 text-white border-primary-600 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                                    role="alert">
                                    This is a Primary alert
                                    <button @click="removeSolidAlert('solidPrimary')"
                                        class="remove-button text-white text-xxl line-height-1">
                                        <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                                    </button>
                                </div>

                                <!-- Solid Success Alert -->
                                <div v-if="solidSuccessVisible"
                                    class="alert alert-success bg-success-600 text-white border-success-600 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                                    role="alert">
                                    This is a Success alert
                                    <button @click="removeSolidAlert('solidSuccess')"
                                        class="remove-button text-white text-xxl line-height-1">
                                        <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                                    </button>
                                </div>

                                <!-- Solid Info Alert -->
                                <div v-if="solidInfoVisible"
                                    class="alert alert-info bg-info-600 text-white border-info-600 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                                    role="alert">
                                    This is a Info alert
                                    <button @click="removeSolidAlert('solidInfo')"
                                        class="remove-button text-white text-xxl line-height-1">
                                        <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <div class="col-sm-6">
                            <div class="d-flex flex-column gap-4">
                                <!-- Solid Secondary Alert -->
                                <div v-if="solidSecondaryVisible"
                                    class="alert alert-lilac bg-lilac-600 text-white border-lilac-600 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                                    role="alert">
                                    This is a Secondary alert
                                    <button @click="removeSolidAlert('solidSecondary')"
                                        class="remove-button text-white text-xxl line-height-1">
                                        <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                                    </button>
                                </div>

                                <!-- Solid Warning Alert -->
                                <div v-if="solidWarningVisible"
                                    class="alert alert-warning bg-warning-600 text-white border-warning-600 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                                    role="alert">
                                    This is a Warning alert
                                    <button @click="removeSolidAlert('solidWarning')"
                                        class="remove-button text-white text-xxl line-height-1">
                                        <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                                    </button>
                                </div>

                                <!-- Solid Danger Alert -->
                                <div v-if="solidDangerVisible"
                                    class="alert alert-danger bg-danger-600 text-white border-danger-600 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                                    role="alert">
                                    This is a Danger alert
                                    <button @click="removeSolidAlert('solidDanger')"
                                        class="remove-button text-white text-xxl line-height-1">
                                        <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Outline Alerts -->
        <div class="col-lg-6">
            <div class="card h-100 p-0">
                <div class="card-header border-bottom bg-base py-16 px-24">
                    <h6 class="text-lg fw-semibold mb-0">Outline Alerts</h6>
                </div>
                <div class="card-body p-24 d-flex flex-column gap-4">
                    <!-- Primary Alert -->
                    <div v-if="outlinePrimaryVisible"
                        class="alert alert-primary bg-primary-50 text-primary-600 border-primary-50 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                        role="alert">
                        <div class="d-flex align-items-center gap-2">
                            <iconify-icon icon="mingcute:emoji-line" class="icon text-xl"></iconify-icon>
                            This is a Primary alert
                        </div>
                        <button @click="removeOutlineAlert('outlinePrimary')"
                            class="remove-button text-primary-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>

                    <!-- Secondary Alert -->
                    <div v-if="outlineSecondaryVisible"
                        class="alert alert-lilac bg-lilac-50 text-lilac-600 border-lilac-50 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                        role="alert">
                        <div class="d-flex align-items-center gap-2">
                            <iconify-icon icon="mingcute:emoji-line" class="icon text-xl"></iconify-icon>
                            This is a Secondary alert
                        </div>
                        <button @click="removeOutlineAlert('outlineSecondary')"
                            class="remove-button text-lilac-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>

                    <!-- Success Alert -->
                    <div v-if="outlineSuccessVisible"
                        class="alert alert-success bg-success-100 text-success-600 border-success-100 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                        role="alert">
                        <div class="d-flex align-items-center gap-2">
                            <iconify-icon icon="akar-icons:double-check" class="icon text-xl"></iconify-icon>
                            This is a Success alert
                        </div>
                        <button @click="removeOutlineAlert('outlineSuccess')"
                            class="remove-button text-success-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>

                    <!-- Warning Alert -->
                    <div v-if="outlineWarningVisible"
                        class="alert alert-warning bg-warning-100 text-warning-600 border-warning-100 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                        role="alert">
                        <div class="d-flex align-items-center gap-2">
                            <iconify-icon icon="mdi:alert-circle-outline" class="icon text-xl"></iconify-icon>
                            This is a Warning alert
                        </div>
                        <button @click="removeOutlineAlert('outlineWarning')"
                            class="remove-button text-warning-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>

                    <!-- Info Alert -->
                    <div v-if="outlineInfoVisible"
                        class="alert alert-info bg-info-100 text-info-600 border-info-100 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                        role="alert">
                        <div class="d-flex align-items-center gap-2">
                            <iconify-icon icon="ci:link" class="icon text-xl"></iconify-icon>
                            This is a Info alert
                        </div>
                        <button @click="removeOutlineAlert('outlineInfo')"
                            class="remove-button text-info-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>

                    <!-- Danger Alert -->
                    <div v-if="outlineDangerVisible"
                        class="alert alert-danger bg-danger-100 text-danger-600 border-danger-100 px-24 py-11 mb-0 fw-semibold text-lg radius-8 d-flex align-items-center justify-content-between"
                        role="alert">
                        <div class="d-flex align-items-center gap-2">
                            <iconify-icon icon="mingcute:delete-2-line" class="icon text-xl"></iconify-icon>
                            This is a Danger alert
                        </div>
                        <button @click="removeOutlineAlert('outlineDanger')"
                            class="remove-button text-danger-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Left Border Alerts -->
        <div class="col-lg-6">
            <div class="card h-100 p-0">
                <div class="card-header border-bottom bg-base py-16 px-24">
                    <h6 class="text-lg fw-semibold mb-0">Left Border Alerts</h6>
                </div>
                <div class="card-body p-24 d-flex flex-column gap-4">
                    <!-- Primary Alert -->
                    <div v-if="leftBorderPrimaryVisible"
                        class="alert alert-primary bg-primary-50 text-primary-600 border-primary-600 border-start-width-4-px border-top-0 border-end-0 border-bottom-0 px-24 py-13 mb-0 fw-semibold text-lg radius-4 d-flex align-items-center justify-content-between"
                        role="alert">
                        <div class="d-flex align-items-center gap-2">
                            <iconify-icon icon="mingcute:emoji-line" class="icon text-xl"></iconify-icon>
                            This is a Primary alert
                        </div>
                        <button @click="removeLeftBorderAlert('leftBorderPrimary')"
                            class="remove-button text-primary-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>

                    <!-- Secondary Alert -->
                    <div v-if="leftBorderSecondaryVisible"
                        class="alert alert-lilac bg-lilac-50 text-lilac-600 border-lilac-600 border-start-width-4-px border-top-0 border-end-0 border-bottom-0 px-24 py-13 mb-0 fw-semibold text-lg radius-4 d-flex align-items-center justify-content-between"
                        role="alert">
                        <div class="d-flex align-items-center gap-2">
                            <iconify-icon icon="mingcute:emoji-line" class="icon text-xl"></iconify-icon>
                            This is a Secondary alert
                        </div>
                        <button @click="removeLeftBorderAlert('leftBorderSecondary')"
                            class="remove-button text-lilac-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>

                    <!-- Success Alert -->
                    <div v-if="leftBorderSuccessVisible"
                        class="alert alert-success bg-success-100 text-success-600 border-success-600 border-start-width-4-px border-top-0 border-end-0 border-bottom-0 px-24 py-13 mb-0 fw-semibold text-lg radius-4 d-flex align-items-center justify-content-between"
                        role="alert">
                        <div class="d-flex align-items-center gap-2">
                            <iconify-icon icon="akar-icons:double-check" class="icon text-xl"></iconify-icon>
                            This is a Success alert
                        </div>
                        <button @click="removeLeftBorderAlert('leftBorderSuccess')"
                            class="remove-button text-success-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>

                    <!-- Warning Alert -->
                    <div v-if="leftBorderWarningVisible"
                        class="alert alert-warning bg-warning-100 text-warning-600 border-warning-600 border-start-width-4-px border-top-0 border-end-0 border-bottom-0 px-24 py-13 mb-0 fw-semibold text-lg radius-4 d-flex align-items-center justify-content-between"
                        role="alert">
                        <div class="d-flex align-items-center gap-2">
                            <iconify-icon icon="mdi:alert-circle-outline" class="icon text-xl"></iconify-icon>
                            This is a Warning alert
                        </div>
                        <button @click="removeLeftBorderAlert('leftBorderWarning')"
                            class="remove-button text-warning-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>

                    <!-- Info Alert -->
                    <div v-if="leftBorderInfoVisible"
                        class="alert alert-info bg-info-100 text-info-600 border-info-600 border-start-width-4-px border-top-0 border-end-0 border-bottom-0 px-24 py-13 mb-0 fw-semibold text-lg radius-4 d-flex align-items-center justify-content-between"
                        role="alert">
                        <div class="d-flex align-items-center gap-2">
                            <iconify-icon icon="ci:link" class="icon text-xl"></iconify-icon>
                            This is a Info alert
                        </div>
                        <button @click="removeLeftBorderAlert('leftBorderInfo')"
                            class="remove-button text-info-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>

                    <!-- Danger Alert -->
                    <div v-if="leftBorderDangerVisible"
                        class="alert alert-danger bg-danger-100 text-danger-600 border-danger-600 border-start-width-4-px border-top-0 border-end-0 border-bottom-0 px-24 py-13 mb-0 fw-semibold text-lg radius-4 d-flex align-items-center justify-content-between"
                        role="alert">
                        <div class="d-flex align-items-center gap-2">
                            <iconify-icon icon="mingcute:delete-2-line" class="icon text-xl"></iconify-icon>
                            This is a Danger alert
                        </div>
                        <button @click="removeLeftBorderAlert('leftBorderDanger')"
                            class="remove-button text-danger-600 text-xxl line-height-1">
                            <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Default Alerts 1 -->
        <div class="col-lg-6">
            <div class="card h-100 p-0">
                <div class="card-header border-bottom bg-base py-16 px-24">
                    <h6 class="text-lg fw-semibold mb-0">Default Alerts</h6>
                </div>
                <div class="card-body p-24 d-flex flex-column gap-4">
                    <!-- Primary Alert -->
                    <div v-if="defaultPrimaryVisible"
                        class="alert alert-primary bg-primary-50 text-primary-600 border-primary-50 px-24 py-11 mb-0 fw-semibold text-lg radius-8"
                        role="alert">
                        <div class="d-flex align-items-center justify-content-between text-lg">
                            This is a Primary alert
                            <button @click="removeDefaultAlert('defaultPrimary')"
                                class="remove-button text-primary-600 text-xxl line-height-1">
                                <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                            </button>
                        </div>
                        <p class="fw-medium text-primary-600 text-sm mt-8">Lorem Ipsum is simply dummy text of the
                            printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy</p>
                    </div>

                    <!-- Success Alert -->
                    <div v-if="defaultSuccessVisible"
                        class="alert alert-success bg-success-100 text-success-600 border-success-100 px-24 py-11 mb-0 fw-semibold text-lg radius-8"
                        role="alert">
                        <div class="d-flex align-items-center justify-content-between text-lg">
                            This is a Success alert
                            <button @click="removeDefaultAlert('defaultSuccess')"
                                class="remove-button text-success-600 text-xxl line-height-1">
                                <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                            </button>
                        </div>
                        <p class="fw-medium text-success-600 text-sm mt-8">Lorem Ipsum is simply dummy text of the
                            printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy</p>
                    </div>

                    <!-- Warning Alert -->
                    <div v-if="defaultWarningVisible"
                        class="alert alert-warning bg-warning-100 text-warning-600 border-warning-100 px-24 py-11 mb-0 fw-semibold text-lg radius-8"
                        role="alert">
                        <div class="d-flex align-items-center justify-content-between text-lg">
                            This is a Warning alert
                            <button @click="removeDefaultAlert('defaultWarning')"
                                class="remove-button text-warning-600 text-xxl line-height-1">
                                <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                            </button>
                        </div>
                        <p class="fw-medium text-warning-600 text-sm mt-8">Lorem Ipsum is simply dummy text of the
                            printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy</p>
                    </div>

                    <!-- Info Alert -->
                    <div v-if="defaultInfoVisible"
                        class="alert alert-info bg-info-100 text-info-600 border-info-100 px-24 py-11 mb-0 fw-semibold text-lg radius-8"
                        role="alert">
                        <div class="d-flex align-items-center justify-content-between text-lg">
                            This is a Info alert
                            <button @click="removeDefaultAlert('defaultInfo')"
                                class="remove-button text-info-600 text-xxl line-height-1">
                                <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                            </button>
                        </div>
                        <p class="fw-medium text-info-600 text-sm mt-8">Lorem Ipsum is simply dummy text of the printing
                            and typesetting industry. Lorem Ipsum has been the industry's standard dummy</p>
                    </div>

                    <!-- Danger Alert -->
                    <div v-if="defaultDangerVisible"
                        class="alert alert-danger bg-danger-100 text-danger-600 border-danger-100 px-24 py-11 mb-0 fw-semibold text-lg radius-8"
                        role="alert">
                        <div class="d-flex align-items-center justify-content-between text-lg">
                            This is a Danger alert
                            <button @click="removeDefaultAlert('defaultDanger')"
                                class="remove-button text-danger-600 text-xxl line-height-1">
                                <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                            </button>
                        </div>
                        <p class="fw-medium text-danger-600 text-sm mt-8">Lorem Ipsum is simply dummy text of the
                            printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Default Alerts 2 -->
        <div class="col-lg-6">
            <div class="card h-100 p-0">
                <div class="card-header border-bottom bg-base py-16 px-24">
                    <h6 class="text-lg fw-semibold mb-0">Default Alerts</h6>
                </div>
                <div class="card-body p-24 d-flex flex-column gap-4">
                    <!-- Primary Alert -->
                    <div v-if="defaultPrimary2Visible"
                        class="alert alert-primary bg-primary-50 text-primary-600 border-primary-50 px-24 py-11 mb-0 fw-semibold text-lg radius-8"
                        role="alert">
                        <div class="d-flex align-items-start justify-content-between text-lg">
                            <div class="d-flex align-items-start gap-2">
                                <iconify-icon icon="mingcute:emoji-line"
                                    class="icon text-xl mt-4 flex-shrink-0"></iconify-icon>
                                <div>
                                    This is a Primary alert
                                    <p class="fw-medium text-primary-600 text-sm mt-8">Lorem Ipsum is simply dummy text
                                        of the printing and typesetting industry. Lorem Ipsum has been the industry's
                                        standard dummy</p>
                                </div>
                            </div>
                            <button @click="removeDefaultAlert('defaultPrimary2')"
                                class="remove-button text-primary-600 text-xxl line-height-1">
                                <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                            </button>
                        </div>
                    </div>

                    <!-- Success Alert -->
                    <div v-if="defaultSuccess2Visible"
                        class="alert alert-success bg-success-100 text-success-600 border-success-100 px-24 py-11 mb-0 fw-semibold text-lg radius-8"
                        role="alert">
                        <div class="d-flex align-items-start justify-content-between text-lg">
                            <div class="d-flex align-items-start gap-2">
                                <iconify-icon icon="bi:patch-check"
                                    class="icon text-xl mt-4 flex-shrink-0"></iconify-icon>
                                <div>
                                    This is a Success alert
                                    <p class="fw-medium text-success-600 text-sm mt-8">Lorem Ipsum is simply dummy text
                                        of the printing and typesetting industry. Lorem Ipsum has been the industry's
                                        standard dummy</p>
                                </div>
                            </div>
                            <button @click="removeDefaultAlert('defaultSuccess2')"
                                class="remove-button text-success-600 text-xxl line-height-1">
                                <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                            </button>
                        </div>
                    </div>

                    <!-- Warning Alert -->
                    <div v-if="defaultWarning2Visible"
                        class="alert alert-warning bg-warning-100 text-warning-600 border-warning-100 px-24 py-11 mb-0 fw-semibold text-lg radius-8"
                        role="alert">
                        <div class="d-flex align-items-start justify-content-between text-lg">
                            <div class="d-flex align-items-start gap-2">
                                <iconify-icon icon="mdi:clock-outline"
                                    class="icon text-xl mt-4 flex-shrink-0"></iconify-icon>
                                <div>
                                    This is a Warning alert
                                    <p class="fw-medium text-warning-600 text-sm mt-8">Lorem Ipsum is simply dummy text
                                        of the printing and typesetting industry. Lorem Ipsum has been the industry's
                                        standard dummy</p>
                                </div>
                            </div>
                            <button @click="removeDefaultAlert('defaultWarning2')"
                                class="remove-button text-warning-600 text-xxl line-height-1">
                                <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                            </button>
                        </div>
                    </div>

                    <!-- Info Alert -->
                    <div v-if="defaultInfo2Visible"
                        class="alert alert-info bg-info-100 text-info-600 border-info-100 px-24 py-11 mb-0 fw-semibold text-lg radius-8"
                        role="alert">
                        <div class="d-flex align-items-start justify-content-between text-lg">
                            <div class="d-flex align-items-start gap-2">
                                <iconify-icon icon="mynaui:check-octagon"
                                    class="icon text-xl mt-4 flex-shrink-0"></iconify-icon>
                                <div>
                                    This is a Info alert
                                    <p class="fw-medium text-info-600 text-sm mt-8">Lorem Ipsum is simply dummy text of
                                        the printing and typesetting industry. Lorem Ipsum has been the industry's
                                        standard dummy</p>
                                </div>
                            </div>
                            <button @click="removeDefaultAlert('defaultInfo2')"
                                class="remove-button text-info-600 text-xxl line-height-1">
                                <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                            </button>
                        </div>
                    </div>

                    <!-- Danger Alert -->
                    <div v-if="defaultDanger2Visible"
                        class="alert alert-danger bg-danger-100 text-danger-600 border-danger-100 px-24 py-11 mb-0 fw-semibold text-lg radius-8"
                        role="alert">
                        <div class="d-flex align-items-start justify-content-between text-lg">
                            <div class="d-flex align-items-start gap-2">
                                <iconify-icon icon="mingcute:delete-2-line"
                                    class="icon text-xl mt-4 flex-shrink-0"></iconify-icon>
                                <div>
                                    This is a Danger alert
                                    <p class="fw-medium text-danger-600 text-sm mt-8">Lorem Ipsum is simply dummy text
                                        of the printing and typesetting industry. Lorem Ipsum has been the industry's
                                        standard dummy</p>
                                </div>
                            </div>
                            <button @click="removeDefaultAlert('defaultDanger2')"
                                class="remove-button text-danger-600 text-xxl line-height-1">
                                <iconify-icon icon="iconamoon:sign-times-light" class="icon"></iconify-icon>
                            </button>
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
            // Default Alerts Visibility
            primaryVisible: true,
            secondaryVisible: true,
            warningVisible: true,
            infoVisible: true,
            dangerVisible: true,

            // Outline Alerts Visibility
            outlinePrimaryVisible: true,
            outlineSecondaryVisible: true,
            outlineWarningVisible: true,
            outlineInfoVisible: true,
            outlineDangerVisible: true,

            // Solid Alerts Visibility
            solidPrimaryVisible: true,
            solidSuccessVisible: true,
            solidInfoVisible: true,
            solidSecondaryVisible: true,
            solidWarningVisible: true,
            solidDangerVisible: true,

            // Outline Alerts Visibility
            outlinePrimaryVisible: true,
            outlineSecondaryVisible: true,
            outlineSuccessVisible: true,
            outlineWarningVisible: true,
            outlineInfoVisible: true,
            outlineDangerVisible: true,

            // Left Border Alerts Visibility
            leftBorderPrimaryVisible: true,
            leftBorderSecondaryVisible: true,
            leftBorderSuccessVisible: true,
            leftBorderWarningVisible: true,
            leftBorderInfoVisible: true,
            leftBorderDangerVisible: true,

            // Default Alerts 1 Visibility
            defaultPrimaryVisible: true,
            defaultSuccessVisible: true,
            defaultWarningVisible: true,
            defaultInfoVisible: true,
            defaultDangerVisible: true,
            // Default Alerts 2 Visibility
            defaultPrimary2Visible: true,
            defaultSuccess2Visible: true,
            defaultWarning2Visible: true,
            defaultInfo2Visible: true,
            defaultDanger2Visible: true,
        };
    },
    methods: {
        // Remove default alert
        removeAlert(alertType) {
            this[`${alertType}Visible`] = false;
        },
        // Remove outline alert
        removeOutlineAlert(alertType) {
            this[`${alertType}Visible`] = false;
        },
        // Remove solid alert
        removeSolidAlert(alertType) {
            this[`${alertType}Visible`] = false;
        },
        removeLeftBorderAlert(alertType) {
            this[`${alertType}Visible`] = false;
        },
        removeDefaultAlert(alertType) {
            this[`${alertType}Visible`] = false;
        }
    }
};
</script>
