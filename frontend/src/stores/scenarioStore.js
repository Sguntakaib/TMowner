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
    
    try {
      // Mock scenarios data for now
      const mockScenarios = [
        {
          id: "scenario1",
          title: "Web Application Security Assessment",
          description: "Design a secure architecture for a web application with user authentication, data storage, and API endpoints.",
          category: "web",
          difficulty: "beginner",
          tags: ["authentication", "web security", "API"],
          requirements: {
            business_context: "A startup needs a secure web application for user management",
            technical_constraints: ["Must support 1000+ concurrent users", "GDPR compliance required"],
            required_elements: ["Web Server", "Database", "Load Balancer", "Authentication Service"]
          },
          scoring_criteria: {
            security_weight: 0.4,
            architecture_weight: 0.3,
            performance_weight: 0.2,
            completeness_weight: 0.1
          },
          max_points: 100,
          time_limit: 60,
          prerequisites: [],
          created_at: "2023-01-01T00:00:00Z",
          updated_at: "2023-01-01T00:00:00Z",
          published: true,
          reference_architectures: []
        },
        {
          id: "scenario2", 
          title: "Cloud Infrastructure Security",
          description: "Design a secure cloud infrastructure for a microservices architecture with proper network segmentation.",
          category: "cloud",
          difficulty: "intermediate",
          tags: ["cloud", "microservices", "network security"],
          requirements: {
            business_context: "Enterprise migration to cloud with multiple services",
            technical_constraints: ["Multi-region deployment", "Zero-trust network"],
            required_elements: ["API Gateway", "Service Mesh", "Container Registry", "Identity Provider"]
          },
          scoring_criteria: {
            security_weight: 0.4,
            architecture_weight: 0.3,
            performance_weight: 0.2,
            completeness_weight: 0.1
          },
          max_points: 100,
          time_limit: 90,
          prerequisites: [],
          created_at: "2023-01-01T00:00:00Z",
          updated_at: "2023-01-01T00:00:00Z",
          published: true,
          reference_architectures: []
        }
      ]
      
      if (page === 0) {
        set({ scenarios: mockScenarios, isLoading: false })
      } else {
        set((state) => ({ 
          scenarios: [...state.scenarios, ...mockScenarios],
          isLoading: false 
        }))
      }
      
      return mockScenarios
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