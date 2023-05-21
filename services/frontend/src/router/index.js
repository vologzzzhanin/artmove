import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../views/LoginPage.vue";
import UserRegistration from "../views/UserRegistration.vue";
import EmailConfirmation from "../views/EmailConfirmation.vue";
import PasswordUpdate from "../views/PasswordUpdate.vue";
import PasswordRestore from "../views/PasswordRestore.vue";
import HomeView from "../views/HomeView.vue";
import AnimationView from "../views/AnimationView.vue";
import ResultView from "../views/ResultView.vue";
import MainLayout from "../layouts/MainLayout.vue";
import EmptyLayout from "../layouts/EmptyLayout.vue";
import { useUserStore } from "@/store/modules/user";
import { resultProps } from "@/utils/results";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "root",
      redirect: "/login",
    },
    {
      path: "/register",
      name: "register",
      component: UserRegistration,
      meta: { layout: EmptyLayout, nonAuth: true },
    },
    {
      path: "/email_confirm",
      name: "email_confirm",
      component: EmailConfirmation,
      props: (route) => ({ token: route.query.token }),
      meta: { layout: EmptyLayout, nonAuth: true },
    },
    {
      path: "/login",
      name: "login",
      component: LoginPage,
      meta: { layout: EmptyLayout, nonAuth: true },
    },
    {
      path: "/update_password",
      name: "update_password",
      component: PasswordUpdate,
      props: (route) => ({ token: route.query.token }),
      meta: { layout: EmptyLayout, nonAuth: true },
    },
    {
      path: "/restore_password",
      name: "restore_password",
      component: PasswordRestore,
      meta: { layout: EmptyLayout, nonAuth: true },
    },
    {
      path: "/logout",
      name: "logout",
      redirect: "/login",
    },
    {
      path: "/animations",
      name: "home",
      component: HomeView,
      meta: { layout: MainLayout, keepAlive: true },
    },
    {
      path: "/animation/:id",
      name: "animation",
      component: AnimationView,
      meta: { layout: MainLayout, keepAlive: true },
    },
    {
      path: "/result",
      name: "result",
      component: ResultView,
      props: (route) => resultProps[route.query.code],
      meta: { layout: EmptyLayout, nonAuth: true },
    },
    {
      path: "/:pathMatch(.*)*",
      redirect: "/404",
    },
  ],
});

router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  if (!to.meta.nonAuth && userStore.isAuthenticated === "false")
    next({ name: "login" });
  else if (to.name === "login" && userStore.isAuthenticated === "true")
    next({ name: "home" });
  else next();
});

export default router;
