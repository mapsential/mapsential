import {Location, LocationType, RouteStatus} from "./Types"
import Leaflet from "leaflet"
import 'leaflet.markercluster/dist/leaflet.markercluster.js'
import 'leaflet-routing-machine'
import 'leaflet-control-geocoder'
import 'leaflet-control-geocoder/dist/Control.Geocoder.css'

const MAP_CENTER: Leaflet.LatLngExpression = [52.520008, 13.404954];  // Center of berlin
const MAP_ZOOM = 13;
const MAP_TILES_URL_TEMPLATE = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const MAP_TILES_LAYER_OPTIONS: Leaflet.TileLayerOptions = {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    minZoom: 5,
}
const MAP_OSRM_URL = "https://routing.openstreetmap.de/routed-foot/route/v1"

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
    mapRoutingControl: Leaflet.Routing.Control,
    mapRoutingPlan: Leaflet.Routing.Plan,
    currentLocation: Leaflet.LatLng | null,
    routeStatus: RouteStatus,
    setRouteStatus: (status: RouteStatus) => void,
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
    },
    currentLocation: null,
    routeStatus: "no-route",
    setRouteStatus: () => {},
}

function createMapAndMapDiv(): {
    map: Leaflet.Map, 
    mapDiv: HTMLDivElement, 
    mapClusterLayer: Leaflet.LayerGroup,
    mapRoutingControl: Leaflet.Routing.Control,
    mapRoutingPlan: Leaflet.Routing.Plan,
} {
    // Create div and use div for leaflet map
    const mapDiv = document.createElement('div')
    mapDiv.classList.add('map')
    const map = Leaflet.map(mapDiv).setView(MAP_CENTER, MAP_ZOOM)

    // Add openstreet maps tiles
    Leaflet.tileLayer(MAP_TILES_URL_TEMPLATE, MAP_TILES_LAYER_OPTIONS).addTo(map)

    // Add cluster layer for location markers
    const mapClusterLayer = Leaflet.markerClusterGroup()
    map.addLayer(mapClusterLayer)

    // Add routing
    const mapRoutingPlan = Leaflet.Routing.plan([], {
        geocoder: (Leaflet.Control as any).Geocoder.nominatim({
            language: "de",
        }),
        createMarker: (waypointIndex: number, waypoint: Leaflet.Routing.Waypoint, numberWaypoints: number) => {
            return null as unknown as Leaflet.Marker<any>
        },
        language: "de",
    })
    const mapRoutingControl = Leaflet.Routing.control({
        plan: mapRoutingPlan,
        router: Leaflet.Routing.osrmv1({
            serviceUrl: MAP_OSRM_URL,
            language: "de",
        }),
        addWaypoints: false,
    });

    return {map, mapDiv, mapClusterLayer, mapRoutingControl, mapRoutingPlan}
}