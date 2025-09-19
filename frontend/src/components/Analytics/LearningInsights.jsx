import React, { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Card,
  CardContent,
  Chip,
  Avatar,
  Grid,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  useTheme,
  alpha,
  CircularProgress
} from '@mui/material'
import {
  TrendingUp,
  TrendingDown,
  Lightbulb,
  Star,
  Timeline,
  Assessment,
  Speed,
  EmojiEvents,
  Psychology,
  School
} from '@mui/icons-material'
import { motion } from 'framer-motion'
import axios from 'axios'

const LearningInsights = () => {
  const theme = useTheme()
  const [insights, setInsights] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchInsights()
  }, [])

  const fetchInsights = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/api/analytics/learning-insights`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setInsights(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Failed to fetch insights:', error)
      setLoading(false)
    }
  }

  const getInsightIcon = (insight) => {
    if (insight.includes('improving')) return <TrendingUp color="success" />
    if (insight.includes('declining')) return <TrendingDown color="error" />
    if (insight.includes('strongest')) return <Star color="warning" />
    if (insight.includes('efficient')) return <Speed color="info" />
    if (insight.includes('consistent')) return <Assessment color="primary" />
    return <Psychology color="secondary" />
  }

  const getRecommendationIcon = (recommendation) => {
    if (recommendation.includes('scenarios')) return <School />
    if (recommendation.includes('feedback')) return <Assessment />
    if (recommendation.includes('time') || recommendation.includes('approach')) return <Timeline />
    return <Lightbulb />
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    )
  }

  if (!insights) {
    return (
      <Box textAlign="center" py={4}>
        <Psychology sx={{ fontSize: 48, color: theme.palette.grey[400], mb: 2 }} />
        <Typography variant="body1" color="textSecondary">
          No insights available yet
        </Typography>
      </Box>
    )
  }

  return (
    <Box>
      <Grid container spacing={3}>
        {/* Performance Summary */}
        <Grid item xs={12} md={4}>
          <Card sx={{ 
            height: '100%',
            background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.1)} 0%, transparent 100%)`
          }}>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Avatar sx={{ bgcolor: alpha(theme.palette.primary.main, 0.1), color: theme.palette.primary.main, mr: 2 }}>
                  <Assessment />
                </Avatar>
                <Typography variant="h6" fontWeight="600">
                  Performance Summary
                </Typography>
              </Box>
              
              <Box mb={2}>
                <Typography variant="body2" color="textSecondary" mb={0.5}>
                  Total Attempts
                </Typography>
                <Typography variant="h4" fontWeight="bold" color="primary.main">
                  {insights.performance_summary.total_attempts}
                </Typography>
              </Box>
              
              <Box mb={2}>
                <Typography variant="body2" color="textSecondary" mb={0.5}>
                  Average Score
                </Typography>
                <Typography variant="h4" fontWeight="bold" color="success.main">
                  {insights.performance_summary.average_score}%
                </Typography>
              </Box>
              
              <Box>
                <Typography variant="body2" color="textSecondary" mb={1}>
                  Skill Breakdown
                </Typography>
                <Box display="flex" flexWrap="wrap" gap={0.5}>
                  {Object.entries(insights.performance_summary.skill_breakdown).map(([skill, score]) => (
                    <Chip
                      key={skill}
                      label={`${skill}: ${score}%`}
                      size="small"
                      color={score >= 80 ? 'success' : score >= 60 ? 'warning' : 'error'}
                      variant="outlined"
                    />
                  ))}
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Key Insights */}
        <Grid item xs={12} md={8}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" fontWeight="600" mb={2} sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Lightbulb color="warning" />
                Key Insights
              </Typography>
              
              <List sx={{ p: 0 }}>
                {insights.insights.map((insight, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <ListItem sx={{ px: 0, py: 1 }}>
                      <ListItemIcon>
                        {getInsightIcon(insight)}
                      </ListItemIcon>
                      <ListItemText
                        primary={insight}
                        primaryTypographyProps={{
                          variant: 'body2',
                          fontWeight: 500
                        }}
                      />
                    </ListItem>
                  </motion.div>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Recommendations */}
        <Grid item xs={12} md={6}>
          <Card sx={{ 
            height: '100%',
            background: `linear-gradient(135deg, ${alpha(theme.palette.success.main, 0.1)} 0%, transparent 100%)`
          }}>
            <CardContent>
              <Typography variant="h6" fontWeight="600" mb={2} sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <EmojiEvents color="success" />
                Recommendations
              </Typography>
              
              <List sx={{ p: 0 }}>
                {insights.recommendations.map((recommendation, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 + index * 0.1 }}
                  >
                    <ListItem sx={{ px: 0, py: 1 }}>
                      <ListItemIcon>
                        {getRecommendationIcon(recommendation)}
                      </ListItemIcon>
                      <ListItemText
                        primary={recommendation}
                        primaryTypographyProps={{
                          variant: 'body2',
                          color: 'textSecondary'
                        }}
                      />
                    </ListItem>
                  </motion.div>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Focus Areas & Next Steps */}
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" fontWeight="600" mb={2} sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Timeline color="info" />
                Next Steps
              </Typography>
              
              {insights.focus_areas.length > 0 && (
                <Box mb={3}>
                  <Typography variant="subtitle2" color="textSecondary" mb={1}>
                    Focus Areas
                  </Typography>
                  <Box display="flex" flexWrap="wrap" gap={1}>
                    {insights.focus_areas.map((area, index) => (
                      <Chip
                        key={index}
                        label={area}
                        color="error"
                        variant="outlined"
                        size="small"
                      />
                    ))}
                  </Box>
                </Box>
              )}
              
              <List sx={{ p: 0 }}>
                {insights.next_steps.map((step, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 1 + index * 0.1 }}
                  >
                    <ListItem sx={{ px: 0, py: 0.5 }}>
                      <ListItemIcon>
                        <Box
                          sx={{
                            width: 24,
                            height: 24,
                            borderRadius: '50%',
                            bgcolor: theme.palette.info.main,
                            color: 'white',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontSize: '0.75rem',
                            fontWeight: 'bold'
                          }}
                        >
                          {index + 1}
                        </Box>
                      </ListItemIcon>
                      <ListItemText
                        primary={step}
                        primaryTypographyProps={{
                          variant: 'body2',
                          fontWeight: 500
                        }}
                      />
                    </ListItem>
                  </motion.div>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}

export default LearningInsights