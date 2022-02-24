export type LocationInformation = {
    lat: number,
    lng: number,
    name: string,
    type?: string
}

export type LocationType = "defibrillator" | "drinking_fountain" | "soup_kitchen" | "toilet"

export type Location = {
    locationId: number,
    detailsId: number,
    locationType: LocationType,
    locationName: string,
    locationAddress: string,
    longitude: number,
    latitude: number
}

export type LocationDetails = {
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
    info? : string
}
export type CommentDetails = {
    commentId: number,
    detailsId: number,
    authorName: string,
    content: string,
    timestamp: string
}

export type CommentList = CommentDetails[]
export type locationList = Location[]

export type FilterLocationResponse = {
    data: LocationInformation[],
}