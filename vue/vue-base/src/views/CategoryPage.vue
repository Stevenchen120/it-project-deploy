<template>
  <Navigator />
  <body>
    <div class="background-overlay"></div>


    <SearchBox :filter="filter" :searchQuery="searchQuery" @search="handleSearch" />

    <div class="filter-container">
  <!-- Capital Letter Filter -->
  <div class="filter">
    <div class="filter-title">Capital Letter</div>
    <div class="buttons">
      <button @click="handleCatalog('all')">ALL</button>
      <button @click="handleCatalog('A')">A</button>
      <button @click="handleCatalog('B')">B</button>
      <button @click="handleCatalog('C')">C</button>
      <button @click="handleCatalog('D')">D</button>
      <button @click="handleCatalog('E')">E</button>
      <button @click="handleCatalog('F')">F</button>
      <button @click="handleCatalog('G')">G</button>
      <button @click="handleCatalog('H')">H</button>
      <button @click="handleCatalog('I')">I</button>
      <button @click="handleCatalog('J')">J</button>
      <button @click="handleCatalog('K')">K</button>
      <button @click="handleCatalog('L')">L</button>
      <button @click="handleCatalog('M')">M</button>
      <button @click="handleCatalog('N')">N</button>
      <button @click="handleCatalog('O')">O</button>
      <button @click="handleCatalog('P')">P</button>
      <button @click="handleCatalog('Q')">Q</button>
      <button @click="handleCatalog('R')">R</button>
      <button @click="handleCatalog('S')">S</button>
      <button @click="handleCatalog('T')">T</button>
      <button @click="handleCatalog('U')">U</button>
      <button @click="handleCatalog('V')">V</button>
      <button @click="handleCatalog('W')">W</button>
      <button @click="handleCatalog('X')">X</button>
      <button @click="handleCatalog('Y')">Y</button>
      <button @click="handleCatalog('Z')">Z</button>
    </div>
  </div>

  <!-- Birth Year Filter -->
  <div class="filter">
    <div class="filter-title">Birth Year</div>
    <div class="buttons">
      <button @click="handleCatalog(selectedLetter, 'all')">ALL</button>
      <button @click="handleCatalog(selectedLetter, '1725-1750')">1725—1750</button>
      <button @click="handleCatalog(selectedLetter, '1750-1775')">1750—1775</button>
      <button @click="handleCatalog(selectedLetter, '1775-1800')">1775—1800</button>
      <button @click="handleCatalog(selectedLetter, '1800-1825')">1800—1825</button>
      <button @click="handleCatalog(selectedLetter, '1825-1850')">1825—1850</button>
      <button @click="handleCatalog(selectedLetter, '1850-1875')">1850—1875</button>
      <button @click="handleCatalog(selectedLetter, '1875-1900')">1875—1900</button>
    </div>
  </div>

  <!-- Death Year Filter -->
  <div class="filter">
    <div class="filter-title">Death Year</div>
    <div class="buttons">
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, 'all')">ALL</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, '1725-1750')">1725—1750</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, '1750-1775')">1750—1775</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, '1775-1800')">1775—1800</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, '1800-1825')">1800—1825</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, '1825-1850')">1825—1850</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, '1850-1875')">1850—1875</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, '1875-1900')">1875—1900</button>
    </div>
  </div>

  <!-- Occupation Filter -->
  <div class="filter">
    <div class="filter-title">Occupation</div>
    <div class="buttons">
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, selectedDeathYear, 'all')">ALL</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, selectedDeathYear, 'Aboriginal')">Aboriginal</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, selectedDeathYear, 'Actor')">Actor</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, selectedDeathYear, 'Artist')">Artist</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, selectedDeathYear, 'Businessman')">Businessman</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, selectedDeathYear, 'Civil')">Civil</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, selectedDeathYear, 'Congregational minister')">Congregational minister</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, selectedDeathYear, 'Cricketer')">Cricketer</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, selectedDeathYear, 'Educationist')">Educationist</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, selectedDeathYear, 'Engineer')">Engineer</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, selectedDeathYear, 'Explorer')">Explorer</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, selectedDeathYear, 'Governor')">Governor</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, selectedDeathYear, 'Grazier')">Grazier</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, selectedDeathYear, 'Headmaster')">Headmaster</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, selectedDeathYear, 'Journalist')">Journalist</button>
      <button @click="handleCatalog(selectedLetter, selectedBirthYear, selectedDeathYear, 'Judge')">Judge</button>
    </div>
  </div>
</div>
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
    </div>
  <!-- 分页组件 -->
    <Page :info="info" @page-changed="handlePageChange" />
  </body>
</template>

<script>
import axios from "axios";
import Page from "@/components/Page.vue";
import Navigator from "@/components/Navigator.vue";
import SearchBox from "@/components/Searchbox.vue"; // 导入 SearchBox 组件

