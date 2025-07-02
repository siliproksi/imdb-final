<template>
  <!-- DESKTOP HEADER -->
  <header class="header desktop-header">
    <div class="container">
      <div class="header-content">
        <router-link to="/" class="logo">IMDB Clone</router-link>
        
        <div class="search-section">
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
    </div>
  </header>

  <!-- MOBILE HEADER -->
  <header class="header mobile-header">
    <div class="container">
      <div class="mobile-header-content">
        <div class="mobile-search">
          <SearchBox />
        </div>
        <div class="hamburger" @click="toggleMobileMenu">
          <span :class="{ active: showMobileMenu }"></span>
          <span :class="{ active: showMobileMenu }"></span>
          <span :class="{ active: showMobileMenu }"></span>
        </div>
      </div>
    </div>
  </header>

  <!-- MOBILE MENU -->
  <div v-if="showMobileMenu" class="mobile-overlay">
    <div class="mobile-menu-content">
      <!-- User email at the very top when logged in -->
      <div v-if="user" class="mobile-user-email">{{ user.email }}</div>
      
      <div class="mobile-language">
        <select v-model="currentLanguage" @change="changeLanguage">
          <option value="en">EN</option>
          <option value="tr">TR</option>
        </select>
      </div>
      
      <div v-if="!user" class="mobile-links">
        <router-link to="/" @click="closeMobileMenu">{{ $t('nav.home') }}</router-link>
        <router-link to="/login" @click="closeMobileMenu">{{ $t('nav.login') }}</router-link>
        <router-link to="/register" @click="closeMobileMenu">{{ $t('nav.register') }}</router-link>
        <button @click="closeMobileMenu" class="close-btn">{{ $t('nav.close') }}</button>
      </div>
      
      <div v-else class="mobile-links">
        <router-link to="/" @click="closeMobileMenu">{{ $t('nav.home') }}</router-link>
        <router-link to="/watchlist" @click="closeMobileMenu">{{ $t('nav.watchlist') }}</router-link>
        <button @click="logout">{{ $t('nav.logout') }}</button>
        <button @click="closeMobileMenu" class="close-btn">{{ $t('nav.close') }}</button>
      </div>
    </div>
  </div>
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
      currentLanguage: this.$i18n.locale,
      showMobileMenu: false
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
      this.closeMobileMenu()
      this.$router.push('/')
    },
    
    toggleMobileMenu() {
      this.showMobileMenu = !this.showMobileMenu
    },
    
    closeMobileMenu() {
      this.showMobileMenu = false
    }
  }
}
</script>

<style scoped>
/* DESKTOP STYLES */
.desktop-header {
  background-color: #1a1a1a;
  padding: 1rem 0;
  border-bottom: 1px solid #333;
  display: block;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #f5c518;
  text-decoration: none;
}

.search-section {
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
  min-width: 60px;
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
  white-space: nowrap;
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

/* MOBILE STYLES */
.mobile-header {
  background-color: #1a1a1a;
  padding: 1rem 0;
  border-bottom: 1px solid #333;
  display: none;
}

.mobile-header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.mobile-search {
  flex: 1;
  max-width: 300px;
}

.mobile-logo {
  font-size: 1.25rem;
  font-weight: bold;
  color: #f5c518;
  text-decoration: none;
}

.hamburger {
  display: flex;
  flex-direction: column;
  cursor: pointer;
  gap: 4px;
  padding: 0.5rem;
}

.hamburger span {
  width: 25px;
  height: 3px;
  background-color: #f5c518;
  transition: all 0.3s ease;
  border-radius: 3px;
}

.hamburger span.active:nth-child(1) {
  transform: rotate(45deg) translate(6px, 6px);
}

.hamburger span.active:nth-child(2) {
  opacity: 0;
}

.hamburger span.active:nth-child(3) {
  transform: rotate(-45deg) translate(6px, -6px);
}

/* MOBILE MENU OVERLAY */
.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.9);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mobile-menu-content {
  background-color: #1a1a1a;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
}

.mobile-user-email {
  color: #f5c518;
  font-weight: bold;
  text-align: center;
  padding: 0.5rem 0;
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
}

.mobile-language {
  margin-bottom: 1.5rem;
}

.mobile-language select {
  width: 100%;
  background-color: #333;
  color: white;
  border: 1px solid #555;
  padding: 0.75rem;
  border-radius: 4px;
}

.mobile-links {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.mobile-links a, .mobile-links button {
  color: white;
  text-decoration: none;
  padding: 1rem;
  border: 1px solid #333;
  border-radius: 4px;
  background: none;
  cursor: pointer;
  font-size: 1rem;
  text-align: center;
  transition: background-color 0.3s;
}

.mobile-links a:hover, .mobile-links button:hover {
  background-color: #333;
}

.mobile-user {
  color: #f5c518;
  font-weight: bold;
  text-align: center;
  padding: 1rem;
  border: 1px solid #f5c518;
  border-radius: 4px;
}

.close-btn {
  background-color: #666 !important;
  border: 1px solid #666 !important;
  color: white !important;
}

.close-btn:hover {
  background-color: #555 !important;
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .desktop-header {
    display: none;
  }
  
  .mobile-header {
    display: block;
  }
}

@media (max-width: 480px) {
  .mobile-header {
    padding: 0.75rem 0;
  }
  
  .mobile-logo {
    font-size: 1.1rem;
  }
}
</style>