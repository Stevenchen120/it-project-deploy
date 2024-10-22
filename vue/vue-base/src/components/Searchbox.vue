<template>
    <div class="search-container">
      <div class="search-wrapper">
        <label for="filter" class="search-label">Your search for</label>
        <select id="filter" name="filter" v-model="localFilter">
          <option value="all">All Fields</option>
          <option value="givenName">Given Name</option>
          <option value="family">Family Name</option>
          <option value="birth">Birth</option>
          <option value="death">Death</option>
          <option value="occupation">Occupation</option>
        </select>
        <input
          type="search"
          id="search-input"
          v-model="localSearchQuery"
          placeholder="Search..."
          aria-label="Search input"
        />
        <button id="search-btn" @click="onSearch">🔍</button>
      </div>
    </div>
  </template>

  <script>
  export default {
    name: "SearchBox",
    props: {
      filter: {
        type: String,
        default: "all",
      },
      searchQuery: {
        type: String,
        default: "",
      },
    },
    data() {
      return {
        localFilter: this.filter,
        localSearchQuery: this.searchQuery,
      };
    },
    methods: {
      onSearch() {
        // Emit search event to parent component
        this.$emit("search", {
          filter: this.localFilter,
          searchQuery: this.localSearchQuery,
        });
      },
    },
    watch: {
      // Sync local state with parent state changes
      filter(newVal) {
        this.localFilter = newVal;
      },
      searchQuery(newVal) {
        this.localSearchQuery = newVal;
      },
    },
  };
  </script>

  <style scoped>
  .search-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    margin: 40px auto;
    width: 70%;
    max-width: 1280px;
  }

  .search-wrapper {
    display: flex;
    align-items: center;
    border: 2px solid #ddd;
    border-radius: 25px;
    overflow: hidden;
    background-color: #fcefef;
    padding: 10px;
    width: 100%;
  }

  .search-label {
    font-size: 1rem;
    font-weight: bold;
    color: #5a2929;
    margin-right: 20px;
    white-space: nowrap;
  }

  #filter {
    border: none;
    padding: 12px;
    font-size: 1rem;
    border-right: 1px solid #ddd;
    outline: none;
    background-color: transparent;
    margin-right: 10px;
  }

  #search-input {
    width: 100%;
    padding: 12px;
    border: none;
    outline: none;
    font-size: 1rem;
    background-color: transparent;
  }

  #search-btn {
    padding: 12px;
    background-color: transparent;
    border: none;
    cursor: pointer;
    font-weight: bold;
    display: flex;
    align-items: center;
  }
  </style>