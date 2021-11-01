import {MapContainer, TileLayer} from 'react-leaflet'
import React, {useContext, useEffect, useState} from 'react'
import {StoreContext} from "./Store";
import MarkerClusterGroup from 'react-leaflet-markercluster'
import {locationDetails} from "./Types";
import MarkerWrapper from "./MarkerWrapper";

export default function MapLeaflet(){

    const store = useContext(StoreContext)

    const [drinkingMarkers, setDrinkingMarkers] = useState<any>()
    const [soupMarkers, setSoupMarkers] = useState<any>()
    const [toiletMarkers, setToiletMarkers] = useState<any>()
    const [defibrillatorMarkers, setDefibrillatorMarkers] = useState<any>()

    useEffect(() => {
        setDrinkingMarkers(store.locations.drinking_fountain_locations.map((marker: locationDetails) => {
            return (
                <MarkerWrapper {...marker} key={marker.locationId}/>
            )
        }))
        setSoupMarkers(store.locations.soup_Kitchen_locations.map((marker: locationDetails) => {
            return (
                <MarkerWrapper {...marker} key={marker.locationId}/>
            )
        }))
        setToiletMarkers(store.locations.toilet_locations.map((marker: locationDetails) => {
            return (
                <MarkerWrapper {...marker} key={marker.locationId}/>
            )
        }))
        setDefibrillatorMarkers(store.locations.defibrillator_locations.map((marker: locationDetails) => {
            return (
                <MarkerWrapper {...marker} key={marker.locationId}/>
            )
        }))
    },[store.locations.toilet_locations,store.locations.defibrillator_locations,store.locations.drinking_fountain_locations,store.locations.soup_Kitchen_locations])
    return(
        <div>
            <MapContainer center={[52.520008, 13.404954]} zoom={13} minZoom={5} scrollWheelZoom={true} style={{height: "95vh",}} tap={false}>
                <TileLayer
                    attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <MarkerClusterGroup disableClusteringAtZoom={18} spiderfyOnMaxZoom={false}>
                    {store.checkboxes.drinking_fountain_checkbox && drinkingMarkers}
                    {store.checkboxes.soup_Kitchen_checkbox && soupMarkers}
                    {store.checkboxes.toilet_checkbox && toiletMarkers}
                    {store.checkboxes.defibrillator_checkbox && defibrillatorMarkers}
                </MarkerClusterGroup>
            </MapContainer>
        </div>
    )
}