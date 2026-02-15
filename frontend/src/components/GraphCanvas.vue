<template>
  <div class="graph-canvas-wrapper">
    <div ref="cyContainer" class="cy-container"></div>
    <div class="canvas-toolbar">
      <button class="btn-icon" :class="{ active: mode === 'select' }" @click="mode = 'select'" title="Select & move">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3l7.07 16.97 2.51-7.39 7.39-2.51L3 3z"/></svg>
      </button>
      <button class="btn-icon" :class="{ active: mode === 'addNode' }" @click="mode = 'addNode'" title="Add node (click canvas)">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
      </button>
      <button class="btn-icon" :class="{ active: mode === 'addEdge' }" @click="mode = 'addEdge'" title="Add edge (click source then target)">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="19" x2="19" y2="5"/><circle cx="5" cy="19" r="3"/><circle cx="19" cy="5" r="3"/></svg>
      </button>
      <button class="btn-icon" :class="{ active: mode === 'delete' }" @click="mode = 'delete'" title="Delete (click node or edge)">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
      <div class="toolbar-sep"></div>
      <button class="btn-icon" @click="fitGraph" title="Fit to view">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>
      </button>
    </div>
    <div v-if="mode === 'addEdge' && edgeSource" class="mode-hint">
      Click target node for edge from <strong>{{ edgeSource }}</strong>
    </div>
    <div v-else-if="mode === 'addNode'" class="mode-hint">Click on canvas to add a node</div>
    <div v-else-if="mode === 'delete'" class="mode-hint">Click a node or edge to delete it</div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import cytoscape from 'cytoscape'
import { useGraphStore } from '../stores/graph'

const store = useGraphStore()
const cyContainer = ref(null)
const mode = ref('select')
const edgeSource = ref(null)
let cy = null

const props = defineProps({
  readonly: { type: Boolean, default: false },
})

const emit = defineEmits(['nodeClick', 'ready'])

function getCyStyle() {
  return [
    {
      selector: 'node',
      style: {
        'background-color': 'data(bgColor)',
        'label': 'data(label)',
        'color': '#f1f5f9',
        'text-valign': 'center',
        'text-halign': 'center',
        'font-size': '12px',
        'font-weight': '600',
        'font-family': 'Inter, sans-serif',
        'width': 36,
        'height': 36,
        'border-width': 'data(borderWidth)',
        'border-color': 'data(borderColor)',
        'text-outline-width': 0,
        'overlay-padding': '4px',
        'z-index': 10,
      },
    },
    {
      selector: 'edge',
      style: {
        'width': 2.5,
        'line-color': 'data(lineColor)',
        'target-arrow-color': 'data(lineColor)',
        'target-arrow-shape': store.directed ? 'triangle' : 'none',
        'curve-style': 'bezier',
        'label': 'data(weightLabel)',
        'font-size': '11px',
        'font-weight': '500',
        'font-family': 'JetBrains Mono, monospace',
        'color': '#94a3b8',
        'text-background-color': '#1e293b',
        'text-background-opacity': 0.9,
        'text-background-padding': '3px',
        'text-background-shape': 'roundrectangle',
        'z-index': 1,
      },
    },
    {
      selector: 'node:selected',
      style: {
        'border-width': 3,
        'border-color': '#6366f1',
      },
    },
    {
      selector: 'edge:selected',
      style: {
        'line-color': '#6366f1',
        'target-arrow-color': '#6366f1',
        'width': 3.5,
      },
    },
  ]
}

function buildElements() {
  const step = store.currentStep
  const visitedNodes = new Set(step?.visited_nodes || [])
  const visitedEdges = new Set(step?.visited_edges || [])
  const highlightNodes = new Set(step?.highlight_nodes || [])
  const highlightEdges = new Set(step?.highlight_edges || [])
  const currentNode = step?.current_node
  const pathNodes = new Set(step?.path || [])

  const nodeElements = store.nodes.map(n => {
    let bgColor = '#475569'
    let borderWidth = 2
    let borderColor = '#475569'

    if (step) {
      if (pathNodes.size > 0 && pathNodes.has(n.id)) {
        bgColor = '#22c55e'
        borderColor = '#22c55e'
        borderWidth = 3
      } else if (n.id === currentNode) {
        bgColor = '#f59e0b'
        borderColor = '#f59e0b'
        borderWidth = 3
      } else if (highlightNodes.has(n.id)) {
        bgColor = '#22c55e'
        borderColor = '#22c55e'
        borderWidth = 3
      } else if (visitedNodes.has(n.id)) {
        bgColor = '#6366f1'
        borderColor = '#6366f1'
      }
    }

    return {
      data: {
        id: n.id,
        label: n.label || n.id,
        bgColor,
        borderWidth,
        borderColor,
      },
      position: { x: n.x || 0, y: n.y || 0 },
    }
  })

  const edgeElements = store.edges.map(e => {
    let lineColor = '#475569'

    if (step) {
      if (highlightEdges.has(e.id)) {
        lineColor = '#22c55e'
      } else if (visitedEdges.has(e.id)) {
        lineColor = '#6366f1'
      }
    }

    return {
      data: {
        id: e.id,
        source: e.source,
        target: e.target,
        weight: e.weight,
        weightLabel: e.weight !== 1 ? String(e.weight) : '',
        lineColor,
      },
    }
  })

  return [...nodeElements, ...edgeElements]
}

