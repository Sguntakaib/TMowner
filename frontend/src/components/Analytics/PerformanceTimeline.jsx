import React from 'react'
import { Box, Typography, Paper } from '@mui/material'

const PerformanceTimeline = () => {
  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Performance Timeline
      </Typography>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 200 }}>
        <Typography variant="body2" color="textSecondary">
          Performance timeline chart will be implemented here
        </Typography>
      </Box>
    </Paper>
  )
}

export default PerformanceTimeline