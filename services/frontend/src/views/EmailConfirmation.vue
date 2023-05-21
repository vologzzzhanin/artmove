<script setup>
import { onMounted } from "vue";
import { useUserStore } from "@/store/modules/user";
import { useAppStore } from "@/store/modules/app";

const props = defineProps({
  token: { type: String },
});

const userStore = useUserStore();
const appStore = useAppStore();

onMounted(async () => {
  await userStore.verifyUser(props.token);
});
</script>

<template>
  <n-space
    v-show="appStore.isLoading"
    justify="center"
    style="height: 100vh; align-items: center"
  >
    <n-spin />
  </n-space>
</template>
