import { createApp } from 'vue'
import App from './App.vue'
import router from './router.js'
import VueApexCharts from "vue3-apexcharts"

// Add this import for Iconify:
import { Icon } from '@iconify/vue'

// Importing Bootstrap and other global CSS files
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import 'vue-slick-carousel/dist/vue-slick-carousel.css'
import 'vue-slick-carousel/dist/vue-slick-carousel-theme.css'

// Your other CSS files
import '@/assets/css/style.css'
import '@/assets/css/remixicon.css'

// Create and mount Vue app
const app = createApp(App)

// Register Iconify globally
app.component('iconify-icon', Icon)

app.use(router)
app.use(VueApexCharts);
app.mount('#app')

