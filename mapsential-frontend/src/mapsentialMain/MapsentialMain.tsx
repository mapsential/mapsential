import React, {createContext, useState} from 'react'
import Map from '../mapsentialMain/Map'
import {Navbar} from "./Navbar";
import {Box} from '@mui/material'

export const CheckboxContext = createContext({
    c1: true,
    setC1: (value: boolean): void => {
    },
    c2: true,
    setC2: (value: boolean): void => {
    },
    c3: true,
    setC3: (value: boolean): void => {
    }
})
export default function MapsentialMain() {
    const [c1, setC1] = useState(true)
    const [c2, setC2] = useState(true)
    const [c3, setC3] = useState(true)
    const value = {c1, setC1, c2, setC2, c3, setC3}

    return (
        // Important! Always set the container height explicitly
        <CheckboxContext.Provider value={value}>
            <Box maxHeight="100%" height="100%">
                <Navbar/>
                <Map/>
            </Box>
        </CheckboxContext.Provider>
    )
}