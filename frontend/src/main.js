import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { createI18n } from 'vue-i18n'

const messages = {
  en: {
    nav: {
      home: 'Home',
      search: 'Search',
      login: 'Login',
      logout: 'Logout',
      register: 'Register',
      watchlist: 'Watchlist'
    },
    home: {
      title: 'Popular Movies',
      rating: 'Rating',
      addToWatchlist: 'Add to Watchlist'
    }
  },
  tr: {
    nav: {
      home: 'Ana Sayfa',
      search: 'Ara',
      login: 'Giriş',
      logout: 'Çıkış',
      register: 'Kayıt Ol',
      watchlist: 'İzleme Listesi'
    },
    home: {
      title: 'Popüler Filmler',
      rating: 'Puan',
      addToWatchlist: 'İzleme Listesine Ekle'
    }
  }
}

const i18n = createI18n({
  locale: navigator.language.startsWith('tr') ? 'tr' : 'en',
  fallbackLocale: 'en',
  messages
})

createApp(App).use(store).use(router).use(i18n).mount('#app')