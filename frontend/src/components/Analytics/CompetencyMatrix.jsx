import React from 'react'
import {
  Box,
  Typography,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  Grid,
  useTheme,
  alpha
} from '@mui/material'
import {
  TrendingUp,
  TrendingDown,
  TrendingFlat,
  Security,
  Architecture,
  Speed,
  Assignment
} from '@mui/icons-material'
import { motion } from 'framer-motion'

const CompetencyMatrix = ({ competencyData = {} }) => {
  const theme = useTheme()

  const defaultCompetencies = {
    Security: { current_level: 'Novice', trend: 'stable', mastery_percentage: 0 },
    Architecture: { current_level: 'Novice', trend: 'stable', mastery_percentage: 0 },
    Performance: { current_level: 'Novice', trend: 'stable', mastery_percentage: 0 },
    Completeness: { current_level: 'Novice', trend: 'stable', mastery_percentage: 0 }
  }

  const competencies = { ...defaultCompetencies, ...competencyData }

  const getLevelColor = (level) => {
    switch (level.toLowerCase()) {
      case 'expert':
        return theme.palette.success.main
      case 'proficient':
        return theme.palette.info.main
      case 'competent':
        return theme.palette.warning.main
      case 'developing':
        return theme.palette.orange?.main || '#ff9800'
      case 'novice':
      default:
        return theme.palette.grey[500]
    }
  }

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'improving':
        return <TrendingUp color="success" />
      case 'declining':
        return <TrendingDown color="error" />
      case 'stable':
      default:
        return <TrendingFlat color="info" />
    }
  }

  const getSkillIcon = (skill) => {
    switch (skill) {
      case 'Security':
        return <Security />
      case 'Architecture':
        return <Architecture />
      case 'Performance':
        return <Speed />
      case 'Completeness':
        return <Assignment />
      default:
        return <Assignment />
    }
  }

  const CompetencyCard = ({ skill, data, index }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.5 }}
    >
      <Card
        sx={{
          height: '100%',
          background: `linear-gradient(135deg, ${alpha(getLevelColor(data.current_level), 0.1)} 0%, transparent 100%)`,
          border: `1px solid ${alpha(getLevelColor(data.current_level), 0.2)}`,
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            transform: 'translateY(-4px)',
            boxShadow: theme.shadows[8]
          }
        }}
      >
        <CardContent sx={{ p: 3 }}>
          {/* Header */}
          <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
            <Box display="flex" alignItems="center" gap={1}>
              <Box sx={{ color: getLevelColor(data.current_level) }}>
                {getSkillIcon(skill)}
              </Box>
              <Typography variant="h6" fontWeight="600">
                {skill}
              </Typography>
            </Box>
            {getTrendIcon(data.trend)}
          </Box>

          {/* Current Level */}
          <Box mb={2}>
            <Typography variant="body2" color="textSecondary" mb={1}>
              Current Level
            </Typography>
            <Chip
              label={data.current_level}
              sx={{
                bgcolor: alpha(getLevelColor(data.current_level), 0.1),
                color: getLevelColor(data.current_level),
                fontWeight: 'bold',
                fontSize: '0.75rem'
              }}
            />
          </Box>

          {/* Mastery Progress */}
          <Box>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
              <Typography variant="body2" color="textSecondary">
                Mastery Progress
              </Typography>
              <Typography variant="body2" fontWeight="600">
                {data.mastery_percentage}%
              </Typography>
            </Box>
            
            <LinearProgress
              variant="determinate"
              value={data.mastery_percentage}
              sx={{
                height: 8,
                borderRadius: 4,
                bgcolor: alpha(getLevelColor(data.current_level), 0.1),
                '& .MuiLinearProgress-bar': {
                  borderRadius: 4,
                  bgcolor: getLevelColor(data.current_level)
                }
              }}
            />
            
            <Typography variant="caption" color="textSecondary" sx={{ mt: 0.5 }}>
              {data.mastery_percentage >= 90 
                ? '🎯 Mastery achieved!' 
                : data.mastery_percentage >= 70 
                  ? '💪 Almost there!' 
                  : '📚 Keep learning!'}
            </Typography>
          </Box>
        </CardContent>
      </Card>
    </motion.div>
  )

  if (!competencyData || Object.keys(competencyData).length === 0) {
    return (
      <Box textAlign="center" py={4}>
        <Assignment sx={{ fontSize: 48, color: theme.palette.grey[400], mb: 2 }} />
        <Typography variant="body1" color="textSecondary">
          Complete more scenarios to see your competency matrix
        </Typography>
      </Box>
    )
  }

  return (
    <Box>
      <Grid container spacing={3}>
        {Object.entries(competencies).map(([skill, data], index) => (
          <Grid item xs={12} sm={6} md={3} key={skill}>
            <CompetencyCard skill={skill} data={data} index={index} />
          </Grid>
        ))}
      </Grid>

      {/* Overall Progress Summary */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6, duration: 0.5 }}
      >
        <Card sx={{ mt: 3, background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.05)} 0%, transparent 100%)` }}>
          <CardContent sx={{ p: 3 }}>
            <Typography variant="h6" fontWeight="600" mb={2}>
              Overall Progress Summary
            </Typography>
            
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Box textAlign="center">
                  <Typography variant="h3" fontWeight="bold" color="primary.main">
                    {Object.values(competencies).reduce((acc, comp) => acc + comp.mastery_percentage, 0) / Object.keys(competencies).length}%
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Average Mastery
                  </Typography>
                </Box>
              </Grid>
              
              <Grid item xs={12} md={4}>
                <Box textAlign="center">
                  <Typography variant="h3" fontWeight="bold" color="success.main">
                    {Object.values(competencies).filter(comp => comp.trend === 'improving').length}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Improving Skills
                  </Typography>
                </Box>
              </Grid>
              
              <Grid item xs={12} md={4}>
                <Box textAlign="center">
                  <Typography variant="h3" fontWeight="bold" color="warning.main">
                    {Object.values(competencies).filter(comp => ['proficient', 'expert'].includes(comp.current_level.toLowerCase())).length}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Advanced Skills
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </motion.div>
    </Box>
  )
}

export default CompetencyMatrix