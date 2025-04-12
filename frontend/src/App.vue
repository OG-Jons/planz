<script setup lang="ts">
import { usePlantsStore } from "@stores/plants.ts";
import {onMounted} from "vue";
import Sidebar from "@cmp/Sidebar.vue";
import {useMediaQuery, useStorage} from "@vueuse/core";
const isLargeScreen = useMediaQuery('(min-width: 1024px)')

const plantStore = usePlantsStore();

const isExpanded = useStorage('is_expanded', false)

onMounted(() => {
  plantStore.fetchPlants()
})
</script>

<template>
  <div class="app-container">
    <sidebar />
    <div :class="['router', {'mobile': !isLargeScreen}, {'expanded': isExpanded}]">
      <router-view />
    </div>
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
  --danger: #ef4444;
  --warning: #f59e0b;
}

.success {
  background-color: var(--primary);

  &:hover {
    background-color: #22c55e;
  }
}
.danger {
  background-color: var(--danger);

  &:hover {
    background-color: #dc2626;
  }
}

.warning {
  background-color: var(--warning);

  &:hover {
    background-color: #ca8a04;
  }
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

.router {
  flex: 1;
  transition: margin-left 0.3s ease-in-out;
  margin-left: calc(2rem + 32px);

  &.expanded {
    margin-left: var(--sidebar-width);
  }

  &.mobile {
    margin-left: 0;
  }
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