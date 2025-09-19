import React, { useState } from 'react'
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Avatar,
  Menu,
  MenuItem,
  IconButton,
  Badge,
  Tooltip
} from '@mui/material'
import {
  AccountCircle,
  Dashboard,
  Psychology,
  Score,
  School,
  Notifications,
  Logout
} from '@mui/icons-material'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../../stores/authStore'

const Navbar = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout } = useAuthStore()
  const [anchorEl, setAnchorEl] = useState(null)

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget)
  }

  const handleMenuClose = () => {
    setAnchorEl(null)
  }

  const handleLogout = () => {
    logout()
    handleMenuClose()
  }

  const navigation = [
    { name: 'Dashboard', path: '/', icon: Dashboard },
    { name: 'Scenarios', path: '/scenarios', icon: Psychology },
    { name: 'Analytics', path: '/analytics', icon: Score },
    { name: 'Achievements', path: '/achievements', icon: School },
    { name: 'Learning', path: '/learning', icon: School },
  ]

  return (
    <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Threat Modeling Platform
        </Typography>

        <Box sx={{ display: { xs: 'none', md: 'flex' }, mr: 2 }}>
          {navigation.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.path
            return (
              <Button
                key={item.name}
                color="inherit"
                startIcon={<Icon />}
                onClick={() => navigate(item.path)}
                sx={{
                  mx: 1,
                  backgroundColor: isActive ? 'rgba(255,255,255,0.1)' : 'transparent',
                  '&:hover': {
                    backgroundColor: 'rgba(255,255,255,0.2)'
                  }
                }}
              >
                {item.name}
              </Button>
            )
          })}
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Tooltip title="Notifications">
            <IconButton color="inherit">
              <Badge badgeContent={0} color="error">
                <Notifications />
              </Badge>
            </IconButton>
          </Tooltip>

          <Tooltip title="Account">
            <IconButton
              color="inherit"
              onClick={handleMenuOpen}
              sx={{ p: 0.5 }}
            >
              <Avatar
                sx={{ width: 32, height: 32 }}
                src={user?.profile?.avatar_url}
              >
                {user?.profile?.first_name?.[0] || user?.email[0].toUpperCase()}
              </Avatar>
            </IconButton>
          </Tooltip>

          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
            anchorOrigin={{
              vertical: 'bottom',
              horizontal: 'right',
            }}
            transformOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
          >
            <MenuItem onClick={() => { navigate('/profile'); handleMenuClose() }}>
              <AccountCircle sx={{ mr: 1 }} />
              Profile
            </MenuItem>
            <MenuItem onClick={handleLogout}>
              <Logout sx={{ mr: 1 }} />
              Logout
            </MenuItem>
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  )
}

export default Navbar