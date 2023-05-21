<script setup>
import { useRouter } from "vue-router";

const props = defineProps({
  status: { type: String, default: "error" },
  title: { type: String, default: "Ошибка" },
  description: { type: String, default: null },
  goTo: { type: String, default: null },
  buttonText: { type: String, default: "Перейти" },
});

const router = useRouter();
</script>

<template>
  <n-space justify="center" style="height: 100vh; align-items: center">
    <n-result
      :status="props.status"
      :title="props.title"
      :description="props.description"
    >
      <template #footer v-if="props.goTo">
        <n-button size="small" @click="router.push({ name: props.goTo })">
          {{ props.buttonText }}
        </n-button>
      </template>
    </n-result>
  </n-space>
</template>
