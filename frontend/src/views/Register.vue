<template>
  <div class="register-page">
    <div class="container">
      <div class="register-form-container">
        <h2>{{ $t('register.title') }}</h2>
        
        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-group">
            <label for="email">{{ $t('register.email') }} *</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="password">{{ $t('register.password') }} *</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              class="form-input"
            />
            <small class="password-help">
              {{ $t('register.passwordHelp') }}
            </small>
          </div>
          
          <div class="form-group">
            <label for="country">{{ $t('register.country') }}</label>
            <input
              id="country"
              v-model="form.country"
              type="text"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="city">{{ $t('register.city') }}</label>
            <input
              id="city"
              v-model="form.city"
              type="text"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="photo">{{ $t('register.photo') }}</label>
            <input
              id="photo"
              type="file"
              @change="handlePhotoChange"
              accept="image/*"
              class="form-input file-input"
            />
            <div v-if="photoPreview" class="photo-preview">
              <img :src="photoPreview" alt="Photo preview" class="preview-image" />
              <button type="button" @click="removePhoto" class="remove-photo-btn">×</button>
            </div>
          </div>
          
          <button type="submit" :disabled="loading" class="submit-btn">
            {{ loading ? $t('register.creatingAccount') : $t('register.registerButton') }}
          </button>
          
          <div v-if="error" class="error-message">
            {{ error }}
            <button type="button" @click="clearError" class="error-close">×</button>
          </div>
          
          <div v-if="success" class="success-message">
            {{ $t('register.successMessage') }}
            <br><br>
            <span class="redirect-message">Redirecting to login in {{ countdown }}...</span>
          </div>
        </form>
        
        <div class="login-link">
          <p>{{ $t('register.hasAccount') }} 
            <router-link to="/login">{{ $t('register.loginLink') }}</router-link>
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
        city: '',
        photo: null
      },
      photoFile: null,
      photoPreview: null,
      error: '',
      success: false,
      countdown: 3,
      countdownInterval: null
    }
  },
  
  computed: {
    ...mapState(['loading'])
  },
  
  methods: {
    ...mapActions(['register']),
    
    handlePhotoChange(event) {
      const file = event.target.files[0]
      if (file) {
        this.photoFile = file
        
        // Create FileReader to convert to base64 and show preview
        const reader = new FileReader()
        
        reader.onload = (e) => {
          const base64 = e.target.result
          this.photoPreview = base64
          this.form.photo = base64
        }
        
        reader.readAsDataURL(file)
      }
    },
    
    removePhoto() {
      this.photoFile = null
      this.photoPreview = null
      this.form.photo = null
      // Clear the file input
      const fileInput = document.getElementById('photo')
      if (fileInput) {
        fileInput.value = ''
      }
    },
    
    async handleRegister() {
      const result = await this.register(this.form)
      
      if (result.success) {
        this.error = '' // Only clear on success
        this.success = true
        this.startCountdown()
      } else {
        this.error = result.message
        this.success = false
        // Error persists until manually dismissed by user
      }
    },
    
    clearError() {
      this.error = ''
    },
    
    startCountdown() {
      this.countdown = 3
      this.countdownInterval = setInterval(() => {
        this.countdown--
        if (this.countdown <= 0) {
          clearInterval(this.countdownInterval)
          this.$router.push('/login')
        }
      }, 1000)
    }
  },
  
  beforeUnmount() {
    // Clean up interval if component is destroyed
    if (this.countdownInterval) {
      clearInterval(this.countdownInterval)
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

/* Mobile Responsive */
@media (max-width: 768px) {
  .register-page {
    padding: 1rem 0;
    align-items: flex-start;
    padding-top: 2rem;
  }
  
  .container {
    max-width: 100%;
  }
  
  .register-form-container {
    padding: 1.5rem;
  }
}

@media (max-width: 480px) {
  .register-page {
    padding: 1rem 0;
  }
  
  .register-form-container {
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

.success-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #28a745;
  color: white;
  border-radius: 4px;
  text-align: center;
}

.redirect-message {
  font-weight: normal;
  opacity: 0.9;
  font-size: 0.9rem;
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

.photo-preview {
  position: relative;
  margin-top: 1rem;
  display: inline-block;
}

.preview-image {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 8px;
  border: 2px solid #f5c518;
}

.remove-photo-btn {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 24px;
  height: 24px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.remove-photo-btn:hover {
  background-color: #c82333;
}

/* Mobile responsive for photo preview */
@media (max-width: 480px) {
  .preview-image {
    width: 100px;
    height: 100px;
  }
  
  .remove-photo-btn {
    width: 20px;
    height: 20px;
    font-size: 14px;
    top: -6px;
    right: -6px;
  }
}
</style>