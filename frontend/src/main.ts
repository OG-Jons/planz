import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import Chart from "chart.js/auto";

const app = createApp(App)
app.use(router)
app.config.globalProperties.$Chart = Chart
app.mount('#app')
