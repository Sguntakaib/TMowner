import React, { useState, useEffect } from 'react'
import {
  Container,
  Grid,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Chip,
  TextField,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  InputAdornment,
  Pagination
} from '@mui/material'
import {
  Search,
  PlayArrow,
  FilterList,
  AccessTime,
  Star
} from '@mui/icons-material'
import { useNavigate } from 'react-router-dom'
import { useScenarioStore } from '../../stores/scenarioStore'
import LoadingSpinner from '../Common/LoadingSpinner'

const ScenarioList = () => {
  const navigate = useNavigate()
  const {
    scenarios,
    isLoading,
    filters,
    categories,
    difficulties,
    fetchScenarios,
    setFilters,
    searchScenarios,
    filterByCategory,
    filterByDifficulty,
    clearFilters
  } = useScenarioStore()

  const [page, setPage] = useState(1)
  const [searchTerm, setSearchTerm] = useState('')
  const scenariosPerPage = 12

  useEffect(() => {
    fetchScenarios(0, scenariosPerPage)
  }, [])

  const handleSearch = (event) => {
    const value = event.target.value
    setSearchTerm(value)
    searchScenarios(value)
    setPage(1)
  }

  const handleCategoryFilter = (event) => {
    const category = event.target.value === 'all' ? null : event.target.value
    filterByCategory(category)
    setPage(1)
  }

  const handleDifficultyFilter = (event) => {
    const difficulty = event.target.value === 'all' ? null : event.target.value
    filterByDifficulty(difficulty)
    setPage(1)
  }

  const handleClearFilters = () => {
    setSearchTerm('')
    clearFilters()
    setPage(1)
  }

  const handlePageChange = (event, newPage) => {
    setPage(newPage)
    fetchScenarios((newPage - 1) * scenariosPerPage, scenariosPerPage)
  }

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'beginner': return 'success'
      case 'intermediate': return 'warning'
      case 'expert': return 'error'
      default: return 'default'
    }
  }

  const getCategoryColor = (category) => {
    const colors = {
      'web': 'primary',
      'api': 'secondary',
      'database': 'info',
      'cloud': 'warning',
      'mobile': 'success',
      'network': 'error',
      'iot': 'default'
    }
    return colors[category] || 'default'
  }

  if (isLoading && scenarios.length === 0) {
    return <LoadingSpinner message="Loading scenarios..." />
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Threat Modeling Scenarios
      </Typography>

      <Typography variant="body1" color="textSecondary" paragraph>
        Choose from a variety of scenarios to practice your threat modeling skills
      </Typography>

      {/* Filters */}
      <Box sx={{ mb: 4 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              placeholder="Search scenarios..."
              value={searchTerm}
              onChange={handleSearch}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Search />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          
          <Grid item xs={12} md={3}>
            <FormControl fullWidth>
              <InputLabel>Category</InputLabel>
              <Select
                value={filters.category || 'all'}
                label="Category"
                onChange={handleCategoryFilter}
              >
                <MenuItem value="all">All Categories</MenuItem>
                {categories.map((category) => (
                  <MenuItem key={category} value={category}>
                    {category.charAt(0).toUpperCase() + category.slice(1)}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} md={3}>
            <FormControl fullWidth>
              <InputLabel>Difficulty</InputLabel>
              <Select
                value={filters.difficulty || 'all'}
                label="Difficulty"
                onChange={handleDifficultyFilter}
              >
                <MenuItem value="all">All Difficulties</MenuItem>
                {difficulties.map((difficulty) => (
                  <MenuItem key={difficulty} value={difficulty}>
                    {difficulty.charAt(0).toUpperCase() + difficulty.slice(1)}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} md={2}>
            <Button
              fullWidth
              variant="outlined"
              startIcon={<FilterList />}
              onClick={handleClearFilters}
            >
              Clear
            </Button>
          </Grid>
        </Grid>
      </Box>

      {/* Scenarios Grid */}
      {scenarios.length === 0 ? (
        <Box textAlign="center" py={8}>
          <Typography variant="h6" color="textSecondary">
            No scenarios found
          </Typography>
          <Typography variant="body2" color="textSecondary">
            Try adjusting your filters or search terms
          </Typography>
        </Box>
      ) : (
        <>
          <Grid container spacing={3}>
            {scenarios.map((scenario) => (
              <Grid item xs={12} sm={6} md={4} key={scenario.id}>
                <Card 
                  sx={{ 
                    height: '100%', 
                    display: 'flex', 
                    flexDirection: 'column',
                    transition: 'transform 0.2s, elevation 0.2s',
                    '&:hover': {
                      transform: 'translateY(-2px)',
                      elevation: 8
                    }
                  }}
                >
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Box sx={{ mb: 2 }}>
                      <Chip 
                        label={scenario.category} 
                        size="small" 
                        color={getCategoryColor(scenario.category)}
                        sx={{ mr: 1 }} 
                      />
                      <Chip 
                        label={scenario.difficulty} 
                        size="small" 
                        color={getDifficultyColor(scenario.difficulty)}
                      />
                    </Box>

                    <Typography variant="h6" gutterBottom>
                      {scenario.title}
                    </Typography>
                    
                    <Typography 
                      variant="body2" 
                      color="textSecondary" 
                      sx={{ mb: 2, minHeight: 60 }}
                    >
                      {scenario.description.length > 120 
                        ? `${scenario.description.substring(0, 120)}...`
                        : scenario.description
                      }
                    </Typography>

                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <Star fontSize="small" color="primary" sx={{ mr: 0.5 }} />
                      <Typography variant="body2" color="textSecondary">
                        Max Points: {scenario.max_points}
                      </Typography>
                    </Box>

                    {scenario.time_limit && (
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <AccessTime fontSize="small" color="action" sx={{ mr: 0.5 }} />
                        <Typography variant="body2" color="textSecondary">
                          Time Limit: {scenario.time_limit} min
                        </Typography>
                      </Box>
                    )}

                    {scenario.tags && scenario.tags.length > 0 && (
                      <Box sx={{ mt: 2 }}>
                        {scenario.tags.slice(0, 3).map((tag) => (
                          <Chip 
                            key={tag} 
                            label={tag} 
                            size="small" 
                            variant="outlined"
                            sx={{ mr: 0.5, mb: 0.5 }}
                          />
                        ))}
                        {scenario.tags.length > 3 && (
                          <Typography variant="caption" color="textSecondary">
                            +{scenario.tags.length - 3} more
                          </Typography>
                        )}
                      </Box>
                    )}
                  </CardContent>
                  
                  <CardActions sx={{ p: 2, pt: 0 }}>
                    <Button 
                      fullWidth
                      variant="contained"
                      startIcon={<PlayArrow />}
                      onClick={() => navigate(`/scenarios/${scenario.id}`)}
                    >
                      View Details
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>

          {/* Pagination */}
          {scenarios.length >= scenariosPerPage && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <Pagination
                count={Math.ceil(scenarios.length / scenariosPerPage)}
                page={page}
                onChange={handlePageChange}
                color="primary"
                size="large"
              />
            </Box>
          )}
        </>
      )}
    </Container>
  )
}

export default ScenarioList