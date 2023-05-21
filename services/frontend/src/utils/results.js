export const resultProps = {
  error: {
    status: "error",
    title: "Ошибка",
  },
  ["404"]: {
    status: "404",
    title: "Страница не найдена",
    goTo: "root",
    buttonText: "Вернуться в приложение",
  },
  userRegistrationSuccess: {
    status: "success",
    title: "Успешно",
    description:
      "На указанный адрес электронной почты отправлена ссылка для подтверждения регистрации",
  },
  userRegistrationError: {
    status: "error",
    title: "Ошибка",
    goTo: "register",
    buttonText: "Попробовать еще раз",
  },
  userVerificationSuccess: {
    status: "success",
    title: "Успешно",
    description: "Адрес электронной почты подтвержден",
    goTo: "login",
    buttonText: "Авторизоваться",
  },
  userVerificationError: {
    status: "error",
    title: "Ошибка",
    description: "Не удалось обновить подтвердить регистрацию",
  },
  passwordRestoreSuccess: {
    status: "success",
    title: "Успешно",
    description:
      "На указанный адрес электронной почты отправлена ссылка для восстановления пароля",
  },
  passwordRestoreError: {
    status: "error",
    title: "Ошибка",
    goTo: "restore_password",
    buttonText: "Попробовать еще раз",
  },
  passwordUpdateError: {
    status: "error",
    title: "Ошибка",
    description: "Не удалось обновить пароль",
    goTo: "restore_password",
    buttonText: "Попробовать еще раз",
  },
};
