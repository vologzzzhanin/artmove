import { http } from "@/utils/http";

export const registerUser = (data) => {
  return http.post("/register", data);
};

export const verifyUser = (data) => {
  return http.post("/email_confirm", data);
};

export const loginUser = (data) => {
  return http.post("/login", data);
};

export const getUserData = () => {
  return http.get("/users/whoami");
};

export const updatePassword = (data) => {
  return http.post("/update_password", data);
};

export const restorePassword = (data) => {
  return http.post("/restore_password", data);
};
