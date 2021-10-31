import React from 'react'
import {locationDetails} from "./Types";
import {Typography} from "@mui/material";
import {Dvr, FoodBank, Water, WaterRounded, Wc} from "@mui/icons-material";

const locationType = new Map()
locationType.set('soup_kitchen', 'Tafel')
locationType.set('drinking_fountain', 'Trinkbrunnen')
locationType.set('toilet', 'Toilette')
locationType.set('defibrillator', 'Defibrillator')

export default function LocationInformation(marker : locationDetails)  {
    return (
        <div>
            {marker.locationType === "drinking_fountain" &&
                <div>
                    <Typography variant="h6"><Water/> {locationType.get(marker.locationType.toLowerCase())}</Typography>
                    <Typography>{marker.locationName}</Typography>
                    <Typography>Adresse: {marker.locationAddress}</Typography>
                    <Typography>Öffnungszeiten: {marker.openingTimes}</Typography>
                </div>
            }
            {marker.locationType === "soup_kitchen" &&
            <div>
                <Typography variant="h6"><FoodBank/> {locationType.get(marker.locationType.toLowerCase())}</Typography>
                <Typography>{marker.locationName}</Typography>
                <Typography>Adresse: {marker.locationAddress}</Typography>
                <Typography>Öffnungszeiten: {marker.openingTimes}</Typography>
            </div>
            }
            {marker.locationType === "toilet" &&
            <div>
                <Typography variant="h6"><Wc/> {locationType.get(marker.locationType.toLowerCase())}</Typography>
                <Typography>{marker.locationName}</Typography>
                <Typography>Adresse: {marker.locationAddress}</Typography>
            </div>
            }
            {marker.locationType === "defibrillator" &&
            <div>
                <Typography variant="h6"><Dvr/> {locationType.get(marker.locationType.toLowerCase())}</Typography>
                <Typography>{marker.locationName}</Typography>
                <Typography>Adresse: {marker.locationAddress}</Typography>
            </div>
            }
        </div>
    )
}