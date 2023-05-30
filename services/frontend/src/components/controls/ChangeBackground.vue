<script setup>
import { h } from "vue";
import { useAnimationsStore } from "@/store/modules/animations";

const animationsStore = useAnimationsStore();

const emit = defineEmits(["saveBackground"]);

const onUpdateShow = (show) => {
  if (!show) {
    emit("saveBackground");
  }
};
</script>

<template>
  <n-color-picker
    v-model:value="animationsStore.currentAnimation.background"
    :modes="['hex']"
    :render-label="
      () => {
        h('span');
      }
    "
    @update:show="onUpdateShow"
  />
</template>
