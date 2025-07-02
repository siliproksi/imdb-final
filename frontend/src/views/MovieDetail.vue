<template>
  <div class="movie-detail" v-if="movie">
    <div class="movie-hero">
      <div class="container">
        <div class="movie-hero-content">
          <div class="movie-poster">
            <img :src="movie.image_url || '/placeholder-movie.jpg'" :alt="movie.title" />
          </div>
          
          <div class="movie-info">
            <h1>{{ movie.title }}</h1>
            <div class="movie-meta">
              <span class="year">{{ movie.release_year }}</span>
              <span class="duration">{{ formatDuration(movie.duration) }}</span>
              <span class="rating">⭐ {{ movie.imdb_score || 'No ratings' }}</span>
            </div>
            
            <p class="movie-summary">{{ movie.summary }}</p>
            
            <div class="movie-actions">
              <button v-if="!user" @click="redirectToLogin" class="action-btn primary">
                {{ $t('movie.rateMovie') }}
              </button>
              <button v-else @click="showRatingModal = true" class="action-btn primary">
                {{ $t('movie.rateMovie') }}
              </button>
              
              <button v-if="!user" @click="redirectToLogin" class="action-btn secondary">
                {{ $t('movie.addToWatchlist') }}
              </button>
              <button v-else @click="addToWatchlist" class="action-btn secondary">
                {{ $t('movie.addToWatchlist') }}
              </button>
            </div>
            
            <div class="movie-stats">
              <div class="stat clickable-stat" @click="showRatingStats">
                <h3>{{ movie.average_rating?.toFixed(1) || 'No ratings' }}</h3>
                <p>{{ $t('movie.averageRating') }}</p>
              </div>
              <div class="stat">
                <h3>{{ movie.total_ratings || 0 }}</h3>
                <p>{{ $t('movie.totalRatings') }}</p>
              </div>
              <div class="stat">
                <h3>{{ movie.popularity_score?.toFixed(0) || 0 }}</h3>
                <p>{{ $t('movie.popularityScore') }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="movie-details-section">
      <div class="container">
        <div class="details-grid">
          <div class="trailer-section" v-if="movie.trailer_url">
            <h3>{{ $t('movie.trailer') }}</h3>
            <div class="trailer-container">
              <iframe 
                :src="getYouTubeEmbedUrl(movie.trailer_url)"
                frameborder="0"
                allowfullscreen
              ></iframe>
            </div>
          </div>
          
          <div class="cast-section" v-if="movie.actors && movie.actors.length > 0">
            <h3>{{ $t('movie.cast') }}</h3>
            <div class="cast-grid">
              <div v-for="actor in movie.actors" :key="actor.actor.id" class="cast-member">
                <img :src="actor.actor.photo_url || '/placeholder-actor.jpg'" :alt="actor.actor.name" />
                <div class="cast-info">
                  <h4>{{ actor.actor.name }}</h4>
                  <p>{{ actor.character_name }}</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- User Ratings & Comments -->
          <div v-if="ratingStats && ratingStats.total_ratings > 0" class="rating-stats-section">
            <div class="stats-header">
              <h3>{{ $t('movie.userRatings') }}</h3>
              <div class="country-filter">
                <label>{{ $t('movie.filterByCountry') }}:</label>
                <select v-model="selectedCountry" @change="onCountryChange" class="country-select">
                  <option v-for="country in ratingStats.available_countries" :key="country" :value="country">
                    {{ getLocalizedCountry(country) }}
                  </option>
                </select>
              </div>
            </div>
            
            <div class="rating-histogram">
              <div 
                v-for="item in ratingStats.rating_distribution" 
                :key="item.rating"
                class="histogram-bar"
              >
                <div class="bar-label">
                  <span class="star-rating">{{ item.rating }} ⭐</span>
                  <span class="percentage">{{ item.percentage }}%</span>
                  <span class="count">({{ item.count }})</span>
                </div>
                <div class="bar-container">
                  <div 
                    class="bar-fill"
                    :style="{ width: item.percentage + '%' }"
                  ></div>
                </div>
              </div>
            </div>
            
            <!-- Comments List (filtered by same country) -->
            <div v-if="ratingStats.ratings && ratingStats.ratings.length > 0" class="ratings-list">
              <div v-for="rating in ratingStats.ratings" :key="rating.id" class="rating-item">
                <div class="rating-header">
                  <span class="user-email">{{ rating.user.email }}</span>
                  <span v-if="rating.user.country" class="user-country">({{ getLocalizedCountry(rating.user.country) }})</span>
                  <span class="rating-score">⭐ {{ rating.rating }}/10</span>
                </div>
                <p v-if="rating.comment" class="rating-comment">{{ rating.comment }}</p>
                <div class="rating-date">{{ formatDate(rating.created_at) }}</div>
              </div>
            </div>
            <div v-else class="no-ratings">
              <p>{{ $t('movie.noRatings') }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Rating Modal -->
    <div v-if="showRatingModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h3>{{ $t('movie.rateMovie') }}</h3>
        <form @submit.prevent="submitRating">
          <div class="form-group">
            <label>{{ $t('movie.rating') }}</label>
            <input v-model.number="ratingForm.rating" type="number" min="1" max="10" step="0.1" required />
          </div>
          <div class="form-group">
            <label>{{ $t('movie.comment') }}</label>
            <textarea v-model="ratingForm.comment" rows="4"></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" @click="closeModal" class="btn-cancel">{{ $t('movie.cancel') }}</button>
            <button type="submit" class="btn-submit">{{ $t('movie.submitRating') }}</button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- Rating Statistics Modal -->
    <RatingStatsModal 
      :show="showStatsModal" 
      :movie-id="movie.id" 
      @close="showStatsModal = false"
    />
  </div>
  
  <div v-else class="loading">
    {{ $t('movie.loading') }}
  </div>
</template>

<script>
import { mapState } from 'vuex'
import api from '../services/api'
import RatingStatsModal from '../components/RatingStatsModal.vue'
import countryMixin from '../mixins/countryMixin'

export default {
  name: 'MovieDetail',
  mixins: [countryMixin],
  components: {
    RatingStatsModal
  },
  data() {
    return {
      movie: null,
      ratingStats: null,
      selectedCountry: 'All',
      showRatingModal: false,
      showStatsModal: false,
      ratingForm: {
        rating: 5,
        comment: ''
      }
    }
  },
  
  computed: {
    ...mapState(['user'])
  },
  
  async created() {
    await this.fetchMovie()
    await this.fetchRatingStats()
    
    // Check if we should open rating modal immediately
    if (this.$route.query.openRating === 'true') {
      this.showRatingModal = true
    }
  },
  
  watch: {
    '$i18n.locale'() {
      this.fetchMovie()
      this.fetchRatingStats()
    }
  },
  
  methods: {
    async fetchMovie() {
      try {
        const response = await api.get(`/movies/${this.$route.params.id}`, {
          params: { lang: this.$i18n.locale }
        })
        this.movie = response.data
      } catch (error) {
        console.error('Error fetching movie:', error)
        this.$router.push('/')
      }
    },
    
    async fetchRatingStats(country = 'All') {
      try {
        const response = await api.get(`/movies/${this.$route.params.id}/rating-stats`, {
          params: { country: country }
        })
        this.ratingStats = response.data
        this.selectedCountry = response.data.selected_country
      } catch (error) {
        console.error('Error fetching rating stats:', error)
      }
    },
    
    formatDuration(minutes) {
      if (!minutes) return 'No duration'
      const hours = Math.floor(minutes / 60)
      const mins = minutes % 60
      return `${hours}h ${mins}m`
    },
    
    getYouTubeEmbedUrl(url) {
      const videoId = url.split('v=')[1]?.split('&')[0]
      return `https://www.youtube.com/embed/${videoId}`
    },
    
    redirectToLogin() {
      this.$router.push({
        path: '/login',
        query: { redirect: this.$route.fullPath }
      })
    },
    
    async addToWatchlist() {
      try {
        await api.post(`/movies/${this.movie.id}/watchlist`)
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
    
    closeModal() {
      this.showRatingModal = false
      this.ratingForm = { rating: 5, comment: '' }
    },
    
    async submitRating() {
      try {
        await api.post(`/movies/${this.movie.id}/rate`, this.ratingForm)
        alert('Rating submitted successfully!')
        this.closeModal()
        await this.fetchMovie() // Refresh movie data
      } catch (error) {
        console.error('Error submitting rating:', error)
        let errorMessage = 'Failed to submit rating'
        
        if (error.response?.status === 400) {
          errorMessage = 'Invalid rating. Please enter a rating between 1 and 10.'
        } else if (error.response?.status === 401) {
          errorMessage = 'Please log in to rate movies'
        } else if (error.response?.status === 404) {
          errorMessage = 'Movie not found'
        } else if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail
        }
        
        alert(errorMessage)
      }
    },
    
    showRatingStats() {
      this.showStatsModal = true
    },
    
    getBarWidth(rating) {
      // Convert rating (0-10) to percentage (0-100)
      return (rating / 10) * 100
    },
    
    async onCountryChange() {
      await this.fetchRatingStats(this.selectedCountry)
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString(this.$i18n.locale, {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }
  }
}
</script>

<style scoped>
.movie-detail {
  min-height: 100vh;
  background-color: #121212;
}

.movie-hero {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  padding: 3rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.movie-hero-content {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 3rem;
  align-items: start;
}

.movie-poster img {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.movie-info h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #f5c518;
}

.movie-meta {
  display: flex;
  gap: 2rem;
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
}

.movie-meta span {
  color: #ccc;
}

.rating {
  color: #f5c518 !important;
  font-weight: bold;
}

.movie-summary {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
  color: #ddd;
}

.movie-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.action-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn.primary {
  background-color: #f5c518;
  color: #000;
}

.action-btn.secondary {
  background-color: transparent;
  color: #f5c518;
  border: 2px solid #f5c518;
}

.action-btn:hover {
  transform: translateY(-2px);
}

.movie-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.stat {
  text-align: center;
}

.stat h3 {
  font-size: 2rem;
  color: #f5c518;
  margin-bottom: 0.5rem;
}

.stat p {
  color: #ccc;
}

.clickable-stat {
  cursor: pointer;
  transition: transform 0.2s ease, background-color 0.2s ease;
  border-radius: 8px;
  padding: 1rem;
}

.clickable-stat:hover {
  transform: translateY(-2px);
  background-color: rgba(245, 197, 24, 0.1);
}

.movie-details-section {
  padding: 3rem 0;
}

.details-grid {
  display: grid;
  gap: 3rem;
}

.details-grid h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #f5c518;
}

.trailer-container {
  position: relative;
  width: 100%;
  height: 0;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
}

.trailer-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.cast-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}

.cast-member {
  text-align: center;
}

.cast-member img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.cast-info h4 {
  color: #fff;
  margin-bottom: 0.25rem;
}

.cast-info p {
  color: #ccc;
  font-size: 0.9rem;
}

.ratings-list {
  max-height: 400px;
  overflow-y: auto;
}

.rating-item {
  background-color: #1e1e1e;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.rating-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.user-email {
  color: #f5c518;
  font-weight: bold;
}

.rating-score {
  color: #f5c518;
}

.user-country {
  color: #ccc;
  font-weight: normal;
  font-size: 0.85rem;
  margin-right: 0.5rem;
}

.rating-comment {
  color: #ddd;
  line-height: 1.4;
  margin: 0.5rem 0;
}

.rating-date {
  color: #888;
  font-size: 0.8rem;
}

.no-ratings {
  text-align: center;
  color: #ccc;
  padding: 2rem;
}

.rating-stats-section {
  margin-bottom: 3rem;
}

.stats-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.country-filter {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.country-filter label {
  color: #ccc;
  font-size: 0.9rem;
}

.country-select {
  background-color: #2a2a2a;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 0.5rem;
  font-size: 0.9rem;
}

.rating-histogram {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 2rem;
}

.histogram-bar {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.bar-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.star-rating {
  color: #f5c518;
  font-weight: bold;
  min-width: 50px;
}

.percentage {
  color: #fff;
  font-weight: bold;
}

.count {
  color: #ccc;
  font-size: 0.8rem;
}

.bar-container {
  height: 20px;
  background-color: #333;
  border-radius: 10px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #f5c518, #e6b800);
  border-radius: 10px;
  transition: width 0.3s ease;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50vh;
  font-size: 1.2rem;
  color: #ccc;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: #1e1e1e;
  padding: 2rem;
  border-radius: 8px;
  max-width: 500px;
  width: 100%;
  margin: 1rem;
}

.modal-content h3 {
  color: #f5c518;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #fff;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #555;
  border-radius: 4px;
  background-color: #2a2a2a;
  color: #fff;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.btn-cancel,
.btn-submit {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.btn-cancel {
  background-color: #666;
  color: #fff;
}

.btn-submit {
  background-color: #f5c518;
  color: #000;
}

@media (max-width: 768px) {
  .movie-hero {
    padding: 2rem 0;
  }
  
  .movie-hero-content {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 2rem;
  }
  
  .movie-poster img {
    max-width: 250px;
    margin: 0 auto;
  }
  
  .movie-info h1 {
    font-size: 2rem;
  }
  
  .movie-actions {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .action-btn {
    width: 100%;
    padding: 1rem;
  }
  
  .movie-stats {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .movie-details-section {
    padding: 2rem 0;
  }
  
  .cast-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }
  
  .cast-member img {
    height: 150px;
  }
  
  .modal-content {
    margin: 1rem;
    padding: 1.5rem;
  }
}

@media (max-width: 480px) {
  .movie-hero {
    padding: 1.5rem 0;
  }
  
  .movie-hero-content {
    gap: 1.5rem;
  }
  
  .movie-poster img {
    max-width: 200px;
  }
  
  .movie-info h1 {
    font-size: 1.75rem;
  }
  
  .movie-meta {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
  
  .movie-summary {
    font-size: 1rem;
  }
  
  .movie-stats {
    text-align: center;
  }
  
  .cast-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 0.75rem;
  }
  
  .cast-member img {
    height: 120px;
  }
  
  .cast-info h4 {
    font-size: 0.9rem;
  }
  
  .cast-info p {
    font-size: 0.8rem;
  }
  
  .rating-item {
    padding: 0.75rem;
  }
  
  .rating-header {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
  
  .stats-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .country-filter {
    width: 100%;
    justify-content: space-between;
  }
  
  .country-select {
    flex: 1;
    margin-left: 0.5rem;
  }
  
  .modal-content {
    margin: 0.5rem;
    padding: 1.25rem;
  }
  
  .modal-actions {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .btn-cancel,
  .btn-submit {
    width: 100%;
  }
}
</style>