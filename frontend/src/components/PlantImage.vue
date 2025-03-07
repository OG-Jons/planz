<script setup lang="ts">

defineProps<{
  path: string | null,
  cache: number | null
}>()

const emits = defineEmits<
    (event: 'submitted', file: File) => void
>()

const submitted = (files: FileList | null) => {
  if (files?.length !== 1) return

  const file = files[0]

  emits('submitted', file)
}
</script>

<template>
  <div class="plant-image">
    <img v-if="path" :src="`/api${path}?${cache}`" alt="plant" width="200" height="200" @click="$refs.file.click()" >
    <div v-else class="no-image" @click="$refs.file.click()">?</div>
    <input type="file" ref="file" style="display: none" @change="submitted(($event.target as HTMLInputElement).files)" />
  </div>
</template>

<style scoped>
.plant-image {
  cursor: pointer;
  width: fit-content;
  height: fit-content;
}

.no-image {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50px;
  height: 50px;
  border: 1px solid black;
  border-radius: 50px;
  font-size: 24px;
}
</style>