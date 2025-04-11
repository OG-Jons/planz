<script setup lang="ts">
import {usePlantsStore} from "@stores/plants.ts";
import {computed} from "vue";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import { h } from 'vue'

const plantStore = usePlantsStore();


const faIcon = (props: any) => {
  return {
    element: h('div', [h(FontAwesomeIcon, { size: 'lg', ...props })]),
  }
}

const presets = [
  {
    title: 'Home',
    icon: faIcon({icon: 'fa-solid fa-home'}),
    to: '/'
  }
];

const menu = computed(() => [
  ...presets,
  ...plantStore.getPlantsWithoutStats.map(plant => ({
    title: plant.name,
    icon: faIcon({icon: 'fa-solid fa-spa'}),
    to: `/${plant.id}`
  }))
]);
</script>
<template>
  <sidebar-menu :menu="menu" />
</template>

