<script setup>
import { useRoute } from "vue-router";
import { computed } from "vue";
import { useLoadingBar, useMessage } from "naive-ui";

window.$loadingBar = useLoadingBar();
window.$message = useMessage();

const route = useRoute();
const layout = computed(() => route.meta.layout);
</script>

<template>
  <component :is="layout"></component>
</template>
