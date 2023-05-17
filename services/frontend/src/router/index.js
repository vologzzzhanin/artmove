import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../views/LoginPage.vue";
import UserRegistration from "../views/UserRegistration.vue";
import EmailConfirmation from "../views/EmailConfirmation.vue";
import HomeView from "../views/HomeView.vue";
import AnimationView from "../views/AnimationView.vue";
import NotFound from "../views/NotFound.vue";
import MainLayout from "../layouts/MainLayout.vue";
import EmptyLayout from "../layouts/EmptyLayout.vue";
import { useUserStore } from "@/store/modules/user";

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
      meta: { layout: EmptyLayout },
    },
    {
      path: "/email_confirm",
      name: "email_confirm",
      component: EmailConfirmation,
      props: (route) => ({ token: route.query.token }),
      meta: { layout: EmptyLayout },
    },
    {
      path: "/login",
      name: "login",
      component: LoginPage,
      meta: { layout: EmptyLayout },
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
      meta: {
        layout: MainLayout,
        keepAlive: true,
      },
    },
    {
      path: "/animation/:id",
      name: "animation",
      component: AnimationView,
      meta: {
        layout: MainLayout,
        keepAlive: true,
      },
    },
    {
      path: "/404",
      name: "404",
      component: NotFound,
      meta: { layout: EmptyLayout },
    },
    {
      path: "/:pathMatch(.*)*",
      redirect: "/404",
    },
  ],
});

router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  let notAuthRoutes = ["login", "register", "email_confirm"];
  if (!notAuthRoutes.includes(to.name) && userStore.isAuthenticated === "false")
    next({ name: "login" });
  else if (to.name === "login" && userStore.isAuthenticated === "true")
    next({ name: "home" });
  else next();
});

export default router;
