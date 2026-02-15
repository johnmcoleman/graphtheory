<template>
  <div class="sandbox">
    <div class="sandbox-layout">
      <div class="sidebar-left card">
        <div class="sidebar-header">
          <input
            v-model="store.graphName"
            class="graph-name-input"
            placeholder="Graph name..."
          />
        </div>

        <div class="sidebar-section">
          <h3>Graph</h3>
          <div class="graph-actions">
            <button class="btn-secondary btn-sm" @click="showPresets = !showPresets">
              Load Preset
            </button>
            <button class="btn-secondary btn-sm" @click="store.clearGraph()">
              Clear
            </button>
          </div>

          <div v-if="showPresets" class="presets-dropdown">
            <div
              v-for="preset in presets"
              :key="preset.id"
              class="preset-item"
              @click="loadPreset(preset)"
            >
              <strong>{{ preset.name }}</strong>
              <span>{{ preset.description }}</span>
            </div>
          </div>
        </div>

        <div class="sidebar-section">
          <div class="graph-info">
            <span>{{ store.nodes.length }} nodes</span>
            <span>{{ store.edges.length }} edges</span>
          </div>
        </div>

        <div class="sidebar-section edge-list">
          <h3>Edges</h3>
          <div v-if="store.edges.length === 0" class="empty-state">
            No edges yet
          </div>
          <div v-for="edge in store.edges" :key="edge.id" class="edge-item">
            <span class="mono edge-label">{{ edge.source }} → {{ edge.target }}</span>
            <input
              type="number"
              :value="edge.weight"
              @change="e => store.updateEdgeWeight(edge.id, parseFloat(e.target.value) || 1)"
              class="weight-input"
              step="any"
            />
          </div>
        </div>

        <div class="sidebar-section save-section">
          <button class="btn-primary" style="width: 100%" @click="saveCurrentGraph" :disabled="saving">
            {{ saving ? 'Saving...' : 'Save Graph' }}
          </button>
          <div v-if="store.shareToken" class="share-link">
            <label>Share link</label>
            <div class="share-url-row">
              <input :value="shareUrl" readonly class="share-url-input" />
              <button class="btn-icon btn-sm" @click="copyShareUrl" title="Copy">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="graph-area">
        <GraphCanvas ref="graphCanvas" />
      </div>

      <div class="sidebar-right card">
        <AlgorithmPanel ref="algoPanel" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useGraphStore } from '../stores/graph'
import { getPresetGraphs, saveGraph } from '../api'
import GraphCanvas from '../components/GraphCanvas.vue'
import AlgorithmPanel from '../components/AlgorithmPanel.vue'

const store = useGraphStore()
const graphCanvas = ref(null)
const algoPanel = ref(null)
const presets = ref([])
const showPresets = ref(false)
const saving = ref(false)

const shareUrl = computed(() => {
  if (!store.shareToken) return ''
  return `${window.location.origin}/share/${store.shareToken}`
})

async function loadPresets() {
  try {
    presets.value = await getPresetGraphs()
  } catch (e) {
    console.error('Failed to load presets:', e)
  }
}

function loadPreset(preset) {
  store.loadGraphData(preset.graph_data, preset.name)
  showPresets.value = false
}

async function saveCurrentGraph() {
  if (store.nodes.length === 0) return
  saving.value = true
  try {
    const res = await saveGraph({
      name: store.graphName,
      graph_data: store.getGraphData(),
    })
    store.graphId = res.id
    store.shareToken = res.share_token
  } catch (e) {
    console.error('Failed to save:', e)
    alert('Failed to save graph')
  } finally {
    saving.value = false
  }
}

function copyShareUrl() {
  navigator.clipboard.writeText(shareUrl.value)
}

onMounted(() => {
  loadPresets()
})
</script>

<style scoped>
.sandbox {
  height: calc(100vh - 53px);
  overflow: hidden;
}

.sandbox-layout {
  display: grid;
  grid-template-columns: 260px 1fr 300px;
  height: 100%;
}

.sidebar-left, .sidebar-right {
  border-radius: 0;
  border-top: none;
  overflow-y: auto;
  padding: 1rem;
}

.sidebar-left {
  border-right: 1px solid var(--border);
  border-left: none;
}

.sidebar-right {
  border-left: 1px solid var(--border);
  border-right: none;
}

.sidebar-header {
  margin-bottom: 1rem;
}

.graph-name-input {
  width: 100%;
  font-size: 1rem;
  font-weight: 600;
  background: transparent;
  border: none;
  border-bottom: 1px solid transparent;
  padding: 0.25rem 0;
  color: var(--text-primary);
}

.graph-name-input:focus {
  border-bottom-color: var(--accent);
}

.sidebar-section {
  margin-bottom: 1rem;
}

.sidebar-section h3 {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  margin-bottom: 0.5rem;
}

.graph-actions {
  display: flex;
  gap: 0.5rem;
}

.presets-dropdown {
  margin-top: 0.5rem;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}

.preset-item {
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  border-bottom: 1px solid var(--bg-tertiary);
  transition: background 0.15s;
}

.preset-item:last-child {
  border-bottom: none;
}

.preset-item:hover {
  background: var(--bg-tertiary);
}

.preset-item strong {
  font-size: 0.85rem;
}

.preset-item span {
  font-size: 0.7rem;
  color: var(--text-muted);
}

.graph-info {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.edge-list {
  max-height: 200px;
  overflow-y: auto;
}

.empty-state {
  font-size: 0.8rem;
  color: var(--text-muted);
  font-style: italic;
}

.edge-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  padding: 0.2rem 0;
  font-size: 0.8rem;
}

.edge-label {
  font-size: 0.75rem;
}

.weight-input {
  width: 56px;
  padding: 0.2rem 0.35rem;
  font-size: 0.75rem;
  text-align: center;
}

.save-section {
  border-top: 1px solid var(--border);
  padding-top: 1rem;
}

.share-link {
  margin-top: 0.5rem;
}

.share-link label {
  font-size: 0.75rem;
  color: var(--text-muted);
  display: block;
  margin-bottom: 0.25rem;
}

.share-url-row {
  display: flex;
  gap: 4px;
}

.share-url-input {
  flex: 1;
  font-size: 0.7rem;
  padding: 0.25rem 0.5rem;
  min-width: 0;
}

.graph-area {
  position: relative;
  background: var(--bg-primary);
}

@media (max-width: 1024px) {
  .sandbox-layout {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr auto;
  }

  .sandbox {
    height: auto;
    overflow: auto;
  }

  .graph-area {
    min-height: 400px;
  }
}
</style>
