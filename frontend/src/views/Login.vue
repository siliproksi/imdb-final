<template>
  <div class="login-page">
    <div class="container">
      <div class="login-form-container">
        <h2>{{ $t('login.title') }}</h2>
        
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="email">{{ $t('login.email') }}</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="password">{{ $t('login.password') }}</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              class="form-input"
            />
          </div>
          
          <button type="submit" :disabled="loading" class="submit-btn">
            {{ loading ? $t('login.loggingIn') : $t('login.loginButton') }}
          </button>
          
          <div class="divider">
            <span>or</span>
          </div>
          
          <button type="button" @click="handleGoogleAuth" class="google-btn">
            <svg width="18" height="18" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            {{ $t('login.googleLogin') }}
          </button>
          
          <div v-if="error" class="error-message">
            {{ error }}
            <button type="button" @click="clearError" class="error-close">×</button>
          </div>
        </form>
        
        <div class="register-link">
          <p>{{ $t('login.noAccount') }} 
            <router-link to="/register">{{ $t('login.registerLink') }}</router-link>
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
  
  mounted() {
    // Initialize Google Sign-In after component is mounted
    this.$nextTick(() => {
      this.initializeGoogleSignIn()
    })
  },
  
  methods: {
    ...mapActions(['login']),
    
    async handleLogin() {
      const result = await this.login(this.form)
      
      if (result.success) {
        this.error = '' // Only clear on success
        const redirectPath = this.$route.query.redirect || '/'
        this.$router.push(redirectPath)
      } else {
        this.error = result.message
        // Error persists until manually dismissed by user
      }
    },
    
    clearError() {
      this.error = ''
    },
    
    handleGoogleAuth() {
      // This function triggers Google Sign-In
      if (window.google) {
        window.google.accounts.id.prompt()
      }
    },
    
    initializeGoogleSignIn() {
      if (window.google) {
        window.google.accounts.id.initialize({
          client_id: '19959323738-2lv4h95g32fdm07oh2q12c67hj27u0r1.apps.googleusercontent.com',
          callback: this.handleGoogleCallback,
          auto_select: false,
          cancel_on_tap_outside: true
        })
      } else {
        console.error('Google Sign-In library not loaded')
      }
    },
    
    async handleGoogleCallback(response) {
      try {
        const result = await this.$store.dispatch('googleLogin', response.credential)
        
        if (result.success) {
          const redirectPath = this.$route.query.redirect || '/'
          this.$router.push(redirectPath)
        } else {
          this.error = result.message
        }
      } catch (error) {
        this.error = 'Google login failed. Please try again.'
      }
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

/* Mobile Responsive */
@media (max-width: 768px) {
  .login-page {
    padding: 1rem 0;
    align-items: flex-start;
    padding-top: 2rem;
  }
  
  .container {
    max-width: 100%;
  }
  
  .login-form-container {
    padding: 1.5rem;
  }
}

@media (max-width: 480px) {
  .login-page {
    padding: 1rem 0;
  }
  
  .login-form-container {
    padding: 1.25rem;
    margin: 0;
    border-radius: 6px;
  }
  
  .form-input {
    font-size: 16px; /* Prevents zoom on iOS */
  }
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
  padding: 0.75rem 2.5rem 0.75rem 0.75rem;
  background-color: #dc3545;
  color: white;
  border-radius: 4px;
  border: 1px solid #c82333;
  position: relative;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(220, 53, 69, 0.3);
}

.error-close {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: white;
  font-size: 1.4rem;
  font-weight: bold;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.error-close:hover {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
}

.divider {
  display: flex;
  align-items: center;
  margin: 1.5rem 0;
  color: #888;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #444;
}

.divider span {
  padding: 0 1rem;
  font-size: 0.9rem;
}

.google-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #fff;
  color: #333;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.google-btn:hover {
  background-color: #f8f9fa;
  border-color: #c6c6c6;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.google-btn svg {
  flex-shrink: 0;
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