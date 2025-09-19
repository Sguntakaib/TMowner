import React, { useState, useEffect } from 'react'
import { Box, Typography, useTheme, CircularProgress } from '@mui/material'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import axios from 'axios'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const PerformanceTimeline = () => {
  const theme = useTheme()
  const [timelineData, setTimelineData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTimelineData()
  }, [])

  const fetchTimelineData = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/api/analytics/performance-timeline?limit=20`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setTimelineData(response.data.timeline)
      setLoading(false)
    } catch (error) {
      console.error('Failed to fetch timeline data:', error)
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100%">
        <CircularProgress />
      </Box>
    )
  }

  if (!timelineData || timelineData.length === 0) {
    return (
      <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" height="100%">
        <Typography variant="body1" color="textSecondary">
          No performance data available yet
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Complete more scenarios to see your progress!
        </Typography>
      </Box>
    )
  }

  const chartData = {
    labels: timelineData.map((_, index) => `Attempt ${index + 1}`),
    datasets: [
      {
        label: 'Total Score',
        data: timelineData.map(item => item.total_score),
        borderColor: theme.palette.primary.main,
        backgroundColor: theme.palette.primary.main + '20',
        fill: true,
        tension: 0.4,
        pointRadius: 6,
        pointHoverRadius: 8,
        pointBackgroundColor: theme.palette.primary.main,
        pointBorderColor: '#fff',
        pointBorderWidth: 2
      },
      {
        label: 'Security',
        data: timelineData.map(item => item.security_score),
        borderColor: theme.palette.error.main,
        backgroundColor: 'transparent',
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6,
        borderWidth: 2
      },
      {
        label: 'Architecture',
        data: timelineData.map(item => item.architecture_score),
        borderColor: theme.palette.info.main,
        backgroundColor: 'transparent',
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6,
        borderWidth: 2
      },
      {
        label: 'Performance',
        data: timelineData.map(item => item.performance_score),
        borderColor: theme.palette.success.main,
        backgroundColor: 'transparent',
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6,
        borderWidth: 2
      }
    ]
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          usePointStyle: true,
          padding: 20,
          font: {
            size: 12
          }
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        backgroundColor: theme.palette.background.paper,
        titleColor: theme.palette.text.primary,
        bodyColor: theme.palette.text.secondary,
        borderColor: theme.palette.divider,
        borderWidth: 1,
        cornerRadius: 8,
        displayColors: true,
        callbacks: {
          title: (context) => {
            const index = context[0].dataIndex
            const date = new Date(timelineData[index].date)
            return `Attempt ${index + 1} - ${date.toLocaleDateString()}`
          },
          afterBody: (context) => {
            const index = context[0].dataIndex
            const timeSpent = timelineData[index].time_spent_minutes
            return [`Time spent: ${timeSpent} minutes`]
          }
        }
      }
    },
    scales: {
      x: {
        grid: {
          display: false
        },
        ticks: {
          maxTicksLimit: 8,
          color: theme.palette.text.secondary,
          font: {
            size: 11
          }
        }
      },
      y: {
        min: 0,
        max: 100,
        grid: {
          color: theme.palette.divider + '40'
        },
        ticks: {
          color: theme.palette.text.secondary,
          font: {
            size: 11
          },
          callback: (value) => `${value}%`
        }
      }
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false
    },
    elements: {
      point: {
        hoverBorderWidth: 3
      }
    }
  }

  return (
    <Box sx={{ height: '100%', position: 'relative' }}>
      <Line data={chartData} options={options} />
    </Box>
  )
}

export default PerformanceTimeline