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
          
          <div v-if="error" class="error-message">
            {{ error }}
            <button type="button" @click="clearError" class="error-close">×</button>
          </div>
        </form>
        
        <div class="divider">
          <span>or</span>
        </div>
        
        <div class="oauth-section">
          <div id="google-signin-button"></div>
        </div>
        
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
    
    initializeGoogleSignIn() {
      if (window.google) {
        window.google.accounts.id.initialize({
          client_id: '19959323738-2lv4h95g32fdm07oh2q12c67hj27u0r1.apps.googleusercontent.com',
          callback: this.handleGoogleCallback,
          auto_select: false,
          cancel_on_tap_outside: true
        })
        
        // Render the button with "continue_with" text
        window.google.accounts.id.renderButton(
          document.getElementById('google-signin-button'),
          {
            theme: 'outline',
            size: 'large',
            width: '100%',
            text: 'continue_with',
            logo_alignment: 'left'
          }
        )
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

.oauth-section {
  margin: 1rem 0;
  text-align: center;
}

#google-signin-button {
  display: flex;
  justify-content: center;
  width: 100%;
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