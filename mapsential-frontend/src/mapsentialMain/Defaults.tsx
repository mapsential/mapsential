import {Location, LocationType} from "./Types";
import Leaflet from "leaflet";
import 'leaflet.markercluster/dist/leaflet.markercluster.js';

const MAP_CENTER: Leaflet.LatLngExpression = [52.520008, 13.404954];  // Center of berlin
const MAP_ZOOM = 13;
const MAP_TILES_URL_TEMPLATE = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const MAP_TILES_LAYER_OPTIONS: Leaflet.TileLayerOptions = {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    minZoom: 5,
}

export interface IStoreContext {
    checkboxes: {
        defibrillator_checkbox: boolean,
        setDefibrillator_checkbox: (isChecked: boolean) => void,
        drinking_fountain_checkbox: boolean,
        setDrinking_Fountain_checkbox: (isChecked: boolean) => void,
        soup_Kitchen_checkbox: boolean,
        setSoup_Kitchen_checkbox: (isChecked: boolean) => void,
        toilet_checkbox: boolean,
        setToilet_checkbox: (isChecked: boolean) => void,
    },
    locations: {
        defibrillator_locations: Location[],
        setDefibrillator_locations: (locations: Location[]) => void,
        drinking_fountain_locations: Location[],
        setDrinking_Fountain_locations: (locations: Location[]) => void,
        soup_Kitchen_locations: Location[],
        setSoup_Kitchen_locations: (locations: Location[]) => void,
        toilet_locations: Location[],
        setToilet_locations: (locations: Location[]) => void,
    },
    map: Leaflet.Map,
    mapClusterLayer: Leaflet.LayerGroup,
    mapDiv: HTMLDivElement,
    mapLayers: Partial<Record<LocationType, Leaflet.Layer>>,
    mapLayersRenderStatus: Record<LocationType, boolean>,
}

export const storeContextDefault: IStoreContext = {
    checkboxes: {
        defibrillator_checkbox: true,
        setDefibrillator_checkbox: (isChecked: boolean): void => {
        },
        drinking_fountain_checkbox: true,
        setDrinking_Fountain_checkbox: (isChecked: boolean): void => {
        },
        soup_Kitchen_checkbox: true,
        setSoup_Kitchen_checkbox: (isChecked: boolean): void => {
        },
        toilet_checkbox: true,
        setToilet_checkbox: (isChecked: boolean): void => {
        },
    },
    locations: {
        defibrillator_locations: [],
        setDefibrillator_locations: (locations: Location[]): void => {
        },
        drinking_fountain_locations: [],
        setDrinking_Fountain_locations: (locations: Location[]): void => {
        },
        soup_Kitchen_locations: [],
        setSoup_Kitchen_locations: (locations: Location[]): void => {
        },
        toilet_locations: [],
        setToilet_locations: (locations: Location[]): void => {
        },
    },
    ...createMapAndMapDiv(),
    mapLayers: {},
    mapLayersRenderStatus: {
        "defibrillator": false,
        "drinking_fountain": false,
        "soup_kitchen": false,
        "toilet": false,
    }
}

function createMapAndMapDiv(): {map: Leaflet.Map, mapDiv: HTMLDivElement, mapClusterLayer: Leaflet.LayerGroup} {
    const mapDiv = document.createElement('div')
    mapDiv.classList.add('map')
    const map = Leaflet.map(mapDiv).setView(MAP_CENTER, MAP_ZOOM)

    Leaflet.tileLayer(MAP_TILES_URL_TEMPLATE, MAP_TILES_LAYER_OPTIONS).addTo(map)

    const mapClusterLayer = Leaflet.markerClusterGroup();
    map.addLayer(mapClusterLayer);

    return {map, mapDiv, mapClusterLayer}
}