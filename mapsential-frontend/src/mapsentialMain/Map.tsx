import React, {useContext} from 'react'
import GoogleMapReact from 'google-map-react'
import Marker from "./Marker"
import {CheckboxContext, LocationContext} from "./MapsentialMain";

export type LocationInformation = {
    lat: number,
    lng: number,
    name: string,
    type?: string
}

type locationDetails = {
    locationId: number,
    detailsId: number,
    locationType: string,
    locationName: string,
    locationAddress: string,
    longitude: number,
    latitude: number
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
    const locations = useContext(LocationContext)
    console.log(locations)
    let markers = locations.location.map((marker: locationDetails) => {
        if ((marker.locationType.toLowerCase() === "water_fountain" && checkboxes.c1 === true) || (marker.locationType.toLocaleLowerCase() === "soup_kitchen" && checkboxes.c2 === true) || (marker.locationType.toLocaleLowerCase() === "toilet" && checkboxes.c3 === true)) {
            console.log(marker)
            return (<Marker lat={marker.latitude / 10} lng={marker.longitude / 10} name={marker.locationName}
                            key={Math.random() * 100000} adress={marker.locationAddress} type={marker.locationType}/>)
        } else {
            return (null)
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