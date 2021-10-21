import React, {useState} from 'react'
import {Drawer} from '@mui/material'
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Sidebar from "./Sidebar";
import {Menu} from "@mui/icons-material";
import './Navbar.css'

export const Navbar = () => {
    const [open, setOpen] = useState(false);

    return (
        <Box sx={{flexGrow: 1}}>
            <AppBar position="static">
                <Toolbar>
                    <IconButton
                        size="large"
                        edge="start"
                        color="inherit"
                        aria-label="menu"
                        sx={{mr: 2}}
                        onClick={() => {
                            setOpen(true)
                        }}
                    >
                        <Menu/>
                    </IconButton>
                    <Typography variant="h6" component="div" sx={{flexGrow: 1}}>
                        Mapsential
                    </Typography>
                    <Button color="inherit">Tipps</Button>
                </Toolbar>
            </AppBar>
            <Drawer
                variant="temporary"
                open={open}
                onClose={() => {
                    setOpen(!open)
                 }
                }
            >
                <Sidebar/>
            </Drawer>
        </Box>
    )
}