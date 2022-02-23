import React, {createContext, useEffect, useState} from 'react'
import axios, {AxiosError} from "axios";
import {Location, LocationDetails, locationList, LocationType, RouteStatus} from "./Types";
import {storeContextDefault, IStoreContext} from "./Defaults";
import Leaflet from "leaflet";
import {getMapIcons} from "./MapIcons";
import ReactDOM from "react-dom";
import LocationInformation from "./LoctionInformation";
import "leaflet-routing-machine"
import "leaflet-routing-machine/dist/leaflet-routing-machine.css"


const FORCE_SHOW_ROUTE_AFTER_MS = 5000


export const StoreContext = createContext<IStoreContext>(storeContextDefault);

export default function Store ({children}: {children: React.ReactNode | React.ReactNode[]}) {
    const [drinking_fountain_checkbox,setDrinking_Fountain_checkbox] = useState<boolean>(true)
    const [soup_Kitchen_checkbox,setSoup_Kitchen_checkbox] = useState<boolean>(true)
    const [toilet_checkbox,setToilet_checkbox] = useState<boolean>(true)
    const [defibrillator_checkbox,setDefibrillator_checkbox] = useState<boolean>(true)

    const [drinking_fountain_locations, setDrinking_Fountain_locations] = useState<Location[]>([])
    const [soup_Kitchen_locations, setSoup_Kitchen_locations] = useState<Location[]>([])
    const [toilet_locations, setToilet_locations] = useState<Location[]>([])
    const [defibrillator_locations, setDefibrillator_locations] = useState<Location[]>([])
    
    const [routeStatus, setRouteStatus] = useState<RouteStatus>("no-route")

    const store: IStoreContext = {
        ...storeContextDefault,
        checkboxes: {
            drinking_fountain_checkbox,
            setDrinking_Fountain_checkbox,
            soup_Kitchen_checkbox,
            setSoup_Kitchen_checkbox,
            toilet_checkbox,setToilet_checkbox,
            defibrillator_checkbox,
            setDefibrillator_checkbox
        },
        locations: {
            drinking_fountain_locations,
            setDrinking_Fountain_locations,
            soup_Kitchen_locations,
            setSoup_Kitchen_locations,
            toilet_locations,
            setToilet_locations,
            defibrillator_locations,
            setDefibrillator_locations
        },
        routeStatus,
        setRouteStatus,
    }

    async function addMapLocationsLayer(locationsType: LocationType, locations: locationList) {
        const mapIcons = await getMapIcons()

        const layer = Leaflet.layerGroup();
        for (const location of locations) {
            const marker = Leaflet.marker([location.latitude, location.longitude], {
                icon: mapIcons[location.locationType],
            });
            marker.on('click', (event) => {
                const popup = event.target.getPopup();

                new Promise(async () => {
                    const details: LocationDetails = (await axios.get(
                        `https://mapsential.de/api/details/${location.locationType}/${location.detailsId}`
                    )).data;

                    const inner: HTMLDivElement = document.createElement('div');
                    ReactDOM.render(
                        <LocationInformation location={location} details={details} key={location.locationId}/>,
                        inner
                    );
                    popup.setContent(inner.outerHTML);

                    const onShowRoute = (location: Location) => {
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

                            setRouteStatus("loaded")

                            marker.getPopup()?.remove()

                            return
                        }

                        store.mapRoutingPlan.setWaypoints([
                            store.currentLocation,
                            new Leaflet.LatLng(location.latitude, location.longitude),
                        ])

                        setRouteStatus("loading")
                        store.mapRoutingControl.addTo(store.map)
                        store.mapRoutingControl.hide()

                        const showRoute = () => {
                            store.mapRoutingControl.show()

                            setRouteStatus("loaded")

                            marker.getPopup()?.remove()
                        }

                        store.mapRoutingControl.on('routesfound', showRoute)
                        setTimeout(() => {
                            if (routeStatus !== "loading") {
                                return
                            }

                            console.warn(
                                `Failed to load route within ${FORCE_SHOW_ROUTE_AFTER_MS} milliseconds, attempting to display anyway`
                            )
                            showRoute()
                        }, FORCE_SHOW_ROUTE_AFTER_MS)
                    }

                    (
                        document.getElementById(`locationButton${location.locationId}`) as HTMLElement
                    ).addEventListener(
                        'click',
                        () => onShowRoute(location),
                    )
                }).catch((error: AxiosError) => console.error(error))
            });
            marker.bindPopup(Leaflet.popup());
            marker.addTo(layer);
        }

        store.mapLayers[locationsType] = layer;
    }

    function updateMapRenderedLocationTypes(layersRenderStatusUpdate: Partial<Record<LocationType, boolean>>) {
        for (const [locationType, newRenderStatus] of Object.entries<boolean>(layersRenderStatusUpdate)) {
            const currentRenderStatus = store.mapLayersRenderStatus[locationType as LocationType]
            if (newRenderStatus === currentRenderStatus) {
                continue;
            }

            const layer = store.mapLayers[locationType as LocationType]
            if (typeof layer === "undefined") {
                console.error(`No layer for location type ${locationType}`);
                return;
            }

            if (newRenderStatus === true) {
                store.mapClusterLayer.addLayer(layer)
                store.mapLayersRenderStatus[locationType as LocationType] = true;
            } else {
                store.mapClusterLayer.removeLayer(layer)
                store.mapLayersRenderStatus[locationType as LocationType] = false;
            }
        }
    }

    useEffect(() => {
        store.map.on('locationfound', (e) => {
            store.currentLocation = e.latlng
        })

        store.map.on('locationerror', (err) => {
            console.error(`Could not find location: ${err}`)
        })

        store.map.locate({watch: true})

        const initializeLocationTypeFromRequest = async (
            [locationType, setLocations]: [LocationType, (locations: Location[]) => void],
        ) => {
            const locations = (await axios.get(
                `https://mapsential.de/api/filter_locations/${locationType}`
            )).data;

            setLocations(locations)
            await addMapLocationsLayer(locationType, locations)
            updateMapRenderedLocationTypes({[locationType]: true})
        }

        Promise.all(([
            ['defibrillator', store.locations.setDefibrillator_locations],
            ['drinking_fountain', store.locations.setDrinking_Fountain_locations],
            ['soup_kitchen', store.locations.setSoup_Kitchen_locations],
            ['toilet', store.locations.setToilet_locations],
        ] as [LocationType, (locations: Location[]) => void][]).map(
            (args) => initializeLocationTypeFromRequest(args)
        )).catch((error: AxiosError) => console.error(error));
    }, [])

    useEffect(() => {
        updateMapRenderedLocationTypes({
            "defibrillator": store.checkboxes.defibrillator_checkbox,
            "drinking_fountain": store.checkboxes.drinking_fountain_checkbox,
            "soup_kitchen": store.checkboxes.soup_Kitchen_checkbox,
            "toilet": store.checkboxes.toilet_checkbox,
        })
    }, [
        store.checkboxes.defibrillator_checkbox,
        store.checkboxes.drinking_fountain_checkbox,
        store.checkboxes.soup_Kitchen_checkbox,
        store.checkboxes.toilet_checkbox,
    ])

    return <StoreContext.Provider value={store}>{children}</StoreContext.Provider>
}
