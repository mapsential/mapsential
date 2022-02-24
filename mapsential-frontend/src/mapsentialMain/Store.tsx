import React, {createContext, useEffect, useState} from 'react'
import axios from "axios";
import {Location, LocationDetails, LocationType, RouteStatus} from "./Types";
import Leaflet from "leaflet";
import {getMapIcons} from "./MapIcons";
import ReactDOM from "react-dom";
import LocationInformation from "./LoctionInformation";
import "leaflet-routing-machine"
import "leaflet-routing-machine/dist/leaflet-routing-machine.css"
import 'leaflet.markercluster/dist/leaflet.markercluster.js'
import 'leaflet-routing-machine'
import 'leaflet-control-geocoder'
import 'leaflet-control-geocoder/dist/Control.Geocoder.css'
import { locationTypes } from './Constants';


const MAP_CENTER: Leaflet.LatLngExpression = [52.520008, 13.404954];  // Center of berlin
const MAP_ZOOM = 13;
const MAP_TILES_URL_TEMPLATE = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const MAP_TILES_LAYER_OPTIONS: Leaflet.TileLayerOptions = {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    minZoom: 5,
}
const MAP_OSRM_URL = "https://routing.openstreetmap.de/routed-foot/route/v1"
const FORCE_SHOW_ROUTE_AFTER_MS = 5000


type LocationTypeEntry = {
    status: "unchecked" | "loading" | "loaded",
    setStatus: (status: "unchecked" | "loading" | "loaded") => void,
    locations: Location[],
    setLocations: (locations: Location[]) => void,
    mapLayer: Leaflet.LayerGroup,
}

type GlobalMapEntries = {
    map: Leaflet.Map,
    mapClusterLayer: Leaflet.LayerGroup,
    mapDiv: HTMLDivElement,
    mapRoutingControl: Leaflet.Routing.Control,
    mapRoutingPlan: Leaflet.Routing.Plan,
}

type IStoreContext = Record<LocationType, LocationTypeEntry> & GlobalMapEntries & {
    currentLocation: Leaflet.LatLng | null,
    routeStatus: RouteStatus,
    setRouteStatus: (status: RouteStatus) => void,
}


const StoreDefaults: IStoreContext = {
    ...Object.fromEntries(locationTypes.map((locationType): [LocationType, LocationTypeEntry] => [locationType, {
        status: "loading",
        setStatus: () => {},
        locations: [],
        setLocations: () => {},
        mapLayer: Leaflet.layerGroup(),
    }])) as unknown as Record<LocationType, LocationTypeEntry>,
    ...createGlobalMapEntries(),
    currentLocation: null,
    routeStatus: "no-route",
    setRouteStatus: () => {},
}


export const StoreContext = createContext<IStoreContext>(StoreDefaults);


export default function Store ({children}: {children: React.ReactNode | React.ReactNode[]}) {
    const [routeStatus, setRouteStatus] = useState<RouteStatus>(StoreDefaults.routeStatus)

    let store: IStoreContext = {
        ...StoreDefaults,
        routeStatus,
        setRouteStatus,
    }

    store = {
        ...store,
        "defibrillator": useLocationTypeEntry(store, "defibrillator"),
        "drinking_fountain": useLocationTypeEntry(store, "drinking_fountain"),
        "soup_kitchen": useLocationTypeEntry(store, "soup_kitchen"),
        "toilet": useLocationTypeEntry(store, "toilet"),
    }

    return <StoreContext.Provider value={store}>{children}</StoreContext.Provider>
}

function useLocationTypeEntry(store: IStoreContext, locationType: LocationType): LocationTypeEntry {
    const defaultEntry = store[locationType]
    const mapLayer = defaultEntry.mapLayer
    
    const [status, setStatus] = useState<"unchecked" | "loading" | "loaded">(defaultEntry.status)
    const [locations, setLocations] = useState<Location[]>(defaultEntry.locations)

    useEffect(() => {
        // TODO: Add error handling
        (async () => {
            const markerIcon = (await getMapIcons())[locationType]

            setStatus("loading")

            const locations = await fetchLocations(locationType)

            setLocations(locations)

            const markers = createMarkersFromLocations(markerIcon, locations)
            const popups = addPopupsToMarkers(markers)
            addMarkersToMapLayer(mapLayer, markers)
            addOnClickEventHandlersToMarkers(store, markers, popups, locations)
            mapLayer.addTo(store.mapClusterLayer)

            setStatus("loaded")
        })();
    }, [])

    useEffect(() => {
        if (status === "unchecked") {
            store.mapClusterLayer.removeLayer(mapLayer)
        } else {
            mapLayer.addTo(store.mapClusterLayer)
        }
    }, [status])

    return {
        status,
        setStatus,
        locations,
        setLocations,
        mapLayer,
    }
}

