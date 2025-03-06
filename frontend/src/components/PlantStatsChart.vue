<script setup lang="ts">
import { Line } from 'vue-chartjs'
import { type Stat } from '@/types'
import {computed} from "vue";

const props = defineProps<{
  stats: Stat[]
}>()

const chartData = computed(() => ({
  labels: props.stats.map(stat => new Date(stat.timestamp).toLocaleDateString()),
  datasets: [
    {
      label: 'Humidity Score',
      backgroundColor: '#f87979',
      data: props.stats.map(stat => stat.humidity_score)
    },
    {
      label: 'Sunlight Score',
      backgroundColor: '#79a6f8',
      data: props.stats.map(stat => stat.sunlight_score)
    }
  ]
}))

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false
}))
</script>

<template>
  <div>
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<style scoped>
</style>
