<template>
  <div class="algorithm-panel">
    <h3>Algorithm</h3>

    <div class="form-group">
      <label>Algorithm</label>
      <select v-model="selectedAlgorithm">
        <option value="">-- Select --</option>
        <option v-for="algo in algorithms" :key="algo.id" :value="algo.id">
          {{ algo.name }}
        </option>
      </select>
    </div>

    <div v-if="selectedAlgoInfo" class="algo-description">
      <span :class="['badge', selectedAlgoInfo.category === 'traversal' ? 'badge-traversal' : 'badge-shortest-path']">
        {{ selectedAlgoInfo.category === 'traversal' ? 'Traversal' : 'Shortest Path' }}
      </span>
      <p>{{ selectedAlgoInfo.description }}</p>
    </div>

    <div class="form-group">
      <label>Start Node</label>
      <select v-model="startNode">
        <option value="">-- Select --</option>
        <option v-for="node in store.nodes" :key="node.id" :value="node.id">
          {{ node.label || node.id }}
        </option>
      </select>
    </div>

    <div class="form-group">
      <label>End Node (optional)</label>
      <select v-model="endNode">
        <option value="">None</option>
        <option v-for="node in store.nodes" :key="node.id" :value="node.id">
          {{ node.label || node.id }}
        </option>
      </select>
    </div>

    <div class="form-group checkbox-group">
      <label>
        <input type="checkbox" v-model="store.directed" />
        Directed graph
      </label>
    </div>

    <button class="btn-primary run-btn" @click="runAlgo" :disabled="!canRun || loading">
      {{ loading ? 'Running...' : 'Run Algorithm' }}
    </button>

    <!-- Playback controls -->
    <div v-if="store.totalSteps > 0" class="playback-section">
      <h3>Playback</h3>
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
        <button class="btn-icon" @click="store.stepBackward()" :disabled="store.currentStepIndex <= 0" title="Step back">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="11 17 6 12 11 7"/><polyline points="18 17 13 12 18 7"/></svg>
        </button>
        <button class="btn-icon play-btn" @click="togglePlay" :title="store.isPlaying ? 'Pause' : 'Play'">
          <svg v-if="!store.isPlaying" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
          <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
        </button>
        <button class="btn-icon" @click="store.stepForward()" :disabled="store.currentStepIndex >= store.totalSteps - 1" title="Step forward">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="13 17 18 12 13 7"/><polyline points="6 17 11 12 6 7"/></svg>
        </button>
        <button class="btn-icon" @click="goToEnd" title="Go to end">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 4 15 12 5 20 5 4"/><line x1="19" y1="5" x2="19" y2="19"/></svg>
        </button>
      </div>

      <div class="speed-control">
        <label>Speed</label>
        <input type="range" min="100" max="2000" step="100" v-model.number="store.playbackSpeed" />
        <span class="mono">{{ store.playbackSpeed }}ms</span>
      </div>

      <!-- Progress bar -->
      <div class="progress-bar">
        <div
          class="progress-fill"
          :style="{ width: ((store.currentStepIndex + 1) / store.totalSteps * 100) + '%' }"
        ></div>
      </div>

      <!-- Data table for shortest path algos -->
      <div v-if="store.currentStep?.distances" class="data-table">
        <h4>Distance Table</h4>
        <table>
          <thead>
            <tr>
              <th>Node</th>
              <th>Distance</th>
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

      <!-- Queue/Stack display for traversal algos -->
      <div v-if="store.currentStep?.queue_or_stack" class="data-display">
        <h4>{{ selectedAlgorithm === 'bfs' ? 'Queue' : 'Stack' }}</h4>
        <div class="queue-display mono">
          [{{ store.currentStep.queue_or_stack.join(', ') }}]
        </div>
      </div>
    </div>

    <div v-if="result" class="result-section">
      <h4>Result</h4>
      <div class="result-content">
        <div v-if="result.path">
          <span class="result-label">Path:</span>
          <span class="mono">{{ result.path.join(' → ') }}</span>
        </div>
        <div v-if="result.distance !== undefined">
          <span class="result-label">Distance:</span>
          <span class="mono">{{ result.distance }}</span>
        </div>
        <div v-if="result.visited_count !== undefined">
          <span class="result-label">Nodes visited:</span>
          <span class="mono">{{ result.visited_count }}</span>
        </div>
        <div v-if="result.negative_cycle">
          <span class="result-label warning">Negative cycle detected!</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from 'vue'
import { useGraphStore } from '../stores/graph'
import { runAlgorithm, listAlgorithms } from '../api'

const store = useGraphStore()

const algorithms = ref([])
const selectedAlgorithm = ref('')
const startNode = ref('')
const endNode = ref('')
const loading = ref(false)
const result = ref(null)
let playInterval = null

const selectedAlgoInfo = computed(() =>
  algorithms.value.find(a => a.id === selectedAlgorithm.value)
)

const canRun = computed(() =>
  selectedAlgorithm.value && startNode.value && store.nodes.length > 0
)

async function loadAlgorithms() {
  try {
    algorithms.value = await listAlgorithms()
  } catch (e) {
    console.error('Failed to load algorithms:', e)
  }
}

async function runAlgo() {
  if (!canRun.value) return
  loading.value = true
  result.value = null
  store.clearVisualization()

  try {
    const res = await runAlgorithm(
      store.getGraphData(),
      selectedAlgorithm.value,
      startNode.value,
      endNode.value || null,
      store.directed,
    )
    store.setAlgorithmSteps(res.steps)
    result.value = res.result
    // Auto-start at step 0
    store.goToStep(0)
  } catch (e) {
    console.error('Algorithm error:', e)
    alert(e.response?.data?.detail || 'Error running algorithm')
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
  if (store.currentStepIndex < 0) {
    store.goToStep(0)
  }
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

// Restart play timer when speed changes
watch(() => store.playbackSpeed, () => {
  if (store.isPlaying) {
    stopPlay()
    startPlay()
  }
})

onUnmounted(() => {
  stopPlay()
})

loadAlgorithms()

defineExpose({
  setAlgorithm(algoId, start, end, directed) {
    selectedAlgorithm.value = algoId
    startNode.value = start
    endNode.value = end || ''
    if (directed !== undefined) store.directed = directed
  },
  runAlgo,
})
</script>

<style scoped>
.algorithm-panel {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.algorithm-panel h3 {
  font-size: 0.95rem;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.form-group label {
  font-size: 0.8rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.85rem;
  color: var(--text-primary);
}

.algo-description {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.algo-description p {
  font-size: 0.8rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

.run-btn {
  width: 100%;
  padding: 0.6rem;
  font-weight: 600;
}

.run-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.playback-section {
  border-top: 1px solid var(--border);
  padding-top: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
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

.data-table {
  margin-top: 0.25rem;
}

.data-table h4 {
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
  color: var(--success);
  font-weight: 600;
}

.data-display {
  margin-top: 0.25rem;
}

.data-display h4 {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-bottom: 0.25rem;
}

.queue-display {
  font-size: 0.8rem;
  padding: 0.35rem 0.5rem;
  background: var(--bg-primary);
  border-radius: 4px;
  color: var(--accent-hover);
}

.result-section {
  border-top: 1px solid var(--border);
  padding-top: 0.5rem;
}

.result-section h4 {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-bottom: 0.35rem;
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.85rem;
}

.result-label {
  color: var(--text-muted);
  margin-right: 0.5rem;
}

.result-label.warning {
  color: var(--warning);
  font-weight: 600;
}

.playback-controls button:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}
</style>
