<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/store/modules/user";
import { useAppStore } from "@/store/modules/app";
import CredentialsForm from "@/components/CredentialsForm.vue";
import FormHeader from "@/components/FormHeader.vue";
import {
  Person24Regular,
  PersonAdd24Regular,
  Fingerprint24Regular,
} from "@vicons/fluent";

const userStore = useUserStore();
const appStore = useAppStore();
const router = useRouter();

const formRef = ref(null);
const setFormRef = (el) => {
  formRef.value = el;
};

const login = async () => {
  formRef.value.validate(async (errors) => {
    if (!errors) {
      const { email, password } = formRef.value.model;
      await userStore.login(email, password);
    }
  });
};

const goToRegistration = () => {
  router.push({ name: "register" });
};
const goToRestorePassword = () => {
  router.push({ name: "restore_password" });
};
</script>

<template>
  <n-space justify="center" style="height: 100vh; align-items: center">
    <n-card style="min-width: 25vw">
      <CredentialsForm
        :fields="['email', 'password']"
        @approve="login"
        @set-form-ref="setFormRef"
      />
      <n-button
        block
        type="primary"
        size="large"
        secondary
        strong
        @click="login"
        :loading="appStore.isLoading"
      >
        <template #icon> <n-icon :component="Person24Regular" /> </template>
        Вход
      </n-button>
      <n-divider />
      <n-space justify="space-between">
        <n-button text @click="goToRegistration">
          <template #icon>
            <n-icon :component="PersonAdd24Regular" />
          </template>
          Регистрация
        </n-button>
        <n-button text @click="goToRestorePassword">
          <template #icon>
            <n-icon :component="Fingerprint24Regular" />
          </template>
          Восстановить пароль
        </n-button>
      </n-space>
      <template #header>
        <FormHeader />
      </template>
    </n-card>
  </n-space>
</template>
