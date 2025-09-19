import React, { useState, useEffect } from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Avatar,
  Chip,
  LinearProgress,
  Tooltip,
  Badge,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  useTheme,
  alpha,
  Fade,
  Zoom,
  Stack
} from '@mui/material'
import {
  EmojiEvents,
  Star,
  Lock,
  TrendingUp,
  Speed,
  Security,
  Architecture,
  Timeline,
  School,
  Close,
  CheckCircle,
  RadioButtonUnchecked
} from '@mui/icons-material'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'
import { useAuthStore } from '../../stores/authStore'
import toast from 'react-hot-toast'

const AchievementsBadges = () => {
  const theme = useTheme()
  const { user } = useAuthStore()
  const [achievements, setAchievements] = useState(null)
  const [loading, setLoading] = useState(true)
  const [selectedBadge, setSelectedBadge] = useState(null)
  const [newAchievements, setNewAchievements] = useState([])

  useEffect(() => {
    fetchAchievements()
    checkNewAchievements()
  }, [])

  const fetchAchievements = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/api/gamification/achievements`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setAchievements(response.data.achievements)
      setLoading(false)
    } catch (error) {
      console.error('Failed to fetch achievements:', error)
      setLoading(false)
    }
  }

  const checkNewAchievements = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/api/gamification/check-achievements`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      })
      
      if (response.data.new_achievements.length > 0) {
        setNewAchievements(response.data.new_achievements)
        response.data.new_achievements.forEach(achievement => {
          toast.success(`🏆 New Achievement: ${achievement.name}!`, {
            duration: 5000,
            position: 'top-center'
          })
        })
        fetchAchievements() // Refresh to show new badges
      }
    } catch (error) {
      console.error('Failed to check achievements:', error)
    }
  }

  const getTierColor = (tier) => {
    const colors = {
      bronze: '#CD7F32',
      silver: '#C0C0C0', 
      gold: '#FFD700',
      platinum: '#E5E4E2'
    }
    return colors[tier] || '#9E9E9E'
  }

  const getTierGradient = (tier) => {
    const gradients = {
      bronze: 'linear-gradient(135deg, #CD7F32 0%, #B8860B 100%)',
      silver: 'linear-gradient(135deg, #C0C0C0 0%, #A9A9A9 100%)',
      gold: 'linear-gradient(135deg, #FFD700 0%, #FFA500 100%)',
      platinum: 'linear-gradient(135deg, #E5E4E2 0%, #D3D3D3 100%)'
    }
    return gradients[tier] || 'linear-gradient(135deg, #9E9E9E 0%, #757575 100%)'
  }

  const BadgeCard = ({ badge, index }) => (
    <motion.div
      initial={{ opacity: 0, scale: 0.8, y: 20 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.5 }}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
    >
      <Card
        sx={{
          height: 200,
          cursor: 'pointer',
          position: 'relative',
          overflow: 'visible',
          background: badge.earned 
            ? getTierGradient(badge.tier)
            : `linear-gradient(135deg, ${alpha(theme.palette.grey[500], 0.1)} 0%, ${alpha(theme.palette.grey[500], 0.05)} 100%)`,
          border: badge.earned 
            ? `2px solid ${getTierColor(badge.tier)}`
            : `2px dashed ${theme.palette.grey[300]}`,
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            boxShadow: badge.earned ? theme.shadows[12] : theme.shadows[4],
            transform: 'translateY(-4px)'
          }
        }}
        onClick={() => setSelectedBadge(badge)}
      >
        {badge.earned && (
          <Box
            sx={{
              position: 'absolute',
              top: -10,
              right: -10,
              zIndex: 1
            }}
          >
            <Avatar
              sx={{
                bgcolor: theme.palette.success.main,
                width: 24,
                height: 24
              }}
            >
              <CheckCircle sx={{ fontSize: 16 }} />
            </Avatar>
          </Box>
        )}

        <CardContent sx={{ 
          p: 3, 
          height: '100%', 
          display: 'flex', 
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center'
        }}>
          {/* Badge Icon */}
          <Box sx={{ mb: 2 }}>
            <Avatar
              sx={{
                width: 64,
                height: 64,
                fontSize: '2rem',
                background: badge.earned 
                  ? 'rgba(255, 255, 255, 0.9)'
                  : alpha(theme.palette.grey[400], 0.3),
                color: badge.earned ? getTierColor(badge.tier) : theme.palette.grey[500],
                border: `3px solid ${badge.earned ? getTierColor(badge.tier) : theme.palette.grey[400]}`,
                filter: badge.earned ? 'none' : 'grayscale(100%)'
              }}
            >
              {badge.icon || '🏆'}
            </Avatar>
          </Box>

          {/* Badge Name */}
          <Typography 
            variant="h6" 
            fontWeight="bold" 
            mb={1}
            color={badge.earned ? 'white' : 'textSecondary'}
            sx={{ textShadow: badge.earned ? '1px 1px 2px rgba(0,0,0,0.3)' : 'none' }}
          >
            {badge.name}
          </Typography>

          {/* Tier Chip */}
          <Chip
            label={badge.tier?.toUpperCase() || 'COMMON'}
            size="small"
            sx={{
              background: badge.earned 
                ? 'rgba(255, 255, 255, 0.9)'
                : alpha(theme.palette.grey[400], 0.2),
              color: badge.earned ? getTierColor(badge.tier) : theme.palette.grey[600],
              fontWeight: 'bold',
              mb: 1
            }}
          />

          {/* Progress Bar (for unearned badges) */}
          {!badge.earned && badge.progress && (
            <Box sx={{ width: '100%', mt: 'auto' }}>
              <Box display="flex" justifyContent="space-between" mb={0.5}>
                <Typography variant="caption" color="textSecondary">
                  Progress
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  {badge.progress.percentage?.toFixed(0) || 0}%
                </Typography>
              </Box>
              <LinearProgress
                variant="determinate" 
                value={badge.progress.percentage || 0}
                sx={{
                  height: 6,
                  borderRadius: 3,
                  bgcolor: alpha(theme.palette.grey[400], 0.2),
                  '& .MuiLinearProgress-bar': {
                    borderRadius: 3,
                    background: getTierGradient(badge.tier)
                  }
                }}
              />
            </Box>
          )}
        </CardContent>
      </Card>
    </motion.div>
  )

  const BadgeDetailDialog = () => (
    <Dialog
      open={!!selectedBadge}
      onClose={() => setSelectedBadge(null)}
      maxWidth="sm"
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: 3,
          background: selectedBadge?.earned 
            ? getTierGradient(selectedBadge.tier)
            : theme.palette.background.paper
        }
      }}
    >
      <DialogTitle sx={{ 
        pb: 1,
        color: selectedBadge?.earned ? 'white' : 'inherit',
        textShadow: selectedBadge?.earned ? '1px 1px 2px rgba(0,0,0,0.5)' : 'none'
      }}>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box display="flex" alignItems="center" gap={2}>
            <Avatar
              sx={{
                width: 56,
                height: 56,
                fontSize: '1.5rem',
                background: selectedBadge?.earned 
                  ? 'rgba(255, 255, 255, 0.9)'
                  : alpha(theme.palette.grey[400], 0.3),
                color: selectedBadge?.earned ? getTierColor(selectedBadge.tier) : theme.palette.grey[500],
                border: `3px solid ${selectedBadge?.earned ? getTierColor(selectedBadge.tier) : theme.palette.grey[400]}`
              }}
            >
              {selectedBadge?.icon || '🏆'}
            </Avatar>
            <Box>
              <Typography variant="h5" fontWeight="bold">
                {selectedBadge?.name}
              </Typography>
              <Chip
                label={selectedBadge?.tier?.toUpperCase() || 'COMMON'}
                size="small"
                sx={{
                  background: selectedBadge?.earned 
                    ? 'rgba(255, 255, 255, 0.9)'
                    : alpha(theme.palette.grey[400], 0.2),
                  color: selectedBadge?.earned ? getTierColor(selectedBadge.tier) : theme.palette.grey[600],
                  fontWeight: 'bold'
                }}
              />
            </Box>
          </Box>
          <IconButton 
            onClick={() => setSelectedBadge(null)}
            sx={{ color: selectedBadge?.earned ? 'white' : 'inherit' }}
          >
            <Close />
          </IconButton>
        </Box>
      </DialogTitle>
      
      <DialogContent sx={{ 
        pb: 4,
        color: selectedBadge?.earned ? 'white' : 'inherit'
      }}>
        <Typography variant="body1" mb={3} sx={{ 
          textShadow: selectedBadge?.earned ? '1px 1px 2px rgba(0,0,0,0.3)' : 'none'
        }}>
          {selectedBadge?.description}
        </Typography>

        {selectedBadge?.earned ? (
          <Box
            sx={{
              p: 2,
              borderRadius: 2,
              background: 'rgba(255, 255, 255, 0.1)',
              textAlign: 'center'
            }}
          >
            <CheckCircle sx={{ fontSize: 48, mb: 1 }} />
            <Typography variant="h6" fontWeight="bold">
              Achievement Unlocked!
            </Typography>
            <Typography variant="body2">
              Earned on {selectedBadge.earned_at ? new Date(selectedBadge.earned_at).toLocaleDateString() : 'N/A'}
            </Typography>
          </Box>
        ) : (
          <Box>
            <Typography variant="h6" mb={2} fontWeight="600">
              Progress to Unlock
            </Typography>
            
            {selectedBadge?.progress && (
              <Box sx={{
                p: 2,
                borderRadius: 2,
                bgcolor: alpha(theme.palette.grey[100], 0.5),
                mb: 2
              }}>
                <Box display="flex" justifyContent="space-between" mb={1}>
                  <Typography variant="body2">
                    Current Progress
                  </Typography>
                  <Typography variant="body2" fontWeight="600">
                    {selectedBadge.progress.current} / {selectedBadge.progress.target}
                  </Typography>
                </Box>
                
                <LinearProgress
                  variant="determinate" 
                  value={selectedBadge.progress.percentage || 0}
                  sx={{
                    height: 8,
                    borderRadius: 4,
                    mb: 1,
                    '& .MuiLinearProgress-bar': {
                      borderRadius: 4,
                      background: getTierGradient(selectedBadge.tier)
                    }
                  }}
                />
                
                <Typography variant="caption" color="textSecondary">
                  {(selectedBadge.progress.percentage || 0).toFixed(1)}% complete
                </Typography>
              </Box>
            )}
            
            <Typography variant="body2" color="textSecondary">
              💡 Keep working on your threat modeling skills to unlock this achievement!
            </Typography>
          </Box>
        )}
      </DialogContent>
    </Dialog>
  )

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        >
          <EmojiEvents sx={{ fontSize: 48, color: theme.palette.primary.main }} />
        </motion.div>
      </Box>
    )
  }

  if (!achievements) {
    return (
      <Box textAlign="center" py={8}>
        <EmojiEvents sx={{ fontSize: 64, color: theme.palette.grey[400], mb: 2 }} />
        <Typography variant="h5" color="textSecondary">
          No achievements data available
        </Typography>
      </Box>
    )
  }

  const earnedBadges = achievements.badges.filter(badge => badge.earned)
  const unearnedBadges = achievements.badges.filter(badge => !badge.earned)

  return (
    <Box>
      {/* Header with Stats */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <Box mb={4}>
          <Typography variant="h4" fontWeight="bold" mb={1}>
            🏆 Achievements & Badges
          </Typography>
          <Typography variant="body1" color="textSecondary" mb={3}>
            Showcase your threat modeling mastery
          </Typography>
          
          {/* Stats Bar */}
          <Box
            sx={{
              p: 3,
              borderRadius: 3,
              background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.1)} 0%, ${alpha(theme.palette.secondary.main, 0.1)} 100%)`,
              border: `1px solid ${alpha(theme.palette.primary.main, 0.2)}`
            }}
          >
            <Grid container spacing={4} alignItems="center">
              <Grid item xs={12} sm={6} md={3}>
                <Box textAlign="center">
                  <Typography variant="h3" fontWeight="bold" color="primary.main">
                    {achievements.earned_badges}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Badges Earned
                  </Typography>
                </Box>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Box textAlign="center">
                  <Typography variant="h3" fontWeight="bold" color="secondary.main">
                    {achievements.completion_percentage.toFixed(0)}%
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Completion
                  </Typography>
                </Box>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Box textAlign="center">
                  <Typography variant="h3" fontWeight="bold" color="warning.main">
                    {achievements.user_level?.current_level || 1}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Current Level
                  </Typography>
                </Box>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Box textAlign="center">
                  <Typography variant="h3" fontWeight="bold" color="success.main">
                    {achievements.experience_points || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Experience Points
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </motion.div>

      {/* Earned Badges */}
      {earnedBadges.length > 0 && (
        <Box mb={6}>
          <Typography variant="h5" fontWeight="bold" mb={3} sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Star sx={{ color: theme.palette.warning.main }} />
            Earned Badges ({earnedBadges.length})
          </Typography>
          
          <Grid container spacing={3}>
            {earnedBadges.map((badge, index) => (
              <Grid item xs={12} sm={6} md={4} lg={3} key={badge.badge_id}>
                <BadgeCard badge={badge} index={index} />
              </Grid>
            ))}
          </Grid>
        </Box>
      )}

      {/* Unearned Badges */}
      {unearnedBadges.length > 0 && (
        <Box>
          <Typography variant="h5" fontWeight="bold" mb={3} sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Lock sx={{ color: theme.palette.grey[500] }} />
            Available Badges ({unearnedBadges.length})
          </Typography>
          
          <Grid container spacing={3}>
            {unearnedBadges.map((badge, index) => (
              <Grid item xs={12} sm={6} md={4} lg={3} key={badge.badge_id}>
                <BadgeCard badge={badge} index={index + earnedBadges.length} />
              </Grid>
            ))}
          </Grid>
        </Box>
      )}

      {/* Badge Detail Dialog */}
      <BadgeDetailDialog />
    </Box>
  )
}

export default AchievementsBadges