import { Dvr, FoodBank, Water, Wc } from "@mui/icons-material";
import { Button, Typography } from "@mui/material";
import { Location, LocationDetails } from "./Types";

const LOCATION_TYPE_NAMES_TO_ICONS: { [locationTypeName: string]: JSX.Element } = {
    "defibrillator": <Dvr />,
    "drinking_fountain": <Water />,
    "soup_kitchen": <FoodBank />,
    "toilet": <Wc />,
}

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
            <div style={{display:"flex"}}>
                {LOCATION_TYPE_NAMES_TO_ICONS[location.type]}
                <Typography variant="h6" style={{marginLeft:4}}>
                    {translations.get(location.type)}
                </Typography>
            </div>

            <Typography>{details.name}</Typography>
            <Typography>Adresse: {details.address}</Typography>
            {"openingTimes" in details && <Typography>Öffnungszeiten: {details.opening_times}</Typography>}
            {"male" in details && (details.male ? <span>M: Ja<br/></span> : <span>M: Nein<br/></span>)}
            {"female" in details && (details.female ? <span>W: Ja<br/></span> : <span>W: Nein<br/></span>)}
            {"unisex" in details && (details.unisex ? <span>Unisex: Ja<br/></span> : <span>Unisex Nein<br/></span>)}
            {"wheelchairAccessible" in details && <span>Rollstuhlgerecht: {translations.get(details.wheelchair_accessible)}<br/></span>}
            {"hasFee" in details && (details.has_fee ? <span>Kostenlos: Nein<br/></span>: <span>Kostenlos: Ja<br/></span>)}
            {"hasHandWashing" in details && (details.has_hand_washing ? <span>Waschbecken: Ja<br/></span>: <span>Waschbecken: Nein<br/></span>)}
            {"hasPaper" in details && (details.has_paper ? <span>Papier: Ja<br/></span>: <span>Papier: Nein<br/></span>)}
            {"changeTable" in details && (details.change_table ? <span>Wickeltisch: Ja<br/></span> : <span>Wickeltisch: Ja<br/></span>)}

            <Button id={`locationButton${location.id}`}>Route anzeigen</Button>
            <Button id={`commentButton:${location.id}`}>Kommentare anzeigen</Button>
        </div>
    )
}