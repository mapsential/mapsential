import { useContext, useEffect } from 'react';
import initializeLocationTypes from './InitalizeLocations';
import "./MapLeaflet.css";
import RemoveRouteButton from './RemoveRouteButton';
import { StoreContext } from "./Store";

export default function MapLeaflet(){
    const store = useContext(StoreContext)

    useEffect(() => initializeLocationTypes(store), [])

    return <div style={{}} ref={(el) => {
        if (el !== null) {
            el.appendChild(store.mapDiv);
            store.map.invalidateSize();
        }
    }}>
        {store.routeStatus === "loaded" && <RemoveRouteButton className='remove-route-btn' />}
    </div>;
}