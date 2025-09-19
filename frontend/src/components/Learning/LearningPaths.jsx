import React, { useState, useEffect } from 'react'
import {
  Container,
  Grid,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Box,
  Chip,
  LinearProgress,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Divider
} from '@mui/material'
import {
  School,
  CheckCircle,
  RadioButtonUnchecked,
  AccessTime,
  Star,
  EmojiEvents,
  TrendingUp
} from '@mui/icons-material'
import { useAuthStore } from '../../stores/authStore'
import LoadingSpinner from '../Common/LoadingSpinner'

const LearningPaths = () => {
  const { api } = useAuthStore()
  const [learningPaths, setLearningPaths] = useState([])
  const [userProgress, setUserProgress] = useState(null)
  const [achievements, setAchievements] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [selectedPath, setSelectedPath] = useState(null)
  const [pathDialog, setPathDialog] = useState(false)

  useEffect(() => {
    const loadLearningData = async () => {
      try {
        setIsLoading(true)
        
        // Fetch learning paths
        const pathsResponse = await api.get('/learning/paths')
        setLearningPaths(pathsResponse.data.learning_paths)
        
        // Fetch user progress
        const progressResponse = await api.get('/learning/progress')
        setUserProgress(progressResponse.data)
        
        // Fetch achievements
        const achievementsResponse = await api.get('/learning/achievements')
        setAchievements(achievementsResponse.data)
      } catch (error) {
        console.error('Failed to load learning data:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadLearningData()
  }, [])

  const handleViewPath = (path) => {
    setSelectedPath(path)
    setPathDialog(true)
  }

  const handleEnrollInPath = async (pathId) => {
    try {
      await api.post(`/learning/paths/${pathId}/enroll`)
      // Refresh progress data
      const progressResponse = await api.get('/learning/progress')
      setUserProgress(progressResponse.data)
      setPathDialog(false)
    } catch (error) {
      console.error('Failed to enroll in path:', error)
    }
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
      'security': 'primary',
      'web': 'secondary',
      'cloud': 'info',
      'network': 'warning'
    }
    return colors[category] || 'default'
  }

  const isEnrolled = (pathId) => {
    if (!userProgress) return false
    return [...userProgress.active_paths, ...userProgress.completed_paths]
      .some(path => path.path_id === pathId)
  }

  const getPathProgress = (pathId) => {
    if (!userProgress) return 0
    const path = [...userProgress.active_paths, ...userProgress.completed_paths]
      .find(p => p.path_id === pathId)
    return path ? path.completion_percentage : 0
  }

  if (isLoading) {
    return <LoadingSpinner message="Loading learning paths..." />
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Learning Paths
      </Typography>

      <Typography variant="body1" color="textSecondary" paragraph>
        Structured learning journeys to master threat modeling
      </Typography>

      <Grid container spacing={3}>
        {/* Progress Overview */}
        <Grid item xs={12}>
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Grid container spacing={3}>
                <Grid item xs={12} sm={6} md={3}>
                  <Box sx={{ textAlign: 'center' }}>
                    <School color="primary" sx={{ fontSize: 40, mb: 1 }} />
                    <Typography variant="h6">
                      {userProgress?.enrolled_paths || 0}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Enrolled Paths
                    </Typography>
                  </Box>
                </Grid>
                
                <Grid item xs={12} sm={6} md={3}>
                  <Box sx={{ textAlign: 'center' }}>
                    <CheckCircle color="success" sx={{ fontSize: 40, mb: 1 }} />
                    <Typography variant="h6">
                      {userProgress?.completed_paths?.length || 0}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Completed Paths
                    </Typography>
                  </Box>
                </Grid>
                
                <Grid item xs={12} sm={6} md={3}>
                  <Box sx={{ textAlign: 'center' }}>
                    <TrendingUp color="info" sx={{ fontSize: 40, mb: 1 }} />
                    <Typography variant="h6">
                      {userProgress?.overall_progress?.toFixed(0) || 0}%
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Overall Progress
                    </Typography>
                  </Box>
                </Grid>
                
                <Grid item xs={12} sm={6} md={3}>
                  <Box sx={{ textAlign: 'center' }}>
                    <EmojiEvents color="warning" sx={{ fontSize: 40, mb: 1 }} />
                    <Typography variant="h6">
                      {achievements?.total_earned || 0}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Badges Earned
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Learning Paths */}
        {learningPaths.map((path) => {
          const enrolled = isEnrolled(path._id)
          const progress = getPathProgress(path._id)
          
          return (
            <Grid item xs={12} md={6} lg={4} key={path._id}>
              <Card 
                sx={{ 
                  height: '100%', 
                  display: 'flex', 
                  flexDirection: 'column',
                  transition: 'transform 0.2s, elevation 0.2s',
                  '&:hover': {
                    transform: 'translateY(-2px)',
                    elevation: 8
                  }
                }}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box sx={{ mb: 2 }}>
                    <Chip 
                      label={path.category} 
                      color={getCategoryColor(path.category)}
                      size="small"
                      sx={{ mr: 1 }}
                    />
                    <Chip 
                      label={path.difficulty} 
                      color={getDifficultyColor(path.difficulty)}
                      size="small"
                    />
                  </Box>

                  <Typography variant="h6" gutterBottom>
                    {path.name}
                  </Typography>
                  
                  <Typography 
                    variant="body2" 
                    color="textSecondary" 
                    sx={{ mb: 2 }}
                  >
                    {path.description}
                  </Typography>

                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <AccessTime fontSize="small" sx={{ mr: 0.5 }} />
                    <Typography variant="body2" color="textSecondary">
                      {path.estimated_hours} hours
                    </Typography>
                  </Box>

                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <School fontSize="small" sx={{ mr: 0.5 }} />
                    <Typography variant="body2" color="textSecondary">
                      {path.modules?.length || 0} modules
                    </Typography>
                  </Box>

                  {enrolled && (
                    <Box sx={{ mt: 2 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="body2">Progress</Typography>
                        <Typography variant="body2">{progress.toFixed(0)}%</Typography>
                      </Box>
                      <LinearProgress 
                        variant="determinate" 
                        value={progress} 
                        sx={{ mb: 1 }}
                      />
                    </Box>
                  )}
                </CardContent>
                
                <CardActions sx={{ p: 2, pt: 0 }}>
                  <Button 
                    fullWidth
                    variant={enrolled ? "outlined" : "contained"}
                    onClick={() => handleViewPath(path)}
                  >
                    {enrolled ? "Continue" : "View Details"}
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          )
        })}
      </Grid>

      {/* Path Detail Dialog */}
      <Dialog
        open={pathDialog}
        onClose={() => setPathDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {selectedPath?.name}
        </DialogTitle>
        <DialogContent>
          {selectedPath && (
            <Box>
              <Box sx={{ mb: 2 }}>
                <Chip 
                  label={selectedPath.category} 
                  color={getCategoryColor(selectedPath.category)}
                  size="small"
                  sx={{ mr: 1 }}
                />
                <Chip 
                  label={selectedPath.difficulty} 
                  color={getDifficultyColor(selectedPath.difficulty)}
                  size="small"
                />
              </Box>

              <Typography variant="body1" paragraph>
                {selectedPath.description}
              </Typography>

              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" color="textSecondary">
                  Estimated completion time: {selectedPath.estimated_hours} hours
                </Typography>
              </Box>

              <Typography variant="h6" gutterBottom>
                Modules
              </Typography>
              
              <List>
                {selectedPath.modules?.map((module, index) => (
                  <React.Fragment key={index}>
                    <ListItem>
                      <ListItemIcon>
                        {isEnrolled(selectedPath._id) ? (
                          <CheckCircle color="success" />
                        ) : (
                          <RadioButtonUnchecked />
                        )}
                      </ListItemIcon>
                      <ListItemText
                        primary={module.name}
                        secondary={`${module.scenarios?.length || 0} scenarios`}
                      />
                    </ListItem>
                    {index < selectedPath.modules.length - 1 && <Divider variant="inset" component="li" />}
                  </React.Fragment>
                ))}
              </List>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPathDialog(false)}>
            Cancel
          </Button>
          {selectedPath && !isEnrolled(selectedPath._id) && (
            <Button 
              variant="contained"
              onClick={() => handleEnrollInPath(selectedPath._id)}
            >
              Enroll Now
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </Container>
  )
}

export default LearningPaths