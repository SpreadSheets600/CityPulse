<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-5xl mx-auto">
      <div class="mb-6 flex items-center justify-between">
        <h1 class="text-2xl font-bold">Manage Issue</h1>
        <router-link to="/admin-dashboard" class="text-indigo-600 hover:text-indigo-800">← Back</router-link>
      </div>

      <div v-if="loading" class="text-center py-10">Loading...</div>
      <div v-else-if="error" class="text-red-600 py-2">{{ error }}</div>

      <div v-else-if="issue">
        <!-- Issue summary -->
        <div class="bg-white rounded shadow p-4 sm:p-6 mb-6">
          <h2 class="text-xl font-semibold mb-2">{{ issue.title }}</h2>
          <p class="text-gray-600 mb-4">{{ issue.description }}</p>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-sm text-gray-500">
            <div><strong>Status:</strong> <span class="capitalize">{{ issue.status }}</span></div>
            <div><strong>Type:</strong> {{ issue.issue_type }}</div>
            <div><strong>Address:</strong> {{ issue.address }}</div>
            <div><strong>Created:</strong> {{ new Date(issue.created_at).toLocaleDateString() }}</div>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Update status -->
          <div class="bg-white rounded shadow p-4 sm:p-6">
            <h3 class="font-semibold mb-4">Update Status</h3>
            <select v-model="status" class="w-full border rounded p-3 mb-4 text-sm">
              <option value="pending">Pending</option>
              <option value="in_progress">In Progress</option>
              <option value="resolved">Resolved</option>
              <option value="rejected">Rejected</option>
              <option value="verified">Verified</option>
            </select>
            <button @click="saveStatus"
              class="w-full bg-blue-600 text-white px-4 py-3 rounded hover:bg-blue-700 text-sm font-medium">Save
              Status</button>
          </div>

          <!-- Assign department -->
          <div class="bg-white rounded shadow p-4 sm:p-6">
            <h3 class="font-semibold mb-4">Assign Department</h3>
            <select v-model="departmentId" class="w-full border rounded p-3 mb-4 text-sm">
              <option disabled value="">Select Department</option>
              <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
            </select>
            <button @click="assignDepartment"
              class="w-full bg-green-600 text-white px-4 py-3 rounded hover:bg-green-700 text-sm font-medium">Assign
              Department</button>
          </div>
        </div>

        <!-- Post update -->
        <div class="bg-white rounded shadow p-4 sm:p-6 mt-6">
          <h3 class="font-semibold mb-4">Post Update</h3>
          <input v-model="updateTitle" type="text" placeholder="Update title"
            class="w-full border rounded p-3 mb-4 text-sm" />
          <textarea v-model="updateBody" rows="4" placeholder="Update details"
            class="w-full border rounded p-3 mb-4 text-sm"></textarea>
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">Progress: {{ progress }}%</label>
            <input v-model.number="progress" type="range" min="0" max="100" class="w-full" />
          </div>
          <input type="file" multiple accept="image/*" @change="onUpdateFileChange"
            class="w-full border rounded p-3 mb-4 text-sm" />
          <button @click="postUpdate"
            class="w-full bg-indigo-600 text-white px-4 py-3 rounded hover:bg-indigo-700 text-sm font-medium">Publish
            Update</button>
        </div>

        <!-- Existing updates -->
        <div class="bg-white rounded shadow p-4 sm:p-6 mt-6">
          <h3 class="font-semibold mb-4">Updates</h3>
          <div v-if="updates.length === 0" class="text-sm text-gray-500 py-4">No updates yet.</div>
          <div v-else class="space-y-4">
            <div v-for="u in updates" :key="u.id" class="border rounded p-4">
              <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start mb-2">
                <h4 class="font-medium mb-1 sm:mb-0">{{ u.title }}</h4>
                <span class="text-xs text-gray-500">{{ new Date(u.created_at).toLocaleString() }}</span>
              </div>
              <p class="text-sm text-gray-700 mb-2">{{ u.body }}</p>
              <div class="text-xs text-gray-500 mb-2">Progress: {{ u.progress }}%</div>
              <div v-if="u.image_urls && u.image_urls.length > 0" class="mt-3">
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                  <img v-for="(url, index) in u.image_urls" :key="index" :src="url" :alt="`Update image ${index + 1}`"
                    class="w-full h-24 object-cover rounded" />
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '../api/client'

const route = useRoute()

const issue = ref(null)
const loading = ref(false)
const error = ref('')

const status = ref('pending')
const departments = ref([])
const departmentId = ref('')

const updateTitle = ref('')
const updateBody = ref('')
const progress = ref(0)

const updates = ref([])

const updateFiles = ref([])

const loadIssue = async () => {
  loading.value = true
  try {
    const resp = await axios.get(`/api/issues/${route.params.id}`)
    issue.value = resp.data.issue
    status.value = issue.value.status
    if (issue.value?.department_id) {
      departmentId.value = issue.value.department_id
    }
  } catch (e) {
    error.value = e.response?.data?.error || 'Failed to load issue'
  } finally {
    loading.value = false
  }
}

const loadDepartments = async () => {
  try {
    const resp = await axios.get('/api/admin/departments')
    departments.value = resp.data.departments
  } catch (e) {
    console.error(e)
  }
}

const loadUpdates = async () => {
  try {
    const resp = await axios.get(`/api/issues/${route.params.id}/updates`)
    updates.value = resp.data.updates
  } catch (e) {
    console.error(e)
  }
}

const saveStatus = async () => {
  try {
    const resp = await axios.put(`/api/admin/issues/${route.params.id}/status`, { status: status.value })
    issue.value = resp.data.issue
  } catch (e) {
    alert(e.response?.data?.error || 'Failed to update status')
  }
}

const assignDepartment = async () => {
  if (!departmentId.value) return
  try {
    const resp = await axios.put(`/api/admin/issues/${route.params.id}/department`, { department_id: departmentId.value })
    issue.value = resp.data.issue
  } catch (e) {
    alert(e.response?.data?.error || 'Failed to assign department')
  }
}

const postUpdate = async () => {
  if (!updateTitle.value) return alert('Title is required')

  const formData = new FormData()
  formData.append('title', updateTitle.value)
  formData.append('body', updateBody.value)
  formData.append('progress', progress.value.toString())

  updateFiles.value.forEach(file => {
    formData.append('images', file)
  })

  try {
    await axios.post(`/api/admin/issues/${route.params.id}/updates`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    updateTitle.value = ''
    updateBody.value = ''
    progress.value = 0
    updateFiles.value = []
    await loadUpdates()
  } catch (e) {
    alert(e.response?.data?.error || 'Failed to post update')
  }
}

const onUpdateFileChange = (event) => {
  updateFiles.value = Array.from(event.target.files)
}

onMounted(async () => {
  await loadIssue()
  await Promise.all([loadDepartments(), loadUpdates()])
})
</script>
