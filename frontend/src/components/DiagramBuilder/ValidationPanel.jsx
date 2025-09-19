import React, { useEffect, useState } from 'react'
import {
  Paper,
  Typography,
  Box,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Alert,
  Button,
  CircularProgress
} from '@mui/material'
import {
  ExpandMore,
  Error,
  Warning,
  Info,
  CheckCircle,
  Refresh
} from '@mui/icons-material'
import { useDigramStore } from '../../stores/diagramStore'

const ValidationPanel = () => {
  const { 
    validationResults, 
    isValidating, 
    validateDiagram,
    nodes,
    edges 
  } = useDigramStore()
  
  const [groupedResults, setGroupedResults] = useState({})

  useEffect(() => {
    // Group validation results by category
    const grouped = validationResults.reduce((acc, result) => {
      if (!acc[result.category]) {
        acc[result.category] = []
      }
      acc[result.category].push(result)
      return acc
    }, {})
    setGroupedResults(grouped)
  }, [validationResults])

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'error':
        return <Error color="error" />
      case 'warning':
        return <Warning color="warning" />
      case 'info':
        return <Info color="info" />
      default:
        return <Info />
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'error':
        return 'error'
      case 'warning':
        return 'warning'
      case 'info':
        return 'info'
      default:
        return 'default'
    }
  }

  const getCategoryColor = (category) => {
    const colors = {
      'security': 'error',
      'architecture': 'primary',
      'performance': 'warning',
      'completeness': 'info'
    }
    return colors[category] || 'default'
  }

  const handleValidate = async () => {
    await validateDiagram()
  }

  const getValidationSummary = () => {
    const errorCount = validationResults.filter(r => r.severity === 'error').length
    const warningCount = validationResults.filter(r => r.severity === 'warning').length
    const infoCount = validationResults.filter(r => r.severity === 'info').length
    
    return { errorCount, warningCount, infoCount }
  }

  const { errorCount, warningCount, infoCount } = getValidationSummary()

  return (
    <Paper
      className="validation-panel"
      sx={{
        position: 'absolute',
        top: 20,
        right: 20,
        width: 320,
        maxHeight: 'calc(100vh - 40px)',
        overflowY: 'auto',
        zIndex: 1000,
        backgroundColor: 'background.paper'
      }}
    >
      <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6">
            Validation
          </Typography>
          <Button
            size="small"
            startIcon={isValidating ? <CircularProgress size={16} /> : <Refresh />}
            onClick={handleValidate}
            disabled={isValidating}
          >
            Validate
          </Button>
        </Box>
        
        {/* Summary */}
        <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
          <Chip
            size="small"
            label={`${errorCount} Errors`}
            color={errorCount > 0 ? 'error' : 'default'}
            variant={errorCount > 0 ? 'filled' : 'outlined'}
          />
          <Chip
            size="small"
            label={`${warningCount} Warnings`}
            color={warningCount > 0 ? 'warning' : 'default'}
            variant={warningCount > 0 ? 'filled' : 'outlined'}
          />
          <Chip
            size="small"
            label={`${infoCount} Info`}
            color={infoCount > 0 ? 'info' : 'default'}
            variant={infoCount > 0 ? 'filled' : 'outlined'}
          />
        </Box>

        <Typography variant="body2" color="textSecondary">
          {nodes.length} elements, {edges.length} connections
        </Typography>
      </Box>

      <Box sx={{ p: 1 }}>
        {validationResults.length === 0 ? (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            {nodes.length === 0 ? (
              <Alert severity="info">
                Add elements to your diagram to see validation results
              </Alert>
            ) : (
              <Box>
                <CheckCircle color="success" sx={{ fontSize: 48, mb: 2 }} />
                <Typography variant="body2" color="textSecondary">
                  No issues found. Click validate to check your design.
                </Typography>
              </Box>
            )}
          </Box>
        ) : (
          Object.entries(groupedResults).map(([category, results]) => (
            <Accordion key={category} defaultExpanded>
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Typography variant="subtitle2" sx={{ textTransform: 'capitalize' }}>
                    {category}
                  </Typography>
                  <Chip
                    size="small"
                    label={results.length}
                    color={getCategoryColor(category)}
                    variant="outlined"
                  />
                </Box>
              </AccordionSummary>
              <AccordionDetails sx={{ p: 0 }}>
                <List dense>
                  {results.map((result, index) => (
                    <ListItem key={`${category}-${index}`} alignItems="flex-start">
                      <ListItemIcon sx={{ minWidth: 36 }}>
                        {getSeverityIcon(result.severity)}
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Box>
                            <Typography variant="body2" fontWeight="medium">
                              {result.rule_name}
                            </Typography>
                            <Chip
                              size="small"
                              label={result.severity}
                              color={getSeverityColor(result.severity)}
                              variant="outlined"
                              sx={{ mt: 0.5 }}
                            />
                          </Box>
                        }
                        secondary={
                          <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
                            {result.message}
                            {result.element_id && (
                              <Box component="span" sx={{ display: 'block', mt: 0.5 }}>
                                Element: {result.element_id}
                              </Box>
                            )}
                          </Typography>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              </AccordionDetails>
            </Accordion>
          ))
        )}
      </Box>

      {validationResults.length > 0 && (
        <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
          <Typography variant="caption" color="textSecondary">
            💡 Fix errors and warnings to improve your threat model score
          </Typography>
        </Box>
      )}
    </Paper>
  )
}

export default ValidationPanel