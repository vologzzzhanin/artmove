<script setup>
import { ref } from "vue";
import { useUserStore } from "@/store/modules/user";
import { useAppStore } from "@/store/modules/app";
import CredentialsForm from "@/components/CredentialsForm.vue";
import FormHeader from "@/components/FormHeader.vue";
import { Password24Filled } from "@vicons/fluent";

const props = defineProps({
  token: { type: String },
});

const userStore = useUserStore();
const appStore = useAppStore();

const formRef = ref(null);
const setFormRef = (el) => {
  formRef.value = el;
};

const updatePassword = () => {
  formRef.value.validate(async (errors) => {
    if (!errors) {
      const { password } = formRef.value.model;
      await userStore.updatePassword(props.token, password);
    }
  });
};
</script>

<template>
  <n-space justify="center" style="height: 100vh; align-items: center">
    <n-card style="min-width: 25vw">
      <n-h3>Обновление пароля</n-h3>
      <n-divider />
      <CredentialsForm
        :fields="['password']"
        :labels="{ password: 'Новый пароль' }"
        @approve="updatePassword"
        @set-form-ref="setFormRef"
      />
      <n-button
        block
        type="primary"
        size="large"
        secondary
        strong
        @click="updatePassword"
        :loading="appStore.isLoading"
      >
        <template #icon>
          <n-icon :component="Password24Filled" />
        </template>
        Обновить пароль
      </n-button>
      <template #header>
        <FormHeader />
      </template>
    </n-card>
  </n-space>
</template>
