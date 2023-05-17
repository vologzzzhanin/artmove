<script setup>
import { ref } from "vue";
import { Sparkle48Regular } from "@vicons/fluent";

const variant = ref("");
const options = [
  {
    label: "Левитация вверх-вниз",
    value: "levitateY",
  },
  {
    label: "Левитация влево-вправо",
    value: "levitateX",
  },
];

const emit = defineEmits(["adjust"]);
</script>

<template>
  <n-popselect
    v-model:value="variant"
    :options="options"
    placement="right"
    @update:value="emit('adjust', variant)"
  >
    <n-button text class="controls">
      <n-icon :component="Sparkle48Regular" />
    </n-button>
  </n-popselect>
</template>
