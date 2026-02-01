import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { Icon } from '@iconify/vue';
import App from './App.vue';
import router from './router';
import './style.css';

const app = createApp(App);
const pinia = createPinia();

// Register plugins
app.use(pinia);
app.use(router);

// Register global components
app.component('Icon', Icon);

app.mount('#app');
