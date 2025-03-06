<script setup lang="ts">
import {ref} from "vue";
import {type Plant} from "@/types.ts";
import axios from "axios";
import PlantStatsChart from "@cmp/PlantStatsChart.vue";

const plantId = ref<number | null>(null)
const plant = ref<Plant | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

const fetchPlantData = async () => {
  if (!plantId.value) {
    error.value = "Please enter a plant ID"
    return
  }

  loading.value = true
  error.value = null

  try {
    const response = await axios.get<Plant>(
      `/api/plants/${plantId.value}?minutes=180`
    )
    plant.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || "An error occurred"
    plant.value = null
  } finally {
    loading.value = false
  }
}

</script>

<template>
  <div class="plant-view">
    <h1>Plant Stats Viewer</h1>
    <div class="search-container">
      <input type="number" v-model.number="plantId" placeholder="Enter plant ID" @keyup.enter="fetchPlantData"/>
      <button @click="fetchPlantData">Get Plant Data</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="plant" class="plant-data">
      <h2>{{ plant.name }} ({{ plant.species }})</h2>
      <div class="chart-container">
        <PlantStatsChart :stats="plant.stats" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.plant-view {
  max-width: 800px;
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
  height: 400px;
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