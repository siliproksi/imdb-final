<template>
  <div id="app">
    <Header />
    <router-view />
  </div>
</template>

<script>
import Header from './components/Header.vue'

export default {
  name: 'App',
  components: {
    Header
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Arial', sans-serif;
  background-color: #121212;
  color: #ffffff;
  overflow-x: hidden;
}

#app {
  min-height: 100vh;
  width: 100%;
}

/* Global responsive utilities */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

@media (max-width: 768px) {
  .container {
    padding: 0 0.75rem;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 0.5rem;
  }
}
</style>