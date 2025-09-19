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
  Divider,
  Fade,
  Grow,
  Slide
} from '@mui/material'
import {
  TrendingUp,
  Psychology,
  EmojiEvents,
  Timeline,
  PlayArrow,
  Star,
  AutoAwesome,
  Rocket,
  Shield,
  Code,
  Cloud,
  Security
} from '@mui/icons-material'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../stores/authStore'
import { useScenarioStore } from '../../stores/scenarioStore'
import { motion } from 'framer-motion'

const MotionCard = motion(Card)
const MotionPaper = motion(Paper)

const EnhancedDashboard = () => {
  const navigate = useNavigate()
  const { user } = useAuthStore()
  const { fetchScenarios, scenarios } = useScenarioStore()
  const [userStats, setUserStats] = useState({
    completed_scenarios: 5,
    average_score: 87.5,
    badges_earned: ['Security Expert', 'Cloud Architect'],
    current_streak: 7
  })
  const [recommendations] = useState([
    {
      title: "Advanced API Security",
      description: "Learn to secure REST APIs with OAuth 2.0 and JWT tokens"
    },
    {
      title: "Zero Trust Architecture", 
      description: "Design secure networks with zero trust principles"
    },
    {
      title: "Container Security",
      description: "Secure containerized applications and orchestration"
    }
  ])
  const [recentScores] = useState([
    { id: 1, scores: { total_score: 95.5 }, submission_time: new Date().toISOString() },
    { id: 2, scores: { total_score: 82.3 }, submission_time: new Date(Date.now() - 86400000).toISOString() },
    { id: 3, scores: { total_score: 91.7 }, submission_time: new Date(Date.now() - 2*86400000).toISOString() }
  ])

  useEffect(() => {
    fetchScenarios(0, 6)
  }, [fetchScenarios])

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'beginner': return 'success'
      case 'intermediate': return 'warning'  
      case 'expert': return 'error'
      default: return 'default'
    }
  }

  const getCategoryIcon = (category) => {
    const icons = {
      'web': Code,
      'api': Shield,
      'database': Security,
      'cloud': Cloud,
      'mobile': Psychology,
      'network': Timeline
    }
    return icons[category] || Code
  }

  const getScoreColor = (score) => {
    if (score >= 90) return 'success'
    if (score >= 70) return 'warning'
    return 'error'
  }

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        delayChildren: 0.3,
        staggerChildren: 0.1
      }
    }
  }

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1
    }
  }

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      {/* Welcome Header with Animation */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <Box sx={{ 
          mb: 4, 
          p: 3, 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          borderRadius: 3,
          color: 'white',
          position: 'relative',
          overflow: 'hidden'
        }}>
          <Box sx={{ 
            position: 'absolute', 
            top: -10, 
            right: -10, 
            opacity: 0.1 
          }}>
            <AutoAwesome sx={{ fontSize: 200 }} />
          </Box>
          <Typography variant="h3" gutterBottom sx={{ fontWeight: 'bold' }}>
            Welcome back, {user?.profile?.first_name || user?.email.split('@')[0]}! 🚀
          </Typography>
          <Typography variant="h6" sx={{ opacity: 0.9 }}>
            Ready to master threat modeling? Your security journey continues here.
          </Typography>
        </Box>
      </motion.div>

      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <Grid container spacing={3}>
          {/* Enhanced Stats Cards */}
          <Grid item xs={12} sm={6} md={3}>
            <motion.div variants={itemVariants}>
              <MotionCard
                whileHover={{ scale: 1.02, y: -5 }}
                transition={{ type: "spring", stiffness: 300 }}
                sx={{ 
                  background: 'linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%)',
                  color: 'white',
                  height: 120
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Box>
                      <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                        {userStats.completed_scenarios}
                      </Typography>
                      <Typography variant="body2" sx={{ opacity: 0.9 }}>
                        Scenarios Completed
                      </Typography>
                    </Box>
                    <Psychology sx={{ fontSize: 40, opacity: 0.8 }} />
                  </Box>
                </CardContent>
              </MotionCard>
            </motion.div>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <motion.div variants={itemVariants}>
              <MotionCard
                whileHover={{ scale: 1.02, y: -5 }}
                transition={{ type: "spring", stiffness: 300 }}
                sx={{ 
                  background: 'linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%)',
                  color: 'white',
                  height: 120
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Box>
                      <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                        {userStats.average_score}
                      </Typography>
                      <Typography variant="body2" sx={{ opacity: 0.9 }}>
                        Average Score
                      </Typography>
                    </Box>
                    <TrendingUp sx={{ fontSize: 40, opacity: 0.8 }} />
                  </Box>
                </CardContent>
              </MotionCard>
            </motion.div>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <motion.div variants={itemVariants}>
              <MotionCard
                whileHover={{ scale: 1.02, y: -5 }}
                transition={{ type: "spring", stiffness: 300 }}
                sx={{ 
                  background: 'linear-gradient(135deg, #A8EDEA 0%, #FED6E3 100%)',
                  color: '#2c3e50',
                  height: 120
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Box>
                      <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                        {userStats.badges_earned.length}
                      </Typography>
                      <Typography variant="body2" sx={{ opacity: 0.8 }}>
                        Badges Earned
                      </Typography>
                    </Box>
                    <EmojiEvents sx={{ fontSize: 40, opacity: 0.8 }} />
                  </Box>
                </CardContent>
              </MotionCard>
            </motion.div>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <motion.div variants={itemVariants}>
              <MotionCard
                whileHover={{ scale: 1.02, y: -5 }}
                transition={{ type: "spring", stiffness: 300 }}
                sx={{ 
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  color: 'white',
                  height: 120
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Box>
                      <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                        {userStats.current_streak}
                      </Typography>
                      <Typography variant="body2" sx={{ opacity: 0.9 }}>
                        Day Streak 🔥
                      </Typography>
                    </Box>
                    <Timeline sx={{ fontSize: 40, opacity: 0.8 }} />
                  </Box>
                </CardContent>
              </MotionCard>
            </motion.div>
          </Grid>

          {/* Enhanced Scenarios Section */}
          <Grid item xs={12} md={8}>
            <motion.div variants={itemVariants}>
              <MotionPaper 
                sx={{ p: 3, borderRadius: 3, boxShadow: '0 8px 32px rgba(0,0,0,0.1)' }}
                whileHover={{ boxShadow: '0 12px 48px rgba(0,0,0,0.15)' }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                  <Rocket sx={{ mr: 2, color: '#667eea' }} />
                  <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#2c3e50' }}>
                    Popular Scenarios
                  </Typography>
                </Box>
                <Grid container spacing={2}>
                  {scenarios.slice(0, 4).map((scenario, index) => {
                    const IconComponent = getCategoryIcon(scenario.category)
                    return (
                      <Grid item xs={12} sm={6} key={scenario.id}>
                        <motion.div
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: index * 0.1 }}
                        >
                          <Card 
                            variant="outlined" 
                            sx={{ 
                              cursor: 'pointer',
                              transition: 'all 0.3s ease',
                              '&:hover': {
                                transform: 'translateY(-4px)',
                                boxShadow: '0 8px 25px rgba(0,0,0,0.15)'
                              }
                            }}
                            onClick={() => navigate(`/scenarios/${scenario.id}`)}
                          >
                            <CardContent>
                              <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 2 }}>
                                <Avatar sx={{ 
                                  bgcolor: 'primary.main', 
                                  mr: 2,
                                  width: 48,
                                  height: 48
                                }}>
                                  <IconComponent />
                                </Avatar>
                                <Box sx={{ flex: 1 }}>
                                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                                    {scenario.title}
                                  </Typography>
                                  <Typography 
                                    variant="body2" 
                                    color="textSecondary" 
                                    sx={{ mb: 2, minHeight: 40 }}
                                  >
                                    {scenario.description.substring(0, 100)}...
                                  </Typography>
                                </Box>
                              </Box>
                              <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                                <Chip 
                                  label={scenario.category} 
                                  size="small" 
                                  color="primary"
                                  sx={{ fontWeight: 'bold' }}
                                />
                                <Chip 
                                  label={scenario.difficulty} 
                                  size="small" 
                                  color={getDifficultyColor(scenario.difficulty)}
                                  sx={{ fontWeight: 'bold' }}
                                />
                              </Box>
                            </CardContent>
                            <CardActions>
                              <Button 
                                size="small" 
                                startIcon={<PlayArrow />}
                                variant="outlined"
                                sx={{ fontWeight: 'bold' }}
                              >
                                Start Challenge
                              </Button>
                            </CardActions>
                          </Card>
                        </motion.div>
                      </Grid>
                    )
                  })}
                </Grid>
                <Box sx={{ mt: 3, textAlign: 'center' }}>
                  <Button 
                    variant="contained" 
                    size="large"
                    onClick={() => navigate('/scenarios')}
                    sx={{ 
                      borderRadius: 3,
                      px: 4,
                      py: 1.5,
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      '&:hover': {
                        background: 'linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%)',
                      }
                    }}
                  >
                    Explore All Scenarios
                  </Button>
                </Box>
              </MotionPaper>
            </motion.div>
          </Grid>

          {/* Enhanced Sidebar */}
          <Grid item xs={12} md={4}>
            <motion.div variants={itemVariants}>
              {/* Recommendations */}
              <MotionPaper sx={{ p: 3, mb: 3, borderRadius: 3, boxShadow: '0 8px 32px rgba(0,0,0,0.1)' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Star sx={{ mr: 2, color: '#FFD700' }} />
                  <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                    Recommended for You
                  </Typography>
                </Box>
                <List>
                  {recommendations.map((rec, index) => (
                    <React.Fragment key={index}>
                      <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                      >
                        <ListItem alignItems="flex-start" sx={{ 
                          borderRadius: 2,
                          '&:hover': { bgcolor: 'action.hover' }
                        }}>
                          <ListItemAvatar>
                            <Avatar sx={{ bgcolor: 'secondary.main' }}>
                              <AutoAwesome />
                            </Avatar>
                          </ListItemAvatar>
                          <ListItemText
                            primary={rec.title}
                            secondary={rec.description}
                            primaryTypographyProps={{ fontWeight: 'bold' }}
                          />
                        </ListItem>
                      </motion.div>
                      {index < recommendations.length - 1 && <Divider variant="inset" component="li" />}
                    </React.Fragment>
                  ))}
                </List>
              </MotionPaper>

              {/* Recent Scores */}
              <MotionPaper sx={{ p: 3, borderRadius: 3, boxShadow: '0 8px 32px rgba(0,0,0,0.1)' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <TrendingUp sx={{ mr: 2, color: '#4ECDC4' }} />
                  <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                    Recent Performance
                  </Typography>
                </Box>
                <List>
                  {recentScores.map((score, index) => (
                    <React.Fragment key={score.id}>
                      <motion.div
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: index * 0.1 }}
                      >
                        <ListItem sx={{ 
                          borderRadius: 2,
                          '&:hover': { bgcolor: 'action.hover' }
                        }}>
                          <ListItemText
                            primary={`Score: ${score.scores.total_score.toFixed(1)}%`}
                            secondary={new Date(score.submission_time).toLocaleDateString()}
                            primaryTypographyProps={{ fontWeight: 'bold' }}
                          />
                          <Chip 
                            label={score.scores.total_score.toFixed(0)}
                            size="small"
                            color={getScoreColor(score.scores.total_score)}
                            sx={{ fontWeight: 'bold' }}
                          />
                        </ListItem>
                      </motion.div>
                      {index < recentScores.length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
                <Box sx={{ mt: 2, textAlign: 'center' }}>
                  <Button 
                    variant="outlined" 
                    size="small"
                    onClick={() => navigate('/scores')}
                    sx={{ borderRadius: 2 }}
                  >
                    View All Scores
                  </Button>
                </Box>
              </MotionPaper>
            </motion.div>
          </Grid>
        </Grid>
      </motion.div>
    </Container>
  )
}

export default EnhancedDashboard