<script setup>
import { useRouter } from "vue-router";
import { Home48Regular } from "@vicons/fluent";

const router = useRouter();
</script>

<template>
  <n-button text class="controls" @click="router.push({ name: 'home' })">
    <n-icon :component="Home48Regular" />
  </n-button>
</template>
