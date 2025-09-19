import React, { useState, useEffect, useCallback, useRef } from 'react'
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  useNodesState,
  useEdgesState,
  Controls,
  MiniMap,
  Background,
  useReactFlow,
  Panel
} from '@reactflow/core'
import { HTML5Backend } from 'react-dnd-html5-backend'
import { DndProvider } from 'react-dnd'
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Typography,
  Chip,
  IconButton,
  Tooltip
} from '@mui/material'
import {
  Save,
  PlayArrow,
  Refresh,
  Visibility,
  VisibilityOff,
  Palette,
  Assessment
} from '@mui/icons-material'
import { useParams, useSearchParams } from 'react-router-dom'
import { useDigramStore } from '../../stores/diagramStore'
import { useScenarioStore } from '../../stores/scenarioStore'
import ElementPalette from './ElementPalette'
import ValidationPanel from './ValidationPanel'
import CustomNodes from './CustomNodes'
import toast from 'react-hot-toast'

const nodeTypes = {
  server: CustomNodes.ServerNode,
  database: CustomNodes.DatabaseNode,
  frontend: CustomNodes.FrontendNode,
  api: CustomNodes.ApiNode,
  security: CustomNodes.SecurityNode,
  network: CustomNodes.NetworkNode,
}

const DiagramBuilderContent = () => {
  const { diagramId } = useParams()
  const [searchParams] = useSearchParams()
  const scenarioId = searchParams.get('scenario')
  
  const reactFlowWrapper = useRef(null)
  const reactFlowInstance = useReactFlow()
  
  const {
    nodes,
    edges,
    setNodes,
    setEdges,
    showElementPalette,
    showValidation,
    toggleElementPalette,
    toggleValidation,
    saveDiagram,
    loadDiagram,
    validateDiagram,
    submitForScoring,
    clearDiagram
  } = useDigramStore()
  
  const { fetchScenario, currentScenario } = useScenarioStore()
  
  const [reactFlowNodes, setReactFlowNodes, onNodesChange] = useNodesState([])
  const [reactFlowEdges, setReactFlowEdges, onEdgesChange] = useEdgesState([])
  const [saveDialog, setSaveDialog] = useState(false)
  const [diagramTitle, setDiagramTitle] = useState('')
  const [startTime] = useState(Date.now())

  // Sync store nodes/edges with ReactFlow
  useEffect(() => {
    setReactFlowNodes(nodes)
  }, [nodes, setReactFlowNodes])

  useEffect(() => {
    setReactFlowEdges(edges)
  }, [edges, setReactFlowEdges])

  // Load diagram or scenario on mount
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        if (diagramId) {
          await loadDiagram(diagramId)
        } else if (scenarioId) {
          await fetchScenario(scenarioId)
          clearDiagram()
        }
      } catch (error) {
        console.error('Failed to load initial data:', error)
      }
    }

    loadInitialData()
  }, [diagramId, scenarioId])

  const onConnect = useCallback((params) => {
    const newEdge = {
      ...params,
      id: `edge-${Date.now()}`,
      type: 'default',
      data: { protocol: 'HTTP', encrypted: false }
    }
    setReactFlowEdges((eds) => addEdge(newEdge, eds))
    setEdges([...edges, newEdge])
  }, [edges, setEdges, setReactFlowEdges])

  const onDragOver = useCallback((event) => {
    event.preventDefault()
    event.dataTransfer.dropEffect = 'move'
  }, [])

  const onDrop = useCallback(
    (event) => {
      event.preventDefault()

      const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect()
      const type = event.dataTransfer.getData('application/reactflow')

      if (typeof type === 'undefined' || !type) {
        return
      }

      const position = reactFlowInstance.project({
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      })

      const newNode = {
        id: `${type}-${Date.now()}`,
        type,
        position,
        data: { 
          label: `${type.charAt(0).toUpperCase() + type.slice(1)} Node`,
          properties: {}
        },
      }

      setReactFlowNodes((nds) => nds.concat(newNode))
      setNodes([...nodes, newNode])
    },
    [reactFlowInstance, nodes, setNodes, setReactFlowNodes]
  )

  const handleSave = async () => {
    try {
      await saveDiagram(diagramTitle, scenarioId)
      setSaveDialog(false)
      setDiagramTitle('')
      toast.success('Diagram saved successfully!')
    } catch (error) {
      toast.error('Failed to save diagram')
    }
  }

  const handleValidate = async () => {
    try {
      await validateDiagram()
      toast.success('Validation completed!')
    } catch (error) {
      toast.error('Validation failed')
    }
  }

  const handleSubmit = async () => {
    try {
      const timeSpent = Math.floor((Date.now() - startTime) / 1000)
      const result = await submitForScoring(timeSpent)
      
      if (result) {
        toast.success(`Submitted! Score: ${result.scores.total_score.toFixed(1)}`)
      }
    } catch (error) {
      toast.error('Failed to submit diagram')
    }
  }

  return (
    <DndProvider backend={HTML5Backend}>
      <Box sx={{ height: '100vh', width: '100%', position: 'relative' }}>
        {/* Element Palette */}
        {showElementPalette && (
          <ElementPalette />
        )}

        {/* Validation Panel */}
        {showValidation && (
          <ValidationPanel />
        )}

        {/* Main Canvas */}
        <Box
          ref={reactFlowWrapper}
          sx={{ height: '100%', width: '100%' }}
        >
          <ReactFlow
            nodes={reactFlowNodes}
            edges={reactFlowEdges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onDrop={onDrop}
            onDragOver={onDragOver}
            nodeTypes={nodeTypes}
            fitView
            attributionPosition="bottom-right"
          >
            <Controls />
            <MiniMap />
            <Background variant="dots" gap={12} size={1} />
            
            {/* Top Panel with Controls */}
            <Panel position="top-center">
              <Box
                sx={{
                  display: 'flex',
                  gap: 1,
                  alignItems: 'center',
                  backgroundColor: 'white',
                  padding: 1,
                  borderRadius: 1,
                  boxShadow: 1
                }}
              >
                {currentScenario && (
                  <Chip 
                    label={currentScenario.title} 
                    color="primary" 
                    size="small"
                  />
                )}
                
                <Tooltip title="Toggle Element Palette">
                  <IconButton 
                    size="small" 
                    onClick={toggleElementPalette}
                    color={showElementPalette ? "primary" : "default"}
                  >
                    <Palette />
                  </IconButton>
                </Tooltip>
                
                <Tooltip title="Toggle Validation Panel">
                  <IconButton 
                    size="small" 
                    onClick={toggleValidation}
                    color={showValidation ? "primary" : "default"}
                  >
                    <Assessment />
                  </IconButton>
                </Tooltip>
                
                <Button
                  size="small"
                  startIcon={<Refresh />}
                  onClick={handleValidate}
                >
                  Validate
                </Button>
                
                <Button
                  size="small"
                  startIcon={<Save />}
                  onClick={() => setSaveDialog(true)}
                >
                  Save
                </Button>
                
                {scenarioId && (
                  <Button
                    size="small"
                    variant="contained"
                    startIcon={<PlayArrow />}
                    onClick={handleSubmit}
                  >
                    Submit
                  </Button>
                )}
              </Box>
            </Panel>
          </ReactFlow>
        </Box>

        {/* Save Dialog */}
        <Dialog
          open={saveDialog}
          onClose={() => setSaveDialog(false)}
          maxWidth="sm"
          fullWidth
        >
          <DialogTitle>
            Save Diagram
          </DialogTitle>
          <DialogContent>
            <TextField
              autoFocus
              margin="dense"
              label="Diagram Title"
              fullWidth
              variant="outlined"
              value={diagramTitle}
              onChange={(e) => setDiagramTitle(e.target.value)}
              placeholder="Enter a title for your diagram..."
            />
            {currentScenario && (
              <Typography variant="body2" color="textSecondary" sx={{ mt: 2 }}>
                This diagram will be associated with: {currentScenario.title}
              </Typography>
            )}
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setSaveDialog(false)}>
              Cancel
            </Button>
            <Button 
              onClick={handleSave}
              variant="contained"
              disabled={!diagramTitle.trim()}
            >
              Save
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </DndProvider>
  )
}

const DiagramBuilder = () => {
  return (
    <ReactFlowProvider>
      <DiagramBuilderContent />
    </ReactFlowProvider>
  )
}

export default DiagramBuilder