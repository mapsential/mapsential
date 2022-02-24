import MapLeaflet from '../mapsentialMain/MapLeaflet'
import {Navbar} from "./Navbar";
import {Box} from '@mui/material'
import Store from "./Store"
import Legend from "./Legend"
import RemoveRouteButton from './RemoveRouteButton';
import CommentDialog from "./CommentDialog";

export default function MapsentialMain() {
    return (
        // Important! Always set the container height explicitly
        <Store>
            <Box maxHeight="100%" height="100%">
                <Navbar />
                <MapLeaflet />
                <Legend />
                <RemoveRouteButton />
                <CommentDialog />
            </Box>
        </Store>
    )
}