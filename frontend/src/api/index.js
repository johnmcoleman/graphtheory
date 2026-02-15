import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
})

export async function runAlgorithm(graphData, algorithm, startNode, endNode = null, directed = false) {
  const res = await api.post('/algorithms/run', {
    graph_data: graphData,
    algorithm,
    start_node: startNode,
    end_node: endNode,
    directed,
  })
  return res.data
}

export async function listAlgorithms() {
  const res = await api.get('/algorithms/list')
  return res.data.algorithms
}

export async function getPresetGraphs() {
  const res = await api.get('/presets/graphs')
  return res.data.presets
}

export async function getTutorials() {
  const res = await api.get('/presets/tutorials')
  return res.data.tutorials
}

export async function saveGraph(graphPayload) {
  const res = await api.post('/graphs/', graphPayload)
  return res.data
}

export async function loadGraph(graphId) {
  const res = await api.get(`/graphs/${graphId}`)
  return res.data
}

export async function loadSharedGraph(shareToken) {
  const res = await api.get(`/graphs/share/${shareToken}`)
  return res.data
}

export async function listSavedGraphs() {
  const res = await api.get('/graphs/')
  return res.data
}

export async function deleteGraph(graphId) {
  const res = await api.delete(`/graphs/${graphId}`)
  return res.data
}
