import { useContext } from "react";
import Button from "@mui/material/Button";
import { StoreContext } from "./Store";

export default function RemoveRouteButton({className}: {className: string}): JSX.Element | null {
    const store = useContext(StoreContext)

    const handleClickRemoveRoute = () => {
        store.mapRoutingPlan.setWaypoints([])
        if (store.mapRoutingControl instanceof Promise) {
            store.mapRoutingControl.then((mapRoutingControl) => {
                mapRoutingControl.remove()
                store.setRouteStatus("no-route")
            })
        } else {
            store.mapRoutingControl.remove()
            store.setRouteStatus("no-route")
        }
    }

    return <Button
        className={className}
        variant="contained"
        onClick={handleClickRemoveRoute}
    >Route löschen</Button>
}