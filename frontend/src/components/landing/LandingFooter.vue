<template>
  <footer class="border-t border-base-content/10 bg-base-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-10">
        <div class="col-span-2">
          <div class="flex items-center gap-2.5 mb-5">
            <div
              class="w-9 h-9 rounded-xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-md shadow-primary/20"
            >
              <Zap class="w-5 h-5 text-white" :stroke-width="2.5" />
            </div>
            <span class="text-xl font-extrabold tracking-tight text-base-content"
              >City<span class="text-primary">Pulse</span></span
            >
          </div>
          <p class="text-sm text-base-content/40 leading-relaxed max-w-xs">
            Empowering municipal teams and neighborhoods with real-time civic analytics and verified
            issue resolution.
          </p>
        </div>
        <nav>
          <h4 class="font-bold text-xs uppercase tracking-widest text-base-content/50 mb-5">
            Product
          </h4>
          <ul class="space-y-3 text-sm text-base-content/40">
            <li>
              <a href="#reports" class="hover:text-primary transition-colors">Live Reports</a>
            </li>
            <li>
              <a href="#" class="hover:text-primary transition-colors">Interactive Maps</a>
            </li>
            <li>
              <a href="#" class="hover:text-primary transition-colors">AI Verification</a>
            </li>
          </ul>
        </nav>
        <nav>
          <h4 class="font-bold text-xs uppercase tracking-widest text-base-content/50 mb-5">
            Company
          </h4>
          <ul class="space-y-3 text-sm text-base-content/40">
            <li><a href="#" class="hover:text-primary transition-colors">About Us</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Blog</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Contact</a></li>
          </ul>
        </nav>
        <nav>
          <h4 class="font-bold text-xs uppercase tracking-widest text-base-content/50 mb-5">
            Legal
          </h4>
          <ul class="space-y-3 text-sm text-base-content/40">
            <li><a href="#" class="hover:text-primary transition-colors">Privacy</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Terms</a></li>
          </ul>
        </nav>
      </div>
      <div
        class="mt-14 pt-6 border-t border-base-content/10 flex flex-col sm:flex-row items-center justify-between gap-4"
      >
        <p class="text-xs text-base-content/30">
          &copy; {{ new Date().getFullYear() }} CityPulse. All rights reserved.
        </p>
        <div class="flex items-center gap-5">
          <a href="#" class="text-base-content/30 hover:text-primary transition-colors"
            ><Globe class="w-4 h-4" :stroke-width="2"
          /></a>
          <a href="#" class="text-base-content/30 hover:text-primary transition-colors"
            ><MessageCircle class="w-4 h-4" :stroke-width="2"
          /></a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { Zap, Globe, MessageCircle } from '@lucide/vue'
</script>
