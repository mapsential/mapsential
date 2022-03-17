// TOOD: Remove!
export type LocationType = "defibrillator" | "drinking_fountain" | "soup_kitchen" | "toilet"

export type Location = {
    id: number,
    type: string,
    detailsId: number,
    latitude: number,
    longitude: number,
}

export type LocationsResponseTypeEntry = {
    id: number[],
    did: number[],
    lat: number[],
    lon: number[],
}

export type LocationsResponse = {
    [locationType: string]: LocationsResponseTypeEntry,
}

export type LocationDetails = {
    name: string,
    address: string,
    operator?:string,
    openingTimes? : string,
    hasFee? : boolean,
    isCustomerOnly? : boolean,
    female? : boolean,
    male? : boolean,
    unisex? : boolean,
    child? : boolean,
    hasSeated? : boolean,
    hasUrinal? : boolean,
    hasSquat? : boolean,
    changeTable? : string,
    wheelchairAccessible? : string
    wheelchairAccessInfo? : string
    hasHandWashing? : boolean,
    hasSoap? : boolean,
    hasHandDisinfectant? : boolean,
    hasHandCreme? : boolean,
    hasHandDrying? : boolean,
    handDryingMethod? : string,
    hasPaper? : boolean,
    hasHotWater ? : boolean,
    hasDrinkingWater ? : boolean,
    soupKitchenInfo? : string
}
export type CommentDetails = {
    commentId: number,
    detailsId: number,
    authorName: string,
    content: string,
    timestamp: string
}

export type CommentList = CommentDetails[]

export type RouteStatus = "no-route" | "loading" | "loaded"