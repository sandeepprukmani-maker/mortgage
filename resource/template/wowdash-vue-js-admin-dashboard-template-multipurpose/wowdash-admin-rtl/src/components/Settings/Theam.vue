<template>
    <div class="card h-100 p-0 radius-12">
        <div class="card-body p-24">
            <form @submit.prevent="handleSubmit" @reset="handleReset">
                <div class="row gy-4">
                    <!-- Logo 1 Upload -->
                    <div class="col-md-6">
                        <label for="imageUpload" class="form-label fw-semibold text-secondary-light text-md mb-8">
                            Logo <span class="text-secondary-light fw-normal">(140px X 140px)</span>
                        </label>
                        <input type="file" class="form-control radius-8" id="imageUpload"
                            @change="handleImageChange($event, 'previewImage1')">
                        <div class="avatar-upload mt-16">
                            <div class="avatar-preview style-two">
                                <div :style="{ backgroundImage: 'url(' + previewImage1 + ')' }" id="previewImage1">
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Logo 2 Upload -->
                    <div class="col-md-6">
                        <label for="imageUploadTwo" class="form-label fw-semibold text-secondary-light text-md mb-8">
                            Logo <span class="text-secondary-light fw-normal">(140px X 140px)</span>
                        </label>
                        <input type="file" class="form-control radius-8" id="imageUploadTwo"
                            @change="handleImageChange($event, 'previewImage2')">
                        <div class="avatar-upload mt-16">
                            <div class="avatar-preview style-two">
                                <div :style="{ backgroundImage: 'url(' + previewImage2 + ')' }" id="previewImage2">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Theme Colors -->
                <div class="mt-32">
                    <h6 class="text-xl mb-16">Theme Colors</h6>
                    <div class="row gy-4">
                        <div v-for="(theme, index) in themes" :key="theme.id" class="col-xxl-2 col-md-4 col-sm-6">
                            <input class="form-check-input payment-gateway-input" name="payment-gateway" type="radio"
                                :id="theme.id" :value="theme.id" v-model="selectedTheme" hidden />
                            <label :for="theme.id" class="payment-gateway-label border radius-8 p-8 w-100">
                                <span class="d-flex align-items-center gap-2">
                                    <span class="w-50 text-center">
                                        <span :class="theme.primaryClass + ' h-72-px w-100 radius-4'"></span>
                                        <span :class="theme.textClass + ' text-md fw-semibold mt-8'">{{ theme.name
                                            }}</span>
                                    </span>
                                    <span class="w-50 text-center">
                                        <span :class="theme.focusClass + ' h-72-px w-100 radius-4'"></span>
                                        <span :class="theme.textClass + ' text-md fw-semibold mt-8'">Focus</span>
                                    </span>
                                </span>
                            </label>
                        </div>
                    </div>

                    <!-- Buttons -->
                    <div class="d-flex align-items-center justify-content-center gap-3 mt-24">
                        <button type="reset"
                            class="border border-danger-600 bg-hover-danger-200 text-danger-600 text-md px-40 py-11 radius-8">
                            Reset
                        </button>
                        <button type="submit"
                            class="btn btn-primary border border-primary-600 text-md px-24 py-12 radius-8">
                            Save Change
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import Logoimg from '@/assets/images/payment/upload-image.png'
export default {
    data() {
        return {
            previewImage1: Logoimg,
            previewImage2: Logoimg,
            selectedTheme: null,
            themes: [
                {
                    id: 'blue',
                    name: 'Blue',
                    primaryClass: 'bg-primary-600',
                    focusClass: 'bg-primary-100',
                    textClass: 'text-secondary-light'
                },
                {
                    id: 'magenta',
                    name: 'Magenta',
                    primaryClass: 'bg-lilac-600',
                    focusClass: 'bg-lilac-100',
                    textClass: 'text-lilac-light'
                },
                {
                    id: 'orange',
                    name: 'Orange',
                    primaryClass: 'bg-warning-600',
                    focusClass: 'bg-warning-100',
                    textClass: 'text-secondary-light'
                },
                {
                    id: 'green',
                    name: 'Green',
                    primaryClass: 'bg-success-600',
                    focusClass: 'bg-success-100',
                    textClass: 'text-secondary-light'
                },
                {
                    id: 'red',
                    name: 'Red',
                    primaryClass: 'bg-danger-600',
                    focusClass: 'bg-danger-100',
                    textClass: 'text-secondary-light'
                },
                {
                    id: 'blueDark',
                    name: 'Blue Dark',
                    primaryClass: 'bg-info-600',
                    focusClass: 'bg-info-100',
                    textClass: 'text-secondary-light'
                }
            ]
        };
    },
    methods: {
        handleImageChange(event, previewId) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = e => {
                    this[previewId] = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        },
        handleSubmit() {
            console.log('Selected Theme:', this.selectedTheme);
            console.log('Preview Image 1:', this.previewImage1);
            console.log('Preview Image 2:', this.previewImage2);
            // Add submission logic here
        },
        handleReset() {
            this.previewImage1 = Logoimg;
            this.previewImage2 = Logoimg;
            this.selectedTheme = null;
        }
    }
};
</script>