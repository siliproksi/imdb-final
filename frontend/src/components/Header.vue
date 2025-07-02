<template>
  <header class="header">
    <div class="container">
      <div class="header-content">
        <div class="nav-brand">
          <router-link to="/" class="logo">IMDB Clone</router-link>
          <button @click="toggleMobileMenu" class="mobile-menu-btn">
            <span :class="{ active: showMobileMenu }"></span>
            <span :class="{ active: showMobileMenu }"></span>
            <span :class="{ active: showMobileMenu }"></span>
          </button>
        </div>
        
        <div class="nav-center desktop-only">
          <SearchBox />
        </div>
        
        <div class="nav-right desktop-only">
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
      
      <!-- Mobile Menu -->
      <div :class="['mobile-menu', { active: showMobileMenu }]">
        <div class="mobile-search">
          <SearchBox />
        </div>
        
        <div class="mobile-nav">
          <div class="language-toggle">
            <select v-model="currentLanguage" @change="changeLanguage">
              <option value="en">EN</option>
              <option value="tr">TR</option>
            </select>
          </div>
          
          <div v-if="!user" class="mobile-auth-links">
            <router-link to="/login" class="mobile-nav-link" @click="closeMobileMenu">{{ $t('nav.login') }}</router-link>
            <router-link to="/register" class="mobile-nav-link" @click="closeMobileMenu">{{ $t('nav.register') }}</router-link>
          </div>
          
          <div v-else class="mobile-user-menu">
            <div class="mobile-username">{{ user.email }}</div>
            <router-link to="/watchlist" class="mobile-nav-link" @click="closeMobileMenu">{{ $t('nav.watchlist') }}</router-link>
            <button @click="logout" class="mobile-nav-link mobile-logout-btn">{{ $t('nav.logout') }}</button>
          </div>
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
.header {
  background-color: #1a1a1a;
  padding: 1rem 0;
  border-bottom: 1px solid #333;
  position: relative;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-brand {
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

.mobile-menu-btn {
  display: none;
  flex-direction: column;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  gap: 4px;
}

.mobile-menu-btn span {
  width: 25px;
  height: 3px;
  background-color: #f5c518;
  transition: all 0.3s ease;
  border-radius: 3px;
}

.mobile-menu-btn span.active:nth-child(1) {
  transform: rotate(45deg) translate(6px, 6px);
}

.mobile-menu-btn span.active:nth-child(2) {
  opacity: 0;
}

.mobile-menu-btn span.active:nth-child(3) {
  transform: rotate(-45deg) translate(6px, -6px);
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

/* Mobile Menu */
.mobile-menu {
  display: none;
  background-color: #1a1a1a;
  border-top: 1px solid #333;
  padding: 1rem 0;
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 1000;
  transform: translateY(-100%);
  opacity: 0;
  transition: all 0.3s ease;
}

.mobile-menu.active {
  transform: translateY(0);
  opacity: 1;
}

.mobile-search {
  margin-bottom: 1rem;
}

.mobile-nav {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.mobile-auth-links, .mobile-user-menu {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mobile-nav-link {
  color: white;
  text-decoration: none;
  padding: 0.75rem;
  border-radius: 4px;
  transition: background-color 0.3s;
  text-align: center;
  border: 1px solid #333;
}

.mobile-nav-link:hover {
  background-color: #333;
}

.mobile-logout-btn {
  background: none;
  border: 1px solid #333;
  cursor: pointer;
  font-size: inherit;
  color: white;
}

.mobile-username {
  color: #f5c518;
  font-weight: bold;
  text-align: center;
  padding: 0.5rem;
}

.desktop-only {
  display: flex;
}

/* Responsive Design */
@media (max-width: 768px) {
  .desktop-only {
    display: none;
  }
  
  .mobile-menu-btn {
    display: flex;
  }
  
  .mobile-menu {
    display: block;
  }
  
  .nav-brand {
    width: 100%;
  }
  
  .logo {
    font-size: 1.25rem;
  }
}

@media (max-width: 480px) {
  .header {
    padding: 0.75rem 0;
  }
  
  .logo {
    font-size: 1.1rem;
  }
  
  .mobile-menu {
    padding: 0.75rem 0;
  }
}
</style>