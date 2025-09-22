<template>
  <div class="location-selector">
    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700 mb-2">
        Location *
      </label>

      <!-- Location Input Options -->
      <div class="flex flex-col sm:flex-row gap-3 mb-4">
        <button @click="useCurrentLocation" :disabled="gettingLocation"
          class="flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex-1 sm:flex-initial">
          <svg v-if="gettingLocation" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
            xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4">
            </circle>
            <path class="opacity-75" fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
            </path>
          </svg>
          <svg v-else class="-ml-1 mr-3 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z">
            </path>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z">
            </path>
          </svg>
          <span class="text-sm">{{ gettingLocation ? 'Getting Location...' : 'Use Current Location' }}</span>
        </button>

        <button @click="showMap = !showMap"
          class="flex items-center justify-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex-1 sm:flex-initial">
          <svg class="-ml-1 mr-3 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7">
            </path>
          </svg>
          <span class="text-sm">{{ showMap ? 'Hide Map' : 'Select on Map' }}</span>
        </button>
      </div>

      <!-- Address/Pincode Input -->
      <div class="mb-4">
        <label for="address" class="block text-sm font-medium text-gray-700 mb-1">
          Or enter address/pincode
        </label>
        <input id="address" v-model="address" type="text" placeholder="Enter address or pincode"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
          @input="onAddressChange" />
        <div v-if="addressSuggestions.length > 0"
          class="mt-2 bg-white border border-gray-300 rounded-lg shadow-lg max-h-40 overflow-y-auto">
          <div v-for="suggestion in addressSuggestions" :key="suggestion.place_id" @click="selectAddress(suggestion)"
            class="px-3 py-2 hover:bg-gray-100 cursor-pointer border-b border-gray-200 last:border-b-0">
            {{ suggestion.display_name }}
          </div>
        </div>
      </div>

      <!-- Map Container -->
      <div v-if="showMap" class="mb-4">
        <div class="h-64 sm:h-80 border border-gray-300 rounded-lg overflow-hidden">
          <div ref="mapContainer" class="h-full w-full"></div>
        </div>
        <p class="text-sm text-gray-600 mt-2">
          Click on the map to set your location, or drag the marker to adjust.
        </p>
      </div>

      <!-- Selected Location Display -->
      <div v-if="selectedLocation" class="bg-gray-50 p-3 rounded-lg">
        <h4 class="text-sm font-medium text-gray-700 mb-2">Selected Location:</h4>
        <p class="text-sm text-gray-600">
          <strong>Coordinates:</strong> {{ selectedLocation.lat.toFixed(6) }}, {{
            selectedLocation.lng.toFixed(6) }}
        </p>
        <p v-if="address" class="text-sm text-gray-600">
          <strong>Address:</strong> {{ address }}
        </p>
      </div>

      <!-- Error Messages -->
      <div v-if="locationError" class="mt-2 text-red-600 text-sm">
        {{ locationError }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted, watch, nextTick } from 'vue'
import L from 'leaflet'

// Props
const props = defineProps({
  modelValue: {
    type: Object,
    default: () => null
  }
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

// Geocoding function using Nominatim (OpenStreetMap)
const searchAddress = async (query) => {
  if (!query || query.length < 3) {
    addressSuggestions.value = []
    return
  }

  try {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=5&countrycodes=IN`
    )
    const results = await response.json()

    addressSuggestions.value = results.map(result => ({
      place_id: result.place_id,
      display_name: result.display_name,
      lat: parseFloat(result.lat),
      lon: parseFloat(result.lon)
    }))
  } catch (error) {
    console.error('Geocoding error:', error)
    addressSuggestions.value = []
  }
}

const selectAddress = (suggestion) => {
  address.value = suggestion.display_name
  selectedLocation.value = {
    lat: suggestion.lat,
    lng: suggestion.lon
  }
  addressSuggestions.value = []

  // Update map if visible
  if (map.value && marker.value) {
    marker.value.setLatLng([suggestion.lat, suggestion.lon])
    map.value.setView([suggestion.lat, suggestion.lon], 15)
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
        maximumAge: 300000
      })
    })

    const lat = position.coords.latitude
    const lng = position.coords.longitude

    selectedLocation.value = { lat, lng }

    // Try to get address from coordinates
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`
      )
      const result = await response.json()
      if (result && result.display_name) {
        address.value = result.display_name
      }
    } catch {
      console.log('Could not reverse geocode location')
    }        // Update map if visible
    if (map.value) {
      initializeMap()
    }

    emitLocation()
  } catch (error) {
    console.error('Geolocation error:', error)
    if (error.code === 1) {
      locationError.value = 'Location access denied. Please enable location permissions and try again.'
    } else if (error.code === 2) {
      locationError.value = 'Location unavailable. Please check your GPS settings and try again.'
    } else if (error.code === 3) {
      locationError.value = 'Location request timed out. Please try again.'
    } else {
      locationError.value = 'Unable to get your location. Please enter address manually or select on map.'
    }
  } finally {
    gettingLocation.value = false
  }
}

const initializeMap = () => {
  if (!mapContainer.value || map.value) return

  // Initialize map
  map.value = L.map(mapContainer.value).setView(
    selectedLocation.value ? [selectedLocation.value.lat, selectedLocation.value.lng] : [20.5937, 78.9629],
    selectedLocation.value ? 15 : 5
  )

  // Add OpenStreetMap tiles
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map.value)

  // Add marker if location is selected
  if (selectedLocation.value) {
    marker.value = L.marker([selectedLocation.value.lat, selectedLocation.value.lng], {
      draggable: true
    }).addTo(map.value)

    marker.value.on('dragend', (event) => {
      const position = event.target.getLatLng()
      selectedLocation.value = {
        lat: position.lat,
        lng: position.lng
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
      draggable: true
    }).addTo(map.value)

    marker.value.on('dragend', (event) => {
      const position = event.target.getLatLng()
      selectedLocation.value = {
        lat: position.lat,
        lng: position.lng
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
    const response = await fetch(
      `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`
    )
    const result = await response.json()
    if (result && result.display_name) {
      address.value = result.display_name
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
      address: address.value
    })
  } else {
    emit('update:modelValue', null)
  }
}

const onAddressChange = () => {
  // Debounce address search
  clearTimeout(window.addressSearchTimeout)
  window.addressSearchTimeout = setTimeout(() => {
    searchAddress(address.value)
  }, 300)
}

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    selectedLocation.value = {
      lat: newValue.latitude,
      lng: newValue.longitude
    }
    address.value = newValue.address || ''
  }
})

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
</script>

<style scoped>
/* Leaflet CSS overrides */
:deep(.leaflet-control-container) {
  font-family: inherit;
}

:deep(.leaflet-popup-content-wrapper) {
  font-family: inherit;
}
</style>
