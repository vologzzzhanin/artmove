import { defineStore } from "pinia";
import { loginUser, registerUser, getUserData, verifyUser } from "@/api/user";

export const useUserStore = defineStore("user", {
  state() {
    return {
      userData: {},
      isAuthenticated: localStorage.getItem("isAuthenticated") || "false",
      isVerified: undefined,
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
      } catch (resp) {
        console.log(resp);
      }
    },
    async register(email, password, fullName) {
      this.$reset();
      try {
        await registerUser({ email, password, full_name: fullName });
        await this.login(email, password);
        this.router.push({ name: "home" });
      } catch (resp) {
        console.log(resp);
      }
    },
    async verifyUser(token) {
      try {
        await verifyUser({ token });
        this.isVerified = true;
      } catch (resp) {
        this.isVerified = false;
        console.log(resp);
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
