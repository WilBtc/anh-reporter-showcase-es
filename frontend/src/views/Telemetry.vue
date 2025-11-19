<template>
  <div>
    <h2 class="text-3xl font-bold mb-6 text-gray-900">Telemetría en Tiempo Real</h2>

    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-600">Cargando datos de telemetría...</p>
    </div>

    <div v-else-if="error" class="bg-red-100 text-red-800 p-6 rounded-lg">
      <p><strong>Error:</strong> {{ error }}</p>
    </div>

    <div v-else>
      <!-- Wells Selector -->
      <div class="bg-white p-6 rounded-lg shadow mb-6">
        <label class="text-gray-700 font-semibold mb-2 block">Seleccionar Pozo:</label>
        <select v-model="selectedWellId" @change="loadTelemetry" class="border rounded px-4 py-2">
          <option value="">Todos los pozos</option>
          <option v-for="well in wells" :key="well.id" :value="well.id">
            {{ well.name }} ({{ well.api_number }})
          </option>
        </select>
      </div>

      <!-- Telemetry Data -->
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Pozo</th>
              <th>Petróleo (bbl/d)</th>
              <th>Gas (KSCF/d)</th>
              <th>Agua (bbl/d)</th>
              <th>Presión (PSI)</th>
              <th>Temp (°F)</th>
              <th>Calidad</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="reading in readings" :key="reading.id">
              <td>{{ formatDate(reading.timestamp) }}</td>
              <td>{{ getWellName(reading.well_id) }}</td>
              <td>{{ formatNumber(reading.oil_rate) }}</td>
              <td>{{ formatNumber(reading.gas_rate) }}</td>
              <td>{{ formatNumber(reading.water_rate) }}</td>
              <td>{{ formatNumber(reading.wellhead_pressure) }}</td>
              <td>{{ formatNumber(reading.wellhead_temperature) }}</td>
              <td>
                <span :class="`badge badge-${getQualityBadge(reading.data_quality_score)}`">
                  {{ reading.data_quality_score }}%
                </span>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="readings.length === 0" class="text-center py-12 text-gray-600">
          No hay datos de telemetría disponibles
        </div>
      </div>

      <!-- Stats Summary -->
      <div v-if="stats" class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
        <div class="stat-card">
          <h3 class="text-gray-600 text-sm font-semibold mb-2">PROMEDIO PETRÓLEO</h3>
          <p class="text-2xl font-bold text-gray-900">{{ formatNumber(stats.avg_oil_rate) }} bbl/d</p>
        </div>
        <div class="stat-card">
          <h3 class="text-gray-600 text-sm font-semibold mb-2">PROMEDIO GAS</h3>
          <p class="text-2xl font-bold text-gray-900">{{ formatNumber(stats.avg_gas_rate) }} KSCF/d</p>
        </div>
        <div class="stat-card">
          <h3 class="text-gray-600 text-sm font-semibold mb-2">TOTAL LECTURAS</h3>
          <p class="text-2xl font-bold text-gray-900">{{ stats.total_readings }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const readings = ref([])
const wells = ref([])
const stats = ref(null)
const selectedWellId = ref('')
const loading = ref(true)
const error = ref(null)

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

const getWellName = (wellId) => {
  const well = wells.value.find(w => w.id === wellId)
  return well ? well.name : `Well #${wellId}`
}

const getQualityBadge = (score) => {
  if (score >= 95) return 'success'
  if (score >= 85) return 'warning'
  return 'danger'
}

const loadWells = async () => {
  try {
    const response = await api.getWells()
    wells.value = response.data
  } catch (err) {
    console.error('Error loading wells:', err)
  }
}

const loadTelemetry = async () => {
  try {
    loading.value = true
    const params = selectedWellId.value ? { well_id: selectedWellId.value, limit: 50 } : { limit: 50 }
    const response = await api.getTelemetryReadings(params)
    readings.value = response.data

    // Load stats if well selected
    if (selectedWellId.value) {
      const statsResponse = await api.getTelemetryStats(selectedWellId.value)
      stats.value = statsResponse.data
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cargar telemetría'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadWells()
  await loadTelemetry()
})
</script>
