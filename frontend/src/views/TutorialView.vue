<template>
  <div class="tutorial-view" v-if="tutorial">
    <div class="tutorial-layout">
      <div class="tutorial-sidebar card">
        <router-link to="/tutorials" class="back-link">&larr; All Tutorials</router-link>
        <h2>{{ tutorial.title }}</h2>
        <span :class="['badge', getCategoryClass()]">
          {{ getCategoryLabel() }}
        </span>
        <div class="tutorial-description" v-html="renderMarkdown(tutorial.description)"></div>
        <button class="btn-primary run-btn" @click="runTutorial" :disabled="loading">
          {{ loading ? 'Running...' : hasRun ? 'Run Again' : 'Run Visualization' }}
        </button>

        <!-- Inline playback controls for tutorial -->
        <div v-if="store.totalSteps > 0" class="playback-section">
          <div class="step-info" v-if="store.currentStep">
            <div class="step-counter mono">
              Step {{ store.currentStepIndex + 1 }} / {{ store.totalSteps }}
            </div>
            <p class="step-description">{{ store.currentStep.description }}</p>
          </div>

          <div class="playback-controls">
            <button class="btn-icon" @click="store.resetVisualization()" title="Reset">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 4v6h6"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>
            </button>
            <button class="btn-icon" @click="store.stepBackward()" :disabled="store.currentStepIndex <= 0">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="11 17 6 12 11 7"/><polyline points="18 17 13 12 18 7"/></svg>
            </button>
            <button class="btn-icon play-btn" @click="togglePlay">
              <svg v-if="!store.isPlaying" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
              <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
            </button>
            <button class="btn-icon" @click="store.stepForward()" :disabled="store.currentStepIndex >= store.totalSteps - 1">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="13 17 18 12 13 7"/><polyline points="6 17 11 12 6 7"/></svg>
            </button>
            <button class="btn-icon" @click="goToEnd">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 4 15 12 5 20 5 4"/><line x1="19" y1="5" x2="19" y2="19"/></svg>
            </button>
          </div>

          <div class="speed-control">
            <label>Speed</label>
            <input type="range" min="100" max="2000" step="100" v-model.number="store.playbackSpeed" />
            <span class="mono">{{ store.playbackSpeed }}ms</span>
          </div>

          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: ((store.currentStepIndex + 1) / store.totalSteps * 100) + '%' }"
            ></div>
          </div>

          <!-- Distance table for shortest path algos -->
          <div v-if="store.currentStep?.distances" class="data-table">
            <h4>Distance Table</h4>
            <table>
              <thead>
                <tr>
                  <th>Node</th>
                  <th>Dist</th>
                  <th>Via</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="node in store.nodes" :key="node.id" :class="{ highlighted: store.currentStep?.highlight_nodes?.includes(node.id) }">
                  <td class="mono">{{ node.label || node.id }}</td>
                  <td class="mono">{{ store.currentStep.distances[node.id] ?? '?' }}</td>
                  <td class="mono">{{ store.currentStep.predecessors?.[node.id] || '-' }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Queue/Stack display -->
          <div v-if="store.currentStep?.queue_or_stack" class="data-display">
            <h4>{{ tutorial.algorithm === 'bfs' ? 'Queue' : 'Stack' }}</h4>
            <div class="queue-display mono">
              [{{ store.currentStep.queue_or_stack.join(', ') }}]
            </div>
          </div>
        </div>

        <button class="btn-secondary" style="width: 100%; margin-top: 0.75rem" @click="openInSandbox">
          Open in Sandbox
        </button>
      </div>

      <div class="graph-area">
        <GraphCanvas :readonly="true" />
      </div>
    </div>
  </div>
  <div v-else class="loading container">Loading tutorial...</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useGraphStore } from '../stores/graph'
import { getTutorials, getPresetGraphs, runAlgorithm } from '../api'
import GraphCanvas from '../components/GraphCanvas.vue'

const props = defineProps({ id: String })
const router = useRouter()
const store = useGraphStore()

const tutorial = ref(null)
const loading = ref(false)
const hasRun = ref(false)
let playInterval = null

function getCategoryClass() {
  const algo = tutorial.value?.algorithm
  if (algo === 'bfs' || algo === 'dfs') return 'badge-traversal'
  return 'badge-shortest-path'
}

function getCategoryLabel() {
  const algo = tutorial.value?.algorithm
  if (algo === 'bfs' || algo === 'dfs') return 'Traversal'
  return 'Shortest Path'
}

function renderMarkdown(text) {
  if (!text) return ''
  return text
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>')
    .replace(/^/, '<p>')
    .replace(/$/, '</p>')
}

async function runTutorial() {
  if (!tutorial.value) return
  loading.value = true
  store.clearVisualization()

  try {
    const res = await runAlgorithm(
      store.getGraphData(),
      tutorial.value.algorithm,
      tutorial.value.start_node,
      tutorial.value.end_node || null,
      tutorial.value.directed,
    )
    store.setAlgorithmSteps(res.steps)
    store.goToStep(0)
    hasRun.value = true
  } catch (e) {
    console.error('Failed to run tutorial:', e)
  } finally {
    loading.value = false
  }
}

