import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Telemetry from '../views/Telemetry.vue'
import Reports from '../views/Reports.vue'
import Alerts from '../views/Alerts.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/telemetry',
      name: 'telemetry',
      component: Telemetry
    },
    {
      path: '/reports',
      name: 'reports',
      component: Reports
    },
    {
      path: '/alerts',
      name: 'alerts',
      component: Alerts
    }
  ]
})

export default router
