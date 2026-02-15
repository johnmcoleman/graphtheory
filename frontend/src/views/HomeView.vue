<template>
  <div class="home">
    <section class="hero">
      <div class="container">
        <div class="hero-content">
          <h1>Graph Theory <span class="gradient-text">Visualizer</span></h1>
          <p class="hero-subtitle">
            Explore graph algorithms interactively. Watch BFS, DFS, Dijkstra's, and Bellman-Ford come to life
            with step-by-step animations on real graph structures.
          </p>
          <div class="hero-actions">
            <router-link to="/sandbox" class="btn-primary hero-btn">
              Open Sandbox
            </router-link>
            <router-link to="/tutorials" class="btn-secondary hero-btn">
              Start Learning
            </router-link>
          </div>
        </div>
        <div class="hero-visual">
          <svg viewBox="0 0 400 300" class="hero-graph">
            <!-- Edges -->
            <line x1="80" y1="60" x2="200" y2="40" stroke="#6366f1" stroke-width="2" opacity="0.6"/>
            <line x1="80" y1="60" x2="160" y2="160" stroke="#6366f1" stroke-width="2" opacity="0.6"/>
            <line x1="200" y1="40" x2="320" y2="80" stroke="#22c55e" stroke-width="2.5"/>
            <line x1="200" y1="40" x2="160" y2="160" stroke="#6366f1" stroke-width="2" opacity="0.6"/>
            <line x1="320" y1="80" x2="340" y2="200" stroke="#22c55e" stroke-width="2.5"/>
            <line x1="160" y1="160" x2="280" y2="240" stroke="#6366f1" stroke-width="2" opacity="0.6"/>
            <line x1="340" y1="200" x2="280" y2="240" stroke="#22c55e" stroke-width="2.5"/>
            <line x1="160" y1="160" x2="60" y2="240" stroke="#6366f1" stroke-width="2" opacity="0.6"/>
            <!-- Weight labels -->
            <text x="240" y="50" fill="#94a3b8" font-size="11" font-family="JetBrains Mono">4</text>
            <text x="340" y="145" fill="#94a3b8" font-size="11" font-family="JetBrains Mono">2</text>
            <text x="320" y="228" fill="#94a3b8" font-size="11" font-family="JetBrains Mono">3</text>
            <!-- Nodes -->
            <circle cx="80" cy="60" r="18" fill="#475569" stroke="#475569" stroke-width="2"/>
            <text x="80" y="65" fill="white" text-anchor="middle" font-size="12" font-weight="600" font-family="Inter">A</text>
            <circle cx="200" cy="40" r="18" fill="#6366f1" stroke="#6366f1" stroke-width="2"/>
            <text x="200" y="45" fill="white" text-anchor="middle" font-size="12" font-weight="600" font-family="Inter">B</text>
            <circle cx="320" cy="80" r="18" fill="#f59e0b" stroke="#f59e0b" stroke-width="3"/>
            <text x="320" y="85" fill="white" text-anchor="middle" font-size="12" font-weight="600" font-family="Inter">C</text>
            <circle cx="160" cy="160" r="18" fill="#6366f1" stroke="#6366f1" stroke-width="2"/>
            <text x="160" y="165" fill="white" text-anchor="middle" font-size="12" font-weight="600" font-family="Inter">D</text>
            <circle cx="340" cy="200" r="18" fill="#22c55e" stroke="#22c55e" stroke-width="2"/>
            <text x="340" y="205" fill="white" text-anchor="middle" font-size="12" font-weight="600" font-family="Inter">E</text>
            <circle cx="280" cy="240" r="18" fill="#475569" stroke="#475569" stroke-width="2"/>
            <text x="280" y="245" fill="white" text-anchor="middle" font-size="12" font-weight="600" font-family="Inter">F</text>
            <circle cx="60" cy="240" r="18" fill="#475569" stroke="#475569" stroke-width="2"/>
            <text x="60" y="245" fill="white" text-anchor="middle" font-size="12" font-weight="600" font-family="Inter">G</text>
          </svg>
        </div>
      </div>
    </section>

    <section class="features container">
      <div class="feature-grid">
        <div class="feature-card card">
          <div class="feature-icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          </div>
          <h3>Step-by-Step Animation</h3>
          <p>Watch algorithms execute one step at a time. Control playback speed, pause, rewind, and step through each operation.</p>
        </div>
        <div class="feature-card card">
          <div class="feature-icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2"><polygon points="14 2 18 6 7 17 3 17 3 13 14 2"/><line x1="3" y1="22" x2="21" y2="22"/></svg>
          </div>
          <h3>Interactive Graph Editor</h3>
          <p>Build custom graphs by clicking to add nodes and edges. Set weights, toggle directed mode, and design any graph structure.</p>
        </div>
        <div class="feature-card card">
          <div class="feature-icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
          </div>
          <h3>Guided Tutorials</h3>
          <p>Learn BFS, DFS, Dijkstra's, and Bellman-Ford through curated lessons with explanations and preset example graphs.</p>
        </div>
        <div class="feature-card card">
          <div class="feature-icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
          </div>
          <h3>Save &amp; Share</h3>
          <p>Save your graphs and share them with others via unique URLs. Great for collaboration and teaching.</p>
        </div>
      </div>
    </section>

    <section class="algorithms-section container">
      <h2>Algorithms</h2>
      <div class="algo-grid">
        <div class="algo-card card">
          <span class="badge badge-traversal">Traversal</span>
          <h3>Breadth-First Search</h3>
          <p>Explores level by level using a queue. Guarantees shortest path in unweighted graphs. O(V+E) time.</p>
        </div>
        <div class="algo-card card">
          <span class="badge badge-traversal">Traversal</span>
          <h3>Depth-First Search</h3>
          <p>Goes deep before going wide using a stack. Foundation for topological sort and cycle detection. O(V+E) time.</p>
        </div>
        <div class="algo-card card">
          <span class="badge badge-shortest-path">Shortest Path</span>
          <h3>Dijkstra's Algorithm</h3>
          <p>Greedy shortest-path with a priority queue. Works with non-negative weights. O((V+E) log V) time.</p>
        </div>
        <div class="algo-card card">
          <span class="badge badge-shortest-path">Shortest Path</span>
          <h3>Bellman-Ford</h3>
          <p>Handles negative weights via V-1 relaxation rounds. Detects negative cycles. O(V*E) time.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.hero {
  padding: 4rem 0 3rem;
}

