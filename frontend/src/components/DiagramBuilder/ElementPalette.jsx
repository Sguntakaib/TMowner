import React from 'react'
import {
  Paper,
  Typography,
  Box,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  Card,
  CardContent
} from '@mui/material'
import {
  ExpandMore,
  Computer,
  Storage,
  Web,
  Api,
  Security,
  Router,
  CloudQueue,
  PhoneAndroid
} from '@mui/icons-material'
import { useDrag } from 'react-dnd'

const DraggableElement = ({ type, label, icon: Icon, description }) => {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: 'node',
    item: { type },
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
  }))

  const onDragStart = (event, nodeType) => {
    event.dataTransfer.setData('application/reactflow', nodeType)
    event.dataTransfer.effectAllowed = 'move'
  }

  return (
    <Card
      ref={drag}
      className={`draggable-node ${isDragging ? 'dragging' : ''}`}
      draggable
      onDragStart={(event) => onDragStart(event, type)}
      sx={{
        cursor: 'grab',
        mb: 1,
        '&:hover': {
          backgroundColor: 'action.hover',
          transform: 'translateY(-1px)',
          boxShadow: 2
        },
        '&:active': {
          cursor: 'grabbing'
        },
        opacity: isDragging ? 0.5 : 1
      }}
    >
      <CardContent sx={{ p: 1.5, '&:last-child': { pb: 1.5 } }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 0.5 }}>
          <Icon fontSize="small" sx={{ mr: 1 }} />
          <Typography variant="body2" fontWeight="medium">
            {label}
          </Typography>
        </Box>
        <Typography variant="caption" color="textSecondary">
          {description}
        </Typography>
      </CardContent>
    </Card>
  )
}

const ElementPalette = () => {
  const elementCategories = [
    {
      name: 'Compute',
      icon: Computer,
      elements: [
        {
          type: 'server',
          label: 'Web Server',
          icon: Computer,
          description: 'Application server hosting web services'
        },
        {
          type: 'api',
          label: 'API Gateway',
          icon: Api,
          description: 'API management and routing service'
        },
        {
          type: 'frontend',
          label: 'Client App',
          icon: Web,
          description: 'Frontend application (web/mobile)'
        }
      ]
    },
    {
      name: 'Storage',
      icon: Storage,
      elements: [
        {
          type: 'database',
          label: 'Database',
          icon: Storage,
          description: 'Primary data storage system'
        },
        {
          type: 'storage',
          label: 'File Storage',
          icon: CloudQueue,
          description: 'Object or file storage service'
        }
      ]
    },
    {
      name: 'Security',
      icon: Security,
      elements: [
        {
          type: 'security',
          label: 'Firewall',
          icon: Security,
          description: 'Network security barrier'
        },
        {
          type: 'auth',
          label: 'Auth Service',
          icon: Security,
          description: 'Authentication and authorization'
        },
        {
          type: 'encryption',
          label: 'Encryption',
          icon: Security,
          description: 'Data encryption service'
        }
      ]
    },
    {
      name: 'Network',
      icon: Router,
      elements: [
        {
          type: 'network',
          label: 'Load Balancer',
          icon: Router,
          description: 'Distributes incoming requests'
        },
        {
          type: 'cdn',
          label: 'CDN',
          icon: Router,
          description: 'Content delivery network'
        },
        {
          type: 'vpn',
          label: 'VPN Gateway',
          icon: Router,
          description: 'Virtual private network access'
        }
      ]
    },
    {
      name: 'External',
      icon: CloudQueue,
      elements: [
        {
          type: 'external',
          label: 'External API',
          icon: CloudQueue,
          description: 'Third-party service integration'
        },
        {
          type: 'user',
          label: 'User/Actor',
          icon: PhoneAndroid,
          description: 'Human user or external system'
        }
      ]
    }
  ]

  return (
    <Paper
      className="element-palette"
      sx={{
        position: 'absolute',
        top: 20,
        left: 20,
        width: 280,
        maxHeight: 'calc(100vh - 40px)',
        overflowY: 'auto',
        zIndex: 1000,
        backgroundColor: 'background.paper'
      }}
    >
      <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
        <Typography variant="h6" gutterBottom>
          System Elements
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Drag elements onto the canvas to build your system architecture
        </Typography>
      </Box>

      <Box sx={{ p: 1 }}>
        {elementCategories.map((category) => (
          <Accordion key={category.name} defaultExpanded>
            <AccordionSummary expandIcon={<ExpandMore />}>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <category.icon fontSize="small" sx={{ mr: 1 }} />
                <Typography variant="subtitle2">
                  {category.name}
                </Typography>
              </Box>
            </AccordionSummary>
            <AccordionDetails sx={{ p: 1 }}>
              {category.elements.map((element) => (
                <DraggableElement
                  key={element.type}
                  type={element.type}
                  label={element.label}
                  icon={element.icon}
                  description={element.description}
                />
              ))}
            </AccordionDetails>
          </Accordion>
        ))}
      </Box>

      <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
        <Typography variant="caption" color="textSecondary">
          💡 Tip: After placing elements, connect them by dragging from the handles that appear on hover
        </Typography>
      </Box>
    </Paper>
  )
}

export default ElementPalette