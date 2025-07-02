<template>
  <div class="actor-detail" v-if="actor">
    <div class="actor-hero">
      <div class="container">
        <div class="actor-hero-content">
          <div class="actor-photo">
            <img :src="actor.photo_url || '/placeholder-actor.jpg'" :alt="actor.name" />
          </div>
          
          <div class="actor-info">
            <h1>{{ actor.name }}</h1>
            <div class="actor-bio">
              <p v-if="actor.bio">{{ actor.bio }}</p>
              <p v-else class="no-bio">{{ $t('actor.noBio') }}</p>
            </div>
            
            <div class="actor-movies" v-if="actor.movies && actor.movies.length > 0">
              <h3>{{ $t('actor.appearsIn') }}</h3>
              <div class="movies-list">
                <div 
                  v-for="movieActor in actor.movies" 
                  :key="movieActor.movie.id"
                  class="movie-item"
                  @click="goToMovie(movieActor.movie.id)"
                >
                  <img :src="movieActor.movie.image_url || '/placeholder-movie.jpg'" :alt="movieActor.movie.title" />
                  <div class="movie-info">
                    <h4>{{ movieActor.movie.title }}</h4>
                    <p class="character">as {{ movieActor.character_name || 'Unknown Character' }}</p>
                    <p class="year">{{ movieActor.movie.release_year }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <div v-else class="loading">
    {{ $t('actor.loading') }}
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'ActorDetail',
  data() {
    return {
      actor: null
    }
  },
  
  async created() {
    await this.fetchActor()
  },
  
  methods: {
    async fetchActor() {
      try {
        const response = await api.get(`/actors/${this.$route.params.id}`)
        this.actor = response.data
      } catch (error) {
        console.error('Error fetching actor:', error)
        this.$router.push('/')
      }
    },
    
    goToMovie(movieId) {
      this.$router.push(`/movie/${movieId}`)
    }
  }
}
</script>

<style scoped>
.actor-detail {
  min-height: 100vh;
  background-color: #121212;
}

.actor-hero {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  padding: 3rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.actor-hero-content {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 3rem;
  align-items: start;
}

.actor-photo img {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.actor-info h1 {
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
  color: #f5c518;
}

.actor-bio {
  margin-bottom: 2rem;
}

.actor-bio p {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #ddd;
}

.no-bio {
  color: #aaa;
  font-style: italic;
}

.actor-movies h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #f5c518;
}

.movies-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.movie-item {
  display: flex;
  background-color: #1e1e1e;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.movie-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.movie-item img {
  width: 80px;
  height: 120px;
  object-fit: cover;
  flex-shrink: 0;
}

.movie-info {
  padding: 1rem;
  flex: 1;
}

.movie-info h4 {
  color: #f5c518;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.character {
  color: #ccc;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.year {
  color: #aaa;
  font-size: 0.8rem;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50vh;
  font-size: 1.2rem;
  color: #ccc;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .actor-hero {
    padding: 2rem 0;
  }
  
  .actor-hero-content {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 2rem;
  }
  
  .actor-photo img {
    max-width: 250px;
    margin: 0 auto;
  }
  
  .actor-info h1 {
    font-size: 2rem;
  }
  
  .movies-list {
    grid-template-columns: 1fr;
  }
  
  .movie-item {
    flex-direction: column;
  }
  
  .movie-item img {
    width: 100%;
    height: 200px;
  }
}

@media (max-width: 480px) {
  .actor-hero {
    padding: 1.5rem 0;
  }
  
  .actor-hero-content {
    gap: 1.5rem;
  }
  
  .actor-photo img {
    max-width: 200px;
  }
  
  .actor-info h1 {
    font-size: 1.75rem;
  }
  
  .actor-bio p {
    font-size: 1rem;
  }
  
  .movie-item img {
    height: 150px;
  }
  
  .movie-info {
    padding: 0.75rem;
  }
  
  .movie-info h4 {
    font-size: 0.9rem;
  }
  
  .character,
  .year {
    font-size: 0.8rem;
  }
}
</style>