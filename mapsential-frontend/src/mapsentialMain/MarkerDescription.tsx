import React from 'react'
import {Box, Typography} from "@mui/material";
import {Markerprops} from "./Marker";

export default function MarkerDescription(props: Markerprops) {

    return (
        <Box style={{}}>
            <Typography variant="h6">{props.type}</Typography>
            <Typography>{props.name}<br/>{props.adress}</Typography>
        </Box>
    )
}