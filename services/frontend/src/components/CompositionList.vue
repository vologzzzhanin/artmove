<script setup>
import { useAnimationsStore } from "@/store/modules/animations";
import {
  CaretDown24Regular,
  CaretUp24Regular,
  Delete48Regular,
} from "@vicons/fluent";

const animationsStore = useAnimationsStore();
</script>

<template>
  <n-card v-for="image in animationsStore.serverImages" :key="image.id" mb-4>
    <n-space align="center">
      {{ image.order }}
      <n-image :src="image.src" height="40" preview-disabled />
      <n-button-group vertical>
        <n-button text>
          <template #icon>
            <n-icon :component="CaretUp24Regular" />
          </template>
        </n-button>
        <n-button text>
          <template #icon>
            <n-icon :component="CaretDown24Regular" />
          </template>
        </n-button>
      </n-button-group>
      <n-slider
        v-model:value="image.opacity"
        :min="0"
        :max="1"
        :step="0.1"
        style="width: 50px"
      />
      <n-checkbox v-model:checked="image.enabled" />
      <n-button text>
        <template #icon>
          <n-icon size="24" :component="Delete48Regular" />
        </template>
      </n-button>
      <n-input v-model:value="image.title" />
    </n-space>
  </n-card>
</template>
