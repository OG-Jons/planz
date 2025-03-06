export interface Plant {
    id: number
    name: string
    species: string
    stats: Stat[]
}

export interface Stat {
    id: number
    humidity_score: number
    sunlight_score: number
    timestamp: string
    plant_id: number
}