import React from 'react';
import ReactDOM from 'react-dom';
import 'normalize.css';
import './index.css';
import reportWebVitals from './reportWebVitals';
import MapsentialMain from "./mapsentialMain/MapsentialMain";


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
