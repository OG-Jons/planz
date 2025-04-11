import {defineStore} from "pinia";
import axios from "axios";
import type {Plant} from "@/types.ts";

// This is a store for the plants
// It will store all the plants gotten from the BE
// On initialization, it will run an API request to get the plants
// One function will return an array of plants, but without the stats.
export const usePlantsStore = defineStore('plants', {
    state: () => ({
        plants: [] as Plant[]
    }),
    actions: {
        async fetchPlants() {
            const response = await axios.get<Plant[]>(
                `/api/plants?minutes=30`
            )
            this.plants = response.data
        },
        async fetchPlant(id: number) {
            const response = await axios.get<Plant>(
                `/api/plants/${id}?minutes=30`
            )
            return response.data
        },
        async uploadPlantImage(id: number, file: File) {
            const formData = new FormData()
            formData.append("file", file)

            await axios.post(`/api/plants/${id}/image`, formData)

        }
    },
    getters: {
        getPlantsWithoutStats: (state) => {
            return state.plants.map(plant => {
                return {
                    id: plant.id,
                    name: plant.name,
                    species: plant.species
                }
            })
        }
    }
})