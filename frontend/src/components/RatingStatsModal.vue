<template>
  <div v-if="show" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>{{ $t('movie.ratingDistribution') }}</h3>
        <button @click="closeModal" class="close-btn">×</button>
      </div>
      
      <div v-if="loading" class="loading">
        {{ $t('movie.loadingStats') }}
      </div>
      
      <div v-else-if="stats" class="stats-content">
        <!-- Country Distribution Chart -->
        <div class="chart-section">
          <h4>{{ $t('movie.ratingByCountry') }}</h4>
          <div v-if="stats.country_distribution.length > 0" class="bar-chart">
            <div 
              v-for="item in stats.country_distribution" 
              :key="item.country"
              class="bar-item"
            >
              <div class="bar-info">
                <span class="country-name">{{ item.country }}</span>
                <span class="rating-info">{{ item.average_rating }} ⭐ ({{ item.rating_count }})</span>
              </div>
              <div class="bar-container">
                <div 
                  class="bar-fill"
                  :style="{ width: getBarWidth(item.average_rating) + '%' }"
                ></div>
              </div>
            </div>
          </div>
          <div v-else class="no-data">
            {{ $t('movie.noCountryData') }}
          </div>
        </div>
        
        <!-- Ratings and Comments -->
        <div class="ratings-section">
          <h4>{{ $t('movie.allRatingsAndComments') }} ({{ stats.total_ratings }})</h4>
          <div v-if="stats.ratings.length > 0" class="ratings-list">
            <div 
              v-for="rating in stats.ratings" 
              :key="rating.id"
              class="rating-item"
            >
              <div class="rating-header">
                <span class="user-info">
                  {{ rating.user.email }}
                  <span v-if="rating.user.country" class="user-country">({{ rating.user.country }})</span>
                </span>
                <span class="rating-score">⭐ {{ rating.rating }}/10</span>
              </div>
              <p v-if="rating.comment" class="rating-comment">{{ rating.comment }}</p>
              <div class="rating-date">{{ formatDate(rating.created_at) }}</div>
            </div>
          </div>
          <div v-else class="no-data">
            {{ $t('movie.noRatings') }}
          </div>
        </div>
      </div>
      
      <div v-else class="error">
        {{ $t('movie.errorLoadingStats') }}
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'RatingStatsModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    movieId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      stats: null,
      loading: false,
      error: false
    }
  },
  watch: {
    show(newValue) {
      if (newValue) {
        this.fetchStats()
      }
    }
  },
  methods: {
    async fetchStats() {
      this.loading = true
      this.error = false
      
      try {
        const response = await api.get(`/movies/${this.movieId}/rating-stats`)
        this.stats = response.data
      } catch (error) {
        console.error('Error fetching rating stats:', error)
        this.error = true
      } finally {
        this.loading = false
      }
    },
    
    closeModal() {
      this.$emit('close')
    },
    
    getBarWidth(rating) {
      // Convert rating (0-10) to percentage (0-100)
      return (rating / 10) * 100
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
  border-radius: 8px;
  max-width: 800px;
  width: 95%;
  max-height: 90vh;
  overflow-y: auto;
  margin: 1rem;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #333;
}

.modal-header h3 {
  color: #f5c518;
  margin: 0;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  color: #ccc;
  font-size: 2rem;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #fff;
}

.loading, .error {
  text-align: center;
  padding: 3rem;
  color: #ccc;
  font-size: 1.1rem;
}

.error {
  color: #dc3545;
}

.stats-content {
  padding: 2rem;
}

.chart-section, .ratings-section {
  margin-bottom: 2rem;
}

.chart-section h4, .ratings-section h4 {
  color: #f5c518;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.bar-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.bar-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.country-name {
  color: #fff;
  font-weight: bold;
}

.rating-info {
  color: #f5c518;
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

.ratings-list {
  max-height: 400px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.rating-item {
  background-color: #2a2a2a;
  padding: 1rem;
  border-radius: 6px;
  border-left: 3px solid #f5c518;
}

.rating-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.user-info {
  color: #f5c518;
  font-weight: bold;
}

.user-country {
  color: #ccc;
  font-weight: normal;
  font-size: 0.85rem;
}

.rating-score {
  color: #f5c518;
  font-weight: bold;
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

.no-data {
  text-align: center;
  color: #666;
  padding: 1.5rem;
  font-style: italic;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .modal-content {
    width: 98%;
    margin: 0.5rem;
  }
  
  .modal-header {
    padding: 1rem;
  }
  
  .stats-content {
    padding: 1rem;
  }
  
  .bar-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
  
  .rating-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
}
</style>