import { createPinia } from "pinia";
import { markRaw } from "vue";
import router from "@/router";

export function setupStore(app) {
  const pinia = createPinia();
  pinia.use(({ store }) => {
    store.router = markRaw(router);
  });
  app.use(pinia);
}
