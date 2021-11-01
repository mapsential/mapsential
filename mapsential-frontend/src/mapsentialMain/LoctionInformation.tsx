import React from 'react'
import {locationDetails} from "./Types";
import {Typography} from "@mui/material";
import {Dvr, FoodBank, Water, Wc} from "@mui/icons-material";

const locationType = new Map()
locationType.set('soup_kitchen', 'Tafel')
locationType.set('drinking_fountain', 'Trinkbrunnen')
locationType.set('toilet', 'Toilette')
locationType.set('defibrillator', 'Defibrillator')
locationType.set("yes","Ja")
locationType.set("no","Nein")
locationType.set("limited","Limitiert")

export default function LocationInformation(marker : locationDetails)  {
    marker.locationType === "toilet" ? console.log(marker) : console.log()
    return (
        <div>
            {marker.locationType === "drinking_fountain" &&
                    <div style={{display:"flex"}}>
                        <Water/><Typography variant="h6" style={{marginLeft:4}}>{locationType.get(marker.locationType.toLowerCase())}</Typography>
                    </div>
            }
            {marker.locationType === "soup_kitchen" &&
                <div style={{display:"flex"}}>
                    <FoodBank/> <Typography variant="h6" style={{marginLeft:4}}> {locationType.get(marker.locationType.toLowerCase())}</Typography>
                </div>
            }
            {marker.locationType === "toilet" &&
                <div style={{display:"flex"}}>
                    <Wc/>  <Typography variant="h6" style={{marginLeft:4}}> {locationType.get(marker.locationType.toLowerCase())}</Typography>
                </div>
            }
            {marker.locationType === "defibrillator" &&
            <div style={{display: "flex"}}>
                <Dvr/><Typography variant="h6" style={{marginLeft: 4}}> {locationType.get(marker.locationType.toLowerCase())}</Typography>
            </div>
            }
            <Typography>{marker.locationName}</Typography>
            <Typography>Adresse: {marker.locationAddress}</Typography>
            {((marker.locationType === "drinking_fountain") || (marker.locationType === "soup_kitchen" || (marker.locationType) ==="toilet")) &&
                ("openingTimes" in marker ) && (<Typography>Öffnungszeiten: {marker.openingTimes}</Typography>)
            }
            {marker.locationType === "toilet" &&
            ((("male" in marker) || ("female" in marker) || ("unisex" in marker) || ("wheelchairAccessible" in marker) ||  ("hasFee" in marker) || ("hasHandWashing" in marker) || ("hasPaper" in marker) || ("changeTable" in marker)) &&
            <Typography>Sonstige Infos:<br/>
                {("male" in marker) && (marker.male ? <span>M: Ja<br/></span> : <span>M: Nein<br/></span>)}
                {("female" in marker) && (marker.female ? <span>W: Ja<br/></span> : <span>W: Nein<br/></span>)}
                {("unisex" in marker) && (marker.unisex ? <span>Unisex: Ja<br/></span> : <span>Unisex Nein<br/></span>)}
                {("wheelchairAccessible" in marker )&& <span>Rollstuhlgerecht: {locationType.get(marker.wheelchairAccessible)}<br/></span>}
                {("hasFee" in marker) &&(marker.hasFee ? <span>Kostenlos: Nein<br/></span>: <span>Kostenlos: Ja<br/></span>)}
                {("hasHandWashing" in marker )&&(marker.hasHandWashing ? <span>Waschbecken: Ja<br/></span>: <span>Waschbecken: Nein<br/></span>)}
                {("hasPaper" in marker )&&(marker.hasPaper ? <span>Papier: Ja<br/></span>: <span>Papier: Nein<br/></span>)}
                {("changeTable" in marker )&& (marker.changeTable ? <span>Wickeltisch: Ja<br/></span> : <span>Wickeltisch: Ja<br/></span>)}
            </Typography>
            )}
        </div>
    )
}