function initCytoscape() {
  if (!cyContainer.value) return

  cy = cytoscape({
    container: cyContainer.value,
    elements: buildElements(),
    style: getCyStyle(),
    layout: { name: 'preset' },
    userZoomingEnabled: true,
    userPanningEnabled: true,
    boxSelectionEnabled: false,
    autoungrabify: props.readonly,
  })

  // Event handlers
  cy.on('tap', (event) => {
    if (props.readonly) return
    if (event.target === cy) {
      // Clicked on background
      if (mode.value === 'addNode') {
        const pos = event.position
        store.addNode(pos.x, pos.y)
        refreshGraph()
      }
      edgeSource.value = null
    }
  })

  cy.on('tap', 'node', (event) => {
    const nodeId = event.target.id()
    emit('nodeClick', nodeId)

    if (props.readonly) return

    if (mode.value === 'addEdge') {
      if (!edgeSource.value) {
        edgeSource.value = nodeId
      } else {
        store.addEdge(edgeSource.value, nodeId)
        edgeSource.value = null
        refreshGraph()
      }
    } else if (mode.value === 'delete') {
      store.removeNode(nodeId)
      refreshGraph()
    }
  })

  cy.on('tap', 'edge', (event) => {
    if (props.readonly) return
    if (mode.value === 'delete') {
      store.removeEdge(event.target.id())
      refreshGraph()
    }
  })

  cy.on('dragfree', 'node', (event) => {
    if (props.readonly) return
    const node = event.target
    const pos = node.position()
    const storeNode = store.nodes.find(n => n.id === node.id())
    if (storeNode) {
      storeNode.x = pos.x
      storeNode.y = pos.y
    }
  })

  emit('ready', cy)
}

function refreshGraph() {
  if (!cy) return
  const elements = buildElements()

  cy.elements().remove()
  cy.add(elements)

  // Update arrow style based on directed flag
  cy.style().selector('edge').style({
    'target-arrow-shape': store.directed ? 'triangle' : 'none',
  }).update()
}

function fitGraph() {
  if (cy) {
    cy.fit(undefined, 40)
  }
}

// Watch for store changes
watch(
  () => [store.nodes.length, store.edges.length, store.currentStepIndex, store.directed],
  () => {
    nextTick(() => refreshGraph())
  },
)

// Deep watch for position and data changes
watch(
  () => JSON.stringify(store.nodes) + JSON.stringify(store.edges),
  () => {
    nextTick(() => refreshGraph())
  },
)

onMounted(() => {
  initCytoscape()
})

onUnmounted(() => {
  if (cy) {
    cy.destroy()
    cy = null
  }
})

defineExpose({ fitGraph, refreshGraph, cy: () => cy })
</script>

<style scoped>
.graph-canvas-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 400px;
  background: var(--bg-primary);
  border-radius: 8px;
  overflow: hidden;
}

.cy-container {
  width: 100%;
  height: 100%;
  min-height: 400px;
}

.canvas-toolbar {
  position: absolute;
  top: 12px;
  left: 12px;
  display: flex;
  gap: 4px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 4px;
  z-index: 10;
}

.canvas-toolbar .btn-icon.active {
  background: var(--accent);
  color: white;
  border-color: var(--accent);
}

.toolbar-sep {
  width: 1px;
  background: var(--border);
  margin: 2px 4px;
}

.mode-hint {
  position: absolute;
  bottom: 12px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.35rem 0.75rem;
  font-size: 0.8rem;
  color: var(--text-secondary);
  z-index: 10;
}
</style>
