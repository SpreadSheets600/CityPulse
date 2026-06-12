<template>
  <div class="min-h-screen bg-base-100 text-base-content antialiased py-8 px-4 sm:px-6 lg:px-8">
    <main class="max-w-7xl mx-auto">
      <div>
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
          <div>
            <h2 class="text-3xl font-extrabold text-slate-100 font-mono tracking-wider uppercase">Geofencing</h2>
            <p class="mt-1 text-sm text-slate-400 font-sans">Map geographic boundary coordinates to specific departments for auto-dispatching.</p>
          </div>
          <button @click="showForm = !showForm" class="btn btn-primary rounded-xl font-bold px-5 shadow-lg shadow-blue-500/10 cursor-pointer">
            {{ showForm ? 'CANCEL' : 'ADD GEOFENCE' }}
          </button>
        </div>

        <!-- Create Geofence Form -->
        <div v-if="showForm" class="bg-base-200 border border-base-300 rounded-3xl p-6 md:p-8 shadow-xl mb-8">
          <h3 class="text-xs font-bold font-mono text-slate-400 uppercase tracking-widest mb-6">New Boundary Rules</h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <div>
              <label class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">Boundary Name</span></label>
              <input v-model="form.name" class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary font-sans text-sm" placeholder="e.g. North Ward Zone A" />
            </div>
            <div>
              <label class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">Assigned Department</span></label>
              <select v-model="form.department_id" class="select select-bordered w-full rounded-xl border-base-300 focus:border-primary font-mono text-xs">
                <option value="">Select department</option>
                <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
              </select>
            </div>
            <div>
              <label class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">Min Latitude</span></label>
              <input v-model.number="form.min_lat" type="number" step="any" class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary font-mono text-xs" />
            </div>
            <div>
              <label class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">Max Latitude</span></label>
              <input v-model.number="form.max_lat" type="number" step="any" class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary font-mono text-xs" />
            </div>
            <div>
              <label class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">Min Longitude</span></label>
              <input v-model.number="form.min_lng" type="number" step="any" class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary font-mono text-xs" />
            </div>
            <div>
              <label class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">Max Longitude</span></label>
              <input v-model.number="form.max_lng" type="number" step="any" class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary font-mono text-xs" />
            </div>
          </div>
          <div class="mt-6">
            <button @click="createGeofence" class="btn btn-accent rounded-xl font-bold px-6 cursor-pointer">
              SAVE GEOFENCE RULE
            </button>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="flex justify-center py-16">
          <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-primary"></div>
        </div>

        <!-- Geofences Table -->
        <div v-else-if="geofences.length" class="bg-base-200 border border-base-300 shadow-xl rounded-3xl overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-base-300 bg-base-200">
              <thead class="bg-base-300/60 font-mono text-2xs uppercase tracking-wider text-slate-400">
                <tr>
                  <th class="px-6 py-4 text-left font-bold">Name</th>
                  <th class="px-6 py-4 text-left font-bold">Department</th>
                  <th class="px-6 py-4 text-left font-bold">Bounds (Latitude)</th>
                  <th class="px-6 py-4 text-left font-bold">Bounds (Longitude)</th>
                  <th class="px-6 py-4"></th>
                </tr>
              </thead>
              <tbody class="divide-y divide-base-300/40 text-slate-200">
                <tr v-for="f in geofences" :key="f.id" class="hover:bg-base-300/10 transition-colors">
                  <td class="px-6 py-4 text-sm font-bold text-slate-100">{{ f.name }}</td>
                  <td class="px-6 py-4 text-sm text-slate-300">{{ f.department_name }}</td>
                  <td class="px-6 py-4 text-sm font-mono text-xs text-slate-400">{{ f.min_lat }} — {{ f.max_lat }}</td>
                  <td class="px-6 py-4 text-sm font-mono text-xs text-slate-400">{{ f.min_lng }} — {{ f.max_lng }}</td>
                  <td class="px-6 py-4 text-right">
                    <button @click="deleteGeofence(f.id)" class="text-error hover:text-red-400 text-xs font-mono cursor-pointer bg-transparent border-0">DELETE</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div v-else class="text-center py-16 border border-dashed border-base-300 rounded-3xl bg-base-200/40 text-slate-500 font-mono text-sm">No geofences configured yet.</div>
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

<style scoped>
/* Scoped styles */
</style>
