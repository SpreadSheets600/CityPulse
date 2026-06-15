<template>
  <section id="features" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32 relative">
    <!-- Background decoration -->
    <div
      class="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full bg-primary/3 blur-[200px] pointer-events-none"
    />

    <div class="text-center max-w-2xl mx-auto mb-20 relative">
      <span
        class="inline-flex items-center gap-2 text-xs font-bold tracking-widest text-primary uppercase bg-primary/8 px-4 py-1.5 rounded-full mb-5 border border-primary/10"
      >
        <Zap class="w-3 h-3" :stroke-width="2.5" />
        Why CityPulse
      </span>
      <h2 class="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight text-base-content">
        Built for civic action
      </h2>
      <p class="mt-5 text-base-content/50 text-lg max-w-lg mx-auto">
        Intelligent, fast, and transparent tools for issue resolution.
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-5 relative">
      <!-- Feature 1 — Large -->
      <div
        class="md:col-span-2 group relative rounded-[2rem] overflow-hidden bg-base-200/40 glass-card p-8 sm:p-10 hover-lift cursor-default border border-base-content/5 hover:border-primary/30 transition-all duration-300 hover:shadow-[0_0_35px_-5px_color-mix(in_srgb,var(--color-primary)_22%,transparent)]"
      >
        <div
          class="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-[80px] -translate-y-1/2 translate-x-1/2 group-hover:bg-primary/8 transition-colors duration-500"
        />
        <div class="relative z-10">
          <div
            class="w-14 h-14 rounded-2xl bg-gradient-to-br from-primary/15 to-primary/5 flex items-center justify-center mb-7 group-hover:scale-110 transition-transform duration-300 border border-primary/20"
          >
            <Zap class="w-7 h-7 text-primary" :stroke-width="2" />
          </div>
          <h3 class="text-2xl font-black tracking-tight text-base-content">Quick Reporting</h3>
          <p class="mt-3 text-base-content/50 leading-relaxed max-w-md text-[15px]">
            File detailed reports in under 30 seconds. Attach photos, record voice notes, or take
            videos with automated geo-tagging and AI classification.
          </p>
        </div>
      </div>

      <!-- Feature 2 -->
      <div
        class="group relative rounded-[2rem] overflow-hidden bg-base-200/40 glass-card p-8 hover-lift cursor-default border border-base-content/5 hover:border-secondary/30 transition-all duration-300 hover:shadow-[0_0_35px_-5px_color-mix(in_srgb,var(--color-secondary)_22%,transparent)]"
      >
        <div
          class="absolute bottom-0 left-0 w-40 h-40 bg-secondary/5 rounded-full blur-[60px] translate-y-1/2 -translate-x-1/2 group-hover:bg-secondary/8 transition-colors duration-500"
        />
        <div class="relative z-10">
          <div
            class="w-14 h-14 rounded-2xl bg-gradient-to-br from-secondary/15 to-secondary/5 flex items-center justify-center mb-7 group-hover:scale-110 transition-transform duration-300 border border-secondary/20"
          >
            <Sparkles class="w-7 h-7 text-secondary" :stroke-width="2" />
          </div>
          <h3 class="text-xl font-black tracking-tight text-base-content">AI Verification</h3>
          <p class="mt-3 text-base-content/50 text-sm leading-relaxed">
            Multi-modal computer vision verifies every report on upload to filter misleading
            submissions and identify duplicates.
          </p>
        </div>
      </div>

      <!-- Feature 3 -->
      <div
        class="group relative rounded-[2rem] overflow-hidden bg-base-200/40 glass-card p-8 hover-lift cursor-default border border-base-content/5 hover:border-accent/30 transition-all duration-300 hover:shadow-[0_0_35px_-5px_color-mix(in_srgb,var(--color-accent)_22%,transparent)]"
      >
        <div
          class="absolute top-0 left-0 w-40 h-40 bg-accent/5 rounded-full blur-[60px] -translate-y-1/2 -translate-x-1/2 group-hover:bg-accent/8 transition-colors duration-500"
        />
        <div class="relative z-10">
          <div
            class="w-14 h-14 rounded-2xl bg-gradient-to-br from-accent/15 to-accent/5 flex items-center justify-center mb-7 group-hover:scale-110 transition-transform duration-300 border border-accent/20"
          >
            <Map class="w-7 h-7 text-accent" :stroke-width="2" />
          </div>
          <h3 class="text-xl font-black tracking-tight text-base-content">Interactive Maps</h3>
          <p class="mt-3 text-base-content/50 text-sm leading-relaxed">
            Live maps show status updates and geofencing helps identify issue hotspots in your
            neighborhood.
          </p>
        </div>
      </div>

      <!-- Feature 4 — Large -->
      <div
        class="md:col-span-2 group relative rounded-[2rem] overflow-hidden bg-base-200/40 glass-card p-8 sm:p-10 hover-lift cursor-default border border-base-content/5 hover:border-success/30 transition-all duration-300 hover:shadow-[0_0_35px_-5px_color-mix(in_srgb,var(--color-success)_22%,transparent)]"
      >
        <div
          class="absolute bottom-0 right-0 w-64 h-64 bg-success/5 rounded-full blur-[80px] translate-y-1/2 translate-x-1/2 group-hover:bg-success/8 transition-colors duration-500"
        />
        <div class="relative z-10">
          <div
            class="w-14 h-14 rounded-2xl bg-gradient-to-br from-success/15 to-success/5 flex items-center justify-center mb-7 group-hover:scale-110 transition-transform duration-300 border border-success/20"
          >
            <Brain class="w-7 h-7 text-success" :stroke-width="2" />
          </div>
          <h3 class="text-2xl font-black tracking-tight text-base-content">Unified AI Pipeline</h3>
          <p class="mt-3 text-base-content/50 leading-relaxed max-w-md text-[15px]">
            Classification, priority scoring, duplicate detection, and department auto-routing — all
            powered by a single intelligent pipeline.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { Zap, Sparkles, Map, Brain } from '@lucide/vue'
</script>
