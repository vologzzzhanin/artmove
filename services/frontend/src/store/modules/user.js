import { defineStore } from "pinia";
import {
  loginUser,
  registerUser,
  getUserData,
  verifyUser,
  updatePassword,
  restorePassword,
} from "@/api/user";

export const useUserStore = defineStore("user", {
  state() {
    return {
      userData: {},
      isAuthenticated: localStorage.getItem("isAuthenticated") || "false",
    };
  },
  getters: {
    myId() {
      return this.userData.id;
    },
  },
  actions: {
    async login(email, password) {
      try {
        const User = new FormData();
        User.append("username", email);
        User.append("password", password);
        await loginUser(User);
        this.isAuthenticated = "true";
        localStorage.setItem("isAuthenticated", "true");
        this.router.push({ name: "home" });
      } catch (resp) {
        console.log(resp);
      }
    },
    async register(email, password, fullName) {
      this.$reset();
      try {
        await registerUser({ email, password, full_name: fullName });
        this.router.push({
          name: "result",
          query: { code: "userRegistrationSuccess" },
        });
      } catch (resp) {
        console.log(resp);
        this.router.push({
          name: "result",
          query: { code: "userRegistrationError" },
        });
      }
    },
    async verifyUser(token) {
      try {
        await verifyUser({ token });
        this.router.push({
          name: "result",
          query: { code: "userVerificationSuccess" },
        });
      } catch (resp) {
        console.log(resp);
        this.router.push({
          name: "result",
          query: { code: "userVerificationError" },
        });
      }
    },
    async getUserData() {
      try {
        let response = await getUserData();
        this.userData = response.data;
      } catch (resp) {
        console.log(resp);
        this.handleLogout();
      }
    },
    async restorePassword(email) {
      try {
        await restorePassword({ email });
        this.router.push({
          name: "result",
          query: { code: "passwordRestoreSuccess" },
        });
      } catch (resp) {
        console.log(resp);
        this.router.push({
          name: "result",
          query: { code: "passwordRestoreError" },
        });
      }
    },
    async updatePassword(token, password) {
      try {
        await updatePassword({ token, password });
        this.router.push({ name: "login" });
      } catch (resp) {
        console.log(resp);
        this.router.push({
          name: "result",
          query: { code: "passwordUpdateError" },
        });
      }
    },
    handleLogout() {
      localStorage.setItem("isAuthenticated", "false");
      this.$reset();
      this.router.push({ name: "logout" });
    },
    async logout() {
      // await logoutUser();
      this.handleLogout();
    },
  },
});
