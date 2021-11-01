import {Marker, Popup} from "react-leaflet";
import React, {useMemo, useState} from "react";
import {locationDetails} from "./Types";
import LocationInformation from "./LoctionInformation";
import * as L from "leaflet"

const axios = require('axios')

const locationType = new Map()
locationType.set('soup_kitchen', 'Tafel')
locationType.set('drinking_fountain', 'Trinkbrunnen')
locationType.set('toilet', 'Toilette')
locationType.set('defibrillator', 'Defibrilator')

let icon : any

export default function MarkerWrapper(marker : locationDetails) {

    if(marker.locationType === "toilet"){
        icon = L.icon({
            iconUrl: 'https://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|00FF00&chf=a,s,ee00FFFF',
        })
    }
    else if(marker.locationType ==="drinking_fountain"){
        icon = L.icon({
            iconUrl: 'https://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|2ACAEA&chf=a,s,ee00FFFF',
        })
    }
    else if(marker.locationType ==="soup_kitchen"){
        icon = L.icon({
            iconUrl: 'https://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|FFFF00&chf=a,s,ee00FFFF',
        })
    }
    else if(marker.locationType ==="defibrillator"){
        icon = L.icon({
            iconUrl: 'https://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|990000&chf=a,s,ee00FFFF',
        })
    }
    const [locationInformation,setLocationInformation] = useState<any>()
    const eventHandlers = useMemo(
        () => ({
            click() {
                axios.get("http://87.138.112.67:11180//api/details/" + marker.locationType + "/" + marker.detailsId).then((response : any) => {
                    setLocationInformation(
                        <LocationInformation {...marker} {...response.data}/>
                    )
                })
            },
        }),
        [],
    )
    return (
        <Marker position={[marker.latitude, marker.longitude]} icon={icon} eventHandlers={eventHandlers}>
            <Popup>
                {locationInformation}
            </Popup>
        </Marker>
    )
}