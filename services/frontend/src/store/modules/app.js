import { defineStore } from "pinia";

export const useAppStore = defineStore("app", {
  state() {
    return {
      isLoading: false,
    };
  },
  actions: {
    setLoadingStatus(isLoading) {
      this.isLoading = isLoading;
    },
  },
});
