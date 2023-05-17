<script setup>
import { onActivated } from "vue";
import { useAnimationsStore } from "@/store/modules/animations";
import MotionView from "@/components/MotionView.vue";

const animationsStore = useAnimationsStore();
const acceptFormats = ".png";

onActivated(() => {
  animationsStore.currentAnimation = {}; // TODO здесь должен быть другой объект, мб newAnimation?
});

const emit = defineEmits({
  closeModal: null,
});

const createAnimation = async () => {
  await animationsStore.createAnimation();
  emit("closeModal");
};
</script>

<template>
  <n-card
    style="width: 600px"
    :bordered="false"
    size="huge"
    role="dialog"
    aria-modal="true"
  >
    <n-scrollbar style="max-height: 200px">
      <n-upload
        v-model:file-list="animationsStore.images"
        multiple
        :accept="acceptFormats"
        :default-upload="false"
        :max="50"
        list-type="image-card"
        directory-dnd
      />
    </n-scrollbar>
    <MotionView
      v-if="animationsStore.images.length"
      :images="animationsStore.clientImages"
      :width="520"
    />
    <template #header>
      <n-input
        v-model:value="animationsStore.currentAnimation.title"
        type="text"
        placeholder="Новая анимация"
      />
    </template>
    <template #footer>
      <n-space justify="space-between">
        <n-button strong secondary type="primary" @click="createAnimation">
          Сохранить и продолжить редактирование
        </n-button>
        <n-button type="error" dashed @click="emit('closeModal')">
          Отмена
        </n-button>
      </n-space>
    </template>
  </n-card>
</template>
