<template>
  <div class="min-h-screen bg-base-100 text-base-content antialiased py-8 px-4 sm:px-6 lg:px-8">
    <main class="max-w-4xl mx-auto">
      <div>
        <div class="mb-8">
          <h2 class="text-3xl font-extrabold text-slate-100 font-mono tracking-wider uppercase">
            User Profile
          </h2>
          <p class="mt-1 text-sm text-slate-400">
            Manage your credentials and neighborhood association profile.
          </p>
        </div>

        <div
          class="bg-base-200 border border-base-300 shadow-xl rounded-3xl overflow-hidden p-6 md:p-8"
        >
          <!-- User Profile Details -->
          <div>
            <div class="flex items-center mb-8 pb-8 border-b border-base-300">
              <div class="flex-shrink-0">
                <img
                  v-if="profilePictureUrl"
                  :src="profilePictureUrl"
                  alt="Profile"
                  class="w-20 h-20 rounded-2xl object-cover border border-base-300 shadow-lg"
                />
                <div
                  v-else
                  class="w-20 h-20 rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center text-white font-mono text-2xl font-bold"
                >
                  {{ userInitials }}
                </div>
              </div>
              <div class="ml-5">
                <h3 class="text-xl font-bold text-slate-100">
                  {{ user?.firstname }} {{ user?.lastname }}
                </h3>
                <p class="text-sm font-mono text-slate-400 mt-1">{{ user?.email }}</p>
              </div>
            </div>

            <!-- Notifications -->
            <div
              v-if="success"
              class="border border-emerald-500/20 bg-emerald-500/5 text-emerald-400 p-4 rounded-xl text-center text-xs font-mono mb-6"
            >
              Profile Updated Successfully
            </div>
            <div
              v-if="error"
              class="border border-error/20 bg-error/5 text-error text-center text-xs font-mono p-4 rounded-xl mb-6"
            >
              {{ error }}
            </div>

            <div class="flex justify-between items-center mb-6">
              <h3 class="text-xs font-bold font-mono text-slate-400 uppercase tracking-widest">
                Personal Information
              </h3>
              <button
                v-if="!editing"
                @click="startEditing"
                class="btn btn-sm btn-outline border-base-300 hover:border-slate-500 rounded-xl font-mono cursor-pointer"
              >
                Edit
              </button>
              <div v-else class="flex gap-2">
                <button
                  @click="saveProfile"
                  :disabled="saving"
                  class="btn btn-sm btn-primary rounded-xl font-mono cursor-pointer"
                >
                  {{ saving ? 'SAVING...' : 'SAVE CHANGES' }}
                </button>
                <button
                  @click="cancelEditing"
                  class="btn btn-sm btn-ghost rounded-xl font-mono cursor-pointer"
                >
                  Cancel
                </button>
              </div>
            </div>

            <dl class="grid grid-cols-1 gap-x-6 gap-y-6 sm:grid-cols-2">
              <div class="sm:col-span-1">
                <dt class="text-2xs font-mono text-slate-500 uppercase tracking-widest">
                  First Name
                </dt>
                <dd v-if="!editing" class="mt-1 text-sm text-slate-200">{{ user?.firstname }}</dd>
                <input
                  v-else
                  v-model="form.firstname"
                  type="text"
                  class="mt-1 input input-bordered input-sm w-full rounded-lg border-base-300 focus:border-primary font-sans"
                />
              </div>
              <div class="sm:col-span-1">
                <dt class="text-2xs font-mono text-slate-500 uppercase tracking-widest">
                  Last Name
                </dt>
                <dd v-if="!editing" class="mt-1 text-sm text-slate-200">{{ user?.lastname }}</dd>
                <input
                  v-else
                  v-model="form.lastname"
                  type="text"
                  class="mt-1 input input-bordered input-sm w-full rounded-lg border-base-300 focus:border-primary font-sans"
                />
              </div>
              <div class="sm:col-span-1">
                <dt class="text-2xs font-mono text-slate-500 uppercase tracking-widest">Email</dt>
                <dd class="mt-1.5 text-sm text-slate-200 font-mono">{{ user?.email }}</dd>
              </div>
              <div class="sm:col-span-1">
                <dt class="text-2xs font-mono text-slate-500 uppercase tracking-widest">Phone</dt>
                <dd v-if="!editing" class="mt-1 text-sm text-slate-200 font-mono">
                  {{ user?.phone }}
                </dd>
                <input
                  v-else
                  v-model="form.phone"
                  type="text"
                  class="mt-1 input input-bordered input-sm w-full rounded-lg border-base-300 focus:border-primary font-mono text-xs"
                />
              </div>
              <div class="sm:col-span-2">
                <dt class="text-2xs font-mono text-slate-500 uppercase tracking-widest">Address</dt>
                <dd v-if="!editing" class="mt-1 text-sm text-slate-200">{{ user?.address }}</dd>
                <input
                  v-else
                  v-model="form.address"
                  type="text"
                  class="mt-1 input input-bordered input-sm w-full rounded-lg border-base-300 focus:border-primary font-sans"
                />
              </div>
              <div class="sm:col-span-1">
                <dt class="text-2xs font-mono text-slate-500 uppercase tracking-widest">Role</dt>
                <dd class="mt-1.5 text-sm text-slate-200 capitalize font-mono">{{ user?.role }}</dd>
              </div>
              <div class="sm:col-span-1">
                <dt class="text-2xs font-mono text-slate-500 uppercase tracking-widest">
                  Member Since
                </dt>
                <dd class="mt-1.5 text-sm text-slate-200 font-mono">
                  {{ formatDate(user?.created_at) }}
                </dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const user = computed(() => authStore.user)

const editing = ref(false)
const saving = ref(false)
const error = ref('')
const success = ref(false)
const form = ref({ firstname: '', lastname: '', phone: '', address: '' })

const userInitials = computed(() => {
  if (!user.value) return 'U'
  const first = user.value.firstname?.charAt(0) || ''
  const last = user.value.lastname?.charAt(0) || ''
  return (first + last).toUpperCase() || 'U'
})

const profilePictureUrl = computed(() => {
  if (!user.value) return null
  return (
    user.value.profile_picture ||
    `https://api.dicebear.com/9.x/notionists-neutral/svg?seed=${user.value.firstname}${user.value.lastname}`
  )
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const startEditing = () => {
  form.value = {
    firstname: user.value.firstname || '',
    lastname: user.value.lastname || '',
    phone: user.value.phone || '',
    address: user.value.address || '',
  }
  editing.value = true
  error.value = ''
  success.value = false
}

const cancelEditing = () => {
  editing.value = false
  error.value = ''
}

const saveProfile = async () => {
  saving.value = true
  error.value = ''
  success.value = false

  const result = await authStore.updateProfile(form.value)
  if (result.success) {
    success.value = true
    editing.value = false
  } else {
    error.value = result.error
  }
  saving.value = false
}
</script>

<style scoped>
/* Scoped styles */
</style>
