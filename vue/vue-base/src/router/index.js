// src/router/index.js
// import { createRouter, createWebHistory } from "vue-router";
// import Login from "../components/Login.vue";
// import HomeView from "../views/HomeView.vue";

// const routes = [
//   {
//     path: "/login",
//     name: "Login",
//     component: Login,
//   },
//   {
//     path: "/",
//     name: "home",
//     component: HomeView,
//   },
// ];

// const router = createRouter({
//   history: createWebHistory(),
//   routes,
// });

// export default router;
import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import HistoryDetail from "@/views/HistoryDetail.vue";
import CategoryPage from "@/views/CategoryPage.vue";
import ActivateEmail from "../views/ActivateEmail.vue";
import Login from "../views/Login.vue";
import ResetPassword from "../views/ResetPassword.vue";
import Passwordreset from "../views/Passwordreset.vue";
import Register from "../views/Register.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/about",
      name: "about",

      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/history/:id",
      name: "HistoryDetail",
      component: HistoryDetail,
    },
    // Add the route for category page
    {
      path: '/category',
      name: "CategoryPage",
      component: CategoryPage,
    },
      {
      path: "/register",
      name: "Register",
      component: Register,
    },
    {
      path: "/activate/:uid/:token",
      name: "ActivateEmail",
      component: ActivateEmail,
    },
    {
      path: "/login",
      name: "Login",
      component: Login,
    },
    {
      path: "/reset_password",
      name: "ResetPassword",
      component: ResetPassword,
    },
    {
      path: "/password_reset/:uid/:token",
      name: "PasswordReset",
      component: Passwordreset,
    },
  ],
});

export default router;
