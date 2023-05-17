<script setup>
import { onMounted } from "vue";
import { RouterView } from "vue-router";
import { useUserStore } from "@/store/modules/user";
import { useAnimationsStore } from "@/store/modules/animations";
import NavBar from "@/components/NavBar.vue";

const userStore = useUserStore();
const animationsStore = useAnimationsStore();

onMounted(async () => {
  await userStore.getUserData();
  await animationsStore.getAnimationsList();
});
</script>

<template>
  <n-layout h-full>
    <n-layout>
      <n-layout-header class="nav"> <NavBar /> </n-layout-header>
      <n-layout-content overflow-auto class="content">
        <RouterView />
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>

<style scoped lang="scss">
.nav {
  height: $header-height;
  z-index: 999;
}
.content {
  height: calc(100vh - $header-height);
  padding: $layout-padding;
}
</style>
