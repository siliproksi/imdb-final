<template>
  <div class="register-page">
    <div class="container">
      <div class="register-form-container">
        <h2>{{ $t('nav.register') }}</h2>
        
        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-group">
            <label for="email">Email *</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="password">Password *</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              class="form-input"
            />
            <small class="password-help">
              Password must be at least 8 characters long, contain 1 number and 1 special character
            </small>
          </div>
          
          <div class="form-group">
            <label for="country">Country</label>
            <input
              id="country"
              v-model="form.country"
              type="text"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="city">City</label>
            <input
              id="city"
              v-model="form.city"
              type="text"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="photo">Profile Photo (Optional)</label>
            <input
              id="photo"
              type="file"
              @change="handlePhotoChange"
              accept="image/*"
              class="form-input file-input"
            />
          </div>
          
          <button type="submit" :disabled="loading" class="submit-btn">
            {{ loading ? 'Creating Account...' : $t('nav.register') }}
          </button>
          
          <div v-if="error" class="error-message">
            {{ error }}
          </div>
          
          <div v-if="success" class="success-message">
            Account created successfully! You can now log in.
          </div>
        </form>
        
        <div class="login-link">
          <p>Already have an account? 
            <router-link to="/login">{{ $t('nav.login') }}</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  name: 'Register',
  data() {
    return {
      form: {
        email: '',
        password: '',
        country: '',
        city: ''
      },
      photoFile: null,
      error: '',
      success: false
    }
  },
  
  computed: {
    ...mapState(['loading'])
  },
  
  methods: {
    ...mapActions(['register']),
    
    handlePhotoChange(event) {
      this.photoFile = event.target.files[0]
    },
    
    async handleRegister() {
      this.error = ''
      this.success = false
      
      const result = await this.register(this.form)
      
      if (result.success) {
        this.success = true
        setTimeout(() => {
          this.$router.push('/login')
        }, 2000)
      } else {
        this.error = result.message
      }
    }
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #121212;
  padding: 2rem 0;
}

.container {
  max-width: 500px;
  width: 100%;
  padding: 0 1rem;
}

.register-form-container {
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

.file-input {
  padding: 0.5rem;
}

.password-help {
  display: block;
  margin-top: 0.5rem;
  color: #aaa;
  font-size: 0.85rem;
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

.success-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #28a745;
  color: white;
  border-radius: 4px;
  text-align: center;
}

.login-link {
  text-align: center;
  margin-top: 2rem;
}

.login-link p {
  color: #ccc;
}

.login-link a {
  color: #f5c518;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>