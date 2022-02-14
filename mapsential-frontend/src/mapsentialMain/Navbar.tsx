import React, {useEffect, useState} from 'react'
import {Drawer} from '@mui/material'
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Sidebar from "./Sidebar";
import {Menu, Public, ArrowForwardIos, ArrowBackIosNew, CloseRounded} from "@mui/icons-material";
import './Navbar.css'
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css'

export const Navbar = () => {
    const [open, setOpen] = useState(false);
    const [popupOpen, setPopupOpen] = useState(false);
    const closePopup = () => setPopupOpen(false);
    const openPopup = () => setPopupOpen(true);
    //let tips: string[] = [];
    const getTips = () => 
        fetch("tips/tips.json")
        .then(response => {
            console.log("Zeile 23 +\n", JSON.stringify(response));
            return response.json();
        }).then(json => {
            console.log("Zeile 26 +\n", json);
            setTips(json.tips);
            console.log("Zeile 28 +\n", tips);
        });
    useEffect(() => {
        getTips();
    }, []);
    const [tips, setTips] = useState([]);
    const [currentTipIndex, setCurrentTipIndex] = useState(0);
    const nextTip = () => {
        
        if(currentTipIndex + 1 >= tips.length) {
            setCurrentTipIndex(0);
        } else {
            setCurrentTipIndex(currentTipIndex + 1);
        }

    }

    const previousTip = () => {
        
        if(currentTipIndex - 1 < 0) {
            setCurrentTipIndex(tips.length - 1);
        } else {
            setCurrentTipIndex(currentTipIndex - 1);
        }

    }

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
                    <Button color="inherit" onClick={openPopup}>Tipps</Button>
                    <Popup open={popupOpen} closeOnDocumentClick onClose={closePopup}>
                        <div className="tip-container">
                            <div className="tip-header">
                                <IconButton color="inherit" aria-label="close" sx={{mt: 0.5, mr: 0.5}} onClick={closePopup}>
                                    <CloseRounded/>
                                </IconButton>
                            </div>
                            <div className="tip-content-container">
                                <h1 className="tip-content">{tips[currentTipIndex]}</h1>
                            </div>
                            <div className="tip-navigation">
                                <IconButton color="inherit" aria-label="back" sx={{ml: 0}} onClick={previousTip}>
                                    <ArrowBackIosNew/>
                                </IconButton>
                                <IconButton color="inherit" aria-label="forward" sx={{mr: 0}} onClick={nextTip}>
                                    <ArrowForwardIos/>
                                </IconButton>
                            </div>    
                        </div>
                    </Popup>                   
                </Toolbar>
            </AppBar>
            <Drawer variant="temporary" open={open} onClose={() => {setOpen(false)}}>
                <Sidebar/>
            </Drawer>
        </Box>
    )
}