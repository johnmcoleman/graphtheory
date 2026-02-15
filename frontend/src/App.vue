<template>
  <div id="app-shell">
    <nav class="navbar">
      <div class="nav-inner container">
        <router-link to="/" class="nav-brand">
          <svg width="24" height="24" viewBox="0 0 100 100" class="nav-logo">
            <circle cx="20" cy="20" r="8" fill="#6366f1" />
            <circle cx="80" cy="20" r="8" fill="#6366f1" />
            <circle cx="50" cy="75" r="8" fill="#6366f1" />
            <line x1="20" y1="20" x2="80" y2="20" stroke="#6366f1" stroke-width="3" />
            <line x1="20" y1="20" x2="50" y2="75" stroke="#6366f1" stroke-width="3" />
            <line x1="80" y1="20" x2="50" y2="75" stroke="#6366f1" stroke-width="3" />
          </svg>
          <span>Graph Theory Visualizer</span>
        </router-link>
        <div class="nav-links">
          <router-link to="/sandbox">Sandbox</router-link>
          <router-link to="/tutorials">Tutorials</router-link>
        </div>
      </div>
    </nav>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.navbar {
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border);
  padding: 0.75rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 1.05rem;
  color: var(--text-primary);
}

.nav-brand:hover {
  color: var(--text-primary);
}

.nav-logo {
  flex-shrink: 0;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-links a {
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 0.9rem;
  padding: 0.25rem 0;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: var(--text-primary);
  border-bottom-color: var(--accent);
}

.main-content {
  flex: 1;
}
</style>
