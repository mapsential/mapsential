import React from 'react'
import MapLeaflet from '../mapsentialMain/MapLeaflet'
import {Navbar} from "./Navbar";
import {Box} from '@mui/material'
import Contexts from "./Contexts"

export default function MapsentialMain() {
    return (
        // Important! Always set the container height explicitly
        <Contexts>
                    <Box maxHeight="100%" height="100%">
                        <Navbar/>
                        <MapLeaflet/>
                    </Box>
        </Contexts>
    )
}