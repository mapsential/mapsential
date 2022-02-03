// @ts-nocheck

// import {MapContainer, TileLayer} from 'react-leaflet'
import React, {useContext, useEffect, useState, useRef} from 'react'
import {StoreContext} from "./Store";
import {locationDetails} from "./Types";
import MarkerWrapper from "./MarkerWrapper";
// import MarkerClusterGroup from "react-leaflet-cluster";
import L, {Map} from 'leaflet';
import ReactDOM from "react";

const mapDiv: HTMLDivElement = document.createElement('div');
mapDiv.style.height = '95vh';
const map: Map = L.map(mapDiv).setView([52.520008, 13.404954], 13, );

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    minZoom: 5,
    scrollWheelZoom: true,
    tap: false,
}).addTo(map);

export default function MapLeaflet(){
    const store = useContext(StoreContext)

    // const [drinkingMarkers, setDrinkingMarkers] = useState<any>()
    // const [soupMarkers, setSoupMarkers] = useState<any>()
    // const [toiletMarkers, setToiletMarkers] = useState<any>()
    // const [defibrillatorMarkers, setDefibrillatorMarkers] = useState<any>()
    //
    // useEffect(() => {
    //     setDrinkingMarkers(store.locations.drinking_fountain_locations.map((marker: locationDetails) => {return [marker.longitude, marker.latitude]}))
    //     // setSoupMarkers(store.locations.soup_Kitchen_locations.map((marker: locationDetails) => {
    //     //
    //     // }))
    //     // setToiletMarkers(store.locations.toilet_locations.map((marker: locationDetails) => {
    //     // }))
    //     // setDefibrillatorMarkers(store.locations.defibrillator_locations.map((marker: locationDetails) => {
    //     //
    //     // }))
    // },[store.locations.toilet_locations,store.locations.defibrillator_locations,store.locations.drinking_fountain_locations,store.locations.soup_Kitchen_locations])

    return <div style={{height: '100%', width: '100%'}} ref={(el) => {
        if (el !== null) {
            el.appendChild(mapDiv);

            for (
                const locationsSet of [
                    store.locations.drinking_fountain_locations,
                    store.locations.soup_Kitchen_locations,
                    store.locations.toilet_locations,
                    store.locations.defibrillator_locations
            ]) {
                const markers = L.markerClusterGroup();
                for (const location of locationsSet) {
                    const marker = L.marker([location.latitude, location.longitude]);
                    marker.on('click', (event) => {
                        const popup = event.target.getPopup();
                        // const inner: HTMLDivElement = document.createElement('div');
                        // ReactDOM.render(<MarkerWrapper {...location} key={location.locationId}/>, inner);
                        // popup.setContent(inner);
                        popup.setContent(`<p>${location.locationName}</p>`)
                    });
                    marker.bindPopup(L.popup());
                    markers.addLayer(marker);
                }
                map.addLayer(markers);
            }
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