<!-- comments/components/Comment.vue -->
<template>
  <div class="comment">
    <!-- Comment Header -->
    <div class="comment-header">
      <div class="comment-author">
        <span class="username">{{ comment.author }}</span>
      </div>
      <img :src="comment.avatar || defaultAvatar" alt="Avatar" class="avatar" />
      <div class="comment-info">
        <span class="timestamp">{{ formattedTimestamp }}</span>
      </div>
    </div>

    <!-- Comment Body -->
    <div class="comment-body">
      <p>{{ comment.text }}</p>
    </div>

    <!-- Comment Actions: Like, Unlike, Delete, and Reply -->
    <div class="comment-actions">
      <button
        @click="toggleLike"
        :disabled="isLikedByCurrentUser === null"
        aria-label="Like comment"
      >
        <span :class="['like-icon', { liked: isLikedByCurrentUser }]">❤</span>
        {{ comment.likes_count || 0 }}
      </button>
      <button @click="toggleReplyBox" class="reply-btn">
        Reply
      </button>
      <button
        v-if="isAuthor"
        @click="deleteComment"
        class="delete-btn"
        aria-label="Delete comment"
      >
        Delete
      </button>
    </div>

    <!-- Reply Box -->
    <div v-if="showReplyBox" class="reply-box">
      <textarea
        v-model="replyText"
        placeholder="Add a reply..."
        @keydown.enter.prevent="submitReply"
      ></textarea>
      <div class="reply-box-actions">
        <button @click="submitReply" class="submit-btn">Submit</button>
        <button @click="toggleReplyBox" class="cancel-btn">Cancel</button>
      </div>
    </div>

    <!-- Replies List -->
    <div v-if="comment.replies && comment.replies.length > 0" class="replies">
      <!-- Show toggle button only if it's a parent comment and has more replies than initial display -->
      <div class="replies-header" v-if="!isChild && hasMoreReplies">
        <span>{{ comment.replies.length }} Replies</span>
        <button @click="toggleReplies" class="toggle-replies-btn">
          {{ areRepliesCollapsed ? `Show More Replies (${comment.replies.length})` : 'Hide Replies' }}
        </button>
      </div>

      <!-- Visible Replies -->
      <div class="replies-list">
        <Comment
          v-for="reply in visibleReplies"
          :key="reply.id"
          :comment="reply"
          :is-child="true"
          @refreshComments="refreshReplies"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import dayjs from "dayjs";

