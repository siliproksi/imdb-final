<template>
  <div class="search-page">
    <div class="container">
      <h1>{{ $t('search.title') }}</h1>
      <p class="search-query">{{ $t('search.resultsFor') }} "{{ $route.query.q }}"</p>
      
      <div v-if="loading" class="loading">
        {{ $t('search.searching') }}
      </div>
      
      <div v-else>
        <div v-if="results.movies && results.movies.length > 0" class="search-section">
          <h2>{{ $t('search.movies') }}</h2>
          <div class="results-grid">
            <div
              v-for="movie in results.movies"
              :key="movie.id"
              class="result-item"
              @click="goToMovie(movie.id)"
            >
              <img :src="movie.image_url || '/placeholder-movie.jpg'" :alt="movie.title" />
              <div class="result-info">
                <h3>{{ movie.title }}</h3>
                <p class="year">{{ movie.release_year }}</p>
                <p class="rating">⭐ {{ movie.imdb_score || 'No ratings' }}</p>
                <p class="summary">{{ truncateText(movie.summary) }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="results.actors && results.actors.length > 0" class="search-section">
          <h2>{{ $t('search.actors') }}</h2>
          <div class="results-grid">
            <div
              v-for="actor in results.actors"
              :key="actor.id"
              class="result-item"
              @click="goToActor(actor.id)"
            >
              <img :src="actor.photo_url || '/placeholder-actor.jpg'" :alt="actor.name" />
              <div class="result-info">
                <h3>{{ actor.name }}</h3>
                <p class="bio">{{ truncateText(actor.bio) }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="(!results.movies || results.movies.length === 0) && (!results.actors || results.actors.length === 0)" class="no-results">
          <h2>{{ $t('search.noResults') }}</h2>
          <p>{{ $t('search.tryDifferent') }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'Search',
  data() {
    return {
      results: {
        movies: [],
        actors: []
      },
      loading: false
    }
  },
  
  async created() {
    await this.performSearch()
  },
  
  watch: {
    '$route.query': {
      handler() {
        this.performSearch()
      },
      deep: true
    }
  },
  
  methods: {
    async performSearch() {
      const query = this.$route.query.q
      const searchType = this.$route.query.type || 'all'
      
      if (!query) {
        this.$router.push('/')
        return
      }
      
      this.loading = true
      
      try {
        const response = await api.get('/search', {
          params: {
            q: query,
            search_type: searchType,
            limit: 20
          }
        })
        
        this.results = response.data
      } catch (error) {
        console.error('Search error:', error)
        this.results = { movies: [], actors: [] }
      } finally {
        this.loading = false
      }
    },
    
    goToMovie(movieId) {
      this.$router.push(`/movie/${movieId}`)
    },
    
    goToActor(actorId) {
      this.$router.push(`/actor/${actorId}`)
    },
    
    truncateText(text) {
      if (!text) return this.$t('common.noDescription')
      return text.length > 150 ? text.substring(0, 150) + '...' : text
    }
  }
}
</script>

<style scoped>
.search-page {
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
  margin-bottom: 0.5rem;
}

.search-query {
  color: #ccc;
  margin-bottom: 2rem;
  font-style: italic;
}

.loading {
  text-align: center;
  color: #ccc;
  padding: 3rem;
  font-size: 1.2rem;
}

.search-section {
  margin-bottom: 3rem;
}

.search-section h2 {
  color: #fff;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #f5c518;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.result-item {
  display: flex;
  background-color: #1e1e1e;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.result-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.result-item img {
  width: 120px;
  height: 180px;
  object-fit: cover;
  flex-shrink: 0;
}

.result-info {
  padding: 1rem;
  flex: 1;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .search-page {
    padding: 1.5rem 0;
  }
  
  .results-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .result-item {
    flex-direction: column;
  }
  
  .result-item img {
    width: 100%;
    height: 200px;
  }
  
  .result-info {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .search-page {
    padding: 1rem 0;
  }
  
  h1 {
    font-size: 1.75rem;
  }
  
  .results-grid {
    gap: 1rem;
  }
  
  .result-item img {
    height: 150px;
  }
  
  .result-info {
    padding: 0.75rem;
  }
  
  .result-info h3 {
    font-size: 1rem;
  }
  
  .year,
  .rating,
  .bio {
    font-size: 0.85rem;
  }
  
  .summary,
  .bio {
    font-size: 0.9rem;
  }
}

.result-info h3 {
  color: #f5c518;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.year,
.rating,
.bio {
  color: #ccc;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.rating {
  color: #f5c518 !important;
}

.summary,
.bio {
  color: #aaa;
  line-height: 1.4;
}

.no-results {
  text-align: center;
  padding: 3rem;
}

.no-results h2 {
  color: #f5c518;
  margin-bottom: 1rem;
}

.no-results p {
  color: #ccc;
}
</style>