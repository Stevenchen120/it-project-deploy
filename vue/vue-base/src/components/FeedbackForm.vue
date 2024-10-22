<template>
    <div>
      <!-- Feedback Button -->
      <button @click="openModal" class="feedback-button">
        <MessageSquare class="icon" /> Feedback
      </button>
  
      <!-- Modal Overlay -->
      <div v-if="show" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
          <!-- Close Button -->
          <button class="close-button" @click="closeModal">&times;</button>
  
          <!-- Feedback Form -->
          <h3>Submit Feedback</h3>
          <form @submit.prevent="submitFeedback">
            <div class="form-group">
              <label for="title">Title:</label>
              <input v-model="title" type="text" id="title" required />
            </div>
            <div class="form-group">
              <label for="message">Message:</label>
              <textarea v-model="message" id="message" required></textarea>
            </div>
            <div class="form-group">
              <label for="rating">Rating:</label>
              <select v-model="rating" id="rating" required>
                <option disabled value="">Select rating</option>
                <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
              </select>
            </div>
            <button type="submit" :disabled="loading">Submit</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { MessageSquare } from 'lucide-vue-next';
  import { useToast } from 'vue-toastification';
  
  export default {
    name: "FeedbackForm",
    components: {
      MessageSquare,
    },
    props: {
      historicalFigureId: {
        type: Number,
        required: true,
      },
    },
    data() {
      return {
        title: "",
        message: "",
        rating: "",
        show: false,      // Controls the display of the modal
        loading: false,   // Indicates if the form is being submitted
      };
    },
    setup() {
      // 使用 useToast 来创建 toast 实例
      const toast = useToast();
      return {
        toast,
      };
    },
    methods: {
      /**
       * Opens the feedback form modal.
       */
      openModal() {
        this.show = true;
      },
  
      /**
       * Closes the feedback form modal.
       */
      closeModal() {
        this.show = false;
      },
  
      /**
       * Submits the feedback form to the backend API.
       */
      submitFeedback() {
        const token = localStorage.getItem("token");
  
        // Check if user is authenticated
        if (!token) {
          this.toast.error("Please log in to submit feedback.");
          this.$router.push({ name: "Login" });
          return;
        }
  
        // Form validation
        if (!this.title || !this.message || !this.rating) {
          this.toast.error("Please fill in all fields.");
          return;
        }
  
        // Validate rating
        if (this.rating < 1 || this.rating > 5) {
          this.toast.error("Please select a rating between 1 and 5.");
          return;
        }
  
        this.loading = true;
  
        // Configure Axios instance
        const axiosInstance = axios.create({
          baseURL: 'http://localhost:8000/api', // Replace with your backend API URL
          headers: {
            Authorization: `Bearer ${token}`, // Corrected the template literal
          },
        });
  
        // Send POST request to feedback API
        axiosInstance
          .post('/feedbacks/', {
            historical_figure: this.historicalFigureId,
            title: this.title,
            message: this.message,
            rating: this.rating,
          })
          .then((response) => {
            this.toast.success("Feedback submitted successfully.");
            // Clear form fields
            this.title = "";
            this.message = "";
            this.rating = "";
            // Emit event to notify parent component
            this.$emit("feedbackSubmitted");
            // Close modal
            this.closeModal();
          })
          .catch((error) => {
            console.error("Error submitting feedback:", error);
            if (error.response) {
              if (error.response.status === 400) {
                this.toast.error("Failed to submit feedback. Please check your input.");
              } else if (error.response.status === 401) {
                this.toast.error("You need to log in to submit feedback.");
                this.$router.push({ name: "Login" });
              } else {
                this.toast.error("Failed to submit feedback. Please try again later.");
              }
            } else if (error.request) {
              this.toast.error("No response from server. Please try again later.");
            } else {
              this.toast.error("An error occurred. Please try again.");
            }
          })
          .finally(() => {
            this.loading = false;
          });
      }
    },
  };
  </script>
  
  <style scoped>
  /* Feedback Button Styles */
  .feedback-button {
    background: none;
    border: none;
    color: #3498db;
    cursor: pointer;
    display: flex;
    align-items: center;
    font-size: 16px;
    padding: 8px 16px;
  }
  
  .feedback-button:hover {
    color: #2980b9;
  }
  
  .icon {
    width: 20px;
    height: 20px;
    margin-right: 5px;
    color: #000;
    vertical-align: middle;
  }
  
  /* Modal Overlay Styles */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5); /* Semi-transparent background */
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000; /* Ensure the modal is on top */
  }
  
  /* Modal Content Styles */
  .modal-content {
    background-color: #fff;
    padding: 20px 30px;
    border-radius: 8px;
    position: relative;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
  }
  
  /* Close Button Styles */
  .close-button {
    position: absolute;
    top: 10px;
    right: 15px;
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
  }
  
  /* Feedback Form Styles */
  .feedback-form h3 {
    margin-bottom: 15px;
    text-align: center;
  }
  
  .form-group {
    margin-bottom: 15px;
    color: #333;
  }
  
  .form-group label {
    display: block;
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  .form-group input,
  .form-group textarea,
  .form-group select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .form-group textarea {
    resize: vertical;
    min-height: 80px;
  }
  
  button[type="submit"] {
    width: 100%;
    padding: 10px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
  }
  
  button[type="submit"]:disabled {
    background-color: #95a5a6;
    cursor: not-allowed;
  }
  
  /* Responsive Design */
  @media (max-width: 600px) {
    .modal-content {
      padding: 15px 20px;
    }
  
    .feedback-button {
      font-size: 14px;
      padding: 6px 12px;
    }
  
    .icon {
      width: 18px;
      height: 18px;
    }
  }
  </style>
  