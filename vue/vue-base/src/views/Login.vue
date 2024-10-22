<template>
  <div>
    <div class="background-overlay"></div>
    <div class="container">
      <header class="header">
        <div class="logo-container">
          <router-link to="/" class="logo-link">
            <img src="../assets/images/Logo.jpeg" alt="Logo" class="logo" />
          </router-link>
          <h1>Australian Dictionary of Biography</h1>
        </div>
      </header>

      <div class="login-container">
        <h2>LOG IN</h2>
        <p>
          Welcome to AUSTRALIAN DICTIONARY OF BIOGRAPHY!<br />Please log in to
          join the conversation
        </p>
        <form @submit.prevent="handleLogin">
          <label for="usename">Uername</label>
          <input
            type="username"
            id="username"
            v-model="username"
            placeholder="Enter your username"
            required
          />

          <label for="password">Password</label>
          <div class="password-container">
            <input
              :type="passwordFieldType"
              id="password"
              v-model="password"
              placeholder="Enter your password"
              required
            />
            <button
              type="button"
              class="show-password"
              @click="togglePasswordVisibility"
            >
              <svg
                class="eye-icon"
                viewBox="0 0 24 24"
                width="24"
                height="24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
            </button>
          </div>

          <button v-on:click.prevent="submitFrom" type="submit">Log In</button>
        </form>
        <div class="login-footer">
          <router-link to="/register">Create an Account</router-link>
          <router-link to="/reset_password">Forget password?</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import showMessage from "@/utils/message";
export default {
  data() {
    return {
      username: "",
      password: "",
      showPassword: false,
    };
  },
  computed: {
    passwordFieldType() {
      return this.showPassword ? "text" : "password";
    },
  },
  methods: {
    submitFrom() {
      const username = this.username;
      const password = this.password;
      if (username === "") {
        showMessage("username cannot be empty");
        return;
      }
      if (password === "") {
        showMessage("password cannot be empty");
        return;
      }
      const formData = {
        username: username,
        password: password,
      };
      axios
        .post("/api/jwt/create/", formData)
        .then((response) => {
          const token = response.data.access;
          const refreshToken = response.data.refresh;
          const username = this.username;
          localStorage.setItem("token", token);
          localStorage.setItem("refreshToken", refreshToken);
          localStorage.setItem("username", username);
          console.log("Token saved to localStorage", token);
          localStorage.setItem("expiredTime", Date.now() + 5 * 60 * 1000);
          showMessage("Login successful", "info", () => {
            this.$router.push({ name: "home" });
          });
        })
        .catch((error) => {
          console.log(error);
          const errorData = error.response.data;
          const errorMessage = Object.values(errorData).flat();
          for (let i = 0; i < errorMessage.length; i++) {
            showMessage(errorMessage[i]);
          }
        });
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },
    handleLogin() {
      // Handle login logic here, e.g., form submission, validation
      console.log("Username:", this.username);
      console.log("Password:", this.password);
    },
  },
};
</script>

<style scoped>
/* General Styles */

body,
html {
  margin: 0;
  padding: 0;
  font-family: "Inter", sans-serif;
  width: 100%;
  height: 100%; /* 确保页面高度为 100% */
  overflow: hidden; /* 防止出现滚动条 */
  position: relative;
}

.background-overlay {
  background: url("@/assets/images/login_background.jpeg") no-repeat center
    center fixed;
  background-size: cover;
  background-attachment: fixed;
  opacity: 0.7;
  width: 100%;
  height: 100%;
  position: fixed; /* 改成 fixed */
  top: 0;
  left: 0;
  z-index: -1;
}

/* Container */
.container {
  box-sizing: border-box;
  position: relative;
  width: 100%;
  max-width: 1440px;
  height: 100vh; /* 确保容器高度占满整个视口 */
  margin: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* Header */
.header {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 0px 10px;
  /* Reduced padding for smaller header */
  background-color: rgba(255, 255, 255, 0.8);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  z-index: 10;
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  height: 50px;
  /* Smaller logo size */
  margin-right: 10px;
}

h1 {
  font-family: "Playwrite CU", cursive;
  font-size: 1.2rem;
  color: #333;
  font-weight: 300;
}

/* Login Form Container */
.login-container {
  background-color: rgba(255, 255, 255, 0.8);
  /* 增加透明度 */
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 500px;
  margin-top: 70px;
  position: relative;
  z-index: 1;
}

span {
  color: #a52a2a;
  margin-right: 15px;
}

h2 {
  font-size: 35px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #333;
}

p {
  font-size: 14px;
  color: #333;
  margin-bottom: 20px;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

label {
  text-align: left;
  width: 100%;
  margin-bottom: 5px;
  font-size: 14px;
  color: #333;
}

input[type="username"] {
  width: 100%;
  padding: 10px;
  padding-right: 40px;
  /* Add padding to avoid overlapping with icon */
  margin-bottom: 15px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 14px;
  box-sizing: border-box;
}

input[type="password"],
input[type="text"] {
  /* 对密码和文本输入框应用相同的样式 */
  width: 100%;
  padding: 10px;
  padding-right: 40px;
  margin-bottom: 15px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 14px;
  box-sizing: border-box;
}

.password-container {
  display: flex;
  align-items: center;
  width: 100%;
  position: relative;
}

.show-password {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  margin-left: -30px;
  /* 根据你的图标大小和间距进行调整 */
  margin-top: -10px;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.eye-icon {
  width: 20px;
  height: 20px;
}

button[type="submit"] {
  background-color: #a52a2a;
  color: white;
  border: none;
  padding: 10px;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  width: 50%;
  margin-top: 20px;
  margin-left: auto;
  margin-right: auto;
  display: block;
  text-align: center;
  text-decoration: none;
  text-transform: uppercase;
  font-weight: bold;
}

button[type="submit"]:hover {
  background-color: #8b0000;
}

.login-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.login-footer a {
  color: #333;
  font-size: 15px;
  text-decoration: none;
}

.login-footer a:hover {
  text-decoration: underline;
}
</style>
