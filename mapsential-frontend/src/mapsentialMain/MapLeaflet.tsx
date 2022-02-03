// @ts-nocheck

import {MapContainer, TileLayer} from 'react-leaflet'
import React, {useContext, useEffect, useState, useRef} from 'react'
import {StoreContext} from "./Store";
import {locationDetails} from "./Types";
import MarkerWrapper from "./MarkerWrapper";
import MarkerClusterGroup from "react-leaflet-cluster";
import L, {Map} from 'leaflet';

export default function MapLeaflet(){
    // let mapContainer;
    //
    // const map: Map = L.map('map').setView([51.505, -0.09], 13);
    //
    // L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    // }).addTo(map);
    //
    // L.marker([51.5, -0.09]).addTo(map)
    //     .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
    //     .openPopup();

    return <div style={{height: 300}} ref={(el) => {
        if (el !== null) {
            const map: Map = L.map(el).setView([51.505, -0.09], 13);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            L.marker([51.5, -0.09]).addTo(map)
                .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
                .openPopup();
        }
    }} />;

    // const store = useContext(StoreContext)
    //
    // const [drinkingMarkers, setDrinkingMarkers] = useState<any>()
    // const [soupMarkers, setSoupMarkers] = useState<any>()
    // const [toiletMarkers, setToiletMarkers] = useState<any>()
    // const [defibrillatorMarkers, setDefibrillatorMarkers] = useState<any>()
    //
    // useEffect(() => {
    //     setDrinkingMarkers(store.locations.drinking_fountain_locations.map((marker: locationDetails) => {
    //         return (
    //             <MarkerWrapper {...marker} key={marker.locationId}/>
    //         )
    //     }))
    //     setSoupMarkers(store.locations.soup_Kitchen_locations.map((marker: locationDetails) => {
    //         return (
    //             <MarkerWrapper {...marker} key={marker.locationId}/>
    //         )
    //     }))
    //     setToiletMarkers(store.locations.toilet_locations.map((marker: locationDetails) => {
    //         return (
    //             <MarkerWrapper {...marker} key={marker.locationId}/>
    //         )
    //     }))
    //     setDefibrillatorMarkers(store.locations.defibrillator_locations.map((marker: locationDetails) => {
    //         return (
    //             <MarkerWrapper {...marker} key={marker.locationId}/>
    //         )
    //     }))
    // },[store.locations.toilet_locations,store.locations.defibrillator_locations,store.locations.drinking_fountain_locations,store.locations.soup_Kitchen_locations])
    //
    // return(
    //     <div>
    //         <MapContainer center={[52.520008, 13.404954]} zoom={13} minZoom={5} scrollWheelZoom={true} style={{height: "95vh",}} tap={false}>
    //             <TileLayer
    //                 attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    //                 url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    //             />
    //             <MarkerClusterGroup>
    //                 {store.checkboxes.drinking_fountain_checkbox && drinkingMarkers}
    //                 {store.checkboxes.soup_Kitchen_checkbox && soupMarkers}
    //                 {store.checkboxes.toilet_checkbox && toiletMarkers}
    //                 {store.checkboxes.defibrillator_checkbox && defibrillatorMarkers}
    //             </MarkerClusterGroup>
    //         </MapContainer>
    //     </div>
    // )
}