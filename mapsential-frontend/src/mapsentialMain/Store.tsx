import React, {createContext, useEffect, useState} from 'react'
import {CommentList, Location, RouteStatus} from "./Types";
import Leaflet from "leaflet";
import "leaflet-routing-machine"
import "leaflet-routing-machine/dist/leaflet-routing-machine.css"
import 'leaflet.markercluster/dist/leaflet.markercluster.js'
import 'leaflet-routing-machine'
import 'leaflet-control-geocoder'
import 'leaflet-control-geocoder/dist/Control.Geocoder.css'


const MAP_CENTER: Leaflet.LatLngExpression = [52.520008, 13.404954];  // Center of berlin
const MAP_ZOOM = 13;
const MAP_TILES_URL_TEMPLATE = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const MAP_TILES_LAYER_OPTIONS: Leaflet.TileLayerOptions = {
    attribution: '&copy; <a class="map-copyright" href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    minZoom: 5,
}
const MAP_MAPBOX_URL = "https://api.mapbox.com/directions/v5"


export type LocationTypeEntry = {
    locations: Location[],
    isDisplayingMapLayer: boolean,
    mapLayer: Leaflet.LayerGroup,
}

export type LocationTypes = {
    [locationType: string]: LocationTypeEntry,
}

type GlobalMapEntries = {
    map: Leaflet.Map,
    mapClusterLayer: Leaflet.LayerGroup,
    mapDiv: HTMLDivElement,
    mapRoutingControl: Leaflet.Routing.Control,
    mapRoutingPlan: Leaflet.Routing.Plan,
}

export type StoreContext = GlobalMapEntries & {
    locationTypes: LocationTypes,
    setLocationTypes: (locatonTypes: LocationTypes) => void,
    toggleLocationType: (locationType: string) => void,
    locationsStatus: "loading" | "loaded" | "failed",
    setLocationsStatus: (locationStatus: "loading" | "loaded" | "failed") => void,
    currentLocation: Leaflet.LatLng | null,
    routeStatus: RouteStatus,
    setRouteStatus: (status: RouteStatus) => void,
    commentDialogOpen: boolean,
    setCommentDialogOpen: (open: boolean) => void
    currentComments: number,
    setCurrentComments: (detailsId: number) => void,
    commentMap: Map<number, CommentList>,
}


const StoreDefaults: StoreContext = {
    locationTypes: {},
    setLocationTypes: () => {},
    toggleLocationType: () => {},
    locationsStatus: "loading",
    setLocationsStatus: (): void => {},
    ...createGlobalMapEntries(),
    currentLocation: null,
    routeStatus: "no-route",
    setRouteStatus: () => {},
    commentDialogOpen: false,
    setCommentDialogOpen: (): void => {},
    currentComments: 0,
    setCurrentComments: () : void => {},
    commentMap: new Map<number, CommentList>()
}


export const StoreContext = createContext<StoreContext>(StoreDefaults);


export default function Store ({children}: {children: React.ReactNode | React.ReactNode[]}) {
    const [locationTypes, setLocationTypes] = useState<LocationTypes>(StoreDefaults.locationTypes);
    const [locationsStatus, setLocationsStatus] = useState<"loading" | "loaded" | "failed">(StoreDefaults.locationsStatus);

    const toggleLocationType = (locationType: string): void => {
        const locationTypesEntry = store.locationTypes[locationType]

        let clusterLayerOperation: (layer: Leaflet.Layer) => void
        let newIsDisplayingMapLayer: boolean
        if (locationTypesEntry.isDisplayingMapLayer) {
            clusterLayerOperation = store.mapClusterLayer.removeLayer.bind(store.mapClusterLayer)
            newIsDisplayingMapLayer = false
        } else {
            clusterLayerOperation = store.mapClusterLayer.addLayer.bind(store.mapClusterLayer)
            newIsDisplayingMapLayer = true
        }

        clusterLayerOperation(locationTypesEntry.mapLayer)
        setLocationTypes({
            ...locationTypes,
            [locationType]: {
                ...locationTypesEntry,
                isDisplayingMapLayer: newIsDisplayingMapLayer,
            }
        })
    } 

    const [routeStatus, setRouteStatus] = useState<RouteStatus>(StoreDefaults.routeStatus)

    const [commentDialogOpen, setCommentDialogOpen] = useState<boolean>(StoreDefaults.commentDialogOpen)
    const [currentComments, setCurrentComments] = useState<number>(StoreDefaults.currentComments)

    let store: StoreContext = {
        ...StoreDefaults,
        locationTypes,
        setLocationTypes,
        toggleLocationType,
        locationsStatus,
        setLocationsStatus,
        routeStatus,
        setRouteStatus,
        commentDialogOpen,
        setCommentDialogOpen,
        currentComments,
        setCurrentComments,
    }

    useEffect(() => {
        store.map.on("locationfound", (e) => {
            store.currentLocation = e.latlng
        })
    
        store.map.on("locationerror", (err) => {
            // TODO: Display error message to user
            console.error(`Could not find location: ${err.message}`)
        })
    
        store.map.locate({watch: true})
    }, [])

    return <StoreContext.Provider value={store}>{children}</StoreContext.Provider>
}

function createGlobalMapEntries(): GlobalMapEntries {
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
            if (waypointIndex >= numberWaypoints - 1) {
                return null as unknown as Leaflet.Marker<null>
            }

            return Leaflet.marker(waypoint.latLng, {
                icon: Leaflet.icon({
                    iconUrl: "./marker-icon-waypoint.png",
                    iconSize: [25, 41],
                    iconAnchor: [25/ 2, 41],
                })
            })
        },
        language: "de",
    })
    const mapRoutingControl = Leaflet.Routing.control({
        plan: mapRoutingPlan,
        router: Leaflet.Routing.mapbox(process.env.REACT_APP_MAPBOX_ACCESS_TOKEN as string, {
            serviceUrl: MAP_MAPBOX_URL,
            profile: "mapbox/walking",
            language: "de",
        }),
        addWaypoints: false,
    })

    return {map, mapDiv, mapClusterLayer, mapRoutingControl, mapRoutingPlan}
}