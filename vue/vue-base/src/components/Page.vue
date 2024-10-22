<template>
  <div class="pagination-container">
    <!-- 上一页按钮 -->
    <span v-if="info.previous" @click="goToPage(prePage)" class="page-link">
      <button class="pagination-button">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="icon"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M12.293 16.707a1 1 0 01-1.414 0l-5-5a1 1 0 010-1.414l5-5a1 1 0 011.414 1.414L8.414 10l4.293 4.293a1 1 0 010 1.414z"
            clip-rule="evenodd"
          />
        </svg>
      </button>
    </span>
    <!-- 页码按钮 -->
    <span v-for="page in pages" :key="page" class="page-link">
      <button
        v-if="page === '...'"
        class="pagination-button"
        :class="{ active: currentPage === page }"
      >
        {{ page }}
      </button>
      <button
        v-else-if="page === currentPage"
        class="pagination-button"
        :class="{ active: currentPage === page }"
      >
        {{ page }}
      </button>
      <button
        v-else
        @click="goToPage(page)"
        class="pagination-button"
        :class="{ active: currentPage === page }"
      >
        {{ page }}
      </button>
    </span>
    <!-- 下一页按钮 -->
    <span v-if="info.next" @click="goToPage(nextPage)" class="page-link">
      <button class="pagination-button">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="icon"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M7.707 3.293a1 1 0 011.414 0l5 5a1 1 0 010 1.414l-5 5a1 1 0 01-1.414-1.414L11.586 10 7.707 6.121a1 1 0 010-1.414z"
            clip-rule="evenodd"
          />
        </svg>
      </button>
    </span>
  </div>
</template>

<script>
export default {
  name: "Page",
  props: ["info"],
  data: function () {
    return {
      currentPage: 1, // 当前页码
    };
  },
  mounted() {
    this.currentPage = this.getPageFromUrl();
  },
  methods: {
    getPageFromUrl() {
      const page = Number(this.$route.query.page);
      return page ? page : 1;
    },
    goToPage(page) {
      this.currentPage = page;
      const params = { ...this.$route.query };
      params.page = page;
      this.$router.push({ query: params });
    },
  },
  computed: {
    lastPage() {
      let pageSize = 12;
      return Math.ceil(this.info.count / pageSize);
    },
    prePage() {
      if (this.currentPage > 1) {
        return this.currentPage - 1;
      }
      return 1;
    },
    nextPage() {
      if (this.currentPage < this.lastPage) {
        return this.currentPage + 1;
      }
      return this.currentPage;
    },
    pages() {
      const pages = [];
      for (let i = 1; i <= this.lastPage; i++) {
        if (
          i === 1 ||
          i === this.lastPage ||
          (i >= this.currentPage - 1 && i <= this.currentPage + 1)
        ) {
          pages.push(i);
        } else if (pages[pages.length - 1] != "...") {
          pages.push("...");
        }
      }
      return pages;
    },
  },
};
</script>

<style scoped>
.pagination-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
  gap: 0.5rem;
}

.page-link {
  display: flex;
  align-items: center;
  text-decoration: none;
}

.pagination-button {
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.25rem; /* 圆角 */
  background-color: #e5e7eb; /* bg-gray-300 */
  color: #4b5563; /* text-gray-600 */
  border: none;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.pagination-button.active {
  background-color: #3b82f6; /* bg-blue-500 */
  color: #ffffff; /* text-white */
}

.pagination-button:hover {
  background-color: #d1d5db; /* hover:bg-gray-400 */
}

.icon {
  height: 1.25rem; /* h-5 */
  width: 1.25rem; /* w-5 */
}
</style>
