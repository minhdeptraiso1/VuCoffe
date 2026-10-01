import { createRouter, createWebHistory } from "vue-router";

import LoginPage from "@/modules/auth/pages/LoginPage.vue";
import RegisterPage from "@/modules/auth/pages/RegisterPage.vue";
import ProfilePage from "@/modules/profile/pages/ProfilePage.vue";
import AdminDashboardPage from "@/pages/AdminDashboardPage.vue";
import CustomerDashboardPage from "@/pages/CustomerDashboardPage.vue";
import EmployeeDashboardPage from "@/pages/EmployeeDashboardPage.vue";
import ForbiddenPage from "@/pages/ForbiddenPage.vue";
import HomePage from "@/pages/HomePage.vue";
import NotFoundPage from "@/pages/NotFoundPage.vue";

import { installRouterGuards } from "./guards";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/login", name: "login", component: LoginPage, meta: { guestOnly: true } },
    { path: "/register", name: "register", component: RegisterPage, meta: { guestOnly: true } },
    { path: "/", name: "home", component: HomePage },
    { path: "/menu", name: "menu", component: () => import("@/pages/MenuPage.vue") },
    {
      path: "/account",
      name: "customer-dashboard",
      component: CustomerDashboardPage,
      meta: { requiresAuth: true, roles: ["customer"] },
    },
    {
      path: "/employee",
      name: "employee-dashboard",
      component: EmployeeDashboardPage,
      meta: { requiresAuth: true, roles: ["employee"] },
    },
    {
      path: "/admin",
      name: "admin-dashboard",
      component: AdminDashboardPage,
      meta: { requiresAuth: true, roles: ["admin"] },
    },
    {
      path: "/admin/employees",
      name: "admin-employees",
      component: () => import("@/modules/employees/pages/EmployeeManagementPage.vue"),
      meta: { requiresAuth: true, roles: ["admin"] },
    },
    {
      path: "/admin/catalog",
      name: "admin-catalog",
      component: () => import("@/modules/catalog/pages/CatalogManagementPage.vue"),
      meta: { requiresAuth: true, roles: ["admin"] },
    },
    {
      path: "/admin/inventory",
      name: "admin-inventory",
      component: () => import("@/modules/inventory/pages/InventoryManagementPage.vue"),
      meta: { requiresAuth: true, roles: ["admin"] },
    },
    {
      path: "/admin/imports",
      name: "admin-imports",
      component: () => import("@/modules/imports/pages/ImportManagementPage.vue"),
      meta: { requiresAuth: true, roles: ["admin"] },
    },
    { path: "/profile", name: "profile", component: ProfilePage, meta: { requiresAuth: true } },
    { path: "/forbidden", name: "forbidden", component: ForbiddenPage },
    { path: "/:pathMatch(.*)*", name: "not-found", component: NotFoundPage },
  ],
  scrollBehavior: (to) => (to.hash ? { el: to.hash } : { top: 0 }),
});

installRouterGuards(router);
