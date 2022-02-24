import React from 'react'
import {LocationDetails, Location} from "./Types";
import {Typography, Button} from "@mui/material";
import {Dvr, FoodBank, Water, Wc} from "@mui/icons-material";

const translations = new Map()
translations.set('soup_kitchen', 'Tafel')
translations.set('drinking_fountain', 'Trinkbrunnen')
translations.set('toilet', 'Toilette')
translations.set('defibrillator', 'Defibrillator')
translations.set("yes","Ja")
translations.set("no","Nein")
translations.set("limited","Limitiert")

export default function LocationInformation({location, details}: {location: Location, details: LocationDetails})  {
    return (
        <div>
            {location.locationType === "drinking_fountain" &&
                    <div style={{display:"flex"}}>
                        <Water/><Typography variant="h6" style={{marginLeft:4}}>{translations.get(location.locationType.toLowerCase())}</Typography>
                    </div>
            }
            {location.locationType === "soup_kitchen" &&
                <div style={{display:"flex"}}>
                    <FoodBank/> <Typography variant="h6" style={{marginLeft:4}}> {translations.get(location.locationType.toLowerCase())}</Typography>
                </div>
            }
            {location.locationType === "toilet" &&
                <div style={{display:"flex"}}>
                    <Wc/>  <Typography variant="h6" style={{marginLeft:4}}> {translations.get(location.locationType.toLowerCase())}</Typography>
                </div>
            }
            {location.locationType === "defibrillator" &&
            <div style={{display: "flex"}}>
                <Dvr/><Typography variant="h6" style={{marginLeft: 4}}> {translations.get(location.locationType.toLowerCase())}</Typography>
            </div>
            }
            <Typography>{location.locationName}</Typography>
            <Typography>Adresse: {location.locationAddress}</Typography>
            {"openingTimes" in details && <Typography>Öffnungszeiten: {details.openingTimes}</Typography>}
            {"male" in details && (details.male ? <span>M: Ja<br/></span> : <span>M: Nein<br/></span>)}
            {"female" in details && (details.female ? <span>W: Ja<br/></span> : <span>W: Nein<br/></span>)}
            {"unisex" in details && (details.unisex ? <span>Unisex: Ja<br/></span> : <span>Unisex Nein<br/></span>)}
            {"wheelchairAccessible" in details && <span>Rollstuhlgerecht: {translations.get(details.wheelchairAccessible)}<br/></span>}
            {"hasFee" in details && (details.hasFee ? <span>Kostenlos: Nein<br/></span>: <span>Kostenlos: Ja<br/></span>)}
            {"hasHandWashing" in details && (details.hasHandWashing ? <span>Waschbecken: Ja<br/></span>: <span>Waschbecken: Nein<br/></span>)}
            {"hasPaper" in details && (details.hasPaper ? <span>Papier: Ja<br/></span>: <span>Papier: Nein<br/></span>)}
            {"changeTable" in details && (details.changeTable ? <span>Wickeltisch: Ja<br/></span> : <span>Wickeltisch: Ja<br/></span>)}
            <Button id={`locationButton${location.locationId}`}>Route anzeigen</Button>
            <Button id={`commentButton:${location.locationId}`}>Kommentare anzeigen</Button>
        </div>
    )
}