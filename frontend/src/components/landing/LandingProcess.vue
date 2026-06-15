<template>
  <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 border-t border-base-300/20">
    <div class="text-center max-w-2xl mx-auto mb-16">
      <span
        class="inline-flex items-center gap-2 text-xs font-bold tracking-widest text-secondary uppercase bg-secondary/8 px-4 py-1.5 rounded-full mb-5 border border-secondary/10"
      >
        <span class="w-1.5 h-1.5 rounded-full bg-secondary" />
        Simple Process
      </span>
      <h2 class="text-3xl sm:text-4xl font-black tracking-tight text-base-content">How it works</h2>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
      <!-- Connecting line -->
      <div
        class="hidden md:block absolute top-12 left-[20%] right-[20%] h-px bg-gradient-to-r from-transparent via-base-300/50 to-transparent"
      />

      <div class="relative text-center group">
        <div
          class="w-24 h-24 rounded-3xl bg-base-200/60 glass-card mx-auto mb-6 flex items-center justify-center group-hover:scale-105 transition-transform duration-300 relative border border-base-content/5 hover:border-primary/20"
        >
          <span class="text-3xl font-black text-primary/20 font-mono">01</span>
          <div
            class="absolute -top-2 -right-2 w-8 h-8 rounded-xl bg-primary flex items-center justify-center shadow-lg shadow-primary/25 border border-primary/20"
          >
            <Camera class="w-4 h-4 text-white" :stroke-width="2.5" />
          </div>
        </div>
        <h3 class="font-bold text-lg mb-2 text-base-content">Snap & Report</h3>
        <p class="text-sm text-base-content/50 max-w-xs mx-auto">
          Capture a photo, add details, and let AI classify and route your issue automatically.
        </p>
      </div>

      <div class="relative text-center group">
        <div
          class="w-24 h-24 rounded-3xl bg-base-200/60 glass-card mx-auto mb-6 flex items-center justify-center group-hover:scale-105 transition-transform duration-300 relative border border-base-content/5 hover:border-secondary/20"
        >
          <span class="text-3xl font-black text-secondary/20 font-mono">02</span>
          <div
            class="absolute -top-2 -right-2 w-8 h-8 rounded-xl bg-secondary flex items-center justify-center shadow-lg shadow-secondary/25 border border-secondary/20"
          >
            <Brain class="w-4 h-4 text-white" :stroke-width="2.5" />
          </div>
        </div>
        <h3 class="font-bold text-lg mb-2 text-base-content">AI Processes</h3>
        <p class="text-sm text-white/50 max-w-xs mx-auto">
          The unified pipeline classifies, scores priority, detects duplicates, and assigns
          departments.
        </p>
      </div>

      <div class="relative text-center group">
        <div
          class="w-24 h-24 rounded-3xl bg-base-200/60 glass-card mx-auto mb-6 flex items-center justify-center group-hover:scale-105 transition-transform duration-300 relative border border-base-content/5 hover:border-success/20"
        >
          <span class="text-3xl font-black text-success/20 font-mono">03</span>
          <div
            class="absolute -top-2 -right-2 w-8 h-8 rounded-xl bg-success flex items-center justify-center shadow-lg shadow-success/25 border border-success/20"
          >
            <CircleCheckBig class="w-4 h-4 text-white" :stroke-width="2.5" />
          </div>
        </div>
        <h3 class="font-bold text-lg mb-2 text-base-content">Track Resolution</h3>
        <p class="text-sm text-white/50 max-w-xs mx-auto">
          Follow real-time status updates as your community issue gets resolved.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { Camera, Brain, CircleCheckBig } from '@lucide/vue'
</script>
