import { create } from 'zustand'
import { subscribeWithSelector } from 'zustand/middleware'
import { useAuthStore } from './authStore'
import toast from 'react-hot-toast'

export const useDiagramStore = create(
  subscribeWithSelector((set, get) => ({
    // Diagram state
    currentDiagram: null,
    nodes: [],
    edges: [],
    selectedNodes: [],
    selectedEdges: [],
    
    // Metadata
    trustBoundaries: [],
    dataFlows: [],
    securityControls: [],
    
    // UI state
    isValidating: false,
    validationResults: [],
    showValidation: true,
    showElementPalette: true,
    
    // Collaboration
    collaborators: [],
    isCollaborating: false,
    
    // Actions
    setCurrentDiagram: (diagram) => set({ currentDiagram: diagram }),
    
    setNodes: (nodes) => set({ nodes }),
    setEdges: (edges) => set({ edges }),
    
    addNode: (node) => set((state) => ({
      nodes: [...state.nodes, node]
    })),
    
    updateNode: (nodeId, updates) => set((state) => ({
      nodes: state.nodes.map(node => 
        node.id === nodeId ? { ...node, ...updates } : node
      )
    })),
    
    removeNode: (nodeId) => set((state) => ({
      nodes: state.nodes.filter(node => node.id !== nodeId),
      edges: state.edges.filter(edge => 
        edge.source !== nodeId && edge.target !== nodeId
      )
    })),
    
    addEdge: (edge) => set((state) => ({
      edges: [...state.edges, edge]
    })),
    
    updateEdge: (edgeId, updates) => set((state) => ({
      edges: state.edges.map(edge => 
        edge.id === edgeId ? { ...edge, ...updates } : edge
      )
    })),
    
    removeEdge: (edgeId) => set((state) => ({
      edges: state.edges.filter(edge => edge.id !== edgeId)
    })),
    
    setSelectedNodes: (nodeIds) => set({ selectedNodes: nodeIds }),
    setSelectedEdges: (edgeIds) => set({ selectedEdges: edgeIds }),
    
    // Metadata actions
    addTrustBoundary: (boundary) => set((state) => ({
      trustBoundaries: [...state.trustBoundaries, boundary]
    })),
    
    addDataFlow: (flow) => set((state) => ({
      dataFlows: [...state.dataFlows, flow]
    })),
    
    addSecurityControl: (control) => set((state) => ({
      securityControls: [...state.securityControls, control]
    })),
    
    // UI actions
    toggleValidation: () => set((state) => ({
      showValidation: !state.showValidation
    })),
    
    toggleElementPalette: () => set((state) => ({
      showElementPalette: !state.showElementPalette
    })),
    
    // Validation
    validateDiagram: async () => {
      const { currentDiagram } = get()
      if (!currentDiagram) return
      
      set({ isValidating: true })
      
      try {
        const { api } = useAuthStore.getState()
        const response = await api.post('/scoring/validate', null, {
          params: { diagram_id: currentDiagram.id }
        })
        
        set({ 
          validationResults: response.data.validation_results,
          isValidating: false 
        })
      } catch (error) {
        set({ isValidating: false })
        toast.error('Validation failed')
      }
    },
    
    // Save diagram
    saveDiagram: async (title, scenarioId = null) => {
      const { nodes, edges, trustBoundaries, dataFlows, securityControls, currentDiagram } = get()
      const { api } = useAuthStore.getState()
      
      const diagramData = {
        title: title || currentDiagram?.title || 'Untitled Diagram',
        scenario_id: scenarioId,
        diagram_data: {
          nodes: nodes.map(node => ({
            id: node.id,
            type: node.type,
            position: node.position,
            data: node.data
          })),
          edges: edges.map(edge => ({
            id: edge.id,
            source: edge.source,
            target: edge.target,
            type: edge.type || 'default',
            data: edge.data || {}
          }))
        },
        metadata: {
          trust_boundaries: trustBoundaries,
          data_flows: dataFlows,
          security_controls: securityControls
        }
      }
      
      try {
        let response
        if (currentDiagram?.id) {
          // Update existing diagram
          response = await api.put(`/diagrams/${currentDiagram.id}`, diagramData)
        } else {
          // Create new diagram
          response = await api.post('/diagrams/', diagramData)
        }
        
        set({ currentDiagram: response.data })
        toast.success('Diagram saved successfully')
        return response.data
      } catch (error) {
        toast.error('Failed to save diagram')
        throw error
      }
    },
    
    // Load diagram
    loadDiagram: async (diagramId) => {
      const { api } = useAuthStore.getState()
      
      try {
        const response = await api.get(`/diagrams/${diagramId}`)
        const diagram = response.data
        
        set({
          currentDiagram: diagram,
          nodes: diagram.diagram_data.nodes,
          edges: diagram.diagram_data.edges,
          trustBoundaries: diagram.metadata.trust_boundaries || [],
          dataFlows: diagram.metadata.data_flows || [],
          securityControls: diagram.metadata.security_controls || []
        })
        
        return diagram
      } catch (error) {
        toast.error('Failed to load diagram')
        throw error
      }
    },
    
    // Submit for scoring
    submitForScoring: async (timeSpent) => {
      const { currentDiagram } = get()
      if (!currentDiagram) return
      
      try {
        const { api } = useAuthStore.getState()
        
        // First submit the diagram
        await api.post(`/diagrams/${currentDiagram.id}/submit`)
        
        // Then score it
        const response = await api.post('/scoring/score', null, {
          params: { 
            diagram_id: currentDiagram.id,
            time_spent: timeSpent 
          }
        })
        
        toast.success('Diagram submitted and scored!')
        return response.data
      } catch (error) {
        toast.error('Failed to submit diagram')
        throw error
      }
    },
    
    // Clear diagram
    clearDiagram: () => set({
      currentDiagram: null,
      nodes: [],
      edges: [],
      trustBoundaries: [],
      dataFlows: [],
      securityControls: [],
      validationResults: [],
      selectedNodes: [],
      selectedEdges: []
    }),
    
    // Collaboration methods (WebSocket integration would go here)
    startCollaboration: async (diagramId) => {
      // WebSocket connection logic would go here
      set({ isCollaborating: true })
    },
    
    stopCollaboration: () => {
      set({ isCollaborating: false, collaborators: [] })
    }
  }))
)