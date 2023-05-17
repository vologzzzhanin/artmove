<script setup>
import { ImageMultiple48Regular } from "@vicons/fluent";

const emit = defineEmits(["showComposition"]);
</script>

<template>
  <n-button text class="controls" @click="emit('showComposition')">
    <n-icon :component="ImageMultiple48Regular" />
  </n-button>
</template>
