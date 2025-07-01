<template>
  <div class="search-container">
    <div class="search-input-container">
      <select v-model="searchType" class="search-type">
        <option value="all">All</option>
        <option value="movies">Movies</option>
        <option value="actors">Actors</option>
      </select>
      
      <input
        v-model="searchQuery"
        @input="handleSearch"
        @focus="showDropdown = true"
        @blur="hideDropdown"
        type="text"
        placeholder="Search movies, actors..."
        class="search-input"
      />
      
      <button @click="performSearch" class="search-btn">Search</button>
    </div>
    
    <div v-if="showDropdown && searchResults.length > 0" class="search-dropdown">
      <div
        v-for="result in searchResults.slice(0, 3)"
        :key="result.id"
        @click="selectResult(result)"
        class="search-result-item"
      >
        <img v-if="result.image_url" :src="result.image_url" alt="" class="result-image" />
        <div class="result-info">
          <div class="result-title">{{ result.title || result.name }}</div>
          <div class="result-subtitle">{{ result.release_year || 'Actor' }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { debounce } from 'lodash'
import api from '../services/api'

export default {
  name: 'SearchBox',
  data() {
    return {
      searchQuery: '',
      searchType: 'all',
      searchResults: [],
      showDropdown: false
    }
  },
  methods: {
    handleSearch: debounce(function() {
      if (this.searchQuery.length >= 3) {
        this.searchMovies()
      } else {
        this.searchResults = []
      }
    }, 300),
    
    async searchMovies() {
      try {
        const response = await api.get('/search', {
          params: {
            q: this.searchQuery,
            search_type: this.searchType,
            limit: this.searchQuery.length === 3 ? 3 : 10
          }
        })
        
        this.searchResults = [
          ...response.data.movies,
          ...response.data.actors
        ]
      } catch (error) {
        console.error('Search error:', error)
      }
    },
    
    selectResult(result) {
      if (result.title) {
        // It's a movie
        this.$router.push(`/movie/${result.id}`)
      } else {
        // It's an actor
        this.$router.push(`/actor/${result.id}`)
      }
      this.showDropdown = false
      this.searchQuery = ''
    },
    
    performSearch() {
      if (this.searchQuery.length > 0) {
        this.$router.push({
          path: '/search',
          query: { q: this.searchQuery, type: this.searchType }
        })
        this.showDropdown = false
      }
    },
    
    hideDropdown() {
      setTimeout(() => {
        this.showDropdown = false
      }, 200)
    }
  }
}
</script>

<style scoped>
.search-container {
  position: relative;
  width: 100%;
}

.search-input-container {
  display: flex;
  border-radius: 4px;
  overflow: hidden;
  background-color: white;
}

.search-type {
  padding: 0.75rem;
  border: none;
  background-color: #f5f5f5;
  min-width: 80px;
}

.search-input {
  flex: 1;
  padding: 0.75rem;
  border: none;
  outline: none;
  color: #333;
}

.search-btn {
  padding: 0.75rem 1.5rem;
  background-color: #f5c518;
  border: none;
  cursor: pointer;
  font-weight: bold;
  color: #000;
}

.search-btn:hover {
  background-color: #e6b800;
}

.search-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: white;
  border: 1px solid #ddd;
  border-top: none;
  border-radius: 0 0 4px 4px;
  max-height: 300px;
  overflow-y: auto;
  z-index: 1000;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.search-result-item {
  display: flex;
  padding: 0.75rem;
  cursor: pointer;
  border-bottom: 1px solid #eee;
  color: #333;
}

.search-result-item:hover {
  background-color: #f5f5f5;
}

.result-image {
  width: 40px;
  height: 60px;
  object-fit: cover;
  margin-right: 0.75rem;
  border-radius: 4px;
}

.result-info {
  flex: 1;
}

.result-title {
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.result-subtitle {
  font-size: 0.9rem;
  color: #666;
}
</style>