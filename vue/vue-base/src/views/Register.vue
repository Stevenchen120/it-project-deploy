<template>
  <div>
    <div class="background-overlay"></div>
    <div class="container">
      <header class="header">
        <div class="logo-container">
          <!-- 使用 router-link 导航到主页 -->
          <router-link to="/" class="logo-link">
            <img src="../assets/images/Logo.jpeg" alt="Logo" class="logo" />
          </router-link>
          <h1>Australian Dictionary of Biography</h1>
        </div>
        <div class="button-container">
          <router-link to="/Login" class="login-button">Login</router-link>
        </div>
      </header>

      <div class="form-container">
        <h2>Create an account</h2>
        <p>
          Please submit an email and username and create a password to create
          your account. You'll be asked to enter a code that will arrive in your
          inbox.
        </p>
        <form @submit.prevent="handleRegister">
          <label for="email">Email Address*</label>
          <input type="email" id="email" v-model="email" required />

          <label for="username">Create Username*</label>
          <input type="text" id="username" v-model="username" required />

          <label for="password">Create Password*</label>
          <div class="password-container">
            <input
              :type="showPassword ? 'text' : 'password'"
              id="password"
              v-model="password"
              minlength="6"
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
          <label for="password">Confirm Password*</label>
          <div class="password-container">
            <input
              :type="showPassword ? 'text' : 'password'"
              id="confirmPassword"
              v-model="confirmPassword"
              minlength="6"
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
          <p>Password must be at least 6 characters.</p>

          <button v-on:click.prevent="register" type="submit">
            Create Account
          </button>
        </form>
        <p class="sign-in-text">
          Already have an account?<router-link to="/Login">
            Sign in</router-link
          >
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import showMessage from "@/utils/message";
import axios from "axios";
export default {
  name: "Register",
  data: function () {
    return {
      email: "",
      username: "",
      password: "",
      confirmPassword: "",
      showPassword: false,
    };
  },
  methods: {
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },
    register() {
      const username = this.username;
      const password = this.password;
      const email = this.email;
      const confirmPassword = this.confirmPassword;
      if (email === "") {
        showMessage("email cannot be empty");
        return;
      }
      var emailRegex =
        /^(([^>()\[\]\\,,;:\s@"]+(\.[^<>()\[\]\\,,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      if (!emailRegex.test(email)) {
        showMessage("Email format error");
        return;
      }
      if (username === "") {
        showMessage("username cannot be empty");
        return;
      }
      if (password === "") {
        showMessage("password cannot be empty");
        return;
      }
      if (confirmPassword === "") {
        showMessage("confirmPassword cannot be empty");
        return;
      }
      if (password !== confirmPassword) {
        showMessage("Two passwords are inconsistent");
        return;
      }
      const formData = {
        username: username,
        password: password,
        email: email,
      };
      axios
        .post("/api/users/", formData)
        .then((response) => {
          showMessage(
            "Registration successful, activate account in email",
            "info"
          );
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
  },
};
</script>

<style scoped>
body,
html {
  margin: 0;
  padding: 0;
  font-family: "Inter", sans-serif;
  width: 100%;
  height: 100%;
  position: relative;
}

.background-overlay {
  background: url("@/assets/images/login_background.jpeg") no-repeat center
    center fixed;
  background-size: cover;
  opacity: 0.3;
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1;
}

/* Container */
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 20px;
  height: 100vh;
  position: relative;
  z-index: 1;
}

/* Header */
.header {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 0px 10px;
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
  margin-right: 10px;
}

h1 {
  font-family: "Playwrite CU", cursive;
  font-size: 1.2rem;
  color: #333;
  font-weight: 300;
}

.button-container {
  display: flex;
  align-items: center;
  margin-left: auto;
}

.login-button {
  background: none;
  color: #a52a2a;
  border: none;
  font-size: 18px;
  cursor: pointer;
  text-decoration: none;
  margin-right: 20px;
}

.login-button:hover {
  text-decoration: underline;
}

/* Form Container */
.form-container {
  background-color: rgba(255, 255, 255, 0.8);
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: left;
  width: 600px;
  margin-top: 70px;
  color :black;
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

input[type="text"],
input[type="email"],
input[type="password"] {
  width: calc(100% - 20px);
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 14px;
  box-sizing: border-box;
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
  margin-top: 10px;
  margin-left: auto;
  margin-right: auto;
  display: block;
}

button[type="submit"]:hover {
  background-color: #8b0000;
}

.form-container p a {
  color: #333;
  text-decoration: none;
  font-size: 14px;
}

.form-container p a:hover {
  text-decoration: underline;
}

.sign-in-text {
  width: 100%;
}
</style>
