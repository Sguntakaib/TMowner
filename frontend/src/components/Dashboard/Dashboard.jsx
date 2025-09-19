import React, { useState, useEffect } from 'react'
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  LinearProgress,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Divider
} from '@mui/material'
import {
  TrendingUp,
  Psychology,
  EmojiEvents,
  Timeline,
  PlayArrow,
  Star
} from '@mui/icons-material'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../stores/authStore'
import { useScenarioStore } from '../../stores/scenarioStore'

const Dashboard = () => {
  const navigate = useNavigate()
  const { user } = useAuthStore()
  const { fetchScenarios, scenarios, getRecommendedScenarios } = useScenarioStore()
  const [userStats, setUserStats] = useState(null)
  const [recommendations, setRecommendations] = useState([])
  const [recentScores, setRecentScores] = useState([])

  useEffect(() => {
    // Fetch dashboard data
    const loadDashboardData = async () => {
      try {
        // Fetch recent scenarios
        await fetchScenarios(0, 6)
        
        // Fetch user stats
        const { api } = useAuthStore.getState()
        const statsResponse = await api.get('/scoring/stats')
        setUserStats(statsResponse.data)
        
        // Fetch recent scores
        const scoresResponse = await api.get('/scoring/history?limit=5')
        setRecentScores(scoresResponse.data)
        
        // Fetch recommendations
        const recs = await getRecommendedScenarios()
        setRecommendations(recs)
      } catch (error) {
        console.error('Failed to load dashboard data:', error)
      }
    }
    
    loadDashboardData()
  }, [])

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'beginner': return 'success'
      case 'intermediate': return 'warning'
      case 'expert': return 'error'
      default: return 'default'
    }
  }

  const getScoreColor = (score) => {
    if (score >= 90) return 'success'
    if (score >= 70) return 'warning'
    return 'error'
  }

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Welcome back, {user?.profile?.first_name || user?.email.split('@')[0]}!
        </Typography>
        <Typography variant="body1" color="textSecondary">
          Continue your threat modeling journey
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* User Stats Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                  <Psychology />
                </Avatar>
                <Box>
                  <Typography variant="h6">
                    {userStats?.completed_scenarios || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Completed Scenarios
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: 'success.main', mr: 2 }}>
                  <TrendingUp />
                </Avatar>
                <Box>
                  <Typography variant="h6">
                    {userStats?.average_score?.toFixed(1) || '0.0'}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Average Score
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: 'warning.main', mr: 2 }}>
                  <EmojiEvents />
                </Avatar>
                <Box>
                  <Typography variant="h6">
                    {userStats?.badges_earned?.length || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Badges Earned
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: 'info.main', mr: 2 }}>
                  <Timeline />
                </Avatar>
                <Box>
                  <Typography variant="h6">
                    {userStats?.current_streak || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Day Streak
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Scenarios */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Scenarios
            </Typography>
            <Grid container spacing={2}>
              {scenarios.slice(0, 6).map((scenario) => (
                <Grid item xs={12} sm={6} key={scenario.id}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        {scenario.title}
                      </Typography>
                      <Typography 
                        variant="body2" 
                        color="textSecondary" 
                        sx={{ mb: 2, minHeight: 40 }}
                      >
                        {scenario.description.substring(0, 100)}...
                      </Typography>
                      <Box sx={{ mb: 2 }}>
                        <Chip 
                          label={scenario.category} 
                          size="small" 
                          sx={{ mr: 1 }} 
                        />
                        <Chip 
                          label={scenario.difficulty} 
                          size="small" 
                          color={getDifficultyColor(scenario.difficulty)}
                        />
                      </Box>
                    </CardContent>
                    <CardActions>
                      <Button 
                        size="small" 
                        startIcon={<PlayArrow />}
                        onClick={() => navigate(`/scenarios/${scenario.id}`)}
                      >
                        Start
                      </Button>
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>
            <Box sx={{ mt: 2, textAlign: 'center' }}>
              <Button 
                variant="outlined" 
                onClick={() => navigate('/scenarios')}
              >
                View All Scenarios
              </Button>
            </Box>
          </Paper>
        </Grid>

        {/* Sidebar */}
        <Grid item xs={12} md={4}>
          {/* Recommendations */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recommended for You
            </Typography>
            <List>
              {recommendations.slice(0, 3).map((rec, index) => (
                <React.Fragment key={index}>
                  <ListItem alignItems="flex-start">
                    <ListItemAvatar>
                      <Avatar>
                        <Star />
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={rec.title}
                      secondary={rec.description}
                    />
                  </ListItem>
                  {index < recommendations.length - 1 && <Divider variant="inset" component="li" />}
                </React.Fragment>
              ))}
            </List>
            {recommendations.length === 0 && (
              <Typography variant="body2" color="textSecondary" textAlign="center">
                Complete more scenarios to get personalized recommendations
              </Typography>
            )}
          </Paper>

          {/* Recent Scores */}
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Scores
            </Typography>
            <List>
              {recentScores.map((score, index) => (
                <React.Fragment key={score.id}>
                  <ListItem>
                    <ListItemText
                      primary={`Score: ${score.scores.total_score.toFixed(1)}`}
                      secondary={new Date(score.submission_time).toLocaleDateString()}
                    />
                    <Chip 
                      label={score.scores.total_score.toFixed(0)}
                      size="small"
                      color={getScoreColor(score.scores.total_score)}
                    />
                  </ListItem>
                  {index < recentScores.length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
            {recentScores.length === 0 && (
              <Typography variant="body2" color="textSecondary" textAlign="center">
                No scores yet. Start a scenario to see your progress!
              </Typography>
            )}
            <Box sx={{ mt: 2, textAlign: 'center' }}>
              <Button 
                variant="outlined" 
                size="small"
                onClick={() => navigate('/scores')}
              >
                View All Scores
              </Button>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  )
}

export default Dashboard