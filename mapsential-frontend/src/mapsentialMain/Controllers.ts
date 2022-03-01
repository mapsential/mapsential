import axios, { AxiosError, AxiosInstance } from "axios"
import { Location, LocationDetails, LocationType } from "./Types"

// TODO: Load urls from .env file
const APIAxiosInstance = axios.create({
    baseURL: process.env.REACT_APP_IS_DOCKER_DEV === "true" ? "http://127.0.0.1:8080/api/" : "https://mapsential.de/api/",
})

export async function fetchLocations(locationType: LocationType): Promise<Location[]> {
    return await fetch(`filter_locations/${locationType}`, APIAxiosInstance)
}

export async function fetchLocationDetails(location: Location): Promise<LocationDetails> {
    return await fetch(`details/${location.locationType}/${location.detailsId}`, APIAxiosInstance)
}

export async function fetchTips(): Promise<string[]> {
    return (await fetch<{tips: string[]}>("tips/tips.json")).tips
}

async function fetch<T>(
    url: string, 
    axiosInstance: AxiosInstance | null = null,
    backoff: number = 10, 
    maxBackoff: number = 1000, 
    retries: number = 10
): Promise<T> {
    try {
        const res = await (axiosInstance || axios).get(url)   

        console.log(res.status)

        if (res.status < 300) {
            return res.data;
        }

        throw new Error(`Unexpected status code ${res.status}!`)
    } catch (err) {
        if (axios.isAxiosError(err)) {
            if (retries <= 0) {
                throw err
            }

            await delay(backoff)

            const nextBackoff = Math.min(2 * backoff, maxBackoff)

            return await fetch(url, axiosInstance, nextBackoff, maxBackoff, retries - 1)
        }

        throw err
    }
}

function delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(() => resolve(), ms))
}