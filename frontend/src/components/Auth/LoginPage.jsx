import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  IconButton,
  InputAdornment,
  Divider,
  Card,
  CardContent,
  Fade,
  Slide
} from '@mui/material'
import {
  Visibility,
  VisibilityOff,
  Security,
  Shield,
  AutoAwesome,
  AccountCircle,
  VpnKey
} from '@mui/icons-material'
import { motion } from 'framer-motion'
import { useAuthStore } from '../../stores/authStore'
import LoadingSpinner from '../Common/LoadingSpinner'

const MotionPaper = motion(Paper)
const MotionCard = motion(Card)

const LoginPage = () => {
  const navigate = useNavigate()
  const { login, isLoading } = useAuthStore()
  
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    
    if (!formData.email || !formData.password) {
      setError('Please fill in all fields')
      return
    }

    const result = await login(formData.email, formData.password)
    if (result.success) {
      navigate('/')
    } else {
      setError(result.error)
    }
  }

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
    // Clear error when user starts typing
    if (error) setError('')
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

  if (isLoading) {
    return <LoadingSpinner />
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 2
      }}
    >
      <Container maxWidth="lg">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <Box
            sx={{
              display: 'flex',
              flexDirection: { xs: 'column', md: 'row' },
              alignItems: 'center',
              gap: 4,
              minHeight: '600px'
            }}
          >
            {/* Left side - Branding */}
            <Box
              sx={{
                flex: 1,
                textAlign: 'center',
                color: 'white',
                mb: { xs: 4, md: 0 }
              }}
            >
              <motion.div variants={itemVariants}>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 3 }}>
                    <Shield sx={{ fontSize: 60, mr: 2 }} />
                    <Typography variant="h2" sx={{ fontWeight: 'bold' }}>
                      ThreatModel
                    </Typography>
                </Box>
                <Typography variant="h4" sx={{ mb: 3, opacity: 0.9 }}>
                  Master Security Architecture
                </Typography>
                <Typography variant="h6" sx={{ mb: 4, opacity: 0.8, lineHeight: 1.6 }}>
                  Interactive learning platform for threat modeling. Design secure systems, validate architectures, and level up your security skills.
                </Typography>
                
                {/* Feature highlights */}
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, maxWidth: 400, mx: 'auto' }}>
                  {[
                    { icon: <Security />, text: 'Real-world scenarios' },
                    { icon: <AutoAwesome />, text: 'AI-powered validation' },
                    { icon: <Shield />, text: 'Expert feedback' }
                  ].map((feature, index) => (
                    <motion.div
                      key={index}
                      variants={itemVariants}
                      whileHover={{ scale: 1.05 }}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        {feature.icon}
                        <Typography variant="body1">{feature.text}</Typography>
                      </Box>
                    </motion.div>
                  ))}
                </Box>
              </motion.div>
            </Box>

            {/* Right side - Login form */}
            <Box sx={{ flex: 1, width: '100%', maxWidth: 450 }}>
              <motion.div variants={itemVariants}>
                <MotionPaper
                  elevation={20}
                  sx={{
                    p: 4,
                    borderRadius: 3,
                    background: 'rgba(255, 255, 255, 0.95)',
                    backdropFilter: 'blur(10px)',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                  }}
                  whileHover={{ y: -5, boxShadow: '0 20px 40px rgba(0,0,0,0.2)' }}
                >
                  <Box sx={{ textAlign: 'center', mb: 4 }}>
                    <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#2c3e50', mb: 1 }}>
                      Welcome Back
                    </Typography>
                    <Typography variant="body1" color="textSecondary">
                      Sign in to continue your learning journey
                    </Typography>
                  </Box>

                  {error && (
                    <Fade in={!!error}>
                      <Alert severity="error" sx={{ mb: 3, borderRadius: 2 }}>
                        {error}
                      </Alert>
                    </Fade>
                  )}

                  <form onSubmit={handleSubmit}>
                    <TextField
                      fullWidth
                      label="Email Address"
                      name="email"
                      type="email"
                      value={formData.email}
                      onChange={handleChange}
                      margin="normal"
                      variant="outlined"
                      autoComplete="email"
                      InputProps={{
                        startAdornment: (
                          <InputAdornment position="start">
                            <AccountCircle color="action" />
                          </InputAdornment>
                        ),
                      }}
                      sx={{
                        '& .MuiOutlinedInput-root': {
                          borderRadius: 2,
                          '&:hover fieldset': {
                            borderColor: '#667eea',
                          },
                          '&.Mui-focused fieldset': {
                            borderColor: '#667eea',
                          },
                        },
                      }}
                    />

                    <TextField
                      fullWidth
                      label="Password"
                      name="password"
                      type={showPassword ? 'text' : 'password'}
                      value={formData.password}
                      onChange={handleChange}
                      margin="normal"
                      variant="outlined"
                      autoComplete="current-password"
                      InputProps={{
                        startAdornment: (
                          <InputAdornment position="start">
                            <VpnKey color="action" />
                          </InputAdornment>
                        ),
                        endAdornment: (
                          <InputAdornment position="end">
                            <IconButton
                              onClick={() => setShowPassword(!showPassword)}
                              edge="end"
                            >
                              {showPassword ? <VisibilityOff /> : <Visibility />}
                            </IconButton>
                          </InputAdornment>
                        ),
                      }}
                      sx={{
                        '& .MuiOutlinedInput-root': {
                          borderRadius: 2,
                          '&:hover fieldset': {
                            borderColor: '#667eea',
                          },
                          '&.Mui-focused fieldset': {
                            borderColor: '#667eea',
                          },
                        },
                      }}
                    />

                    <Button
                      type="submit"
                      fullWidth
                      variant="contained"
                      disabled={isLoading}
                      sx={{
                        mt: 3,
                        mb: 2,
                        py: 1.5,
                        borderRadius: 2,
                        fontSize: '1.1rem',
                        fontWeight: 'bold',
                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        boxShadow: '0 4px 15px rgba(102, 126, 234, 0.4)',
                        '&:hover': {
                          background: 'linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%)',
                          boxShadow: '0 6px 20px rgba(102, 126, 234, 0.6)',
                        },
                        '&:disabled': {
                          background: '#ccc',
                          boxShadow: 'none',
                        },
                      }}
                    >
                      {isLoading ? 'Signing In...' : 'Sign In'}
                    </Button>

                    <Divider sx={{ my: 3 }}>
                      <Typography variant="body2" color="textSecondary">
                        or
                      </Typography>
                    </Divider>

                    <Box sx={{ textAlign: 'center' }}>
                      <Typography variant="body2" color="textSecondary">
                        New to ThreatModel?{' '}
                        <Link
                          to="/register"
                          style={{
                            color: '#667eea',
                            textDecoration: 'none',
                            fontWeight: 'bold',
                          }}
                        >
                          Create an account
                        </Link>
                      </Typography>
                    </Box>
                  </form>
                </MotionPaper>
              </motion.div>

              {/* Demo credentials */}
              <motion.div variants={itemVariants}>
                <MotionCard
                  sx={{
                    mt: 3,
                    background: 'rgba(255, 255, 255, 0.1)',
                    backdropFilter: 'blur(10px)',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                  }}
                  whileHover={{ scale: 1.02 }}
                >
                  <CardContent>
                    <Typography variant="h6" sx={{ color: 'white', mb: 2, textAlign: 'center' }}>
                      🚀 Demo Accounts
                    </Typography>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                      <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.9)' }}>
                        <strong>Student:</strong> student@example.com / student123
                      </Typography>
                      <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.9)' }}>
                        <strong>Admin:</strong> admin@threatmodeling.com / admin123
                      </Typography>
                    </Box>
                  </CardContent>
                </MotionCard>
              </motion.div>
            </Box>
          </Box>
        </motion.div>
      </Container>
    </Box>
  )
}

export default LoginPage