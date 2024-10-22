<template>
  <div class="header">
    <router-link to="/category/:letter-:birthYear-:deathYear-:occupation" class="category">Category</router-link>
    <div v-if="$store.state.isLogin" class="username-menu">
      <div class="username" @click="toggleMenu">
        {{ username }}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
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
           <li v-if="isStaff">
            <a href="http://127.0.0.1:8000/admin/" class="menu-item"
              >Management</a
            >
          </li>
          <li>
            <router-link
              to="/"
              @click.prevent="logout"
              class="menu-item logout-item"
              >Logout</router-link
            >
          </li>
        </ul>
      </div>
    </div>
    <div v-else class="right-header">
      <router-link to="/Login" class="login"> Login </router-link>
    </div>
  </div>
</template>

<!-- <template>
    <div class="header">
      <router-link to="#" class="category">Category</router-link>
      <div v-if="$store.state.isLogin" class="username">
        {{ username }}
      </div>
      <div v-else class="right-header">
        <router-link to="/Login" class="login">
          <LogIn class="login-icon" />
          Login
        </router-link>
      </div>
    </div>
  </template> -->

<script>
import axios from "axios";
export default {
  name: "Header",
  data: function () {
    return {
      info: "",
      username: "",
      showMenu: false,
    };
  },
  methods: {
    toggleMenu() {
      this.showMenu = !this.showMenu; // 切换菜单显示状态
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
    console.log(currentTime);
    console.log(expiredTime);
    if (expiredTime > currentTime) {
      this.$store.commit("setLoginStatus", true);
    } else if (refreshToken) {
      axios
        .post("/api/jwt/refresh/", { refresh: refreshToken })
        .then((response) => {
          console.log("run refresh");
          const token = response.data.access;
          localStorage.setItem("token", token);
          const expiredTime = Date.now() + 5 * 60 * 1000;
          localStorage.setItem("expiredTime", expiredTime);
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
    axios
      .get("/api/history")
      .then((response) => (this.info = response.data))
      .catch((error) => {
        console.log(error);
      });
  },
};
</script>
<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.header {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between; /* 左右部分分开 */
  padding: 0px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  z-index: 10;
}

.category {
  font-size: 24px;
  background-color: #693c3c;
  padding: 10px 20px;
  text-decoration: none;
  color: white;
  border-radius: 5px;
}

.right-header .login {
  text-decoration: none;
  color: rgb(48, 42, 42);
  font-size: 18px;
  margin-right: 40px;
}

.username {
  font-size: 20px; /* 增大用户名的字体大小 */
  color: rgb(0, 55, 128); /* 设置用户名的颜色 */
  cursor: pointer;
}

.username svg {
  margin-left: 10px;
  width: 20px;
  height: 20px;
  fill: #333;
}

/* 用户信息菜单的样式 */
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

/* 特别为“退出”按钮单独设置样式 */
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
