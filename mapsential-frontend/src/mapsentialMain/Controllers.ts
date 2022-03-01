import axios from "axios"
import { Location, LocationDetails, LocationType } from "./Types"

// TODO: Load urls from .env file
const APIAxiosInstance = axios.create({
    baseURL: process.env.REACT_APP_IS_DOCKER_DEV === "true" ? "http://127.0.0.1:8080/api/" : "https://mapsential.de/api/",
})

export async function fetchLocations(locationType: LocationType): Promise<Location[]> {
    return (await APIAxiosInstance.get<Location[]>(
        `filter_locations/${locationType}`
    )).data
}

export async function fetchLocationDetails(location: Location): Promise<LocationDetails> {
    return (await APIAxiosInstance.get<LocationDetails>(
        `details/${location.locationType}/${location.detailsId}`
    )).data
}
