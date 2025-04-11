import type {RouteRecordRaw} from "vue-router";
import {createRouter, createWebHistory} from "vue-router";
import PlantView from "@/views/PlantView.vue";
import PlantDetail from "@/views/PlantDetail.vue";


const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'PlantView',
        component: PlantView
    },
    // Path to show a single plant with id
    {
        path: '/:id',
        name: 'PlantDetail',
        component: PlantDetail
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router