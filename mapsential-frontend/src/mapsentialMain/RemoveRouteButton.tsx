import { useContext } from "react";
import Button from "@mui/material/Button";
import { StoreContext } from "./Store";
import "./RemoveRouteButton.css"

export default function RemoveRouteButton(): JSX.Element | null {
    const store = useContext(StoreContext)

    const handleClickRemoveRoute = () => {
        if (store.currentRoutingControl !== null) {
            store.map.removeControl(store.currentRoutingControl)
            store.setCurrentRoutingControl(null)
            store.currentRoutingControl = null
        } else {
            console.error(
                "Remove route button should only be clickable while a route is shown"
            )
        }
    }

    if (store.currentRoutingControl === null) {
        return null;
    }

    return <Button
        className="remove-route-btn"
        variant="contained"
        onClick={handleClickRemoveRoute}
    >Route löschen</Button>
}