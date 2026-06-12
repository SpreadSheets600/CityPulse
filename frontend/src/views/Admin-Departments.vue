<template>
  <div class="min-h-screen bg-gray-50">
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="flex justify-between items-center mb-8">
          <div>
            <h2 class="text-2xl font-bold text-gray-900">Departments</h2>
            <p class="mt-1 text-sm text-gray-600">Manage departments for issue assignment.</p>
          </div>
          <button @click="showForm = !showForm" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
            {{ showForm ? 'Cancel' : 'Add Department' }}
          </button>
        </div>

        <!-- Create Department Form -->
        <div v-if="showForm" class="bg-white shadow rounded-lg p-6 mb-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">New Department</h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Name *</label>
              <input v-model="form.name" class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm" placeholder="e.g. Road Maintenance" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Description</label>
              <input v-model="form.description" class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm" placeholder="Brief description" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Contact Email *</label>
              <input v-model="form.contact_email" type="email" class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm" placeholder="dept@citypulse.com" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Contact Phone *</label>
              <input v-model="form.contact_phone" type="tel" class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm" placeholder="+1234567890" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">SLA Hours</label>
              <input v-model.number="form.sla_hours" type="number" class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm" placeholder="72" />
            </div>
          </div>
          <div class="mt-4">
            <button @click="createDepartment" :disabled="creating" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 disabled:opacity-50">
              {{ creating ? 'Creating...' : 'Create Department' }}
            </button>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
        </div>

        <!-- Departments Table -->
        <div v-else-if="departments.length" class="bg-white shadow overflow-hidden sm:rounded-lg">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Description</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Contact Email</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Contact Phone</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">SLA (hrs)</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Issues</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr v-for="dept in departments" :key="dept.id">
                <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ dept.name }}</td>
                <td class="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">{{ dept.description || '-' }}</td>
                <td class="px-6 py-4 text-sm text-gray-500">{{ dept.contact_email }}</td>
                <td class="px-6 py-4 text-sm text-gray-500">{{ dept.contact_phone }}</td>
                <td class="px-6 py-4 text-sm text-gray-500">{{ dept.sla_hours || 72 }}</td>
                <td class="px-6 py-4 text-sm text-gray-500">{{ dept.issue_count || 0 }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else class="text-center py-12 bg-white shadow rounded-lg">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No departments yet</h3>
          <p class="mt-1 text-sm text-gray-500">Create your first department to start assigning issues.</p>
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
