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
              <span class="rating">⭐ {{ movie.imdb_score || 'N/A' }}</span>
            </div>
            
            <p class="movie-summary">{{ movie.summary }}</p>
            
            <div class="movie-actions">
              <button v-if="!user" @click="redirectToLogin" class="action-btn primary">
                Rate Movie
              </button>
              <button v-else @click="showRatingModal = true" class="action-btn primary">
                Rate Movie
              </button>
              
              <button v-if="!user" @click="redirectToLogin" class="action-btn secondary">
                Add to Watchlist
              </button>
              <button v-else @click="addToWatchlist" class="action-btn secondary">
                Add to Watchlist
              </button>
            </div>
            
            <div class="movie-stats">
              <div class="stat">
                <h3>{{ movie.average_rating?.toFixed(1) || 'N/A' }}</h3>
                <p>Average Rating</p>
              </div>
              <div class="stat">
                <h3>{{ movie.total_ratings || 0 }}</h3>
                <p>Total Ratings</p>
              </div>
              <div class="stat">
                <h3>{{ movie.popularity_score?.toFixed(0) || 0 }}</h3>
                <p>Popularity Score</p>
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
            <h3>Trailer</h3>
            <div class="trailer-container">
              <iframe 
                :src="getYouTubeEmbedUrl(movie.trailer_url)"
                frameborder="0"
                allowfullscreen
              ></iframe>
            </div>
          </div>
          
          <div class="cast-section" v-if="movie.actors && movie.actors.length > 0">
            <h3>Cast</h3>
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
          
          <div class="ratings-section">
            <h3>User Ratings & Comments</h3>
            <div v-if="movie.ratings && movie.ratings.length > 0" class="ratings-list">
              <div v-for="rating in movie.ratings" :key="rating.id" class="rating-item">
                <div class="rating-header">
                  <span class="user-email">{{ rating.user.email }}</span>
                  <span class="rating-score">⭐ {{ rating.rating }}/10</span>
                </div>
                <p v-if="rating.comment" class="rating-comment">{{ rating.comment }}</p>
              </div>
            </div>
            <div v-else class="no-ratings">
              <p>No ratings yet. Be the first to rate this movie!</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Rating Modal -->
    <div v-if="showRatingModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h3>Rate Movie</h3>
        <form @submit.prevent="submitRating">
          <div class="form-group">
            <label>Rating (1-10)</label>
            <input v-model.number="ratingForm.rating" type="number" min="1" max="10" step="0.1" required />
          </div>
          <div class="form-group">
            <label>Comment (Optional)</label>
            <textarea v-model="ratingForm.comment" rows="4"></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" @click="closeModal" class="btn-cancel">Cancel</button>
            <button type="submit" class="btn-submit">Submit Rating</button>
          </div>
        </form>
      </div>
    </div>
  </div>
  
  <div v-else class="loading">
    Loading movie details...
  </div>
</template>

<script>
import { mapState } from 'vuex'
import api from '../services/api'

export default {
  name: 'MovieDetail',
  data() {
    return {
      movie: null,
      showRatingModal: false,
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
  },
  
  methods: {
    async fetchMovie() {
      try {
        const response = await api.get(`/movies/${this.$route.params.id}`)
        this.movie = response.data
      } catch (error) {
        console.error('Error fetching movie:', error)
        this.$router.push('/')
      }
    },
    
    formatDuration(minutes) {
      if (!minutes) return 'N/A'
      const hours = Math.floor(minutes / 60)
      const mins = minutes % 60
      return `${hours}h ${mins}m`
    },
    
    getYouTubeEmbedUrl(url) {
      const videoId = url.split('v=')[1]?.split('&')[0]
      return `https://www.youtube.com/embed/${videoId}`
    },
    
    redirectToLogin() {
      this.$router.push('/login')
    },
    
    async addToWatchlist() {
      try {
        await api.post(`/movies/${this.movie.id}/watchlist`)
        alert('Added to watchlist!')
      } catch (error) {
        console.error('Error adding to watchlist:', error)
        alert('Failed to add to watchlist')
      }
    },
    
    closeModal() {
      this.showRatingModal = false
      this.ratingForm = { rating: 5, comment: '' }
    },
    
    async submitRating() {
      try {
        await api.post(`/movies/${this.movie.id}/rate`, this.ratingForm)
        alert('Rating submitted!')
        this.closeModal()
        await this.fetchMovie() // Refresh movie data
      } catch (error) {
        console.error('Error submitting rating:', error)
        alert('Failed to submit rating')
      }
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

.rating-comment {
  color: #ddd;
  line-height: 1.4;
}

.no-ratings {
  text-align: center;
  color: #ccc;
  padding: 2rem;
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
  .movie-hero-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .movie-stats {
    grid-template-columns: 1fr;
  }
}
</style>