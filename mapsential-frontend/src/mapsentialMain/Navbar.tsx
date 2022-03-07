import { ArrowBackIosNew, ArrowForwardIos, CloseRounded } from "@mui/icons-material";
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Toolbar from '@mui/material/Toolbar';
import { useEffect, useState } from 'react';
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import { fetchTips } from './Controllers';
import Logo from './Logo';
import './Navbar.css';

export const Navbar = () => {
    const [popupOpen, setPopupOpen] = useState(false);
    const closePopup = () => setPopupOpen(false);
    const openPopup = () => setPopupOpen(true);
    useEffect(() => {
        fetchTips().then(tips => setTips(tips));
    }, []);
    const [tips, setTips] = useState<string[]>([]);
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
                <Toolbar className="toolbar">
                    <Logo />
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
        </Box>
    )
}