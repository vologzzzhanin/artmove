<script setup>
import AppWrapper from "@/components/AppWrapper.vue";
import { darkTheme, dateRuRU, ruRU } from "naive-ui";
</script>

<template>
  <n-config-provider
    :locale="ruRU"
    :date-locale="dateRuRU"
    style="height: 100%"
    :theme="darkTheme"
  >
    <n-message-provider>
      <n-loading-bar-provider>
        <AppWrapper />
      </n-loading-bar-provider>
    </n-message-provider>
  </n-config-provider>
</template>
