<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/store/modules/user";
import { useAppStore } from "@/store/modules/app";
import {
  Person24Regular,
  PersonAdd24Regular,
  MailOpenPerson24Regular,
  Fingerprint24Regular,
} from "@vicons/fluent";

const userStore = useUserStore();
const appStore = useAppStore();
const router = useRouter();

const credentials = ref({
  email: "",
  password: "",
});
const rules = {
  email: {
    required: true,
    message: "Введите email",
  },
  password: {
    required: true,
    message: "Введите пароль",
  },
};
const formRef = ref(null);

const login = () => {
  formRef.value.validate(async (errors) => {
    if (!errors) {
      await userStore.login(
        credentials.value.email,
        credentials.value.password
      );
      // Go to home page
      router.push({ name: "home" });
    }
  });
};

const goToRegistration = () => {
  router.push({ name: "register" });
};
</script>
<template>
  <n-space justify="center" style="height: 100vh; align-items: center">
    <n-card>
      <n-form
        ref="formRef"
        :model="credentials"
        :rules="rules"
        :show-require-mark="false"
        @keyup.enter="login"
      >
        <n-form-item path="email" label="Электронная почта">
          <n-input
            v-model:value="credentials.email"
            @keydown.enter.prevent
            placeholder="Email"
            clearable
          >
            <template #prefix>
              <n-icon size="22" :component="MailOpenPerson24Regular" />
            </template>
          </n-input>
        </n-form-item>
        <n-form-item path="password" label="Пароль">
          <n-input
            v-model:value="credentials.password"
            type="password"
            @keydown.enter.prevent
            show-password-on="mousedown"
            placeholder="Пароль"
            ><template #prefix>
              <n-icon size="22" :component="Fingerprint24Regular" />
            </template>
          </n-input>
        </n-form-item>
      </n-form>
      <n-button
        block
        type="primary"
        secondary
        strong
        @click="login"
        :loading="appStore.isLoading"
      >
        <template #icon> <n-icon :component="Person24Regular" /> </template>
        Вход
      </n-button>
      <n-button block type="primary" secondary strong @click="goToRegistration">
        <template #icon> <n-icon :component="PersonAdd24Regular" /> </template>
        Регистрация
      </n-button>
    </n-card>
  </n-space>
</template>
