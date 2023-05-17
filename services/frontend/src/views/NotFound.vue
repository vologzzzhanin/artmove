<script setup>
import { useRouter } from "vue-router";
const router = useRouter();
</script>

<template>
  <n-space justify="center" style="height: 100vh; align-items: center">
    <n-result status="404" title="404 Страница не найдена">
      <template #footer>
        <n-button size="small" @click="router.push({ name: 'home' })">
          Вернуться в приложение
        </n-button>
      </template>
    </n-result>
  </n-space>
</template>
