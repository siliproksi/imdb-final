import axios from 'axios'

const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token to requests if available
const token = localStorage.getItem('token')
if (token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Only redirect if we have a token (user was logged in) and it's not a login/register endpoint
      const isAuthEndpoint = error.config?.url?.includes('/login') || error.config?.url?.includes('/register') || error.config?.url?.includes('/auth/google')
      
      if (!isAuthEndpoint && localStorage.getItem('token')) {
        // Token expired or invalid for authenticated user
        localStorage.removeItem('token')
        delete api.defaults.headers.common['Authorization']
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default api