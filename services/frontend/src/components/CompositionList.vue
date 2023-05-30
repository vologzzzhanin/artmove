<script setup>
import { useAnimationsStore } from "@/store/modules/animations";
import {
  CaretDown24Regular,
  CaretUp24Regular,
  Delete48Regular,
} from "@vicons/fluent";

const animationsStore = useAnimationsStore();

const moveImage = async ({ id }, fromIndex, toIndex) => {
  await animationsStore.moveImage(id, fromIndex, toIndex);
};
const deleteImage = async ({ id }) => {
  await animationsStore.deleteImage(id);
};
const updateComposition = async () => {
  await animationsStore.updateComposition();
};
</script>

<template>
  <n-card v-for="(el, index) in animationsStore.serverImages" :key="el.id" mb-4>
    <n-space align="center">
      {{ el.order }}
      <n-image :src="el.src" height="40" preview-disabled />
      <n-button-group vertical>
        <n-button
          text
          @click="moveImage(el, index, index - 1)"
          :disabled="index === 0"
        >
          <template #icon>
            <n-icon :component="CaretUp24Regular" />
          </template>
        </n-button>
        <n-button
          text
          @click="moveImage(el, index, index + 1)"
          :disabled="index === animationsStore.serverImages.length - 1"
        >
          <template #icon>
            <n-icon :component="CaretDown24Regular" />
          </template>
        </n-button>
      </n-button-group>
      <n-slider
        v-model:value="el.options.opacity"
        :min="0.1"
        :max="1"
        :step="0.1"
        :disabled="!el.options.visible"
        style="width: 50px"
        @update:value="updateComposition"
      />
      <n-checkbox
        v-model:checked="el.options.visible"
        @update:value="updateComposition"
      />
      <n-button text @click="deleteImage(el)">
        <template #icon>
          <n-icon size="24" :component="Delete48Regular" />
        </template>
      </n-button>
      <n-input
        v-model:value="el.image.title"
        @update:value="updateComposition"
      />
    </n-space>
  </n-card>
</template>
