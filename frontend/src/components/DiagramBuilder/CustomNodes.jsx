import React, { memo } from 'react'
import { Handle, Position } from '@reactflow/core'
import { Box, Typography, Paper } from '@mui/material'
import {
  Computer,
  Storage,
  Web,
  Api,
  Security,
  Router
} from '@mui/icons-material'

const BaseNode = ({ data, children, backgroundColor = '#ffffff', borderColor = '#1976d2' }) => {
  return (
    <Paper
      elevation={2}
      sx={{
        padding: 1,
        minWidth: 100,
        textAlign: 'center',
        backgroundColor,
        border: `2px solid ${borderColor}`,
        borderRadius: 1,
        '&:hover': {
          boxShadow: 4,
          transform: 'translateY(-1px)'
        },
        transition: 'all 0.2s ease-in-out'
      }}
    >
      <Handle
        type="target"
        position={Position.Top}
        style={{
          background: borderColor,
          width: 8,
          height: 8
        }}
      />
      
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 0.5 }}>
        {children}
        <Typography variant="caption" fontWeight="medium">
          {data.label}
        </Typography>
        {data.properties && Object.keys(data.properties).length > 0 && (
          <Typography variant="caption" color="textSecondary" fontSize="0.7rem">
            {Object.entries(data.properties).map(([key, value]) => `${key}: ${value}`).join(', ')}
          </Typography>
        )}
      </Box>
      
      <Handle
        type="source"
        position={Position.Bottom}
        style={{
          background: borderColor,
          width: 8,
          height: 8
        }}
      />
    </Paper>
  )
}

const ServerNode = memo(({ data, isConnectable }) => {
  return (
    <BaseNode 
      data={data} 
      backgroundColor="#e3f2fd" 
      borderColor="#1976d2"
    >
      <Computer fontSize="small" color="primary" />
    </BaseNode>
  )
})

const DatabaseNode = memo(({ data, isConnectable }) => {
  return (
    <BaseNode 
      data={data} 
      backgroundColor="#f3e5f5" 
      borderColor="#7b1fa2"
    >
      <Storage fontSize="small" sx={{ color: '#7b1fa2' }} />
    </BaseNode>
  )
})

const FrontendNode = memo(({ data, isConnectable }) => {
  return (
    <BaseNode 
      data={data} 
      backgroundColor="#e8f5e8" 
      borderColor="#388e3c"
    >
      <Web fontSize="small" sx={{ color: '#388e3c' }} />
    </BaseNode>
  )
})

const ApiNode = memo(({ data, isConnectable }) => {
  return (
    <BaseNode 
      data={data} 
      backgroundColor="#fff3e0" 
      borderColor="#f57c00"
    >
      <Api fontSize="small" sx={{ color: '#f57c00' }} />
    </BaseNode>
  )
})

const SecurityNode = memo(({ data, isConnectable }) => {
  return (
    <BaseNode 
      data={data} 
      backgroundColor="#ffebee" 
      borderColor="#d32f2f"
    >
      <Security fontSize="small" sx={{ color: '#d32f2f' }} />
    </BaseNode>
  )
})

const NetworkNode = memo(({ data, isConnectable }) => {
  return (
    <BaseNode 
      data={data} 
      backgroundColor="#f9fbe7" 
      borderColor="#827717"
    >
      <Router fontSize="small" sx={{ color: '#827717' }} />
    </BaseNode>
  )
})

const CustomNodes = {
  ServerNode,
  DatabaseNode,
  FrontendNode,
  ApiNode,
  SecurityNode,
  NetworkNode
}

export default CustomNodes