import axios from "axios";
import router from "@/router/index";
import { useUserStore } from "@/store/modules/user";
import { useAppStore } from "@/store/modules/app";

function createAxios() {
  // Сконфигурируем axios для использования по всему приложению
  const http = axios.create();

  http.defaults.xsrfCookieName = "csrftoken";
  http.defaults.xsrfHeaderName = "X-CSRFToken";
  http.defaults.withCredentials = true;
  http.defaults.baseURL = import.meta.env.ARTMOVE_API_URL;

  // Установка глобального индикатора загрузки
  http.interceptors.request.use((config) => {
    const appStore = useAppStore();
    appStore.setLoadingStatus(true);
    window.$loadingBar.start();
    return config;
  });

  // При получении 401 (Пользователь не авторизован на сервере)
  // снимаем также его авторизацию на фронтэнде, иначе фронт может зависнуть,
  // например, когда истекла сессия
  http.interceptors.response.use(
    (response) => {
      const appStore = useAppStore();
      appStore.setLoadingStatus(false);
      window.$loadingBar.finish();
      return response;
    },
    (error) => {
      const userStore = useUserStore();
      const appStore = useAppStore();
      appStore.setLoadingStatus(false);
      window.$loadingBar.error();

      if (!error.response) {
        window.$message.error("Сервер не отвечает");
        return Promise.reject(error);
      }

      if (error.response.status === 401) {
        userStore.handleLogout();
      } else if (error.response.status === 404) {
        router.push({ name: "404" });
      } else if (error.response.status === 500) {
        window.$message.error("Ошибка на сервере");
      } else {
        window.$message.error(error.response.data.detail);
      }

      return Promise.reject(error);
    }
  );

  return http;
}

export const http = createAxios();
