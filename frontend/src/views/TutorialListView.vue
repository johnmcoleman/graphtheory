<template>
  <div class="tutorials-page container">
    <div class="page-header">
      <h1>Tutorials</h1>
      <p>Learn fundamental graph algorithms through interactive, step-by-step visualizations.</p>
    </div>

    <div class="tutorial-grid">
      <router-link
        v-for="tutorial in tutorials"
        :key="tutorial.id"
        :to="{ name: 'tutorial', params: { id: tutorial.id } }"
        class="tutorial-card card"
      >
        <span :class="['badge', getCategoryClass(tutorial.algorithm)]">
          {{ getCategoryLabel(tutorial.algorithm) }}
        </span>
        <h3>{{ tutorial.title }}</h3>
        <p>{{ getShortDescription(tutorial.description) }}</p>
        <span class="tutorial-link">Start tutorial &rarr;</span>
      </router-link>
    </div>

    <div class="famous-graphs">
      <h2>Famous Graphs</h2>
      <p class="section-subtitle">Explore well-known graph structures from mathematics.</p>
      <div class="famous-grid">
        <div
          v-for="preset in famousPresets"
          :key="preset.id"
          class="famous-card card"
          @click="openInSandbox(preset)"
        >
          <h3>{{ preset.name }}</h3>
          <p>{{ preset.description }}</p>
          <span class="tutorial-link">Open in sandbox &rarr;</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getTutorials, getPresetGraphs } from '../api'
import { useGraphStore } from '../stores/graph'

const router = useRouter()
const store = useGraphStore()
const tutorials = ref([])
const famousPresets = ref([])

function getCategoryClass(algo) {
  if (algo === 'bfs' || algo === 'dfs') return 'badge-traversal'
  return 'badge-shortest-path'
}

function getCategoryLabel(algo) {
  if (algo === 'bfs' || algo === 'dfs') return 'Traversal'
  return 'Shortest Path'
}

function getShortDescription(desc) {
  // Get first line of the markdown description
  const firstLine = desc.split('\n').find(l => l.trim() && !l.startsWith('*'))
  return firstLine?.replace(/\*\*/g, '').substring(0, 120) + '...' || ''
}

function openInSandbox(preset) {
  store.loadGraphData(preset.graph_data, preset.name)
  router.push('/sandbox')
}

onMounted(async () => {
  try {
    tutorials.value = await getTutorials()
    const presets = await getPresetGraphs()
    famousPresets.value = presets.filter(p => p.category === 'famous')
  } catch (e) {
    console.error('Failed to load tutorials:', e)
  }
})
</script>

<style scoped>
.tutorials-page {
  padding: 2rem 0 4rem;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.page-header p {
  color: var(--text-secondary);
  font-size: 1.05rem;
}

.tutorial-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 3rem;
}

.tutorial-card {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  transition: border-color 0.2s, transform 0.15s;
  cursor: pointer;
  color: var(--text-primary);
}

.tutorial-card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
  color: var(--text-primary);
}

.tutorial-card h3 {
  font-size: 1.1rem;
  font-weight: 600;
}

.tutorial-card p {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.5;
  flex: 1;
}

.tutorial-link {
  font-size: 0.85rem;
  color: var(--accent);
  font-weight: 500;
  margin-top: 0.5rem;
}

.famous-graphs h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.section-subtitle {
  color: var(--text-secondary);
  margin-bottom: 1rem;
}

.famous-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.famous-card {
  cursor: pointer;
  transition: border-color 0.2s, transform 0.15s;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.famous-card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
}

.famous-card h3 {
  font-size: 1rem;
  font-weight: 600;
}

.famous-card p {
  font-size: 0.8rem;
  color: var(--text-secondary);
  line-height: 1.5;
  flex: 1;
}

@media (max-width: 768px) {
  .tutorial-grid,
  .famous-grid {
    grid-template-columns: 1fr;
  }
}
</style>
