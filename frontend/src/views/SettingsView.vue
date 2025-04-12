<script lang="ts" setup>

import {usePlantsStore} from "@stores/plants.ts";
import type {Plant} from "@/types.ts";
import {ref} from "vue";
import {AxiosError} from "axios";

const plantStore = usePlantsStore();

const errorMsg = ref<string | null>(null);

const savePlant = async (plant: Plant) => {
  try {
    await plantStore.savePlant(plant);
  } catch (error: unknown) {
    handleError(error);
  }
};

const deletePlant = async (id: number) => {
  try {
    await plantStore.deletePlant(id);
  } catch (error) {
    handleError(error);
  }
};

const resetStats = async (plant: Plant) => {
  try {
    await plantStore.resetPlantStats(plant.id);
  } catch (error) {
    handleError(error);
  }
};

const handleError = (error: unknown) => {
  if (error instanceof AxiosError) {
    errorMsg.value = error.response?.data?.detail || "An error occurred";
  } else {
    errorMsg.value = "An unexpected error occurred";
  }
};
</script>

<template>
  <div class="settings-view">
    <h1>Settings</h1>
    <p>Manage your plants here.</p>
    <div class="settings-container">
      <span v-if="errorMsg" class="error-message">An error occured: {{ errorMsg }}</span>
      <table>
        <thead>
        <tr>
          <th>Plant Name</th>
          <th>Species</th>
          <th>Wet Value</th>
          <th>Dry Value</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="plant in plantStore.plants" :key="plant.id">
          <td><input type="text" v-model="plant.name"/></td>
          <td><input type="text" v-model="plant.species"/></td>
          <td><input type="number" v-model="plant.soil_wet"/></td>
          <td><input type="number" v-model="plant.soil_dry"/></td>
          <td>
            <button class="danger" @click="deletePlant(plant.id)">Delete</button>
            <button class="success" @click="savePlant(plant)">Save/Update</button>
            <button class="warning" @click="resetStats(plant)">Reset Stats</button>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.error-message {
  color: var(--danger);
  font-size: 1rem;
  margin: 1rem auto;
  text-align: center;
}

.settings-view {
  width: 80%;
  margin: 2rem auto auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  font-size: 1rem;
  text-align: left;
}

th, td {
  border: 1px solid #ddd;
  padding: 0.75rem;
}

th {
  background-color: var(--dark);
  color: white;
  font-weight: bold;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f1f5f9;
}

button {
  margin-right: 0.5rem;
  padding: 0.5rem 1rem;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
</style>