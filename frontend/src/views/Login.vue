<template>
  <div class="login-page">
    <div class="container">
      <div class="login-form-container">
        <h2>{{ $t('nav.login') }}</h2>
        
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="email">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="password">Password</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              class="form-input"
            />
          </div>
          
          <button type="submit" :disabled="loading" class="submit-btn">
            {{ loading ? 'Logging in...' : $t('nav.login') }}
          </button>
          
          <div v-if="error" class="error-message">
            {{ error }}
          </div>
        </form>
        
        <div class="oauth-section">
          <button @click="loginWithGoogle" class="google-btn">
            Login with Google
          </button>
        </div>
        
        <div class="register-link">
          <p>Don't have an account? 
            <router-link to="/register">{{ $t('nav.register') }}</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  name: 'Login',
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      error: ''
    }
  },
  
  computed: {
    ...mapState(['loading'])
  },
  
  methods: {
    ...mapActions(['login']),
    
    async handleLogin() {
      this.error = ''
      
      const result = await this.login(this.form)
      
      if (result.success) {
        this.$router.push('/')
      } else {
        this.error = result.message
      }
    },
    
    loginWithGoogle() {
      // TODO: Implement Google OAuth
      alert('Google OAuth not implemented yet')
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #121212;
  padding: 2rem 0;
}

.container {
  max-width: 400px;
  width: 100%;
  padding: 0 1rem;
}

.login-form-container {
  background-color: #1e1e1e;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #f5c518;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #fff;
  font-weight: bold;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #555;
  border-radius: 4px;
  background-color: #2a2a2a;
  color: #fff;
  font-size: 1rem;
}

.form-input:focus {
  outline: none;
  border-color: #f5c518;
}

.submit-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #f5c518;
  color: #000;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-btn:hover:not(:disabled) {
  background-color: #e6b800;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #dc3545;
  color: white;
  border-radius: 4px;
  text-align: center;
}

.oauth-section {
  margin: 2rem 0;
  text-align: center;
}

.google-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #4285f4;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.google-btn:hover {
  background-color: #357ae8;
}

.register-link {
  text-align: center;
  margin-top: 2rem;
}

.register-link p {
  color: #ccc;
}

.register-link a {
  color: #f5c518;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>