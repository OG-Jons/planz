import type {RouteRecordRaw} from "vue-router";
import {createRouter, createWebHistory} from "vue-router";
import PlantView from "@/views/PlantView.vue";

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'PlantView',
        component: PlantView
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router