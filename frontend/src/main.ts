import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import VueApexCharts from 'vue3-apexcharts';
import VueSidebarMenu from 'vue-sidebar-menu';
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
import {createPinia} from "pinia";
import './fontawesome.ts'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

const pinia = createPinia()
const app = createApp(App)

app
    .use(router)
    .use(pinia)
    .use(VueApexCharts)
    .use(VueSidebarMenu)
    .component('font-awesome-icon', FontAwesomeIcon)
    .mount('#app')
