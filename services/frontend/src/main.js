import "@/styles/main.scss";
import "uno.css";

import { createApp } from "vue";
import { setupStore } from "@/store";
import { MotionPlugin } from "@vueuse/motion";

import App from "./App.vue";
import router from "./router";
import naive from "naive-ui";

const app = createApp(App);

setupStore(app);
app.use(router);
app.use(naive);
app.use(MotionPlugin);

app.mount("#app");
