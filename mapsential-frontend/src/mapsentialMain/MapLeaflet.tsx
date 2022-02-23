import React, {useContext} from 'react'
import {StoreContext} from "./Store";
import "./MapLeaflet.css";
import RemoveRouteButton from './RemoveRouteButton';

export default function MapLeaflet(){
    const store = useContext(StoreContext)

    return <div style={{}} ref={(el) => {
        if (el !== null) {
            el.appendChild(store.mapDiv);
            store.map.invalidateSize();
        }
    }}>
        {store.routeStatus === "loaded" && <RemoveRouteButton className='remove-route-btn' />}
    </div>;
}