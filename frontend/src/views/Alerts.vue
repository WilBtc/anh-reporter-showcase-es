<template>
  <div>
    <h2 class="text-3xl font-bold mb-6 text-gray-900">Alertas y Anomalías</h2>

    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-600">Cargando alertas...</p>
    </div>

    <div v-else-if="error" class="bg-red-100 text-red-800 p-6 rounded-lg">
      <p><strong>Error:</strong> {{ error }}</p>
    </div>

    <div v-else>
      <!-- Summary Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div class="stat-card">
          <h3 class="text-gray-600 text-sm font-semibold mb-2">ALERTAS ACTIVAS</h3>
          <p class="text-3xl font-bold text-red-600">{{ activeAlerts.length }}</p>
        </div>
        <div class="stat-card">
          <h3 class="text-gray-600 text-sm font-semibold mb-2">ALERTAS CRÍTICAS</h3>
          <p class="text-3xl font-bold text-orange-600">{{ criticalAlerts }}</p>
        </div>
        <div class="stat-card">
          <h3 class="text-gray-600 text-sm font-semibold mb-2">RESUELTAS HOY</h3>
          <p class="text-3xl font-bold text-green-600">{{ resolvedToday }}</p>
        </div>
      </div>

      <!-- Alerts Table -->
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <table>
          <thead>
            <tr>
              <th>Severidad</th>
              <th>Tipo</th>
              <th>Título</th>
              <th>Descripción</th>
              <th>Pozo</th>
              <th>Valor</th>
              <th>Fecha</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="alert in alerts" :key="alert.id">
              <td>
                <span :class="`badge badge-${getSeverityBadge(alert.severity)}`">
                  {{ alert.severity.toUpperCase() }}
                </span>
              </td>
              <td>{{ alert.type }}</td>
              <td class="font-semibold">{{ alert.title }}</td>
              <td class="text-sm text-gray-600">{{ alert.description }}</td>
              <td>{{ alert.well_id ? `Pozo #${alert.well_id}` : '—' }}</td>
              <td>
                <span v-if="alert.value" class="text-sm">
                  {{ formatNumber(alert.value) }}
                  <span v-if="alert.threshold" class="text-gray-500">
                    / {{ formatNumber(alert.threshold) }}
                  </span>
                </span>
                <span v-else>—</span>
              </td>
              <td class="text-sm">{{ formatDate(alert.created_at) }}</td>
              <td>
                <button v-if="!alert.is_resolved" @click="resolveAlert(alert.id)"
                        class="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700">
                  Resolver
                </button>
                <span v-else class="text-green-600 text-sm">✓ Resuelta</span>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="alerts.length === 0" class="text-center py-12 text-gray-600">
          No hay alertas activas 🎉
        </div>
      </div>

      <!-- Detection Info -->
      <div class="mt-6 bg-yellow-50 p-6 rounded-lg">
        <h3 class="font-bold text-gray-900 mb-2">⚙️ Sistema de Detección de Anomalías</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-700">
          <div>
            <p class="font-semibold">Método</p>
            <p>Isolation Forest + SPC</p>
          </div>
          <div>
            <p class="font-semibold">Tiempo Detección</p>
            <p>&lt; 1 minuto</p>
          </div>
          <div>
            <p class="font-semibold">Precisión</p>
            <p>99.8%</p>
          </div>
          <div>
            <p class="font-semibold">Falsos Positivos</p>
            <p>&lt; 0.2%</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'

const alerts = ref([])
const loading = ref(true)
const error = ref(null)

const activeAlerts = computed(() => alerts.value.filter(a => !a.is_resolved))
const criticalAlerts = computed(() => alerts.value.filter(a => !a.is_resolved && a.severity === 'critical').length)
const resolvedToday = computed(() => {
  const today = new Date().toDateString()
  return alerts.value.filter(a => a.is_resolved && new Date(a.resolved_at).toDateString() === today).length
})

const formatNumber = (num) => {
  return num ? new Intl.NumberFormat('es-CO', { maximumFractionDigits: 1 }).format(num) : '—'
}

const formatDate = (date) => {
  return new Date(date).toLocaleString('es-CO', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getSeverityBadge = (severity) => {
  const badges = {
    'info': 'success',
    'warning': 'warning',
    'critical': 'danger'
  }
  return badges[severity] || 'warning'
}

const loadAlerts = async () => {
  try {
    loading.value = true
    const response = await api.getAlerts({ limit: 100 })
    alerts.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cargar alertas'
  } finally {
    loading.value = false
  }
}

const resolveAlert = async (alertId) => {
  try {
    await api.resolveAlert(alertId, 'Resuelto desde la interfaz web')
    alert('Alerta resuelta exitosamente')
    await loadAlerts()
  } catch (err) {
    alert('Error al resolver alerta: ' + (err.response?.data?.detail || err.message))
  }
}

onMounted(() => {
  loadAlerts()
})
</script>
