import React, { useState, useEffect } from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  LinearProgress,
  Avatar,
  IconButton,
  Tooltip,
  useTheme,
  alpha,
  Fade,
  Zoom
} from '@mui/material'
import {
  TrendingUp,
  TrendingDown,
  Speed,
  Assessment,
  EmojiEvents,
  Psychology,
  Timeline,
  Insights,
  AutoGraph,
  School
} from '@mui/icons-material'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'
import { useAuthStore } from '../../stores/authStore'
import SkillRadarChart from './SkillRadarChart'
import PerformanceTimeline from './PerformanceTimeline'
import LearningInsights from './LearningInsights'
import CompetencyMatrix from './CompetencyMatrix'

const AnalyticsDashboard = () => {
  const theme = useTheme()
  const { user } = useAuthStore()
  const [analyticsData, setAnalyticsData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [selectedMetric, setSelectedMetric] = useState('overview')

  useEffect(() => {
    fetchAnalyticsData()
  }, [])

  const fetchAnalyticsData = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/api/analytics/dashboard?days=90`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setAnalyticsData(response.data.analytics)
      setLoading(false)
    } catch (error) {
      console.error('Failed to fetch analytics:', error)
      setLoading(false)
    }
  }

  const MetricCard = ({ title, value, subtitle, icon, trend, color = 'primary', onClick, delay = 0 }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.6, ease: 'easeOut' }}
    >
      <Card 
        sx={{ 
          height: '100%',
          cursor: onClick ? 'pointer' : 'default',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': onClick ? {
            transform: 'translateY(-4px)',
            boxShadow: theme.shadows[8],
            bgcolor: alpha(theme.palette[color].main, 0.02)
          } : {},
          background: `linear-gradient(135deg, ${alpha(theme.palette[color].main, 0.05)} 0%, ${alpha(theme.palette[color].main, 0.01)} 100%)`,
          border: `1px solid ${alpha(theme.palette[color].main, 0.1)}`
        }}
        onClick={onClick}
      >
        <CardContent sx={{ p: 3 }}>
          <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
            <Avatar 
              sx={{ 
                bgcolor: alpha(theme.palette[color].main, 0.1),
                color: theme.palette[color].main,
                width: 48,
                height: 48
              }}
            >
              {icon}
            </Avatar>
            {trend && (
              <Chip
                icon={trend.direction === 'up' ? <TrendingUp /> : <TrendingDown />}
                label={`${trend.value}%`}
                size="small"
                color={trend.direction === 'up' ? 'success' : 'error'}
                variant="outlined"
              />
            )}
          </Box>
          
          <Typography variant="h4" fontWeight="bold" color={`${color}.main`} mb={1}>
            {value}
          </Typography>
          
          <Typography variant="h6" color="textPrimary" mb={0.5}>
            {title}
          </Typography>
          
          <Typography variant="body2" color="textSecondary">
            {subtitle}
          </Typography>
        </CardContent>
      </Card>
    </motion.div>
  )

  const ProgressCard = ({ title, current, target, color = 'primary', icon, delay = 0 }) => {
    const progress = Math.min((current / target) * 100, 100)
    
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay, duration: 0.5 }}
      >
        <Card sx={{ height: '100%', background: `linear-gradient(135deg, ${alpha(theme.palette[color].main, 0.05)} 0%, transparent 100%)` }}>
          <CardContent sx={{ p: 3 }}>
            <Box display="flex" alignItems="center" mb={2}>
              <Avatar sx={{ bgcolor: alpha(theme.palette[color].main, 0.15), color: theme.palette[color].main, mr: 2 }}>
                {icon}
              </Avatar>
              <Typography variant="h6" fontWeight="600">
                {title}
              </Typography>
            </Box>
            
            <Box mb={2}>
              <Box display="flex" justifyContent="space-between" mb={1}>
                <Typography variant="body2" color="textSecondary">
                  Progress
                </Typography>
                <Typography variant="body2" fontWeight="600">
                  {current} / {target}
                </Typography>
              </Box>
              
              <LinearProgress
                variant="determinate"
                value={progress}
                sx={{
                  height: 8,
                  borderRadius: 4,
                  bgcolor: alpha(theme.palette[color].main, 0.1),
                  '& .MuiLinearProgress-bar': {
                    borderRadius: 4,
                    background: `linear-gradient(90deg, ${theme.palette[color].main}, ${theme.palette[color].dark})`
                  }
                }}
              />
            </Box>
            
            <Typography variant="body2" color="textSecondary">
              {progress >= 100 ? '🎉 Target achieved!' : `${(100 - progress).toFixed(0)}% to go`}
            </Typography>
          </CardContent>
        </Card>
      </motion.div>
    )
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        >
          <Assessment sx={{ fontSize: 48, color: theme.palette.primary.main }} />
        </motion.div>
      </Box>
    )
  }

  if (!analyticsData) {
    return (
      <Box textAlign="center" py={8}>
        <Assessment sx={{ fontSize: 64, color: theme.palette.grey[400], mb: 2 }} />
        <Typography variant="h5" color="textSecondary">
          No analytics data available yet
        </Typography>
        <Typography variant="body1" color="textSecondary">
          Complete some scenarios to see your progress!
        </Typography>
      </Box>
    )
  }

  const { performance_overview, skill_radar, learning_velocity, improvement_trends, time_analytics } = analyticsData

  return (
    <Box>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <Box mb={4}>
          <Typography variant="h4" fontWeight="bold" mb={1}>
            📊 Learning Analytics
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Track your progress and identify areas for improvement
          </Typography>
        </Box>
      </motion.div>

      {/* Overview Metrics */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Current Level"
            value={performance_overview.current_level}
            subtitle={`${performance_overview.total_scenarios} scenarios completed`}
            icon={<School />}
            color="primary"
            delay={0.1}
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Average Score"
            value={`${performance_overview.average_score}%`}
            subtitle="Recent performance"
            icon={<Assessment />}
            trend={{
              direction: performance_overview.performance_trend === 'improving' ? 'up' : 'down',
              value: Math.abs(performance_overview.improvement_rate).toFixed(1)
            }}
            color="success"
            delay={0.2}
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Best Score"
            value={`${performance_overview.best_score}%`}
            subtitle="Personal record"
            icon={<EmojiEvents />}
            color="warning"
            delay={0.3}
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Learning Velocity"
            value={`${learning_velocity.scenarios_per_week}`}
            subtitle="Scenarios per week"
            icon={<Speed />}
            trend={{
              direction: learning_velocity.velocity_trend === 'accelerating' ? 'up' : 'down',
              value: 15
            }}
            color="info"
            delay={0.4}
          />
        </Grid>
      </Grid>

      {/* Progress Tracking */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} md={6}>
          <ProgressCard
            title="Weekly Goal"
            current={learning_velocity.scenarios_per_week || 0}
            target={5}
            icon={<Timeline />}
            color="primary"
            delay={0.5}
          />
        </Grid>
        
        <Grid item xs={12} md={6}>
          <ProgressCard
            title="Mastery Progress"
            current={Math.round(performance_overview.average_score)}
            target={90}
            icon={<Psychology />}
            color="secondary"
            delay={0.6}
          />
        </Grid>
      </Grid>

      {/* Detailed Analytics */}
      <Grid container spacing={4}>
        {/* Skill Radar Chart */}
        <Grid item xs={12} lg={6}>
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.7, duration: 0.6 }}
          >
            <Card sx={{ height: 400 }}>
              <CardContent sx={{ p: 3, height: '100%' }}>
                <Box display="flex" alignItems="center" mb={3}>
                  <AutoGraph sx={{ mr: 2, color: theme.palette.primary.main }} />
                  <Typography variant="h6" fontWeight="600">
                    Skill Assessment
                  </Typography>
                </Box>
                <SkillRadarChart data={skill_radar} />
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Performance Timeline */}
        <Grid item xs={12} lg={6}>
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.8, duration: 0.6 }}
          >
            <Card sx={{ height: 400 }}>
              <CardContent sx={{ p: 3, height: '100%' }}>
                <Box display="flex" alignItems="center" mb={3}>
                  <Timeline sx={{ mr: 2, color: theme.palette.success.main }} />
                  <Typography variant="h6" fontWeight="600">
                    Performance Trend
                  </Typography>
                </Box>
                <PerformanceTimeline />
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Learning Insights */}
        <Grid item xs={12}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.9, duration: 0.6 }}
          >
            <Card>
              <CardContent sx={{ p: 3 }}>
                <Box display="flex" alignItems="center" mb={3}>
                  <Insights sx={{ mr: 2, color: theme.palette.info.main }} />
                  <Typography variant="h6" fontWeight="600">
                    Personalized Insights
                  </Typography>
                </Box>
                <LearningInsights />
              </CardContent>
            </Card>
          </motion.div>
        </Grid>
      </Grid>
    </Box>
  )
}

export default AnalyticsDashboard