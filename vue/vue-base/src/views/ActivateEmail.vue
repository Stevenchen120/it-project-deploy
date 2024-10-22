<template>
  <div id="container">
    <Header />
    <div class="title">Activate your account</div>
    <div class="content">
      <div class="info-box">
        <div class="info-text">
          Please click the button below to activate your account
        </div>
      </div>
      <div class="button-box">
        <button v-on:click="activate" class="activate-button">
          Activate account
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
import showMessage from "@/utils/message";
import axios from "axios";
export default {
  name: "ActivateEmail",
  components: { Header },
  methods: {
    activate() {
      const uid = this.$route.params.uid;
      const token = this.$route.params.token;
      const fromData = {
        uid: uid,
        token: token,
      };
      axios
        .post("/api/users/activation/", fromData)
        .then((response) => {
          showMessage(
            "Account activation successful, please log in on the login page",
            "info",
            () => {
              this.$router.push({ name: "Login" });
            }
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
/* 清除默认边距和填充 */
html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
  overflow: hidden; /* 防止页面滚动 */
}

/* 整个页面容器 */
#container {
  background-color: #e0f7fa; /* 背景色 */
  min-height: 100vh; /* 确保页面高度至少占满屏幕 */
  padding: 2rem; /* 添加内边距 */
  color: black; /* 设置文本颜色 */
  font-size: 0.875rem; /* 字体大小 */
  box-sizing: border-box; /* 确保 padding 不影响总宽度 */
}

/* 标题样式 */
.title {
  text-align: center;
  font-size: 2rem;
  padding: 2rem 0;
  color: black; /* 改成黑色，使其在浅色背景下可见 */
}

/* 内容容器 */
.content {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

/* 信息盒子样式 */
.info-box {
  width: 25%;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 0.5rem;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  margin-bottom: 1rem;
}

/* 按钮居中容器 */
.button-box {
  display: flex;
  justify-content: center;
}

/* 激活按钮样式 */
.activate-button {
  background-color: #38a169;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  border: none;
  cursor: pointer;
}

.activate-button:hover {
  background-color: #2f855a; /* 悬停效果 */
}
</style>
