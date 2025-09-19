import { create } from 'zustand'
import { useAuthStore } from './authStore'
import toast from 'react-hot-toast'

export const useScenarioStore = create((set, get) => ({
  // State
  scenarios: [],
  currentScenario: null,
  categories: ['web', 'api', 'database', 'cloud', 'mobile', 'network', 'iot'],
  difficulties: ['beginner', 'intermediate', 'expert'],
  isLoading: false,
  filters: {
    category: null,
    difficulty: null,
    search: '',
    tags: []
  },

  // Actions
  setFilters: (filters) => set((state) => ({
    filters: { ...state.filters, ...filters }
  })),

  setCurrentScenario: (scenario) => set({ currentScenario: scenario }),

  // Fetch scenarios with filters
  fetchScenarios: async (page = 0, limit = 20) => {
    set({ isLoading: true })
    const { filters } = get()
    const { api } = useAuthStore.getState()

    try {
      const params = new URLSearchParams({
        skip: page * limit,
        limit: limit.toString()
      })

      if (filters.category) params.append('category', filters.category)
      if (filters.difficulty) params.append('difficulty', filters.difficulty)
      if (filters.search) params.append('search', filters.search)
      if (filters.tags.length > 0) params.append('tags', filters.tags.join(','))

      const response = await api.get(`/scenarios/?${params}`)
      
      if (page === 0) {
        set({ scenarios: response.data, isLoading: false })
      } else {
        set((state) => ({ 
          scenarios: [...state.scenarios, ...response.data],
          isLoading: false 
        }))
      }
      
      return response.data
    } catch (error) {
      set({ isLoading: false })
      toast.error('Failed to fetch scenarios')
      return []
    }
  },

  // Fetch single scenario
  fetchScenario: async (scenarioId) => {
    const { api } = useAuthStore.getState()

    try {
      const response = await api.get(`/scenarios/${scenarioId}`)
      set({ currentScenario: response.data })
      return response.data
    } catch (error) {
      toast.error('Failed to fetch scenario')
      throw error
    }
  },

  // Get scenario progress
  getScenarioProgress: async (scenarioId) => {
    const { api } = useAuthStore.getState()

    try {
      const response = await api.get(`/scenarios/${scenarioId}/progress`)
      return response.data
    } catch (error) {
      console.error('Failed to fetch scenario progress:', error)
      return null
    }
  },

  // Create scenario (admin only)
  createScenario: async (scenarioData) => {
    const { api } = useAuthStore.getState()

    try {
      const response = await api.post('/scenarios/', scenarioData)
      set((state) => ({
        scenarios: [response.data, ...state.scenarios]
      }))
      toast.success('Scenario created successfully')
      return response.data
    } catch (error) {
      toast.error('Failed to create scenario')
      throw error
    }
  },

  // Update scenario (admin only)
  updateScenario: async (scenarioId, scenarioData) => {
    const { api } = useAuthStore.getState()

    try {
      const response = await api.put(`/scenarios/${scenarioId}`, scenarioData)
      set((state) => ({
        scenarios: state.scenarios.map(scenario =>
          scenario.id === scenarioId ? response.data : scenario
        ),
        currentScenario: response.data
      }))
      toast.success('Scenario updated successfully')
      return response.data
    } catch (error) {
      toast.error('Failed to update scenario')
      throw error
    }
  },

  // Delete scenario (admin only)
  deleteScenario: async (scenarioId) => {
    const { api } = useAuthStore.getState()

    try {
      await api.delete(`/scenarios/${scenarioId}`)
      set((state) => ({
        scenarios: state.scenarios.filter(scenario => scenario.id !== scenarioId)
      }))
      toast.success('Scenario deleted successfully')
    } catch (error) {
      toast.error('Failed to delete scenario')
      throw error
    }
  },

  // Search scenarios
  searchScenarios: (query) => {
    set((state) => ({
      filters: { ...state.filters, search: query }
    }))
    get().fetchScenarios(0, 20)
  },

  // Filter by category
  filterByCategory: (category) => {
    set((state) => ({
      filters: { ...state.filters, category }
    }))
    get().fetchScenarios(0, 20)
  },

  // Filter by difficulty
  filterByDifficulty: (difficulty) => {
    set((state) => ({
      filters: { ...state.filters, difficulty }
    }))
    get().fetchScenarios(0, 20)
  },

  // Clear filters
  clearFilters: () => {
    set({
      filters: {
        category: null,
        difficulty: null,
        search: '',
        tags: []
      }
    })
    get().fetchScenarios(0, 20)
  },

  // Get recommended scenarios based on user progress
  getRecommendedScenarios: async () => {
    const { api } = useAuthStore.getState()

    try {
      const response = await api.get('/learning/recommendations', {
        params: { limit: 5 }
      })
      return response.data.recommendations
    } catch (error) {
      console.error('Failed to fetch recommendations:', error)
      return []
    }
  }
}))