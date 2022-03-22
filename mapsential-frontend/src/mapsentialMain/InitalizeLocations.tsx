import Leaflet from "leaflet";
import 'leaflet-control-geocoder';
import 'leaflet-control-geocoder/dist/Control.Geocoder.css';
import "leaflet-routing-machine";
import "leaflet-routing-machine/dist/leaflet-routing-machine.css";
import 'leaflet.markercluster/dist/leaflet.markercluster.js';
import ReactDOM from "react-dom";
import { fetchLocationDetails, fetchLocations } from './Controllers';
import LocationInformation from "./LocationInformation";
import { createLeafletMarkerIcon } from "./MapIcons";
import { StoreContext } from "./Store";
import { Location, LocationsResponse, LocationsResponseTypeEntry, LocationTypeEntries } from "./Types";


const FORCE_SHOW_ROUTE_AFTER_MS = 5000


export default function initializeLocationTypes(store: StoreContext): void {
    initializeLocationsPromise(store).catch((err) => {
        // TODO: Inform user of error
        store.setLocationsStatus("failed");
        console.error(`Could not load locations: ${err}`);
    })
}

async function initializeLocationsPromise(store: StoreContext): Promise<void> {
    const locationsResponse: LocationsResponse = await fetchLocations()

    const locationTypes = Object.keys(locationsResponse)

    const initialized: LocationTypeEntries = {};

    for (let i = 0; i < locationTypes.length; i++) {
        const locationType = locationTypes[i]
        const responseEntry = locationsResponse[locationType]

        const locations = getLocationsFromResponseEntry(locationType, responseEntry)

        const mapLayer = await createMapLayer(
            store, 
            locationType, 
            locations,
            responseEntry.color,
        )

        initialized[locationType] = {
            locations,
            mapLayer,
            isDisplayingMapLayer: true,
            translations: responseEntry.trans,
            cssColor: responseEntry.color,
        }

        store.mapClusterLayer.addLayer(mapLayer);
    }

    store.setLocationTypes(initialized)
    store.setLocationsStatus("loaded")
}

function getLocationsFromResponseEntry(
    type: string,
    responseEntry: LocationsResponseTypeEntry
): Location[] {
    const locations: Location[] = []

    for (let i = 0; i < responseEntry.id.length; i++) {
        locations.push({
            id: responseEntry.id[i],
            type,
            detailsId: responseEntry.did[i],
            latitude: responseEntry.lat[i],
            longitude: responseEntry.lon[i],
        })
    }

    return locations
}

async function createMapLayer(
    store: StoreContext,
    locationType: string,
    locations: Location[],
    markerCssColor: string,
): Promise<Leaflet.LayerGroup> {
    const mapLayer = Leaflet.layerGroup()

    // TODO: Remove LocationType type
    const markerIcon = createLeafletMarkerIcon(markerCssColor)

    const markers = createMarkersForType(markerIcon, locations)
    const popups = addPopupsToMarkers(markers)
    addMarkersToMapLayer(mapLayer, markers)
    addOnClickEventHandlersToMarkers(store, markers, popups, locations)

    return mapLayer
}

function createMarkersForType(
    markerIcon: Leaflet.DivIcon, 
    locations: Location[],
): Leaflet.Marker[] {
    return locations.map((location) => createMarkerFromLocation(markerIcon, location))
}

function createMarkerFromLocation(markerIcon: Leaflet.DivIcon, location: Location): Leaflet.Marker {
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
    store: StoreContext,
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
    store: StoreContext,
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
    store: StoreContext,
    marker: Leaflet.Marker,
    popup: Leaflet.Popup,
    location: Location
): void {
    // TODO: Add error handling
    (async () => {
        const details = await fetchLocationDetails(location)

        const inner: HTMLDivElement = document.createElement('div');
        ReactDOM.render(
            <LocationInformation location={location} details={details} key={location.id} />,
            inner
        );
        (popup as any).setContent(inner.outerHTML)

        createShowRouteButtonClickEventListener(
            store,
            marker,
            location,
        )
        createCommentsButtonClickEventListener(store, location)
    })()
}

function createShowRouteButtonClickEventListener(
    store: StoreContext,
    marker: Leaflet.Marker,
    location: Location,
): void {
    const btnEl = document.getElementById(`locationButton${location.id}`) as HTMLElement
    btnEl.addEventListener("click", () => handleShowRouteClick(
        store,
        location,
        marker,
    ))
}

function createCommentsButtonClickEventListener(
    store: StoreContext,
    location: Location,
): void {
    const btnEl =  document.getElementById(`commentButton:${location.id}`) as HTMLElement
    btnEl.addEventListener("click", () => {
        store.setCurrentCommentLocation(location)
        store.setCommentsAreOpen(true)
    })
}

function handleShowRouteClick(
    store: StoreContext,
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