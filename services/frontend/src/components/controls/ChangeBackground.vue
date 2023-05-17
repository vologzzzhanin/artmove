<script setup>
import { h } from "vue";
import { useAnimationsStore } from "@/store/modules/animations";

const animationsStore = useAnimationsStore();

const emit = defineEmits(["saveBackground"]);
</script>

<template>
  <n-color-picker
    v-model:value="animationsStore.currentAnimation.background"
    :modes="['hex']"
    :actions="['clear']"
    :render-label="
      () => {
        h('span');
      }
    "
    @update:value="emit('saveBackground')"
  />
</template>
