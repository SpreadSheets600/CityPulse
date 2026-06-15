<template>
  <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 border-t border-base-300/20">
    <div
      class="glass-card rounded-[2rem] p-6 sm:p-8 shadow-2xl border border-base-content/5 hover:border-accent/10 transition-all duration-500 shadow-[0_0_50px_-12px_rgba(236,72,153,0.08)]"
    >
      <div class="flex items-center justify-between mb-8 flex-wrap gap-4">
        <div class="flex items-center gap-3">
          <div class="relative">
            <div class="w-3 h-3 rounded-full bg-accent" />
            <div class="absolute inset-0 w-3 h-3 rounded-full bg-accent animate-ping" />
          </div>
          <h3 class="font-black text-lg uppercase tracking-wider text-base-content">
            Interactive City Map
          </h3>
        </div>
        <p class="text-xs text-base-content/40 max-w-md">
          Aggregated visualization of active local reports. Click markers to inspect specific
          problems.
        </p>
      </div>
      <div class="relative h-[420px] rounded-2xl overflow-hidden border border-base-content/10">
        <l-map
          :zoom="zoom"
          :center="center"
          :use-global-leaflet="false"
          style="height: 100%"
          @update:zoom="emit('update:zoom', $event)"
          @update:center="emit('update:center', $event)"
        >
          <l-tile-layer
            :url="mapTileUrl"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          />
          <l-marker
            v-for="issue in issues"
            :key="issue.id"
            :lat-lng="[issue.latitude, issue.longitude]"
          >
            <l-popup>
              <div class="w-52 p-1 text-base-content">
                <p class="font-black text-sm border-b border-base-300 pb-1.5 mb-1.5">
                  {{ issue.title }}
                </p>
                <p class="text-xs"><strong>Type:</strong> {{ issue.issue_type }}</p>
                <p class="text-xs truncate"><strong>Loc:</strong> {{ issue.address }}</p>
                <p class="text-xs">
                  <strong>Status:</strong>
                  <span class="capitalize font-bold text-primary">{{ issue.status }}</span>
                </p>
              </div>
            </l-popup>
          </l-marker>
        </l-map>
      </div>
    </div>
  </section>
</template>

<script setup>
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'

defineProps({
  zoom: {
    type: Number,
    required: true,
  },
  center: {
    type: Array,
    required: true,
  },
  issues: {
    type: Array,
    required: true,
  },
  mapTileUrl: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['update:zoom', 'update:center'])
</script>
