<script setup>
import { computed, getCurrentInstance, onBeforeUpdate, onUpdated } from "vue";
import { initialMotion } from "@/utils/motions";

const props = defineProps({
  images: { type: Array },
  motion: { type: Function, default: initialMotion },
  width: { type: Number, required: false },
  aspectRatio: { type: Number, default: 1.25 },
  background: { type: String, default: "" },
});

const emit = defineEmits({
  initImageMotions: (value) => typeof value === "object",
});

let imageRefs = [];
onBeforeUpdate(() => {
  imageRefs = [];
});

const setImageRef = (el) => {
  if (el) imageRefs.push(el);
};

onUpdated(() => {
  if (imageRefs.length < props.images.length) return;
  let imageMotions = {};
  imageRefs.forEach((ref, index) => {
    imageMotions["image" + index] = props.motion(ref, index);
  });
  emit("initImageMotions", imageMotions);
});

const usedHeight = 120; // Found by trial and error method
const dimensions = computed(() => {
  if (props.width) {
    return {
      width: props.width + "px",
      height: props.width * props.aspectRatio + "px",
    };
  } else {
    let height =
      Math.max(document.documentElement.clientHeight, window.innerHeight || 0) -
      usedHeight;
    return {
      width: height / props.aspectRatio + "px",
      height: height + "px",
    };
  }
});

const instance = getCurrentInstance();
const refresh = () => {
  instance.proxy.$forceUpdate();
};

defineExpose({ refresh });
</script>

<template>
  <div class="animotion">
    <n-image
      v-for="(image, index) in props.images"
      :ref="setImageRef"
      :key="index"
      :src="image.src"
      preview-disabled
      class="overlay"
    />
  </div>
</template>

<style>
.animotion {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  position: relative;
  width: v-bind("dimensions.width");
  height: v-bind("dimensions.height");
  background-color: v-bind("props.background");
}
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
</style>
