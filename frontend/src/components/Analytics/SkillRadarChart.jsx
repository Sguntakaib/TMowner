import React, { useState, useEffect } from 'react'
import { Box, useTheme, Typography, Tooltip } from '@mui/material'
import { motion } from 'framer-motion'

const SkillRadarChart = ({ data = {} }) => {
  const theme = useTheme()
  const [animatedData, setAnimatedData] = useState({})
  
  const skills = ['Security', 'Architecture', 'Performance', 'Completeness', 'Overall']
  const maxValue = 100
  
  useEffect(() => {
    // Animate the values
    const timer = setTimeout(() => {
      setAnimatedData(data)
    }, 500)
    return () => clearTimeout(timer)
  }, [data])

  const getColor = (skill, value) => {
    if (value >= 85) return theme.palette.success.main
    if (value >= 70) return theme.palette.warning.main
    if (value >= 50) return theme.palette.info.main
    return theme.palette.error.main
  }

  const getSkillIcon = (skill) => {
    const icons = {
      Security: '🔒',
      Architecture: '🏗️',
      Performance: '⚡',
      Completeness: '✅',
      Overall: '🎯'
    }
    return icons[skill] || '📊'
  }

  // Convert to polar coordinates
  const getPolygonPoints = (values) => {
    const points = values.map((value, index) => {
      const angle = (index * 2 * Math.PI) / values.length - Math.PI / 2
      const radius = (value / maxValue) * 120 // 120 is the radius of our chart
      const x = 150 + radius * Math.cos(angle) // 150 is center x
      const y = 150 + radius * Math.sin(angle) // 150 is center y
      return `${x},${y}`
    }).join(' ')
    return points
  }

  const getGridPolygonPoints = (gridValue) => {
    const values = new Array(skills.length).fill(gridValue)
    return getPolygonPoints(values)
  }

  const values = skills.map(skill => animatedData[skill.toLowerCase()] || 0)

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      {/* SVG Radar Chart */}
      <motion.div
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.8, delay: 0.2 }}
      >
        <svg width="300" height="300" viewBox="0 0 300 300">
          <defs>
            <radialGradient id="radarGradient" cx="50%" cy="50%">
              <stop offset="0%" stopColor={theme.palette.primary.main} stopOpacity="0.3" />
              <stop offset="100%" stopColor={theme.palette.primary.main} stopOpacity="0.1" />
            </radialGradient>
          </defs>
          
          {/* Grid lines */}
          {[20, 40, 60, 80, 100].map((gridValue) => (
            <polygon
              key={gridValue}
              points={getGridPolygonPoints(gridValue)}
              fill="none"
              stroke={theme.palette.divider}
              strokeWidth="1"
              opacity={0.3}
            />
          ))}
          
          {/* Axis lines */}
          {skills.map((_, index) => {
            const angle = (index * 2 * Math.PI) / skills.length - Math.PI / 2
            const x2 = 150 + 120 * Math.cos(angle)
            const y2 = 150 + 120 * Math.sin(angle)
            return (
              <line
                key={index}
                x1="150"
                y1="150"
                x2={x2}
                y2={y2}
                stroke={theme.palette.divider}
                strokeWidth="1"
                opacity={0.3}
              />
            )
          })}
          
          {/* Data polygon */}
          <motion.polygon
            points={getPolygonPoints(values)}
            fill="url(#radarGradient)"
            stroke={theme.palette.primary.main}
            strokeWidth="2"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ duration: 1, delay: 0.5 }}
          />
          
          {/* Data points */}
          {values.map((value, index) => {
            const angle = (index * 2 * Math.PI) / values.length - Math.PI / 2
            const radius = (value / maxValue) * 120
            const x = 150 + radius * Math.cos(angle)
            const y = 150 + radius * Math.sin(angle)
            
            return (
              <motion.circle
                key={index}
                cx={x}
                cy={y}
                r="4"
                fill={getColor(skills[index], value)}
                stroke="white"
                strokeWidth="2"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ duration: 0.5, delay: 0.7 + index * 0.1 }}
              />
            )
          })}
          
          {/* Skill labels */}
          {skills.map((skill, index) => {
            const angle = (index * 2 * Math.PI) / skills.length - Math.PI / 2
            const labelRadius = 140
            const x = 150 + labelRadius * Math.cos(angle)
            const y = 150 + labelRadius * Math.sin(angle)
            
            return (
              <text
                key={skill}
                x={x}
                y={y}
                textAnchor="middle"
                dominantBaseline="central"
                fontSize="12"
                fill={theme.palette.text.primary}
                fontWeight="600"
              >
                {skill}
              </text>
            )
          })}
        </svg>
      </motion.div>
      
      {/* Skill breakdown */}
      <Box sx={{ mt: 2, width: '100%' }}>
        <Box display="flex" flexWrap="wrap" gap={1} justifyContent="center">
          {skills.map((skill, index) => (
            <motion.div
              key={skill}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1 + index * 0.1 }}
            >
              <Tooltip title={`${skill}: ${(animatedData[skill.toLowerCase()] || 0).toFixed(1)}%`}>
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 0.5,
                    px: 1.5,
                    py: 0.5,
                    borderRadius: 2,
                    bgcolor: alpha => alpha(getColor(skill, animatedData[skill.toLowerCase()] || 0), 0.1),
                    color: getColor(skill, animatedData[skill.toLowerCase()] || 0),
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                    '&:hover': {
                      transform: 'scale(1.05)',
                      bgcolor: alpha => alpha(getColor(skill, animatedData[skill.toLowerCase()] || 0), 0.2)
                    }
                  }}
                >
                  <span>{getSkillIcon(skill)}</span>
                  <span>{(animatedData[skill.toLowerCase()] || 0).toFixed(0)}%</span>
                </Box>
              </Tooltip>
            </motion.div>
          ))}
        </Box>
      </Box>
    </Box>
  )
}

export default SkillRadarChart