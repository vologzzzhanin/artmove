<script setup>
import { ArrowClockwise32Regular } from "@vicons/fluent";

const emit = defineEmits(["refresh"]);
</script>

<template>
  <n-button text class="controls" @click="emit('refresh')">
    <n-icon :component="ArrowClockwise32Regular" />
  </n-button>
</template>
