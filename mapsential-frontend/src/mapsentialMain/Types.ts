import Leaflet from "leaflet";


export type TranslationEntry = {
    singular: string,
    plural: string,
}

export type Translations = {
    [countryCode: string]: TranslationEntry,
}

export type LocationsResponseTypeEntry = {
    id: number[],
    did: number[],
    lat: number[],
    lon: number[],
    trans: Translations,
    color: string,
}

export type LocationsResponse = {
    [locationType: string]: LocationsResponseTypeEntry,
}

export type LocationTypeEntry = {
    locations: Location[],
    isDisplayingMapLayer: boolean,
    mapLayer: Leaflet.LayerGroup,
    translations: Translations,
    cssColor: string,
}

export type LocationTypeEntries = {
    [locationType: string]: LocationTypeEntry,
}

export type Location = {
    id: number,
    type: string,
    detailsId: number,
    latitude: number,
    longitude: number,
}

export type LocationDetails = {
    name?: string,
    operator?: string,
    opening_times?: string,
    
    address: string,
    street?: string,
    district?: string,
    town?: string,
    city?: string,
    state?: string,
    postcode?: string,
    country?: string,
    country_code?: string,

    has_fee?: boolean,
    fee?: number,
    is_customer_only?: boolean,
    
    female?: boolean,
    male?: boolean,
    child?: boolean,
    unisex?: boolean,

    has_seated?: string,
    has_urinal?: string,
    has_squat?: string,

    change_table?: string,

    wheelchair_accessible?: string,
    wheelchair_access_info?: string,

    has_hand_washing?: boolean,
    has_soap?: boolean,
    has_hand_disinfectant?: boolean,
    has_hand_creme?: boolean,
    has_hand_drying?: boolean,
    hand_drying_method?: string,
    has_paper?: boolean,
    has_hot_water?: boolean,
    has_shower?: boolean,
    has_drinking_water?: boolean,

    soup_kitchen_info?: boolean,
}

export type CaptchaResponse = {
    token: string,
    jpeg: string,
}

export type PrePostComment = {
    captcha_token: string,
    captcha_answer: string,
    location_id: number,
    author_name: string,
    content: string,
}

export type Comment = {
    id: number,
    timestamp: string,
} & PrePostComment

export type RouteStatus = "no-route" | "loading" | "loaded"