import React, { useState } from 'react'
import {
  Container,
  Grid,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Avatar,
  Card,
  CardContent,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider
} from '@mui/material'
import {
  Person,
  Email,
  Edit,
  Save,
  Cancel,
  EmojiEvents,
  TrendingUp,
  AccessTime,
  Star
} from '@mui/icons-material'
import { useForm } from 'react-hook-form'
import { useAuthStore } from '../../stores/authStore'
import toast from 'react-hot-toast'

const Profile = () => {
  const { user, updateProfile } = useAuthStore()
  const [isEditing, setIsEditing] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors }
  } = useForm({
    defaultValues: {
      first_name: user?.profile?.first_name || '',
      last_name: user?.profile?.last_name || '',
      bio: user?.profile?.bio || '',
      theme: user?.preferences?.theme || 'light',
      notifications: user?.preferences?.notifications || true
    }
  })

  const handleEdit = () => {
    setIsEditing(true)
    reset({
      first_name: user?.profile?.first_name || '',
      last_name: user?.profile?.last_name || '',
      bio: user?.profile?.bio || '',
      theme: user?.preferences?.theme || 'light',
      notifications: user?.preferences?.notifications || true
    })
  }

  const handleCancel = () => {
    setIsEditing(false)
    reset()
  }

  const onSubmit = async (data) => {
    setIsLoading(true)
    try {
      const result = await updateProfile(data)
      if (result.success) {
        setIsEditing(false)
        toast.success('Profile updated successfully')
      }
    } catch (error) {
      console.error('Failed to update profile:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const getInitials = () => {
    const firstName = user?.profile?.first_name || ''
    const lastName = user?.profile?.last_name || ''
    if (firstName && lastName) {
      return `${firstName[0]}${lastName[0]}`
    }
    return user?.email?.[0]?.toUpperCase() || 'U'
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Profile
      </Typography>

      <Grid container spacing={3}>
        {/* Profile Information */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
              <Typography variant="h6">
                Personal Information
              </Typography>
              {!isEditing && (
                <Button
                  startIcon={<Edit />}
                  onClick={handleEdit}
                >
                  Edit Profile
                </Button>
              )}
            </Box>

            <Box component="form" onSubmit={handleSubmit(onSubmit)}>
              <Grid container spacing={3}>
                {/* Avatar */}
                <Grid item xs={12} sx={{ textAlign: 'center', mb: 2 }}>
                  <Avatar
                    sx={{ 
                      width: 100, 
                      height: 100, 
                      margin: '0 auto',
                      fontSize: '2rem'
                    }}
                    src={user?.profile?.avatar_url}
                  >
                    {getInitials()}
                  </Avatar>
                </Grid>

                {/* Email (readonly) */}
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Email"
                    value={user?.email || ''}
                    disabled
                    InputProps={{
                      startAdornment: <Email sx={{ mr: 1, color: 'action.active' }} />
                    }}
                  />
                </Grid>

                {/* First Name */}
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="First Name"
                    disabled={!isEditing}
                    {...register('first_name', {
                      required: 'First name is required'
                    })}
                    error={!!errors.first_name}
                    helperText={errors.first_name?.message}
                  />
                </Grid>

                {/* Last Name */}
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Last Name"
                    disabled={!isEditing}
                    {...register('last_name', {
                      required: 'Last name is required'
                    })}
                    error={!!errors.last_name}
                    helperText={errors.last_name?.message}
                  />
                </Grid>

                {/* Bio */}
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Bio"
                    multiline
                    rows={3}
                    disabled={!isEditing}
                    {...register('bio')}
                    placeholder="Tell us about yourself..."
                  />
                </Grid>

                {/* Action Buttons */}
                {isEditing && (
                  <Grid item xs={12}>
                    <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
                      <Button
                        startIcon={<Cancel />}
                        onClick={handleCancel}
                      >
                        Cancel
                      </Button>
                      <Button
                        type="submit"
                        variant="contained"
                        startIcon={<Save />}
                        disabled={isLoading}
                      >
                        Save Changes
                      </Button>
                    </Box>
                  </Grid>
                )}
              </Grid>
            </Box>
          </Paper>
        </Grid>

        {/* Stats & Achievements */}
        <Grid item xs={12} md={4}>
          {/* User Stats */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Your Statistics
              </Typography>
              
              <List>
                <ListItem>
                  <ListItemIcon>
                    <Star color="primary" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Level"
                    secondary={user?.progress?.level || 1}
                  />
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <TrendingUp color="success" />
                  </ListItemIcon>
                  <ListItemText
                    primary="XP Points"
                    secondary={user?.progress?.experience_points || 0}
                  />
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <AccessTime color="info" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Completed Scenarios"
                    secondary={user?.progress?.completed_scenarios?.length || 0}
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>

          {/* Achievements */}
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Achievements
              </Typography>
              
              {user?.progress?.badges?.length > 0 ? (
                <Box>
                  {user.progress.badges.map((badge, index) => (
                    <Chip
                      key={index}
                      label={badge}
                      icon={<EmojiEvents />}
                      color="primary"
                      variant="outlined"
                      sx={{ m: 0.5 }}
                    />
                  ))}
                </Box>
              ) : (
                <Typography variant="body2" color="textSecondary" sx={{ textAlign: 'center', py: 2 }}>
                  No achievements yet. Complete scenarios to earn badges!
                </Typography>
              )}
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="body2" color="textSecondary">
                Member since: {new Date(user?.created_at).toLocaleDateString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  )
}

export default Profile