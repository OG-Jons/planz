<script setup lang="ts">
import { usePlantsStore } from "@stores/plants.ts";
import { onMounted } from "vue";
import Sidebar from "@cmp/Sidebar.vue";

const plantStore = usePlantsStore();

onMounted(() => {
  plantStore.fetchPlants();
});
</script>

<template>
  <div class="app-container">
    <sidebar />
    <router-view />
  </div>
</template>

<style lang="scss">
:root {
  --primary: #4ade80;
  --primary-alt: #22c55e;
  --grey: #64748b;
  --dark: #1e293b;
  --dark-alt: #334155;
  --light: #f1f5f9;
  --sidebar-width: 300px;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Fira sans', sans-serif;
}

body {
  background: var(--light);
}

router-view {
  margin-left: calc(2rem + 32px);
}

button {
  cursor: pointer;
  appearance: none;
  border: none;
  outline: none;
  background: none;
}

.app-container {
  display: flex;
}
</style>