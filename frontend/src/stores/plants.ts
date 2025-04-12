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
                `/api/plants?minutes=60`
            )
            this.plants = response.data
        },
        async fetchPlant(id: number) {
            const response = await axios.get<Plant>(
                `/api/plants/${id}?minutes=120`
            )
            return response.data
        },
        async uploadPlantImage(id: number, file: File) {
            const formData = new FormData()
            formData.append("file", file)

            await axios.post(`/api/plants/${id}/image`, formData)

        },
        async resetPlantStats(id: number) {
            await axios.delete(`/api/plants/${id}/stats/reset`)
            const plant = this.plants.find(plant => plant.id === id)
            if (plant) {
                plant.stats = []
            }
        },
        async deletePlant(id: number) {
            await axios.delete(`/api/plants/${id}`)
            this.plants = this.plants.filter(plant => plant.id !== id)
        },
        async savePlant(plant: Plant) {
            const response = await axios.put<Plant>(`/api/plants/${plant.id}`, plant)
            const index = this.plants.findIndex(p => p.id === plant.id)
            if (index !== -1) {
                this.plants[index] = {...plant, ...response.data}
            } else {
                this.plants.push(response.data)
            }
        }
    },
    getters: {
        getPlantsWithoutStats: (state) => {
            return state.plants.map(plant => {
                return {
                    id: plant.id,
                    name: plant.name,
                    species: plant.species,
                    soil_wet: plant.soil_wet,
                    soil_dry: plant.soil_dry,
                }
            })
        }
    }
})