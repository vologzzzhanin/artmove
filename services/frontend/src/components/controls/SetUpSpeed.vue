<script setup>
import { TimePicker24Regular } from "@vicons/fluent";
</script>

<template>
  <n-popover trigger="hover">
    <template #trigger>
      <n-button text class="controls">
        <n-icon :component="TimePicker24Regular" />
      </n-button>
    </template>
    <span>TODO</span>
  </n-popover>
</template>
