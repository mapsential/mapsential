import React, {useContext} from 'react'
import {StoreContext} from "./Store";
import "./MapLeaflet.css";

export default function MapLeaflet(){
    const store = useContext(StoreContext)

    return <div style={{}} ref={(el) => {
        if (el !== null) {
            el.appendChild(store.mapDiv);
            store.map.invalidateSize();
        }
    }} />;
}