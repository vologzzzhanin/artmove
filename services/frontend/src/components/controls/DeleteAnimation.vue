<script setup>
import { useRoute, useRouter } from "vue-router";
import { useAnimationsStore } from "@/store/modules/animations";
import { Delete48Regular } from "@vicons/fluent";

const route = useRoute();
const router = useRouter();
const animationsStore = useAnimationsStore();

const deleteAnimation = async () => {
  let animationId = route.params.id;
  await animationsStore.deleteAnimation(animationId);
  router.push({ name: "home" });
};
</script>

<template>
  <n-popconfirm :negative-text="null" @positive-click="deleteAnimation">
    <template #trigger>
      <n-button text class="controls">
        <n-icon :component="Delete48Regular" />
      </n-button>
    </template>
    Вы уверены, что хотите удалить анимацию?
  </n-popconfirm>
</template>