export default {
  name: "About",
  components: {
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
          .get(url, {params})
          .then((response) => {
            this.info = response.data;
          })
          .catch((error) => {
            console.error("Error fetching data:", error);
            this.info = {results: []};  // Set empty results on error
          });
    },

    handleSearch({filter, searchQuery}) {

      // Update the component's data with the current search filter and query
      this.filter = filter;
      this.searchQuery = searchQuery;

      // Push the new search query into the URL, resetting the page to 1
      this.$router.push({
        name: "about",
        query: {search: searchQuery, filter: filter, page: 1}
      }).then(() => {
        // Fetch data again after updating the route (URL)
        this.get_history_data();
      }).catch((err) => {
        console.error('Navigation error:', err);
      });
    },
    handleCatalog(letter = this.selectedLetter, birthYear = this.selectedBirthYear, deathYear = this.selectedDeathYear, occupation = this.selectedOccupation) {
      // Update the state with new filter values
      this.selectedLetter = letter || this.selectedLetter;
      this.selectedBirthYear = birthYear || this.selectedBirthYear;
      this.selectedDeathYear = deathYear || this.selectedDeathYear;
      this.selectedOccupation = occupation || this.selectedOccupation;

      // Push selected filters into URL query parameters
      this.$router.push({
        name: "CategoryPage",
        query: {
          letter: this.selectedLetter !== "all" ? this.selectedLetter : null,
          birth_year: this.selectedBirthYear !== "all" ? this.selectedBirthYear : null,
          death_year: this.selectedDeathYear !== "all" ? this.selectedDeathYear : null,
          occupation: this.selectedOccupation !== "all" ? this.selectedOccupation : null,
          page: 1 // Reset to page 1 when changing filters
        }
      }).then(() => {
        // Fetch the data after the URL is updated with filters
        this.getCatalogData(this.selectedLetter, this.selectedBirthYear, this.selectedDeathYear, this.selectedOccupation);
      }).catch((err) => {
        console.error("Error navigating to the category:", err);
      });
    },
    getCatalogData(category = "all", birthYear = "all", deathYear = "all", occupation = "all", page = 1) {
      const url = "/api/history/";

      // Prepare the params for the API call
      const params = {page};

      // Add only non-default filter values to the request
      if (category !== "all") {
        params.category = category;
      }
      if (birthYear !== "all") {
        params.birth_year = birthYear;
      }
      if (deathYear !== "all") {
        params.death_year = deathYear;
      }
      if (occupation !== "all") {
        params.occupation = occupation;
      }

      // Send the GET request to the backend
      axios
          .get(url, {params})
          .then((response) => {
            this.info = response.data;  // Store the response data
          })
          .catch((error) => {
            console.error("Error fetching catalog data:", error);
            this.info = {results: []};  // Set empty results on error
          });
    }
  },

  handlePageChange(newPage) {
    // Pass the current query parameters (from this.$route.query) to getCatalogData
    const category = this.$route.query.letter || "all";
    const birthYear = this.$route.query.birth_year || "all";
    const deathYear = this.$route.query.death_year || "all";
    const occupation = this.$route.query.occupation || "all";

    this.$router.push({
      name: "CategoryPage",
      query: {
        ...this.$route.query, // Keep existing filters and search query in the URL
        page: newPage,        // Update the page number
      }
    }).then(() => {
      // Pass the filters and page number to getCatalogData
      this.getCatalogData(category, birthYear, deathYear, occupation, newPage);
    }).catch((err) => {
      console.error('Navigation error:', err);
    });
  },
  watch: {
  $route(to, from) {
    // Check if any relevant query parameters have changed
    if (
      to.query.letter !== from.query.letter ||
      to.query.birth_year !== from.query.birth_year ||
      to.query.death_year !== from.query.death_year ||
      to.query.occupation !== from.query.occupation ||
      to.query.page !== from.query.page
    ) {
      // Pass the current filters and page number to getCatalogData
      const category = to.query.letter || "all";
      const birthYear = to.query.birth_year || "all";
      const deathYear = to.query.death_year || "all";
      const occupation = to.query.occupation || "all";
      const page = to.query.page || 1;

      this.getCatalogData(category, birthYear, deathYear, occupation, page);
    }
  }
},
};
</script>

<style scoped>

body {
  padding-top: 50px; /* Adjust this value to move content down */
}


.background-overlay {
  position: absolute;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.5);
  z-index: 15;
  width: 100%;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
}


h1 {
  font-family: "Playwrite CU", cursive;
  font-size: 1.2rem;
  color: #333;
  font-weight: 300;
}

span {
  color: #a52a2a;
  margin-right: 15px;
}


.filter-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-right: 20px;
  width: 100%;
}
.filter {
  border-top: 1px solid black;
  margin-bottom: 20px;
  width: 90%;
}

.filter-title {
  font-weight: bold;
}

.buttons button {
  border: none;
  margin-right: 5px;
  padding: 5px 10px;
  margin-top: 20px;
  display: inline-block;
  background: none;
  cursor: pointer;
  font-size: 18px;
  color: #ffffff; /* Text color (white) */
  border-radius: 5px; /* Optional: Rounded corners */
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

/* end of searching lebal */


</style>