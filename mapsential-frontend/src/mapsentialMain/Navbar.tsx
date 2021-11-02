import React, {useState} from 'react'
import {Drawer} from '@mui/material'
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Sidebar from "./Sidebar";
import {Menu, Public} from "@mui/icons-material";
import './Navbar.css'

export const Navbar = () => {
    const [open, setOpen] = useState(false);

    return (
        <Box>
            <AppBar position="static">
                <Toolbar>
                    <IconButton color="inherit" aria-label="menu" sx={{mr: 2}} onClick={() => {setOpen(true)}}>
                        <Menu/>
                    </IconButton>
                    <Public/>
                    <Typography variant="h6" sx={{flexGrow: 1}}>
                       Mapsential
                    </Typography>
                    <Button color="inherit" disabled>Tipps</Button>
                </Toolbar>
            </AppBar>
            <Drawer variant="temporary" open={open} onClose={() => {setOpen(false)}}>
                <Sidebar/>
            </Drawer>
        </Box>
    )
}