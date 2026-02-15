<template>
  <div class="shared-view" v-if="loaded">
    <div class="shared-layout">
      <div class="shared-sidebar card">
        <router-link to="/" class="back-link">&larr; Home</router-link>
        <h2>{{ store.graphName }}</h2>
        <p class="shared-info">
          {{ store.nodes.length }} nodes, {{ store.edges.length }} edges
        </p>
        <button class="btn-primary" style="width: 100%" @click="openInSandbox">
          Open in Sandbox
        </button>
        <AlgorithmPanel />
      </div>
      <div class="graph-area">
        <GraphCanvas />
      </div>
    </div>
  </div>
  <div v-else-if="error" class="error-page container">
    <h2>Graph not found</h2>
    <p>This shared graph link may be invalid or expired.</p>
    <router-link to="/" class="btn-primary" style="display: inline-block; margin-top: 1rem">Go Home</router-link>
  </div>
  <div v-else class="loading container">Loading shared graph...</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGraphStore } from '../stores/graph'
import { loadSharedGraph } from '../api'
import GraphCanvas from '../components/GraphCanvas.vue'
import AlgorithmPanel from '../components/AlgorithmPanel.vue'

const props = defineProps({ token: String })
const router = useRouter()
const store = useGraphStore()
const loaded = ref(false)
const error = ref(false)

function openInSandbox() {
  router.push('/sandbox')
}

onMounted(async () => {
  try {
    const graph = await loadSharedGraph(props.token)
    store.loadGraphData(graph.graph_data, graph.name)
    store.graphId = graph.id
    store.shareToken = graph.share_token
    loaded.value = true
  } catch (e) {
    error.value = true
  }
})
</script>

<style scoped>
.shared-view {
  height: calc(100vh - 53px);
  overflow: hidden;
}

.shared-layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  height: 100%;
}

.shared-sidebar {
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

.shared-sidebar h2 {
  font-size: 1.2rem;
  font-weight: 700;
}

.shared-info {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.graph-area {
  background: var(--bg-primary);
}

.error-page, .loading {
  padding: 3rem;
  text-align: center;
}

.error-page h2 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.error-page p {
  color: var(--text-secondary);
}
</style>
