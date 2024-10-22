<template>
  <header class="header">
    <div class="header-content">
      <div class="logo-container">
        <router-link to="/">
          <img src="../assets/images/Logo.jpeg" alt="Logo" class="logo" />
        </router-link>
        <h1>Australian Dictionary of Biography</h1>
      </div>
      <div class="right-header">
        
        <div v-if="$store.state.isLogin" class="username-menu">
          <div class="username" @click="toggleMenu">
            {{ username }}
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path
                fill-rule="evenodd"
                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <div :class="{ hidden: !showMenu }" class="userinfo_menu">
            <ul>
              <li>
                <span class="menu-item">Personal Center</span>
              </li>
              <li>
                <router-link to="/" @click.prevent="logout" class="menu-item logout-item">Logout</router-link>
              </li>
            </ul>
          </div>
        </div>
        <div v-else>
          <router-link to="/login" class="login">Login</router-link>
        </div>
      </div>
    </div>
    <nav class="nav-bar">
      <ul>
        <li><router-link to="/category" class="category">Category</router-link></li>
        <li><router-link to="/">Home</router-link></li>
      </ul>
    </nav>
  </header>
</template>

<script>
import axios from "axios";

export default {
  name: "Navigator",
  data() {
    return {
      username: "",
      showMenu: false,
    };
  },
  methods: {
    toggleMenu() {
      this.showMenu = !this.showMenu;
      console.log("Menu toggled", this.showMenu);
    },
    logout() {
      localStorage.clear();
      this.$store.commit("setLoginStatus", false);
    },
  },
  mounted() {
    this.username = localStorage.getItem("username");
    const currentTime = Date.now();
    const expiredTime = localStorage.getItem("expiredTime");
    const refreshToken = localStorage.getItem("refreshToken");

    if (expiredTime > currentTime) {
      this.$store.commit("setLoginStatus", true);
    } else if (refreshToken) {
      axios
        .post("/api/jwt/refresh/", { refresh: refreshToken })
        .then((response) => {
          console.log("run refresh");
          const token = response.data.access;
          localStorage.setItem("token", token);
          const newExpiredTime = Date.now() + 5 * 60 * 1000;
          localStorage.setItem("expiredTime", newExpiredTime);
          this.$store.commit("setLoginStatus", true);
        })
        .catch((error) => {
          console.log(error);
          this.$store.commit("setLoginStatus", false);
          localStorage.clear();
        });
    } else {
      this.$store.commit("setLoginStatus", false);
      localStorage.clear();
    }
  },
};
</script>

<style scoped>
.header {
  width: 100%;
  display: flex;
  flex-direction: column; /* 使用列方向以便放置导航栏 */
  background: linear-gradient(212deg, #904949 19.07%, #2a1515 57.85%);
  position: fixed;
  top: 0;
  left: 0;
  z-index: 9;
  color: white;
  margin: 0;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between; /* 在左右两侧对齐 */
  padding: 0 10px;
  height: 60px; /* 使高度一致 */
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  height: 50px;
  margin-right: 15px;
}

h1 {
  font-family: 'Playwrite CU', cursive;
  font-size: 1.5rem;
  color: white;
  font-weight: 400;
}

.right-header {
  display: flex;
  align-items: center;
}

.right-header a {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: white;
  font-size: 18px;
  margin-left: 20px;
}

.nav-bar {
  background-color: #2a1515;
  padding: 10px 20px;
  margin: 0;
  display: flex;
  justify-content: flex-start;
}

.nav-bar ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: flex-start;
}

.nav-bar ul li {
  margin-right: 20px;
}

.nav-bar ul li a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

/* 用户信息菜单的样式 */
.username {
  font-size: 20px; /* 增大用户名的字体大小 */
  color: rgb(0, 55, 128); /* 设置用户名的颜色 */
  cursor: pointer;
  position: relative;
}

.username svg {
  margin-left: 10px;
  width: 20px;
  height: 20px;
  fill: #fff;
}

.userinfo_menu {
  position: absolute;
  top: 40px;
  right: 0;
  background-color: white;
  width: 150px;
  border-radius: 5px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.userinfo_menu ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.userinfo_menu li {
  padding: 10px;
  border-bottom: 1px solid #e0e0e0;
}

.userinfo_menu li:last-child {
  border-bottom: none;
}

.menu-item {
  color: #333; /* 设置字体颜色为深灰色 */
  font-size: 16px; /* 设置菜单项字体大小 */
  cursor: pointer; /* 鼠标悬停时显示手形光标 */
}

.menu-item:hover {
  color: #555; /* 悬停时的颜色变化 */
}

.logout-item {
  color: red; /* 退出按钮设置为红色 */
}

.logout-item:hover {
  color: darkred; /* 悬停时颜色变为深红 */
}

.hidden {
  display: none;
}

.login {
  font-size: 18px;
  color: #fff;
  background-color: #3498db;
  padding: 8px 15px;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.login:hover {
  background-color: #2980b9;
}
</style>
