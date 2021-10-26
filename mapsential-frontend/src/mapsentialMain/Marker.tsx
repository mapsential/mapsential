import React, {useState} from 'react'
import {PushPin} from "@mui/icons-material";
import {Box, IconButton, Popover} from "@mui/material";
import MarkerDescription from "./MarkerDescription";

export type Markerprops = {
    name: string
    lat: number
    lng: number
    type: string
    adress: string
}

export default function Marker(text: Markerprops) {
    const [open, setOpen] = useState(false);
    const [currentAnchor, setAnchor] = useState<any>()
    return (
        <Box>
            <IconButton
                onClick={(event) => {
                    setOpen(true)
                    setAnchor(event.currentTarget)
                }
                }
            >
                <PushPin/>
            </IconButton>
            <Popover
                id={'sdfsd'}
                open={open}
                anchorEl={currentAnchor}
                onClose={() => {
                    setOpen(false)
                }
                }
                anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'left',
                }}
            >
                <MarkerDescription lat={text.lat} lng={text.lng} name={text.name} type={text.type} adress={text.adress}/>
            </Popover>
        </Box>
    )
}
