<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAnimationsStore } from "@/store/modules/animations";
import { Add28Regular } from "@vicons/fluent";
import NewAnimation from "@/components/NewAnimation.vue";
import { motionButtonGlow } from "@/utils/motions";

const router = useRouter();
const animationsStore = useAnimationsStore();

const showModal = ref(false);

const selectAnimation = async (animationId) => {
  await router.push({ name: "animation", params: { id: animationId } });
};
</script>

<template>
  <n-grid x-gap="24" y-gap="24" :cols="4" style="padding: 24px">
    <n-gi>
      <n-button
        v-motion="motionButtonGlow"
        dashed
        @click="showModal = true"
        size="large"
        style="width: 100%; min-height: 85.4px"
      >
        <template #icon>
          <n-icon :component="Add28Regular" size="32" />
        </template>
        Добавить
      </n-button>
    </n-gi>
    <n-gi
      v-for="animation in animationsStore.animationsList"
      :key="animation.id"
    >
      <n-card
        hoverable
        style="cursor: pointer"
        size="huge"
        @click="selectAnimation(animation.id)"
      >
        <template #cover>
          <n-space justify="center" w-full>
            <n-image :src="animation.src" preview-disabled />
          </n-space>
        </template>
        <template #header>
          <n-ellipsis :line-clamp="1">
            {{ animation.title }}
          </n-ellipsis>
        </template>
      </n-card>
    </n-gi>
  </n-grid>
  <n-modal v-model:show="showModal" :mask-closable="false">
    <NewAnimation @close-modal="showModal = false" />
  </n-modal>
</template>
