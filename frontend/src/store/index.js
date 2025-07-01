import { createStore } from 'vuex'
import api from '../services/api'

export default createStore({
  state: {
    user: null,
    token: localStorage.getItem('token'),
    movies: [],
    loading: false
  },
  
  mutations: {
    SET_USER(state, user) {
      state.user = user
    },
    
    SET_TOKEN(state, token) {
      state.token = token
      if (token) {
        localStorage.setItem('token', token)
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`
      } else {
        localStorage.removeItem('token')
        delete api.defaults.headers.common['Authorization']
      }
    },
    
    SET_MOVIES(state, movies) {
      state.movies = movies
    },
    
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    
    LOGOUT(state) {
      state.user = null
      state.token = null
      localStorage.removeItem('token')
      delete api.defaults.headers.common['Authorization']
    }
  },
  
  actions: {
    async login({ commit }, credentials) {
      try {
        commit('SET_LOADING', true)
        const response = await api.post('/login', credentials)
        const { access_token, user } = response.data
        
        commit('SET_TOKEN', access_token)
        commit('SET_USER', user)
        
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          message: error.response?.data?.detail || 'Login failed' 
        }
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async register({ commit }, userData) {
      try {
        commit('SET_LOADING', true)
        await api.post('/register', userData)
        return { success: true }
      } catch (error) {
        return { 
          success: false, 
          message: error.response?.data?.detail || 'Registration failed' 
        }
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchMovies({ commit }) {
      try {
        commit('SET_LOADING', true)
        const response = await api.get('/movies')
        commit('SET_MOVIES', response.data)
      } catch (error) {
        console.error('Error fetching movies:', error)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    logoutUser({ commit }) {
      commit('LOGOUT')
    }
  },
  
  getters: {
    isAuthenticated: state => !!state.token,
    currentUser: state => state.user
  }
})