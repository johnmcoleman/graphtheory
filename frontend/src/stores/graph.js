import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useGraphStore = defineStore('graph', () => {
  const nodes = ref([])
  const edges = ref([])
  const directed = ref(false)
  const graphName = ref('Untitled Graph')
  const graphId = ref(null)
  const shareToken = ref(null)

  // Algorithm visualization state
  const algorithmSteps = ref([])
  const currentStepIndex = ref(-1)
  const isPlaying = ref(false)
  const playbackSpeed = ref(1000) // ms per step

  const currentStep = computed(() => {
    if (currentStepIndex.value >= 0 && currentStepIndex.value < algorithmSteps.value.length) {
      return algorithmSteps.value[currentStepIndex.value]
    }
    return null
  })

  const totalSteps = computed(() => algorithmSteps.value.length)

  let nextNodeId = 1

  function generateNodeId() {
    const existingIds = new Set(nodes.value.map(n => n.id))
    while (existingIds.has(String(nextNodeId))) {
      nextNodeId++
    }
    const id = String(nextNodeId)
    nextNodeId++
    return id
  }

  function addNode(x, y, label = null) {
    const id = generateNodeId()
    nodes.value.push({
      id,
      label: label || id,
      x,
      y,
    })
    return id
  }

  function removeNode(nodeId) {
    nodes.value = nodes.value.filter(n => n.id !== nodeId)
    edges.value = edges.value.filter(e => e.source !== nodeId && e.target !== nodeId)
  }

  let nextEdgeId = 1

  function generateEdgeId() {
    const existingIds = new Set(edges.value.map(e => e.id))
    while (existingIds.has(`e${nextEdgeId}`)) {
      nextEdgeId++
    }
    const id = `e${nextEdgeId}`
    nextEdgeId++
    return id
  }

  function addEdge(source, target, weight = 1) {
    const exists = edges.value.some(
      e => (e.source === source && e.target === target) ||
           (!directed.value && e.source === target && e.target === source)
    )
    if (exists || source === target) return null

    const id = generateEdgeId()
    edges.value.push({
      id,
      source,
      target,
      weight,
      directed: directed.value,
    })
    return id
  }

  function removeEdge(edgeId) {
    edges.value = edges.value.filter(e => e.id !== edgeId)
  }

  function updateEdgeWeight(edgeId, weight) {
    const edge = edges.value.find(e => e.id === edgeId)
    if (edge) edge.weight = weight
  }

  function clearGraph() {
    nodes.value = []
    edges.value = []
    nextNodeId = 1
    nextEdgeId = 1
    clearVisualization()
  }

  function loadGraphData(graphData, name = null) {
    nodes.value = graphData.nodes || []
    edges.value = graphData.edges || []
    if (name) graphName.value = name

    // Reset ID counters
    const maxNodeId = Math.max(0, ...nodes.value.map(n => parseInt(n.id) || 0))
    nextNodeId = maxNodeId + 1
    const maxEdgeNum = Math.max(0, ...edges.value.map(e => {
      const match = e.id.match(/^e(\d+)$/)
      return match ? parseInt(match[1]) : 0
    }))
    nextEdgeId = maxEdgeNum + 1
    clearVisualization()
  }

  function getGraphData() {
    return {
      nodes: nodes.value.map(n => ({ ...n })),
      edges: edges.value.map(e => ({ ...e })),
    }
  }

  // Visualization controls
  function setAlgorithmSteps(steps) {
    algorithmSteps.value = steps
    currentStepIndex.value = -1
    isPlaying.value = false
  }

  function clearVisualization() {
    algorithmSteps.value = []
    currentStepIndex.value = -1
    isPlaying.value = false
  }

  function stepForward() {
    if (currentStepIndex.value < algorithmSteps.value.length - 1) {
      currentStepIndex.value++
    }
  }

  function stepBackward() {
    if (currentStepIndex.value > 0) {
      currentStepIndex.value--
    }
  }

  function goToStep(index) {
    if (index >= 0 && index < algorithmSteps.value.length) {
      currentStepIndex.value = index
    }
  }

  function resetVisualization() {
    currentStepIndex.value = -1
    isPlaying.value = false
  }

  return {
    nodes,
    edges,
    directed,
    graphName,
    graphId,
    shareToken,
    algorithmSteps,
    currentStepIndex,
    currentStep,
    totalSteps,
    isPlaying,
    playbackSpeed,
    addNode,
    removeNode,
    addEdge,
    removeEdge,
    updateEdgeWeight,
    clearGraph,
    loadGraphData,
    getGraphData,
    setAlgorithmSteps,
    clearVisualization,
    stepForward,
    stepBackward,
    goToStep,
    resetVisualization,
  }
})
