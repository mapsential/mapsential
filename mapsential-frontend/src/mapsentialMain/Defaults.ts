import {locationDetails, locationList} from "./Types";

export const locationDefault : locationDetails = {
    locationId: 0,
    detailsId: 0,
    locationType: "undefined",
    locationName: "undefined",
    locationAddress: "undefined",
    longitude: 0,
    latitude: 0
}

export const storeContextDefault = {
    checkboxes: {
        drinking_fountain_checkbox: true,
        setDrinking_Fountain_checkbox: (value: boolean): void => {
        },
        soup_Kitchen_checkbox: true,
        setSoup_Kitchen_checkbox: (value: boolean): void => {
        },
        toilet_checkbox: true,
        setToilet_checkbox: (value: boolean): void => {
        },
        defibrillator_checkbox: true,
        setDefibrillator_checkbox: (value: boolean): void => {
        }
    },
    locations: {
        drinking_fountain_locations: [locationDefault],
        setDrinking_Fountain_locations: (value: locationList): void => {
        },
        soup_Kitchen_locations: [locationDefault],
        setSoup_Kitchen_locations: (value: locationList): void => {
        },
        toilet_locations: [locationDefault],
        setToilet_locations: (value: locationList): void => {
        },
        defibrillator_locations: [locationDefault],
        setDefibrillator_locations: (value: locationList): void => {
        }
    }
}