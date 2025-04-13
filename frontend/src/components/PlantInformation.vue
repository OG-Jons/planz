<script setup lang="ts">
import PlantImage from "@cmp/PlantImage.vue";
defineProps<{
  name: string,
  species: string,
  image: string,
  cache: number | null,
  isSingle: boolean
}>()

defineEmits(['submitted', 'refresh'])
</script>

<template>
  <div class="plant-info">
    <div class="plant-title">
      <span class="title">{{ name }} </span>
      <span class="subtitle">{{ species }}</span>
      <button v-if="isSingle" @click="$emit('refresh')">
        <span class="material-icons">refresh</span>
      </button>
    </div>
    <div class="plant-image">
      <PlantImage :path="image" :cache="cache" @submitted="(file) => $emit('submitted', file)" />
    </div>
  </div>
</template>

<style scoped>
.plant-title {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.title {
  font-size: 1.5rem;
  font-weight: bold;
}

.subtitle {
  color: #555;
}

.plant-info {
  display: flex;
  justify-content: space-between;
}
</style>