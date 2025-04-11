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
<!--    <sidebar />-->
    <div class="content-container">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
}

.sidebar {
  width: 250px; /* Adjust the width as needed */
}

.content-container {
  flex-grow: 1;
  padding: 20px; /* Adjust the padding as needed */
}
</style>