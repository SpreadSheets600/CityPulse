<template>
  <div v-if="ai" class="relative overflow-hidden border-t border-base-300 p-6 md:p-8 bg-base-200/30 backdrop-blur-md rounded-b-3xl">
    <!-- Subtle background radial glow -->
    <div class="absolute -top-24 -right-24 w-80 h-80 bg-primary/5 rounded-full blur-3xl pointer-events-none" />

    <!-- AI Header with pulsing status indicator -->
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-sm font-bold font-mono uppercase tracking-wider text-base-content/70 flex items-center gap-2">
        <div class="p-1.5 bg-primary/10 rounded-lg text-primary">
          <Sparkles class="w-4 h-4" />
        </div>
        AI Decision Insights
      </h3>
      <div class="flex items-center gap-2 px-3 py-1 bg-emerald-500/10 border border-emerald-500/20 rounded-full text-2xs font-mono font-bold text-emerald-400">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
        AUTOMATION ON
      </div>
    </div>

    <!-- Bento Grid for AI Metrics -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- Card 1: Classification -->
      <div v-if="ai.classification" class="bg-base-100/50 hover:bg-base-100/80 border border-base-content/5 hover:border-primary/20 rounded-2xl p-5 transition-all duration-300 hover:shadow-md flex flex-col justify-between group">
        <div>
          <div class="flex items-center justify-between mb-3.5">
            <div class="flex items-center gap-2">
              <div class="p-1 bg-purple-500/10 rounded-md text-purple-400">
                <Tag class="w-3.5 h-3.5" />
              </div>
              <span class="text-2xs font-mono text-base-content/40 uppercase tracking-widest font-semibold">Classification</span>
            </div>
            <span class="text-3xs uppercase font-mono font-extrabold tracking-widest px-1.5 py-0.5 rounded-md bg-base-300/80 text-base-content/50 border border-base-content/5">
              Source: {{ ai.classification.source }}
            </span>
          </div>
          <p class="text-sm font-extrabold text-base-content group-hover:text-primary transition-colors duration-200">{{ ai.classification.category }}</p>
          <p class="text-xs text-base-content/60 mt-1.5 leading-relaxed">{{ ai.classification.reasoning }}</p>
        </div>
        <div class="mt-4 pt-4 border-t border-base-content/5">
          <div class="flex justify-between text-2xs font-mono text-base-content/40 mb-1.5 font-bold">
            <span>Confidence Index</span>
            <span class="text-primary">{{ Math.round(ai.classification.confidence * 100) }}%</span>
          </div>
          <div class="w-full bg-base-300 rounded-full h-1.5 overflow-hidden">
            <div class="bg-gradient-to-r from-violet-500 to-indigo-500 h-1.5 rounded-full transition-all duration-500" :style="{ width: Math.round(ai.classification.confidence * 100) + '%' }" />
          </div>
        </div>
      </div>

      <!-- Card 2: Priority Assessment -->
      <div v-if="ai.priority" class="bg-base-100/50 hover:bg-base-100/80 border border-base-content/5 hover:border-primary/20 rounded-2xl p-5 transition-all duration-300 hover:shadow-md flex flex-col justify-between group">
        <div>
          <div class="flex items-center gap-2 mb-3.5">
            <div class="p-1 bg-orange-500/10 rounded-md text-orange-400">
              <ShieldAlert class="w-3.5 h-3.5" />
            </div>
            <span class="text-2xs font-mono text-base-content/40 uppercase tracking-widest font-semibold">Priority Index</span>
          </div>
          <div class="flex items-center gap-2.5 mb-2">
            <span :class="priorityBadgeClass" class="px-2 py-0.5 text-2xs font-extrabold uppercase tracking-wider rounded-md border">
              {{ ai.priority.level }}
            </span>
            <span class="text-xs font-mono font-bold text-base-content/60 bg-base-200/60 px-1.5 py-0.5 rounded-md border border-base-content/5">
              Score: {{ ai.priority.score }}/100
            </span>
          </div>
          <p class="text-xs text-base-content/60 leading-relaxed">{{ ai.priority.reasoning }}</p>
        </div>
        <!-- Progress representation of score -->
        <div class="mt-4 pt-4 border-t border-base-content/5">
          <div class="w-full bg-base-300 rounded-full h-1.5 overflow-hidden">
            <div class="h-1.5 rounded-full transition-all duration-500" :class="priorityColorClass" :style="{ width: ai.priority.score + '%' }" />
          </div>
        </div>
      </div>

      <!-- Card 3: Visual Consensus -->
      <div v-if="ai.verification && ai.verification.status !== 'skipped'" class="bg-base-100/50 hover:bg-base-100/80 border border-base-content/5 hover:border-primary/20 rounded-2xl p-5 transition-all duration-300 hover:shadow-md flex flex-col justify-between group">
        <div>
          <div class="flex items-center gap-2 mb-3.5">
            <div class="p-1 bg-emerald-500/10 rounded-md text-emerald-400">
              <FileImage class="w-3.5 h-3.5" />
            </div>
            <span class="text-2xs font-mono text-base-content/40 uppercase tracking-widest font-semibold">Visual Verification</span>
          </div>
          <div class="flex items-center gap-2 mb-2">
            <span :class="verificationBadgeClass" class="px-2 py-0.5 text-2xs font-extrabold uppercase tracking-wider rounded-md border flex items-center gap-1">
              <CheckCircle2 v-if="ai.verification.status === 'verified'" class="w-3 h-3" />
              <XCircle v-else class="w-3 h-3" />
              {{ ai.verification.status }}
            </span>
            <span v-if="ai.verification.confidence" class="text-xs font-mono font-bold text-base-content/60 bg-base-200/60 px-1.5 py-0.5 rounded-md border border-base-content/5">
              Consensus: {{ Math.round(ai.verification.confidence * 100) }}%
            </span>
          </div>
          <p class="text-xs text-base-content/60 leading-relaxed">{{ ai.verification.reasoning }}</p>
        </div>
        <!-- Visual graph accent line -->
        <div class="mt-4 pt-4 border-t border-base-content/5">
          <div class="w-full bg-base-300 rounded-full h-1.5 overflow-hidden">
            <div class="bg-emerald-500 h-1.5 rounded-full transition-all duration-500" :style="{ width: (ai.verification.confidence ? Math.round(ai.verification.confidence * 100) : 100) + '%' }" />
          </div>
        </div>
      </div>

      <!-- Card 4: Router Workflow -->
      <div v-if="ai.department && ai.department.auto_assigned" class="bg-base-100/50 hover:bg-base-100/80 border border-base-content/5 hover:border-primary/20 rounded-2xl p-5 transition-all duration-300 hover:shadow-md flex flex-col justify-between group">
        <div>
          <div class="flex items-center gap-2 mb-3.5">
            <div class="p-1 bg-pink-500/10 rounded-md text-pink-400">
              <Building2 class="w-3.5 h-3.5" />
            </div>
            <span class="text-2xs font-mono text-base-content/40 uppercase tracking-widest font-semibold">Router Workflow</span>
          </div>
          <!-- Visual Automation Routing Path -->
          <div class="flex items-center gap-1.5 bg-base-200/50 border border-base-content/5 p-2 rounded-xl text-3xs font-mono text-base-content/40 mb-3">
            <span>Report Received</span>
            <ArrowRight class="w-2.5 h-2.5 text-base-content/30" />
            <span class="text-primary font-bold">AI Parser</span>
            <ArrowRight class="w-2.5 h-2.5 text-base-content/30" />
            <span class="text-pink-400 font-bold">Routed</span>
          </div>
          <p class="text-sm font-extrabold text-base-content group-hover:text-primary transition-colors duration-200">{{ ai.department.department_name }}</p>
          <p class="text-xs text-base-content/50 mt-1 leading-relaxed">Incident matched successfully and auto-routed to department queue.</p>
        </div>
      </div>
    </div>

    <!-- Duplicate Warnings -->
    <div v-if="ai.duplicates && ai.duplicates.length > 0" class="mt-5 bg-warning/5 border border-warning/15 rounded-2xl p-5 flex gap-3.5 items-start">
      <div class="p-1.5 bg-warning/10 rounded-lg text-warning shrink-0 mt-0.5">
        <AlertTriangle class="w-4 h-4 animate-bounce" />
      </div>
      <div class="min-w-0 flex-1">
        <p class="text-xs font-mono font-extrabold text-warning uppercase tracking-wider mb-2">
          Collision warning: {{ ai.duplicates.length }} Potential Duplicate{{ ai.duplicates.length > 1 ? 's' : '' }} Found
        </p>
        <div class="space-y-2 border-t border-warning/10 pt-2.5">
          <div v-for="dup in ai.duplicates" :key="dup.id" class="flex items-center justify-between text-xs gap-3">
            <span class="text-base-content/75 truncate font-medium hover:text-warning cursor-pointer transition-colors">{{ dup.title }}</span>
            <div class="flex items-center gap-2 shrink-0">
              <span class="font-mono text-3xs text-base-content/35 font-bold uppercase">Similarity</span>
              <span class="font-mono font-bold bg-warning/10 text-warning px-1.5 py-0.5 rounded-md border border-warning/15">{{ Math.round(dup.similarity * 100) }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  Sparkles,
  Tag,
  ShieldAlert,
  FileImage,
  Building2,
  CheckCircle2,
  XCircle,
  ArrowRight,
  AlertTriangle
} from '@lucide/vue'

