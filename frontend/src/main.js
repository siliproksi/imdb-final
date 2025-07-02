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
      watchlist: 'Watchlist',
      close: 'Close'
    },
    home: {
      title: 'Popular Movies',
      rating: 'Rating',
      addToWatchlist: 'Add to Watchlist',
      subtitle: 'Discover amazing movies and share your thoughts'
    },
    login: {
      title: 'Login',
      email: 'Email',
      password: 'Password',
      loginButton: 'Login',
      loggingIn: 'Logging in...',
      googleLogin: 'Login with Google',
      noAccount: "Don't have an account?",
      registerLink: 'Register'
    },
    register: {
      title: 'Register',
      email: 'Email',
      password: 'Password',
      country: 'Country',
      city: 'City',
      photo: 'Profile Photo (Optional)',
      registerButton: 'Register',
      creatingAccount: 'Creating Account...',
      passwordHelp: 'Password must be at least 8 characters long, contain 1 number and 1 special character',
      hasAccount: 'Already have an account?',
      loginLink: 'Login',
      successMessage: 'Account created successfully! You can now log in.'
    },
    search: {
      title: 'Search Results',
      resultsFor: 'Results for:',
      searching: 'Searching...',
      movies: 'Movies',
      actors: 'Actors',
      noResults: 'No results found',
      tryDifferent: 'Try searching with different keywords.',
      placeholder: 'Search movies, actors...',
      searchButton: 'Search',
      all: 'All'
    },
    movie: {
      averageRating: 'Average Rating',
      totalRatings: 'Total Ratings',
      popularityScore: 'Popularity Score',
      trailer: 'Trailer',
      cast: 'Cast',
      userRatings: 'User Ratings & Comments',
      noRatings: 'No ratings yet. Be the first to rate this movie!',
      loading: 'Loading movie details...',
      rateMovie: 'Rate Movie',
      addToWatchlist: 'Add to Watchlist',
      rating: 'Rating (1-10)',
      comment: 'Comment (Optional)',
      cancel: 'Cancel',
      submitRating: 'Submit Rating'
    },
    watchlist: {
      title: 'My Watchlist',
      loading: 'Loading your watchlist...',
      empty: 'Your watchlist is empty',
      emptyMessage: 'Start adding movies to your watchlist to keep track of what you want to watch!',
      browseMovies: 'Browse Movies',
      addedDate: 'Added:',
      removeButton: 'Remove from Watchlist'
    },
    actor: {
      noBio: 'No biography available',
      appearsIn: 'Appears in',
      loading: 'Loading actor details...'
    },
    common: {
      year: 'Year',
      duration: 'Duration',
      noDescription: 'No description available',
      noSummary: 'No summary available'
    }
  },
  tr: {
    nav: {
      home: 'Ana Sayfa',
      search: 'Ara',
      login: 'Giriş',
      logout: 'Çıkış',
      register: 'Kayıt Ol',
      watchlist: 'İzleme Listesi',
      close: 'Kapat'
    },
    home: {
      title: 'Popüler Filmler',
      rating: 'Puan',
      addToWatchlist: 'İzleme Listesine Ekle',
      subtitle: 'Harika filmleri keşfedin ve düşüncelerinizi paylaşın'
    },
    login: {
      title: 'Giriş',
      email: 'E-posta',
      password: 'Şifre',
      loginButton: 'Giriş Yap',
      loggingIn: 'Giriş yapılıyor...',
      googleLogin: 'Google ile Giriş',
      noAccount: 'Hesabınız yok mu?',
      registerLink: 'Kayıt Ol'
    },
    register: {
      title: 'Kayıt Ol',
      email: 'E-posta',
      password: 'Şifre',
      country: 'Ülke',
      city: 'Şehir',
      photo: 'Profil Fotoğrafı (İsteğe Bağlı)',
      registerButton: 'Kayıt Ol',
      creatingAccount: 'Hesap oluşturuluyor...',
      passwordHelp: 'Şifre en az 8 karakter olmalı, 1 rakam ve 1 özel karakter içermelidir',
      hasAccount: 'Zaten hesabınız var mı?',
      loginLink: 'Giriş Yap',
      successMessage: 'Hesap başarıyla oluşturuldu! Artık giriş yapabilirsiniz.'
    },
    search: {
      title: 'Arama Sonuçları',
      resultsFor: 'Arama sonuçları:',
      searching: 'Aranıyor...',
      movies: 'Filmler',
      actors: 'Oyuncular',
      noResults: 'Sonuç bulunamadı',
      tryDifferent: 'Farklı anahtar kelimelerle aramayı deneyin.',
      placeholder: 'Filmleri, oyuncuları arayın...',
      searchButton: 'Ara',
      all: 'Tümü'
    },
    movie: {
      averageRating: 'Ortalama Puan',
      totalRatings: 'Toplam Puanlama',
      popularityScore: 'Popülerlik Puanı',
      trailer: 'Fragman',
      cast: 'Oyuncular',
      userRatings: 'Kullanıcı Puanları ve Yorumları',
      noRatings: 'Henüz puanlama yok. Bu filmi puanlayan ilk kişi olun!',
      loading: 'Film detayları yükleniyor...',
      rateMovie: 'Filmi Puanla',
      addToWatchlist: 'İzleme Listesine Ekle',
      rating: 'Puan (1-10)',
      comment: 'Yorum (İsteğe Bağlı)',
      cancel: 'İptal',
      submitRating: 'Puanı Gönder'
    },
    watchlist: {
      title: 'İzleme Listem',
      loading: 'İzleme listeniz yükleniyor...',
      empty: 'İzleme listeniz boş',
      emptyMessage: 'İzlemek istediğiniz filmleri takip etmek için izleme listenize film eklemeye başlayın!',
      browseMovies: 'Filmlere Göz At',
      addedDate: 'Eklenme Tarihi:',
      removeButton: 'İzleme Listesinden Çıkar'
    },
    actor: {
      noBio: 'Biyografi mevcut değil',
      appearsIn: 'Oynadığı filmler',
      loading: 'Oyuncu detayları yükleniyor...'
    },
    common: {
      year: 'Yıl',
      duration: 'Süre',
      noDescription: 'Açıklama mevcut değil',
      noSummary: 'Özet mevcut değil'
    }
  }
}

const i18n = createI18n({
  locale: navigator.language.startsWith('tr') ? 'tr' : 'en',
  fallbackLocale: 'en',
  messages
})

createApp(App).use(store).use(router).use(i18n).mount('#app')