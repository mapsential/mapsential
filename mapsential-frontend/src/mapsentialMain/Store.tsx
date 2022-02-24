import React, {createContext, useEffect, useState} from 'react'
import axios, {AxiosError} from "axios";
import {Location, LocationDetails, locationList, LocationType, CommentList} from "./Types";
import {storeContextDefault, IStoreContext} from "./Defaults";
import Leaflet from "leaflet";
import {getMapIcons} from "./MapIcons";
import ReactDOM from "react-dom";
import LocationInformation from "./LoctionInformation";
import 'leaflet-routing-machine';
import {Dialog} from "@mui/material";

let polyline = require('polyline')

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
    const [currentRoutingControl, setCurrentRoutingControl] = useState<Leaflet.Routing.Control | null>(null)

    const [commentDialogOpen,setCommentDialogOpen] = useState<boolean>(false)
    const [currentComments, setCurrentComments] = useState<number>(0)

    const commentMap = new Map<number, CommentList>()

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
        currentRoutingControl,
        setCurrentRoutingControl,
        commentDialogOpen,
        setCommentDialogOpen,
        currentComments,
        setCurrentComments,
        commentMap
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

                    const onShowRoute = (location: Location, currentLocation: Leaflet.LatLng) => {
                        if (store.currentRoutingControl !== null) {
                            store.map.removeControl(store.currentRoutingControl)
                        }

                        setCurrentRoutingControl(null)

                        const leafletDestinationLocation = new Leaflet.LatLng(location.latitude, location.longitude)

                        console.log(process.env.REACT_APP_MAP_BOX_API_TOKEN)

                        const routingControl = (Leaflet.Routing as any).control({
                            waypoints: [
                                currentLocation,
                                leafletDestinationLocation,
                            ],
                            router:  Leaflet.Routing.mapbox(process.env.REACT_APP_MAP_BOX_API_TOKEN as string,{
                                profile: "mapbox/walking",
                                language: "de"
                            }),
                            lineOptions: {
                                addWaypoints: false,
                            },
                            createMarker: function(i: any, waypoint: any, n:any){
                                return null
                            }
                        })
                        routingControl.addTo(store.map)
                        setCurrentRoutingControl(routingControl)
                        store.currentRoutingControl = routingControl
                    }

                    (
                        document.getElementById(`locationButton${location.locationId}`) as HTMLElement
                    ).addEventListener(
                        'click',
                        () => {
                            if (store.currentRoutingControl !== null) {
                                store.map.removeControl(store.currentRoutingControl);
                            }
                            store.currentRoutingControl = null;
                            onShowRoute(location, store.currentLocation as unknown as Leaflet.LatLng)}
                    );

                    (
                        document.getElementById(`commentButton:${location.locationId}`) as HTMLElement
                    ).addEventListener(
                        'click',
                        () => {
                            setCommentDialogOpen(true)
                            setCurrentComments(5)
                            setTimeout(() => {console.log(currentComments);}, 1000)
                            getComments(location.locationId)
                        }
                    )

                }).catch((error: AxiosError) => console.error(error))
            });
            marker.bindPopup(Leaflet.popup());
            marker.addTo(layer);
        }

        store.mapLayers[locationsType] = layer;
    }

    function getComments(locationId: number){
        if(!commentMap.has(locationId)){
            if(locationId % 4 === 0){
                commentMap.set(locationId, [{
                    timestamp: "0",
                    content: "Kommentar 0",
                    authorName: "Tester 0",
                    detailsId: locationId,
                    commentId: 0,
                }])

            }
            if(locationId % 4 === 1){
                commentMap.set(locationId, [{
                    timestamp: "1",
                    content: "Kommentar 1",
                    authorName: "Tester 1",
                    detailsId: locationId,
                    commentId: 1,
                }])

            }
            if(locationId % 4 === 2){
                commentMap.set(locationId, [{
                    timestamp: "2",
                    content: "Kommentar 2",
                    authorName: "Tester 2",
                    detailsId: locationId,
                    commentId: 2,
                }])

            }
            if(locationId % 4 === 3){
                commentMap.set(locationId, [{
                    timestamp: "3",
                    content: "Kommentar 3",
                    authorName: "Tester 3",
                    detailsId: locationId,
                    commentId: 3,
                }])

            }
        }
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
