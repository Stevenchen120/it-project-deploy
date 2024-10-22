<template>
  <div>
    <Navigator />
    <div class="container">
      <div class="title">
        <h1>AUSTRALIAN DICTIONARY OF BIOGRAPHY</h1>
      </div>
      <div class="image-container">
        <img src="../assets/images/Logo.jpeg" alt="Biography Image" />
      </div>
      <!-- 搜索框部分 -->
      <div class="search-container">
        <!-- 搜索输入框 -->
        <input
          v-model="keyword"
          type="text"
          placeholder="Search..."
          @keydown.enter="searchFigures"
        />
        <!-- 将放大镜图标作为按钮 -->
        <button v-on:click.prevent="searchFigures" class="search-icon-button">
          &#x1F50D;
          <!-- 使用你已经有的放大镜图标 -->
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
import Navigator from "@/components/Navigator.vue";
export default {
  name: "HomeView",
  data: function () {
    return {
      keyword: "",
    };
  },
  methods: {
    searchFigures() {
      const keyword = this.keyword.trim();
      this.$router.push({
        name: "about",
        query: { search: keyword },
      });
    },
  },
  components: {
    Navigator,
    Header,
  },
};
</script>

<style>
/* 全局样式放在这里或在全局 CSS 文件中 */
body {
  height: 100%;
  margin: 0;
  font-family: "Arial", sans-serif;
  background: linear-gradient(212deg, #904949 19.07%, #2a1515 57.85%);
  color: white;
}
.container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 1440px;
  margin: auto;
}
.title {
  margin-top: 60px; /* 避免Header遮挡 */
  margin-bottom: 10px;
}
.title h1 {
  font-family: "Georgia", serif;
  font-size: 36px;
  letter-spacing: 3px;
}
.image-container {
  margin-top: 40px;
  margin-bottom: 20px;
}
.image-container img {
  width: 350px;
  height: 350px;
  border-radius: 20px;
}
.search-container {
  position: relative;
  display: flex;
  align-items: center;
}
.search-container input {
  width: 600px;
  padding: 10px;
  padding-left: 40px;
  border-radius: 25px;
  border: 1px solid #ccc;
  font-size: 16px;
  background-color: #fff;
  color: #000;
  outline: none;
}
.search-container .search-icon-button {
  position: absolute;
  left: 10px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  color: #aaa;
  display: flex;
  align-items: center;
}
</style>
