<template>
  <div class="location-selector font-sans text-base-content">
    <div class="mb-4">
      <label class="label"
        ><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider"
          >Report Location *</span
        ></label
      >

      <!-- Location Input Options -->
      <div class="flex flex-col sm:flex-row gap-3 mb-4">
        <button
          type="button"
          @click="useCurrentLocation"
          :disabled="gettingLocation"
          class="btn btn-primary rounded-xl flex items-center justify-center gap-2 cursor-pointer flex-1 sm:flex-initial text-sm py-2"
        >
          <svg
            v-if="gettingLocation"
            class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          <svg
            v-else
            class="-ml-1 mr-2 h-4 w-4"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
            ></path>
            <circle cx="12" cy="11" r="3" />
          </svg>
          <span>{{ gettingLocation ? 'GETTING LOCATION...' : 'USE CURRENT GPS' }}</span>
        </button>

        <button
          type="button"
          @click="showMap = !showMap"
          class="btn btn-accent rounded-xl flex items-center justify-center gap-2 cursor-pointer flex-1 sm:flex-initial text-sm py-2"
        >
          <svg
            class="-ml-1 mr-2 h-4 w-4"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"
            ></path>
          </svg>
          <span>{{ showMap ? 'HIDE MAP' : 'SELECT ON MAP' }}</span>
        </button>
      </div>

      <!-- Address/Pincode Input -->
      <div class="mb-4 relative">
        <label for="address" class="label">
          <span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider"
            >Or search address / landmark</span
          >
        </label>
        <input
          id="address"
          v-model="address"
          type="text"
          placeholder="Enter address or pincode"
          class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary focus:ring-1 focus:ring-primary transition-all font-sans text-sm"
          @input="onAddressChange"
        />

        <div
          v-if="addressSuggestions.length > 0"
          class="absolute left-0 right-0 mt-2 bg-base-200 border border-base-300 rounded-2xl shadow-2xl max-h-48 overflow-y-auto z-[200]"
        >
          <div
            v-for="suggestion in addressSuggestions"
            :key="suggestion.place_id"
            @click="selectAddress(suggestion)"
            class="px-4 py-3 hover:bg-base-300 cursor-pointer border-b border-base-300 last:border-b-0 text-slate-200 text-xs font-mono"
          >
            {{ suggestion.display_name }}
          </div>
        </div>
      </div>

      <!-- Map Container -->
      <div v-if="showMap" class="mb-4">
        <div class="h-64 sm:h-80 border border-base-300 rounded-2xl overflow-hidden shadow-inner">
          <div ref="mapContainer" class="h-full w-full"></div>
        </div>
        <p class="text-xs font-mono text-slate-400 mt-2">
          Click on map to position the flag marker, or drag it to refine.
        </p>
      </div>

      <!-- Selected Location Display -->
      <div v-if="selectedLocation" class="bg-base-300/30 border border-base-300/80 p-4 rounded-2xl">
        <h4 class="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider mb-2">
          Selected Location Meta:
        </h4>
        <p class="text-xs font-mono text-slate-300">
          <strong>GPS Coordinates:</strong> {{ selectedLocation.lat.toFixed(6) }},
          {{ selectedLocation.lng.toFixed(6) }}
        </p>
        <p v-if="address" class="text-xs font-sans text-slate-300 mt-1 leading-relaxed">
          <strong>Physical Address:</strong> {{ address }}
        </p>
      </div>

      <!-- Error Messages -->
      <div
        v-if="locationError"
        class="mt-3 border border-error/20 bg-error/5 text-error text-center text-xs font-mono p-3 rounded-xl"
      >
        {{ locationError }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted, watch, nextTick } from 'vue'
import L from 'leaflet'
import axios from '../api/client'

// Props
const props = defineProps({
  modelValue: {
    type: Object,
    default: () => null,
  },
  autoLocate: {
    type: Boolean,
    default: false,
  },
})

// Emits
const emit = defineEmits(['update:modelValue'])

// Reactive data
const showMap = ref(false)
const gettingLocation = ref(false)
const selectedLocation = ref(null)
const address = ref('')
const addressSuggestions = ref([])
const locationError = ref('')
const map = ref(null)
const marker = ref(null)

// Refs
const mapContainer = ref(null)

// Geocoding function using backend API
const searchAddress = async (query) => {
  if (!query || query.length < 3) {
    addressSuggestions.value = []
    return
  }

  try {
    const response = await axios.get(`/api/geocode?q=${encodeURIComponent(query)}`)
    addressSuggestions.value = response.data.suggestions || []
  } catch (error) {
    console.error('Geocoding error:', error)
    addressSuggestions.value = []
  }
}

const selectAddress = (suggestion) => {
  address.value = suggestion.display_name
  selectedLocation.value = {
    lat: Number(suggestion.lat),
    lng: Number(suggestion.lon),
  }
  addressSuggestions.value = []

  // Update map if visible
  if (map.value && marker.value) {
    marker.value.setLatLng([Number(suggestion.lat), Number(suggestion.lon)])
    map.value.setView([Number(suggestion.lat), Number(suggestion.lon)], 15)
  }

  emitLocation()
}