async function fetchLocations(locationType: LocationType): Promise<Location[]> {
    return (await axios.get<Location[]>(
        `https://mapsential.de/api/filter_locations/${locationType}`
    )).data
}

async function fetchLocationDetails(location: Location): Promise<LocationDetails> {
    return (await axios.get<LocationDetails>(
        `https://mapsential.de/api/details/${location.locationType}/${location.detailsId}`
    )).data
}

function createMarkersFromLocations(markerIcon: Leaflet.Icon, locations: Location[]): Leaflet.Marker[] {
    return locations.map((location) => createMarkerFromLocation(markerIcon, location))
}

function createMarkerFromLocation(markerIcon: Leaflet.Icon, location: Location): Leaflet.Marker {
    return Leaflet.marker([location.latitude, location.longitude], {icon: markerIcon})
}

function addPopupsToMarkers(markers: Leaflet.Marker[]): Leaflet.Popup[] {
    return markers.map(addPopupToMarker)
}

function addPopupToMarker(marker: Leaflet.Marker): Leaflet.Popup {
    const popup = Leaflet.popup()

    marker.bindPopup(popup)

    return popup;
}

function addMarkersToMapLayer(layer: Leaflet.LayerGroup, markers: Leaflet.Marker[]): void {
    markers.forEach((marker) => addMarkerToLayer(layer, marker))
}

function addMarkerToLayer(layer: Leaflet.LayerGroup, marker: Leaflet.Marker): void {
    marker.addTo(layer)
}

function addOnClickEventHandlersToMarkers(
    store: IStoreContext,
    markers: Leaflet.Marker[], 
    popups: Leaflet.Popup[],
    locations: Location[],
): void {
    for (let i = 0; i < markers.length; i++) {
        const marker = markers[i]
        const popup = popups[i]
        const location = locations[i]

        addOnClickEventHandlerToMarker(store, marker, popup, location)
    }
}

function addOnClickEventHandlerToMarker(
    store: IStoreContext,
    marker: Leaflet.Marker,
    popup: Leaflet.Popup,
    location: Location
): void {
    marker.on("click", () => handleMarkerClick(
        store,
        marker,
        popup,
        location,
    ))
}

function handleMarkerClick(
    store: IStoreContext,
    marker: Leaflet.Marker,
    popup: Leaflet.Popup,
    location: Location
): void {
    // TODO: Add error handling
    (async () => {
        const details = await fetchLocationDetails(location)

        const inner: HTMLDivElement = document.createElement('div');
        ReactDOM.render(
            <LocationInformation location={location} details={details} key={location.locationId}/>,
            inner
        );
        (popup as any).setContent(inner.outerHTML)

        createShowRouteButtonClickEventListener(
            store,
            marker,
            popup,
            location,
        )
    })()
}

function createShowRouteButtonClickEventListener(
    store: IStoreContext,
    marker: Leaflet.Marker,
    popup: Leaflet.Popup,
    location: Location,
): void {
    const btnEl = document.getElementById(`locationButton${location.locationId}`) as HTMLElement
    btnEl.addEventListener("click", () => handleShowRouteClick(
        store,
        location,
        marker,
    ))
}

function handleShowRouteClick(
    store: IStoreContext,
    location: Location,
    marker: Leaflet.Marker,
): void {
    if (store.currentLocation === null) {
        store.mapRoutingPlan.spliceWaypoints(
            1,
            store.mapRoutingPlan.getWaypoints().length,
            new Leaflet.Routing.Waypoint(
                new Leaflet.LatLng(location.latitude, location.longitude),
                "",
                {}
            )
        )

        store.mapRoutingControl.addTo(store.map)

        store.setRouteStatus("loaded")

        marker.getPopup()?.remove()

        return
    }

    store.mapRoutingPlan.setWaypoints([
        store.currentLocation,
        new Leaflet.LatLng(location.latitude, location.longitude),
    ])

    store.setRouteStatus("loading")
    store.mapRoutingControl.addTo(store.map)
    store.mapRoutingControl.hide()

    const showRoute = () => {
        store.mapRoutingControl.show()

        store.setRouteStatus("loaded")

        marker.getPopup()?.remove()
    }

    store.mapRoutingControl.on('routesfound', showRoute)
    setTimeout(() => {
        if (store.routeStatus !== "loading") {
            return
        }

        console.warn(
            `Failed to load route within ${FORCE_SHOW_ROUTE_AFTER_MS} milliseconds, attempting to display anyway`
        )
        showRoute()
    }, FORCE_SHOW_ROUTE_AFTER_MS)
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
