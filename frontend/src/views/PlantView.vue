<script setup lang="ts">
import {onMounted, ref} from "vue";
import {type Plant} from "@/types.ts";
import axios from "axios";
import PlantStatsChart from "@cmp/PlantStatsChart.vue";
import PlantImage from "@cmp/PlantImage.vue";

const plants = ref<Plant[] | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const cache = ref<number | null>(new Date().getTime())

const fetchPlantData = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await axios.get<Plant[]>(
      `/api/plants`
    )
    plants.value = response.data
    cache.value = new Date().getTime()
  } catch (err: any) {
    error.value = err.response?.data?.detail || "An error occurred"
    plants.value = null
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchPlantData()
})

const uploadPlantImage = async (file: File, id: number) => {
  const formData = new FormData()
  formData.append("file", file)

  try {
    await axios.post(`/api/plants/${id}/image`, formData)
    await fetchPlantData()
    cache.value = Date.now()
  } catch (err: any) {
    error.value = err.response?.data?.detail || "An error occurred"
  }
}

</script>

<template>
  <div class="plant-view">
    <h1>Plant Stats Viewer</h1>
    <div class="search-container">
      <button @click="fetchPlantData">Get Plant Data</button>
    </div>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div v-for="plant in plants">
      <div v-if="plant" class="plant-data">
        <h2>{{ plant.name }} ({{ plant.species }})</h2>

        <div class="plant-image">
          <PlantImage :path="plant.image" :cache="cache" @submitted="(file) => uploadPlantImage(file, plant.id)" />
        </div>
        <div class="chart-container">
          <PlantStatsChart :stats="plant.stats" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.plant-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-container {
  margin: 20px 0;
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