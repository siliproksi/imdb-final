<template>
  <div class="home">
    <div class="hero-section">
      <div class="container">
        <h1>{{ $t('home.title') }}</h1>
        <p>{{ $t('home.subtitle') }}</p>
      </div>
    </div>
    
    <div class="movies-section">
      <div class="container">
        
        <div v-if="loading" class="loading">
          {{ $t('movie.loading') }}
        </div>
        
        <div v-else class="movies-slider">
          <div class="movies-horizontal-scroll">
            <div
              v-for="movie in movies.slice(0, 10)"
              :key="movie.id"
              class="movie-card"
              @click="goToMovie(movie.id)"
            >
              <div class="movie-image">
                <img :src="movie.image_url || '/placeholder-movie.jpg'" :alt="movie.title" />
              </div>
              
              <div class="movie-info">
                <h3 class="movie-title">{{ movie.title }}</h3>
                <div class="movie-meta">
                  <span class="movie-year">{{ movie.release_year }}</span>
                  <span class="movie-rating">
                    ⭐ {{ movie.imdb_score || 'No ratings' }}
                  </span>
                </div>
                <p class="movie-summary">{{ truncateSummary(movie.summary) }}</p>
                
                <div class="movie-actions">
                  <button v-if="!user" @click.stop="redirectToLogin" class="action-btn watchlist-btn">
                    {{ $t('home.addToWatchlist') }}
                  </button>
                  <button v-else @click.stop="addToWatchlist(movie.id)" class="action-btn watchlist-btn">
                    {{ $t('home.addToWatchlist') }}
                  </button>
                  
                  <button v-if="!user" @click.stop="redirectToLogin" class="action-btn rate-btn">
                    {{ $t('movie.rateMovie') }}
                  </button>
                  <button v-else @click.stop="goToMovieWithRating(movie.id)" class="action-btn rate-btn">
                    {{ $t('movie.rateMovie') }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import api from '../services/api'

export default {
  name: 'Home',
  computed: {
    ...mapState(['movies', 'loading', 'user'])
  },
  
  async created() {
    await this.fetchMovies(this.$i18n.locale)
  },
  
  watch: {
    '$i18n.locale'(newLocale) {
      this.fetchMovies(newLocale)
    }
  },
  
  methods: {
    ...mapActions(['fetchMovies']),
    
    goToMovie(movieId) {
      this.$router.push(`/movie/${movieId}`)
    },
    
    goToMovieWithRating(movieId) {
      this.$router.push({
        path: `/movie/${movieId}`,
        query: { openRating: 'true' }
      })
    },
    
    redirectToLogin() {
      this.$router.push({
        path: '/login',
        query: { redirect: this.$route.fullPath }
      })
    },
    
    async addToWatchlist(movieId) {
      try {
        await api.post(`/movies/${movieId}/watchlist`)
        alert('Added to watchlist!')
      } catch (error) {
        console.error('Error adding to watchlist:', error)
        let errorMessage = 'Failed to add to watchlist'
        
        if (error.response?.status === 400) {
          errorMessage = 'Movie already in your watchlist'
        } else if (error.response?.status === 401) {
          errorMessage = 'Please log in to add movies to your watchlist'
        } else if (error.response?.status === 404) {
          errorMessage = 'Movie not found'
        } else if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail
        }
        
        alert(errorMessage)
      }
    },
    
    truncateSummary(summary) {
      if (!summary) return this.$t('common.noSummary')
      return summary.length > 120 ? summary.substring(0, 120) + '...' : summary
    }
  }
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background-color: #121212;
}

.hero-section {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  padding: 4rem 0;
  text-align: center;
}

.hero-section h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #f5c518;
}

.hero-section p {
  font-size: 1.2rem;
  color: #ccc;
}

.movies-section {
  padding: 3rem 0;
}

.section-header {
  margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 2rem;
  color: #fff;
}

.loading {
  text-align: center;
  color: #ccc;
  font-size: 1.2rem;
  padding: 2rem;
}

.movies-horizontal-scroll {
  display: flex;
  overflow-x: auto;
  gap: 1.5rem;
  padding: 1rem 0;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}

.movies-horizontal-scroll::-webkit-scrollbar {
  height: 8px;
}

.movies-horizontal-scroll::-webkit-scrollbar-track {
  background: #333;
  border-radius: 4px;
}

.movies-horizontal-scroll::-webkit-scrollbar-thumb {
  background: #f5c518;
  border-radius: 4px;
}

.movies-horizontal-scroll::-webkit-scrollbar-thumb:hover {
  background: #e6b800;
}

.movie-card {
  background-color: #1e1e1e;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  flex: 0 0 280px;
  width: 280px;
}

.movie-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .hero-section {
    padding: 2.5rem 0;
  }
  
  .hero-section h1 {
    font-size: 2.5rem;
  }
  
  .hero-section p {
    font-size: 1.1rem;
  }
  
  .movies-section {
    padding: 2rem 0;
  }
  
  .section-header h2 {
    font-size: 1.75rem;
  }
  
  .movies-horizontal-scroll {
    gap: 1rem;
  }
  
  .movie-card {
    flex: 0 0 250px;
    width: 250px;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 2rem 0;
  }
  
  .hero-section h1 {
    font-size: 2rem;
  }
  
  .hero-section p {
    font-size: 1rem;
  }
  
  .movies-section {
    padding: 1.5rem 0;
  }
  
  .section-header h2 {
    font-size: 1.5rem;
  }
  
  .movies-horizontal-scroll {
    gap: 0.75rem;
  }
  
  .movie-card {
    flex: 0 0 180px;
    width: 180px;
  }
  
  .movie-image {
    height: 270px;
  }
  
  .action-btn {
    padding: 0.4rem 0.6rem;
    font-size: 0.7rem;
  }
  
  .movie-actions {
    gap: 0.4rem;
    margin-top: 0.75rem;
  }
  
  .loading {
    padding: 1.5rem;
    font-size: 1rem;
  }
}

.movie-image {
  position: relative;
  height: 375px;
  overflow: hidden;
}

.movie-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.movie-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.action-btn {
  flex: 1;
  padding: 0.5rem 0.75rem;
  border: none;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.watchlist-btn {
  background-color: #f5c518;
  color: #000;
}

.watchlist-btn:hover {
  background-color: #e6b800;
}

.rate-btn {
  background-color: transparent;
  color: #f5c518;
  border: 1px solid #f5c518;
}

.rate-btn:hover {
  background-color: #f5c518;
  color: #000;
}

.movie-info {
  padding: 1rem;
}

.movie-title {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  color: #fff;
}

.movie-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.movie-year {
  color: #ccc;
}

.movie-rating {
  color: #f5c518;
  font-weight: bold;
}

.movie-summary {
  font-size: 0.85rem;
  color: #aaa;
  line-height: 1.4;
}
</style>