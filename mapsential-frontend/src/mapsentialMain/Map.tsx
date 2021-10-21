import React, {useContext} from 'react'
import GoogleMapReact from 'google-map-react'
import Marker from "./Marker"
import {CheckboxContext} from "./MapsentialMain";

export type LocationInformation = {
    lat: number,
    lng: number,
    name: string,
    type?: string
}
let locations: Array<LocationInformation> = [
    {
        lat: 52.42515,
        lng: 13.320114,
        name: "Berliner Wasserbetriebe - Öffentliche Trinkbrunnen",
        type: "drinking_fountain"
    },
    {
        lat: 52.455401, lng: 13.302277, name: "Berliner Wasserbetriebe - Öffentliche Trinkbrunnen", type: "soup_kitchen"
    },
    {
        lat: 52.476613, lng: 13.210473, name: "Berliner Wasserbetriebe - Öffentliche Trinkbrunnen", type: "toilet"
    }
]

export default function Map() {
    const defaultProps = {
        center: {
            lat: 52.520008,
            lng: 13.404954
        },
        zoom: 12
    };
    const checkboxes = useContext(CheckboxContext)
    const markers = locations.map((marker: LocationInformation) => {
        if ((marker.type === "drinking_fountain" && checkboxes.c1 === true) || (marker.type === "soup_kitchen" && checkboxes.c2 === true) || (marker.type === "toilet" && checkboxes.c3 === true)) {
            return (<Marker lat={marker.lat} lng={marker.lng} text={marker.name} key={Math.random()*100000}/>)
        }
        else{
            return(null)
        }
    })
    return (
        // Important! Always set the container height explicitly
        <div style={{height: '90vh', width: '100%'}}>
            <GoogleMapReact
                bootstrapURLKeys={{key: "AIzaSyAZaCnnDwAhbdWre8eKZW47Fm1FlxK1ysU"}}
                defaultCenter={defaultProps.center}
                defaultZoom={defaultProps.zoom}>
                {markers}
            </GoogleMapReact>
        </div>
    )
}