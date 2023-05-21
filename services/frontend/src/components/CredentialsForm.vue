<script setup>
import { computed, onBeforeMount, onMounted, ref } from "vue";
import {
  Person24Regular,
  MailOpenPerson24Regular,
  Password24Regular,
} from "@vicons/fluent";

const props = defineProps({
  fields: { type: Array },
  labels: {
    type: Object,
    default: () => {
      return {
        email: "Электронная почта",
        password: "Пароль",
        fullName: "Полное имя",
      };
    },
  },
});

const credentials = ref({
  email: "",
  password: "",
  fullName: "",
});

const fieldSet = {
  email: {
    fieldProps: { placeholder: "Email", clearable: true },
    icon: MailOpenPerson24Regular,
    required: true,
    message: "Введите email",
  },
  password: {
    fieldProps: {
      placeholder: "Пароль",
      type: "password",
      showPasswordOn: "mousedown",
    },
    icon: Password24Regular,
    required: true,
    message: "Введите пароль",
  },
  fullName: {
    fieldProps: { placeholder: "Полное имя", clearable: true },
    icon: Person24Regular,
    required: true,
    message: "Введите полное имя",
  },
};

const rules = computed(() => {
  let formRules = {};
  for (const [key, value] of Object.entries(fieldSet)) {
    if (props.fields.includes(key)) {
      const { required, message } = value;
      formRules[key] = { required, message };
    }
  }
  return formRules;
});
const items = computed(() => {
  let formItems = {};
  for (const [key, value] of Object.entries(fieldSet)) {
    if (props.fields.includes(key)) {
      let label = props.labels[key];
      const { fieldProps, icon } = value;
      formItems[key] = { props: fieldProps, icon, label, key };
    }
  }
  return formItems;
});

let formRef = null;
const setFormRef = (el) => {
  if (el) formRef = el;
};
onMounted(() => {
  emit("setFormRef", formRef);
});
onBeforeMount(() => {
  formRef = null;
});

const emit = defineEmits({
  approve: null,
  setFormRef: (el) => typeof el === "object",
});
</script>

<template>
  <n-form
    :ref="setFormRef"
    :model="credentials"
    :rules="rules"
    :show-require-mark="false"
    @keyup.enter="emit('approve')"
  >
    <n-form-item
      v-for="item in items"
      :key="item.key"
      :path="item.key"
      :label="item.label"
    >
      <n-input
        v-model:value="credentials[item.key]"
        v-bind="item.props"
        size="large"
        @keydown.enter.prevent
      >
        <template #prefix>
          <n-icon size="22" :component="item.icon" />
        </template>
      </n-input>
    </n-form-item>
  </n-form>
</template>
