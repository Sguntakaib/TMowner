import React, { useState, useEffect } from 'react'
import {
  Container,
  Grid,
  Paper,
  Typography,
  Button,
  Box,
  Chip,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Alert,
  LinearProgress
} from '@mui/material'
import {
  PlayArrow,
  CheckCircle,
  AccessTime,
  Star,
  Assignment,
  Security,
  Architecture,
  Speed,
  CheckCircleOutline
} from '@mui/icons-material'
import { useParams, useNavigate } from 'react-router-dom'
import { useScenarioStore } from '../../stores/scenarioStore'
import { useDigramStore } from '../../stores/diagramStore'
import LoadingSpinner from '../Common/LoadingSpinner'

const ScenarioDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { currentScenario, fetchScenario, getScenarioProgress } = useScenarioStore()
  const { clearDiagram } = useDigramStore()
  const [isLoading, setIsLoading] = useState(true)
  const [progress, setProgress] = useState(null)

  useEffect(() => {
    const loadScenarioData = async () => {
      try {
        setIsLoading(true)
        await fetchScenario(id)
        const progressData = await getScenarioProgress(id)
        setProgress(progressData)
      } catch (error) {
        console.error('Failed to load scenario:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadScenarioData()
  }, [id])

  const handleStartScenario = () => {
    // Clear any existing diagram and start fresh
    clearDiagram()
    navigate(`/diagram?scenario=${id}`)
  }

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'beginner': return 'success'
      case 'intermediate': return 'warning'
      case 'expert': return 'error'
      default: return 'default'
    }
  }

  const getCategoryColor = (category) => {
    const colors = {
      'web': 'primary',
      'api': 'secondary',
      'database': 'info',
      'cloud': 'warning',
      'mobile': 'success',
      'network': 'error',
      'iot': 'default'
    }
    return colors[category] || 'default'
  }

  if (isLoading) {
    return <LoadingSpinner message="Loading scenario..." />
  }

  if (!currentScenario) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="error">
          Scenario not found
        </Alert>
      </Container>
    )
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Main Content */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, mb: 3 }}>
            {/* Header */}
            <Box sx={{ mb: 3 }}>
              <Box sx={{ mb: 2 }}>
                <Chip 
                  label={currentScenario.category} 
                  color={getCategoryColor(currentScenario.category)}
                  sx={{ mr: 1 }} 
                />
                <Chip 
                  label={currentScenario.difficulty} 
                  color={getDifficultyColor(currentScenario.difficulty)}
                />
              </Box>

              <Typography variant="h4" gutterBottom>
                {currentScenario.title}
              </Typography>

              <Typography variant="body1" color="textSecondary" paragraph>
                {currentScenario.description}
              </Typography>
            </Box>

            {/* Business Context */}
            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                Business Context
              </Typography>
              <Typography variant="body1" paragraph>
                {currentScenario.requirements.business_context}
              </Typography>
            </Box>

            {/* Technical Constraints */}
            {currentScenario.requirements.technical_constraints.length > 0 && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Technical Constraints
                </Typography>
                <List dense>
                  {currentScenario.requirements.technical_constraints.map((constraint, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <Assignment fontSize="small" />
                      </ListItemIcon>
                      <ListItemText primary={constraint} />
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}

            {/* Required Elements */}
            {currentScenario.requirements.required_elements.length > 0 && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Required System Components
                </Typography>
                <List dense>
                  {currentScenario.requirements.required_elements.map((element, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <CheckCircle fontSize="small" color="primary" />
                      </ListItemIcon>
                      <ListItemText primary={element} />
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}

            {/* Tags */}
            {currentScenario.tags.length > 0 && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Topics Covered
                </Typography>
                <Box>
                  {currentScenario.tags.map((tag) => (
                    <Chip 
                      key={tag} 
                      label={tag} 
                      variant="outlined"
                      sx={{ mr: 1, mb: 1 }}
                    />
                  ))}
                </Box>
              </Box>
            )}

            {/* Action Button */}
            <Box sx={{ textAlign: 'center', mt: 4 }}>
              <Button
                variant="contained"
                size="large"
                startIcon={<PlayArrow />}
                onClick={handleStartScenario}
                sx={{ px: 4, py: 1.5 }}
              >
                Start Modeling
              </Button>
            </Box>
          </Paper>
        </Grid>

        {/* Sidebar */}
        <Grid item xs={12} md={4}>
          {/* Scenario Info */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Scenario Information
              </Typography>
              
              <List>
                <ListItem>
                  <ListItemIcon>
                    <Star color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Max Points" 
                    secondary={currentScenario.max_points}
                  />
                </ListItem>
                
                {currentScenario.time_limit && (
                  <ListItem>
                    <ListItemIcon>
                      <AccessTime color="action" />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Time Limit" 
                      secondary={`${currentScenario.time_limit} minutes`}
                    />
                  </ListItem>
                )}
                
                <ListItem>
                  <ListItemIcon>
                    <Assignment color="action" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Difficulty" 
                    secondary={currentScenario.difficulty.charAt(0).toUpperCase() + currentScenario.difficulty.slice(1)}
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>

          {/* Scoring Criteria */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Scoring Criteria
              </Typography>
              
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Security fontSize="small" sx={{ mr: 1 }} />
                  <Typography variant="body2">Security</Typography>
                  <Typography variant="body2" sx={{ ml: 'auto' }}>
                    {(currentScenario.scoring_criteria.security_weight * 100).toFixed(0)}%
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={currentScenario.scoring_criteria.security_weight * 100} 
                  sx={{ mb: 1 }}
                />
              </Box>

              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Architecture fontSize="small" sx={{ mr: 1 }} />
                  <Typography variant="body2">Architecture</Typography>
                  <Typography variant="body2" sx={{ ml: 'auto' }}>
                    {(currentScenario.scoring_criteria.architecture_weight * 100).toFixed(0)}%
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={currentScenario.scoring_criteria.architecture_weight * 100} 
                  sx={{ mb: 1 }}
                />
              </Box>

              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Speed fontSize="small" sx={{ mr: 1 }} />
                  <Typography variant="body2">Performance</Typography>
                  <Typography variant="body2" sx={{ ml: 'auto' }}>
                    {(currentScenario.scoring_criteria.performance_weight * 100).toFixed(0)}%
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={currentScenario.scoring_criteria.performance_weight * 100} 
                  sx={{ mb: 1 }}
                />
              </Box>

              <Box>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <CompletionCircle fontSize="small" sx={{ mr: 1 }} />
                  <Typography variant="body2">Completeness</Typography>
                  <Typography variant="body2" sx={{ ml: 'auto' }}>
                    {(currentScenario.scoring_criteria.completeness_weight * 100).toFixed(0)}%
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={currentScenario.scoring_criteria.completeness_weight * 100} 
                />
              </Box>
            </CardContent>
          </Card>

          {/* Progress (if available) */}
          {progress && (
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Your Progress
                </Typography>
                
                <List>
                  <ListItem>
                    <ListItemText 
                      primary="Attempts" 
                      secondary={progress.attempts}
                    />
                  </ListItem>
                  
                  <ListItem>
                    <ListItemText 
                      primary="Best Score" 
                      secondary={`${progress.best_score.toFixed(1)}/100`}
                    />
                  </ListItem>
                  
                  <ListItem>
                    <ListItemText 
                      primary="Status" 
                      secondary={progress.completed ? 'Completed' : 'In Progress'}
                    />
                  </ListItem>
                  
                  {progress.last_attempt && (
                    <ListItem>
                      <ListItemText 
                        primary="Last Attempt" 
                        secondary={new Date(progress.last_attempt).toLocaleDateString()}
                      />
                    </ListItem>
                  )}
                </List>

                {progress.completed && (
                  <Alert severity="success" sx={{ mt: 2 }}>
                    Congratulations! You've completed this scenario.
                  </Alert>
                )}
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>
    </Container>
  )
}

export default ScenarioDetail