const useCurrentLocation = async () => {
  if (!navigator.geolocation) {
    locationError.value = 'Geolocation is not supported by this browser.'
    return
  }

  gettingLocation.value = true
  locationError.value = ''

  try {
    const position = await new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(resolve, reject, {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 300000,
      })
    })

    const lat = position.coords.latitude
    const lng = position.coords.longitude

    selectedLocation.value = { lat, lng }

    // Try to get address from coordinates
    try {
      const response = await axios.get(`/api/reverse-geocode?lat=${lat}&lon=${lng}`)
      if (response.data.address) {
        address.value = response.data.address
      }
    } catch {
      console.log('Could not reverse geocode location')
    }
    // Update map if visible
    if (map.value) {
      initializeMap()
    }

    emitLocation()
  } catch (error) {
    console.error('Geolocation error:', error)
    if (error.code === 1) {
      locationError.value =
        'Location access denied. Please enable location permissions and try again.'
    } else if (error.code === 2) {
      locationError.value = 'Location unavailable. Please check your GPS settings and try again.'
    } else if (error.code === 3) {
      locationError.value = 'Location request timed out. Please try again.'
    } else {
      locationError.value =
        'Unable to get your location. Please enter address manually or select on map.'
    }
  } finally {
    gettingLocation.value = false
  }
}

const initializeMap = () => {
  if (!mapContainer.value || map.value) return

  // Initialize map
  map.value = L.map(mapContainer.value).setView(
    selectedLocation.value
      ? [selectedLocation.value.lat, selectedLocation.value.lng]
      : [20.5937, 78.9629],
    selectedLocation.value ? 15 : 5,
  )

  // Add CartoDB Dark Matter tile layer for dark styling
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    maxZoom: 19,
  }).addTo(map.value)

  // Add marker if location is selected
  if (selectedLocation.value) {
    marker.value = L.marker([selectedLocation.value.lat, selectedLocation.value.lng], {
      draggable: true,
    }).addTo(map.value)

    marker.value.on('dragend', (event) => {
      const position = event.target.getLatLng()
      selectedLocation.value = {
        lat: position.lat,
        lng: position.lng,
      }

      // Try to get address for new position
      reverseGeocode(position.lat, position.lng)
      emitLocation()
    })
  }

  // Handle map clicks
  map.value.on('click', (event) => {
    const { lat, lng } = event.latlng

    selectedLocation.value = { lat, lng }

    // Remove existing marker
    if (marker.value) {
      map.value.removeLayer(marker.value)
    }

    // Add new marker
    marker.value = L.marker([lat, lng], {
      draggable: true,
    }).addTo(map.value)

    marker.value.on('dragend', (event) => {
      const position = event.target.getLatLng()
      selectedLocation.value = {
        lat: position.lat,
        lng: position.lng,
      }
      reverseGeocode(position.lat, position.lng)
      emitLocation()
    })

    // Try to get address
    reverseGeocode(lat, lng)
    emitLocation()
  })
}

const reverseGeocode = async (lat, lng) => {
  try {
    const response = await axios.get(`/api/reverse-geocode?lat=${lat}&lon=${lng}`)
    if (response.data.address) {
      address.value = response.data.address
    }
  } catch {
    console.log('Could not reverse geocode location')
  }
}

const emitLocation = () => {
  if (selectedLocation.value) {
    emit('update:modelValue', {
      latitude: selectedLocation.value.lat,
      longitude: selectedLocation.value.lng,
      address: address.value,
    })
  } else {
    emit('update:modelValue', null)
  }
}

const onAddressChange = () => {
  clearTimeout(window.addressSearchTimeout)
  window.addressSearchTimeout = setTimeout(() => {
    searchAddress(address.value)
  }, 300)
}

// Watch for external changes
watch(
  () => props.modelValue,
  (newValue) => {
    if (newValue) {
      selectedLocation.value = {
        lat: newValue.latitude,
        lng: newValue.longitude,
      }
      address.value = newValue.address || ''
    }
  },
)

// Initialize map when showMap becomes true
watch(showMap, (newValue) => {
  if (newValue) {
    nextTick(() => {
      initializeMap()
    })
  } else {
    // Clean up map
    if (map.value) {
      map.value.remove()
      map.value = null
      marker.value = null
    }
  }
})

// Cleanup on unmount
onUnmounted(() => {
  if (map.value) {
    map.value.remove()
  }
})

// Auto-locate if requested
if (props.autoLocate) {
  useCurrentLocation()
}
</script>

<style scoped>
/* Leaflet CSS overrides */
:deep(.leaflet-control-container) {
  font-family: inherit;
}

:deep(.leaflet-popup-content-wrapper) {
  font-family: inherit;
}

/* Lower Leaflet z-index so app modals clearly overlay */
:deep(.leaflet-pane),
:deep(.leaflet-top),
:deep(.leaflet-bottom) {
  z-index: 100 !important;
}

/* Custom styles for leaflet dark map popup override */
:deep(.leaflet-popup-content-wrapper) {
  background-color: #0f172a !important;
  color: #f8fafc !important;
  border: 1px solid #334155;
  border-radius: 12px;
}

:deep(.leaflet-popup-tip) {
  background-color: #0f172a !important;
  border: 1px solid #334155;
}
</style>
