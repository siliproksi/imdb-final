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
        let errorMessage = 'Login failed'
        
        if (error.response?.status === 401) {
          errorMessage = 'Invalid credentials. Please check your email and password.'
        } else if (error.response?.status === 422) {
          // Parse Pydantic validation errors
          if (error.response.data?.detail && Array.isArray(error.response.data.detail)) {
            const validationErrors = error.response.data.detail
            if (validationErrors.length > 0) {
              const firstError = validationErrors[0]
              if (firstError.msg) {
                let msg = firstError.msg
                // Clean up common validation messages
                if (msg.includes('Password must contain at least 1 non-alphanumeric character')) {
                  msg = 'Password must contain at least one special character (!@#$%^&* etc.)'
                } else if (msg.includes('Value error,')) {
                  msg = msg.replace('Value error, ', '')
                }
                errorMessage = msg
              } else {
                errorMessage = 'Please check your input and try again.'
              }
            }
          } else {
            errorMessage = 'Please enter a valid email address and password.'
          }
        } else if (error.response?.status === 429) {
          errorMessage = 'Too many login attempts. Please try again later.'
        } else if (error.response?.status === 500) {
          errorMessage = 'Server error. Please try again later.'
        } else if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail
        } else if (error.message) {
          errorMessage = error.message
        }
        
        return { 
          success: false, 
          message: errorMessage
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
        let errorMessage = 'Registration failed'
        
        if (error.response?.status === 400) {
          if (error.response.data?.detail?.includes('Email already registered')) {
            errorMessage = 'An account with this email already exists. Please use a different email or try logging in.'
          } else {
            errorMessage = error.response.data?.detail || 'Invalid registration data. Please check your information.'
          }
        } else if (error.response?.status === 422) {
          // Parse Pydantic validation errors
          if (error.response.data?.detail && Array.isArray(error.response.data.detail)) {
            const validationErrors = error.response.data.detail
            if (validationErrors.length > 0) {
              const firstError = validationErrors[0]
              if (firstError.msg) {
                let msg = firstError.msg
                // Clean up common validation messages
                if (msg.includes('Password must contain at least 1 non-alphanumeric character')) {
                  msg = 'Password must contain at least one special character (!@#$%^&* etc.)'
                } else if (msg.includes('Value error,')) {
                  msg = msg.replace('Value error, ', '')
                }
                errorMessage = msg
              } else {
                errorMessage = 'Please check your input and try again.'
              }
            }
          } else {
            errorMessage = 'Please fill in all required fields correctly.'
          }
        } else if (error.response?.status === 500) {
          errorMessage = 'Server error. Please try again later.'
        } else if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail
        } else if (error.message) {
          errorMessage = error.message
        }
        
        return { 
          success: false, 
          message: errorMessage
        }
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async googleLogin({ commit }, token) {
      try {
        commit('SET_LOADING', true)
        const response = await api.post('/auth/google', { token })
        const { access_token, user } = response.data
        
        commit('SET_TOKEN', access_token)
        commit('SET_USER', user)
        
        return { success: true }
      } catch (error) {
        let errorMessage = 'Google login failed'
        
        if (error.response?.status === 400) {
          errorMessage = 'Invalid Google authentication. Please try again.'
        } else if (error.response?.status === 401) {
          errorMessage = 'Google authentication failed. Please check your account permissions.'
        } else if (error.response?.status === 500) {
          errorMessage = 'Server error during Google login. Please try again later.'
        } else if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail
        } else if (error.message) {
          errorMessage = error.message
        }
        
        return { 
          success: false, 
          message: errorMessage
        }
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchMovies({ commit }, lang = 'en') {
      try {
        commit('SET_LOADING', true)
        const response = await api.get('/movies', {
          params: { lang }
        })
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