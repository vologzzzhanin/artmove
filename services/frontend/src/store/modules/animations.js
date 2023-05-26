import { defineStore } from "pinia";
import {
  loadAnimation,
  createAnimation,
  updateAnimation,
  deleteAnimation,
  getAnimationsList,
} from "@/api/animations";
import { getImageURL } from "@/utils/urls";

export const useAnimationsStore = defineStore("animations", {
  state() {
    return {
      animations: [],
      currentAnimation: {
        title: "",
        composition: [],
        background: "",
      },
      images: [],
    };
  },
  getters: {
    serverImages(state) {
      return state.currentAnimation.composition
        .sort((a, b) => {
          return a.order - b.order;
        })
        .map((comp) => {
          let src = getImageURL(comp.image.img);
          const { order, options } = comp;
          return { ...comp.image, order, options, src };
        });
    },
    clientImages(state) {
      return state.images.map((image) => {
        let src = URL.createObjectURL(image.file);
        return { src };
      });
    },
    animationsList(state) {
      return state.animations.map((animation) => {
        let src = animation.thumbnail?.img
          ? getImageURL(animation.thumbnail.img)
          : "/public/logo.png";
        return { ...animation, src };
      });
    },
  },
  actions: {
    async getAnimationsList() {
      try {
        let response = await getAnimationsList();
        this.animations = response.data;
      } catch (e) {
        console.log(e);
      }
    },
    async loadAnimation(animationId) {
      try {
        let response = await loadAnimation(animationId);
        this.currentAnimation = response.data;
      } catch (e) {
        console.log(e);
      }
    },
    async createAnimation() {
      let data = new FormData();
      data.append(
        "animation",
        JSON.stringify({
          title: this.currentAnimation.title || "Новая анимация",
        })
      );
      this.images.forEach((image) => {
        data.append("images", image.file, image.name);
      });
      try {
        let response = await createAnimation(data);
        this.currentAnimation = response.data;
        this.images = [];
        await this.getAnimationsList();
      } catch (e) {
        console.log(e);
      }
    },
    async updateAnimation(payload, soft = false) {
      try {
        let response = await updateAnimation(this.currentAnimation.id, payload);
        if (!soft) this.currentAnimation = response.data;
      } catch (e) {
        console.log(e);
      }
    },
    async deleteAnimation(animationId) {
      try {
        await deleteAnimation(animationId);
        this.$reset;
        await this.getAnimationsList();
      } catch (e) {
        console.log(e);
      }
    },
  },
});
