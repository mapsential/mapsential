import React, {createContext, useEffect, useState} from 'react'
import {locationList} from "./Types";
import {locationDefault} from "./Defaults"
import axios from "axios";

export const StoreContext = createContext({
    checkboxes: {
        drinking_fountain_checkbox: true,
        setDrinking_Fountain_checkbox: (value: boolean): void => {
        },
        soup_Kitchen_checkbox: true,
        setSoup_Kitchen_checkbox: (value: boolean): void => {
        },
        toilet_checkbox: true,
        setToilet_checkbox: (value: boolean): void => {
        },
        defibrillator_checkbox: true,
        setDefibrillator_checkbox: (value: boolean): void => {
        }
    },
    locations: {
        drinking_fountain_locations: [locationDefault],
        setDrinking_Fountain_locations: (value: locationList): void => {
        },
        soup_Kitchen_locations: [locationDefault],
        setSoup_Kitchen_locations: (value: locationList): void => {
        },
        toilet_locations: [locationDefault],
        setToilet_locations: (value: locationList): void => {
        },
        defibrillator_locations: [locationDefault],
        setDefibrillator_locations: (value: locationList): void => {
        }
    }
})

export default function Contexts ({children} : any) {

    const [drinking_fountain_checkbox,setDrinking_Fountain_checkbox] = useState(true)
    const [soup_Kitchen_checkbox,setSoup_Kitchen_checkbox] = useState(true)
    const [toilet_checkbox,setToilet_checkbox] = useState(true)
    const [defibrillator_checkbox,setDefibrillator_checkbox] = useState(true)

    const [drinking_fountain_locations, setDrinking_Fountain_locations] = useState([locationDefault])
    const [soup_Kitchen_locations, setSoup_Kitchen_locations] = useState([locationDefault])
    const [toilet_locations, setToilet_locations] = useState([locationDefault])
    const [defibrillator_locations, setDefibrillator_locations] = useState([locationDefault])


    const store = {
        checkboxes: {
            drinking_fountain_checkbox,
            setDrinking_Fountain_checkbox,
            soup_Kitchen_checkbox,
            setSoup_Kitchen_checkbox,
            toilet_checkbox,setToilet_checkbox,
            defibrillator_checkbox,
            setDefibrillator_checkbox
        },
        locations:{
            drinking_fountain_locations,
            setDrinking_Fountain_locations,
            soup_Kitchen_locations,
            setSoup_Kitchen_locations,
            toilet_locations,
            setToilet_locations,
            defibrillator_locations,
            setDefibrillator_locations
        }
    }
    useEffect(() => {
        axios.get("http://87.138.112.67:11180/api/filter_location/drinking_fountain").then((response: any) => {
            store.locations.setDrinking_Fountain_locations(response.data)
        })
        axios.get("http://87.138.112.67:11180/api/filter_location/soup_kitchen").then((response: any) => {
            store.locations.setSoup_Kitchen_locations(response.data)
        })
        axios.get("http://87.138.112.67:11180/api/filter_location/toilet").then((response: any) => {
            store.locations.setToilet_locations(response.data)
        })
        axios.get("http://87.138.112.67:11180/api/filter_location/defibrillator").then((response: any) => {
            store.locations.setDefibrillator_locations(response.data)
        })
    },[])
    return <StoreContext.Provider value={store}>{children}</StoreContext.Provider>

}
