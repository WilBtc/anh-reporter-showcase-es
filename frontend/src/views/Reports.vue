<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-3xl font-bold text-gray-900">Reportes ANH</h2>
      <button @click="generateNewReport" class="bg-blue-900 text-white px-6 py-2 rounded font-semibold hover:bg-blue-800">
        + Generar Reporte
      </button>
    </div>

    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-600">Cargando reportes...</p>
    </div>

    <div v-else-if="error" class="bg-red-100 text-red-800 p-6 rounded-lg">
      <p><strong>Error:</strong> {{ error }}</p>
    </div>

    <div v-else>
      <!-- Reports Table -->
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <table>
          <thead>
            <tr>
              <th>Fecha Reporte</th>
              <th>Archivo</th>
              <th>Estado</th>
              <th>Pozos</th>
              <th>Lecturas</th>
              <th>Calidad</th>
              <th>Producción</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="report in reports" :key="report.id">
              <td>{{ formatDate(report.report_date) }}</td>
              <td class="text-sm font-mono">{{ report.filename }}</td>
              <td>
                <span :class="`badge badge-${getStatusBadge(report.status)}`">
                  {{ report.status.toUpperCase() }}
                </span>
              </td>
              <td>{{ report.total_wells || '—' }}</td>
              <td>{{ report.total_readings || '—' }}</td>
              <td>
                <span v-if="report.data_quality_score" :class="`badge badge-${report.data_quality_score >= 95 ? 'success' : 'warning'}`">
                  {{ report.data_quality_score }}%
                </span>
                <span v-else>—</span>
              </td>
              <td class="text-sm">
                <div v-if="report.oil_production_total">
                  Petróleo: {{ formatNumber(report.oil_production_total) }} bbl
                </div>
                <div v-if="report.gas_production_total">
                  Gas: {{ formatNumber(report.gas_production_total) }} KSCF
                </div>
              </td>
              <td>
                <button v-if="report.status === 'ready'" @click="uploadReport(report.id)"
                        class="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700">
                  Subir FTP
                </button>
                <button v-else-if="report.status === 'uploaded'"
                        class="bg-gray-300 text-gray-600 px-3 py-1 rounded text-sm cursor-not-allowed">
                  Enviado ✓
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="reports.length === 0" class="text-center py-12 text-gray-600">
          No hay reportes disponibles
        </div>
      </div>

      <!-- Report Generation Info -->
      <div class="mt-6 bg-blue-50 p-6 rounded-lg">
        <h3 class="font-bold text-gray-900 mb-2">📋 Información de Generación</h3>
        <ul class="text-sm text-gray-700 space-y-1">
          <li>• Generación automática: Diariamente a las 6:00 AM COT</li>
          <li>• Upload automático a FTP ANH: 6:50 AM COT</li>
          <li>• Formato: JSON según Anexo 4 Resolución ANH 0651/2025</li>
          <li>• Validación: 300+ reglas de negocio</li>
          <li>• Cumplimiento: 100% garantizado</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const reports = ref([])
const loading = ref(true)
const error = ref(null)

const formatNumber = (num) => {
  return num ? new Intl.NumberFormat('es-CO', { maximumFractionDigits: 0 }).format(num) : '—'
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('es-CO', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getStatusBadge = (status) => {
  const badges = {
    'pending': 'warning',
    'generating': 'warning',
    'ready': 'success',
    'uploaded': 'success',
    'failed': 'danger'
  }
  return badges[status] || 'warning'
}

const loadReports = async () => {
  try {
    loading.value = true
    const response = await api.getReports()
    reports.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cargar reportes'
  } finally {
    loading.value = false
  }
}

const generateNewReport = async () => {
  try {
    const reportDate = new Date().toISOString()
    await api.generateReport(reportDate)
    alert('Reporte generado exitosamente')
    await loadReports()
  } catch (err) {
    alert('Error al generar reporte: ' + (err.response?.data?.detail || err.message))
  }
}

const uploadReport = async (reportId) => {
  try {
    await api.uploadReport(reportId)
    alert('Reporte enviado a FTP ANH exitosamente')
    await loadReports()
  } catch (err) {
    alert('Error al subir reporte: ' + (err.response?.data?.detail || err.message))
  }
}

onMounted(() => {
  loadReports()
})
</script>
