import React, { useState, useEffect } from 'react'
import {
  Container,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Box,
  Grid,
  Card,
  CardContent,
  LinearProgress,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  Divider
} from '@mui/material'
import {
  TrendingUp,
  Star,
  AccessTime,
  Visibility,
  EmojiEvents
} from '@mui/icons-material'
import { useAuthStore } from '../../stores/authStore'
import LoadingSpinner from '../Common/LoadingSpinner'

const ScoreHistory = () => {
  const { api } = useAuthStore()
  const [scores, setScores] = useState([])
  const [userStats, setUserStats] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [selectedScore, setSelectedScore] = useState(null)
  const [feedbackDialog, setFeedbackDialog] = useState(false)

  useEffect(() => {
    const loadScoreData = async () => {
      try {
        setIsLoading(true)
        
        // Fetch score history
        const scoresResponse = await api.get('/scoring/history?limit=50')
        setScores(scoresResponse.data)
        
        // Fetch user stats
        const statsResponse = await api.get('/scoring/stats')
        setUserStats(statsResponse.data)
      } catch (error) {
        console.error('Failed to load score data:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadScoreData()
  }, [])

  const handleViewFeedback = async (scoreId) => {
    try {
      const response = await api.get(`/scoring/feedback/${scoreId}`)
      setSelectedScore(response.data)
      setFeedbackDialog(true)
    } catch (error) {
      console.error('Failed to load feedback:', error)
    }
  }

  const getScoreColor = (score) => {
    if (score >= 90) return 'success'
    if (score >= 70) return 'warning'
    if (score >= 50) return 'info'
    return 'error'
  }

  const getScoreLabel = (score) => {
    if (score >= 90) return 'Excellent'
    if (score >= 70) return 'Good'
    if (score >= 50) return 'Fair'
    return 'Needs Improvement'
  }

  if (isLoading) {
    return <LoadingSpinner message="Loading scores..." />
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Score History
      </Typography>

      {/* User Stats Overview */}
      {userStats && (
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Star color="primary" sx={{ mr: 2 }} />
                  <Box>
                    <Typography variant="h6">
                      {userStats.average_score.toFixed(1)}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Average Score
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <TrendingUp color="success" sx={{ mr: 2 }} />
                  <Box>
                    <Typography variant="h6">
                      {userStats.best_score.toFixed(1)}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Best Score
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <EmojiEvents color="warning" sx={{ mr: 2 }} />
                  <Box>
                    <Typography variant="h6">
                      {userStats.completed_scenarios}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Completed
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <AccessTime color="info" sx={{ mr: 2 }} />
                  <Box>
                    <Typography variant="h6">
                      {Math.round(userStats.total_time_spent / 3600)}h
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Total Time
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Scores Table */}
      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Date</TableCell>
                <TableCell>Scenario</TableCell>
                <TableCell>Total Score</TableCell>
                <TableCell>Security</TableCell>
                <TableCell>Architecture</TableCell>
                <TableCell>Performance</TableCell>
                <TableCell>Completeness</TableCell>
                <TableCell>Time</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {scores.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={9} align="center">
                    <Typography variant="body1" color="textSecondary" sx={{ py: 4 }}>
                      No scores yet. Complete a scenario to see your results here!
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : (
                scores.map((score) => (
                  <TableRow key={score.id}>
                    <TableCell>
                      {new Date(score.submission_time).toLocaleDateString()}
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">
                        Scenario #{score.scenario_id.slice(-6)}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={`${score.scores.total_score.toFixed(1)}`}
                        color={getScoreColor(score.scores.total_score)}
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', minWidth: 60 }}>
                        <LinearProgress
                          variant="determinate"
                          value={score.scores.security_score}
                          sx={{ flexGrow: 1, mr: 1 }}
                        />
                        <Typography variant="caption">
                          {score.scores.security_score.toFixed(0)}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', minWidth: 60 }}>
                        <LinearProgress
                          variant="determinate"
                          value={score.scores.architecture_score}
                          sx={{ flexGrow: 1, mr: 1 }}
                        />
                        <Typography variant="caption">
                          {score.scores.architecture_score.toFixed(0)}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', minWidth: 60 }}>
                        <LinearProgress
                          variant="determinate"
                          value={score.scores.performance_score}
                          sx={{ flexGrow: 1, mr: 1 }}
                        />
                        <Typography variant="caption">
                          {score.scores.performance_score.toFixed(0)}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', minWidth: 60 }}>
                        <LinearProgress
                          variant="determinate"
                          value={score.scores.completeness_score}
                          sx={{ flexGrow: 1, mr: 1 }}
                        />
                        <Typography variant="caption">
                          {score.scores.completeness_score.toFixed(0)}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      {Math.round(score.time_spent / 60)}m
                    </TableCell>
                    <TableCell>
                      <Button
                        size="small"
                        startIcon={<Visibility />}
                        onClick={() => handleViewFeedback(score.id)}
                      >
                        Feedback
                      </Button>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Feedback Dialog */}
      <Dialog
        open={feedbackDialog}
        onClose={() => setFeedbackDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Detailed Feedback
        </DialogTitle>
        <DialogContent>
          {selectedScore && (
            <Box>
              {/* Score Summary */}
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Score Summary
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="textSecondary">
                        Overall Score
                      </Typography>
                      <Typography variant="h4" color="primary">
                        {selectedScore.score.scores.total_score.toFixed(1)}
                      </Typography>
                      <Chip
                        label={getScoreLabel(selectedScore.score.scores.total_score)}
                        color={getScoreColor(selectedScore.score.scores.total_score)}
                        size="small"
                      />
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="textSecondary">
                        Time Spent
                      </Typography>
                      <Typography variant="h6">
                        {Math.round(selectedScore.score.time_spent / 60)} minutes
                      </Typography>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>

              {/* Detailed Feedback */}
              {selectedScore.score.feedback && (
                <Box>
                  <Typography variant="h6" gutterBottom>
                    Summary
                  </Typography>
                  <Typography variant="body1" paragraph>
                    {selectedScore.score.feedback.summary}
                  </Typography>

                  {selectedScore.score.feedback.strengths.length > 0 && (
                    <Box sx={{ mb: 3 }}>
                      <Typography variant="h6" gutterBottom color="success.main">
                        Strengths
                      </Typography>
                      <List>
                        {selectedScore.score.feedback.strengths.map((strength, index) => (
                          <ListItem key={index}>
                            <ListItemText primary={strength} />
                          </ListItem>
                        ))}
                      </List>
                    </Box>
                  )}

                  {selectedScore.score.feedback.weaknesses.length > 0 && (
                    <Box sx={{ mb: 3 }}>
                      <Typography variant="h6" gutterBottom color="warning.main">
                        Areas for Improvement
                      </Typography>
                      <List>
                        {selectedScore.score.feedback.weaknesses.map((weakness, index) => (
                          <ListItem key={index}>
                            <ListItemText primary={weakness} />
                          </ListItem>
                        ))}
                      </List>
                    </Box>
                  )}

                  {selectedScore.score.feedback.recommendations.length > 0 && (
                    <Box>
                      <Typography variant="h6" gutterBottom color="info.main">
                        Recommendations
                      </Typography>
                      <List>
                        {selectedScore.score.feedback.recommendations.map((rec, index) => (
                          <ListItem key={index}>
                            <ListItemText primary={rec} />
                          </ListItem>
                        ))}
                      </List>
                    </Box>
                  )}
                </Box>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setFeedbackDialog(false)}>
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  )
}

export default ScoreHistory