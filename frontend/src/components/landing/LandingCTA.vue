<template>
  <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
    <div
      class="relative rounded-[2.5rem] overflow-hidden bg-gradient-to-br from-primary via-secondary to-accent p-14 sm:p-24 text-center noise border border-white/10 shadow-[0_0_80px_-20px_rgba(59,130,246,0.3)]"
    >
      <!-- Decorative elements -->
      <div
        class="absolute -top-32 -left-32 h-80 w-80 rounded-full bg-white/10 blur-3xl pointer-events-none"
      />
      <div
        class="absolute -bottom-32 -right-32 h-80 w-80 rounded-full bg-accent/20 blur-3xl pointer-events-none"
      />
      <div
        class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full bg-white/5 blur-[100px] pointer-events-none"
      />

      <div class="relative z-10">
        <h2 class="text-4xl sm:text-5xl lg:text-6xl font-black text-white tracking-tight">
          Make your city better
        </h2>
        <p class="mt-6 text-white/70 max-w-xl mx-auto text-lg sm:text-xl leading-relaxed">
          Join thousands of active residents making their neighborhoods cleaner, safer, and better
          through verified reporting.
        </p>
        <div class="mt-12 flex flex-col sm:flex-row gap-4 justify-center">
          <router-link
            to="/register"
            class="group relative inline-flex items-center gap-3 px-9 py-4 rounded-2xl bg-white text-black font-bold text-sm hover:bg-white/95 shadow-2xl shadow-black/20 hover:shadow-[0_20px_60px_-12px_rgba(255,255,255,0.2)] hover:-translate-y-1 active:translate-y-0 transition-all duration-300 overflow-hidden"
          >
            <span
              class="absolute inset-0 bg-gradient-to-r from-primary/10 via-secondary/10 to-accent/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
            />
            <Rocket class="w-5 h-5 text-primary relative z-10" :stroke-width="2.5" />
            <span class="relative z-10">Get Started Free</span>
          </router-link>
          <a
            href="#reports"
            class="inline-flex items-center gap-3 px-9 py-4 rounded-2xl border border-white/20 text-white font-bold text-sm hover:bg-white/10 hover:border-white/30 hover:-translate-y-1 active:translate-y-0 transition-all duration-300 backdrop-blur-sm"
          >
            <Play class="w-5 h-5" :stroke-width="2.5" />
            See it in action
          </a>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { Rocket, Play } from '@lucide/vue'
</script>
