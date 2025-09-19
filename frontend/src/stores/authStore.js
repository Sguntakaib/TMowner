import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import axios from 'axios'
import toast from 'react-hot-toast'

const API_BASE = import.meta.env.REACT_APP_BACKEND_URL || 'http://localhost:8001'

const api = axios.create({
  baseURL: `${API_BASE}/api`,
})

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth-token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear auth state and redirect to login
      useAuthStore.getState().logout()
    }
    return Promise.reject(error)
  }
)

export const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isLoading: false,

      login: async (email, password) => {
        set({ isLoading: true })
        try {
          const response = await api.post('/auth/login', { email, password })
          const { user, access_token } = response.data
          
          localStorage.setItem('auth-token', access_token)
          set({ user, token: access_token, isLoading: false })
          
          toast.success('Welcome back!')
          return { success: true }
        } catch (error) {
          set({ isLoading: false })
          const message = error.response?.data?.detail || 'Login failed'
          toast.error(message)
          return { success: false, error: message }
        }
      },

      register: async (userData) => {
        set({ isLoading: true })
        try {
          const response = await api.post('/auth/register', userData)
          const { user, access_token } = response.data
          
          localStorage.setItem('auth-token', access_token)
          set({ user, token: access_token, isLoading: false })
          
          toast.success('Account created successfully!')
          return { success: true }
        } catch (error) {
          set({ isLoading: false })
          const message = error.response?.data?.detail || 'Registration failed'
          toast.error(message)
          return { success: false, error: message }
        }
      },

      logout: () => {
        localStorage.removeItem('auth-token')
        set({ user: null, token: null })
        toast.success('Logged out successfully')
      },

      checkAuth: async () => {
        const token = localStorage.getItem('auth-token')
        if (!token) {
          set({ isLoading: false })
          return
        }

        set({ isLoading: true })
        try {
          // Mock user for now until backend is fixed
          const mockUser = {
            id: "test123",
            email: "test@example.com",
            profile: {
              first_name: "Test",
              last_name: "User",
              avatar_url: null,
              bio: null
            },
            role: "student",
            progress: {
              level: 1,
              experience_points: 0,
              completed_scenarios: [],
              badges: []
            },
            preferences: {
              theme: "light",
              notifications: true
            }
          }
          set({ user: mockUser, token, isLoading: false })
        } catch (error) {
          localStorage.removeItem('auth-token')
          set({ user: null, token: null, isLoading: false })
        }
      },

      updateProfile: async (profileData) => {
        try {
          const response = await api.put('/auth/profile', profileData)
          set({ user: response.data })
          toast.success('Profile updated successfully')
          return { success: true }
        } catch (error) {
          const message = error.response?.data?.detail || 'Update failed'
          toast.error(message)
          return { success: false, error: message }
        }
      },

      // API instance for other stores to use
      api,
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ 
        user: state.user, 
        token: state.token 
      }),
    }
  )
)