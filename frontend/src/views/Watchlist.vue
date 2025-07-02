<template>
  <div class="watchlist-page">
    <div class="container">
      <h1>{{ $t('watchlist.title') }}</h1>
      
      <div v-if="loading" class="loading">
        {{ $t('watchlist.loading') }}
      </div>
      
      <div v-else-if="validWatchlistItems.length === 0" class="empty-watchlist">
        <h2>{{ $t('watchlist.empty') }}</h2>
        <p>{{ $t('watchlist.emptyMessage') }}</p>
        <router-link to="/" class="browse-btn">{{ $t('watchlist.browseMovies') }}</router-link>
      </div>
      
      <div v-else class="watchlist-grid">
        <div
          v-for="item in validWatchlistItems"
          :key="item.id"
          class="watchlist-item"
        >
          <div class="movie-card" @click="goToMovie(item.movie.id)">
            <div class="movie-image">
              <img :src="item.movie.image_url || '/placeholder-movie.jpg'" :alt="item.movie.title" />
            </div>
            
            <div class="movie-info">
              <h3>{{ item.movie.title }}</h3>
              <div class="movie-meta">
                <span class="year">{{ item.movie.release_year }}</span>
                <span class="rating">⭐ {{ item.movie.imdb_score || 'No ratings' }}</span>
              </div>
              <p class="summary">{{ truncateSummary(item.movie.summary) }}</p>
              <p class="added-date">{{ $t('watchlist.addedDate') }} {{ formatDate(item.added_at) }}</p>
            </div>
          </div>
          
          <button @click="removeFromWatchlist(item.id)" class="remove-btn">
            {{ $t('watchlist.removeButton') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'Watchlist',
  data() {
    return {
      watchlist: [],
      loading: false
    }
  },
  
  computed: {
    validWatchlistItems() {
      return this.watchlist.filter(item => item.movie)
    }
  },
  
  async created() {
    await this.fetchWatchlist()
  },
  
  methods: {
    async fetchWatchlist() {
      this.loading = true
      
      try {
        const response = await api.get('/me/watchlist')
        this.watchlist = response.data
      } catch (error) {
        console.error('Error fetching watchlist:', error)
        this.watchlist = []
      } finally {
        this.loading = false
      }
    },
    
    goToMovie(movieId) {
      this.$router.push(`/movie/${movieId}`)
    },
    
    async removeFromWatchlist(watchlistId) {
      try {
        await api.delete(`/watchlist/${watchlistId}`)
        this.watchlist = this.watchlist.filter(item => item.id !== watchlistId)
        alert('Removed from watchlist!')
      } catch (error) {
        console.error('Error removing from watchlist:', error)
        let errorMessage = 'Failed to remove from watchlist'
        
        if (error.response?.status === 401) {
          errorMessage = 'Please log in to manage your watchlist'
        } else if (error.response?.status === 404) {
          errorMessage = 'Item not found in your watchlist'
        } else if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail
        }
        
        alert(errorMessage)
      }
    },
    
    truncateSummary(summary) {
      if (!summary) return this.$t('common.noSummary')
      return summary.length > 120 ? summary.substring(0, 120) + '...' : summary
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.watchlist-page {
  min-height: 100vh;
  background-color: #121212;
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

h1 {
  color: #f5c518;
  margin-bottom: 2rem;
  font-size: 2.5rem;
}

.loading {
  text-align: center;
  color: #ccc;
  padding: 3rem;
  font-size: 1.2rem;
}

.empty-watchlist {
  text-align: center;
  padding: 3rem;
}

.empty-watchlist h2 {
  color: #fff;
  margin-bottom: 1rem;
}

.empty-watchlist p {
  color: #ccc;
  margin-bottom: 2rem;
}

.browse-btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background-color: #f5c518;
  color: #000;
  text-decoration: none;
  border-radius: 4px;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.browse-btn:hover {
  background-color: #e6b800;
}

.watchlist-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.watchlist-item {
  background-color: #1e1e1e;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.watchlist-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .watchlist-page {
    padding: 1.5rem 0;
  }
  
  h1 {
    font-size: 2rem;
  }
  
  .watchlist-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
  }
  
  .empty-watchlist {
    padding: 2rem;
  }
  
  .empty-watchlist h2 {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .watchlist-page {
    padding: 1rem 0;
  }
  
  h1 {
    font-size: 1.75rem;
    margin-bottom: 1.5rem;
  }
  
  .watchlist-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .movie-image {
    height: 300px;
  }
  
  .movie-info {
    padding: 0.75rem;
  }
  
  .movie-info h3 {
    font-size: 1.1rem;
  }
  
  .movie-meta {
    font-size: 0.85rem;
    flex-direction: column;
    gap: 0.25rem;
    text-align: center;
  }
  
  .summary {
    font-size: 0.85rem;
  }
  
  .added-date {
    font-size: 0.75rem;
  }
  
  .remove-btn {
    padding: 0.6rem;
    font-size: 0.9rem;
  }
  
  .empty-watchlist {
    padding: 1.5rem;
  }
  
  .empty-watchlist h2 {
    font-size: 1.25rem;
  }
  
  .empty-watchlist p {
    font-size: 0.9rem;
  }
  
  .browse-btn {
    padding: 0.6rem 1.25rem;
    font-size: 0.9rem;
  }
}

.movie-card {
  cursor: pointer;
}

.movie-image {
  height: 400px;
  overflow: hidden;
}

.movie-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.movie-info {
  padding: 1rem;
}

.movie-info h3 {
  color: #f5c518;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
}

.movie-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.year {
  color: #ccc;
}

.rating {
  color: #f5c518;
  font-weight: bold;
}

.summary {
  color: #aaa;
  line-height: 1.4;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.added-date {
  color: #666;
  font-size: 0.8rem;
  font-style: italic;
}

.remove-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #dc3545;
  color: white;
  border: none;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.remove-btn:hover {
  background-color: #c82333;
}
</style>