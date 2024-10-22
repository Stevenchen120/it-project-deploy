import { createApp } from "vue";
import App from "/src/App.vue";
import router from "./router/index.js";
import store from "./store/index.js";
import axios from "axios";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

const app = createApp(App);
// 使用 Toastification 插件
const toastOptions = {
    position: "top-right",
    timeout: 5000,
    closeOnClick: true,
    pauseOnFocusLoss: true,
    pauseOnHover: true,
    draggable: true,
    draggablePercent: 0.6,
    showCloseButtonOnHover: false,
    hideProgressBar: false,
    closeButton: "button",
    icon: true,
    rtl: false,
};

app.use(Toast, toastOptions);
app.use(router);
app.use(store);

app.config.globalProperties.$axios = axios;

app.mount("#app");
