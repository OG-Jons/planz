<script setup lang="ts">
import { type Stat } from '@/types'
import {computed} from "vue";
import type {ApexOptions} from "apexcharts";

const props = defineProps<{
  stats: Stat[]
}>()

const chartData = computed(() => ({
  series: [
    {
      name: 'Soil Humidity Score',
      data: props.stats.map(stat => [stat.timestamp, stat.soil_moisture_score])
    },
    {
      name: 'Sunlight Score',
      data: props.stats.map(stat => [stat.timestamp, stat.sunlight_score])
    },
    {
      name: 'Temperature Score',
      data: props.stats.map(stat => [stat.timestamp, stat.temperature_score])
    },
    {
      name: 'Air Humidity Score',
      data: props.stats.map(stat => [stat.timestamp, stat.humidity_score])
    }
  ],
}));

const chartOptions = computed<ApexOptions>(() => ({
  chart: {
    type: 'area',
    height: 600,
    zoom: {
      enabled: true
    },
    events: {
      beforeZoom(_: any, {xaxis}: any) {
        // From the props, get the field with the latest date
        const mainDiff = (new Date(props.stats[0].timestamp).valueOf())
        const zoomdifference = xaxis.max - xaxis.min ;
        if (zoomdifference > mainDiff) {
          return {
            xaxis: {
              min: props.stats[0].timestamp,
              max: props.stats[props.stats.length - 1].timestamp
            }
          }
        } else {
          return {
            xaxis: {
              min: xaxis.min,
              max: xaxis.max
            }
          }
        }
      }
    },
    toolbar: {
      tools: {
        download: true,
        reset: true,
        zoom: true,
        zoomin: false,
        zoomout: false,
        pan: true,
      },
    }
  },
  colors: ['#37ca10', '#f6c811', '#e85908', '#00a6ff'],
  dataLabels: {
    enabled: false
  },
  stroke: {
    curve: 'smooth'
  },
  xaxis: {
    type: 'datetime',
    min: new Date().getTime() - 1000 * 60 * 60,
    tickAmount: 6,
    labels: {
      datetimeUTC: false
    }
  },
  yaxis: {
    min: 0,
    max: 100,
  },
  tooltip: {
    shared: true,
    intersect: false
  },
  responsive: [{
    breakpoint: 480,
    options: {
      chart: {
        width: 200
      },
      legend: {
        position: 'bottom'
      }
    }
  }]
}))
</script>

<template>
  <div>
    <apexchart :options="chartOptions" :series="chartData.series" />
  </div>
</template>

<style scoped>
</style>
