<template>
  <div class="custom-background">
    <!-- Add a wrapper to prevent Navigator from covering other elements -->
    <div class="navigator-wrapper">
      <Navigator />
    </div>

    <!-- History Detail Content -->
    <div class="history-detail-container" v-if="history">
      <div class="history-header">
        <FormattedName
          :given_names="history.given_names || 'Unknown'"
          :family_name="history.family_name || 'Unknown'"
          :birth_year="history.birth_year || 'N/A'"
          :death_year="history.death_year || 'N/A'"
          :short_description="history.short_description || ''"
        />
        <!-- Search Bar Container -->
        <div class="search-bar-container">
          <input
            v-model="keyword"
            type="text"
            placeholder="Search historical figures..."
            @keydown.enter="searchFigures"
            class="search-input"
            aria-label="Search historical figures"
          />
          <button @click.prevent="searchFigures" class="search-button" aria-label="Search">
            🔍
          </button>
        </div>
      </div>

      <!-- Links Container -->
      <div class="link-container">
        <!-- Feedback Button: Render only if history.id is available -->
        <div class="external-link feedback-button">
          <FeedbackForm 
            v-if="history.id" 
            :historicalFigureId="Number(history.id)" 
            @feedbackSubmitted="handleFeedbackSubmitted" 
          />
        </div>
        <a :href="history.link" target="_blank" class="external-link">
          <ExternalLink class="icon" /> Read More
        </a>
      </div>

      <!-- Biography Content -->
      <div v-if="history.biography_content" class="biography-content">
        {{ history.biography_content }}
      </div>
      
      <!-- Comment Section -->
      <CommentSection v-if="history.id" :historicalFigureId="Number(history.id)" />
    </div>

    <!-- Placeholder if history data is not loaded yet -->
    <div v-else class="loading">
      Loading historical figure details...
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Navigator from "@/components/Navigator.vue";
import FormattedName from "@/components/FormattedName.vue";
import CommentSection from "@/components/CommentSection.vue";
import FeedbackForm from "@/components/FeedbackForm.vue";
import { ExternalLink } from 'lucide-vue-next';

export default {
  name: "HistoryDetail",
  data() {
    return {
      history: null, // Initialize as null to handle loading state
      keyword: "",
    };
  },
  components: {
    Navigator,
    FormattedName,
    CommentSection,
    FeedbackForm,
    ExternalLink,
  },
  mounted() {
    console.log("HistoryDetail component mounted."); // Debugging log
    this.getHistoryInfo();
  },
  methods: {
    /**
     * Fetches the historical figure's information from the backend.
     */
    getHistoryInfo() {
      const id = this.$route.params.id;
      if (!id) {
        this.$toast.error("No historical figure ID provided.");
        return;
      }

      axios.get(`/api/history/${id}/`)
        .then((response) => {
          this.history = response.data;
          console.log("Fetched history data:", this.history); // Debugging log
        })
        .catch((error) => {
          console.error("Error fetching history info:", error);
          this.$toast.error("Failed to load historical figure details.");
        });
    },
    
    /**
     * Handles the search functionality.
     */
    searchFigures() {
      const keyword = this.keyword.trim();
      if (keyword) {
        console.log(`Searching for keyword: ${keyword}`); // Debugging log
        this.$router.push({
          name: "about",
          query: { search: keyword },
        });
      } else {
        this.$toast.info("Please enter a keyword to search.");
      }
    },
    
    /**
     * Handles actions after successful feedback submission.
     */
    handleFeedbackSubmitted() {
      console.log("Feedback submitted successfully."); // Debugging log
      // Optionally perform other actions, e.g., refresh data
      // this.getHistoryInfo();
    },
  },
};
</script>

<style scoped>
.custom-background {
  background-color: #f7f7f7;
  min-height: 100vh;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.navigator-wrapper {
  width: 100%;
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: #f7f7f7;
}

.history-detail-container {
  max-width: 1100px;
  width: 90%;
  margin-top: 100px;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 15px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar-container {
  display: flex;
  align-items: center;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 5px 10px;
  width: 100%;
  max-width: 400px; /* Adjust as needed */
}

.search-input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #ccc;
  border-radius: 25px 0 0 25px;
  font-size: 16px;
  outline: none;
  transition: box-shadow 0.3s ease;
}

.search-input:focus {
  box-shadow: 0 0 8px rgba(52, 152, 219, 0.5);
}

.search-button {
  padding: 10px 15px;
  border: none;
  background-color: #3498db;
  color: #fff;
  cursor: pointer;
  font-size: 18px;
  border-radius: 0 25px 25px 0;
  transition: background-color 0.3s ease;
}

.search-button:hover {
  background-color: #2980b9;
}

.link-container {
  display: flex;
  gap: 20px;
  margin-top: 25px;
  flex-wrap: wrap;
  justify-content: flex-start;
}

.external-link,
.feedback-button {
  display: flex;
  align-items: center;
  color: #3498db;
  text-decoration: none;
  font-size: 16px;
  padding: 10px 15px;
  border-radius: 8px;
  background-color: #f0f8ff;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 8px rgba(52, 152, 219, 0.2);
}

.external-link:hover,
.feedback-button:hover {
  color: #2980b9;
  background-color: #e0f0ff;
  box-shadow: 0 6px 12px rgba(41, 128, 185, 0.3);
}

.biography-content {
  margin: 30px 0;
  color: #333; /* Dark text for better readability */
  font-size: 18px; /* Increased font size for better readability */
  line-height: 1.8; /* Increased line height for better readability */
  white-space: pre-wrap; /* Preserve whitespace and line breaks */
  word-wrap: break-word; /* Enable word wrapping */
}

.loading {
  margin-top: 50px;
  font-size: 18px;
  color: #555;
}

@media (max-width: 1024px) {
  .history-detail-container {
    padding: 20px;
  }
}

@media (max-width: 768px) {
  .history-detail-container {
    margin: 20px;
    padding: 15px;
  }

  .history-header {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }

  .search-bar-container {
    width: 100%;
  }

  .link-container {
    flex-direction: column;
    gap: 15px;
  }
}
</style>