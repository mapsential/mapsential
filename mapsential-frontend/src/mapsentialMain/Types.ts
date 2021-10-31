export type LocationInformation = {
    lat: number,
    lng: number,
    name: string,
    type?: string
}

export type locationDetails = {
    locationId: number,
    detailsId: number,
    locationType: string,
    locationName: string,
    locationAddress: string,
    longitude: number,
    latitude: number,
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

export type locationList = {
    locationId: number,
    detailsId: number,
    locationType: string,
    locationName: string,
    locationAddress: string,
    longitude: number,
    latitude: number
}[]