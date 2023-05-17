<script setup>
import { ref } from "vue";
import { useAnimationsStore } from "@/store/modules/animations";
import { Rename28Regular, Save24Regular } from "@vicons/fluent";

const title = ref("");

const animationsStore = useAnimationsStore();
const getTitle = (show) => {
  if (show) title.value = animationsStore.currentAnimation.title;
};

const emit = defineEmits({
  saveTitle: (title) => typeof title === "string",
});
</script>

<template>
  <n-popover trigger="click" placement="right" @update:show="getTitle">
    <template #trigger>
      <n-button text class="controls">
        <n-icon :component="Rename28Regular" />
      </n-button>
    </template>
    <n-input-group>
      <n-input
        v-model:value="title"
        size="large"
        :style="{ minWidth: '350px' }"
        placeholder="Введите название для анимации"
      />
      <n-button
        size="large"
        type="primary"
        ghost
        @click="emit('saveTitle', title)"
      >
        <n-icon size="24" :component="Save24Regular" />
      </n-button>
    </n-input-group>
  </n-popover>
</template>