.hero .container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
}

h1 {
  font-size: 2.75rem;
  font-weight: 700;
  line-height: 1.15;
  margin-bottom: 1rem;
}

.gradient-text {
  background: linear-gradient(135deg, #6366f1, #22c55e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 1.5rem;
  max-width: 500px;
}

.hero-actions {
  display: flex;
  gap: 0.75rem;
}

.hero-btn {
  display: inline-flex;
  padding: 0.7rem 1.5rem;
  font-weight: 600;
  border-radius: 8px;
  font-size: 0.95rem;
}

.hero-visual {
  display: flex;
  justify-content: center;
}

.hero-graph {
  width: 100%;
  max-width: 400px;
  filter: drop-shadow(0 4px 20px rgba(99, 102, 241, 0.15));
}

.features {
  padding: 2rem 0 3rem;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.feature-card {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.feature-icon {
  margin-bottom: 0.25rem;
}

.feature-card h3 {
  font-size: 0.95rem;
  font-weight: 600;
}

.feature-card p {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

.algorithms-section {
  padding: 2rem 0 4rem;
}

.algorithms-section h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.algo-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.algo-card {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.algo-card h3 {
  font-size: 1rem;
  font-weight: 600;
}

.algo-card p {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

@media (max-width: 768px) {
  .hero .container {
    grid-template-columns: 1fr;
  }

  .hero-visual {
    display: none;
  }

  h1 {
    font-size: 2rem;
  }

  .feature-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .algo-grid {
    grid-template-columns: 1fr;
  }
}
</style>
