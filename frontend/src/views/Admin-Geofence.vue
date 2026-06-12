<template>
  <div class="min-h-screen bg-gray-50">
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="flex justify-between items-center mb-8">
          <div>
            <h2 class="text-2xl font-bold text-gray-900">Geofencing</h2>
            <p class="mt-1 text-sm text-gray-600">Map geographic zones to departments for auto-assignment.</p>
          </div>
          <button @click="showForm = !showForm" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
            {{ showForm ? 'Cancel' : 'Add Geofence' }}
          </button>
        </div>

        <div v-if="showForm" class="bg-white shadow rounded-lg p-6 mb-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">New Geofence</h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Name</label>
              <input v-model="form.name" class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Department</label>
              <select v-model="form.department_id" class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm">
                <option value="">Select department</option>
                <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Min Latitude</label>
              <input v-model.number="form.min_lat" type="number" step="any" class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Max Latitude</label>
              <input v-model.number="form.max_lat" type="number" step="any" class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Min Longitude</label>
              <input v-model.number="form.min_lng" type="number" step="any" class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Max Longitude</label>
              <input v-model.number="form.max_lng" type="number" step="any" class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm" />
            </div>
          </div>
          <div class="mt-4">
            <button @click="createGeofence" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700">
              Save Geofence
            </button>
          </div>
        </div>

        <div v-if="loading" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
        </div>

        <div v-else-if="geofences.length" class="bg-white shadow overflow-hidden sm:rounded-lg">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Department</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Bounds (Lat)</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Bounds (Lng)</th>
                <th class="px-6 py-3"></th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr v-for="f in geofences" :key="f.id">
                <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ f.name }}</td>
                <td class="px-6 py-4 text-sm text-gray-500">{{ f.department_name }}</td>
                <td class="px-6 py-4 text-sm text-gray-500">{{ f.min_lat }} — {{ f.max_lat }}</td>
                <td class="px-6 py-4 text-sm text-gray-500">{{ f.min_lng }} — {{ f.max_lng }}</td>
                <td class="px-6 py-4 text-right">
                  <button @click="deleteGeofence(f.id)" class="text-red-600 hover:text-red-900 text-sm">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="text-center py-8 text-gray-500">No geofences configured yet.</div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from '../api/client'

const geofences = ref([])
const departments = ref([])
const loading = ref(false)
const showForm = ref(false)
const form = reactive({ name: '', department_id: '', min_lat: 0, max_lat: 0, min_lng: 0, max_lng: 0 })

const fetchAll = async () => {
  loading.value = true
  try {
    const [gfRes, deptRes] = await Promise.all([
      axios.get('/api/admin/geofences'),
      axios.get('/api/admin/departments'),
    ])
    geofences.value = gfRes.data.geofences || []
    departments.value = deptRes.data.departments || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const createGeofence = async () => {
  try {
    await axios.post('/api/admin/geofences', form)
    showForm.value = false
    form.name = ''
    form.department_id = ''
    form.min_lat = 0
    form.max_lat = 0
    form.min_lng = 0
    form.max_lng = 0
    await fetchAll()
  } catch (e) {
    console.error(e)
  }
}

const deleteGeofence = async (id) => {
  if (!confirm('Delete this geofence?')) return
  try {
    await axios.delete(`/api/admin/geofences/${id}`)
    await fetchAll()
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => fetchAll())
</script>
