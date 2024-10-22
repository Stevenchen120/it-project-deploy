<template>
  <div class="custom-background">
    <!-- 使用 Navigator 组件 -->
    <Navigator/>

    <!-- 搜索框部分 -->
    <SearchBox :filter="filter" :searchQuery="searchQuery" @search="handleSearch" />

    <!-- 数据展示部分 -->
    <div class="data-list">
      <!-- 检查是否有结果 -->
      <div v-if="info.results && info.results.length > 0">
        <!-- 使用 v-for 循环遍历 info 数据列表 -->
        <div class="data-item" v-for="(item, index) in info.results" :key="index">
          <router-link :to="'/history/' + item.id">
            <!-- 第一行：Given Names 和 Family Name -->
            <p class="primary-text">
              {{ item.given_names }} {{ item.family_name }}
            </p>
            <!-- 第二行：Birth, Death 和 Short Description -->
            <p class="secondary-text">
              Birth: {{ item.birth_year }} | Death: {{ item.death_year }}
              <span v-if="item.short_description.length > 50">
                {{ item.short_description.slice(0, 50) }}...
              </span>
              <span v-else>
                {{ item.short_description }}
              </span>
            </p>
          </router-link>
        </div>
      </div>
      <!-- 如果没有结果 -->
      <div v-else class="no-results">
        <p>No results found for your search.</p>
        <p>Try modifying your search.</p>
      </div>
      <!-- 分页组件 -->
      <Page :info="info" @page-changed="handlePageChange" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Page from "@/components/Page.vue";
import Navigator from "@/components/Navigator.vue";
import SearchBox from "@/components/Searchbox.vue";
import Header from "@/components/Header.vue"; // 导入 SearchBox 组件

export default {
  name: "About",
  components: {
    Header,
    Navigator,
    Page,
    SearchBox,
  },
  data() {
    return {
      filter: this.$route.query.filter || "all", // 从路由查询参数初始化过滤器
      searchQuery: this.$route.query.search || "", // 从路由查询参数初始化搜索查询
      info: {}, // 初始化为对象以存储从 API 获取的数据
    };
  },
  mounted() {
    this.get_history_data();
  },
  methods: {
    get_history_data() {
      const url = "/api/history/";  // Assuming your API endpoint
  const page = Number(this.$route.query.page) || 1;  // Default to page 1
  const search = this.$route.query.search;
  const filter = this.$route.query.filter || this.filter;  // Default to current filter

  // Initialize params object to be sent to the back-end
    const params = {
      page: page,  // Always include the page parameter
    };

    // Add search and filter params if they exist
    if (search && filter) {
      params.search = search;
      params.filter = filter;
    }

  // Add the search and corresponding filter
  if (search) {
    switch (filter) {
      case 'Birth':
        params.birth_year = search;
        break;
      case 'Death':
        params.death_year = search;
        break;
      case 'Family_Name':
        params.family_name = search;
        break;
      case 'Given_Name':
        params.given_names = search;
        break;
      case 'Occupation':
        params.short_description = search;
        break;
      default:
        params.search = search;  // General search
    }

    // Update the component's state with the current search and filter
    this.searchQuery = search;
    this.filter = filter;
  }

  // Use axios to make the GET request with the constructed params
    axios
    .get(url, { params })
    .then((response) => {
      this.info = response.data;
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
      this.info = { results: [] };  // Set empty results on error
      });
    },

    handleSearch({ filter, searchQuery }) {

      // Update the component's data with the current search filter and query
      this.filter = filter;
      this.searchQuery = searchQuery;

      // Push the new search query into the URL, resetting the page to 1
      this.$router.push({
        name: "about",
        query: { search: searchQuery, filter: filter, page: 1 }
      }).then(() => {
        // Fetch data again after updating the route (URL)
        this.get_history_data();
      }).catch((err) => {
       console.error('Navigation error:', err);
      });
      },

    handlePageChange(newPage) {
    this.$router.push({
        name: "about",
        query: { ...this.$route.query, page: newPage }
      }).then(() => {
        this.get_history_data();
      }).catch((err) => {
        console.error('Navigation error:', err);
      });
    }
  },
  watch: {
    $route(to, from) {
      if (to.query.search !== from.query.search || to.query.filter !== from.query.filter || to.query.page !== from.query.page) {
        this.get_history_data(); // 每当路由参数变化时，重新获取数据
      }
    },
  },
};
</script>

<style scoped>
.custom-background {
  background-color: #fcefef; /* 覆盖全局背景颜色 */
  min-height: 100vh; /* 确保页面内容至少占据整个视口高度 */
  padding-top: 60px; /* 为 Header 留出空间 */
}

.data-list {
  padding: 20px;
  border-radius: 8px;
}

.data-item {
  margin-bottom: 20px;
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.primary-text {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

.secondary-text {
  font-size: 14px;
  color: #555;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.no-results {
  text-align: center;
  padding: 20px;
  color: #666;
}
</style>









