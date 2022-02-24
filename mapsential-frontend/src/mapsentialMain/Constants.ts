import { LocationType } from "./Types";



export const locationTypes: ["defibrillator", "drinking_fountain", "soup_kitchen", "toilet"] = ["defibrillator", "drinking_fountain", "soup_kitchen", "toilet"]

export const locationTypeNames: Record<LocationType, {singular: string, plural: string}> = {
    "defibrillator": {singular: "Defibrillator", plural: "Defibrillatoren"},
    "drinking_fountain": {singular: "Trinkbrunnen", plural: "Trinkbrunnen"},
    "soup_kitchen": {singular: "Tafel", plural: "Tafeln"},
    "toilet": {singular: "Toilette", plural: "Toiletten"},
}

export const locationTypesSortedByNames: LocationType[] = locationTypes.sort((a: LocationType, b: LocationType): -1 | 0 | 1 => {
    const nameA = locationTypeNames[a].singular;
    const nameB = locationTypeNames[b].singular;

    if (nameA < nameB) {
        return -1
    } 
    
    if (nameB > nameA) {
        return 1
    }

    return 0
})

export const locationTypeColors: Record<LocationType, string> = {
    "drinking_fountain": "blue",
    "soup_kitchen": "gold",
    "toilet": "green",
    "defibrillator": "red",
}