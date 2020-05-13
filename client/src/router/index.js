import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/TSP",
    name: "TSP",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/TSP.vue")
  },
  {
    path: "/FE",
    name: "FE",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/FE.vue")
  },
  {
    path: "/SAT",
    name: "SAT",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/SAT.vue")
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
