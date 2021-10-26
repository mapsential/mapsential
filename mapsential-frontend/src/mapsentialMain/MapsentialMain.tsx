import React, {createContext, useEffect, useState} from 'react'
import Map from '../mapsentialMain/Map'
import {Navbar} from "./Navbar";
import {Box} from '@mui/material'

const axios = require('axios')

type location = {
    locationId: number,
    detailsId: number,
    locationType: string,
    locationName: string,
    locationAddress: string,
    longitude: number,
    latitude: number
}[]

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

export const LocationContext = createContext({
    location: [{
        locationId: 0,
        detailsId: 0,
        locationType: "undefined",
        locationName: "undefined",
        locationAddress: "undefined",
        longitude: 0,
        latitude: 0
    }],
    setLocation: (value: location): void => {
    }
})

export default function MapsentialMain() {
    const [c1, setC1] = useState(true)
    const [c2, setC2] = useState(true)
    const [c3, setC3] = useState(true)
    const checkboxValue = {c1, setC1, c2, setC2, c3, setC3}
    const [location, setLocation] = useState([{
        locationId: 0,
        detailsId: 0,
        locationType: "undefined",
        locationName: "undefined",
        locationAddress: "undefined",
        longitude: 0,
        latitude: 0
    }])
    const locationValue = {location, setLocation}
    useEffect(() => {
        axios.get("http://localhost:8080/api/location").then((response: any) => {
            setLocation(response.data)
        })
            .then((error: any) => {

            })
    }, [])

    return (
        // Important! Always set the container height explicitly
        <CheckboxContext.Provider value={checkboxValue}>
            <LocationContext.Provider value={locationValue}>
                <Box maxHeight="100%" height="100%">
                    <Navbar/>
                    <Map/>
                </Box>
            </LocationContext.Provider>
        </CheckboxContext.Provider>
    )
}