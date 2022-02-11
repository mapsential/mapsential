import React from 'react';
import ReactDOM from 'react-dom';
import 'normalize.css';
import './index.css';
import reportWebVitals from './reportWebVitals';
import MapsentialMain from './mapsentialMain/MapsentialMain';

import 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
import 'leaflet-routing-machine/dist/leaflet-routing-machine.css'

ReactDOM.render(
    <React.StrictMode>
        <MapsentialMain/>
    </React.StrictMode>,
    document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
