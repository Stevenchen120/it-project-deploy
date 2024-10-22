<!-- CommentSection.vue -->
<template>
  <div class="comment-section">
    <h2>Comments ({{ totalComments }})</h2>

    <!-- 新增评论输入框 -->
    <div v-if="$store.state.isLogin" class="comment-input">
      <textarea
        v-model="newComment"
        placeholder="Add a comment..."
        id="comment-textarea"
      ></textarea>
      <div class="comment-input-actions">
        <button @click="addComment" class="post-btn">Post</button>
      </div>
    </div>
    <div v-else class="login-prompt">
      <p>Please <router-link to="/login" class="login-link">login</router-link> to add a comment.</p>
    </div>

    <!-- 评论列表 -->
    <div class="comments">
      <Comment
        v-for="commentItem in paginatedComments"
        :key="commentItem.id"
        :comment="commentItem"
        @refreshComments="fetchComments"
      />
    </div>

    <!-- 分页控制 -->
    <div class="pagination-controls" v-if="totalPages > 1">
      <button
        @click="goToPreviousPage"
        :disabled="currentPage === 1"
        class="pagination-btn"
      >
        Previous
      </button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button
        @click="goToNextPage"
        :disabled="currentPage === totalPages"
        class="pagination-btn"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Comment from "./Comment.vue";

export default {
  name: "CommentSection",
  components: {
    Comment,
  },
  props: {
    historicalFigureId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      comments: [], // 当前页的顶级评论
      newComment: "", // 新顶级评论内容
      currentPage: 1, // 当前页码
      commentsPerPage: 10, // 每页显示的评论数量
      totalComments: 0, // 总评论数
      totalPages: 1, // 总页数
    };
  },
  mounted() {
    if (this.historicalFigureId) {
      this.fetchComments();
    }
  },
  computed: {
    paginatedComments() {
      return this.comments;
    },
  },
  methods: {
    // 获取认证 token
    getToken() {
      return localStorage.getItem("token");
    },
    // 获取评论列表
    fetchComments(page = this.currentPage) {
      const token = this.getToken();
      const params = {
        historical_figure: this.historicalFigureId,
        page: page,
        page_size: this.commentsPerPage,
      };
      axios
        .get(`/api/comments/`, {
          params: params,
          headers: token ? { Authorization: `Bearer ${token}` } : {},
        })
        .then((response) => {
          if (response.data.results) {
            const comments = this.processComments(response.data.results);
            this.comments = comments;
            this.totalComments = response.data.count; // 假设 API 返回总数
            this.totalPages = Math.ceil(this.totalComments / this.commentsPerPage);
            this.currentPage = page; // 更新当前页码
          } else {
            console.error("Unexpected response format:", response.data);
          }
        })
        .catch((error) => {
          console.error("Error fetching comments:", error);
        });
    },
    // 处理评论数据，组织父子关系
    processComments(comments) {
      const commentMap = {};
      comments.forEach((comment) => {
        comment.replies = [];
        comment.replyCount = 0; // 初始化回复计数
        commentMap[comment.id] = comment;
      });
      comments.forEach((comment) => {
        if (comment.parent) {
          // 如果父评论在当前页中
          if (commentMap[comment.parent]) {
            commentMap[comment.parent].replies.push(comment);
            commentMap[comment.parent].replyCount += 1; // 增加回复计数
          }
        }
      });
      // 过滤出所有顶级评论（parent === null）
      return Object.values(commentMap).filter(comment => comment.parent === null);
    },
    // 添加新评论
    addComment() {
      if (this.newComment.trim() === "") {
        return;
      }

      const token = this.getToken();
      if (!token) {
        console.error("User is not authenticated");
        this.$router.push({ name: "Login" });
        return;
      }

      axios
        .post(
          `/api/comments/`,
          {
            historical_figure: this.historicalFigureId,
            text: this.newComment,
            parent: null, // Null indicates a top-level comment
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )
        .then(() => {
          this.newComment = "";
          this.fetchComments(1); // 重新加载第一页以显示新评论
        })
        .catch((error) => {
          console.error("Error posting comment:", error);
        });
    },
    // 跳转到上一页
    goToPreviousPage() {
      if (this.currentPage > 1) {
        this.fetchComments(this.currentPage - 1);
      }
    },
    // 跳转到下一页
    goToNextPage() {
      if (this.currentPage < this.totalPages) {
        this.fetchComments(this.currentPage + 1);
      }
    },
  },
};
</script>

<style scoped>
.comment-section {
  margin-top: 30px;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.comment-section h2 {
  margin-bottom: 20px;
  color: #333333;
}

.comment-input {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.comment-input textarea {
  width: 100%;
  min-height: 80px;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  resize: vertical;
  font-size: 14px;
  color: #333333;
}

.comment-input-actions {
  display: flex;
  align-items: center;
  margin-top: 10px;
}

.post-btn {
  padding: 8px 16px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.post-btn:hover {
  background-color: #2980b9;
}

.login-prompt p {
  color: #555555;
}

.login-link {
  color: #3498db;
  text-decoration: underline;
}

.comments {
  margin-top: 20px;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination-btn {
  padding: 8px 16px;
  margin: 0 10px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.pagination-btn:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #2980b9;
}
</style>
