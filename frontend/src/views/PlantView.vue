<script setup lang="ts">
import {ref} from "vue";
import {type Plant} from "@/types.ts";
import PlantStatsChart from "@cmp/PlantStatsChart.vue";
import {usePlantsStore} from "@stores/plants.ts";
import PlantInformation from "@cmp/PlantInformation.vue";

const loading = ref(false)
const error = ref<string | null>(null)
const cache = ref<number | null>(new Date().getTime())

const plantStore = usePlantsStore()

const fetchPlantData = async () => {
  loading.value = true
  error.value = null

  try {
    await plantStore.fetchPlants()
    cache.value = new Date().getTime()
  } catch (err: any) {
    error.value = err.response?.data?.detail || "An error occurred"
    plantStore.plants = [] as Plant[]
  } finally {
    loading.value = false
  }
}

const uploadPlantImage = async (file: File, id: number) => {
  try {
    await plantStore.uploadPlantImage(id, file)
    await fetchPlantData()
    cache.value = Date.now()
  } catch (err: any) {
    error.value = err.response?.data?.detail || "An error occurred"
  }
}

</script>

<template>
  <div class="heading">
    <h1>Planz</h1>
    <div class="search-container">
      <button @click="fetchPlantData"><span class="material-icons">refresh</span></button>
    </div>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
  <div class="plant-view">

    <div v-for="plant in plantStore.plants">
      <div v-if="plant" class="plant-data">
        <plant-information
            :name="plant.name"
            :species="plant.species"
            :cache="cache"
            :image="plant.image"
            @submitted="(file) => uploadPlantImage(file, plant.id)"
            :is-single="false"
        />
        <div class="chart-container">
          <PlantStatsChart :stats="plant.stats"/>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.heading {
  margin: 1.5rem 0 0 1.5rem;
}

.plant-view {
  width: 100%;
  padding: 20px;
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 20px;
}

@media (min-width: 768px) {
  .plant-view {
    grid-template-columns: repeat(2, 1fr);
  }
}

input {
  padding: 8px;
  margin-right: 10px;
  width: 200px;
}

button {
  padding: 8px 16px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #3aa876;
}

.chart-container {
  margin-top: 40px;
}

.loading {
  color: #42b983;
  margin: 20px 0;
}

.error {
  color: #ff4444;
  margin: 20px 0;
}
</style>