export default {
  name: "Comment",
  components: {
    Comment: () => import('./Comment.vue'), // Recursive component
  },
  props: {
    comment: {
      type: Object,
      required: true,
      validator(value) {
        return 'author_id' in value;
      },
    },
    isChild: {
      type: Boolean,
      default: false, // Defaults to parent comment
    },
  },
  data() {
    return {
      showReplyBox: false, // Controls reply box visibility
      replyText: '', // Reply content
      areRepliesCollapsed: true, // Controls replies collapse state
      initialRepliesToShow: 1, // Initial number of replies to show
      defaultAvatar: 'https://via.placeholder.com/40', // Default avatar URL
      isLikedByCurrentUser: null, // Indicates if the current user has liked this comment
    };
  },
  computed: {
    // Compute visible replies based on collapse state
    visibleReplies() {
      if (!this.isChild && this.areRepliesCollapsed) {
        return this.comment.replies.slice(0, this.initialRepliesToShow);
      }
      return this.comment.replies;
    },
    // Determine if there are more replies to show
    hasMoreReplies() {
      return !this.isChild && this.comment.replies.length > this.initialRepliesToShow;
    },
    // Format timestamp
    formattedTimestamp() {
      return dayjs(this.comment.created_at).format('YYYY-MM-DD HH:mm');
    },
    // Check if the current user is the author of the comment
    isAuthor() {
      const token = localStorage.getItem("token");
      if (!token) return false;
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        console.log("User ID from Token:", payload.user_id, "Author ID:", this.comment.author_id);
        return payload.user_id === this.comment.author_id;
      } catch (e) {
        console.error("Invalid token:", e);
        return false;
      }
    },
  },
  mounted() {
    this.fetchUserLikeStatus();
  },
  methods: {
    // Fetch if the current user has liked this comment
    fetchUserLikeStatus() {
      const token = localStorage.getItem("token");
      if (!token) {
        this.isLikedByCurrentUser = false;
        return;
      }

      axios
        .get(`/api/comments/${this.comment.id}/liked_by_user/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          this.isLikedByCurrentUser = response.data.liked;
        })
        .catch((error) => {
          console.error("Error fetching user like status:", error);
          this.isLikedByCurrentUser = false;
        });
    },
    // Toggle like/unlike
    toggleLike() {
      if (this.isLikedByCurrentUser) {
        this.unlikeComment();
      } else {
        this.likeComment();
      }
    },
    // Like the comment
    likeComment() {
      const likeUrl = `/api/comments/${this.comment.id}/like/`;
      const token = localStorage.getItem("token");
      if (!token) {
        alert("Please log in to like comments.");
        this.$router.push({ name: "Login" });
        return;
      }

      axios
        .post(likeUrl, {}, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          this.isLikedByCurrentUser = true;
          this.comment.likes_count = response.data.likes_count;
        })
        .catch((error) => {
          console.error("Error liking comment:", error);
          if (error.response && error.response.status === 400) {
            this.showError("You have already liked this comment.");
          } else if (error.response && error.response.status === 404) {
            this.showError("Comment not found.");
          } else {
            this.showError("Failed to like the comment. Please try again later.");
          }
        });
    },
    // Unlike the comment
    unlikeComment() {
      const unlikeUrl = `/api/comments/${this.comment.id}/unlike/`;
      const token = localStorage.getItem("token");
      if (!token) {
        alert("Please log in to unlike comments.");
        this.$router.push({ name: "Login" });
        return;
      }

      axios
        .post(unlikeUrl, {}, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          this.isLikedByCurrentUser = false;
          this.comment.likes_count = response.data.likes_count;
        })
        .catch((error) => {
          console.error("Error unliking comment:", error);
          if (error.response && error.response.status === 400) {
            this.showError("You have not liked this comment.");
          } else if (error.response && error.response.status === 404) {
            this.showError("Comment not found.");
          } else {
            this.showError("Failed to unlike the comment. Please try again later.");
          }
        });
    },
    // Delete the comment
    deleteComment() {
  if (!confirm("Are you sure you want to delete this comment?")) {
    return;
  }

  const deleteUrl = `/api/comments/${this.comment.id}/`;
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Please log in to delete comments.");
    this.$router.push({ name: "Login" });
    return;
  }

  axios
    .delete(deleteUrl, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    .then(() => {
      if (this.isChild) {
        // If this is a child comment, remove it from the parent's replies array
        const parentComment = this.$parent.comment;
        parentComment.replies = parentComment.replies.filter(reply => reply.id !== this.comment.id);
      } else {
        // For parent comments, refresh the entire comment list
        this.$emit('refreshComments');
      }
    })
    .catch((error) => {
      console.error("Error deleting comment:", error);
      this.showError("Failed to delete the comment. Please try again later.");
    });
}
,
    // Toggle reply box visibility
    toggleReplyBox() {
      this.showReplyBox = !this.showReplyBox;
      if (this.showReplyBox) {
        this.replyText = "";
      }
    },
    // Submit a reply
    submitReply() {
      if (this.replyText.trim() === "") return;

      const token = localStorage.getItem("token");
      if (!token) {
        alert("Please log in to reply.");
        this.$router.push({ name: "Login" });
        return;
      }

      axios
        .post(
          `/api/comments/`,
          {
            historical_figure: this.comment.historical_figure, // Assuming each comment has this field
            text: this.replyText,
            parent: this.comment.id,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )
        .then((response) => {
          const newReply = response.data; // Assuming API returns the newly created reply
          newReply.replies = []; // Initialize replies for the new reply
          newReply.likes_count = 0; // Initialize likes count
          this.comment.replies.unshift(newReply); // Add the new reply to the beginning of the replies array
          this.replyText = "";
          this.showReplyBox = false;
          // If the parent comment was collapsed, expand to show the new reply
          if (!this.isChild) {
            this.areRepliesCollapsed = false;
          }
        })
        .catch((error) => {
          console.error("Error posting reply:", error);
          this.showError("Failed to post reply. Please try again later.");
        });
    },
    // Toggle replies collapse state
    toggleReplies() {
      this.areRepliesCollapsed = !this.areRepliesCollapsed;
    },
    // Refresh replies after actions like delete or add
    refreshReplies() {
      const token = localStorage.getItem("token");
      if (!token) return;

      axios
        .get(`/api/comments/?historical_figure=${this.comment.historical_figure}&parent=${this.comment.id}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          if (Array.isArray(response.data)) {
            this.$set(this.comment, 'replies', response.data);
            this.areRepliesCollapsed = true; // Reset to collapsed state
          }
        })
        .catch((error) => {
          console.error("Error fetching replies:", error);
          this.showError("Failed to refresh replies. Please try again later.");
        });
    },
    // Show error message (can be replaced with a better UI component like toast notifications)
    showError(message) {
      alert(message);
    },
  },
};
</script>

