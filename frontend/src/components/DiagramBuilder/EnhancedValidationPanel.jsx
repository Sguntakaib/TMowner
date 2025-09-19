import React, { useState, useEffect } from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Collapse,
  IconButton,
  Alert,
  LinearProgress,
  Tooltip,
  useTheme,
  alpha,
  Badge,
  Divider
} from '@mui/material'
import {
  Error,
  Warning,
  Info,
  CheckCircle,
  ExpandMore,
  ExpandLess,
  Security,
  Architecture,
  Speed,
  Assignment,
  Shield,
  BugReport,
  Lightbulb,
  Timeline,
  AutoFixHigh
} from '@mui/icons-material'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'

const EnhancedValidationPanel = ({ diagramId, onValidationComplete }) => {
  const theme = useTheme()
  const [validationResults, setValidationResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [expandedSections, setExpandedSections] = useState({})
  const [lastValidated, setLastValidated] = useState(null)

  useEffect(() => {
    if (diagramId) {
      validateDiagram()
    }
  }, [diagramId])

  const validateDiagram = async () => {
    if (!diagramId) return
    
    setLoading(true)
    try {
      const token = localStorage.getItem('token')
      const response = await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/api/scoring/validate`,
        { diagram_id: diagramId },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      
      setValidationResults(response.data.validation_results || [])
      setLastValidated(new Date())
      
      if (onValidationComplete) {
        onValidationComplete(response.data.validation_results)
      }
    } catch (error) {
      console.error('Validation failed:', error)
      setValidationResults([])
    } finally {
      setLoading(false)
    }
  }

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'error':
        return <Error color="error" />
      case 'warning':
        return <Warning color="warning" />
      case 'info':
        return <Info color="info" />
      default:
        return <Info color="info" />
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'error':
        return theme.palette.error.main
      case 'warning':
        return theme.palette.warning.main
      case 'info':
        return theme.palette.info.main
      default:
        return theme.palette.grey[500]
    }
  }

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'security':
        return <Security />
      case 'architecture':
        return <Architecture />
      case 'performance':
        return <Speed />
      case 'completeness':
        return <Assignment />
      default:
        return <BugReport />
    }
  }

  const getCategoryColor = (category) => {
    switch (category) {
      case 'security':
        return theme.palette.error.main
      case 'architecture':
        return theme.palette.primary.main
      case 'performance':
        return theme.palette.success.main
      case 'completeness':
        return theme.palette.info.main
      default:
        return theme.palette.grey[500]
    }
  }

  const groupResultsByCategory = () => {
    const grouped = validationResults.reduce((acc, result) => {
      const category = result.category || 'other'
      if (!acc[category]) {
        acc[category] = []
      }
      acc[category].push(result)
      return acc
    }, {})

    // Sort by severity within each category
    Object.keys(grouped).forEach(category => {
      grouped[category].sort((a, b) => {
        const severityOrder = { error: 0, warning: 1, info: 2 }
        return severityOrder[a.severity] - severityOrder[b.severity]
      })
    })

    return grouped
  }

  const getValidationScore = () => {
    if (validationResults.length === 0) return 100

    const errors = validationResults.filter(r => r.severity === 'error').length
    const warnings = validationResults.filter(r => r.severity === 'warning').length
    const infos = validationResults.filter(r => r.severity === 'info').length

    // Calculate score: errors are -20 points, warnings are -10, infos are -5
    const deduction = (errors * 20) + (warnings * 10) + (infos * 5)
    return Math.max(0, 100 - deduction)
  }

  const toggleSection = (category) => {
    setExpandedSections(prev => ({
      ...prev,
      [category]: !prev[category]
    }))
  }

  const groupedResults = groupResultsByCategory()
  const categories = Object.keys(groupedResults)
  const validationScore = getValidationScore()

  const getScoreColor = (score) => {
    if (score >= 90) return theme.palette.success.main
    if (score >= 70) return theme.palette.warning.main
    return theme.palette.error.main
  }

  const getScoreLabel = (score) => {
    if (score >= 90) return 'Excellent'
    if (score >= 80) return 'Good'
    if (score >= 70) return 'Fair'
    if (score >= 50) return 'Poor'
    return 'Critical'
  }

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Box sx={{ p: 2, borderBottom: `1px solid ${theme.palette.divider}` }}>
        <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
          <Typography variant="h6" fontWeight="600" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Shield color="primary" />
            Threat Model Validation
          </Typography>
          
          <IconButton
            onClick={validateDiagram}
            disabled={loading || !diagramId}
            sx={{
              bgcolor: theme.palette.primary.main,
              color: 'white',
              '&:hover': { bgcolor: theme.palette.primary.dark },
              '&:disabled': { bgcolor: theme.palette.grey[300] }
            }}
          >
            <AutoFixHigh />
          </IconButton>
        </Box>

        {/* Validation Score */}
        <Card sx={{ 
          background: `linear-gradient(135deg, ${alpha(getScoreColor(validationScore), 0.1)} 0%, ${alpha(getScoreColor(validationScore), 0.05)} 100%)`,
          border: `1px solid ${alpha(getScoreColor(validationScore), 0.2)}`
        }}>
          <CardContent sx={{ p: 2 }}>
            <Box display="flex" alignItems="center" justifyContent="between">
              <Box flex={1}>
                <Typography variant="body2" color="textSecondary" mb={0.5}>
                  Validation Score
                </Typography>
                <Typography variant="h4" fontWeight="bold" color={getScoreColor(validationScore)}>
                  {validationScore}%
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  {getScoreLabel(validationScore)} Design
                </Typography>
              </Box>
              
              <Box flex={1}>
                <LinearProgress
                  variant="determinate"
                  value={validationScore}
                  sx={{
                    height: 8,
                    borderRadius: 4,
                    bgcolor: alpha(getScoreColor(validationScore), 0.1),
                    '& .MuiLinearProgress-bar': {
                      borderRadius: 4,
                      bgcolor: getScoreColor(validationScore)
                    }
                  }}
                />
                <Box display="flex" justifyContent="space-between" mt={1}>
                  <Typography variant="caption" color="textSecondary">
                    Issues Found: {validationResults.length}
                  </Typography>
                  {lastValidated && (
                    <Typography variant="caption" color="textSecondary">
                      Last check: {lastValidated.toLocaleTimeString()}
                    </Typography>
                  )}
                </Box>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </Box>

      {/* Loading State */}
      {loading && (
        <Box sx={{ p: 2 }}>
          <LinearProgress />
          <Typography variant="body2" color="textSecondary" textAlign="center" mt={1}>
            Analyzing your threat model...
          </Typography>
        </Box>
      )}

      {/* Validation Results */}
      <Box sx={{ flex: 1, overflow: 'auto' }}>
        {!loading && validationResults.length === 0 && (
          <Box sx={{ p: 3, textAlign: 'center' }}>
            <CheckCircle sx={{ fontSize: 48, color: theme.palette.success.main, mb: 2 }} />
            <Typography variant="h6" fontWeight="600" mb={1}>
              No Issues Found!
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Your threat model looks great. Keep up the excellent work!
            </Typography>
          </Box>
        )}

        {!loading && categories.length > 0 && (
          <List sx={{ p: 0 }}>
            {categories.map((category) => (
              <motion.div
                key={category}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
              >
                {/* Category Header */}
                <ListItem
                  button
                  onClick={() => toggleSection(category)}
                  sx={{
                    bgcolor: alpha(getCategoryColor(category), 0.05),
                    borderLeft: `4px solid ${getCategoryColor(category)}`,
                    mb: 1
                  }}
                >
                  <ListItemIcon>
                    <Badge badgeContent={groupedResults[category].length} color="error">
                      {getCategoryIcon(category)}
                    </Badge>
                  </ListItemIcon>
                  
                  <ListItemText
                    primary={
                      <Typography variant="subtitle1" fontWeight="600" sx={{ textTransform: 'capitalize' }}>
                        {category} Issues
                      </Typography>
                    }
                    secondary={
                      <Box display="flex" gap={1} mt={0.5}>
                        {['error', 'warning', 'info'].map(severity => {
                          const count = groupedResults[category].filter(r => r.severity === severity).length
                          return count > 0 ? (
                            <Chip
                              key={severity}
                              label={`${count} ${severity}${count > 1 ? 's' : ''}`}
                              size="small"
                              color={severity === 'error' ? 'error' : severity === 'warning' ? 'warning' : 'info'}
                              variant="outlined"
                            />
                          ) : null
                        })}
                      </Box>
                    }
                  />
                  
                  <IconButton size="small">
                    {expandedSections[category] ? <ExpandLess /> : <ExpandMore />}
                  </IconButton>
                </ListItem>

                {/* Category Items */}
                <Collapse in={expandedSections[category]} timeout="auto" unmountOnExit>
                  <List sx={{ pl: 2 }}>
                    <AnimatePresence>
                      {groupedResults[category].map((result, index) => (
                        <motion.div
                          key={`${result.rule_id}-${index}`}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: -20 }}
                          transition={{ delay: index * 0.1 }}
                        >
                          <ListItem
                            sx={{
                              alignItems: 'flex-start',
                              py: 1.5,
                              borderRadius: 1,
                              mb: 1,
                              bgcolor: alpha(getSeverityColor(result.severity), 0.05),
                              border: `1px solid ${alpha(getSeverityColor(result.severity), 0.1)}`
                            }}
                          >
                            <ListItemIcon sx={{ mt: 0.5 }}>
                              <Tooltip title={`${result.severity.toUpperCase()}: ${result.rule_name}`}>
                                {getSeverityIcon(result.severity)}
                              </Tooltip>
                            </ListItemIcon>
                            
                            <ListItemText
                              primary={
                                <Box display="flex" alignItems="center" gap={1} mb={0.5}>
                                  <Typography variant="subtitle2" fontWeight="600">
                                    {result.rule_name}
                                  </Typography>
                                  <Chip
                                    label={result.rule_id}
                                    size="small"
                                    variant="outlined"
                                    sx={{ fontSize: '0.7rem', height: 20 }}
                                  />
                                </Box>
                              }
                              secondary={
                                <Box>
                                  <Typography variant="body2" color="textSecondary" mb={1}>
                                    {result.message}
                                  </Typography>
                                  
                                  {result.element_id && (
                                    <Chip
                                      label={`Element: ${result.element_id}`}
                                      size="small"
                                      icon={<Lightbulb />}
                                      sx={{ fontSize: '0.7rem' }}
                                    />
                                  )}
                                </Box>
                              }
                            />
                          </ListItem>
                        </motion.div>
                      ))}
                    </AnimatePresence>
                  </List>
                </Collapse>
              </motion.div>
            ))}
          </List>
        )}
      </Box>

      {/* Quick Actions */}
      {validationResults.length > 0 && (
        <Box sx={{ p: 2, borderTop: `1px solid ${theme.palette.divider}` }}>
          <Alert
            severity="info"
            icon={<Timeline />}
            sx={{ fontSize: '0.875rem' }}
          >
            <Typography variant="body2" mb={1}>
              <strong>Quick Tips:</strong>
            </Typography>
            <Typography variant="body2">
              • Address errors first - they impact security
              <br />
              • Warnings suggest improvements
              <br />
              • Info items are optimization opportunities
            </Typography>
          </Alert>
        </Box>
      )}
    </Box>
  )
}

export default EnhancedValidationPanel