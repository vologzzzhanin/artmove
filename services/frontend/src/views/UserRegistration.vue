<script setup>
import { ref } from "vue";
import { useUserStore } from "@/store/modules/user";
import { useAppStore } from "@/store/modules/app";
import CredentialsForm from "@/components/CredentialsForm.vue";
import FormHeader from "@/components/FormHeader.vue";
import { PersonAdd24Regular } from "@vicons/fluent";

const userStore = useUserStore();
const appStore = useAppStore();

const formRef = ref(null);
const setFormRef = (el) => {
  formRef.value = el;
};

const register = () => {
  formRef.value.validate(async (errors) => {
    if (!errors) {
      const { email, password, fullName } = formRef.value.model;
      await userStore.register(email, password, fullName);
    }
  });
};
</script>

<template>
  <n-space justify="center" style="height: 100vh; align-items: center">
    <n-card style="min-width: 25vw">
      <n-h3>Регистрация</n-h3>
      <n-divider />
      <CredentialsForm
        :fields="['email', 'password', 'fullName']"
        @approve="register"
        @set-form-ref="setFormRef"
      />
      <n-button
        block
        type="primary"
        size="large"
        secondary
        strong
        @click="register"
        :loading="appStore.isLoading"
      >
        <template #icon> <n-icon :component="PersonAdd24Regular" /> </template>
        Зарегистрироваться
      </n-button>
      <template #header>
        <FormHeader />
      </template>
    </n-card>
  </n-space>
</template>
