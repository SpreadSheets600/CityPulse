<template>
  <section class="relative min-h-screen flex items-center justify-center overflow-hidden isolate">
    <!-- Background image -->
    <div class="absolute inset-0 -z-30">
      <img
        :src="bgImage"
        alt=""
        class="w-full h-full object-cover scale-105"
        style="filter: brightness(0.42) contrast(1.05) saturate(1.15)"
      />
      <div class="absolute inset-0 bg-gradient-to-b from-black/40 via-black/20 to-base-100" />
    </div>

    <!-- Animated gradient orbs -->
    <div class="absolute inset-0 -z-20 overflow-hidden">
      <div
        class="absolute top-[15%] left-[10%] w-[500px] h-[500px] rounded-full bg-primary/20 blur-[130px] animate-float"
      />
      <div
        class="absolute bottom-[20%] right-[15%] w-[400px] h-[400px] rounded-full bg-secondary/15 blur-[110px] animate-float"
        style="animation-delay: -2s"
      />
      <div
        class="absolute top-[60%] left-[50%] w-[300px] h-[300px] rounded-full bg-accent/12 blur-[90px] animate-float"
        style="animation-delay: -4s"
      />
      <div
        class="absolute top-[10%] right-[30%] w-[250px] h-[250px] rounded-full bg-success/10 blur-[80px] animate-float"
        style="animation-delay: -1s"
      />
    </div>

    <!-- Dot grid pattern -->
    <div
      class="absolute inset-0 -z-10 opacity-[0.04]"
      :style="{
        backgroundImage:
          'linear-gradient(rgba(255, 255, 255, 0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.035) 1px, transparent 1px)',
        backgroundSize: '44px 44px',
        backgroundPosition: 'center',
      }"
    />

    <!-- Content -->
    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full py-20 text-center">
      <!-- Live badge -->
      <div
        class="inline-flex items-center gap-2.5 px-4 py-2 rounded-full bg-white/5 backdrop-blur-md border border-white/10 mb-10 animate-fade-up cursor-default"
      >
        <span class="relative flex h-2 w-2">
          <span
            class="animate-ping absolute inline-flex h-full w-full rounded-full bg-success opacity-75"
          ></span>
          <span class="relative inline-flex rounded-full h-2 w-2 bg-success"></span>
        </span>
        <span class="text-xs font-semibold text-white/75 tracking-widest uppercase"
          >Live civic intelligence</span
        >
      </div>

      <!-- Headline with Vue-based text slide-up animation -->
      <h1
        class="text-6xl sm:text-7xl lg:text-[5.5rem] xl:text-[6.5rem] font-black tracking-tighter leading-[0.9] text-white animate-fade-up"
        style="animation-delay: 80ms"
      >
        Your city's
        <br class="hidden sm:block" />
        <span
          class="relative inline-block text-gradient min-w-[200px] sm:min-w-[320px] transition-all duration-500 py-2"
          :style="{
            textShadow: '0 0 20px color-mix(in srgb, var(--color-primary) 50%, transparent)',
          }"
        >
          <Transition
            enter-active-class="transition duration-400 ease-out"
            enter-from-class="transform translate-y-3 opacity-0"
            enter-to-class="transform translate-y-0 opacity-100"
            leave-active-class="transition duration-400 ease-in"
            leave-from-class="transform translate-y-0 opacity-100"
            leave-to-class="transform -translate-y-3 opacity-0"
            mode="out-in"
          >
            <span :key="activeWord" class="inline-block">{{ activeWord }}</span>
          </Transition>
        </span>
        <br class="sm:hidden" />
        starts here.
      </h1>

      <!-- Subtitle -->
      <p
        class="mt-8 text-lg sm:text-xl text-white/60 max-w-xl mx-auto leading-relaxed font-normal animate-fade-up"
        style="animation-delay: 160ms"
      >
        Report local issues, coordinate responders, and track civic action in real time with
        AI-powered verification.
      </p>

      <!-- CTAs -->
      <div
        class="mt-12 flex flex-col sm:flex-row gap-4 justify-center animate-fade-up"
        style="animation-delay: 240ms"
      >
        <router-link
          to="/register"
          class="group relative inline-flex items-center gap-3 px-8 py-4 rounded-2xl bg-white text-black font-bold text-sm hover:bg-white/95 shadow-2xl shadow-black/20 hover:shadow-[0_20px_60px_-12px_rgba(255,255,255,0.15)] hover:-translate-y-1 active:translate-y-0 transition-all duration-300 overflow-hidden"
        >
          <span
            class="absolute inset-0 bg-gradient-to-r from-primary/10 via-secondary/10 to-accent/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
          />
          <ShieldCheck class="w-5 h-5 text-primary relative z-10" :stroke-width="2.5" />
          <span class="relative z-10">Report an Issue</span>
          <svg
            class="w-4 h-4 text-black/30 group-hover:translate-x-1 transition-transform relative z-10"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2.5"
              d="M9 5l7 7-7 7"
            />
          </svg>
        </router-link>
        <a
          href="#reports"
          class="inline-flex items-center gap-3 px-8 py-4 rounded-2xl border border-white/15 text-white font-bold text-sm hover:bg-white/8 hover:border-white/25 hover:-translate-y-1 active:translate-y-0 transition-all duration-300 backdrop-blur-sm"
        >
          <MapPin class="w-5 h-5" :stroke-width="2" />
          See Nearby Reports
        </a>
      </div>

      <!-- Stats with text glow effects -->
      <div
        class="mt-20 flex flex-wrap items-center justify-center gap-10 sm:gap-16 animate-fade-up"
        style="animation-delay: 320ms"
      >
        <div class="flex items-center gap-4">
          <div
            class="w-12 h-12 rounded-2xl bg-success/15 backdrop-blur-sm flex items-center justify-center border border-success/20 shadow-[0_0_15px_rgba(34,197,94,0.15)]"
          >
            <CircleCheckBig class="w-6 h-6 text-success animate-pulse-subtle" :stroke-width="2" />
          </div>
          <div class="text-left">
            <p
              class="text-3xl font-black text-white tracking-tight font-mono"
              :style="{
                textShadow: '0 0 20px color-mix(in srgb, var(--color-success) 50%, transparent)',
              }"
            >
              {{ totalIssuesText }}
            </p>
            <p class="text-xs text-white/40 font-semibold uppercase tracking-widest mt-0.5">
              Issues resolved
            </p>
          </div>
        </div>
        <div class="w-px h-12 bg-white/10 hidden sm:block" />
        <div class="flex items-center gap-4">
          <div
            class="w-12 h-12 rounded-2xl bg-primary/15 backdrop-blur-sm flex items-center justify-center border border-primary/20 shadow-[0_0_15px_rgba(59,130,246,0.15)]"
          >
            <Users
              class="w-6 h-6 text-primary animate-pulse-subtle"
              :stroke-width="2"
              style="animation-delay: 1.5s"
            />
          </div>
          <div class="text-left">
            <p
              class="text-3xl font-black text-white tracking-tight font-mono"
              :style="{
                textShadow: '0 0 20px color-mix(in srgb, var(--color-primary) 50%, transparent)',
              }"
            >
              {{ volunteersText }}
            </p>
            <p class="text-xs text-white/40 font-semibold uppercase tracking-widest mt-0.5">
              Active responders
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Scroll indicator -->
    <div
      class="absolute bottom-10 left-1/2 -translate-x-1/2 animate-fade-up"
      style="animation-delay: 500ms"
    >
      <a
        href="#features"
        class="flex flex-col items-center gap-3 text-white/30 hover:text-white/50 transition-colors group"
      >
        <span class="text-2xs font-bold uppercase tracking-[0.2em]">Explore</span>
        <div
          class="w-6 h-10 rounded-full border-2 border-white/20 flex justify-center pt-2 group-hover:border-white/40 transition-colors"
        >
          <div class="w-1.5 h-1.5 rounded-full bg-white/50 animate-bounce" />
        </div>
      </a>
    </div>
  </section>
</template>

<script setup>
import { ShieldCheck, MapPin, CircleCheckBig, Users } from '@lucide/vue'

defineProps({
  bgImage: {
    type: String,
    required: true,
  },
  activeWord: {
    type: String,
    required: true,
  },
  totalIssuesText: {
    type: String,
    required: true,
  },
  volunteersText: {
    type: String,
    required: true,
  },
})
</script>


