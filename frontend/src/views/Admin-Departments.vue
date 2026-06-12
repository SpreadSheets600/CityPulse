<template>
  <div class="min-h-screen bg-base-100 text-base-content antialiased py-8 px-4 sm:px-6 lg:px-8">
    <main class="max-w-7xl mx-auto">
      <div>
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
          <div>
            <h2 class="text-3xl font-extrabold text-slate-100 font-mono tracking-wider uppercase">Departments</h2>
            <p class="mt-1 text-sm text-slate-400 font-sans">Manage city department contact details and SLA parameters.</p>
          </div>
          <button @click="showForm = !showForm" class="btn btn-primary rounded-xl font-bold px-5 shadow-lg shadow-blue-500/10 cursor-pointer">
            {{ showForm ? 'CANCEL' : 'ADD DEPARTMENT' }}
          </button>
        </div>

        <!-- Create Department Form -->
        <div v-if="showForm" class="bg-base-200 border border-base-300 rounded-3xl p-6 md:p-8 shadow-xl mb-8">
          <h3 class="text-xs font-bold font-mono text-slate-400 uppercase tracking-widest mb-6">New Department Profile</h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <div>
              <label class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">Name *</span></label>
              <input v-model="form.name" class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary font-sans text-sm" placeholder="e.g. Road Maintenance" />
            </div>
            <div>
              <label class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">Description</span></label>
              <input v-model="form.description" class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary font-sans text-sm" placeholder="Brief description" />
            </div>
            <div>
              <label class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">Contact Email *</span></label>
              <input v-model="form.contact_email" type="email" class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary font-mono text-xs" placeholder="dept@citypulse.com" />
            </div>
            <div>
              <label class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">Contact Phone *</span></label>
              <input v-model="form.contact_phone" type="tel" class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary font-mono text-xs" placeholder="+1234567890" />
            </div>
            <div>
              <label class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">SLA Hours (Resolution limit)</span></label>
              <input v-model.number="form.sla_hours" type="number" class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary font-mono text-xs" placeholder="72" />
            </div>
          </div>
          <div class="mt-6">
            <button @click="createDepartment" :disabled="creating" class="btn btn-accent rounded-xl font-bold px-6 cursor-pointer">
              {{ creating ? 'CREATING...' : 'CREATE DEPARTMENT' }}
            </button>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="flex justify-center py-16">
          <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-primary"></div>
        </div>

        <!-- Departments Table -->
        <div v-else-if="departments.length" class="bg-base-200 border border-base-300 shadow-xl rounded-3xl overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-base-300 bg-base-200">
              <thead class="bg-base-300/60 font-mono text-2xs uppercase tracking-wider text-slate-400">
                <tr>
                  <th class="px-6 py-4 text-left font-bold">Name</th>
                  <th class="px-6 py-4 text-left font-bold">Description</th>
                  <th class="px-6 py-4 text-left font-bold">Contact Email</th>
                  <th class="px-6 py-4 text-left font-bold">Contact Phone</th>
                  <th class="px-6 py-4 text-left font-bold">SLA (hrs)</th>
                  <th class="px-6 py-4 text-left font-bold">Issues</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-base-300/40 text-slate-200">
                <tr v-for="dept in departments" :key="dept.id" class="hover:bg-base-300/10 transition-colors">
                  <td class="px-6 py-4 text-sm font-bold text-slate-100">{{ dept.name }}</td>
                  <td class="px-6 py-4 text-sm text-slate-400 max-w-xs truncate">{{ dept.description || '-' }}</td>
                  <td class="px-6 py-4 text-sm font-mono text-slate-300 text-xs">{{ dept.contact_email }}</td>
                  <td class="px-6 py-4 text-sm font-mono text-slate-300 text-xs">{{ dept.contact_phone }}</td>
                  <td class="px-6 py-4 text-sm font-mono text-slate-300">{{ dept.sla_hours || 72 }}</td>
                  <td class="px-6 py-4 text-sm font-mono text-slate-300">{{ dept.issue_count || 0 }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-else class="text-center py-16 border border-dashed border-base-300 rounded-3xl bg-base-200/40">
          <svg class="mx-auto h-12 w-12 text-slate-600 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
          <h3 class="text-lg font-bold text-slate-300">No departments cataloged yet</h3>
          <p class="mt-1.5 text-sm text-slate-500">Create your first department to start assigning issues.</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from '../api/client'

const departments = ref([])
const loading = ref(false)
const creating = ref(false)
const showForm = ref(false)
const form = reactive({
  name: '',
  description: '',
  contact_email: '',
  contact_phone: '',
  sla_hours: 72,
})

const fetchDepartments = async () => {
  loading.value = true
  try {
    const resp = await axios.get('/api/admin/departments')
    departments.value = resp.data.departments || []
  } catch (e) {
    console.error('Failed to fetch departments', e)
  } finally {
    loading.value = false
  }
}

const createDepartment = async () => {
  if (!form.name || !form.contact_email || !form.contact_phone) {
    return alert('Name, Contact Email, and Contact Phone are required')
  }
  creating.value = true
  try {
    await axios.post('/api/admin/departments', {
      name: form.name,
      description: form.description,
      contact_email: form.contact_email,
      contact_phone: form.contact_phone,
      sla_hours: form.sla_hours,
    })
    form.name = ''
    form.description = ''
    form.contact_email = ''
    form.contact_phone = ''
    form.sla_hours = 72
    showForm.value = false
    await fetchDepartments()
  } catch (e) {
    alert(e.response?.data?.error || 'Failed to create department')
  } finally {
    creating.value = false
  }
}

onMounted(() => {
  fetchDepartments()
})
</script>

<style scoped>
/* Scoped styles */
</style>