<style scoped>
.comment {
  padding: 15px;
  margin-bottom: 15px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.comment-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.comment-author {
  margin-right: 10px;
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: bold;
  color: #333333;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.comment-info {
  display: flex;
  flex-direction: column;
}

.timestamp {
  font-size: 12px;
  color: #777777;
}

.comment-body {
  margin-bottom: 10px;
}

.comment-body p {
  margin: 0;
  color: #555555;
}

.comment-actions {
  display: flex;
  align-items: center;
}

.comment-actions button {
  background: none;
  border: none;
  color: #3498db;
  cursor: pointer;
  margin-right: 15px;
  display: flex;
  align-items: center;
}

.reply-btn {
  /* Add styles as needed */
}

.delete-btn {
  background: none;
  border: none;
  color: #e74c3c;
  cursor: pointer;
}

.delete-btn:hover {
  text-decoration: underline;
}

.like-icon {
  margin-right: 5px;
  color: #bbb;
  transition: color 0.3s;
}

.like-icon.liked {
  color: #e74c3c;
}

.comment-actions button:hover .like-icon {
  color: #e74c3c;
}

.comment-actions button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.reply-box {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
}

.reply-box textarea {
  width: 100%;
  min-height: 60px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: vertical;
}

.reply-box-actions {
  display: flex;
  align-items: center;
  margin-top: 5px;
}

.reply-box-actions .submit-btn {
  padding: 6px 12px;
  background-color: #2ecc71;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.reply-box-actions .cancel-btn {
  padding: 6px 12px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px;
}

.reply-box-actions button:hover {
  opacity: 0.9;
}

.replies {
  margin-top: 15px;
  padding-left: 20px;
  border-left: 2px solid #e0e0e0;
}

.replies-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.toggle-replies-btn {
  background: none;
  border: none;
  color: #3498db;
  cursor: pointer;
  font-size: 14px;
  text-decoration: underline;
}

.toggle-replies-btn:hover {
  color: #2980b9;
}

.load-more-btn {
  margin-top: 10px;
  padding: 6px 12px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.load-more-btn:hover {
  background-color: #2980b9;
}

@media (max-width: 600px) {
  .comment {
    padding: 10px;
  }

  .avatar {
    width: 30px;
    height: 30px;
  }

  .comment-actions button {
    margin-right: 10px;
  }
}
</style>
