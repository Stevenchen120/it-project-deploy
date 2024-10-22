<template>
  <!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>Australian Dictionary of Biography - Forget Password</title>
      <link rel="icon" href="../static/favicon.ico" />
      <link rel="stylesheet" href="forget_pw.css" />
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link rel="preconnect" href="https://fonts.gstatic.com" />
      <link
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Playwrite+CU:wght@100..400&display=swap"
        rel="stylesheet"
      />
    </head>

    <body>
      <div class="background-overlay"></div>
      <div class="container">
        <header class="header">
          <div class="logo-container">
            <a href="home_page.html">
              <img src="../assets/images/Logo.jpeg" alt="Logo" class="logo" />
            </a>
            <h1>Australian Dictionary of Biography</h1>
          </div>
          <div class="button-container">
            <a href="login.html" class="login-button">Login</a>
            <span>|</span>
            <a href="register_page.html" class="register-button">Register</a>
          </div>
        </header>

        <div class="forget-password-container">
          <h2>Forget your password?</h2>
          <p>
            Enter your email address and we’ll send the link to reset your
            passwords
          </p>
          <form>
            <label for="email">Email:</label>
            <div class="email-container">
              <input
                type="email"
                id="email"
                placeholder="Enter your email"
                v-model="email"
                required
              />
              <button
                type="button"
                v-on:click="resetPassword"
                class="send-code"
              >
                <svg
                  class="send-icon"
                  viewBox="0 0 24 24"
                  width="24"
                  height="24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <line x1="22" y1="2" x2="11" y2="13"></line>
                  <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                </svg>
              </button>
            </div>
          </form>
        </div>
      </div>
    </body>
  </html>
</template>

<script>
import axios from "axios";
import showMessage from "@/utils/message";
export default {
  name: "ResetPassword",
  data: function () {
    return {
      email: "",
    };
  },
  methods: {
    resetPassword() {
      const email = this.email.trim();
      axios
        .post("/api/users/reset_password/", { email: email })
        .then((response) => {
          showMessage("Email has been sent, please confirm", "info", () => {
            this.$router.push({
              name: "Login",
            });
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
  },
};
</script>

<style scoped>
.playwrite-cu-custom {
  font-family: "Playwrite CU", cursive;
  font-optical-sizing: auto;
  font-weight: 300;
  font-style: normal;
}

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
  background: url("../assets/images/login_background.jpeg") no-repeat center
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
  box-sizing: border-box;
  position: relative;
  width: 100%;
  max-width: 1440px;
  height: 100vh;
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
  background-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  position: fixed;
  top: 0;
  left: 0;
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
  margin-left: auto; /* Pushes button container to the right */
}

.login-button,
.register-button {
  background: none;
  color: #a52a2a;
  border: none;
  font-size: 14px;
  cursor: pointer;
  text-decoration: none;
  margin-right: 20px;
}

.login-button:hover,
.register-button:hover {
  text-decoration: underline; /* Underline on hover */
}

span {
  color: #a52a2a;
  margin-right: 15px;
}

/* Forget Password Form Container */
.forget-password-container {
  background-color: rgba(255, 255, 255, 0.8);
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 400px;
  margin-top: 70px;
  position: relative;
  z-index: 1;
}

/* Styles for Input and Button */
.email-container,
.verify-container {
  display: flex;
  align-items: center;
  width: 100%;
  margin-bottom: 15px;
  position: relative;
}
h2 {
  font-size: 25px;
  font-weight: 600;
  margin-bottom: 40px;
  text-align: center;
}

p {
  font-size: 14px;
  color: #333;
  margin-bottom: 20px;
  text-align: left;
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
  margin-bottom: 5px;
  font-size: 14px;
}

.send-code {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  margin-left: -30px; /* Adjust as needed */
  margin-top: -10px;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-icon {
  width: 24px;
  height: 24px;
}

input[type="email"],
input[type="text"] {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 14px;
  box-sizing: border-box;
  margin-bottom: 10px;
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
}

button[type="submit"]:hover {
  background-color: #8b0000;
}
</style>
