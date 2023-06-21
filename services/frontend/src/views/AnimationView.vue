<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { useAnimationsStore } from "@/store/modules/animations";
import { leftControls, rightControls } from "@/utils/controls";
import MotionView from "@/components/MotionView.vue";
import CompositionList from "@/components/CompositionList.vue";
// import {
//   useMotionProperties,
//   useMotionControls,
//   useMotionTransitions,
// } from "@vueuse/motion";

const animationsStore = useAnimationsStore();
const route = useRoute();

onMounted(async () => {
  let animationId = route.params.id;
  await animationsStore.loadAnimation(animationId);
});

const motionRef = ref(null);
const showComposition = ref(false);

const controlActions = {
  adjust: () => {
    console.log("adjust");
  },
  showComposition: () => {
    showComposition.value = true;
  },
  refresh: () => {
    motionRef.value.refresh();
  },
  saveTitle: async (title) => {
    await animationsStore.updateAnimation({ title }, true);
    animationsStore.currentAnimation.title = title;
  },
  saveBackground: async () => {
    let background = animationsStore.currentAnimation.background;
    await animationsStore.updateAnimation({ background }, true);
  },
};

const imageMotions = ref({});
const onInitImageMotions = (motions) => {
  imageMotions.value = motions;
};

const visibleImages = computed(() => {
  return animationsStore.serverImages.map((comp) => {
    if (comp.options?.visible) return comp;
  });
});

// TODO изменение анимации на лету
// const motionChange = async () => {
//   let motionProperties = imageMotions.value["image0"].motionProperties;

//   const { push, stop } = useMotionTransitions();

//   stop();
//   motionProperties.x = 0;
//   motionProperties.y = 0;
//   push("x", 25, motionProperties, {
//     duration: 2000,
//     repeat: Infinity,
//     ease: "easeInOut",
//     repeatType: "mirror",
//   });
//   // await imageMotions.value["image0"].stopTransitions();
//   // await imageMotions.value["image0"].apply("levitateX");
// };
</script>

<template>
  <n-space h-full w-full>
    <n-space vertical justify="space-between" style="height: 50%">
      <component
        v-for="control in leftControls"
        :key="control.title"
        :is="control.component"
        v-on="controlActions"
      />
    </n-space>
    <n-space justify="center" class="motion">
      <MotionView
        ref="motionRef"
        :images="visibleImages"
        :background="animationsStore.currentAnimation.background"
        @init-image-motions="onInitImageMotions"
      />
    </n-space>
    <n-space vertical justify="space-between" style="height: 40%">
      <component
        v-for="control in rightControls"
        :key="control.title"
        :is="control.component"
        v-on="controlActions"
      />
    </n-space>
  </n-space>
  <n-drawer v-model:show="showComposition" width="40%" placement="right">
    <n-drawer-content title="Композиция">
      <CompositionList />
    </n-drawer-content>
  </n-drawer>
</template>

<style scoped lang="scss">
.motion {
  width: calc(100vw - $controls-width - 2 * $layout-padding - $rest-width);
}
</style>