const props = defineProps({
  ai: {
    type: Object,
    default: null,
  },
})

const priorityBadgeClass = computed(() => {
  const level = props.ai?.priority?.level
  return {
    critical: 'bg-red-500/10 text-red-400 border-red-500/25 shadow-[0_0_10px_rgba(239,68,68,0.05)]',
    high: 'bg-orange-500/10 text-orange-400 border-orange-500/25',
    medium: 'bg-blue-500/10 text-blue-400 border-blue-500/25',
    low: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/25',
  }[level] || 'bg-slate-500/10 text-base-content/50 border-slate-500/20'
})

const priorityColorClass = computed(() => {
  const level = props.ai?.priority?.level
  return {
    critical: 'bg-red-500',
    high: 'bg-orange-500',
    medium: 'bg-blue-500',
    low: 'bg-emerald-500',
  }[level] || 'bg-slate-500'
})

const verificationBadgeClass = computed(() => {
  const status = props.ai?.verification?.status
  return {
    verified: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/25 shadow-[0_0_10px_rgba(16,185,129,0.05)]',
    rejected: 'bg-red-500/10 text-red-400 border-red-500/25',
    pending: 'bg-orange-500/10 text-orange-400 border-orange-500/25',
  }[status] || 'bg-slate-500/10 text-base-content/50 border-slate-500/20'
})
</script>