function togglePlay() {
  if (store.isPlaying) {
    stopPlay()
  } else {
    startPlay()
  }
}

function startPlay() {
  store.isPlaying = true
  if (store.currentStepIndex < 0) store.goToStep(0)
  playInterval = setInterval(() => {
    if (store.currentStepIndex < store.totalSteps - 1) {
      store.stepForward()
    } else {
      stopPlay()
    }
  }, store.playbackSpeed)
}

function stopPlay() {
  store.isPlaying = false
  if (playInterval) {
    clearInterval(playInterval)
    playInterval = null
  }
}

function goToEnd() {
  stopPlay()
  store.goToStep(store.totalSteps - 1)
}

watch(() => store.playbackSpeed, () => {
  if (store.isPlaying) {
    stopPlay()
    startPlay()
  }
})

function openInSandbox() {
  router.push('/sandbox')
}

onMounted(async () => {
  try {
    const [tutorials, presets] = await Promise.all([
      getTutorials(),
      getPresetGraphs(),
    ])
    tutorial.value = tutorials.find(t => t.id === props.id)
    if (tutorial.value) {
      const preset = presets.find(p => p.id === tutorial.value.preset_id)
      if (preset) {
        store.loadGraphData(preset.graph_data, preset.name)
        if (tutorial.value.directed !== undefined) {
          store.directed = tutorial.value.directed
        }
      }
    }
  } catch (e) {
    console.error('Failed to load tutorial:', e)
  }
})

onUnmounted(() => {
  stopPlay()
})
</script>

<style scoped>
.tutorial-view {
  height: calc(100vh - 53px);
  overflow: hidden;
}

.tutorial-layout {
  display: grid;
  grid-template-columns: 380px 1fr;
  height: 100%;
}

.tutorial-sidebar {
  border-radius: 0;
  border-top: none;
  border-left: none;
  border-right: 1px solid var(--border);
  overflow-y: auto;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.back-link {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.back-link:hover {
  color: var(--accent);
}

.tutorial-sidebar h2 {
  font-size: 1.25rem;
  font-weight: 700;
}

.tutorial-description {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.6;
}

.tutorial-description :deep(strong) {
  color: var(--text-primary);
  font-weight: 600;
}

.tutorial-description :deep(p) {
  margin-bottom: 0.5rem;
}

.run-btn {
  width: 100%;
  padding: 0.6rem;
  font-weight: 600;
}

.run-btn:disabled {
  opacity: 0.5;
}

.graph-area {
  background: var(--bg-primary);
}

.loading {
  padding: 3rem;
  text-align: center;
  color: var(--text-muted);
}

/* Playback styles (same as AlgorithmPanel) */
.playback-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  border-top: 1px solid var(--border);
  padding-top: 0.75rem;
}

.step-info {
  background: var(--bg-primary);
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
}

.step-counter {
  font-size: 0.7rem;
  color: var(--text-muted);
  margin-bottom: 0.25rem;
}

.step-description {
  font-size: 0.85rem;
  color: var(--text-primary);
  line-height: 1.4;
}

.playback-controls {
  display: flex;
  gap: 4px;
  justify-content: center;
  align-items: center;
}

.play-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--accent);
  color: white;
  border-color: var(--accent);
}

.play-btn:hover {
  background: var(--accent-hover);
}

.speed-control {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
}

.speed-control label {
  color: var(--text-secondary);
  min-width: 40px;
}

.speed-control input[type="range"] {
  flex: 1;
  padding: 0;
  border: none;
  background: transparent;
  accent-color: var(--accent);
}

.speed-control .mono {
  font-size: 0.7rem;
  color: var(--text-muted);
  min-width: 48px;
  text-align: right;
}

.progress-bar {
  height: 3px;
  background: var(--bg-tertiary);
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--accent);
  transition: width 0.2s ease;
}

.data-table h4, .data-display h4 {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-bottom: 0.35rem;
}

.data-table table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.75rem;
}

.data-table th {
  text-align: left;
  padding: 0.25rem 0.5rem;
  color: var(--text-muted);
  font-weight: 500;
  border-bottom: 1px solid var(--border);
}

.data-table td {
  padding: 0.2rem 0.5rem;
  color: var(--text-primary);
  border-bottom: 1px solid var(--bg-tertiary);
}

.data-table tr.highlighted td {
  color: #22c55e;
  font-weight: 600;
}

.queue-display {
  font-size: 0.8rem;
  padding: 0.35rem 0.5rem;
  background: var(--bg-primary);
  border-radius: 4px;
  color: #818cf8;
}

.playback-controls button:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .tutorial-layout {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr;
  }

  .tutorial-view {
    height: auto;
    overflow: auto;
  }

  .graph-area {
    min-height: 400px;
  }
}
</style>
