<script setup>
import { VideoRecording20Regular } from "@vicons/fluent";
</script>

<template>
  <n-popover trigger="hover">
    <template #trigger>
      <n-button text class="controls">
        <n-icon :component="VideoRecording20Regular" />
      </n-button>
    </template>
    <span>TODO</span>
  </n-popover>
</template>
