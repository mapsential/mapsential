import {LocationType} from "./Types";
import Leaflet from "leaflet";

async function createLeafletIconByLocationType(locationType: LocationType): Promise<Leaflet.Icon> {
    const img = new Image()
    img.src = `marker-icon-${locationType}.png`
    await (new Promise<void>(resolve => img.onload = () => resolve()))

    return Leaflet.icon({
        iconUrl: img.src,
        iconSize: [img.width, img.height],
        iconAnchor: [img.width / 2, img.height],
        popupAnchor: [0, -0.75 * img.height],
    });
}

let _icons: null | Record<LocationType, Leaflet.Icon> = null;
export async function getMapIcons(): Promise<Record<LocationType, Leaflet.Icon>> {
    if (_icons !== null) {
        return _icons;
    }

    _icons = {
        "defibrillator": (await createLeafletIconByLocationType("defibrillator")),
        "drinking_fountain": (await createLeafletIconByLocationType("drinking_fountain")),
        "soup_kitchen": (await createLeafletIconByLocationType("soup_kitchen")),
        "toilet": (await createLeafletIconByLocationType("toilet")),
    }

    return _icons;
}