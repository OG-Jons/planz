export interface Plant {
    id: number
    name: string
    species: string
    image: string
    stats: Stat[]
    soil_wet: number
    soil_dry: number
}

export interface Stat {
    id: number
    humidity_score: number
    sunlight_score: number
    temperature_score: number
    soil_moisture_score: number
    timestamp: string
    plant_id: number
}