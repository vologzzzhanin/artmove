<script setup>
import { ref } from "vue";
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

const credentials = ref({
  email: "",
  password: "",
  fullName: "",
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
  fullName: {
    required: true,
    message: "Введите полное имя",
  },
};
const formRef = ref(null);

const register = () => {
  formRef.value.validate(async (errors) => {
    if (!errors) {
      await userStore.register(
        credentials.value.email,
        credentials.value.password,
        credentials.value.fullName
      );
    }
  });
};
</script>
<template>
  <n-space justify="center" style="height: 100vh; align-items: center">
    <n-card w-100 card-shadow bg-white bg-opacity-60>
      <n-form
        ref="formRef"
        :model="credentials"
        :rules="rules"
        :show-require-mark="false"
        @keyup.enter="register"
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
          >
            <template #prefix>
              <n-icon size="22" :component="Fingerprint24Regular" />
            </template>
          </n-input>
        </n-form-item>
        <n-form-item path="fullName" label="Полное имя">
          <n-input
            v-model:value="credentials.fullName"
            @keydown.enter.prevent
            placeholder="Введите полное имя"
            clearable
          >
            <template #prefix>
              <n-icon size="22" :component="Person24Regular" />
            </template>
          </n-input>
        </n-form-item>
      </n-form>
      <n-button
        block
        type="primary"
        secondary
        strong
        @click="register"
        :loading="appStore.isLoading"
      >
        <template #icon> <n-icon :component="PersonAdd24Regular" /> </template>
        Зарегистрироваться
      </n-button>
    </n-card>
  </n-space>
</template>
