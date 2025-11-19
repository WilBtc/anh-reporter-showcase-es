<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <nav class="bg-blue-900 text-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-bold">ANH Smart Reporter</h1>
            <span class="ml-4 text-sm text-blue-200">v3.0.0</span>
          </div>
          <div class="flex space-x-4">
            <router-link to="/" class="hover:bg-blue-800 px-3 py-2 rounded">Dashboard</router-link>
            <router-link to="/telemetry" class="hover:bg-blue-800 px-3 py-2 rounded">Telemetría</router-link>
            <router-link to="/reports" class="hover:bg-blue-800 px-3 py-2 rounded">Reportes</router-link>
            <router-link to="/alerts" class="hover:bg-blue-800 px-3 py-2 rounded">Alertas</router-link>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <router-view />
    </main>

    <footer class="bg-gray-800 text-white text-center py-4 mt-12">
      <p>&copy; 2025 INSA Ingeniería y Automatización - Todos los derechos reservados</p>
    </footer>
  </div>
</template>

<script setup>
// App component
</script>
