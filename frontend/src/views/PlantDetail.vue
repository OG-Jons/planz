<script setup lang="ts">
import {onMounted, reactive, ref} from "vue";
import {type Plant} from "@/types.ts";
import PlantStatsChart from "@cmp/PlantStatsChart.vue";
import {usePlantsStore} from "@stores/plants.ts";
import {onBeforeRouteUpdate, useRoute} from "vue-router";
import PlantInformation from "@cmp/PlantInformation.vue";

const plant = reactive<Plant>({} as Plant)
const loading = ref(false)
const error = ref<string | null>(null)
const cache = ref<number | null>(new Date().getTime())

const plantStore = usePlantsStore()

const fetchPlantData = async (id: number) => {
  loading.value = true
  error.value = null

  try {
    Object.assign(plant, await plantStore.fetchPlant(id))
    cache.value = new Date().getTime()
  } catch (err: any) {
    error.value = err.response?.data?.detail || "An error occurred"
    Object.assign(plant, {} as Plant)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  const route = useRoute()
  fetchPlantData(Number(route.params.id))
})

const uploadPlantImage = async (file: File, id: number) => {
  try {
    await plantStore.uploadPlantImage(id, file)
    await fetchPlantData(id)
    cache.value = Date.now()
  } catch (err: any) {
    error.value = err.response?.data?.detail || "An error occurred"
  }
}

onBeforeRouteUpdate(async (to, from) => {
  if (to.params.id !== from.params.id) {
    await fetchPlantData(Number(to.params.id))
  }
})

</script>

<template>
  <div class="plant-view">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="plant.id" class="plant-data">
      <plant-information :name="plant.name" :species="plant.species" :cache="cache" :image="plant.image"
                         @submitted="(file) => uploadPlantImage(file, plant.id)" @refresh="fetchPlantData(plant.id)" :is-single="true" />
      <div class="chart-container">
        <PlantStatsChart :stats="plant.stats"/>
      </div>
    </div>
  </div>
</template>

<style scoped>
.plant-view {
  max-width: 60vw;
  margin: 0 auto;
  padding: 20px;
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