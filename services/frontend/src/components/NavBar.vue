<script setup>
import { useRouter } from "vue-router";
import { getActivePinia } from "pinia";
import { useUserStore } from "@/store/modules/user";
import { Person24Regular, SignOut24Regular } from "@vicons/fluent";

const userStore = useUserStore();
const router = useRouter();

const logout = async () => {
  await userStore.logout();
  // очистить данные всех хранилищ
  getActivePinia()._s.forEach((store) => store.$reset());
  router.push({
    name: "logout",
  });
};
</script>

<template>
  <n-grid :cols="3" h-full>
    <n-gi>
      <n-space align="center" h-full pl-5>
        <n-image height="42" src="/public/logo.png" preview-disabled />
      </n-space>
    </n-gi>
    <n-gi>
      <n-space justify="center" align="center" h-full>
        <n-h2 m-0>ART:move</n-h2>
      </n-space>
    </n-gi>
    <n-gi>
      <n-space justify="end" align="center" h-full pr-4>
        <n-icon size="22" :component="Person24Regular" />
        {{ userStore.userData.full_name }}
        <n-button dashed @click="logout">
          Выход
          <template #icon> <n-icon :component="SignOut24Regular" /> </template>
        </n-button>
      </n-space>
    </n-gi>
  </n-grid>
</template>
