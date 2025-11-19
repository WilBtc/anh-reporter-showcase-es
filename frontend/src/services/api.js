import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:9110/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default {
  // Auth
  login(credentials) {
    return api.post('/auth/login', credentials)
  },

  // Dashboard
  getDashboardOverview() {
    return api.get('/dashboard/overview')
  },

  getProductionHistory(days = 7) {
    return api.get(`/dashboard/production/history?days=${days}`)
  },

  getRealtimeMetrics() {
    return api.get('/dashboard/realtime')
  },

  // Telemetry
  getTelemetryReadings(params) {
    return api.get('/telemetry/', { params })
  },

  createTelemetryReading(data) {
    return api.post('/telemetry/', data)
  },

  getTelemetryStats(wellId, params) {
    return api.get(`/telemetry/stats/${wellId}`, { params })
  },

  // Wells
  getWells(params) {
    return api.get('/wells/', { params })
  },

  getWell(id) {
    return api.get(`/wells/${id}`)
  },

  // Reports
  getReports(params) {
    return api.get('/reports/', { params })
  },

  getReport(id) {
    return api.get(`/reports/${id}`)
  },

  generateReport(reportDate) {
    return api.post('/reports/generate', { report_date: reportDate })
  },

  uploadReport(id) {
    return api.post(`/reports/${id}/upload`)
  },

  // Alerts
  getAlerts(params) {
    return api.get('/alerts/', { params })
  },

  getAlert(id) {
    return api.get(`/alerts/${id}`)
  },

  resolveAlert(id, notes) {
    return api.post(`/alerts/${id}/resolve`, { notes })
  },

  getAnomalies(params) {
    return api.get('/alerts/anomalies/', { params })
  },

  // System
  getSystemInfo() {
    return api.get('/system/info')
  },

  healthCheck() {
    return api.get('/health')
  }
}
