<script setup>
import { ref } from "vue";
import { useUserStore } from "@/store/modules/user";
import { useAppStore } from "@/store/modules/app";
import CredentialsForm from "@/components/CredentialsForm.vue";
import FormHeader from "@/components/FormHeader.vue";
import { MailCheckmark20Regular } from "@vicons/fluent";

const userStore = useUserStore();
const appStore = useAppStore();

const formRef = ref(null);
const setFormRef = (el) => {
  formRef.value = el;
};

const restorePassword = () => {
  formRef.value.validate(async (errors) => {
    if (!errors) {
      const { email } = formRef.value.model;
      await userStore.restorePassword(email);
    }
  });
};
</script>

<template>
  <n-space justify="center" style="height: 100vh; align-items: center">
    <n-card style="min-width: 25vw">
      <n-h3>Восстановление пароля</n-h3>
      <n-divider />
      <CredentialsForm
        :fields="['email']"
        @approve="restorePassword"
        @set-form-ref="setFormRef"
      />
      <n-button
        block
        type="primary"
        size="large"
        secondary
        strong
        @click="restorePassword"
        :loading="appStore.isLoading"
      >
        <template #icon>
          <n-icon :component="MailCheckmark20Regular" />
        </template>
        Подтвердить
      </n-button>
      <template #header>
        <FormHeader />
      </template>
    </n-card>
  </n-space>
</template>
