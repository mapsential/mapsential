import React from 'react'
import {Box} from "@mui/material";
import {Markerprops} from "./Marker";

export default function MarkerDescription(props: Markerprops) {

    return (
        <Box>
            <p>Hier werden noch Informatidonen angefügt</p>
            <p>lat: {props.lat} <b/> lng:{props.lng}</p>
        </Box>
    )
}