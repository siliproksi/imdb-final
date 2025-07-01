<template>
  <header class="header">
    <div class="container">
      <div class="nav-brand">
        <router-link to="/" class="logo">IMDB Clone</router-link>
      </div>
      
      <div class="nav-center">
        <SearchBox />
      </div>
      
      <div class="nav-right">
        <div class="language-toggle">
          <select v-model="currentLanguage" @change="changeLanguage">
            <option value="en">EN</option>
            <option value="tr">TR</option>
          </select>
        </div>
        
        <div v-if="!user" class="auth-links">
          <router-link to="/login" class="nav-link">{{ $t('nav.login') }}</router-link>
          <router-link to="/register" class="nav-link">{{ $t('nav.register') }}</router-link>
        </div>
        
        <div v-else class="user-menu">
          <span class="username">{{ user.email }}</span>
          <router-link to="/watchlist" class="nav-link">{{ $t('nav.watchlist') }}</router-link>
          <button @click="logout" class="nav-link logout-btn">{{ $t('nav.logout') }}</button>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import SearchBox from './SearchBox.vue'

export default {
  name: 'Header',
  components: {
    SearchBox
  },
  data() {
    return {
      currentLanguage: this.$i18n.locale
    }
  },
  computed: {
    ...mapState(['user'])
  },
  methods: {
    ...mapActions(['logoutUser']),
    changeLanguage() {
      this.$i18n.locale = this.currentLanguage
      localStorage.setItem('language', this.currentLanguage)
    },
    logout() {
      this.logoutUser()
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.header {
  background-color: #1a1a1a;
  padding: 1rem 0;
  border-bottom: 1px solid #333;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #f5c518;
  text-decoration: none;
}

.nav-center {
  flex: 1;
  max-width: 400px;
  margin: 0 2rem;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.language-toggle select {
  background-color: #333;
  color: white;
  border: 1px solid #555;
  padding: 0.5rem;
  border-radius: 4px;
}

.auth-links, .user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-link:hover {
  background-color: #333;
}

.logout-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: inherit;
}

.username {
  color: #f5c518;
  font-weight: bold;
}
</style>