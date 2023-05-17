<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/store/modules/user";

const props = defineProps({
  token: { type: String },
});

const router = useRouter();
const userStore = useUserStore();

onMounted(async () => {
  await userStore.verifyUser(props.token);
});
</script>

<template>
  <n-space
    v-if="userStore.isVerified !== undefined"
    justify="center"
    style="height: 100vh; align-items: center"
  >
    <n-result
      v-if="userStore.isVerified"
      status="success"
      title="Адрес электронной почты подтвержден"
    >
      <template #footer>
        <n-button size="small" @click="router.push({ name: 'login' })">
          Авторизоваться
        </n-button>
      </template>
    </n-result>
    <n-result
      v-else
      status="403"
      title="Ошибка"
      description="Не удалось подтвердить адрес электронной почты"
    />
  </n-space>
</template>
